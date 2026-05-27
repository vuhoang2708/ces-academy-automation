# PROJECT STATUS: CES Academy Automation

**Ngày cập nhật:** 2026-05-27 (handoff 03+04 completed)
**Mục đích:** Nguồn trạng thái hiện tại để tránh spec-code drift.

---

## Trạng Thái Module

| Module | Trạng thái hiện tại | Ghi chú |
|---|---|---|
| V10 CES Web Capture | Partial UAT, blocked by login | Đã bỏ hardcoded Google Drive path; test 2026-05-27 ghi summary `blocked_login`, cần Chrome/CES session đã đăng nhập để PASS. |
| V11 SharePoint | Skeleton/basic screenshot | Chưa có CV auto-stop/CSS injection trong code hiện tại. Decision: Hướng A (basic). Xem `Implementation Plan/decision_v11_sharepoint_basic_20260527.md`. |
| V12 Zalo Screenshot | Validated test run | Đã có restore minimized window, focus click và duplicate detection. |
| V13 Facebook | Partial UAT, blocked by missing CDP | Đã thêm timeout, MIME check, streaming download và run summary; test 2026-05-27 thiếu Chrome debug `9222`, cần live Facebook session để PASS. |
| V13 Zalo | Quarantined/unavailable — RETIRED | File cũ corrupt/null bytes; không có source hợp lệ trong Git history. Stub compile-safe. Zalo media → V14. Xem `Implementation Plan/decision_v13_zalo_retired_20260527.md`. |
| V14 Zalo Desktop | Diagnostic only | Chưa phải downloader end-to-end. |
| Hub Server / Portal | Planned | `hub_server.py` chưa có trong repo hiện tại. |
| AI sidecar | Local CLI scaffold implemented | Có `analyze_artifact.py` tạo Markdown/JSON local-only; Gemini API vẫn chưa gọi tự động. |

---

## Quy Tắc Truth

- File này ưu tiên hơn các spec cũ khi nói về trạng thái hiện tại.
- Claim `completed` chỉ hợp lệ nếu có file thật và validation tương ứng.
- Raw captures, chat screenshots và AI sidecar chứa dữ liệu riêng tư mặc định là local-only.
