# UAT Result: V10 CES Web Capture

**Ngày chạy:** 2026-05-27
**Người chạy:** Codex
**Kết quả:** PARTIAL
**Module:** `capture_antigravity.py`

---

## 1. Mục tiêu

Chạy Handoff 02 để kiểm tra V10 sau khi chuyển output về repo-relative `outputs/` và chuẩn bị cho AI sidecar contract.

---

## 2. Môi trường test

Để tránh điều hướng nhầm Antigravity/IDE đang mở ở port `9333`, test dùng Chrome debug riêng:

```text
http://localhost:9444
```

Chrome được mở headless bằng profile tạm:

```powershell
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$profile = Join-Path $env:TEMP 'ces-v10-cdp-9444'
Start-Process -FilePath $chrome -ArgumentList @(
  '--headless=new',
  '--remote-debugging-port=9444',
  "--user-data-dir=$profile",
  '--disable-gpu',
  '--no-first-run',
  '--window-size=1280,900',
  'about:blank'
) -WindowStyle Hidden
```

---

## 3. Lệnh đã chạy

```powershell
$py = 'C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe'
& $py -m py_compile .\capture_antigravity.py
```

```powershell
$env:CES_VIEWER_CDP_PORT='9444'
$env:CES_V10_TOTAL_PAGES='2'
$py = 'C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe'
& $py .\capture_antigravity.py
```

---

## 4. Kết quả thực tế

Script kết nối Chrome được nhưng CES redirect về trang login:

```text
URL hiện tại: https://academy.cesglobal.com.vn/login.html
Tiêu đề: Đăng nhập — CES ACADEMY
```

Summary được tạo tại:

```text
outputs/v10_ces_web_capture/latest_run_summary.json
```

Nội dung summary chính:

```json
{
  "status": "blocked_login",
  "requested_pages": 2,
  "current_url": "https://academy.cesglobal.com.vn/login.html",
  "title": "Đăng nhập — CES ACADEMY",
  "pdf": "",
  "errors": [
    "CES viewer redirected to login page; authenticated session required."
  ]
}
```

Screenshot chẩn đoán:

```text
outputs/v10_ces_web_capture/screenshots_high_res/page_001.png
```

PDF stale từ lần chạy đầu đã được xóa để tránh hiểu nhầm là capture giáo trình thành công.

---

## 5. Đánh giá

PARTIAL, không phải PASS live UAT.

Đã xác minh:

- Script compile được.
- Script dùng output trong `outputs/v10_ces_web_capture/`.
- Script phát hiện login redirect và không đóng gói PDF như thể thành công.
- Output trong `outputs/` được `.gitignore` bảo vệ.

Chưa xác minh:

- Chưa capture được nội dung giáo trình sau login.
- Chưa tạo PDF học liệu hợp lệ.
- Chưa tạo AI sidecar nội dung V10 vì chưa có artifact giáo trình thật.

---

## 6. Fix đã thực hiện

Sửa `capture_antigravity.py`:

- thêm `sys.path` để portable Python import được `config.py`;
- cấu hình UTF-8 cho stdout/stderr để tránh lỗi `UnicodeEncodeError` trên Windows;
- thêm `latest_run_summary.json`;
- phát hiện login redirect và dừng sớm;
- sửa log số trang từ hardcoded `81` sang `TOTAL_PAGES`.

---

## 7. Điều kiện để chạy lại và đạt PASS

Agent/user cần dùng Chrome debug port có session CES đã đăng nhập.

Ví dụ nếu dùng port riêng:

```powershell
$env:CES_VIEWER_CDP_PORT='<port có Chrome đã login CES>'
$env:CES_V10_TOTAL_PAGES='5'
$py = 'C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe'
& $py .\capture_antigravity.py
```

PASS chỉ hợp lệ nếu:

- `latest_run_summary.json` không còn `blocked_login`;
- screenshot là nội dung viewer/giáo trình thật;
- PDF được tạo từ nội dung học liệu;
- AI sidecar V10 có thể phân tích bài học thật hoặc ghi rõ phạm vi sample.
