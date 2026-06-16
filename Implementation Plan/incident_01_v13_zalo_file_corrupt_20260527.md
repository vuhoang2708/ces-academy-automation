# Incident 01: File V13 Zalo Media Downloader Bị Corrupt

**Ngày:** 2026-05-27
**Mức độ ưu tiên:** P0
**Trạng thái:** Đã xác nhận
**File liên quan:** `Project_V13_Media_Downloader/v13_zalo_media_downloader.py`

---

## 1. Tóm Tắt Điều Hành

`v13_zalo_media_downloader.py` không còn là file Python hợp lệ trong repo hiện tại. File có null bytes và không thể compile bằng Python.

Việc này chặn toàn bộ hướng V13 Zalo media downloader cho đến khi file được restore, rewrite, hoặc quarantine rõ ràng.

---

## 2. Giải Thích Thuật Ngữ

- **Corrupt file**: file bị hỏng hoặc sai encoding đến mức không đọc/chạy được.
- **Null byte**: byte có giá trị `0`; Python source không được chứa null byte.
- **Restore**: khôi phục từ Git history, backup, hoặc artifact cũ.
- **Rewrite**: viết lại file dựa trên spec và hành vi mong muốn.
- **Quarantine**: cách ly/đánh dấu file là không dùng được để tránh agent khác tưởng là functional.

---

## 3. Triệu Chứng Người Dùng Nhìn Thấy

Nếu người dùng hoặc launcher gọi V13 Zalo downloader:

- Python không parse được file.
- Không có media nào được tải.
- Tài liệu nào ghi V13 Zalo đang hoạt động sẽ gây hiểu nhầm.

---

## 4. Hiện Trạng Kỹ Thuật

Đã xác nhận:

- File tồn tại nhưng chỉ có 32 bytes.
- File chứa 15 null bytes.
- Python compile lỗi với thông báo `SyntaxError: source code string cannot contain null bytes`.
- Nội dung đọc bằng UTF-8 chỉ hiện kiểu `import cv2...`, không phải source hoàn chỉnh.

Chưa xác minh:

- Có version hợp lệ trong Git history hay không.
- V13 Zalo nên được restore như legacy module hay chuyển hẳn sang hướng V14.

---

## 5. Bằng Chứng Đã Thu Thập

Lệnh compile:

```powershell
python -m py_compile Project_V13_Media_Downloader\v13_zalo_media_downloader.py
```

Kết quả:

```text
SyntaxError: source code string cannot contain null bytes
```

Byte inspection:

```text
Bytes: 32
NullBytes: 15
FirstBytes: FF FE 69 00 6D 00 70 00 6F 00 72 00 74 00 ...
```

Tài liệu cũng đã ghi nhận:

- `BAO_CAO_TONG_HOP_DU_AN.md` đánh dấu file này là corrupt.

---

## 6. Nguyên Nhân Gốc

Nguyên nhân trực tiếp:

- File hiện tại không còn là source Python hợp lệ.

Nguyên nhân rộng hơn:

- Repo chưa có quality gate (cổng kiểm tra chất lượng) tối thiểu cho source file.
- Chưa có bước compile check trước khi gọi module là usable.
- Code experimental và production có dấu hiệu bị trộn mà không có release checklist.

---

## 7. Mẫu Lỗi Thiết Kế Tổng Quát

Dự án đang để một file “tồn tại trong repo” bị hiểu nhầm là “module chạy được”.

Với automation suite, một module chỉ nên được xem là có thể dùng khi qua tối thiểu:

- compile check;
- encoding check;
- dependency check;
- smoke test (test chạy nhanh để xác nhận không chết ngay).

---

## 8. Thay Đổi Đề Xuất

1. Tìm và restore file từ Git history hoặc backup nếu có.
2. Nếu không restore được, thay bằng stub rõ ràng báo “module unavailable” hoặc rewrite theo hướng V14.
3. Thêm compile validation vào checklist chung.
4. Cập nhật docs: phân biệt V13 Facebook production với V13 Zalo đang hỏng/chưa usable.

---

## 9. Lựa Chọn Triển Khai

### Option A: Restore từ Git

Khôi phục version hợp lệ cuối cùng của file.

Ưu điểm:

- Giữ đúng ý định ban đầu.
- Ít rủi ro thiết kế lại.

Nhược điểm:

- Có thể không có version hợp lệ trong history.

### Option B: Rewrite theo hướng V14

Dùng hướng V14 diagnostic/template matching để viết lại Zalo downloader.

Ưu điểm:

- Gần roadmap hiện tại hơn.

Nhược điểm:

- Cần UAT với Zalo UI thật.
- Tốn công hơn.

### Option C: Quarantine file

Đổi docs/status để nói rõ file này không dùng được, mọi Zalo media work chuyển sang V14.

Ưu điểm:

- Trung thực và nhanh.

Nhược điểm:

- Không khôi phục V13 Zalo.

Khuyến nghị: làm Option A trước. Nếu không có source hợp lệ, dùng Option C để chặn hiểu nhầm, rồi mới cân nhắc Option B.

---

## 10. Rủi Ro Và Giảm Thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| Restore code cũ nhưng Zalo UI đã đổi | Phải có UAT và screenshot mới |
| Rewrite trùng lặp với V14 | Chốt rõ V13 là legacy hay chuyển hẳn sang V14 |
| Còn lỗi encoding ẩn | Compile toàn bộ `.py` sau khi sửa |
| Ghi đè nhầm thay đổi của người dùng | Kiểm tra diff trước khi sửa source |

---

## 11. Output Mong Đợi

Sau khi duyệt và triển khai:

- File không còn chứa null bytes.
- `python -m py_compile` pass với file này, hoặc file được quarantine rõ ràng.
- Docs không còn claim V13 Zalo functional nếu chưa có bằng chứng.

---

## 12. Kế Hoạch Thực Thi Sau Khi Duyệt

1. Kiểm tra Git history cho file.
2. Restore source nếu có.
3. Nếu không có, tạo stub rõ ràng hoặc rewrite nếu được duyệt.
4. Chạy compile check.
5. Cập nhật README/spec liên quan.

---

## 13. Câu Hỏi Còn Mở

1. Có backup/export nào chứa V13 Zalo hợp lệ không?
2. V13 Zalo cần được restore như legacy hay chuyển toàn bộ hướng Zalo media sang V14?

---

## 14. Ghi Chú Cho Agent Khác

- Không sửa bằng cách đoán encoding; file chỉ có 32 bytes nên không phải source hoàn chỉnh.
- Không gọi V13 Zalo là functional nếu chưa compile và UAT pass.

---

## 15. Đánh Giá Cuối

Đây là P0 blocker thật. Cần restore hoặc quarantine trước mọi claim release liên quan đến Zalo media downloader.
