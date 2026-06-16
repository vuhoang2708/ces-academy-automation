# Incident 02: Spec Và Code Đang Lệch Nhau

**Ngày:** 2026-05-27
**Mức độ ưu tiên:** P0
**Trạng thái:** Đã xác nhận
**File liên quan:** `BAO_CAO_TONG_HOP_DU_AN.md`, `TECHNICAL_SPEC_UNIFIED_HUB.md`, source code hiện tại

---

## 1. Tóm Tắt Điều Hành

Một số tài liệu đang mô tả khác với trạng thái repo hiện tại.

Các điểm lệch quan trọng:

- Báo cáo nói V12 còn bug timestamp, nhưng code V12 hiện tại đã sửa.
- Unified Hub spec nói `hub_server.py` đã hoàn thành, nhưng repo không có file này.
- Báo cáo mô tả V11 có tính năng production, nhưng file V11 hiện tại chỉ là screenshot loop đơn giản.

Nếu không sửa, agent sau có thể sửa nhầm việc, approve sai readiness, hoặc overclaim tiến độ.

---

## 2. Giải Thích Thuật Ngữ

- **Spec-code drift**: tài liệu/spec và code thực tế bị lệch nhau.
- **Stale claim**: nhận định từng đúng hoặc được viết trong bối cảnh cũ, nhưng không còn đúng với repo hiện tại.
- **Source of truth**: nguồn sự thật ưu tiên; ở đây là file thật, command output và runtime evidence.
- **Overclaim**: tuyên bố quá mức so với bằng chứng.

---

## 3. Triệu Chứng Người Dùng Nhìn Thấy

Người dùng hoặc agent có thể:

- Sửa lại bug V12 timestamp dù bug này đã sửa.
- Đi tìm `hub_server.py` không tồn tại.
- Tin rằng V11 production-ready trong khi code chưa có tính năng production.
- Dựa vào roadmap/tài liệu thay vì kiểm chứng repo thật.

---

## 4. Hiện Trạng Kỹ Thuật

Đã xác nhận:

- `Project_V12_Zalo_Screenshot/capture_v12_zalo_pro.py` đang dùng `%Y%m%d_%H%M%S`.
- `TECHNICAL_SPEC_UNIFIED_HUB.md` claim `hub_server.py` đã hoàn thành.
- `Test-Path .\hub_server.py` trả về `False`.
- `Project_V11_SharePoint_Capture/capture_v11_sharepoint.py` chỉ có logic PyAutoGUI screenshot và PageDown.

Chưa xác minh:

- `hub_server.py` có tồn tại ở repo/thư mục khác hay không.
- Báo cáo đang cố ghi lại lịch sử hay muốn là source of truth hiện tại.

---

## 5. Bằng Chứng Đã Thu Thập

V12 code hiện tại:

```text
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
```

Hub Server:

```powershell
Test-Path .\hub_server.py
```

Kết quả:

```text
False
```

V11 code hiện tại chỉ thấy:

```text
pyautogui.screenshot(...)
pyautogui.press('pagedown')
img2pdf.convert(...)
```

Không thấy bằng chứng code cho:

- CSS injection;
- CDP connection;
- CV auto-stop;
- retry logic.

---

## 6. Nguyên Nhân Gốc

Nguyên nhân trực tiếp:

- Tài liệu được tổng hợp từ lịch sử/spec mà chưa đối chiếu đầy đủ với repo hiện tại.

Nguyên nhân rộng hơn:

- Dự án chưa phân tách rõ trạng thái của từng claim:
  - implemented (đã implement);
  - verified (đã kiểm chứng);
  - planned (dự kiến);
  - experimental (thử nghiệm);
  - historical (lịch sử);
  - missing (không có trong repo hiện tại).

---

## 7. Mẫu Lỗi Thiết Kế Tổng Quát

Repo đang dùng cùng một giọng văn cho cả phần đã làm, phần định làm, phần từng có trong lịch sử và phần chưa tồn tại. Điều này làm người đọc khó biết đâu là sự thật hiện tại.

---

## 8. Thay Đổi Đề Xuất

1. Thêm bảng trạng thái module vào docs.
2. Đánh dấu rõ claim nào là historical/planned/missing.
3. Sửa các claim sai về V12, V11 và Hub Server.
4. Thêm checklist kiểm chứng trước khi ghi “completed”.

---

## 9. Lựa Chọn Triển Khai

### Option A: Sửa doc tối thiểu

Chỉ sửa những claim sai đã xác nhận.

Ưu điểm:

- Nhanh, ít đụng file.

Nhược điểm:

- Chưa chặn drift tái diễn.

### Option B: Thêm mô hình trạng thái tài liệu

Mỗi module/claim có status rõ.

Ưu điểm:

- Giảm hiểu nhầm lâu dài.

Nhược điểm:

- Cần sửa nhiều docs hơn.

### Option C: Sinh status bằng script kiểm tra

Script kiểm file tồn tại, compile status, artifact status.

Ưu điểm:

- Mạnh nhất về lâu dài.

Nhược điểm:

- Cần thêm code/tooling.

Khuyến nghị: Option B ngay, Option C sau khi source ổn định.

---

## 10. Rủi Ro Và Giảm Thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| Xóa nhầm lịch sử hữu ích | Giữ lịch sử nhưng label là historical |
| Agent vẫn tin báo cáo cũ | Đưa current repo truth lên đầu docs |
| Hub bị bỏ quên | Giữ trong roadmap, không ghi completed nếu chưa có file |

---

## 11. Output Mong Đợi

Sau khi duyệt:

- Docs ghi rõ V12 timestamp bug đã được sửa trong code hiện tại.
- Docs ghi rõ `hub_server.py` chưa có trong repo snapshot này.
- V11 được mô tả đúng là skeleton/simple screenshot loop nếu chưa restore.
- Roadmap không lẫn với trạng thái đã verify.

---

## 12. Kế Hoạch Thực Thi Sau Khi Duyệt

1. Patch `BAO_CAO_TONG_HOP_DU_AN.md`.
2. Patch `TECHNICAL_SPEC_UNIFIED_HUB.md`.
3. Thêm module status table vào README hoặc file status riêng.
4. Chạy `rg`/compile check để đối chiếu claim.

---

## 13. Câu Hỏi Còn Mở

1. `BAO_CAO_TONG_HOP_DU_AN.md` nên là báo cáo lịch sử hay source of truth hiện tại?
2. Source of truth chính nên là README, MASTER_SPECIFICATION, hay `PROJECT_STATUS.md` mới?

---

## 14. Ghi Chú Cho Agent Khác

- Không tin claim “completed” nếu chưa đối chiếu file thật.
- Với claim runtime, cần log/UAT/backend evidence chứ không chỉ đọc docs.

---

## 15. Đánh Giá Cuối

Đây là P0 vì nó ảnh hưởng quyết định triển khai. Cần sửa drift trước khi giao việc implementation cho agent khác.
