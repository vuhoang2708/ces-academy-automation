# UAT Result: V13 Facebook Downloader

**Ngày chạy:** 2026-05-27
**Người chạy:** Codex
**Kết quả:** PARTIAL
**Module:** `Project_V13_Media_Downloader/v13_fb_media_downloader.py`

---

## 1. Mục tiêu

Chạy Handoff 01 để kiểm tra V13 Facebook downloader sau hardening:

- compile script;
- chạy với giới hạn nhỏ;
- xác nhận khi thiếu Chrome CDP/tab Facebook thì script fail có summary, không fail im lặng.

---

## 2. Lệnh đã chạy

```powershell
$py = 'C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe'
& $py -m py_compile .\config.py .\capture_antigravity.py .\Project_V13_Media_Downloader\v13_fb_media_downloader.py
```

```powershell
$env:CES_V13_MAX_POSTS='3'
$env:CES_V13_MAX_MEDIA_PER_POST='5'
$env:CES_FORCE_DOWNLOAD='0'
$py = 'C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe'
& $py .\Project_V13_Media_Downloader\v13_fb_media_downloader.py
```

---

## 3. Kết quả thực tế

Script không kết nối được Chrome debug tại:

```text
http://localhost:9222/json
```

Lỗi runtime:

```text
No connection could be made because the target machine actively refused it
```

Sau khi sửa, script đã tạo summary thay vì thoát im lặng:

```text
downloads/v13_facebook/latest_run_summary.json
```

Nội dung summary chính:

```json
{
  "posts_found": 0,
  "posts_saved": 0,
  "media_attempted": 0,
  "media_downloaded": 0,
  "media_failed": 0,
  "media_skipped": 0,
  "errors": [
    {
      "reason": "no_facebook_tab_or_cdp_unavailable:http://localhost:9222/json"
    }
  ]
}
```

---

## 4. Đánh giá

PARTIAL, không phải PASS live UAT.

Đã xác minh:

- Script compile được.
- Failure path khi thiếu CDP đã có summary.
- Output summary nằm trong `downloads/` và được `.gitignore` bảo vệ.

Chưa xác minh:

- Chưa đọc được Facebook DOM thật.
- Chưa tải được post/media thật.
- Chưa kiểm tra MIME/download trong live session.

---

## 5. Fix đã thực hiện

Sửa `Project_V13_Media_Downloader/v13_fb_media_downloader.py`:

- thêm `write_summary(summary)`;
- khi không có tab Facebook/CDP, ghi lỗi vào summary và in path summary.

---

## 6. Điều kiện để chạy lại và đạt PASS

Agent/user cần mở Chrome với remote debug port `9222` và tab Facebook đang đăng nhập:

```powershell
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
& $chrome --remote-debugging-port=9222 --user-data-dir="$env:TEMP\ces-chrome-cdp-9222"
```

Sau đó mở Facebook group/page cần capture trong Chrome đó và chạy lại:

```powershell
$env:CES_V13_MAX_POSTS='3'
$env:CES_V13_MAX_MEDIA_PER_POST='5'
$py = 'C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe'
& $py .\Project_V13_Media_Downloader\v13_fb_media_downloader.py
```

PASS chỉ hợp lệ nếu summary có post/media hoặc lý do hợp lệ từ Facebook session thật.
