# Decision Note: Plan 07 — V14 Zalo Media Completion

**Ngày:** 2026-05-27  
**Handoff gốc:** `Agent Handoff/remaining_07_v14_zalo_media_completion_20260527.md`  
**Verdict:** **DRY_RUN_READY**

---

## Thay đổi đã thực hiện

| File | Thay đổi |
|---|---|
| `Project_V14_Zalo_Media_Downloader/zalo_media_v14.py` | Rewrite hoàn toàn — 3-mode CLI, config.py integration, run summary JSON |

---

## Kết quả verify

```powershell
# Compile
python -m py_compile Project_V14_Zalo_Media_Downloader/zalo_media_v14.py → exit 0

# Diagnostic (Zalo Desktop đang mở)
python zalo_media_v14.py --mode diagnostic
→ Window found: title='Zalo' rect={'left': -8, 'top': -8, 'width': 1296, 'height': 816}
→ Screenshot saved: outputs/v14_zalo_diagnostic/diag_20260527_140703.png
→ Diagnostic PASS

# Dry-run
python zalo_media_v14.py --mode dry-run --max-items 3
→ 3 planned actions logged. No files downloaded.
→ Dry-run PASS
```

---

## Trạng thái từng mode

| Mode | Trạng thái | Ghi chú |
|---|---|---|
| `--mode diagnostic` | PASS | Detect window, chụp screenshot, log rect/coordinates |
| `--mode dry-run` | PASS | Log planned actions, không click, không download |
| `--mode execute` | PARTIAL/BLOCKED | Cần calibration screenshot review trước khi dùng |

---

## Execute mode — điều kiện để PASS

Execute mode hiện tại:
1. Kiểm tra diagnostic screenshot tồn tại (guard).
2. Activate Zalo window.
3. Thử Ctrl+Shift+M để mở media panel.
4. Chụp post-action screenshot.

Để PASS execute hoàn toàn cần thêm:
- Review screenshot diagnostic để xác định tọa độ media panel.
- Template matching hoặc tọa độ calibrated cho nút download.
- Duplicate detection bằng file hash.
- Tải ít nhất 1 media thật với size > 0.

---

## Output local-only

- `outputs/v14_zalo_diagnostic/diag_*.png` — screenshot diagnostic (trong .gitignore qua `outputs/`)
- `outputs/v14_zalo_diagnostic/dryrun_*.png` — screenshot dry-run
- `outputs/v14_zalo_diagnostic/latest_run_summary.json`
- `downloads/v14_zalo_media/` — output media khi execute (chưa có file)

---

## Chưa xác minh được

- Execute với media thật: cần user mở chat Zalo có media và chạy `--mode execute`.
- Template matching: chưa có template image calibrated.
- Duplicate detection: code có `_file_hash()` nhưng chưa dùng trong execute flow.
