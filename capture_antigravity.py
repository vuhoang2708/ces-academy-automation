import asyncio
from playwright.async_api import async_playwright
import os
import img2pdf

# --- CẤU HÌNH ---
OUTPUT_FOLDER = r"g:\My Drive\antigravity\ces-academy-automation\screenshots_high_res"
FINAL_PDF = r"g:\My Drive\antigravity\ces-academy-automation\Lam_Chu_ANTIGRAVITY_30_Ngay.pdf"
TOTAL_PAGES = 81
CDP_URL = "http://localhost:9333"
VIEWER_URL = "https://academy.cesglobal.com.vn/viewer.html?id=43cc2aaa-7358-436a-a464-5630916f8aa2"
# --- --- ---

async def capture_pages():
    if os.path.exists(OUTPUT_FOLDER):
        for f in os.listdir(OUTPUT_FOLDER):
            if f.endswith(".png"):
                os.remove(os.path.join(OUTPUT_FOLDER, f))
    else:
        os.makedirs(OUTPUT_FOLDER)

    async with async_playwright() as p:
        print("Kết nối vào Chrome...")
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]

        # Vào thẳng viewer
        print("Mở trang giáo trình...")
        await page.goto(VIEWER_URL, wait_until="networkidle")
        await asyncio.sleep(8)
        print(f"URL hiện tại: {page.url}")

        # Kiểm tra xem viewer đã load chưa
        title = await page.title()
        print(f"Tiêu đề: {title}")

        # Chụp thử trang 1 để kiểm tra
        test_path = os.path.join(OUTPUT_FOLDER, "page_001.png")
        await page.screenshot(path=test_path)
        print(f"🔍 Chụp thử trang 1: {test_path}")

        image_paths = [test_path]
        for i in range(2, TOTAL_PAGES + 1):
            print(f"📸 Trang {i}/{TOTAL_PAGES}")
            await page.keyboard.press("ArrowRight")
            await asyncio.sleep(3)
            file_path = os.path.join(OUTPUT_FOLDER, f"page_{i:03d}.png")
            await page.screenshot(path=file_path)
            image_paths.append(file_path)

        print("\n✅ Chụp xong 81 trang!")
        return image_paths

def merge_pdf(image_paths):
    print("📦 Đóng gói PDF...")
    with open(FINAL_PDF, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    size_mb = os.path.getsize(FINAL_PDF) / (1024 * 1024)
    print(f"✅ PDF: {FINAL_PDF} ({size_mb:.1f} MB)")

async def run():
    paths = await capture_pages()
    if paths:
        merge_pdf(paths)

if __name__ == "__main__":
    asyncio.run(run())
