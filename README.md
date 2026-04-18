# CES Academy Automation Suite

Bộ công cụ tự động hóa toàn diện giúp trích xuất tài liệu, chụp ảnh màn hình và tải Media từ các nền tảng SharePoint, Zalo và Facebook.

## 📋 Tổng quan các phiên bản (Versions)

### 🚀 Project V13 - Media Downloader Engine (Current)
*   **Mục tiêu:** Tải tập tin và hình ảnh gốc thay vì chỉ chụp ảnh màn hình.
*   **Zalo Desktop:** Sử dụng **OpenCV** để nhận diện Icon "Tải về" và tự động click. 
    *   *Script:* `Project_V12_Desktop_Capture/v13_zalo_media_downloader.py`
*   **Facebook Group:** Sử dụng kỹ thuật **CDP (Chrome DevTools Protocol)** để trích xuất Media từ Group kín mà không cần API.
    *   *Script:* `Project_V12_Desktop_Capture/v13_fb_media_downloader.py`

### 📸 Project V12 - Zalo Screenshot Pro
*   **Mục tiêu:** Chụp trọn vẹn lịch sử hội thoại Zalo Desktop thành file PDF siêu sạch.
*   **Tính năng:** 
    *   Tự động cuộn bằng phím điều hướng (Arrow Down).
    *   Cảm biến "Mắt thần" (Image Comparison) để nhận diện điểm dừng hội thoại.
    *   Crop ảnh siêu sát để loại bỏ Menu và Header của Zalo.
*   *Script:* `Project_V12_Desktop_Capture/capture_v12_zalo_pro.py`

### 📂 Project V11 - SharePoint PDF Extractor
*   **Mục tiêu:** Trích xuất nội dung từ trình xem PDF của Microsoft SharePoint/Teams.
*   **Tính năng:** Điều khiển trình duyệt để cuộn và chụp từng trang tài liệu, sau đó đóng gói thành PDF duy nhất.
*   *Script:* `capture_v11_sharepoint.py`

---

## 🛠️ Yêu cầu hệ thống (Prerequisites)
- **Python 3.12+ (Portable)**
- **Thư viện:** `pyautogui`, `opencv-python`, `img2pdf`, `mss`, `pygetwindow`, `websockets`, `requests`.

## ⚙️ Cấu hình GitHub
Toàn bộ mã nguồn được duy trì tại repository: `vuhoang2708/antigravity-sync-data`.

---
*📍 Được cập nhật ngày 18/04/2026 bởi Antigravity Agent.*
