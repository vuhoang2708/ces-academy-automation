# Handoff 09: Dọn Hai Plan V13 Cũ Đang Untracked

**Ưu tiên:** P2
**Loại việc:** repo hygiene + docs consistency
**File liên quan:**

- `Project_V13_Media_Downloader/implementation_plan_20260419_UAT_V13_FB.md`
- `Project_V13_Media_Downloader/implementation_plan_20260419_V13_Timeline.md`

---

## 1. Mục tiêu

Hai file plan cũ đang untracked và có trạng thái `WAITING FOR APPROVAL`. Chúng có thể làm agent khác hiểu nhầm vì:

- Ghi output path cũ `v13_fb_downloads`.
- Nhắc port `9222`; đây vẫn là default của V13 Facebook, nhưng docs cũ chưa nói rõ phải đọc từ `config.py` và khác với V10 viewer port `9333`.
- Không phản ánh hardening hiện tại của V13 Facebook.
- Chưa được đồng bộ với AI sidecar/second brain plan.

Mục tiêu là quyết định archive, rewrite, hoặc xóa theo approval của user.

---

## 2. Trạng thái hiện tại đã xác nhận

`git status` hiện có:

```text
?? Project_V13_Media_Downloader/implementation_plan_20260419_UAT_V13_FB.md
?? Project_V13_Media_Downloader/implementation_plan_20260419_V13_Timeline.md
```

Các file này chưa nằm trong commit hiện tại.

---

## 3. Hướng A: archive làm tài liệu lịch sử

Khuyến nghị nếu muốn giữ lại bối cảnh cũ.

Các bước:

1. Tạo folder:

```text
Implementation Plan/Archived/
```

2. Di chuyển hai file vào đó.
3. Thêm đầu file:

```text
Archive note: File này là plan cũ ngày 2026-04-19, không còn là nguồn hướng dẫn hiện tại. Xem handoff mới trong Implementation Plan/Agent Handoff/.
```

4. Commit archive nếu không chứa private content.

---

## 4. Hướng B: rewrite thành UAT docs mới

Làm nếu muốn biến chúng thành tài liệu active.

Yêu cầu:

- Giữ port `9222` nếu nói về V13 Facebook, nhưng phải ghi rõ đây là default đọc từ `config.py`; không lẫn với V10 viewer port `9333`.
- Update output từ `v13_fb_downloads` sang `downloads/v13_facebook/`.
- Link tới `remaining_01_v13_facebook_live_uat_20260527.md`.
- Bỏ status `WAITING FOR APPROVAL` nếu đã có handoff mới.
- Thêm privacy rule: không commit `downloads/`.

---

## 5. Hướng C: xóa

Chỉ làm nếu user duyệt xóa.

Lệnh xóa phải rõ path:

```powershell
Remove-Item -LiteralPath 'Project_V13_Media_Downloader/implementation_plan_20260419_UAT_V13_FB.md'
Remove-Item -LiteralPath 'Project_V13_Media_Downloader/implementation_plan_20260419_V13_Timeline.md'
```

Không xóa bằng wildcard.

---

## 6. Tiêu chí PASS

PASS khi:

- `git status --short` không còn hai file untracked gây nhiễu, hoặc có ghi chú rõ vì sao giữ untracked.
- Nếu archive/rewrite, docs không còn mâu thuẫn với `PROJECT_STATUS.md`.
- Không làm mất thông tin nếu user muốn giữ lịch sử.

FAIL khi:

- Commit file cũ nguyên trạng khiến agent khác chạy nhầm port/path cũ.
- Xóa file không có approval.
- Di chuyển file nhưng không ghi archive note.

---

## 7. File được phép sửa

- Hai file plan cũ nêu trên.
- `Implementation Plan/Archived/` nếu tạo archive.
- `Implementation Plan/Agent Handoff/remaining_plan_index_20260527.md` nếu cần cập nhật trạng thái.
