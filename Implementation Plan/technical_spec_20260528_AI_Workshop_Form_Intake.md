# Technical Spec: AI Workshop Intake Form

**Ngày:** 2026-05-28  
**Module:** `AI_Workshop_Form/`  
**Backend:** Google Apps Script Web App  
**Storage:** Google Sheet `1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64`  
**Email nhận thông báo:** `vuhoang2708@gmail.com`

---

## 1. Mục Tiêu Kỹ Thuật

Tạo một form tĩnh để thu nhu cầu người tham gia AI Workshop, gửi dữ liệu tới Google Apps Script, ghi vào Google Sheet, và gửi email xác nhận.

Yêu cầu chính:

- không cần backend server riêng;
- không dùng full Google Sheet URL trong Apps Script;
- frontend gửi `application/x-www-form-urlencoded` để tránh CORS preflight;
- email người điền và email người hướng dẫn đều phải được gửi;
- schema Sheet không lệch khi bỏ/sửa field.

---

## 2. File Và Vai Trò

| File | Vai trò |
|---|---|
| `AI_Workshop_Form/index.html` | Form HTML tĩnh, style và JS submit |
| `AI_Workshop_Form/apps_script_ai_workshop.gs` | Apps Script Web App: parse payload, ghi Sheet, gửi email |
| `AI_Workshop_Form/README.md` | Hướng dẫn deploy Apps Script |
| `Gemini_Test/GEMINI_BROWSER_UAT_20260528_AI_WORKSHOP_FORM.md` | Browser UAT script |
| `Implementation Plan/uat_ai_workshop_form_endpoint_20260528.md` | Kết quả endpoint smoke test |

---

## 3. Frontend Contract

Endpoint:

```javascript
const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxcnPEZ3DnS33IDNY_Pa0HxVikWVCYOKIc4ipT6EkZ1hfkC11j-osX8qJ4Aq5vdBpZO/exec';
```

Method:

```text
POST
```

Content-Type:

```text
application/x-www-form-urlencoded;charset=UTF-8
```

Body shape:

```text
payload=<JSON string>
```

Required fields:

```text
fullName
email
roleTeam
sessionPreference
expectation
concreteTask
consentEmail
```

Optional fields:

```text
phoneZalo
joinMode
aiTools
aiToolsOther
aiUseCases
aiUseCasesOther
satisfaction
frustrations
budgetRange
preferredOutput
website
```

Honeypot:

```text
website
```

Nếu `website` có giá trị, Apps Script trả `ok: true` nhưng bỏ qua submission.

---

## 4. Payload JSON

Ví dụ payload:

```json
{
  "kind": "ai_workshop_intake",
  "submissionId": "aiw_1770000000000_abc123",
  "source": "AI_Workshop_Form/index.html",
  "fullName": "Nguyen Van A",
  "email": "learner@example.com",
  "phoneZalo": "0900000000",
  "roleTeam": "Marketing",
  "sessionPreference": "Thứ Hai 01/06",
  "joinMode": "Online",
  "aiTools": ["Gemini / Gemini Pro", "ChatGPT"],
  "aiToolsOther": "",
  "aiUseCases": ["Viết kịch bản TikTok/video"],
  "aiUseCasesOther": "",
  "satisfaction": "AI giúp lên dàn ý nhanh.",
  "frustrations": "Phải mô tả quá chi tiết và cần kiểm chứng.",
  "expectation": "Muốn biết cách dùng AI agent cho việc thật.",
  "concreteTask": "Biến chat Zalo thành action items.",
  "budgetRange": "200.000đ - 500.000đ",
  "preferredOutput": "Demo live trên bài toán thật",
  "consentEmail": "yes",
  "website": ""
}
```

---

## 5. Google Sheet Schema

Tab:

```text
AIWorkshopResponses
```

Headers:

```text
timestamp
submissionId
source
fullName
email
phoneZalo
roleTeam
sessionPreference
joinMode
aiTools
aiToolsOther
aiUseCases
aiUseCasesOther
satisfaction
frustrations
expectation
concreteTask
budgetRange
preferredOutput
consentEmail
status
rawPayloadJson
```

Status value hiện tại:

```text
new
```

Header migration:

- `ensureHeaders_()` kiểm tra row 1.
- Nếu header cũ hoặc dư cột đã bỏ, function clear row 1 và set lại headers mới.
- Dữ liệu cũ không bị xóa, nhưng nếu schema cũ đã có row data, cần kiểm tra bằng mắt sau redeploy để chắc các dòng mới không lệch.

---

## 6. Apps Script Flow

### `doGet()`

Trả health JSON:

```json
{
  "ok": true,
  "service": "AI Agent Workshop intake endpoint",
  "sheetId": "1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64",
  "responsesTab": "AIWorkshopResponses"
}
```

### `doPost(e)`

1. Parse payload từ `e.parameter.payload`.
2. Nếu không có `payload`, fallback parse JSON raw body hoặc form fields.
3. Gọi `handleWorkshopIntake_`.
4. Trả JSON `ok: true` hoặc `ok: false`.

### `handleWorkshopIntake_(payload)`

1. Kiểm tra honeypot.
2. Kiểm tra required fields.
3. Validate email.
4. Kiểm tra `consentEmail === "yes"`.
5. Ghi row vào `AIWorkshopResponses`.
6. Gửi email instructor.
7. Gửi email participant.
8. Trả `submissionId`.

---

## 7. Email Behavior

### Instructor Email

Recipient:

```text
vuhoang2708@gmail.com
```

Subject:

```text
[AI Workshop] Form mới - <fullName>
```

Body gồm:

- submission ID;
- thời gian;
- họ tên;
- email;
- SĐT/Zalo;
- vai trò/team;
- hình thức tham gia;
- lịch mong muốn;
- công cụ AI;
- use case;
- điều hài lòng;
- điểm khó chịu;
- kỳ vọng;
- bài toán thật;
- budget;
- output mong muốn;
- CTA cho người hướng dẫn.

### Participant Email

Recipient:

```text
payload.email
```

Subject:

```text
Xác nhận đã nhận thông tin đăng ký AI Agent Workshop
```

Body gồm:

- tên người điền;
- vai trò/team;
- lịch mong muốn;
- hình thức tham gia;
- công cụ AI đang dùng;
- bài toán muốn mang tới workshop;
- mã phản hồi;
- gợi ý chuẩn bị prompt/output thật trước workshop.

---

## 8. Deploy Checklist

1. Mở Google Sheet.
2. `Extensions` > `Apps Script`.
3. Paste code mới từ `AI_Workshop_Form/apps_script_ai_workshop.gs`.
4. Kiểm tra:

   ```javascript
   SHEET_ID: '1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64'
   ```

5. `Deploy` > `Manage deployments` hoặc `New deployment`.
6. Type: `Web app`.
7. `Execute as`: `Me`.
8. `Who has access`: `Anyone with the link`.
9. Authorize Google Sheets và MailApp.
10. Mở `/exec`, kỳ vọng `ok: true`.

---

## 9. Verification Checklist

Local:

```powershell
node -e "const fs=require('fs'); new Function(fs.readFileSync('AI_Workshop_Form/apps_script_ai_workshop.gs','utf8')); console.log('apps_script_syntax_OK')"
node -e "const fs=require('fs'); const html=fs.readFileSync('AI_Workshop_Form/index.html','utf8'); const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/gi)].map(m=>m[1]); for (const [i,s] of scripts.entries()) { new Function(s); console.log('script_'+(i+1)+'_OK'); }"
git diff --check
```

Backend:

```powershell
Invoke-RestMethod -Uri "<WEB_APP_URL>" -Method Get
```

Browser UAT:

```text
Gemini_Test/GEMINI_BROWSER_UAT_20260528_AI_WORKSHOP_FORM.md
```

PASS khi:

- form validation hoạt động;
- browser submit success;
- Sheet row đúng schema;
- email participant nhận được;
- `vuhoang2708@gmail.com` nhận notification;
- không còn field đã bỏ trong UI/UAT/schema.

---

## 10. Security And Privacy Notes

- Web App URL đang hardcode trong frontend. Nếu form public rộng, cần thêm token hoặc rate limit.
- Payload có email/SĐT và bài toán công việc thật, không export public.
- Không commit data Google Sheet hoặc email content thật.
- Nếu cần chia sẻ cho NotebookLM/second brain, chỉ dùng bản đã sanitize.

---

## 11. Known Limitations

- Apps Script deployment thủ công; repo code không tự redeploy Google.
- `ensureHeaders_()` chỉ normalize header, không migrate dữ liệu cũ theo cột mới.
- Browser UAT sau cleanup field vẫn đang pending.
- Mail delivery có thể bị delay hoặc vào spam.

---

## 12. Handoff Summary

Agent tiếp theo cần:

1. Redeploy Apps Script bằng bản mới.
2. Chạy browser UAT.
3. Kiểm tra Google Sheet header và row mới.
4. Kiểm tra cả email người điền và email instructor.
5. Cập nhật `Implementation Plan/uat_ai_workshop_form_endpoint_20260528.md` với kết quả mới.
