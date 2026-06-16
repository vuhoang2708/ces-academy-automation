# Implementation Plan: Chạy V12 Zalo Screenshot (Bản cập nhật Đã Xác Minh & Tối Ưu)
**Ngày:** 2026-05-27
**Tên task:** Run V12 Zalo Screenshot Pro - khôi phục cửa sổ minimized và nhận diện ảnh trùng

---

## 1. Đề bài (Task Description)
Chạy script tự động hóa V12 (`Project_V12_Zalo_Screenshot/capture_v12_zalo_pro.py`) để chụp ảnh màn hình cuộc hội thoại Zalo đang mở với "Minh Đỗ", sau đó xuất ra tệp tin PDF tổng hợp lịch sử chat.
*Các điều kiện đã hoàn tất và kiểm chứng*:
- Thêm logic click chuột lấy focus vào vùng chat.
- Thêm cơ chế nhận diện ảnh trùng lặp (Duplicate Detection) để dừng sớm nếu không cuộn được hoặc chạm đáy.
- Đã chạy thử nghiệm và xác minh thành công việc cuộn trang cũng như cơ chế tự động ngắt sớm ở trang 5 (trang 6 trùng).

## 2. Hiện Trạng Và Phân Tích
- **Vấn đề đã xử lý**:
  - Không có focus dẫn đến lặp trang -> Đã sửa bằng cách click vào vùng an toàn của khung chat.
  - Cửa sổ bị thu nhỏ (minimized) gây lỗi tọa độ âm (-32000) -> Đã sửa bằng cách dùng `win.restore()` khôi phục cửa sổ trước khi activate.
  - Lặp trang khi chạm đáy -> Đã sửa bằng cách so sánh ảnh liền trước bằng `ImageChops.difference`.
  - Đã xóa tệp PDF lỗi 0-byte từ phiên chạy đầu tiên (`Zalo_Chat_History_20260527_102639.pdf`).

## 3. Giải pháp kỹ thuật (Technical Solution)
1. **Sửa đổi Code** `Project_V12_Zalo_Screenshot/capture_v12_zalo_pro.py`:
   - Dọn dẹp ảnh cũ trong thư mục output trước mỗi phiên chạy mới.
   - Kiểm tra và phục hồi cửa sổ bị thu nhỏ trước khi lấy tọa độ:
     ```python
     if win.isMinimized:
         win.restore()
         time.sleep(1.5)
     ```
   - Click lấy focus tại `(left + width * 0.40, top + 200)`.
   - Cấu hình trang tối đa: `MAX_SCROLLS = 100` (được bảo vệ bởi cơ chế dừng sớm tự động khi chạm đáy).
   - So sánh ảnh bằng `ImageChops.difference(img1, img2).getbbox() is None` để dừng chụp sớm khi chạm đáy.

2. **Tiêu chí Xác thực (Validation Criteria)**:
   - Ảnh chụp đầu ra trong `zalo_captures/` phải có nội dung khác nhau (kích thước tệp tin hoặc hash ảnh khác biệt).
   - Script phải dừng kèm thông báo lý do rõ ràng khi phát hiện trang trùng lặp (chạm đáy cuộc hội thoại) trước khi xuất PDF.
   - Không còn tệp PDF lỗi 0-byte trong thư mục dự án.

3. **Kết luận Trạng thái**:
   - Đây được coi là một **validated test run cho case hiện tại** (lượt chạy đã được xác minh thành công trên môi trường thử nghiệm với Zalo đang mở).

## 4. Các file bị ảnh hưởng (Affected Files)
- Sửa đổi trực tiếp file: `Project_V12_Zalo_Screenshot/capture_v12_zalo_pro.py`.

## 5. Rủi Ro Và Biện Pháp Phòng Ngừa
- Đảm bảo người dùng không tương tác chuột/bàn phím khi script đang hoạt động để tránh kích hoạt fail-safe của PyAutoGUI.

---
## 6. Auditor Review
- Người rà soát: Codex / Auditor
