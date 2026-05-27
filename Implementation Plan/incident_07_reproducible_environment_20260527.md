# Incident 07: Thiếu Môi Trường Tái Tạo, Config Và Run Report

**Ngày:** 2026-05-27
**Mức độ ưu tiên:** P2
**Trạng thái:** Đã xác nhận
**Phạm vi:** Toàn repo

---

## 1. Tóm Tắt Điều Hành

Repo chưa có `requirements.txt`, config chung, hoặc chuẩn run report. Điều này làm dự án khó cài lại, khó debug, khó bàn giao, và dễ hiểu nhầm khi một run chỉ thành công một phần.

---

## 2. Giải Thích Thuật Ngữ

- **Reproducible environment**: môi trường có thể cài lại và chạy lại bằng các bước rõ ràng.
- **Pinned version**: phiên bản thư viện được cố định, ví dụ `requests==2.31.0`.
- **Run report**: báo cáo sau mỗi lần chạy, gồm input, output, số thành công, số lỗi.
- **Preflight**: kiểm tra điều kiện trước khi chạy.
- **Config**: nơi cấu hình đường dẫn, port, output folder, model/API.

---

## 3. Triệu Chứng Người Dùng Nhìn Thấy

Người dùng hoặc agent có thể gặp:

- Import error trên máy mới.
- Thư viện khác version gây hành vi khác.
- Không biết run thành công hoàn toàn hay một phần.
- Không biết file nào do module nào sinh ra.

---

## 4. Hiện Trạng Kỹ Thuật

Đã xác nhận:

- Không tìm thấy `requirements.txt`.
- Scripts dùng nhiều dependency: `playwright`, `img2pdf`, `pyautogui`, `pygetwindow`, `Pillow`, `opencv-python`, `numpy`, `requests`, `websockets`.
- Chưa có `config.py`.
- Chưa có chuẩn `logs/` hoặc summary JSON/Markdown.

Chưa xác minh:

- Version thư viện trong Python portable hiện tại.
- Portable Python đang có đủ package hay không.

---

## 5. Bằng Chứng Đã Thu Thập

Lệnh:

```powershell
Get-ChildItem -Path . -Filter requirements*.txt -Recurse -File
```

Kết quả: không có requirements file.

README chỉ liệt kê thư viện yêu cầu nhưng không pin version.

---

## 6. Nguyên Nhân Gốc

Nguyên nhân trực tiếp:

- Dependency đang được ghi informal trong README, chưa thành installable metadata.

Nguyên nhân rộng hơn:

- Scripts phát triển như local utility, chưa được chuẩn hóa thành automation suite.
- Config, output, log và run summary chưa được thiết kế từ đầu.

---

## 7. Mẫu Lỗi Thiết Kế Tổng Quát

Dự án có nhiều module automation nhưng chưa có operational contract chung:

- config loading;
- dependency documentation;
- preflight checks;
- run summary;
- error reporting;
- output convention.

---

## 8. Thay Đổi Đề Xuất

1. Thêm `requirements.txt`.
2. Thêm `config.py`.
3. Thêm `.env.example` nếu dùng environment override.
4. Chuẩn hóa folder `outputs/` hoặc `downloads/`.
5. Chuẩn hóa run summary JSON/Markdown.
6. Thêm compile check vào validation.

---

## 9. Lựa Chọn Triển Khai

### Option A: Chỉ thêm requirements

Ưu điểm: nhanh.

Nhược điểm: chưa giải quyết config/reporting.

### Option B: Config + requirements + setup docs

Ưu điểm: cân bằng tốt.

Nhược điểm: cần sửa vài script/docs.

### Option C: Full packaging

Tạo `pyproject.toml`, package layout, console entrypoint.

Ưu điểm: sạch về dài hạn.

Nhược điểm: quá nặng cho trạng thái hiện tại.

Khuyến nghị: Option B.

---

## 10. Rủi Ro Và Giảm Thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| Version pin xung đột với Python portable | Test install trong đúng môi trường |
| Dependency khác theo module | Ghi comment nhóm dependency theo module |
| Config migration làm hỏng command cũ | Giữ default backward-compatible |
| Log chứa dữ liệu riêng tư | Log count/path/error, không log full private content |

---

## 11. Output Mong Đợi

Sau khi duyệt:

- Có `requirements.txt`.
- README có hướng dẫn setup.
- Có config pattern chung.
- Mỗi run lớn có summary rõ thành công/thất bại.

---

## 12. Kế Hoạch Thực Thi Sau Khi Duyệt

1. Inventory import của mọi Python file.
2. Tạo `requirements.txt`.
3. Tạo `config.py` với default repo-relative.
4. Patch từng module dùng config dần.
5. Thêm run summary cho V13 trước, rồi V10/V11/V12/V14.

---

## 13. Câu Hỏi Còn Mở

1. Pin version theo báo cáo hay theo môi trường hiện tại?
2. Repo nên giữ dạng scripts rời hay thành package Python?
3. Generated artifacts nằm trong repo hay ngoài repo?

---

## 14. Ghi Chú Cho Agent Khác

- Đừng assume dependency đã có chỉ vì code compile.
- Compile check không thay thế runtime/UI test.
- Raw media/capture riêng tư không nên commit nếu chưa được duyệt.

---

## 15. Đánh Giá Cuối

Đây là nền móng cho các bước sau. Nên thêm reproducibility trước khi mở rộng Hub Server hoặc Gemini automation.
