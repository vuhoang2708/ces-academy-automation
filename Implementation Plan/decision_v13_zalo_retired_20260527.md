# Decision Note: V13 Zalo — Hướng B (Quarantine/Retired → V14)

**Ngày:** 2026-05-27
**Handoff gốc:** `Agent Handoff/remaining_04_v13_zalo_decision_20260527.md`
**Quyết định:** **Hướng B — giữ quarantine stub, mọi Zalo media work chuyển sang V14**

---

## Căn cứ quyết định

### Git history review

```
git log --oneline --all -- Project_V13_Media_Downloader/v13_zalo_media_downloader.py
7e1eb4a stabilize CES automation and add AI sidecar plans
524a8e7 refactor: Re-organize workspace into separate V11, V12, V13 folders
```

Kiểm tra nội dung commit 524a8e7 (reorganize):

```
git show 524a8e7:Project_V13_Media_Downloader/v13_zalo_media_downloader.py
→ UTF-16 LE, 32 bytes, 15 null bytes, nội dung: "import cv2..."
```

File trong commit reorganize là **corrupt** (UTF-16 với null bytes). Không có source
hợp lệ nào trong toàn bộ Git history. Commit 3a97ac8 (initial) không có file này.

### Trạng thái hiện tại (đã xác nhận)

- `v13_zalo_media_downloader.py`: stub compile-safe, in thông báo unavailable rõ ràng.
- `Project_V13_Media_Downloader/INFO.md`: đã ghi V13 Zalo = quarantined/unavailable.
- `PROJECT_STATUS.md`: đã ghi V13 Zalo = Quarantined/unavailable.
- `launcher_gui.py`: **không có nút V13 Zalo** — đã bị bỏ trước handoff này.
- Compile: **PASS** (`python -m py_compile` exit 0).

### Lý do chọn Hướng B

- Không có source hợp lệ để restore (Hướng A không khả thi).
- V14 đang là hướng diagnostic cho Zalo Desktop media — đây là forward path đúng.
- Giữ stub rõ ràng tốt hơn là để trống hoặc để file corrupt.

---

## Trạng thái sau quyết định

| Tiêu chí | Kết quả |
|---|---|
| Quyết định ghi rõ: V13 Zalo = RETIRED | PASS |
| Stub compile-safe | PASS |
| Stub in thông báo rõ khi chạy | PASS |
| Launcher không có nút V13 Zalo | PASS (đã bỏ trước) |
| PROJECT_STATUS.md đồng bộ | PASS |
| INFO.md đồng bộ | PASS |
| UAT thật với Zalo Desktop | N/A — module retired |

---

## Forward path

Mọi Zalo Desktop media automation tiếp tục theo **V14 Zalo Diagnostic**:
- Script: `Project_V14_Zalo_Media_Downloader/zalo_media_v14.py`
- Launcher: nút "V14 - Zalo Diagnostic Capture" trong `launcher_gui.py`

Nếu cần restore V13 Zalo trong tương lai, cần tìm backup ngoài repo (không có trong Git history).
