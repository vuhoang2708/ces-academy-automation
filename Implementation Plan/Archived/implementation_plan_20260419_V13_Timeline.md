> **Archive note:** File này là plan cũ ngày 2026-04-19, không còn là nguồn hướng dẫn hiện tại. Xem handoff mới trong `Implementation Plan/Agent Handoff/`. Output path cũ `v13_fb_downloads` đã được thay bằng `downloads/v13_facebook/`. Không commit folder `downloads/`.

---

# Implementation Plan - Timeline & Content Extraction (V13.1)
**Date:** 2026-04-19
**Task:**
Nâng cấp script FB Media Downloader để thu thập theo sự kiện (từng bài viết), tải chung nội dung văn bản (text), tóm tắt, và lưu vào cùng một folder với ảnh để chuẩn bị dữ liệu cho trang "Dòng thời gian".

## Giải pháp kỹ thuật (Technical Solution)

### Nâng cấp Extractor (V13.1)
1.  **Cập nhật `v13_fb_media_downloader.py`:**
    *   Tự động cuộn trang (Scroll) hoặc trích xuất nội dung của từng bài đăng riêng biệt (Feed Unit).
    *   Sử dụng DOM hierarchy (ví dụ: thẻ `div[role="article"]`) để gộp nội dung chữ (post content) và ảnh/video của cùng một bài viết nhằm tránh lẫn lộn.
    *   Tạo thư mục cho mỗi sự kiện. Sẽ dùng quy tắc lấy N chữ cái đầu của đoạn text làm tên thư mục nếu không tích hợp AI, hoặc tự động tạo ID.
    *   Lưu ảnh vào thư mục sự kiện tương ứng + tạo file `content.txt` (nội dung gốc).

## Các file bị ảnh hưởng
- `Project_V13_Media_Downloader/v13_fb_media_downloader.py`
- `downloads/v13_facebook/` (output path mới — không commit)

## Rủi ro & Khắc phục
- **DOM Facebook Rất Phức Tạp:** Class của FB thường xuyên thay đổi. Để gộp ảnh và chữ, tìm container gốc của mỗi bài post (thường là component `role="article"`).
- **Solution:** Viết script chạy JS qua CDP để `querySelectorAll` theo thẻ `div[role="article"]`. Sau đó lọc lấy `textContent` và lọc các `img` có link `fbcdn.net` trong phạm vi bài post đó.

## Auditor Review
- Scope Update: Khóa chặt phạm vi vào Scraping (Thu thập dữ liệu), không đụng chạm đến code Frontend Web.
- Tuân thủ toàn bộ Rule 1.1 và Rule 1.2
- Đã thiết kế kiến trúc thuần tự động lấy dữ liệu đóng gói.

---
**Status:** ARCHIVED — superseded by `Implementation Plan/Agent Handoff/remaining_01_v13_facebook_live_uat_20260527.md`
