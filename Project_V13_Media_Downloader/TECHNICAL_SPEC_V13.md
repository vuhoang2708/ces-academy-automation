# Technical Specification - Project V13 Facebook Media Downloader

## 1. Tổng quan kiến trúc
V13 Facebook là công cụ bóc tách dữ liệu Facebook Group qua **CDP (Chrome DevTools Protocol)**. Module này dùng Chrome debug tab đã đăng nhập để đọc DOM, tìm post, lưu text và tải media liên quan.

## 2. Các công nghệ lõi (Core Technologies)
- **CDP Engine:** quản lý WebSocket theo request id, có timeout và CDP error rõ.
- **Dynamic Discovery:** tìm bài viết qua text indicators như `Thích`, `Bình luận`, giảm phụ thuộc vào class CSS.
- **Indestructible Scroll:** dùng `Input.dispatchKeyEvent` PageDown thay vì `window.scrollBy`.
- **Hardened Download:** kiểm tra HTTP status, MIME type và tải streaming theo chunk.
- **Run Summary:** ghi `latest_run_summary.json` để biết posts/media thành công hoặc lỗi.

## 3. Quy trình thực thi (Execution Pipeline)
1. **Handshake:** Kết nối tới `localhost:9222` và xác thực Tab mục tiêu.
2. **Environment Isolation:** Sử dụng `--user-data-dir` để cô lập Profile, bypass các rào cản từ Plugin hoặc thiết lập bảo mật của User.
3. **Deep Scanning:** Thực hiện chuỗi sự kiện Keyboard (PageDown) có giãn cách (Sleep) để ép Facebook render dữ liệu cũ.
4. **Data Extraction:**
    - Chạy JS Script bóc tách Media từ các cụm `div` lân cận Indicators.
    - Lọc nhiễu Text bằng Regex và Array Filter.
5. **Sanitization & persistence:**
    - Xử lý ký tự đặc biệt (WinError 123) bằng giải thuật replace newline/special chars.
    - Duy trì cấu trúc thư mục phân cấp theo bài viết trong `downloads/v13_facebook/`.

## 4. Chẩn đoán & Xử lý lỗi (Diagnostics)
- **Fail-fast:** CDP Client ném Exception ngay khi có lỗi `id` hoặc `timeout`.
- **MIME Hijacking Protection:** Kiểm tra `Content-Type` của Media trước khi download để tránh lưu file lỗi.
- **Summary:** Kiểm tra `latest_run_summary.json` sau run.

---
*Cập nhật: 27/05/2026*
