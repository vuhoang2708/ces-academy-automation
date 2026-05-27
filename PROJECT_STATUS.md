# PROJECT STATUS: CES Academy Automation

**Ngày cập nhật:** 2026-05-27
**Mục đích:** Nguồn trạng thái hiện tại để tránh spec-code drift.

---

## Trạng Thái Module

| Module | Trạng thái hiện tại | Ghi chú |
|---|---|---|
| V10 CES Web Capture | Functional, cần UAT lại | Đã bỏ hardcoded Google Drive path; output mặc định nằm trong `outputs/`. |
| V11 SharePoint | Skeleton/basic screenshot | Chưa có CV auto-stop/CSS injection trong code hiện tại. |
| V12 Zalo Screenshot | Validated test run | Đã có restore minimized window, focus click và duplicate detection. |
| V13 Facebook | Hardened script, cần live UAT | Đã thêm timeout, MIME check, streaming download và run summary. |
| V13 Zalo | Quarantined/unavailable | File cũ corrupt/null bytes; hiện là stub báo unavailable. |
| V14 Zalo Desktop | Diagnostic only | Chưa phải downloader end-to-end. |
| Hub Server / Portal | Planned | `hub_server.py` chưa có trong repo hiện tại. |
| AI sidecar | Early P1 scope | Có template và Gemini test script; chưa gọi API tự động. |

---

## Quy Tắc Truth

- File này ưu tiên hơn các spec cũ khi nói về trạng thái hiện tại.
- Claim `completed` chỉ hợp lệ nếu có file thật và validation tương ứng.
- Raw captures, chat screenshots và AI sidecar chứa dữ liệu riêng tư mặc định là local-only.
