# HƯỚNG DẪN TEST V13 - FACEBOOK DOWNLOADER

Để chạy thử nghiệm thành công tính năng cào Media từ Facebook, anh vui lòng thực hiện đúng theo 3 bước sau:

### 🛠 Bước 1: Khởi động Chrome/Edge ở chế độ Debug
Anh cần đóng hoàn toàn trình duyệt đang mở và chạy lệnh sau từ cửa sổ **CMD** (hoặc Win + R):

**Dành cho Chrome:**
```cmd
chrome.exe --remote-debugging-port=9222
```

**Dành cho Edge:**
```cmd
msedge.exe --remote-debugging-port=9222
```

### 🌐 Bước 2: Mở trang mục tiêu
Trong cửa sổ trình duyệt vừa hiện ra, anh đăng nhập Facebook và truy cập vào Group cần cào:
👉 [Link Group Test](https://www.facebook.com/share/g/1DAUzU9uVw/)

*Lưu ý: Anh hãy cuộn chuột xuống vài lần để Facebook hiển thị (render) thêm các hình ảnh cũ.*

### 🚀 Bước 3: Thực thi Script V13
Mở Terminal/PowerShell tại thư mục dự án và chạy:

```powershell
python Project_V13_Media_Downloader/v13_fb_media_downloader.py
```

---
### 📊 Kết quả kiểm chứng
1.  **Console:** Sẽ xuất hiện dòng `✅ Phát hiện X đối tượng Media.`.
2.  **Folder:** Toàn bộ ảnh/file sẽ được tải về thư mục `Project_V13_Media_Downloader/v13_fb_downloads/`.

*📍 Hướng dẫn được tạo ngày 19/04/2026 bởi Antigravity Agent.*
