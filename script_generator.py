from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from pathlib import Path
import os
from typing import List


class ScriptGenerator:
    def __init__(self, results_dir: Path):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.results_dir = results_dir

    async def generate_test_script(
        self, vulnerability: str, details: str, vuln_type: str
    ) -> str:
        # Base template that includes proper screenshot handling and results structure
        base_template = """
from pathlib import Path
import pandas as pd

async def take_screenshot(page, name: str, results_dir: Path) -> str:
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = results_dir / f"{timestamp}_{name}.png"
    await page.screenshot(path=str(screenshot_path))
    return str(screenshot_path)

async def main():
    results = {
        "success": False,
        "evidence": [],
        "screenshots": [],
        "steps_to_reproduce": [],
        "console_logs": []
    }
    
    # Setup console logging
    page.on("console", lambda msg: results["console_logs"].append(msg.text))
    results_dir = Path("results")
    
    try:
        await page.goto(TARGET_URL)
        results["screenshots"].append(
            await take_screenshot(page, "initial_state", results_dir)
        )
"""

        vuln_specific_prompts = {
            "sql_injection": {
                "context": """
Common SQL injection test points:
- Login forms: email/username fields
- Search functionality: query parameters
- URL parameters: especially IDs and filters
- User registration forms
- Profile update forms

Common SQL injection payloads:
- ' OR '1'='1
- admin' --
- ' UNION SELECT NULL--
- ') OR ('1'='1
- ' OR 1=1;--
""",
                "example": """
        # Test login form
        await page.goto(f"{TARGET_URL}/login")
        results["steps_to_reproduce"].append("1. Navigate to login page")
        results["screenshots"].append(
            await take_screenshot(page, "before_login", results_dir)
        )
        
        payloads = ["' OR '1'='1", "admin' --"]
        for payload in payloads:
            results["steps_to_reproduce"].append(f"2. Try payload: {payload}")
            await page.fill('input[name="email"]', payload)
            await page.fill('input[name="password"]', "any")
            results["screenshots"].append(
                await take_screenshot(page, f"payload_{payload[:10]}", results_dir)
            )
            
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
            
            if "/profile" in page.url or "/account" in page.url:
                results["success"] = True
                results["evidence"].append(f"Login bypass successful with: {payload}")
                results["screenshots"].append(
                    await take_screenshot(page, "success_state", results_dir)
                )
                break
""",
            },
            "xss": {
                "context": """
Common XSS test points:
- Search forms
- Comment fields
- User profile fields
- URL parameters
- File upload names

Common XSS payloads:
- <script>alert(1)</script>
- <img src=x onerror=alert(1)>
- <svg onload=alert(1)>
- javascript:alert(1)
""",
                "example": """
        # Test search functionality
        await page.goto(f"{TARGET_URL}/search")
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>"
        ]
        
        for payload in payloads:
            results["steps_to_reproduce"].append(f"1. Testing search with: {payload}")
            await page.fill('input[type="search"]', payload)
            results["screenshots"].append(
                await take_screenshot(page, f"before_payload_{payload[:10]}", results_dir)
            )
            
            await page.keyboard.press("Enter")
            await page.wait_for_load_state("networkidle")
            
            # Check for XSS success (looking for alerts or script execution)
            dialog_promised = page.wait_for_event("dialog", timeout=3000).catch(lambda: None)
            results["screenshots"].append(
                await take_screenshot(page, f"after_payload_{payload[:10]}", results_dir)
            )
            
            dialog = await dialog_promised
            if dialog:
                results["success"] = True
                results["evidence"].append(f"XSS successful with: {payload}")
                await dialog.dismiss()
""",
            },
        }

        vuln_info = vuln_specific_prompts.get(vuln_type, {"context": "", "example": ""})

        messages: List[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": f"""Generate a Playwright test script that:
1. Uses the provided screenshot function
2. Records all steps in results["steps_to_reproduce"]
3. Adds evidence of successful exploits
4. Takes screenshots at key points

Context for this vulnerability type:
{vuln_info['context']}

Base template and example:
{base_template}
{vuln_info['example']}
""",
            },
            {
                "role": "user",
                "content": f"""
Create a script for:
Vulnerability: {vulnerability}
Details: {details}

Follow the template format and include comprehensive testing. YOU MUST OMIT '```python' AND '```'!!!
End the script with:
        return results
    except Exception as e:
        results["error"] = str(e)
        return results
""",
            },
        ]

        response = self.client.chat.completions.create(
            model="gpt-4", messages=messages, temperature=0.7
        )
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI API returned no content")
        return content
