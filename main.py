import json
import asyncio
import pandas as pd
from pathlib import Path
import typer
from rich.console import Console
from rich.progress import track
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
from vulnerability_classifier import classify_vulnerability, VulnerabilityType
from exploit_runners import SQLInjectionRunner, XSSRunner

app = typer.Typer()
console = Console()


class VulnerabilityScanner:
    def __init__(self, target_url: str, timeout: int = 5000):
        self.target_url = target_url
        self.timeout = timeout
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)

        # Initialize runners
        self.runners = {
            VulnerabilityType.SQL_INJECTION: SQLInjectionRunner(
                target_url, self.results_dir
            ),
            VulnerabilityType.XSS: XSSRunner(target_url, self.results_dir),
        }

    async def check_site_availability(self) -> tuple[bool, str]:
        console.print(f"Checking if {self.target_url} is accessible...", style="yellow")
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page()
                await page.goto(self.target_url, timeout=self.timeout)
                await browser.close()
                console.print("\n✅ Target site is accessible!", style="green")
                return True, ""
            except PlaywrightTimeoutError:
                error_msg = (
                    f"\n❌ Error: Cannot access {self.target_url}\n"
                    "Please make sure the Docker container is running and the site is accessible."
                )
                await browser.close()
                return False, error_msg
            except Exception as e:
                error_msg = f"\n❌ Error checking site availability: {str(e)}"
                await browser.close()
                return False, error_msg

    async def save_results(self, vulnerability: str, results: dict):
        """
        Save test results in JSON format with metadata
        """
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        result_data = {
            "timestamp": timestamp,
            "vulnerability": vulnerability,
            "target_url": self.target_url,
            "results": results,
        }

        # Save JSON results
        output_file = (
            self.results_dir / f"{timestamp}_{vulnerability.replace(' ', '_')}.json"
        )
        with open(output_file, "w") as f:
            json.dump(result_data, f, indent=2)

        console.print(f"Results saved to {output_file}", style="green")

    async def run_vulnerability_test(self, vulnerability: str, details: str):
        vuln_type, can_use_playwright = classify_vulnerability(vulnerability, details)
        console.print(f"\nClassified as: {vuln_type.value}", style="blue")

        # Get specialized runner if available
        runner = self.runners.get(vuln_type)

        try:
            if runner:
                console.print("Running specialized exploit...", style="yellow")
                results = await runner.run(vulnerability, details)
                await self.save_results(vulnerability, results)
            elif can_use_playwright:
                console.print("Using Playwright for basic testing...", style="yellow")
                results = await self.run_playwright_test(vulnerability, details)
                await self.save_results(vulnerability, results)
            else:
                console.print(
                    "Manual testing required for this vulnerability", style="red"
                )
                await self.save_results(
                    vulnerability,
                    {
                        "status": "manual_testing_required",
                        "reason": "No automated test available for this vulnerability type",
                    },
                )
        except Exception as e:
            console.print(f"Error during test execution: {str(e)}", style="red")
            await self.save_results(vulnerability, {"status": "error", "error": str(e)})

    # async def run_playwright_test(self, vulnerability: str, details: str) -> bool:
    #     async with async_playwright() as p:
    #         browser = await p.chromium.launch(headless=True)
    #         context = await browser.new_context()
    #         page = await context.new_page()
    #
    #         try:
    #             # Take initial screenshot
    #             timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    #             screenshot_path = (
    #                 self.results_dir
    #                 / f"{timestamp}_{vulnerability.replace(' ', '_')}.png"
    #             )
    #
    #             await page.goto(self.target_url)
    #             await page.screenshot(path=str(screenshot_path))
    #
    #             # Store results
    #             with open(
    #                 self.results_dir
    #                 / f"{timestamp}_{vulnerability.replace(' ', '_')}.txt",
    #                 "w",
    #             ) as f:
    #                 f.write(f"Vulnerability: {vulnerability}\nDetails: {details}\n")
    #
    #             console.print(f"✅ Test completed for: {vulnerability}", style="green")
    #             return True
    #
    #         except Exception as e:
    #             console.print(
    #                 f"❌ Error testing {vulnerability}: {str(e)}", style="red"
    #             )
    #             return False
    #         finally:
    #             await context.close()
    #             await browser.close()
    #

    async def run_playwright_test(self, vulnerability: str, details: str):
        """
        Basic Playwright-based testing for general vulnerabilities
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")

                # Navigate to target URL
                await page.goto(self.target_url)

                # Take screenshot
                screenshot_path = (
                    self.results_dir
                    / f"{timestamp}_{vulnerability.replace(' ', '_')}.png"
                )
                await page.screenshot(path=str(screenshot_path))

                # Get page console logs
                console_messages = []
                page.on("console", lambda msg: console_messages.append(msg.text))

                # Basic interaction simulation
                await page.wait_for_load_state("networkidle")

                return {
                    "status": "completed",
                    "screenshot": str(screenshot_path),
                    "console_logs": console_messages,
                    "url": page.url,
                    "content_length": len(await page.content()),
                }

            finally:
                await context.close()
                await browser.close()


@app.command()
def scan(
    target_url: str = typer.Argument(..., help="Target URL to scan"),
    csv_path: str = typer.Argument(..., help="Path to vulnerabilities CSV file"),
):
    """
    Run automated vulnerability scanning based on CSV input
    """

    async def run_scan():
        scanner = VulnerabilityScanner(target_url)

        is_available, error_msg = await scanner.check_site_availability()
        if not is_available:
            console.print(error_msg, style="red")
            return  # Exit gracefully without raising an exception

        df = pd.read_csv(csv_path)
        console.print(f"\nFound {len(df)} vulnerabilities to test", style="blue")

        for _, row in track(
            df.iterrows(), total=len(df), description="Running tests..."
        ):
            await scanner.run_vulnerability_test(
                str(row["Vulnerability"]), str(row["Details"])
            )

    asyncio.run(run_scan())


if __name__ == "__main__":
    app()
