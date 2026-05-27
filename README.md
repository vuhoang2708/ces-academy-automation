# CES Academy Automation Suite

> [!IMPORTANT]
> **[MASTER SPECIFICATION](./MASTER_SPECIFICATION.md)**: Xem toàn bộ kiến trúc giải pháp và khung kỹ thuật tổng quát tại đây.
> **[PROJECT STATUS](./PROJECT_STATUS.md)**: Xem trạng thái hiện tại đã đối chiếu với repo thật tại đây.

Bộ công cụ tự động hóa toàn diện giúp trích xuất tài liệu, chụp ảnh màn hình và tải Media từ các nền tảng SharePoint, Zalo và Facebook.

## 📁 Cấu trúc thư mục (New Structure)

### 🚀 [Project V13 - Media Downloader Engine](Project_V13_Media_Downloader/)
*   Facebook CDP downloader đã được harden thêm run summary và kiểm lỗi tải media.
*   V13 Zalo hiện được quarantine vì source cũ corrupt; hướng Zalo media mới nằm ở V14 diagnostic.
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
- **Thư viện:** xem `requirements.txt`.

## 🧠 AI Analysis Và Second Brain
- Mỗi artifact capture/download có thể đi kèm AI sidecar dạng `*_AI_ANALYSIS.md`.
- CLI local-first để tạo sidecar: `analyze_artifact.py`.
- Template phân tích nằm ở `templates/ai_analysis_sidecar_template.md`.
- Kịch bản test Gemini nằm ở `Gemini_Test/GEMINI_TEST_SCRIPT_20260527.md`.
- Raw captures và chat analysis chứa dữ liệu riêng tư mặc định không commit lên GitHub.

## ⚙️ Cấu hình GitHub
Toàn bộ mã nguồn được duy trì tại repository: `vuhoang2708/ces-academy-automation`.

---
*📍 Re-organized on 19/04/2026 for better workspace management.*
