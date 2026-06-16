# Hướng Dẫn UAT V13 - Facebook Media Downloader

Tài liệu này dùng để kiểm thử V13 Facebook sau khi hardening. Không dùng cho V13 Zalo vì V13 Zalo hiện đã được quarantine.

---

## 🛠️ Bước 1: Chuẩn bị môi trường Chrome (Quan trọng nhất)

Để Script có thể "điều khiển" được trình duyệt, anh **bắt buộc** phải mở Chrome ở chế độ Debug chuyên dụng.

### 1.1 Tắt sạch Chrome cũ
- Nhấn chuột phải vào Taskbar -> **Task Manager**.
- Tìm các dòng **Google Chrome**, chuột phải chọn **End Task**.
- *Hoặc chạy lệnh này trong PowerShell:* `taskkill /F /IM chrome.exe /T`

### 1.2 Mở Chrome bằng debug port 9222
Anh dán lệnh sau vào PowerShell để mở một cửa sổ Chrome debug:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\vu.hoang\.gemini\antigravity\scratch\chrome_debug_profile"
```

### 1.3 Kiểm tra kết nối
- Truy cập địa chỉ: `http://localhost:9222/json`
- Nếu thấy hiện ra danh sách các thẻ JSON (như hình loằng ngoằng) -> **Đã sẵn sàng.**

---

## 🚀 Bước 2: Thực thi cào dữ liệu

1. **Vào Group Facebook:** Trong cửa sổ Chrome vừa mở, anh đăng nhập Facebook và truy cập vào Group [CON CHÁU TỘC HOÀNG](https://www.facebook.com/share/g/1DAUzU9uVw/).
2. **Chạy lệnh cào:** Quay lại Terminal/PowerShell và chạy:

```powershell
C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe Project_V13_Media_Downloader/v13_fb_media_downloader.py
```

---

## 📂 Bước 3: Kiểm tra kết quả

Sau khi Script chạy xong, toàn bộ dữ liệu sẽ nằm tại:
`downloads\v13_facebook\`

Mỗi bài viết sẽ là một thư mục riêng gồm:
- `content.txt`: Nội dung văn bản của bài viết.
- `img_1.jpg`, `img_2.jpg`...: Các hình ảnh/media tải được.
- `latest_run_summary.json`: Summary số post/media thành công, skipped, lỗi.

---

## ⚙️ Tùy chỉnh (Dành cho Anh Vũ)

Nếu anh muốn giới hạn số bài/media:

```powershell
$env:CES_V13_MAX_POSTS="20"
$env:CES_V13_MAX_MEDIA_PER_POST="5"
```

Nếu muốn tải lại file đã có:

```powershell
$env:CES_FORCE_DOWNLOAD="1"
```

---
*Cập nhật: 27/05/2026*
