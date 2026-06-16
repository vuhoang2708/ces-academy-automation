# Incident 04: V11 SharePoint Chưa Khớp Claim Production

**Ngày:** 2026-05-27
**Mức độ ưu tiên:** P1
**Trạng thái:** Đã xác nhận
**File liên quan:** `Project_V11_SharePoint_Capture/capture_v11_sharepoint.py`

---

## 1. Tóm Tắt Điều Hành

V11 hiện tại chỉ là screenshot loop đơn giản bằng PyAutoGUI và PageDown. File không có các tính năng production được mô tả trong báo cáo như CV auto-stop, CSS injection, CDP connection hoặc ẩn toolbar Microsoft.

Nếu docs vẫn gọi V11 là production-ready thì đây là readiness gap nghiêm trọng.

---

## 2. Giải Thích Thuật Ngữ

- **Skeleton**: bản code tối thiểu, chưa đủ tính năng để gọi là production.
- **CV auto-stop**: dùng computer vision để nhận biết khi đã tới cuối tài liệu.
- **CSS injection**: chèn CSS vào trang web để ẩn toolbar hoặc phần giao diện gây nhiễu.
- **CDP**: Chrome DevTools Protocol, giao thức điều khiển Chrome debug.
- **UAT**: kiểm thử chấp nhận bởi người dùng trên workflow thật.

---

## 3. Triệu Chứng Người Dùng Nhìn Thấy

Người dùng có thể gặp:

- Chụp quá nhiều hoặc quá ít trang.
- Toolbar Microsoft/browser UI lọt vào ảnh.
- Script không tự dừng khi đến cuối tài liệu.
- PDF output phụ thuộc mạnh vào viewport/focus.

---

## 4. Hiện Trạng Kỹ Thuật

Đã xác nhận:

- Script import `pyautogui`, `time`, `os`, `img2pdf`.
- Script chụp màn hình và bấm PageDown.
- Không tìm thấy code cho CDP, CSS injection hoặc image-difference auto-stop.

Chưa xác minh:

- Có bản V11 đầy đủ trong Git history hoặc export logs hay không.
- V11 skeleton hiện tại còn chạy được với SharePoint document cụ thể hay không.

---

## 5. Bằng Chứng Đã Thu Thập

Code hiện tại có:

```text
pyautogui.screenshot(img_path)
pyautogui.press('pagedown')
img2pdf.convert(image_paths)
```

Báo cáo cũng ghi V11 hiện tại là skeleton và thiếu tính năng nâng cao.

---

## 6. Nguyên Nhân Gốc

Nguyên nhân trực tiếp:

- Source hiện tại không phải bản production được mô tả.

Nguyên nhân rộng hơn:

- Phiên bản đã test thành công chưa được bảo tồn/tag/commit rõ.
- Docs không phân biệt current code với historical behavior.

---

## 7. Mẫu Lỗi Thiết Kế Tổng Quát

Dự án chưa có quy tắc bảo tồn artifact/code prototype đã chạy tốt. Khi module tiến hóa, bản known-good cần được tag, commit, hoặc archive trước khi thay thế/simplify.

---

## 8. Thay Đổi Đề Xuất

1. Quyết định restore V11 hay downgrade docs.
2. Nếu restore:
   - thêm CDP nếu cần;
   - thêm CSS injection;
   - thêm CV auto-stop;
   - thêm crop/config controls;
   - thêm UAT guide.
3. Nếu không restore:
   - ghi rõ V11 hiện chỉ là basic screenshot extractor.

---

## 9. Lựa Chọn Triển Khai

### Option A: Downgrade documentation

Gọi V11 đúng là basic screenshot tool.

Ưu điểm: trung thực ngay.

Nhược điểm: không khôi phục tính năng production.

### Option B: Restore từ history

Tìm Git/export logs để khôi phục V11 production.

Ưu điểm: giữ behavior đã từng chạy.

Nhược điểm: có thể không có source.

### Option C: Rebuild production V11

Viết lại CV auto-stop và CSS injection.

Ưu điểm: code hiện đại hơn.

Nhược điểm: cần SharePoint session thật để UAT.

Khuyến nghị: Option A ngay, sau đó tìm Option B. Chỉ làm Option C nếu V11 vẫn là ưu tiên.

---

## 10. Rủi Ro Và Giảm Thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| SharePoint UI khác theo tenant/document | Thêm calibration và screenshot UAT |
| CSS selector thay đổi | Best-effort injection và fallback rõ |
| PageDown bỏ sót trang | Dùng visual diff và summary page count |
| PyAutoGUI ảnh hưởng người dùng | Luôn cảnh báo trước khi chạy |

---

## 11. Output Mong Đợi

Sau khi duyệt:

- V11 status chính xác.
- Có bản V11 production restored, hoặc docs ghi đúng limitation.
- UAT guide mô tả điều kiện cửa sổ SharePoint trước khi chạy.

---

## 12. Kế Hoạch Thực Thi Sau Khi Duyệt

1. Search Git history/export logs.
2. Chọn restore, rebuild hoặc doc downgrade.
3. Implement hoặc sửa docs theo lựa chọn.
4. Chạy compile check.
5. UAT với SharePoint document nếu có session.

---

## 13. Câu Hỏi Còn Mở

1. V11 còn quan trọng hơn V13/V14 không?
2. Có SharePoint document cụ thể để làm acceptance test không?
3. V11 nên dùng browser/CDP hay tiếp tục desktop screenshot?

---

## 14. Ghi Chú Cho Agent Khác

- Không claim V11 có CV auto-stop nếu code và UAT chưa chứng minh.
- Nếu thêm CSS injection, phải log rõ success/fallback.

---

## 15. Đánh Giá Cuối

V11 hiện tại không nên được approve là production. Đây là việc restore hoặc sửa tài liệu cho trung thực.
