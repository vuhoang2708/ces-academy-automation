import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import os
import sys

# Cấu hình encoding cho Console Windows
sys.stdout.reconfigure(encoding='utf-8')

# --- CẤU HÌNH ---
TARGET_WINDOW = "Zalo"
TEMPLATE_FILE = "zalo_download_icon.png"
THRESHOLD = 0.8  # Độ chính xác (0.0 đến 1.0)

def get_window(title):
    try:
        wins = gw.getWindowsWithTitle(title)
        for w in wins:
            if w.title == "Zalo": return w
        for w in wins:
            if title.lower() in w.title.lower() and "antigravity" not in w.title.lower():
                return w
        return None
    except: return None

def find_and_click_icons():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"🔍 Không tìm thấy file mẫu {TEMPLATE_FILE}. Script sẽ dừng lại.")
        return

    win = get_window(TARGET_WINDOW)
    if not win:
        print("❌ Không thấy Zalo!")
        return

    win.activate()
    time.sleep(1)

    left, top, width, height = win.left, win.top, win.width, win.height
    
    # Chỉ quét vùng Chat ở giữa (V4 style)
    scan_left = left + int(width * 0.34)
    scan_right = left + width - 10
    scan_top = top + 120
    scan_bottom = top + height - 125
    
    screenshot = pyautogui.screenshot(region=(scan_left, scan_top, scan_right - scan_left, scan_bottom - scan_top))
    screen_arr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    template = cv2.imread(TEMPLATE_FILE)
    if template is None: return
        
    th, tw = template.shape[:2]
    res = cv2.matchTemplate(screen_arr, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= THRESHOLD)

    detect_count = 0
    clicked_points = []
    
    for pt in zip(*loc[::-1]):
        is_duplicate = False
        for cp in clicked_points:
            if abs(pt[0] - cp[0]) < 25 and abs(pt[1] - cp[1]) < 25:
                is_duplicate = True
                break
        
        if not is_duplicate:
            click_x = scan_left + pt[0] + tw // 2
            click_y = scan_top + pt[1] + th // 2
            
            print(f"🎯 Phát hiện nút Tải về tại: ({click_x}, {click_y})")
            pyautogui.click(click_x, click_y)
            clicked_points.append(pt)
            detect_count += 1
            time.sleep(0.5)

    print(f"✅ Đã thực hiện Click {detect_count} nút Tải về.")

if __name__ == "__main__":
    find_and_click_icons()
