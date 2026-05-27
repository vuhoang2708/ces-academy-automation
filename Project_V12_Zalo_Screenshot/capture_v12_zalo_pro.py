import pyautogui
import pygetwindow as gw
import time
import os
from PIL import ImageChops
import img2pdf
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from config import ZALO_CAPTURES_DIR

# Cấu hình encoding cho Console Windows
sys.stdout.reconfigure(encoding='utf-8')

# --- CẤU HÌNH ---
TARGET_WINDOW = "Zalo"
OUTPUT_DIR = "zalo_captures"
FINAL_PDF_BASE = "Zalo_Chat_History"
MAX_SCROLLS = 100  # Đặt tối đa 100 trang, cơ chế duplicate detection sẽ dừng sớm khi hết chat
SCROLL_DELAY = 1.5

def get_window(title):
    wins = gw.getWindowsWithTitle(title)
    for w in wins:
        if w.title == "Zalo": return w
    return None

def capture_v12():
    # Dọn dẹp ảnh cũ trong thư mục output
    output_dir = ZALO_CAPTURES_DIR
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        for path in output_dir.glob("*.png"):
            try:
                path.unlink()
            except OSError as exc:
                print(f"⚠️ Không xóa được ảnh cũ {path}: {exc}")

    win = get_window(TARGET_WINDOW)
    if not win:
        print("❌ Không tìm thấy cửa sổ Zalo. Vui lòng mở Zalo lên.")
        return

    # Khôi phục cửa sổ nếu đang bị thu nhỏ (minimized)
    if win.isMinimized:
        print("ℹ️ Cửa sổ Zalo đang thu nhỏ (minimized). Tiến hành khôi phục (restore)...")
        win.restore()
        time.sleep(1.5)

    win.activate()
    time.sleep(1)

    # Lấy tọa độ thực tế sau khi khôi phục và kích hoạt
    left, top, width, height = win.left, win.top, win.width, win.height

    # Click vào vùng chat (40% width, cách top 200px) để lấy focus cuộn
    click_x = left + int(width * 0.40)
    click_y = top + 200
    print(f"👉 Click focus vào vùng chat tại tọa độ: ({click_x}, {click_y})")
    pyautogui.click(click_x, click_y)
    time.sleep(1)

    image_paths = []
    prev_screenshot = None

    for i in range(1, MAX_SCROLLS + 1):
        img_path = output_dir / f"page_{i:03d}.png"
        screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # Crop logic
        c_left = int(width * 0.34)
        c_right = width - 10
        screenshot = screenshot.crop((c_left, 120, c_right, height - 125))

        # Duplicate detection (Nhận diện ảnh trùng lặp)
        if prev_screenshot is not None:
            diff = ImageChops.difference(screenshot, prev_screenshot)
            if diff.getbbox() is None:
                print(f"⚠️ Phát hiện ảnh trang {i:02d} trùng với trang {i-1:02d}. Dừng chụp sớm!")
                break

        screenshot.save(str(img_path))
        image_paths.append(img_path)
        prev_screenshot = screenshot

        print(f"📸 Đã chụp trang {i:02d}...")

        for _ in range(18): pyautogui.press('down')
        time.sleep(SCROLL_DELAY)

    if image_paths:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = f"{FINAL_PDF_BASE}_{timestamp}.pdf"
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert([str(path) for path in image_paths]))
        print(f"✅ V12 PDF Created: {pdf_path} (Tổng số trang: {len(image_paths)})")
    else:
        print("❌ Không có trang nào được chụp thành công.")

if __name__ == "__main__":
    capture_v12()
