# Gemini Test Script: Review Hai UAT Đầu Tiên V13 Facebook Và V10 CES

**Ngày:** 2026-05-27
**Mục tiêu:** Dùng Gemini để kiểm tra khách quan hai lượt chạy đầu tiên sau hardening: V13 Facebook và V10 CES Web Capture.
**Phạm vi:** Không phân tích raw Facebook/Zalo/private content; chỉ phân tích code, UAT note và summary kỹ thuật đã sanitize.

---

## 1. Nguyên tắc bảo mật

- Không upload raw `downloads/`, `outputs/`, `zalo_captures/`, screenshot chat, PDF học liệu, hoặc media cá nhân.
- Chỉ đưa Gemini các file repo docs/code và summary kỹ thuật đã sanitize.
- Nếu Gemini yêu cầu artifact riêng tư, trả lời: `Không có approval upload dữ liệu riêng tư; chỉ được đánh giá từ summary kỹ thuật.`

---

## 2. Input Cho Gemini

Đưa Gemini các file sau:

```text
PROJECT_STATUS.md
Implementation Plan/Agent Handoff/remaining_plan_index_20260527.md
Implementation Plan/Agent Handoff/remaining_01_v13_facebook_live_uat_20260527.md
Implementation Plan/Agent Handoff/remaining_02_v10_uat_and_ai_contract_20260527.md
Implementation Plan/uat_v13_facebook_partial_20260527.md
Implementation Plan/uat_v10_ces_web_capture_partial_20260527.md
Project_V13_Media_Downloader/v13_fb_media_downloader.py
capture_antigravity.py
config.py
```

Không đưa các file này nếu chứa dữ liệu thật/private trong môi trường khác:

```text
downloads/
outputs/
zalo_captures/
*_AI_ANALYSIS.md
*_AI_ANALYSIS.json
```

---

## 3. Prompt Chính

```text
Bạn là reviewer kỹ thuật cho repo CES Academy Automation.

Hãy đánh giá hai lượt chạy UAT đầu tiên:

1. V13 Facebook Downloader.
2. V10 CES Web Capture.

Chỉ dùng các file được cung cấp. Không giả định có dữ liệu Facebook/CES thật nếu summary nói bị chặn.

Yêu cầu output bằng tiếng Việt:

1. Kết luận ngắn: PASS, PARTIAL hay FAIL cho từng plan.
2. Bằng chứng chính từ UAT note, code và PROJECT_STATUS.
3. Kiểm tra xem code đã fail có summary chưa.
4. Kiểm tra xem docs/status có overclaim không.
5. Chỉ ra blocker còn lại để đạt PASS thật.
6. Viết checklist chạy lại cho agent khác.
7. Đề xuất 3-5 chỉnh sửa nhỏ nếu còn thiếu.

Giữ thuật ngữ English technical terms nếu cần, nhưng giải nghĩa tiếng Việt ở lần xuất hiện đầu tiên, ví dụ CDP là Chrome DevTools Protocol, giao thức điều khiển Chrome qua port debug.

Không phân tích nội dung riêng tư. Không yêu cầu upload raw screenshots/PDF/media.
```

---

## 4. Expected Gemini Verdict

Gemini phải kết luận:

| Plan | Verdict đúng |
|---|---|
| V13 Facebook | PARTIAL |
| V10 CES Web Capture | PARTIAL |

Gemini không được kết luận PASS vì:

- V13 chưa có Chrome debug `9222` hoặc tab Facebook đăng nhập thật.
- V10 bị redirect về `https://academy.cesglobal.com.vn/login.html`.

---

## 5. Sanitized Summary Nếu Không Gửi File JSON

Nếu không muốn gửi file summary local, paste đoạn này cho Gemini:

```text
V13 Facebook summary:
- posts_found: 0
- posts_saved: 0
- media_attempted: 0
- media_downloaded: 0
- error: no_facebook_tab_or_cdp_unavailable:http://localhost:9222/json
- output summary path local-only: downloads/v13_facebook/latest_run_summary.json

V10 CES summary:
- status: blocked_login
- requested_pages: 2
- cdp_url: http://localhost:9444
- viewer_url: https://academy.cesglobal.com.vn/viewer.html?id=43cc2aaa-7358-436a-a464-5630916f8aa2
- current_url: https://academy.cesglobal.com.vn/login.html
- title: Đăng nhập — CES ACADEMY
- pdf: empty
- error: authenticated session required
- output summary path local-only: outputs/v10_ces_web_capture/latest_run_summary.json
```

---

## 6. Câu Hỏi Test Gemini

Sau prompt chính, hỏi lần lượt:

```text
1. Có phần nào trong PROJECT_STATUS đang claim quá mức so với UAT note không?
2. V13 đã đủ gọi là live UAT chưa? Nếu chưa, thiếu điều kiện gì?
3. V10 đã đủ gọi là capture học liệu chưa? Nếu chưa, thiếu điều kiện gì?
4. Hai script đã có failure summary đủ để agent khác debug chưa?
5. Checklist chạy lại ngắn nhất để đạt PASS thật là gì?
```

---

## 7. Tiêu chí PASS Cho Gemini Test

Gemini output đạt nếu:

- Phân loại đúng `PARTIAL` cho cả hai.
- Không nhầm V13 port `9222` với V10 viewer port `9333` hoặc test port `9444`.
- Không nói V10 đã tạo PDF học liệu thật.
- Không yêu cầu upload raw private output.
- Chỉ ra rõ cần Chrome/Facebook session thật cho V13 và Chrome/CES session đã login cho V10.
- Đề xuất cập nhật docs/code dựa trên bằng chứng, không bịa thêm trạng thái.

Gemini output fail nếu:

- Kết luận PASS từ compile-only.
- Tự suy đoán Facebook/CES content.
- Bỏ qua blocker login/CDP.
- Gợi ý commit `downloads/` hoặc `outputs/`.

---

## 8. Expected Follow-Up Sau Gemini

Nếu Gemini review pass, agent tiếp theo có thể:

1. Mở Chrome debug `9222` có Facebook session thật và chạy lại V13.
2. Mở Chrome/CDP có CES login thật và chạy lại V10.
3. Sau khi có artifact thật, dùng `GEMINI_TEST_SCRIPT_20260527.md` để kiểm tra AI sidecar nội dung.
