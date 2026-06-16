# Incident 03: Hardcoded Path Và Launcher Chưa Portable

**Ngày:** 2026-05-27
**Mức độ ưu tiên:** P1
**Trạng thái:** Đã xác nhận
**File liên quan:** `capture_antigravity.py`, `launcher_gui.py`

---

## 1. Tóm Tắt Điều Hành

Dự án đang phụ thuộc vào đường dẫn và môi trường riêng của một máy.

V10 ghi output vào Google Drive mount `G:\...`. Launcher hardcode Python portable dưới profile người dùng và gọi `chrome.exe` mà không có bước tìm đường dẫn hoặc fallback.

Điều này làm automation dễ hỏng khi đổi máy, đổi thư mục, đổi mount Google Drive, hoặc đổi cách cài Chrome/Python.

---

## 2. Giải Thích Thuật Ngữ

- **Portable**: có thể chạy ở máy/thư mục khác với ít cấu hình.
- **Hardcode**: ghi cứng đường dẫn, số trang, tọa độ, hoặc cấu hình vào code.
- **Path discovery**: tự tìm đường dẫn dựa trên `__file__`, `PATH`, biến môi trường, hoặc config.
- **Fallback**: phương án dự phòng nếu cấu hình chính không tồn tại.

---

## 3. Triệu Chứng Người Dùng Nhìn Thấy

Người dùng có thể gặp:

- V10 fail vì không có `G:\My Drive\...`.
- Launcher fail vì Python portable không đúng path.
- Chrome debug không mở vì `chrome.exe` không nằm trong PATH.
- Output nằm sai chỗ hoặc bị ghi đè/xóa ngoài ý muốn.

---

## 4. Hiện Trạng Kỹ Thuật

Đã xác nhận:

- `capture_antigravity.py` hardcode `OUTPUT_FOLDER` và `FINAL_PDF`.
- `capture_antigravity.py` hardcode `TOTAL_PAGES = 81`.
- `capture_antigravity.py` xóa ảnh cũ trước khi chạy.
- `launcher_gui.py` hardcode Python executable.
- `launcher_gui.py` gọi `chrome.exe` bằng tên.
- Launcher chưa có nút V14.

Chưa xác minh:

- Máy hiện tại còn mount `G:` đúng như code hay không.
- Python portable path hiện tại còn tồn tại hay không.
- Chrome có nằm trong PATH hay không.

---

## 5. Bằng Chứng Đã Thu Thập

`capture_antigravity.py`:

```text
OUTPUT_FOLDER = r"g:\My Drive\..."
FINAL_PDF = r"g:\My Drive\..."
TOTAL_PAGES = 81
```

`launcher_gui.py`:

```text
executable = r"C:\Users\vu.hoang\...\python.exe"
subprocess.Popen(["chrome.exe", "--remote-debugging-port=9222"])
```

---

## 6. Nguyên Nhân Gốc

Nguyên nhân trực tiếp:

- Script được viết để giải quyết nhanh workflow trên một máy cụ thể.

Nguyên nhân rộng hơn:

- Chưa có `config.py`.
- Chưa có preflight check (kiểm tra điều kiện trước khi chạy).
- Chưa tách default, override theo máy, và output runtime.

---

## 7. Mẫu Lỗi Thiết Kế Tổng Quát

Dự án đang coi local state như code. Các thứ như đường dẫn, executable, số trang, output folder nên là config hoặc input runtime, không nên nằm cứng trong script.

---

## 8. Thay Đổi Đề Xuất

1. Thêm `config.py` hoặc `.env.example`.
2. Dùng path tương đối từ `Path(__file__).resolve().parent`.
3. Cho override qua biến môi trường:
   - `OUTPUT_BASE`;
   - `PYTHON_EXE`;
   - `CHROME_EXE`;
   - `CDP_PORT`.
4. Launcher phải kiểm tra path trước khi launch.
5. V14 chỉ nên có nút launcher khi đã ghi rõ là diagnostic hoặc đã chạy end-to-end.

---

## 9. Lựa Chọn Triển Khai

### Option A: Sửa path tối thiểu

Chuyển hardcoded path sang repo-relative path.

Ưu điểm: nhanh, ít đổi hành vi.

Nhược điểm: chưa giải quyết đủ Python/Chrome discovery.

### Option B: Config module chung

Tạo `config.py` với default và environment override.

Ưu điểm: dùng lại cho V10-V14 và Hub Server.

Nhược điểm: cần sửa nhiều script.

### Option C: Launcher preflight

Giữ module gần như cũ, thêm kiểm tra trong GUI.

Ưu điểm: tốt cho user không rành kỹ thuật.

Nhược điểm: không giúp khi chạy CLI trực tiếp.

Khuyến nghị: Option B, áp dụng một phần Option A ngay nơi an toàn.

---

## 10. Rủi Ro Và Giảm Thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| Đổi output path làm user khó tìm file | Giữ override legacy path qua env var |
| Mất ảnh cũ khi chạy lại | Tạo per-run folder thay vì xóa chung |
| Chrome install path khác nhau | Check PATH và các path Windows phổ biến |
| V14 bị hiểu nhầm là production | Label rõ diagnostic nếu đưa vào launcher |

---

## 11. Output Mong Đợi

Sau khi duyệt:

- V10 output vào folder repo-relative hoặc config.
- Launcher tìm được Python/Chrome hoặc báo lỗi rõ.
- Không còn hardcode path theo user profile trong launcher.
- Các module dùng chung pattern config.

---

## 12. Kế Hoạch Thực Thi Sau Khi Duyệt

1. Thêm `config.py`.
2. Patch V10 dùng config.
3. Patch launcher dùng config và preflight.
4. Thêm `.gitignore` cho output nếu cần.
5. Chạy compile check và dry-run phần không đụng UI.

---

## 13. Câu Hỏi Còn Mở

1. Output mặc định nên nằm ở `outputs/`, `downloads/`, hay folder riêng từng module?
2. Google Drive còn là sync target mặc định hay chỉ là tùy chọn?
3. Launcher có cần UI chỉnh path không?

---

## 14. Ghi Chú Cho Agent Khác

- Không xóa output cũ khi migrate path nếu chưa được duyệt.
- Cẩn thận với logic xóa screenshot trong V10.
- Config riêng của máy không nên commit lên Git.

---

## 15. Đánh Giá Cuối

Đây là P1. Không chặn mọi workflow trên máy gốc, nhưng chặn portability và release rộng hơn.
