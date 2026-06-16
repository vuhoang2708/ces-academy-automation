# Incident 06: V14 Zalo Desktop Hiện Chỉ Là Diagnostic

**Ngày:** 2026-05-27
**Mức độ ưu tiên:** P2
**Trạng thái:** Đã xác nhận
**File liên quan:** `Project_V14_Zalo_Media_Downloader/zalo_media_v14.py`

---

## 1. Tóm Tắt Điều Hành

V14 đã có file trong repo nhưng chưa phải Zalo Desktop media downloader hoàn chỉnh. Code hiện tại chủ yếu capture screenshot chẩn đoán cửa sổ Zalo và test thao tác, chưa có luồng tìm media panel, template matching nút download, xử lý Save As, hoặc summary output.

V14 cần giữ trạng thái “in development/diagnostic” cho đến khi tải media end-to-end được verify.

---

## 2. Giải Thích Thuật Ngữ

- **Diagnostic mode**: chế độ chụp/ghi nhận để quan sát, chưa tự động tải thật.
- **Template matching**: dùng ảnh mẫu để tìm icon/nút trên màn hình.
- **Save As dialog**: cửa sổ Windows dùng để chọn nơi lưu file.
- **Dry-run**: chạy thử để phát hiện vị trí/target nhưng chưa click thật.
- **UAT**: kiểm thử workflow thật từ góc nhìn người dùng.

---

## 3. Triệu Chứng Người Dùng Nhìn Thấy

Nếu user kỳ vọng V14 tải media:

- Script không tải media end-to-end.
- Có thể chỉ tạo diagnostic image.
- Có thể gửi phím/click mà chưa hoàn thành workflow.

---

## 4. Hiện Trạng Kỹ Thuật

Đã xác nhận:

- Code import `pyautogui`, `pygetwindow`, `PIL`, `cv2`, `numpy`.
- Có `TEMP_DIR = "zalo_templates"`.
- Có capture screenshot region của cửa sổ Zalo.
- Có lưu diagnostic capture.
- Có thao tác test `enter`.
- Không thấy loop tải media, template matching download icon, hoặc Save As handling.

Chưa xác minh:

- Diagnostic capture hiện chạy tốt với Zalo window thật hay không.
- Có template image phù hợp ở ngoài repo hay không.

---

## 5. Bằng Chứng Đã Thu Thập

Code hiện tại có:

```text
TEMP_DIR = "zalo_templates"
pyautogui.screenshot(region=(...))
screenshot.save(diag_path)
pyautogui.press('enter')
```

Báo cáo cũng ghi V14 là early development/diagnostic only.

---

## 6. Nguyên Nhân Gốc

Nguyên nhân trực tiếp:

- V14 mới có bước diagnostic đầu tiên.

Nguyên nhân rộng hơn:

- Zalo Desktop automation phụ thuộc UI, tọa độ và template dễ thay đổi.
- Chưa có calibration workflow.
- Chưa có protocol an toàn cho click tự động.

---

## 7. Mẫu Lỗi Thiết Kế Tổng Quát

UI automation module cần lifecycle rõ:

1. Diagnostic capture.
2. Calibration/template setup.
3. Dry-run detection.
4. Controlled click/download.
5. Save dialog handling.
6. Output verification.
7. UAT note.

V14 hiện mới ở bước 1.

---

## 8. Thay Đổi Đề Xuất

1. Giữ V14 label là diagnostic cho đến khi end-to-end pass.
2. Thêm calibration mode.
3. Thêm template matching cho:
   - media panel;
   - photo/video tab;
   - download icon.
4. Thêm dry-run overlay/target report.
5. Thêm controlled execute mode.
6. Thêm Save As handling.
7. Thêm output manifest và summary.

---

## 9. Lựa Chọn Triển Khai

### Option A: Hoàn thiện V14 thành đường Zalo media chính

Ưu điểm: định hướng rõ.

Nhược điểm: cần UAT Zalo UI thật.

### Option B: Restore V13 Zalo trước

Ưu điểm: có thể nhanh nếu source cũ còn.

Nhược điểm: dễ trùng hướng V14.

### Option C: Xây shared Zalo UI toolkit

Tách helper cho window finding, screenshot, template matching, click safety.

Ưu điểm: giúp cả V12, V13 Zalo và V14.

Nhược điểm: cần thiết kế thêm.

Khuyến nghị: Option C nếu Zalo là workflow lớn; nếu không, Option A là đủ.

---

## 10. Rủi Ro Và Giảm Thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| Click nhầm trong Zalo | Dry-run trước execute |
| Đổi resolution làm template fail | Dùng confidence threshold và template theo scale |
| Save As dialog khác ngôn ngữ Windows | Detect control phổ biến và có manual fallback |
| Automation chiếm chuột/phím | Countdown và hướng dẫn dừng khẩn cấp |

---

## 11. Output Mong Đợi

Sau khi duyệt và triển khai:

- V14 có diagnostic/dry-run/execute mode.
- Target detection có confidence score.
- File tải về nằm ở folder dự đoán được.
- Có run summary và UAT note.

---

## 12. Kế Hoạch Thực Thi Sau Khi Duyệt

1. Capture screenshot diagnostic ở màn hình hiện tại.
2. Tạo template calibration.
3. Thêm dry-run target detection.
4. Thêm click/download flow.
5. Thêm Save As handling.
6. Chạy UAT với chat/media thật.

---

## 13. Câu Hỏi Còn Mở

1. V14 tải toàn bộ media của chat hay chỉ media đang hiển thị?
2. Filename giữ tên gốc Zalo hay tạo timestamp?
3. Có đưa V14 vào launcher khi vẫn là diagnostic không?

---

## 14. Ghi Chú Cho Agent Khác

- Không gọi V14 là production.
- Không thêm nút “download” vào launcher nếu flow chưa tải thật.
- Screenshot fixture/private artifact không nên commit nếu chưa được duyệt.

---

## 15. Đánh Giá Cuối

V14 là feature đang phát triển, chưa phải downloader. Nên làm sau P0/P1 hoặc sau khi có shared Zalo UI toolkit.
