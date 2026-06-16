> **Archive note:** File này là plan cũ ngày 2026-04-19, không còn là nguồn hướng dẫn hiện tại. Xem handoff mới trong `Implementation Plan/Agent Handoff/`. Port `9222` vẫn là default của V13 Facebook nhưng phải đọc từ `config.py` (`FB_CDP_PORT`). Output path cũ `v13_fb_downloads` đã được thay bằng `downloads/v13_facebook/`.

---

# Implementation Plan - UAT V13 Facebook Media Downloader
**Date:** 2026-04-19
**Task:** Tự động thực hiện UAT cho Module V13 (Media Downloader) trên Facebook Group.

## 1. Hiện trạng (Current State)
- Script `v13_fb_media_downloader.py` đã sẵn sàng.
- Thiếu thư viện `websockets` trong môi trường Python Portable (đang cài đặt).
- Cần khởi động Chrome với port 9222 để CDP có thể kết nối.

## 2. Giải pháp kỹ thuật (Technical Solution)
- **Step 1:** Cài đặt `websockets` và `requests` cho Python Portable.
- **Step 2:** Sử dụng `open_browser_url` của Antigravity để mở Group Facebook.
    - *Lưu ý:* Môi trường Browser của Agent có thể không hỗ trợ port 9222 theo cách thông thường. Nếu `open_browser_url` không tự động mở port 9222, tôi sẽ thử khởi động một tiến trình Chrome độc lập qua `run_command` với flag `--remote-debugging-port=9222 --headless`.
- **Step 3:** Thực thi script `v13_fb_media_downloader.py`.
- **Step 4:** Kiểm tra folder `v13_fb_downloads` và tóm tắt kết quả.

## 3. Các file bị ảnh hưởng (Affected Files)
- `Project_V13_Media_Downloader/v13_fb_media_downloader.py` (Chạy script).
- `Project_V13_Media_Downloader/v13_fb_downloads/` (Thư mục output — đã đổi thành `downloads/v13_facebook/` trong handoff mới).

## 4. Rủi ro & Giải pháp (Risks & Mitigations)
- **Rủi ro 1: Facebook chặn truy cập.**
    - *Giải pháp:* Sử dụng User-Agent thông thường và cuộn chuột từ từ.
- **Rủi ro 2: CDP Port 9222 không hoạt động trong môi trường Agent.**
    - *Giải pháp:* Nếu không kết nối được, thử cài đặt `playwright` hoặc `selenium`.
- **Rủi ro 3: Group yêu cầu Login.**
    - *Giải pháp:* Nếu bị chặn bởi màn hình Login, báo cáo User.

## 5. Auditor Review (Chờ Codex phê duyệt)
- Quy trình tuân thủ Rule 6.3 (Tự kích hoạt browser và chụp ảnh chứng minh).
- Tuân thủ Rule 1.1 (Plan before action).

---
**Status:** ARCHIVED — superseded by `Implementation Plan/Agent Handoff/remaining_01_v13_facebook_live_uat_20260527.md`
