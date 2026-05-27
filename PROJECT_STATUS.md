# PROJECT STATUS: CES Academy Automation

**Ngày cập nhật:** 2026-05-27 (handoff 03+04+06+07+08+09 completed; V10/V13 live UAT attempted)
**Mục đích:** Nguồn trạng thái hiện tại để tránh spec-code drift.

---

## Trạng Thái Module

| Module | Trạng thái hiện tại | Ghi chú |
|---|---|---|
| V10 CES Web Capture | Partial UAT, blocked by login | Script compile OK; phát hiện login redirect đúng. Blocker: cần Chrome session CES đã đăng nhập. Xem `Implementation Plan/uat_v10_ces_live_partial_20260527.md`. |
| V11 SharePoint | Skeleton/basic screenshot | Chưa có CV auto-stop/CSS injection trong code hiện tại. Decision: Hướng A (basic). Xem `Implementation Plan/decision_v11_sharepoint_basic_20260527.md`. |
| V12 Zalo Screenshot | Validated test run | Đã có restore minimized window, focus click và duplicate detection. |
| V13 Facebook | Partial UAT, blocked by missing CDP | Script compile OK; fail path có summary rõ. Blocker: cần Chrome debug port 9222 + Facebook session. Xem `Implementation Plan/uat_v13_facebook_live_partial_20260527.md`. |
| V13 Zalo | Quarantined/unavailable — RETIRED | File cũ corrupt/null bytes; không có source hợp lệ trong Git history. Stub compile-safe. Zalo media → V14. Xem `Implementation Plan/decision_v13_zalo_retired_20260527.md`. |
| V14 Zalo Desktop | DRY_RUN_READY | 3-mode CLI (diagnostic/dry-run/execute). Diagnostic PASS + Dry-run PASS 2026-05-27. Execute cần calibration. Xem `Implementation Plan/decision_plan07_v14_zalo_dryrun_20260527.md`. |
| Hub Server / Portal | Minimal implemented | `hub_server.py` có /health /modules /artifacts. Bind 127.0.0.1 only. POST /run blocked. Xem `Implementation Plan/decision_plan08_hub_server_minimal_20260527.md`. |
| AI sidecar | Local CLI scaffold implemented | Có `analyze_artifact.py` tạo Markdown/JSON local-only; `record_artifact.py` ghi manifest JSONL. Gemini API chưa gọi tự động. |

---

## Quy Tắc Truth

- File này ưu tiên hơn các spec cũ khi nói về trạng thái hiện tại.
- Claim `completed` chỉ hợp lệ nếu có file thật và validation tương ứng.
- Raw captures, chat screenshots và AI sidecar chứa dữ liệu riêng tư mặc định là local-only.
