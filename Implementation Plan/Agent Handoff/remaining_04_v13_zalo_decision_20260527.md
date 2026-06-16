# Handoff 04: Quyết Định V13 Zalo Legacy Hay Chuyển Sang V14

**Ưu tiên:** P1
**Loại việc:** scope decision + optional restore
**Module:** `Project_V13_Media_Downloader/v13_zalo_media_downloader.py`
**Plan gốc:** `incident_01_v13_zalo_file_corrupt_20260527.md`

---

## 1. Mục tiêu

Chốt số phận V13 Zalo:

- Restore legacy downloader nếu có code hợp lệ và còn dùng được.
- Hoặc giữ quarantine/stub và chuyển mọi Zalo media work sang V14.

Không viết lại hai hướng song song nếu chưa có quyết định, vì sẽ tạo drift mới.

---

## 2. Trạng thái hiện tại đã xác nhận

- File cũ từng corrupt/null bytes.
- Hiện file đã được thay bằng stub compile-safe báo module unavailable.
- Docs/status đã phân biệt V13 Facebook với V13 Zalo.
- V14 đang là hướng diagnostic cho Zalo Desktop media.

---

## 3. Bước 1: tìm nguồn restore

```powershell
git status --short --branch
git log --oneline --all -- Project_V13_Media_Downloader/v13_zalo_media_downloader.py
git log --oneline --all -- \"*zalo*\" \"*Zalo*\"
rg -n \"v13_zalo|Zalo Media|download|template|Save As|media panel\" .
```

Nếu có commit cũ:

```powershell
git show <commit>:Project_V13_Media_Downloader/v13_zalo_media_downloader.py
```

Nếu có backup ngoài repo, phải ghi rõ path backup và checksum/hash nếu có.

---

## 4. Hướng A: restore V13 Zalo

Chỉ làm nếu:

- Có source code hợp lệ.
- Code compile được.
- User vẫn muốn V13 Zalo legacy sống riêng với V14.

Các bước:

1. Restore thủ công bằng `apply_patch`.
2. Bỏ hardcoded path, dùng `config.py`.
3. Thêm mode dry-run nếu script thao tác desktop.
4. Thêm run summary.
5. Compile.
6. UAT trên Zalo Desktop thật.

Verify:

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\Project_V13_Media_Downloader\v13_zalo_media_downloader.py
```

---

## 5. Hướng B: giữ quarantine và chuyển sang V14

Khuyến nghị nếu không tìm được source hợp lệ.

Cần làm:

- Giữ `v13_zalo_media_downloader.py` là stub rõ ràng.
- `PROJECT_STATUS.md`: V13 Zalo = quarantined/unavailable.
- `README.md`: Zalo media mới theo V14.
- `launcher_gui.py`: nếu có nút V13 Zalo, label phải là unavailable hoặc không cho chạy nhầm.

PASS khi user/agent gọi script thì nhận thông báo rõ, không crash bằng null byte/syntax error.

---

## 6. Tiêu chí PASS

PASS khi có quyết định rõ:

- `RESTORED`: code compile + UAT note + docs cập nhật, hoặc
- `RETIRED`: stub giữ lại + docs/status nói mọi Zalo media chuyển sang V14.

FAIL khi:

- Restore code cũ nhưng không compile.
- Vừa gọi V13 Zalo unavailable vừa docs claim functional.
- Không ghi quyết định vào status.

---

## 7. File được phép sửa

- `Project_V13_Media_Downloader/v13_zalo_media_downloader.py`
- `Project_V13_Media_Downloader/INFO.md`
- `README.md`
- `PROJECT_STATUS.md`
- `launcher_gui.py` nếu cần tránh chạy nhầm
- UAT/decision note mới trong `Implementation Plan/`
