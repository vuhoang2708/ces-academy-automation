# Gemini Browser UAT: AI Workshop Intake Form

**Ngày tạo:** 2026-05-28  
**Mục tiêu:** Dùng Gemini/agent có browser để test form thu thập nhu cầu AI Workshop, Google Sheet write và email notification.  
**Phạm vi:** `AI_Workshop_Form/index.html` + `AI_Workshop_Form/apps_script_ai_workshop.gs`

---

## 1. Điều Kiện Trước Khi Test

Agent phải xác nhận đủ các điều kiện sau:

1. Google Sheet đích mở được:

   ```text
   https://docs.google.com/spreadsheets/d/1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64/edit?gid=0#gid=0
   ```

2. Apps Script đã được paste từ:

   ```text
   AI_Workshop_Form/apps_script_ai_workshop.gs
   ```

3. `CONFIG.SHEET_ID` trong Apps Script là raw ID, không phải full URL:

   ```text
   1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64
   ```

4. Apps Script đã deploy dạng Web App:
   - Execute as: `Me`
   - Who has access: `Anyone with the link`

5. Web App URL mới đã được dán vào:

   ```javascript
   const APPS_SCRIPT_URL = '.../exec';
   ```

   trong file:

   ```text
   AI_Workshop_Form/index.html
   ```

Nếu chưa có Web App URL thì chỉ được test giao diện và validation local, không được kết luận Sheet/email PASS.

---

## 2. Prompt Cho Gemini Browser Agent

Paste đoạn này cho Gemini/agent:

```text
Bạn đang test form AI Workshop trong repo:

C:\Users\vu.hoang\.gemini\antigravity\scratch\ces-academy-automation

Mục tiêu: xác minh form `AI_Workshop_Form/index.html` có thể submit thành công vào Google Sheet và gửi email xác nhận.

Không sửa logic nếu chưa có bằng chứng lỗi. Hãy test theo thứ tự:

1. Kiểm tra `AI_Workshop_Form/index.html` đã có Apps Script Web App URL thật chưa. Nếu vẫn là `PASTE_APPS_SCRIPT_WEB_APP_URL_HERE`, dừng live test và báo BLOCKED_CONFIG.
2. Mở form trong browser.
3. Test validation: bấm submit khi còn thiếu trường bắt buộc, form phải chặn.
4. Điền test data dưới đây.
5. Submit.
6. Kiểm tra thông báo trên form.
7. Mở Google Sheet và kiểm tra tab `AIWorkshopResponses` có dòng mới.
8. Kiểm tra email người điền form có mail xác nhận.
9. Kiểm tra `vuhoang2708@gmail.com` nhận email notification.
10. Kết luận PASS/PARTIAL/FAIL, nêu bằng chứng cụ thể.

Không upload dữ liệu riêng tư ngoài test data giả.
Không commit Web App URL nếu user không yêu cầu.
```

---

## 3. Test Data

```text
Họ tên: Codex Gemini UAT AI Workshop
Email: dùng email test thật mà agent/user có thể kiểm tra inbox
SĐT/Zalo: 0900000000
Vai trò/team: UAT / AI adoption test
Đơn vị/công ty: CES test
Khu vực: Online
Lịch mong muốn: Thứ Hai 01/06
Hình thức tham gia: Online
Công cụ đang dùng: Gemini / Gemini Pro, ChatGPT, Claude
Công cụ khác: Perplexity
Use case: Viết kịch bản TikTok/video, Làm poster/nội dung thiết kế, Tự động hóa công việc
Use case khác: Phân tích chat Zalo thành action items
Điều hài lòng: AI giúp tạo dàn ý và bản nháp nhanh hơn.
Điều gây khó chịu: Phải mô tả rất chi tiết, đôi khi sai thông tin và cần kiểm chứng.
Kỳ vọng: Biết cách dùng AI agent để biến một đoạn chat thành kế hoạch hành động.
Bài toán thật: Lấy một cuộc trao đổi Zalo, bóc tách nguyên văn, tóm tắt, phân tích tone, CTA và việc cần làm.
Budget: 200.000đ - 500.000đ
Output mong muốn: Demo live trên bài toán thật
Consent email: checked
```

---

## 4. Expected Sheet Row

Tab phải là:

```text
AIWorkshopResponses
```

Headers tối thiểu phải có:

```text
timestamp
submissionId
source
fullName
email
phoneZalo
roleTeam
organization
location
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

Dòng mới phải có:

- `fullName = Codex Gemini UAT AI Workshop`
- `status = new`
- `submissionId` bắt đầu bằng `aiw_`
- `aiTools` chứa `Gemini / Gemini Pro`, `ChatGPT`, `Claude`
- `rawPayloadJson` là JSON parse được

---

## 5. Expected Emails

### Email người điền form

Subject chứa:

```text
Xác nhận đã nhận thông tin đăng ký AI Agent Workshop
```

Body phải có:

- tên người điền;
- lịch mong muốn;
- công cụ AI đang dùng;
- bài toán thật;
- mã phản hồi.

### Email người hướng dẫn

Recipient:

```text
vuhoang2708@gmail.com
```

Subject chứa:

```text
[AI Workshop] Form mới
```

Body phải có:

- họ tên;
- email;
- vai trò/team;
- lịch mong muốn;
- công cụ/use case;
- kỳ vọng;
- bài toán thật;
- CTA cho người hướng dẫn.

---

## 6. PASS / PARTIAL / FAIL

PASS khi:

- Form validation hoạt động.
- Submit trả thành công.
- Google Sheet có dòng mới đúng tab/headers.
- Người điền form nhận email.
- `vuhoang2708@gmail.com` nhận email notification.

PARTIAL khi:

- Giao diện và validation OK nhưng chưa có Web App URL.
- Sheet ghi được nhưng email chưa xác minh được.
- Email gửi được nhưng chưa kiểm được Sheet vì thiếu quyền xem.

FAIL khi:

- Form submit báo thành công giả nhưng Sheet không có dòng mới.
- Apps Script dùng full Sheet URL trong `SHEET_ID`.
- Lỗi `Document ... is missing`.
- Browser báo CORS/preflight do gửi `application/json` thay vì `application/x-www-form-urlencoded`.
- Không có email nào được gửi dù Apps Script trả `ok: true`.

---

## 7. Báo Cáo Kết Quả Cần Trả Về

```text
AI Workshop Form UAT: PASS/PARTIAL/FAIL
Web App URL configured: YES/NO
Validation test: PASS/PARTIAL/FAIL
Submit response: <message>
Sheet row: PASS/PARTIAL/FAIL
Learner email: PASS/PARTIAL/FAIL
Instructor email: PASS/PARTIAL/FAIL
Screenshots captured: <paths or browser screenshot names>
Notes/blockers:
- ...
```
