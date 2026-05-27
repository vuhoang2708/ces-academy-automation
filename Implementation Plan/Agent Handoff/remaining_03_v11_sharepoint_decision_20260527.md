# Handoff 03: Quyết Định Và Xử Lý V11 SharePoint

**Ưu tiên:** P1
**Loại việc:** scope decision + optional restore/rebuild
**Module:** `Project_V11_SharePoint_Capture/capture_v11_sharepoint.py`
**Plan gốc:** `incident_04_v11_sharepoint_production_gap_20260527.md`

---

## 1. Mục tiêu

Chốt V11 theo một trong ba hướng:

1. Giữ là basic screenshot extractor và docs nói đúng limitation.
2. Restore bản production nếu tìm được trong Git history/export.
3. Rebuild production V11 nếu SharePoint vẫn là ưu tiên.

Không được gọi V11 là production-ready khi chưa có UAT thật.

---

## 2. Trạng thái hiện tại đã xác nhận

- V11 hiện là screenshot loop cơ bản bằng PyAutoGUI/PageDown.
- Chưa thấy CV auto-stop, CSS injection, CDP, hoặc ẩn toolbar Microsoft trong code hiện tại.
- `PROJECT_STATUS.md` đã ghi V11 là `Skeleton/basic screenshot`.

---

## 3. Bước 1: kiểm tra lịch sử trước khi sửa

```powershell
git status --short --branch
git log --oneline --all -- Project_V11_SharePoint_Capture/capture_v11_sharepoint.py
git log --oneline --all -- \"*sharepoint*\" \"*SharePoint*\"
rg -n \"SharePoint|capture_v11|CV auto-stop|CSS injection|PageDown|CDP\" .
```

Nếu tìm được commit cũ có code tốt:

```powershell
git show <commit>:Project_V11_SharePoint_Capture/capture_v11_sharepoint.py
```

Không dùng `git checkout --` nếu có nguy cơ ghi đè thay đổi hiện tại; dùng `git show` để đọc trước.

---

## 4. Hướng A: giữ V11 là basic

Làm nếu V11 không phải ưu tiên ngay.

Cần sửa:

- `PROJECT_STATUS.md`: giữ V11 là basic/skeleton.
- `README.md` hoặc docs liên quan: nói rõ V11 chưa có production features.
- Tạo UAT guide ngắn: điều kiện cửa sổ SharePoint, output, limitation.

PASS khi docs không còn claim V11 có CV/CDP/CSS nếu code chưa có.

---

## 5. Hướng B: restore bản production

Làm nếu tìm được code cũ tin cậy.

Các bước:

1. Trích code bằng `git show` ra file tạm để review.
2. So sánh với `config.py` hiện tại và bỏ hardcoded path.
3. Merge thủ công bằng `apply_patch`.
4. Compile.
5. UAT với SharePoint session thật.

Verify:

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\Project_V11_SharePoint_Capture\capture_v11_sharepoint.py .\config.py
```

PASS khi:

- Code compile.
- Có UAT note.
- Docs mô tả đúng tính năng thật.

---

## 6. Hướng C: rebuild production

Chỉ làm nếu user xác nhận V11 vẫn quan trọng.

Thiết kế tối thiểu:

- Config output vào `outputs/v11_sharepoint/`.
- Có mode test giới hạn trang.
- Có duplicate detection hoặc visual stop để không loop vô hạn.
- Có run summary JSON.
- Nếu dùng desktop automation, có focus/click rõ như V12.
- Nếu dùng browser/CDP, ghi rõ URL/session và selector/JS dùng.

Không build quá rộng trước khi có SharePoint document thật để UAT.

---

## 7. Tiêu chí PASS chung

PASS khi một quyết định được ghi rõ:

- `V11 = basic` và docs đồng bộ, hoặc
- `V11 = restored/rebuilt` và có compile + UAT evidence.

FAIL khi:

- Chỉ sửa docs cho đẹp nhưng code không khớp.
- Claim production mà không có UAT.
- Tự động chạy SharePoint desktop khi user chưa chuẩn bị cửa sổ.

---

## 8. File được phép sửa

- `Project_V11_SharePoint_Capture/capture_v11_sharepoint.py`
- `PROJECT_STATUS.md`
- `README.md`
- `Implementation Plan/incident_04_v11_sharepoint_production_gap_20260527.md`
- UAT note mới trong `Implementation Plan/`
