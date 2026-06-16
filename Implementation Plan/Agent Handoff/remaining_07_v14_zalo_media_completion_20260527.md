# Handoff 07: Hoàn Thiện V14 Zalo Desktop Media Downloader

**Ưu tiên:** P2
**Loại việc:** desktop automation + UAT thật
**Module:** `Project_V14_Zalo_Media_Downloader/zalo_media_v14.py`
**Plan gốc:** `incident_06_v14_zalo_desktop_completion_20260527.md`

---

## 1. Mục tiêu

Biến V14 từ diagnostic thành downloader end-to-end cho Zalo Desktop media, nhưng chỉ khi có Zalo window thật để UAT.

Không gọi V14 là production cho đến khi tải media thật thành công và có run summary.

---

## 2. Trạng thái hiện tại đã xác nhận

- V14 hiện là diagnostic only.
- Chưa có luồng hoàn chỉnh:
  - tìm media panel,
  - template matching nút download,
  - Save As,
  - duplicate handling,
  - run summary.
- Launcher nếu gọi V14 phải label rõ diagnostic.

---

## 3. Điều kiện vào việc

1. User mở Zalo Desktop đúng chat có media.
2. User đồng ý agent thao tác desktop bằng PyAutoGUI.
3. Agent chạy dry-run trước execute.
4. Output media giữ local-only, không commit.

---

## 4. Thiết kế mode bắt buộc

V14 phải có ít nhất 3 mode:

```text
--mode diagnostic
--mode dry-run
--mode execute
```

- `diagnostic`: chụp screenshot, detect cửa sổ, ghi tọa độ.
- `dry-run`: tìm nút/media, log hành động dự kiến, không click download.
- `execute`: click và tải thật.

Không cho execute nếu diagnostic chưa pass.

---

## 5. Bước implementation tối thiểu

1. Dùng shared Zalo window restore/focus giống V12.
2. Chụp screenshot toàn cửa sổ và crop vùng media.
3. Tạo calibration log:
   - window title,
   - rect,
   - focus click,
   - screenshot path,
   - confidence template.
4. Tìm media item/nút download bằng template hoặc tọa độ calibrated.
5. Thêm duplicate detection bằng hash file hoặc image hash.
6. Tải vào `downloads/v14_zalo_media/`.
7. Ghi `latest_run_summary.json`.
8. Tạo optional AI sidecar/media inventory nếu Handoff 05 đã xong.

---

## 6. Lệnh verify

Compile:

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\Project_V14_Zalo_Media_Downloader\zalo_media_v14.py
```

Diagnostic:

```powershell
& $py .\Project_V14_Zalo_Media_Downloader\zalo_media_v14.py --mode diagnostic
```

Dry-run:

```powershell
& $py .\Project_V14_Zalo_Media_Downloader\zalo_media_v14.py --mode dry-run --max-items 3
```

Execute nhỏ:

```powershell
& $py .\Project_V14_Zalo_Media_Downloader\zalo_media_v14.py --mode execute --max-items 1
```

---

## 7. Tiêu chí PASS

PASS diagnostic:

- Detect đúng cửa sổ Zalo.
- Screenshot không blank.
- Tọa độ focus nằm trong vùng chat/media hợp lý.

PASS dry-run:

- Tìm được item/nút dự kiến.
- Không tải file thật.
- Có log hành động.

PASS execute:

- Tải được ít nhất 1 media thật.
- File tải có size > 0 và MIME/extension hợp lý.
- Có summary JSON.
- Docs/status cập nhật từ diagnostic lên validated test nếu đạt.

FAIL khi:

- Click mù không có tọa độ/log.
- Execute chạy khi window minimized hoặc focus sai.
- Tải trùng lặp liên tục không dừng.

---

## 8. File được phép sửa

- `Project_V14_Zalo_Media_Downloader/zalo_media_v14.py`
- `launcher_gui.py` nếu label/nút V14 cần sửa
- `PROJECT_STATUS.md`
- `README.md`
- UAT note trong `Implementation Plan/`

Không commit:

- `downloads/v14_zalo_media/`
- screenshot/media Zalo private.
