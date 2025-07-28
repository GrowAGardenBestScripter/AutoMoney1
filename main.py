import asyncio
import threading
from flask import Flask
from playwright.async_api import async_playwright

# === Lootdest URL ===
LOOTDEST_URL = "https://lootdest.org/s?Quh5zXjp&data=l%2BVS0fBwFTqe3k34ic8jObg%2FV%2FDN6P1SRAO3x2%2BvpntTUJ0oMB%2BMdkA%2FLnEwjpQuwFch8FPVzQ5z1oTefr64Oeg2uHB%2FioklOge%2F25YCgXJUpQRp%2FjgFTAvHygTF9OIkZhMIV4V%2BqsQo4QzsgfGgOGi84OTnAK%2FANHjHjCQVEEDS8t2lxkfEgVB8cRCowy8peJ08aEQujymrUDpTJP6trWrjVMvJtz3gtYBzAdJ5UQzYLw9pK2i8pp6vgy%2FPlaUJ"

# === Flask App to Keep Service Alive ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running."

# === Bot Logic ===
async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        while True:
            try:
                print("Opening Lootdest page...")
                await page.goto(LOOTDEST_URL, timeout=120000)

                await asyncio.sleep(2)

                # Click the ad
                buttons = await page.query_selector_all("button")
                for btn in buttons:
                    try:
                        text = await btn.inner_text()
                        if any(word in text.lower() for word in ["discover", "download", "install", "try", "read more"]):
                            print("Clicking ad button:", text)
                            await btn.click()
                            break
                    except:
                        continue

                # Close ad tab
                await asyncio.sleep(3)
                if len(context.pages) > 1:
                    await context.pages[1].close()

                # Wait and unlock
                await asyncio.sleep(60)
                for btn in await page.query_selector_all("button"):
                    try:
                        if "unlock" in (await btn.inner_text()).lower():
                            print("Clicking unlock button")
                            await btn.click()
                            break
                    except:
                        continue

            except Exception as e:
                print("Error:", e)

            await asyncio.sleep(5)

# === Start Bot in a Thread ===
def start_bot():
    asyncio.run(run_bot())

threading.Thread(target=start_bot).start()
