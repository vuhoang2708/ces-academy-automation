# AI Workshop Intake Form

Form này thu thập thông tin người tham gia trước buổi chia sẻ AI agent/Antigravity, ghi dữ liệu vào Google Sheet và gửi email cho:

- người điền form;
- người hướng dẫn: `vuhoang2708@gmail.com`.

Google Sheet đích:

```text
https://docs.google.com/spreadsheets/d/1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64/edit?gid=0#gid=0
```

Raw Sheet ID đang dùng trong Apps Script:

```text
1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64
```

## File Chính

| File | Vai trò |
|---|---|
| `index.html` | Form tĩnh để mở trên browser hoặc host ở bất kỳ static hosting nào |
| `apps_script_ai_workshop.gs` | Backend Google Apps Script ghi Sheet và gửi email |

## Cách Triển Khai Apps Script

1. Mở Google Sheet đích.
2. Chọn `Extensions` > `Apps Script`.
3. Xóa code mẫu và paste toàn bộ nội dung từ `apps_script_ai_workshop.gs`.
4. Kiểm tra `CONFIG.SHEET_ID` chỉ là raw ID:

   ```javascript
   SHEET_ID: '1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64'
   ```

   Không paste full URL `/edit?gid=...` vào `SHEET_ID`.

5. Bấm `Deploy` > `New deployment`.
6. Chọn type `Web app`.
7. Cấu hình:
   - `Execute as`: `Me`
   - `Who has access`: `Anyone with the link`
8. Authorize quyền truy cập Sheet và gửi email.
9. Copy Web App URL dạng:

   ```text
   https://script.google.com/macros/s/.../exec
   ```

10. Mở `index.html`, tìm:

    ```javascript
    const APPS_SCRIPT_URL = 'PASTE_APPS_SCRIPT_WEB_APP_URL_HERE';
    ```

    Thay bằng Web App URL mới.

## Cách Test Nhanh

1. Mở `AI_Workshop_Form/index.html` trong Chrome.
2. Điền dữ liệu test, ví dụ:
   - Họ tên: `Codex Test AI Workshop`
   - Email: email thật để kiểm tra nhận thư
   - Vai trò/team: `Test team`
   - Lịch mong muốn: `Thứ Hai 01/06`
   - Kỳ vọng: `Biết cách dùng AI agent cho việc thật`
   - Bài toán thật: `Tạo prompt phân tích chat Zalo và ra action items`
3. Submit form.
4. Kết quả PASS khi:
   - form báo thành công;
   - Sheet có tab `AIWorkshopResponses`;
   - dòng mới có đủ thông tin;
   - người điền form nhận email;
   - `vuhoang2708@gmail.com` nhận email thông báo.

## Lưu Ý Bảo Mật

- Form không chứa dữ liệu nhạy cảm mặc định, nhưng nội dung bài toán thật có thể là thông tin nội bộ.
- Không commit Web App URL nếu muốn giữ endpoint private hơn.
- Không dùng Google Sheet URL đầy đủ trong Apps Script; chỉ dùng raw Sheet ID.
