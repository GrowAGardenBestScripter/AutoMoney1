import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://lootdest.com")

        while True:
            print("Looking for ad button...")
            buttons = await page.query_selector_all("button")
            clicked = False

            for btn in buttons:
                text = await btn.inner_text()
                if any(keyword in text.lower() for keyword in ["discover", "download", "install", "try"]):
                    await btn.click()
                    clicked = True
                    print(f"Clicked: {text}")
                    break

            if not clicked:
                print("No ad button found. Retrying in 10 seconds.")
                await asyncio.sleep(10)
                continue

            await asyncio.sleep(3)

            # Close the ad tab
            if len(context.pages) > 1:
                await context.pages[1].close()
                print("Closed ad tab.")

            print("Waiting 60 seconds...")
            await asyncio.sleep(60)

            # Click Unlock Content
            buttons = await page.query_selector_all("button")
            for btn in buttons:
                text = await btn.inner_text()
                if "unlock content" in text.lower():
                    await btn.click()
                    print("Clicked 'Unlock Content'")
                    break

            await asyncio.sleep(5)

asyncio.run(run_bot())
