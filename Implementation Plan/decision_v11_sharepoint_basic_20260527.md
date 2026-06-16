# Decision Note: V11 SharePoint — Hướng A (Basic/Skeleton)

**Ngày:** 2026-05-27
**Handoff gốc:** `Agent Handoff/remaining_03_v11_sharepoint_decision_20260527.md`
**Quyết định:** **Hướng A — giữ V11 là basic screenshot extractor**

---

## Căn cứ quyết định

### Git history review

```
git log --oneline --all -- Project_V11_SharePoint_Capture/capture_v11_sharepoint.py
524a8e7 refactor: Re-organize workspace into separate V11, V12, V13 folders
```

Chỉ có một commit duy nhất chứa file này (commit reorganize). Không có bản production
nào trong Git history với CV auto-stop, CSS injection, CDP, hay ẩn toolbar Microsoft.

### Code hiện tại (đã xác nhận)

- `pyautogui.screenshot()` + `pyautogui.press('pagedown')` trong vòng lặp cố định.
- Không có CV, không có CDP, không có config.py integration.
- Compile: **PASS** (`python -m py_compile` exit 0).

### Lý do chọn Hướng A

- Không có source production hợp lệ để restore (Hướng B không khả thi).
- V11 SharePoint không phải ưu tiên ngay trong sprint hiện tại (Hướng C chưa cần).
- Giữ basic và docs đúng tốt hơn là claim production khi chưa có UAT.

---

## Thay đổi đã thực hiện

| File | Thay đổi |
|---|---|
| `Project_V11_SharePoint_Capture/capture_v11_sharepoint.py` | Thêm module docstring rõ limitation; bỏ unused `datetime` import; format code nhất quán |
| `Project_V11_SharePoint_Capture/INFO.md` | Tạo mới — mô tả tính năng có/chưa có, điều kiện UAT |
| `PROJECT_STATUS.md` | Giữ nguyên `Skeleton/basic screenshot` — đã đúng |
| `README.md` | Giữ nguyên — V11 section không claim production features |

---

## Tiêu chí PASS

- [x] Quyết định được ghi rõ: `V11 = basic/skeleton`
- [x] Docs (INFO.md + docstring) không claim CV/CDP/CSS
- [x] Code compile: PASS
- [x] PROJECT_STATUS.md đồng bộ
- [ ] UAT thật với SharePoint session: **PENDING** — cần user chuẩn bị cửa sổ SharePoint

---

## Điều kiện để nâng cấp V11 lên production

1. User xác nhận V11 SharePoint là ưu tiên.
2. Thiết kế theo Hướng C trong handoff gốc (CV stop, config.py, run summary).
3. UAT với tài liệu SharePoint thật.
4. Tạo UAT evidence note mới.
