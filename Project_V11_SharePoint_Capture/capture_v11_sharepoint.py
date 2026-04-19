import pyautogui
import time
import os
import img2pdf
from datetime import datetime

# --- CẤU HÌNH ---
OUTPUT_DIR = "v11_captures"
FINAL_PDF_NAME = "SharePoint_Capture.pdf"
PAGES_TO_CAPTURE = 5
DELAY_BETWEEN_PAGES = 2

def capture_sharepoint():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    print("🚀 Bắt đầu tiến trình cào SharePoint V11...")
    image_paths = []
    
    for i in range(1, PAGES_TO_CAPTURE + 1):
        print(f"📸 Chụp trang {i}...")
        img_path = os.path.join(OUTPUT_DIR, f"page_{i:03d}.png")
        pyautogui.screenshot(img_path)
        image_paths.append(img_path)
        
        # Cuộn sang trang tiếp theo (Giả lập Click hoặc Phím)
        pyautogui.press('pagedown')
        time.sleep(DELAY_BETWEEN_PAGES)

    print("📦 Đóng gói tài liệu...")
    with open(FINAL_PDF_NAME, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    print(f"✅ Hoàn tất! File lưu tại: {FINAL_PDF_NAME}")

if __name__ == "__main__":
    capture_sharepoint()
