import pyautogui
import pygetwindow as gw
import time
import os
from PIL import Image, ImageChops, ImageStat
import img2pdf
from datetime import datetime
import sys

# Cấu hình encoding cho Console Windows
sys.stdout.reconfigure(encoding='utf-8')

# --- CẤU HÌNH ---
TARGET_WINDOW = "Zalo"
OUTPUT_DIR = "zalo_captures"
FINAL_PDF_BASE = "Zalo_Chat_History"
MAX_SCROLLS = 100
SCROLL_DELAY = 1.5

def get_window(title):
    wins = gw.getWindowsWithTitle(title)
    for w in wins:
        if w.title == "Zalo": return w
    return None

def capture_v12():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    win = get_window(TARGET_WINDOW)
    if not win: return

    win.activate()
    time.sleep(1)

    left, top, width, height = win.left, win.top, win.width, win.height
    image_paths = []
    
    for i in range(1, MAX_SCROLLS + 1):
        img_path = os.path.join(OUTPUT_DIR, f"page_{i:03d}.png")
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        
        # Crop logic
        c_left = int(width * 0.34)
        c_right = width - 10
        screenshot = screenshot.crop((c_left, 120, c_right, height - 125))
        
        screenshot.save(img_path)
        image_paths.append(img_path)
        
        for _ in range(18): pyautogui.press('down')
        time.sleep(SCROLL_DELAY)

    if image_paths:
        timestamp = datetime.now().strftime("%Y%M%D_%H%M%S")
        pdf_path = f"{FINAL_PDF_BASE}_{timestamp}.pdf"
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))
        print(f"✅ V12 PDF Created: {pdf_path}")

if __name__ == "__main__":
    capture_v12()
