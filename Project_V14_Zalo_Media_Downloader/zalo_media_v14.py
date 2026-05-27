import pyautogui
import pygetwindow as gw
import time
import os
import sys
import cv2
import numpy as np
from datetime import datetime

# Cấu hình encoding cho Console Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# --- CẤU HÌNH ---
TARGET_WINDOW = "Zalo"
OUTPUT_DIR = "zalo_v14_downloads"
TEMP_DIR = "zalo_templates" # Nơi chứa ảnh mẫu các icon

class ZaloV14Downloader:
    def __init__(self):
        if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
        if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)
        self.win = self._get_zalo_window()

    def _get_zalo_window(self):
        print(f"[*] Đang tìm cửa sổ {TARGET_WINDOW}...")
        wins = gw.getWindowsWithTitle(TARGET_WINDOW)
        for w in wins:
            # Lọc chính xác cửa sổ Zalo chính
            if w.title == "Zalo": return w
        return None

    def activate(self):
        if self.win:
            self.win.activate()
            time.sleep(1)
            print("✅ Đã kích hoạt cửa sổ Zalo.")
            return True
        print("❌ Không tìm thấy Zalo. Hãy mở app Zalo lên trước!")
        return False

    def diagnostic_capture(self):
        """Chụp ảnh vùng làm việc để xác định tọa độ các nút i, Media, File."""
        print("[*] Đang chụp ảnh chẩn đoán...")
        left, top, width, height = self.win.left, self.win.top, self.win.width, self.win.height
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        diag_path = os.path.join(TEMP_DIR, "zalo_layout_diag.png")
        screenshot.save(diag_path)
        print(f"📸 Đã lưu ảnh chẩn đoán tại: {diag_path}")
        print("💡 Anh hãy mở ảnh này lên để xem Script đang 'nhìn' Zalo của anh như thế nào.")

    def auto_save_as_dialog(self):
        """Tự động xử lý cửa sổ Save As của Windows (Nhấn Enter)."""
        time.sleep(1)
        # Giả lập nhấn Enter để xác nhận lưu file
        pyautogui.press('enter')
        print("💾 Đã ra lệnh Save file.")
        time.sleep(1)

# --- THI CÔNG ---
def run_v14():
    print("🚀 Project V14 - Zalo Desktop Media Downloader")
    downloader = ZaloV14Downloader()

    if downloader.activate():
        # Bước 1: Chụp ảnh để anh em mình soi tọa độ
        downloader.diagnostic_capture()

        print("\n--- KẾ HOẠCH TIẾP THEO ---")
        print("1. Em đã chụp ảnh layout Zalo của anh.")
        print("2. Anh hãy mở mục 'Thông tin hội thoại' -> 'Ảnh/Video' sẵn trên Zalo.")
        print("3. Ở bước sau, em sẽ dùng OpenCV để 'quét' và tải hàng loạt.")

if __name__ == "__main__":
    run_v14()
