# Gemini Browser UAT Script: Test Các Phần Chưa PASS

**Ngày:** 2026-05-28
**Mục tiêu:** Dùng Gemini/agent có browser để test lại những phần chưa test được vì thiếu session thật hoặc thiếu calibration.
**Phạm vi:** V10 CES live capture, V13 Facebook live downloader, V14 Zalo dry-run/execute calibration, Hub browser smoke test.

---

## 1. Nguyên Tắc Bắt Buộc

- Không upload dữ liệu riêng tư từ CES/Facebook/Zalo lên Gemini, Google Drive, NotebookLM hoặc cloud.
- Không commit `outputs/`, `downloads/`, `zalo_captures/`, `*_AI_ANALYSIS.md`, `*_AI_ANALYSIS.json`.
- Không gọi PASS nếu chỉ compile, chỉ mở được login page, hoặc chỉ tạo summary lỗi.
- Nếu browser tool dùng browser riêng không có CDP port, phải nói rõ và không giả vờ Python script đã dùng được session đó.
- Nếu cần login CES/Facebook, user phải tự thao tác credential. Agent không được yêu cầu user gửi password.
- Mọi raw output chứa dữ liệu thật phải để local-only.

---

## 2. Prompt Tổng Cho Gemini Browser Agent

Paste đoạn này cho Gemini/agent:

```text
Bạn đang làm trong repo:

c:\Users\vu.hoang\.gemini\antigravity\scratch\ces-academy-automation

Nhiệm vụ: dùng browser để test lại các phần đang PARTIAL/DRY_RUN_READY:

1. V10 CES Web Capture: cần Chrome/CES session đã đăng nhập.
2. V13 Facebook Downloader: cần Chrome debug port 9222 có tab Facebook đã đăng nhập.
3. V14 Zalo: browser-assisted review diagnostic/dry-run outputs và Hub endpoints; không execute Zalo nếu chưa được user duyệt desktop automation.
4. Hub Server: browser smoke test các endpoint local.

Bắt đầu bằng:

git status --short --branch

Đọc trước:
- PROJECT_STATUS.md
- Implementation Plan/uat_v10_ces_live_partial_20260527.md
- Implementation Plan/uat_v13_facebook_live_partial_20260527.md
- Implementation Plan/decision_plan07_v14_zalo_dryrun_20260527.md
- Implementation Plan/decision_plan08_hub_server_minimal_20260527.md
- capture_antigravity.py
- Project_V13_Media_Downloader/v13_fb_media_downloader.py
- Project_V14_Zalo_Media_Downloader/zalo_media_v14.py
- hub_server.py
- config.py

Không được claim PASS nếu không có source evidence:
- V10 PASS cần summary không còn blocked_login và screenshot viewer thật.
- V13 PASS cần Facebook tab/session thật và summary có posts_found > 0 hoặc media/content saved.
- V14 EXECUTE_VALIDATED cần tải ít nhất 1 media thật với file size > 0 và summary JSON. Nếu chỉ diagnostic/dry-run thì verdict vẫn DRY_RUN_READY.
- Hub browser smoke test PASS chỉ chứng minh endpoint local chạy, không chứng minh run API/Portal hoàn chỉnh.

Cuối cùng tạo UAT note mới trong Implementation Plan/ và cập nhật PROJECT_STATUS.md nếu trạng thái thay đổi.
```

---

## 3. Kịch Bản A: V10 CES Browser Login + Capture

### Mục tiêu

Chuyển V10 từ:

```text
Partial UAT, blocked by login
```

sang PASS nếu có CES session thật.

### Browser Steps

1. Mở Chrome debug riêng hoặc kiểm tra port đang có.
2. Vào CES Academy bằng browser.
3. Nếu thấy login page, yêu cầu user tự đăng nhập trong browser đó.
4. Sau login, mở viewer tài liệu cần capture.
5. Xác nhận URL không còn là:

```text
https://academy.cesglobal.com.vn/login.html
```

### PowerShell Preflight

```powershell
git status --short --branch

$ports = @(9333, 9444, 9555)
foreach ($port in $ports) {
  try {
    $tabs = (Invoke-WebRequest -UseBasicParsing "http://localhost:$port/json" -TimeoutSec 3).Content | ConvertFrom-Json
    Write-Host "PORT $port OPEN tabs=$($tabs.Count)"
    $tabs | Where-Object { $_.url -like "*academy*" -or $_.url -like "*cesglobal*" } | ForEach-Object {
      Write-Host "  CES: $($_.url)"
    }
  } catch {
    Write-Host "PORT $port CLOSED"
  }
}
```

### Nếu cần mở Chrome debug mới

Chỉ làm nếu user đồng ý login trong profile tạm:

```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$profile = "$env:TEMP\ces-browser-uat-9555"
& $chrome --remote-debugging-port=9555 --user-data-dir="$profile" --no-first-run
```

Sau đó user đăng nhập CES trong Chrome đó.

### Chạy Capture Nhỏ

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\capture_antigravity.py .\config.py

$env:CES_VIEWER_CDP_PORT = "9555"
$env:CES_V10_TOTAL_PAGES = "5"
& $py .\capture_antigravity.py
```

Đổi `9555` thành port thật có CES session.

### Verify PASS

```powershell
Get-Content .\outputs\v10_ces_web_capture\latest_run_summary.json -Encoding UTF8
Get-ChildItem .\outputs\v10_ces_web_capture -Recurse | Select-Object FullName,Length,LastWriteTime
git check-ignore -v .\outputs .\outputs\v10_ces_web_capture\latest_run_summary.json
```

PASS nếu:

- `status` là `captured` hoặc `pdf_created`.
- `current_url` là viewer/tài liệu thật, không phải login.
- Screenshot đầu tiên không phải login page.
- PDF được tạo từ nội dung học liệu thật.

Nếu PASS, tạo:

```text
Implementation Plan/uat_v10_ces_browser_live_pass_20260528.md
```

Nếu vẫn fail, tạo:

```text
Implementation Plan/uat_v10_ces_browser_live_partial_20260528.md
```

---

## 4. Kịch Bản B: V13 Facebook Browser Session + Downloader

### Mục tiêu

Chuyển V13 Facebook từ:

```text
Partial UAT, blocked by missing Facebook tab/session on CDP 9222
```

sang PASS nếu có Facebook session thật.

### Browser Steps

1. Mở Chrome debug port `9222`.
2. User tự đăng nhập Facebook trong Chrome đó nếu cần.
3. Mở group/page cần capture.
4. Kiểm tra `/json` có ít nhất một tab URL chứa `facebook.com`.

### Mở Chrome Debug

```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$profile = "$env:TEMP\ces-facebook-cdp-9222"
& $chrome --remote-debugging-port=9222 --user-data-dir="$profile" --no-first-run
```

### Kiểm Tra CDP Và Tab Facebook

```powershell
$tabs = (Invoke-WebRequest -UseBasicParsing "http://localhost:9222/json" -TimeoutSec 3).Content | ConvertFrom-Json
$tabs | ForEach-Object { Write-Host "[$($_.type)] $($_.url)" }
$fbTabs = $tabs | Where-Object { $_.url -like "*facebook.com*" }
Write-Host "FB tabs: $($fbTabs.Count)"
```

Không chạy downloader nếu `FB tabs: 0`, trừ khi mục tiêu là tạo failure summary.

### Chạy Downloader Nhỏ

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\Project_V13_Media_Downloader\v13_fb_media_downloader.py .\config.py

$env:CES_V13_MAX_POSTS = "3"
$env:CES_V13_MAX_MEDIA_PER_POST = "5"
$env:CES_FORCE_DOWNLOAD = "0"
& $py .\Project_V13_Media_Downloader\v13_fb_media_downloader.py
```

### Verify PASS

```powershell
Get-Content .\downloads\v13_facebook\latest_run_summary.json -Encoding UTF8
Get-ChildItem .\downloads\v13_facebook -Recurse | Select-Object FullName,Length,LastWriteTime
git check-ignore -v .\downloads .\downloads\v13_facebook\latest_run_summary.json
```

PASS nếu:

- Không còn lỗi chỉ là `no_facebook_tab_or_cdp_unavailable`.
- `posts_found > 0`, hoặc `posts_saved > 0`, hoặc `media_downloaded > 0`.
- Nếu không có media, vẫn cần `content.txt` hoặc evidence đã đọc được post text.

Nếu PASS, tạo:

```text
Implementation Plan/uat_v13_facebook_browser_live_pass_20260528.md
```

Nếu vẫn fail, tạo:

```text
Implementation Plan/uat_v13_facebook_browser_live_partial_20260528.md
```

---

## 5. Kịch Bản C: V14 Browser-Assisted Calibration Và Hub Smoke Test

### Mục tiêu

V14 hiện là `DRY_RUN_READY`, chưa execute validated. Browser có thể hỗ trợ:

- mở ảnh diagnostic/dry-run để review vùng media;
- test Hub endpoints bằng browser;
- không thay thế desktop automation test.

### Browser Review Diagnostic PNG

Nếu có file:

```text
outputs/v14_zalo_diagnostic/latest_run_summary.json
outputs/v14_zalo_diagnostic/diag_*.png
outputs/v14_zalo_diagnostic/dryrun_*.png
```

Mở ảnh local bằng browser hoặc viewer, rồi ghi nhận:

- Zalo window có đúng chat không?
- Media panel có hiện không?
- Có vùng nút download/media item nào xác định được không?
- Có thể đề xuất tọa độ tương đối theo window rect không?

Không click Zalo thật nếu user chưa duyệt execute.

### Chạy Diagnostic/Dry-run Lại Nếu User Đồng Ý

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\Project_V14_Zalo_Media_Downloader\zalo_media_v14.py

& $py .\Project_V14_Zalo_Media_Downloader\zalo_media_v14.py --mode diagnostic
& $py .\Project_V14_Zalo_Media_Downloader\zalo_media_v14.py --mode dry-run --max-items 3
```

Verdict vẫn là `DRY_RUN_READY` nếu chưa execute tải media thật.

### Hub Browser Smoke Test

Start server:

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py .\hub_server.py --port 8768
```

Mở bằng browser:

```text
http://127.0.0.1:8768/health
http://127.0.0.1:8768/modules
http://127.0.0.1:8768/artifacts
```

PASS nếu browser thấy JSON hợp lệ:

- `/health` có `status: ok`;
- `/modules` có danh sách module từ `PROJECT_STATUS.md`;
- `/artifacts` đọc từ `outputs_manifest.jsonl`.

Tạo note:

```text
Implementation Plan/uat_v14_browser_calibration_partial_20260528.md
Implementation Plan/uat_hub_browser_smoke_20260528.md
```

---

## 6. Final Packaging Cho Agent

Sau khi chạy một hoặc nhiều kịch bản:

```powershell
git diff --check

$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\capture_antigravity.py .\Project_V13_Media_Downloader\v13_fb_media_downloader.py .\Project_V14_Zalo_Media_Downloader\zalo_media_v14.py .\hub_server.py

git check-ignore -v .\outputs .\downloads .\zalo_captures
git status --short --branch
```

Commit only docs/code/status, never raw outputs:

```powershell
git add PROJECT_STATUS.md "Implementation Plan/<new_uat_note>.md"
git commit -m "browser-uat open blockers"
git push origin codex/ces-ai-stabilization
```

Final report format:

```text
V10 CES browser UAT: PASS/PARTIAL/FAIL
V13 Facebook browser UAT: PASS/PARTIAL/FAIL
V14 browser-assisted calibration: DRY_RUN_READY/EXECUTE_VALIDATED/PARTIAL
Hub browser smoke: PASS/PARTIAL/FAIL

Browser/session used:
CDP ports:
Raw outputs created local-only:
Files committed:
Commit hash/push:
Git status final:
```
