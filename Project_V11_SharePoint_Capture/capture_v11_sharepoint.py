"""V11 SharePoint Capture - Basic Screenshot Extractor.

STATUS: Basic/Skeleton — NOT production-ready.

Limitations (as of 2026-05-27):
- Captures a fixed number of full-screen screenshots via pyautogui.
- Uses PageDown keypress to advance; no CV auto-stop or visual duplicate detection.
- No CSS injection, CDP, or Microsoft toolbar hiding.
- Output path is hardcoded (v11_captures/); not integrated with config.py.
- No run summary JSON.

UAT requirement: must have SharePoint document open and focused in foreground
before running. Script does NOT open or navigate to SharePoint automatically.

To use in production, this module needs: CV-based stop condition, config.py
integration, output to outputs/v11_sharepoint/, and a real UAT session.
"""

import pyautogui
import time
import os
import img2pdf

# --- CẤU HÌNH ---
OUTPUT_DIR = "v11_captures"
FINAL_PDF_NAME = "SharePoint_Capture.pdf"
PAGES_TO_CAPTURE = 5
DELAY_BETWEEN_PAGES = 2


def capture_sharepoint():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("Bắt đầu tiến trình cào SharePoint V11 (basic screenshot mode)...")
    print("CAUTION: Script chụp toàn màn hình. Đảm bảo cửa sổ SharePoint đang focus.")
    image_paths = []

    for i in range(1, PAGES_TO_CAPTURE + 1):
        print(f"Chụp trang {i}/{PAGES_TO_CAPTURE}...")
        img_path = os.path.join(OUTPUT_DIR, f"page_{i:03d}.png")
        pyautogui.screenshot(img_path)
        image_paths.append(img_path)
        pyautogui.press('pagedown')
        time.sleep(DELAY_BETWEEN_PAGES)

    print("Đóng gói tài liệu...")
    with open(FINAL_PDF_NAME, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    print(f"Hoàn tất! File lưu tại: {FINAL_PDF_NAME}")
    print("NOTE: Đây là basic capture. Kiểm tra output thủ công để xác nhận đủ trang.")


if __name__ == "__main__":
    capture_sharepoint()
