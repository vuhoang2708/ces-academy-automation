# UAT Result: AI Workshop Form Endpoint

**Ngày chạy:** 2026-05-28  
**Kết quả:** PASS cho backend endpoint qua GET và POST trực tiếp
**Module:** `AI_Workshop_Form/`

---

## 1. Endpoint Đang Dùng

```text
https://script.google.com/macros/s/AKfycbwen9Ev8uCqfniWswTBn0krubpfVlPsA0ILvcSI_7j4Rj5JitCzaDJWVeI66r7dwFV1/exec
```

File đã gắn URL:

```text
AI_Workshop_Form/index.html
```

Endpoint cũ bị loại khỏi form:

```text
https://script.google.com/macros/s/AKfycbyzbTxCSENSDhi77tDueLHv6Kc0TnUmf7Exxa41hT5IH0xAbO0zBHM_sSCJDlIukRWS/exec
```

Endpoint cũ từng trả `403 Forbidden`.

---

## 2. Kết Quả Kiểm Tra GET

Lệnh kiểm tra:

```powershell
Invoke-RestMethod -Uri "https://script.google.com/macros/s/AKfycbwen9Ev8uCqfniWswTBn0krubpfVlPsA0ILvcSI_7j4Rj5JitCzaDJWVeI66r7dwFV1/exec" -Method Get
```

Kết quả:

```json
{
  "ok": true,
  "service": "AI Agent Workshop intake endpoint",
  "sheetId": "1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64",
  "responsesTab": "AIWorkshopResponses"
}
```

Đánh giá: PASS. Web App hiện chạy được public endpoint theo cấu hình cần thiết.

---

## 3. Kết Quả Kiểm Tra POST Trực Tiếp

Test data đã gửi bằng `application/x-www-form-urlencoded` với field `payload` chứa JSON.

Submission ID:

```text
aiw_codex_live_test_20260528_135246
```

Email test:

```text
vuhoang2708+aiworkshoptest@gmail.com
```

Kết quả Apps Script trả về:

```json
{
  "ok": true,
  "kind": "ai_workshop_intake",
  "submissionId": "aiw_codex_live_test_20260528_135246",
  "message": "Thông tin đã được ghi vào Google Sheet và email xác nhận đã được gửi."
}
```

Đánh giá: PASS cho đường backend trực tiếp. Apps Script xác nhận đã ghi Google Sheet và gửi email.

---

## 4. Trạng Thái Còn Cần Browser UAT

Sau feedback ngày 2026-05-28, form đã bỏ hai trường thông tin phụ không cần thiết và đổi tiêu đề section nội bộ thành ngôn ngữ người dùng bình thường.

Repo backend cũng đã bỏ hai field đó khỏi schema. Cần redeploy Apps Script từ `AI_Workshop_Form/apps_script_ai_workshop.gs` để Google Sheet/email dùng schema mới. Code mới có `ensureHeaders_()` để normalize header row của tab `AIWorkshopResponses`, tránh append dữ liệu mới bị lệch cột nếu tab đang còn header cũ.

Chưa chạy browser UAT đầy đủ trên form HTML sau khi thay endpoint mới và sau cleanup field. Cần dùng:

```text
Gemini_Test/GEMINI_BROWSER_UAT_20260528_AI_WORKSHOP_FORM.md
```

Browser UAT cần xác nhận thêm:

- form validation chặn thiếu trường bắt buộc;
- browser submit thành công từ `AI_Workshop_Form/index.html`;
- tab `AIWorkshopResponses` có dòng mới;
- inbox nhận email xác nhận;
- `vuhoang2708@gmail.com` nhận email notification.

---

## 5. Kết Luận

Backend Apps Script đã qua smoke test thật bằng GET và POST.

Trạng thái tổng thể:

```text
Backend endpoint: PASS
Frontend wired to endpoint: PASS
Full browser UAT: PENDING
```
