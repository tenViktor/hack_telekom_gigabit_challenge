from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from pathlib import Path
import os
import re
from typing import List


class ScriptGenerator:
    def __init__(self, results_dir: Path):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.results_dir = results_dir

    def validate_generated_script(self, script: str) -> bool:
        """Validate generated script meets requirements"""
        required_patterns = [
            r"results\[\"steps_to_reproduce\"\]\.append",
            r"results\[\"screenshots\"\]\.append",
            r"results\[\"evidence\"\]\.append",
            r"await take_screenshot\(",
        ]
        return all(re.search(pattern, script) for pattern in required_patterns)

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
            "broken_auth": {
                "context": """
Common authentication test points:
- Password reset functionality
- Session handling
- Remember me functionality
- Account lockout
- Registration process
- Token handling

Common authentication tests:
- Brute force attempts
- Password policy bypass
- Session fixation
- Token predictability
- Account enumeration
- Password reset poisoning
""",
                "example": """
        # Test password reset functionality
        await page.goto(f"{TARGET_URL}/forgot-password")
        results["steps_to_reproduce"].append("1. Navigate to password reset page")
        results["screenshots"].append(
            await take_screenshot(page, "password_reset_page", results_dir)
        )
        
        # Test account enumeration
        test_emails = ["admin@example.com", "nonexistent@example.com"]
        for email in test_emails:
            results["steps_to_reproduce"].append(f"2. Testing password reset with: {email}")
            await page.fill('input[type="email"]', email)
            
            # Capture the response time
            start_time = time.time()
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
            response_time = time.time() - start_time
            
            results["screenshots"].append(
                await take_screenshot(page, f"reset_response_{email.split('@')[0]}", results_dir)
            )
            
            # Check for timing differences or revealing messages
            page_content = await page.content()
            if "user found" in page_content.lower() or response_time > 2:
                results["success"] = True
                results["evidence"].append(f"Account enumeration possible with email: {email}")
                results["evidence"].append(f"Response time: {response_time:.2f}s")
""",
            },
            "security_misconfig": {
                "context": """
Common security misconfiguration test points:
- Default credentials
- Error messages
- Directory listing
- Security headers
- Debug/dev endpoints
- Backup files
- Admin interfaces

Common misconfiguration tests:
- Check for verbose errors
- Test default credentials
- Scan for common paths
- Verify security headers
- Check for exposed config files
- Test for debug endpoints
""",
                "example": """
        # Test for common misconfigurations
        sensitive_paths = [
            "/admin",
            "/phpinfo.php",
            "/config",
            "/.env",
            "/backup",
            "/api/debug",
            "/swagger",
            "/actuator"
        ]
        
        for path in sensitive_paths:
            results["steps_to_reproduce"].append(f"1. Testing path: {path}")
            full_url = f"{TARGET_URL}{path}"
            
            response = await page.goto(full_url)
            status = response.status if response else 404
            
            results["screenshots"].append(
                await take_screenshot(page, f"path_test_{path.replace('/', '_')}", results_dir)
            )
            
            # Check response status and content
            if status < 400:
                page_content = await page.content()
                if any(term in page_content.lower() for term in ["admin", "config", "debug", "error"]):
                    results["success"] = True
                    results["evidence"].append(f"Sensitive path accessible: {path}")
                    results["evidence"].append(f"Status code: {status}")
        
        # Test for security headers
        response = await page.goto(TARGET_URL)
        headers = response.headers if response else {}
        required_headers = [
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Strict-Transport-Security",
            "Content-Security-Policy"
        ]
        
        for header in required_headers:
            if header not in headers:
                results["success"] = True
                results["evidence"].append(f"Missing security header: {header}")
""",
            },
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
            model="gpt-4",
            messages=messages,
            temperature=0.2,  # Lower temperature for more focused outputs
            presence_penalty=0.1,  # Slight penalty to avoid repetition
            frequency_penalty=0.1,  # Slight penalty to encourage variety
        )
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI API returned no content")
        return content

    async def generate_with_retry(self, *args, max_retries=3) -> str:
        for attempt in range(max_retries):
            try:
                script = await self.generate_test_script(*args)
                if self.validate_generated_script(script):
                    return script
            except Exception:
                if attempt == max_retries - 1:
                    raise
                continue
        raise ValueError("Failed to generate valid script")
