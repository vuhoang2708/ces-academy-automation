# TECHNICAL SPECIFICATION: Antigravity Unified Hub
**Versatility, Scalability, and Intelligence**

## 1. Tầm nhìn chiến lược (Strategic Vision)
Xây dựng một "Siêu ứng dụng" (Umbrella App) đóng vai trò là lớp giao diện và xử lý trung tâm cho tất cả các dự án của anh. Nền tảng này cho phép quản lý chéo giữa các lĩnh vực (Dòng tộc, Học máy, Chứng khoán, Media) mà không làm loãng mã nguồn của từng dự án riêng lẻ.

## 2. Kiến trúc hệ thống (System Architecture)

### 2.1. Lớp giao diện (Frontend Layer)
- **Framework:** Next.js 14+ (App Router).
- **Core Engine:**
    - **Modular Service:** Mỗi dự án là một Module cấu hình độc lập.
    - **Adaptive UI:** Giao diện tự thích ứng dựa trên loại dự án đang truy cập.
- **Design System:** Glassmorphism (Kính mờ), Dark Mode theo chuẩn Premium.

### 2.2. Lớp tích hợp (Integration Layer)
- **Local Integration:** Kết nối với các script Python (V11-V14) thông qua **Hub Server (Python-based Execution Engine)**.
- **Execution Protocol:** Sử dụng `subprocess.Popen` với `CREATE_NEW_CONSOLE` để mở terminal độc lập cho từng version automation.
- **Data Sync:** Cơ chế quét thư mục đệ quy (`sync_hub_data.py`) để đồng bộ trạng thái scrapper vào Hub UI.
- **Cloud Integration:** Kết nối với Vercel (Deployment) và GitHub (Data Sync).
- **AI Brain:** Tích hợp Gemini 3 để phân tích artifacts được quét tự động bởi Hub.

## 3. Cấu trúc dữ liệu "Multi-Project"
Hệ thống sử dụng một file cấu hình duy nhất để quản lý các dự án vệ tinh:

```json
{
  "projects": [
    {
      "id": "clan-hub",
      "name": "Tộc Hoàng Portal",
      "status": "Production",
      "url": "https://dh-crm-landing.vercel.app/",
      "capabilities": ["Gallery", "Genealogy", "Registration"]
    },
    {
      "id": "ces-automation",
      "name": "CES Academy Automation",
      "status": "Development",
      "capabilities": ["PDF_Capture", "CDP_Scraper", "Zalo_Downloader"]
    }
  ]
}
```

## 4. Các tính năng cốt lõi (Core Features)

### A. Project Switcher (Điều phối dự án)
- Một thanh điều hướng thông minh cho phép người dùng chuyển đổi không gian làm việc giữa các mục tiêu khác nhau.

### B. Unified AI Workspace
- Cho phép đặt câu hỏi chéo dữ liệu. Ví dụ: "Dựa trên dữ liệu cào từ Zalo tối qua và file PDF trong SharePoint, hãy tóm tắt nội dung cuộc họp".

### C. Live Monitoring & Launcher Hub
- Theo dõi trạng thái của các script đang chạy local và nút bấm tải về bộ Launcher mới nhất cho từng máy tính.

## 5. Hiện trạng triển khai (Current Implementation Status)
- **Phase 1: Shell Architecture:** Planned/External. Chưa thấy source Next.js trong repo hiện tại.
- **Phase 2: Execution Engine:** Planned. `hub_server.py` chưa có trong repo hiện tại.
- **Phase 3: Data Connector:** Planned. `hub_data.json`/sync engine chưa có trong repo hiện tại.
- **Phase 4: Content Visualization:** Planned. Chưa có implementation trong repo hiện tại.
- **AI Sidecar:** Early P1 scope. Có template và kịch bản Gemini test để phân tích artifact trước khi có full Hub.

## 6. Sơ đồ vận hành (Operational Flow)
1. **User** truy cập Dashboard → 2. **Hub Server** nhận lệnh Launch → 3. **Windows Terminal** chạy automation script → 4. **Script** lưu data vào `ces-academy-automation` → 5. **Sync Engine** cập nhật `hub_data.json` → 6. **Dashboard** hiển thị kết quả Real-time.

---
*📍 Cập nhật 27/05/2026: trạng thái trên đã được chỉnh theo repo hiện tại để tránh spec-code drift.*
