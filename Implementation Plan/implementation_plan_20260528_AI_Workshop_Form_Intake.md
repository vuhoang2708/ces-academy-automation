# Implementation Plan: AI Workshop Intake Form

**Ngày:** 2026-05-28  
**Trạng thái:** Đã implement bản đầu, cần redeploy Apps Script và browser UAT sau chỉnh field  
**Phạm vi:** `AI_Workshop_Form/`, Google Sheet, Apps Script Web App, email notification  
**Repo nguồn:** `ces-academy-automation`  
**Project nhận bản copy:** `C:\Users\vu.hoang\.gemini\antigravity\scratch\training_AI`

---

## 1. Executive Summary

Người dùng cần một form thu thập thông tin trước buổi AI Workshop. Form phải lấy thông tin cơ bản, cách người tham gia đang dùng AI, điểm hài lòng/khó chịu, kỳ vọng, bài toán thật muốn mang tới workshop, sau đó ghi vào Google Sheet và gửi email cho người điền form cùng người hướng dẫn `vuhoang2708@gmail.com`.

Bản đầu đã có frontend HTML, Apps Script backend, Google Sheet target, email flow và Gemini browser UAT script. Sau feedback mới nhất, form đã bỏ các trường không cần thiết và đổi section wording từ ngôn ngữ nội bộ sang ngôn ngữ người dùng.

---

## 2. Terminology Notes

- **Frontend**: phần giao diện người dùng, ở đây là `AI_Workshop_Form/index.html`.
- **Backend**: phần xử lý phía sau, ở đây là Google Apps Script Web App.
- **Apps Script Web App**: ứng dụng Google Apps Script được deploy thành URL `/exec` để form gửi dữ liệu tới.
- **Schema**: cấu trúc cột dữ liệu của Google Sheet.
- **UAT**: kiểm thử chấp nhận người dùng, tức test như người dùng thật.
- **Redeploy**: deploy lại Apps Script sau khi sửa code để endpoint chạy bản mới.
- **Smoke test**: test nhanh để kiểm tra đường chính có hoạt động hay không.

---

## 3. User-Visible Symptoms

Các vấn đề người dùng đã chỉ ra:

1. Trường `Khu vực` không rõ ý nghĩa và không quan trọng.
2. Trường `Đơn vị / công ty` không cần thiết.
3. Tiêu đề `Câu hỏi giống luồng trao đổi với Hằng` đưa ngữ cảnh nội bộ vào form, gây cảm giác thiếu chuyên nghiệp.

Kỳ vọng mới:

- Form phải sạch, dùng ngôn ngữ người điền hiểu ngay.
- Ngữ cảnh từ chat chỉ dùng để thiết kế câu hỏi, không đưa nguyên văn vào UI.
- Tài liệu plan/spec phải được copy sang project `training_AI`.

---

## 4. Current Technical State

Đã có:

- `AI_Workshop_Form/index.html`: form HTML tĩnh, gửi payload bằng `application/x-www-form-urlencoded`.
- `AI_Workshop_Form/apps_script_ai_workshop.gs`: Apps Script ghi Sheet và gửi email.
- `AI_Workshop_Form/README.md`: hướng dẫn deploy.
- `Gemini_Test/GEMINI_BROWSER_UAT_20260528_AI_WORKSHOP_FORM.md`: kịch bản browser UAT.
- `Implementation Plan/uat_ai_workshop_form_endpoint_20260528.md`: ghi nhận backend smoke test.

Đã kiểm tra:

- Endpoint mới trả `GET ok: true`.
- POST trực tiếp trả `ok: true` với submission ID `aiw_codex_live_test_20260528_135246`.
- Sau cleanup field, local syntax check đã PASS cho Apps Script và JS trong HTML.

Chưa kiểm tra xong:

- Browser submit từ `index.html` sau cleanup field.
- Inbox người điền form nhận email sau redeploy bản mới.
- `vuhoang2708@gmail.com` nhận email notification sau redeploy bản mới.
- Google Sheet header đã được normalize theo schema mới sau redeploy.

---

## 5. Evidence Collected

Code evidence:

```text
AI_Workshop_Form/index.html
- Form required fields hiện còn: fullName, email, roleTeam, sessionPreference, expectation, concreteTask, consentEmail.
- Section chính đã đổi thành "Nhu cầu và kỳ vọng".
- APPS_SCRIPT_URL đã trỏ tới endpoint mới.

AI_Workshop_Form/apps_script_ai_workshop.gs
- SHEET_ID: 1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64
- RESPONSES_TAB: AIWorkshopResponses
- doGet trả service health JSON.
- doPost parse payload và gọi handleWorkshopIntake_.
- ensureHeaders_ normalize header row khi schema thay đổi.
- MailApp.sendEmail gửi email.
```

Runtime evidence:

```text
GET /exec:
{
  "ok": true,
  "service": "AI Agent Workshop intake endpoint",
  "sheetId": "1R1zkTEK_uCrK9UngQgkHZXqpDoGq0Xas3oN6XZmbi64",
  "responsesTab": "AIWorkshopResponses"
}

POST /exec:
{
  "ok": true,
  "kind": "ai_workshop_intake",
  "submissionId": "aiw_codex_live_test_20260528_135246",
  "message": "Thông tin đã được ghi vào Google Sheet và email xác nhận đã được gửi."
}
```

Git evidence:

```text
Branch nguồn: codex/ces-ai-stabilization
Gần nhất đã push: d21ae9d simplify AI workshop intake form fields
```

---

## 6. Root Causes

Immediate cause:

- Bản form đầu dùng trực tiếp ngữ cảnh cuộc trao đổi để đặt nhãn section, dẫn tới UI lộ thông tin nội bộ và thiếu tự nhiên.

Broader cause:

- Chưa tách rõ ba lớp: thông tin ngữ cảnh dùng cho người thiết kế, câu hỏi hiển thị cho người điền, và schema lưu trữ kỹ thuật.

---

## 7. Generalized Pattern Or Design Flaw

Khi chuyển từ chat nội bộ sang form public/semi-public, không được bê nguyên phrasing của cuộc trao đổi vào UI.

Pattern bền hơn:

1. Dùng chat nội bộ để rút insight.
2. Chuyển insight thành câu hỏi trung tính.
3. Chỉ lưu các field thật sự có tác dụng vận hành.
4. Tách UI label, backend schema và UAT script để khi sửa field không bị lệch.

---

## 8. Proposed Changes

Đã làm:

- Bỏ `Khu vực`.
- Bỏ `Đơn vị / công ty`.
- Đổi tiêu đề section thành `Nhu cầu và kỳ vọng`.
- Bỏ hai field phụ khỏi frontend payload.
- Bỏ hai field phụ khỏi Apps Script schema và email instructor.
- Bỏ hai field phụ khỏi Gemini UAT script.
- Thêm `ensureHeaders_()` để normalize Google Sheet header sau redeploy.

Cần làm tiếp:

- Paste lại `AI_Workshop_Form/apps_script_ai_workshop.gs` vào Google Apps Script.
- Redeploy Web App.
- Chạy browser UAT theo `Gemini_Test/GEMINI_BROWSER_UAT_20260528_AI_WORKSHOP_FORM.md`.
- Kiểm tra tab `AIWorkshopResponses` và email thật.

---

## 9. Implementation Options

### Option A: Giữ HTML tĩnh + Apps Script

Ưu điểm:

- Nhẹ, dễ deploy, không cần server riêng.
- Phù hợp Google Sheet/email workflow hiện tại.

Nhược điểm:

- Web App URL nằm trong HTML, cần quản lý spam/rate limit nếu public rộng.
- Mỗi lần đổi backend phải redeploy Apps Script thủ công.

### Option B: Chuyển sang full web app có backend riêng

Ưu điểm:

- Kiểm soát auth/rate limit tốt hơn.
- Dễ versioning endpoint.

Nhược điểm:

- Quá nặng cho nhu cầu form workshop hiện tại.

Khuyến nghị: tiếp tục Option A, thêm guard nhẹ nếu form public rộng.

---

## 10. Risks And Mitigations

| Rủi ro | Ảnh hưởng | Giảm thiểu |
|---|---|---|
| Apps Script chưa redeploy sau sửa code | Endpoint vẫn chạy schema cũ | Redeploy trước browser UAT |
| Header Sheet cũ còn cột đã bỏ | Dòng mới lệch cột | `ensureHeaders_()` normalize header |
| Public endpoint bị spam | Sheet/mail bị nhiễu | Honeypot field, có thể thêm token/rate-limit nếu cần |
| Browser UAT chưa chạy sau cleanup | Không chắc UI submit thật | Chạy Gemini/browser UAT |
| Email bị vào spam | Người học không thấy xác nhận | Kiểm tra inbox/spam bằng email test |

---

## 11. Expected Outputs

Trong repo CES:

- `Implementation Plan/implementation_plan_20260528_AI_Workshop_Form_Intake.md`
- `Implementation Plan/technical_spec_20260528_AI_Workshop_Form_Intake.md`

Trong project `training_AI`:

- `Implementation Plan/implementation_plan_20260528_AI_Workshop_Form_Intake.md`
- `Implementation Plan/technical_spec_20260528_AI_Workshop_Form_Intake.md`

---

## 12. Execution Plan After Approval

1. Copy hai tài liệu plan/spec sang `training_AI/Implementation Plan/`.
2. Redeploy Apps Script bằng code mới từ `AI_Workshop_Form/apps_script_ai_workshop.gs`.
3. Chạy `GET /exec` để xác nhận endpoint dùng bản mới.
4. Mở `AI_Workshop_Form/index.html` bằng browser.
5. Test validation thiếu field.
6. Submit test data thật.
7. Kiểm tra Sheet row, email người điền, email instructor.
8. Cập nhật UAT result từ `PENDING` sang `PASS/PARTIAL/FAIL`.

---

## 13. Validation Criteria

PASS khi:

- UI không còn các field/label đã bị loại.
- Apps Script schema không còn hai field phụ đã bỏ.
- Google Sheet header khớp schema mới.
- Browser submit trả success.
- Sheet có dòng mới đúng cột.
- Email người điền và instructor được gửi.
- Gemini UAT script không còn hướng dẫn nhập các field đã bỏ.

PARTIAL khi:

- Backend POST trực tiếp PASS nhưng browser UAT chưa chạy.
- Browser submit PASS nhưng chưa xác minh email.

FAIL khi:

- Form vẫn hiển thị field/label cũ.
- Sheet append bị lệch cột.
- Apps Script trả `ok: true` nhưng Sheet/email không có bằng chứng.

---

## 14. Open Questions

1. Form sẽ dùng nội bộ qua link hay public rộng?
2. Có cần thêm câu hỏi phân loại trình độ AI hiện tại không?
3. Có cần thêm field chọn workshop cụ thể nếu sau này có nhiều buổi?
4. Có cần token chống spam nếu link được chia sẻ ngoài nhóm nhỏ?

---

## 15. Notes For Other Agents

- Không đưa ngữ cảnh chat nội bộ vào UI label.
- Không thêm lại `Khu vực` hoặc `Đơn vị / công ty` nếu chưa có yêu cầu rõ.
- Không claim PASS toàn bộ nếu chỉ mới POST trực tiếp.
- Nếu sửa schema, phải kiểm tra header Sheet và UAT script cùng lúc.
- Raw Google Sheet data có thể chứa thông tin cá nhân, không export public nếu chưa có approval.

---

## 16. Final Assessment

Form đang ở trạng thái implementation tốt hơn sau cleanup, nhưng cần redeploy Apps Script và chạy browser UAT để xác nhận end-to-end. Đây là một workflow nhỏ, nên giữ kiến trúc HTML tĩnh + Apps Script + Google Sheet là đủ, miễn là schema và UAT được giữ đồng bộ.
