# Incident 05: V13 Facebook Cần Hardening Trước Khi Mở Rộng

**Ngày:** 2026-05-27
**Mức độ ưu tiên:** P1
**Trạng thái:** Rủi ro đã xác nhận qua static inspection; chưa live-verify trong lượt này
**File liên quan:** `Project_V13_Media_Downloader/v13_fb_media_downloader.py`, `Project_V13_Media_Downloader/v13_fb_media_downloader_v17.py`

---

## 1. Tóm Tắt Điều Hành

V13 Facebook là module có giá trị production cao nhất hiện tại, nhưng script chính còn nhiều điểm yếu: nuốt lỗi bằng `except: pass`, thiếu timeout rõ, thiếu summary cuối run, và chưa có cơ chế dedup/checkpoint đầy đủ.

File V17 experimental có nhiều phần tốt hơn như typed error, timeout handling, streaming download và sanitize folder name. Hướng đúng là giữ discovery logic đã chứng minh giá trị của V13, rồi merge phần hardening từ V17 vào bản stable.

---

## 2. Giải Thích Thuật Ngữ

- **Hardening**: làm code bền hơn trước lỗi network, timeout, UI thay đổi, và dữ liệu bất thường.
- **Silent failure**: lỗi bị nuốt mất, người dùng không biết fail ở đâu.
- **MIME validation**: kiểm tra `Content-Type` để chắc file tải về đúng loại.
- **Streaming download**: tải file theo từng chunk, phù hợp hơn với file lớn.
- **Dedup**: tránh tải/lưu trùng cùng một post hoặc media.

---

## 3. Triệu Chứng Người Dùng Nhìn Thấy

Người dùng có thể gặp:

- Thiếu ảnh nhưng không có log lỗi.
- Folder có content nhưng media tải thiếu.
- Chạy lại tạo folder/post trùng.
- Facebook scroll/discovery fail mà script vẫn im lặng.
- Không biết post/image nào thành công hay thất bại.

---

## 4. Hiện Trạng Kỹ Thuật

Đã xác nhận:

- Main V13 có `except: pass`.
- Main V13 dùng `requests.get(url, timeout=10)` nhưng chưa có reporting đủ rõ.
- Main V13 ghi output vào `v13_fb_downloads`.
- V17 có `CDPError`, `CDPTimeout`, structured CDP send, `sanitize_folder_name`, và `smart_download`.

Chưa xác minh:

- V13 main có còn chạy tốt với Facebook hiện tại hay không.
- V17 discovery có tương đương hoặc tốt hơn V13 main hay không.
- Chrome debug tab/Facebook login hiện có sẵn hay không.

---

## 5. Bằng Chứng Đã Thu Thập

Main V13 có các điểm rủi ro:

```text
except: pass
requests.get(url, timeout=10)
output dir: v13_fb_downloads
```

V17 có các điểm đáng merge:

```text
CDPError / CDPTimeout
timeout handling
sanitize_folder_name
smart_download with Content-Type and iter_content
```

---

## 6. Nguyên Nhân Gốc

Nguyên nhân trực tiếp:

- Script production ưu tiên chạy nhanh/compact hơn là observability.

Nguyên nhân rộng hơn:

- Chưa có run summary chuẩn.
- Chưa có success/failure counter.
- Chưa có dedup/checkpoint contract.
- Experimental hardening chưa được merge lại vào stable.

---

## 7. Mẫu Lỗi Thiết Kế Tổng Quát

Dự án đang coi “đã từng tạo output” là production readiness. Với downloader automation, production readiness cần có:

- preflight rõ;
- lỗi nhìn thấy được;
- output lặp lại được;
- run summary;
- dedup/resume;
- UAT evidence.

---

## 8. Thay Đổi Đề Xuất

1. Giữ dynamic discovery của V13 main.
2. Merge từ V17:
   - typed CDP errors;
   - timeout;
   - folder sanitization;
   - streaming download;
   - MIME validation.
3. Thay `except: pass` bằng warning/counter.
4. Thêm run summary:
   - posts found;
   - posts saved;
   - images attempted;
   - images succeeded;
   - images failed;
   - output directory.
5. Thêm dedup hoặc per-run manifest.

---

## 9. Lựa Chọn Triển Khai

### Option A: Patch main V13 tại chỗ

Thêm logging/counter vào `v13_fb_media_downloader.py`.

Ưu điểm: ít đổi behavior.

Nhược điểm: cấu trúc code vẫn khó bảo trì.

### Option B: Promote V17 sau khi giữ discovery của V13

Đưa discovery ổn định từ V13 vào cấu trúc sạch hơn của V17, rồi chọn một stable file.

Ưu điểm: maintainability tốt hơn.

Nhược điểm: cần UAT kỹ để tránh regression.

### Option C: Giữ cả hai bản

Launcher cho chọn stable/experimental.

Ưu điểm: ít rủi ro với bản cũ.

Nhược điểm: dễ gây nhầm và tăng chi phí maintain.

Khuyến nghị: Option B, nhưng chỉ sau khi capture baseline live của V13 main.

---

## 10. Rủi Ro Và Giảm Thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| Refactor làm hỏng discovery đang chạy được | Chạy baseline trước khi merge |
| Facebook UI thay đổi | Giữ text/role-based discovery và diagnostic output |
| Log lộ nội dung riêng tư | Log count/path/error, không log full post nếu không cần |
| Dedup skip nhầm lần muốn tải lại | Thêm `--force` |

---

## 11. Output Mong Đợi

Sau khi duyệt:

- Chỉ có một V13 Facebook stable rõ ràng.
- Không còn silent exception trong download path.
- Có summary cuối run.
- Output folder behavior dễ đoán.
- UAT guide cập nhật theo counter thành công/thất bại.

---

## 12. Kế Hoạch Thực Thi Sau Khi Duyệt

1. Chạy baseline V13 main với Chrome debug tab nếu có.
2. So sánh output V13 và V17.
3. Merge hardening vào file stable được chọn.
4. Chạy compile check.
5. Chạy live UAT và lưu result note.

---

## 13. Câu Hỏi Còn Mở

1. Stable filename có giữ là `v13_fb_media_downloader.py` không?
2. V17 có archive sau merge không?
3. Output nên dùng shared folder hay timestamped per-run folder?

---

## 14. Ghi Chú Cho Agent Khác

- Không làm mất dynamic discovery của V13 nếu chưa có bằng chứng V17 tốt hơn.
- Không dựa vào câu “download completed” chung chung; phải kiểm count và file.

---

## 15. Đánh Giá Cuối

Đây không phải P0 như file V13 Zalo corrupt, nhưng cần làm trước khi mở rộng V13 hoặc tích hợp vào Hub Server.
