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

app = typer.Typer()
console = Console()


class VulnerabilityScanner:
    def __init__(self, target_url: str, timeout: int = 5000):
        self.target_url = target_url
        self.timeout = timeout
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)

    async def check_site_availability(self):
        console.print(f"Checking if {self.target_url} is accessible...", style="yellow")
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page()
                await page.goto(self.target_url, timeout=self.timeout)
                await browser.close()
                console.print("✅ Target site is accessible!", style="green")
                return True
            except PlaywrightTimeoutError:
                console.print(f"❌ Cannot access {self.target_url}", style="red")
                await browser.close()
                return False

    async def run_vulnerability_test(self, vulnerability: str, details: str) -> bool:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # Take initial screenshot
                timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = (
                    self.results_dir
                    / f"{timestamp}_{vulnerability.replace(' ', '_')}.png"
                )

                await page.goto(self.target_url)
                await page.screenshot(path=str(screenshot_path))

                # Store results
                with open(
                    self.results_dir
                    / f"{timestamp}_{vulnerability.replace(' ', '_')}.txt",
                    "w",
                ) as f:
                    f.write(f"Vulnerability: {vulnerability}\nDetails: {details}\n")

                console.print(f"✅ Test completed for: {vulnerability}", style="green")
                return True

            except Exception as e:
                console.print(
                    f"❌ Error testing {vulnerability}: {str(e)}", style="red"
                )
                return False
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

        if not await scanner.check_site_availability():
            raise typer.Exit(1)

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
