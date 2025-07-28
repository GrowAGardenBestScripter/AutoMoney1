import asyncio
from playwright.async_api import async_playwright

LOOTDEST_URL = "https://lootdest.org/s?Quh5zXjp&data=l%2BVS0fBwFTqe3k34ic8jObg%2FV%2FDN6P1SRAO3x2%2BvpntTUJ0oMB%2BMdkA%2FLnEwjpQuwFch8FPVzQ5z1oTefr64Oeg2uHB%2FioklOge%2F25YCgXJUpQRp%2FjgFTAvHygTF9OIkZhMIV4V%2BqsQo4QzsgfGgOGi84OTnAK%2FANHjHjCQVEEDS8t2lxkfEgVB8cRCowy8peJ08aEQujymrUDpTJP6trWrjVMvJtz3gtYBzAdJ5UQzYLw9pK2i8pp6vgy%2FPlaUJ"

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Use headless=False if debugging
        context = await browser.new_context()
        page = await context.new_page()

        while True:
            print("Visiting Lootdest URL...")
            await page.goto(LOOTDEST_URL, timeout=120000)

            # Wait for ad/start button
            print("Looking for ad/start button...")
            try:
                await page.wait_for_selector("button", timeout=15000)
                buttons = await page.query_selector_all("button")
                clicked = False
                for btn in buttons:
                    text = (await btn.inner_text()).lower()
                    if any(trigger in text for trigger in ["discover", "download", "install", "try", "read more"]):
                        await btn.click()
                        print(f"Clicked ad button: {text}")
                        clicked = True
                        break

                if not clicked:
                    print("❌ No ad button found — retrying...")

                # Wait for ad to open
                await asyncio.sleep(3)
                pages = context.pages
                if len(pages) > 1:
                    print("Ad page opened — closing it.")
                    await pages[1].close()

                # Wait for unlock
                print("Waiting 60s for unlock button...")
                await asyncio.sleep(60)

                # Click "Unlock Content"
                unlock_clicked = False
                for btn in await page.query_selector_all("button"):
                    text = (await btn.inner_text()).lower()
                    if "unlock" in text and "content" in text:
                        await btn.click()
                        print("✅ Clicked 'Unlock Content'")
                        unlock_clicked = True
                        break

                if not unlock_clicked:
                    print("⚠️ 'Unlock Content' button not found — skipping.")

            except Exception as e:
                print(f"⚠️ Error: {e}")

            print("🔁 Looping again in 5s...")
            await asyncio.sleep(5)

asyncio.run(run_bot())
gTF9OIkZhMIV4V%2BqsQo4QzsgfGgOGi84OTnAK%2FANHjHjCQVEEDS8t2lxkfEgVB8cRCowy8peJ08aEQujymrUDpTJP6trWrjVMvJtz3gtYBzAdJ5UQzYLw9pK2i8pp6vgy%2FPlaUJ
