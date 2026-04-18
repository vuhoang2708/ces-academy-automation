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
OUTPUT_DIR = "zalo_pro_captures"
FINAL_PDF_BASE = "Zalo_Chat_Export"
MAX_SCROLLS = 100  # Giới hạn an toàn
SCROLL_DELAY = 1.5  # Thời gian chờ app load tin nhắn (giây)
CROP_CHAT_ONLY = True # Chỉ lấy phần nội dung chat ở giữa

def get_window(title):
    try:
        # Ưu tiên lấy cửa sổ Zalo chính xác, bỏ qua các cửa sổ PDF viewer
        wins = gw.getWindowsWithTitle(title)
        for w in wins:
            if w.title == "Zalo": return w
        for w in wins:
            if title.lower() in w.title.lower() and "antigravity" not in w.title.lower():
                return w
        return None
    except: return None

def capture_and_scroll():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    win = get_window(TARGET_WINDOW)
    if not win:
        print(f"❌ Không tìm thấy cửa sổ: {TARGET_WINDOW}")
        return

    if win.isMinimized:
        win.restore()
    win.activate()
    time.sleep(1)

    left, top, width, height = win.left, win.top, win.width, win.height
    print(f"🎯 Đang nhắm mục tiêu: {win.title} ({width}x{height})")

    # Lấy tiêu điểm tại vùng an toàn (Biên trái vùng chat)
    chat_focus_x = left + int(width * 0.40)
    chat_focus_y = top + int(height * 0.5)
    
    print(f"🎯 Đang lấy tiêu điểm tại vùng biên an toàn (X={chat_focus_x})...")
    pyautogui.click(chat_focus_x, chat_focus_y)
    time.sleep(0.5)

    image_paths = []
    prev_img_data = None
    
    print("\n🚀 Bắt đầu chu trình cuộn và chụp tự động...")
    
    for i in range(1, MAX_SCROLLS + 1):
        print(f"📸 Đang chụp trang {i}...", end="\r")
        
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        
        # Crop lấy vùng chat tinh khiết (V4 - Tight Crop)
        if CROP_CHAT_ONLY:
            c_left = int(width * 0.34)  # Lề trái sạch
            c_right = width - 10        # Lề phải trọn vẹn
            c_top = 120                 
            c_bottom = height - 125    
            screenshot = screenshot.crop((c_left, c_top, c_right, c_bottom))
        
        # Kiểm tra nội dung có thay đổi không (Mắt thần - Bottom Detection)
        current_img_data = screenshot.convert("L").tobytes()
        if prev_img_data:
            diff = ImageChops.difference(screenshot, prev_img)
            stat = ImageStat.Stat(diff)
            if sum(stat.mean) < 1.0: # Không đổi -> Chạm đáy
                print(f"\n🛑 HỆ THỐNG NHẬN DIỆN: Đã chạm đáy cuộc trò chuyện ở trang {i-1}!")
                break
        
        prev_img = screenshot
        prev_img_data = current_img_data
        
        img_path = os.path.join(OUTPUT_DIR, f"page_{i:03d}.png")
        screenshot.save(img_path)
        image_paths.append(img_path)
        
        # Cuộn xuống bằng tổ hợp phím mũi tên
        for _ in range(18):
            pyautogui.press('down')
        time.sleep(SCROLL_DELAY)

    if image_paths:
        timestamp = datetime.now().strftime("%H%M%S")
        pdf_path = f"{FINAL_PDF_BASE}_{timestamp}.pdf"
        print(f"\n📦 Đang đóng gói {len(image_paths)} trang thành PDF...")
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))
        print(f"✅ HOÀN TẤT! File đã lưu tại: {os.path.abspath(pdf_path)}")

if __name__ == "__main__":
    capture_and_scroll()
