# CES Academy Automation Suite

> [!IMPORTANT]
> **[MASTER SPECIFICATION](./MASTER_SPECIFICATION.md)**: Xem toàn bộ kiến trúc giải pháp và khung kỹ thuật tổng quát tại đây.

Bộ công cụ tự động hóa toàn diện giúp trích xuất tài liệu, chụp ảnh màn hình và tải Media từ các nền tảng SharePoint, Zalo và Facebook.

## 📁 Cấu trúc thư mục (New Structure)

### 🚀 [Project V13 - Media Downloader Engine](Project_V13_Media_Downloader/)
*   Tải tập tin và hình ảnh gốc từ Zalo (OpenCV) và Facebook (CDP).
*   *Tài liệu:* `Project_V13_Media_Downloader/TECHNICAL_SPEC_V13.md`

### 📸 [Project V12 - Zalo Screenshot Pro](Project_V12_Zalo_Screenshot/)
*   Chụp ảnh màn hình hội thoại Zalo sạch, ghép PDF tự động.
*   *Script:* `Project_V12_Zalo_Screenshot/capture_v12_zalo_pro.py`

### 📂 [Project V11 - SharePoint PDF Extractor](Project_V11_SharePoint_Capture/)
*   Trích xuất tài liệu PDF từ Microsoft SharePoint/Teams.
*   *Script:* `Project_V11_SharePoint_Capture/capture_v11_sharepoint.py`

---

## 🛠️ Yêu cầu hệ thống (Prerequisites)
- **Python 3.12+ (Portable)**
- **Thư viện:** `pyautogui`, `opencv-python`, `img2pdf`, `mss`, `pygetwindow`, `websockets`, `requests`.

## ⚙️ Cấu hình GitHub
Toàn bộ mã nguồn được duy trì tại repository: `vuhoang2708/ces-academy-automation`.

---
*📍 Re-organized on 19/04/2026 for better workspace management.*
