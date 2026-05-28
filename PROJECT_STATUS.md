# PROJECT STATUS: CES Academy Automation

**Ngày cập nhật:** 2026-05-28 (Gemini Browser UAT for open blockers completed)
**Mục đích:** Nguồn trạng thái hiện tại để tránh spec-code drift.

---

## Trạng Thái Module

| Module | Trạng thái hiện tại | Ghi chú |
|---|---|---|
| V10 CES Web Capture | Live UAT PASS | Script captured pages and generated PDF via CDP port 9555. Xem `Implementation Plan/uat_v10_ces_browser_live_pass_20260528.md`. |
| V11 SharePoint | Skeleton/basic screenshot | Chưa có CV auto-stop/CSS injection trong code hiện tại. Decision: Hướng A (basic). Xem `Implementation Plan/decision_v11_sharepoint_basic_20260527.md`. |
| V12 Zalo Screenshot | Validated test run | Đã có restore minimized window, focus click và duplicate detection. |
| V13 Facebook | Live UAT PASS | Script found 14 posts and saved 3 via CDP port 9222. Xem `Implementation Plan/uat_v13_facebook_browser_live_pass_20260528.md`. |
| V13 Zalo | Quarantined/unavailable — RETIRED | File cũ corrupt/null bytes; không có source hợp lệ trong Git history. Stub compile-safe. Zalo media → V14. Xem `Implementation Plan/decision_v13_zalo_retired_20260527.md`. |
| V14 Zalo Desktop | DRY_RUN_READY | Browser review of diagnostic PNG completed; media panel not open. Cần calibration thêm. Xem `Implementation Plan/uat_v14_browser_calibration_partial_20260528.md`. |
| Hub Server / Portal | Minimal implemented (Smoke PASS) | `hub_server.py` có /health /modules /artifacts. Đã test bằng Browser. Xem `Implementation Plan/uat_hub_browser_smoke_pass_20260528.md`. |
| AI sidecar | Local CLI scaffold implemented | Có `analyze_artifact.py` tạo Markdown/JSON local-only; `record_artifact.py` ghi manifest JSONL. Gemini API chưa gọi tự động. |

---

## Quy Tắc Truth

- File này ưu tiên hơn các spec cũ khi nói về trạng thái hiện tại.
- Claim `completed` chỉ hợp lệ nếu có file thật và validation tương ứng.
- Raw captures, chat screenshots và AI sidecar chứa dữ liệu riêng tư mặc định là local-only.
