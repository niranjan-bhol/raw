import asyncio
from playwright.async_api import async_playwright
import os

async def download_excel_from_hkex(url: str, download_path: str = "."):
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)

            await page.wait_for_selector("text=Export to Excel", timeout=60000)
            download_button = page.get_by_text("Export to Excel").first

            async with page.expect_download() as download_info:
                await download_button.click(timeout=60000)

            download = await download_info.value
            file_name = download.suggested_filename
            file_path = os.path.join(download_path, file_name)
            await download.save_as(file_path)

            print(f"Excel file downloaded successfully to: {file_path}")

            await browser.close()

    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    hkex_url = "https://www.hkex.com.hk/Market-Data/Futures-and-Options-Prices/Foreign-Exchange/UIN---INR_USD-Futures?sc_lang=en#&product=UIN"
    download_directory = "downloads"
    os.makedirs(download_directory, exist_ok=True)
    await download_excel_from_hkex(hkex_url, download_directory)

if __name__ == "__main__":
    asyncio.run(main())