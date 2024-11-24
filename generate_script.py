from openai import OpenAI
import pandas as pd
import asyncio
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
import sys

TARGET_URL = "http://localhost:3000"
TIMEOUT = 5000  # 5 seconds timeout for checking site availability

client = OpenAI()

df = pd.read_csv("juice-shop_vulnerabilities_2024-11-14T1526.csv")


"""
TODO:
- Figure out the vulnerability type - SQL Injections, XSS, Missing Security Headers, Path Traversal
- run the best tool (headless or a Python script)
- Generate script (look into the vector DB)
- Run the script (we need to get screenshots or documentations, where we cannot take them)
- Save the output types based on the vulnerability type (logs, headers, or only the screenshots)
- Generate steps to manually recreate based on the scripts
- Store everything
"""

async def run_test(script_content):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True
        )  # Set to True if you don't want to see the browser
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Create a namespace for the script execution
            namespace = {
                "page": page,
                "TARGET_URL": TARGET_URL,
                "asyncio": asyncio,
                "__builtins__": __builtins__,
            }

            # Compile the script first
            compiled_code = compile(script_content, "<string>", "exec")

            # Execute the compiled code
            exec(compiled_code, namespace)

            # If the script defines a main function, run it
            if "main" in namespace and callable(namespace["main"]):
                main_func = namespace["main"]
                # Call main() and await its result if it's a coroutine
                result = main_func()
                if asyncio.iscoroutine(result):
                    await result
                else:
                    print("Warning: main() function is not async")
            else:
                print("Warning: No main() function found in the generated script")

        except Exception as e:
            print(f"Error executing script: {str(e)}")
            import traceback

            traceback.print_exc()
        finally:
            await context.close()
            await browser.close()


async def check_site_availability():
    print(f"Checking if {TARGET_URL} is accessible...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            page = await browser.new_page()
            await page.goto(TARGET_URL, timeout=TIMEOUT)
            await browser.close()
            print("✅ Target site is accessible!")
            return True
        except PlaywrightTimeoutError:
            print(f"❌ Error: Cannot access {TARGET_URL}")
            print(
                "Please make sure the Docker container is running and the site is accessible."
            )
            await browser.close()
            return False
        except Exception as e:
            print(f"❌ Error checking site availability: {str(e)}")
            await browser.close()
            return False


async def main():
    # Check if the site is accessible before running tests
    is_accessible = await check_site_availability()
    if not is_accessible:
        print("Exiting due to inaccessible target site.")
        sys.exit(1)

    for _, row in df.iterrows():
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You're a pentest generator. Generate only pure Python code WITHOUT any markdown (meaning also without '```python' and '```'), comments, or runtime execution code.
Important rules:
1. DO NOT include asyncio.run() or any event loop handling
2. DO NOT include if __name__ == '__main__' block
3. ONLY define the async main() function and any helper functions needed
4. All Playwright operations must be awaited
5. The page object and TARGET_URL will be provided
6. NO imports needed - they are already provided""",
                },
                {
                    "role": "user",
                    "content": f"""Write a pentest using the python playwright package for the following vulnerability:
Vulnerability: {row['Vulnerability']}
Details: {row['Details']}

Your code will have access to:
- page (Playwright page object)
- TARGET_URL (the target URL string)

ONLY write the async main() function and any helper functions needed.
DO NOT include imports, asyncio.run(), or __main__ block.
Example structure:
async def main():
    await page.goto(TARGET_URL)
    # ... your test code here
""",
                },
            ],
        )

        script_content = completion.choices[0].message.content
        print(f"\nExecuting test for: {row['Vulnerability']}")
        print("-" * 50)
        print(script_content)
        print("-" * 50)

        await run_test(script_content)


if __name__ == "__main__":
    asyncio.run(main())
