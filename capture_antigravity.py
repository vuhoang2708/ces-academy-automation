import asyncio
from playwright.async_api import async_playwright
import os
import img2pdf
from config import VIEWER_CDP_URL, module_output_dir

# --- CẤU HÌNH ---
RUN_DIR = module_output_dir("v10_ces_web_capture")
OUTPUT_FOLDER = RUN_DIR / "screenshots_high_res"
FINAL_PDF = RUN_DIR / "Lam_Chu_ANTIGRAVITY_30_Ngay.pdf"
TOTAL_PAGES = int(os.getenv("CES_V10_TOTAL_PAGES", "81"))
CDP_URL = VIEWER_CDP_URL
VIEWER_URL = "https://academy.cesglobal.com.vn/viewer.html?id=43cc2aaa-7358-436a-a464-5630916f8aa2"
# --- --- ---

async def capture_pages():
    if OUTPUT_FOLDER.exists():
        for f in os.listdir(OUTPUT_FOLDER):
            if f.endswith(".png"):
                os.remove(OUTPUT_FOLDER / f)
    else:
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

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
        test_path = OUTPUT_FOLDER / "page_001.png"
        await page.screenshot(path=str(test_path))
        print(f"🔍 Chụp thử trang 1: {test_path}")

        image_paths = [test_path]
        for i in range(2, TOTAL_PAGES + 1):
            print(f"📸 Trang {i}/{TOTAL_PAGES}")
            await page.keyboard.press("ArrowRight")
            await asyncio.sleep(3)
            file_path = OUTPUT_FOLDER / f"page_{i:03d}.png"
            await page.screenshot(path=str(file_path))
            image_paths.append(file_path)

        print("\n✅ Chụp xong 81 trang!")
        return image_paths

def merge_pdf(image_paths):
    print("📦 Đóng gói PDF...")
    with open(FINAL_PDF, "wb") as f:
        f.write(img2pdf.convert([str(path) for path in image_paths]))
    size_mb = os.path.getsize(FINAL_PDF) / (1024 * 1024)
    print(f"✅ PDF: {FINAL_PDF} ({size_mb:.1f} MB)")

async def run():
    paths = await capture_pages()
    if paths:
        merge_pdf(paths)

if __name__ == "__main__":
    asyncio.run(run())
