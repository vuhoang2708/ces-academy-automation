# Handoff 01: Live UAT V13 Facebook Downloader

**Ưu tiên:** P1
**Loại việc:** UAT + docs update
**Module:** `Project_V13_Media_Downloader/v13_fb_media_downloader.py`
**Plan gốc:** `incident_05_v13_facebook_hardening_20260527.md`

---

## 1. Mục tiêu

Kiểm thử live V13 Facebook downloader sau khi đã harden code. Mục tiêu không phải viết thêm tính năng mới ngay, mà là chứng minh script hiện tại còn chạy được với Facebook session thật, có summary rõ, và không âm thầm fail.

---

## 2. Trạng thái hiện tại đã xác nhận

- Script chính đã được harden với timeout, MIME check, streaming download và run summary.
- Output mặc định chuyển về `downloads/v13_facebook/`.
- Repo vẫn ghi V13 Facebook là “hardened script, cần live UAT”.
- Có UAT guide: `UAT_V13_FB_GUIDE.md`.

Chưa xác minh:

- Facebook DOM/session hiện tại có cho script đọc bài viết/media không.
- Summary JSON có đủ counter thành công/thất bại trong run thật không.
- Có cần đăng nhập bằng Chrome profile của user hay dùng browser đang mở sẵn.

---

## 3. Điều kiện vào việc

Trước khi chạy:

1. User đã mở Facebook group/page cần capture trong Chrome đăng nhập thật.
2. Chrome phải có CDP debug port đúng với `config.py`, mặc định V13 Facebook là `9222`.
3. User biết script sẽ cuộn/đọc trang Facebook đang mở.
4. Không upload output Facebook lên GitHub hoặc cloud.

---

## 4. Lệnh chuẩn bị

Chạy từ root repo:

```powershell
git status --short --branch
Get-Content .\UAT_V13_FB_GUIDE.md -Encoding UTF8
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\Project_V13_Media_Downloader\v13_fb_media_downloader.py .\config.py
```

Nếu cần mở Chrome debug mới:

```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
& $chrome --remote-debugging-port=9222 --user-data-dir="$env:TEMP\ces-chrome-cdp-9222"
```

Nếu user đã có Chrome đăng nhập thật, ưu tiên dùng Chrome đó nếu có thể bật debug port theo cách an toàn.

---

## 5. Lệnh chạy UAT

Giới hạn nhỏ để tránh tải quá nhiều:

```powershell
$env:CES_V13_MAX_POSTS = "3"
$env:CES_V13_MAX_MEDIA_PER_POST = "5"
$env:CES_FORCE_DOWNLOAD = "0"
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py .\Project_V13_Media_Downloader\v13_fb_media_downloader.py
```

Nếu run quá rộng hoặc có dữ liệu nhạy cảm, dừng và ghi rõ partial result.

---

## 6. Cần kiểm tra sau khi chạy

Kiểm tra output:

```powershell
Get-ChildItem .\downloads\v13_facebook -Force
Get-Content .\downloads\v13_facebook\latest_run_summary.json -Encoding UTF8
```

Kiểm tra không stage output riêng tư:

```powershell
git check-ignore -v .\downloads\v13_facebook\latest_run_summary.json
git status --short
```

Nếu summary bị ignore đúng thì không commit file output.

---

## 7. Tiêu chí PASS

PASS khi có đủ:

- Script kết nối CDP được hoặc fail với lỗi rõ ràng.
- Nếu có quyền đọc trang, script tạo `downloads/v13_facebook/latest_run_summary.json`.
- Summary có counter hoặc danh sách media/post đã xử lý.
- Có ít nhất một artifact tải được, hoặc có lý do rõ vì sao không tải được.
- `PROJECT_STATUS.md`/UAT note được cập nhật kết quả thật.

PARTIAL khi:

- Không vào được Facebook do login/session/CDP, nhưng lỗi được ghi rõ và không crash mơ hồ.

FAIL khi:

- Script treo không timeout.
- Không có summary.
- Download file sai MIME nhưng vẫn báo success.

---

## 8. File được phép sửa

- `UAT_V13_FB_GUIDE.md`
- `PROJECT_STATUS.md`
- `Project_V13_Media_Downloader/v13_fb_media_downloader.py` nếu chỉ sửa bug phát hiện trong UAT
- Một UAT note mới trong `Implementation Plan/`, ví dụ `uat_v13_facebook_20260527.md`

Không sửa:

- Không rewrite toàn bộ V13 khi chỉ đang làm UAT.
- Không stage `downloads/`.

---

## 9. Mẫu báo cáo cuối

```text
V13 Facebook live UAT: PASS/PARTIAL/FAIL

CDP port:
Chrome/session:
Số post đọc được:
Số media tải được:
Summary path:
Lỗi chính nếu có:
File docs đã cập nhật:
Raw output đã giữ local-only:
```

---

## 10. Lượt chạy Codex 2026-05-27

Kết quả: PARTIAL.

- Compile pass.
- Không có Chrome debug tại `http://localhost:9222/json`.
- Script đã được sửa để vẫn tạo `downloads/v13_facebook/latest_run_summary.json` khi thiếu CDP/tab Facebook.
- Xem chi tiết: `Implementation Plan/uat_v13_facebook_partial_20260527.md`.
