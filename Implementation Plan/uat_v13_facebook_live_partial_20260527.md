# UAT Result: V13 Facebook Downloader — Live Attempt 2

**Ngày chạy:** 2026-05-27
**Người chạy:** Agent (lần 2)
**Kết quả:** PARTIAL — blocker: không có Chrome debug port 9222 / không có Facebook session
**Module:** `Project_V13_Media_Downloader/v13_fb_media_downloader.py`

---

## 1. Điều kiện đã kiểm tra

| Điều kiện | Trạng thái |
|---|---|
| Chrome debug port 9222 | CLOSED — connection refused |
| Chrome debug port 9333 | OPEN — Antigravity IDE (không phải browser) |
| Chrome debug port 9444 | OPEN — CES login page (không phải Facebook) |
| Facebook session | Không có |
| User xác nhận | Không có session Facebook — bỏ qua V13 |

---

## 2. Lệnh đã chạy

```powershell
# Compile check
python -m py_compile .\capture_antigravity.py .\Project_V13_Media_Downloader\v13_fb_media_downloader.py .\config.py
→ exit 0

# Port scan
Invoke-WebRequest http://localhost:9222/json → REFUSED
Invoke-WebRequest http://localhost:9333/json → Antigravity IDE tabs
Invoke-WebRequest http://localhost:9444/json → CES login tab

# Run V13 (no CDP)
$env:CES_V13_MAX_POSTS="3"; $env:CES_V13_MAX_MEDIA_PER_POST="5"; $env:CES_FORCE_DOWNLOAD="0"
python .\Project_V13_Media_Downloader\v13_fb_media_downloader.py
```

---

## 3. Output thực tế

```
❌ Không kết nối được Chrome debug tại http://localhost:9222/json
⚠️ Không có tab Facebook đang mở trong Chrome debug.
📊 Summary: downloads/v13_facebook/latest_run_summary.json
```

Summary JSON:
```json
{
  "posts_found": 0,
  "posts_saved": 0,
  "media_attempted": 0,
  "media_downloaded": 0,
  "media_failed": 0,
  "media_skipped": 0,
  "errors": [{"reason": "no_facebook_tab_or_cdp_unavailable:http://localhost:9222/json"}]
}
```

---

## 4. Đánh giá

**PARTIAL** — script hoạt động đúng (fail có summary, không crash im lặng), nhưng chưa có live Facebook session.

Đã xác minh:
- Compile PASS
- Script phát hiện thiếu CDP và ghi summary rõ ràng
- Output trong `downloads/` được `.gitignore` bảo vệ
- Không có raw Facebook data nào được tạo

Chưa xác minh:
- Đọc Facebook DOM thật
- Tải post/media thật
- MIME check trong live download
- Summary counter với data thật

---

## 5. Điều kiện để đạt PASS

User cần:
1. Mở Chrome với debug port 9222:
   ```powershell
   $chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
   & $chrome --remote-debugging-port=9222 --user-data-dir="$env:TEMP\ces-chrome-cdp-9222"
   ```
2. Đăng nhập Facebook trong Chrome đó.
3. Mở Facebook group/page cần capture.
4. Chạy lại:
   ```powershell
   $env:CES_V13_MAX_POSTS="3"; $env:CES_V13_MAX_MEDIA_PER_POST="5"
   python .\Project_V13_Media_Downloader\v13_fb_media_downloader.py
   ```

PASS khi summary có `posts_found > 0` hoặc `media_downloaded > 0`.

---

## 6. Raw output

- `downloads/v13_facebook/latest_run_summary.json` — local-only, gitignored, không commit
