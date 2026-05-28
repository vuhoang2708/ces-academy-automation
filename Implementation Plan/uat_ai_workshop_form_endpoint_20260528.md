# UAT Result: AI Workshop Form Endpoint

**Ngày chạy:** 2026-05-28  
**Kết quả:** PARTIAL - form đã được cấu hình endpoint, nhưng Web App URL hiện trả `403 Forbidden`  
**Module:** `AI_Workshop_Form/`

---

## 1. Endpoint Được Cấu Hình

```text
https://script.google.com/macros/s/AKfycbyzbTxCSENSDhi77tDueLHv6Kc0TnUmf7Exxa41hT5IH0xAbO0zBHM_sSCJDlIukRWS/exec
```

File đã gắn URL:

```text
AI_Workshop_Form/index.html
```

---

## 2. Kết Quả Kiểm Tra GET

Lệnh kiểm tra:

```powershell
Invoke-RestMethod -Uri "https://script.google.com/macros/s/AKfycbyzbTxCSENSDhi77tDueLHv6Kc0TnUmf7Exxa41hT5IH0xAbO0zBHM_sSCJDlIukRWS/exec" -Method Get
```

Kết quả:

```text
403 Forbidden
```

Nội dung HTML của Google hiển thị:

```text
Bạn cần có quyền truy cập
Trực tiếp mở tài liệu để xem có thể yêu cầu cấp quyền truy cập hay không hoặc chuyển sang tài khoản có quyền truy cập.
```

---

## 3. Đánh Giá

Form frontend không còn bị thiếu cấu hình endpoint, nhưng chưa thể gọi live backend thành công.

Nguyên nhân có khả năng cao:

1. Web App deploy chưa đặt `Who has access` là `Anyone with the link`.
2. Apps Script chưa authorize xong quyền đọc/ghi Google Sheet và gửi email.
3. URL đang trỏ tới Apps Script project/deployment mà tài khoản hiện tại hoặc public user chưa có quyền chạy.
4. Sau khi đổi quyền, chưa `Deploy` lại bản mới.

---

## 4. Cách Sửa Trên Google Apps Script

Trong Apps Script:

1. Bấm `Deploy` > `Manage deployments`.
2. Chọn deployment hiện tại hoặc tạo `New deployment`.
3. Type: `Web app`.
4. Cấu hình:
   - `Execute as`: `Me`
   - `Who has access`: `Anyone with the link`
5. Authorize đủ quyền:
   - Google Sheets
   - MailApp/Gmail send
6. Copy lại URL `/exec`.
7. Mở URL trong tab ẩn danh hoặc browser không đăng nhập. PASS khi trả JSON:

```json
{
  "ok": true,
  "service": "AI Agent Workshop intake endpoint",
  "sheetId": "1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64",
  "responsesTab": "AIWorkshopResponses"
}
```

---

## 5. Điều Kiện Để Kết Luận PASS

Chỉ kết luận PASS khi:

- `GET /exec` trả JSON `ok: true`;
- form submit test data thành công;
- Sheet có dòng mới trong tab `AIWorkshopResponses`;
- email người điền form được gửi;
- `vuhoang2708@gmail.com` nhận email notification.
