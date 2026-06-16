# Handoff Index: Các Plan Còn Lại Chưa Thực Hiện Xong

**Ngày:** 2026-05-27
**Repo/branch hiện tại:** `codex/ces-ai-stabilization`
**Mục đích:** Danh sách việc còn lại để giao từng agent khác chạy tuần tự, có bằng chứng, không claim quá tay.

---

## 1. Thuật ngữ dùng chung

- **UAT**: kiểm thử chấp nhận trên workflow thật, không chỉ chạy compile.
- **CDP**: Chrome DevTools Protocol, giao thức để script điều khiển Chrome qua port debug.
- **AI sidecar**: file phân tích AI đi kèm artifact gốc, ví dụ `*_AI_ANALYSIS.md`.
- **Manifest**: mục lục metadata để lưu đường dẫn artifact, hash, tag, link Google Drive, NotebookLM, database ID.
- **Dry-run**: chạy thử không tải/chỉnh thật, chỉ ghi log hoặc screenshot chẩn đoán.
- **Local-only**: chỉ lưu trên máy local, không upload GitHub/Google Drive/cloud API.
- **Cloud API**: API chạy trên máy chủ bên ngoài, ví dụ Gemini API; không gửi dữ liệu riêng tư nếu chưa được duyệt rõ.

---

## 2. Trạng thái đã xử lý một phần

Các phần này đã có nền tảng, nhưng chưa đủ gọi là hoàn tất toàn bộ roadmap:

| Mảng | Trạng thái hiện tại | Việc còn lại |
|---|---|---|
| V12 Zalo Screenshot | Đã validate test run | Chỉ cần giữ như baseline, không mở rộng nếu không có yêu cầu mới |
| Portability/config | Đã có `config.py`, output repo-relative | Cần UAT lại V10/V13 với config mới |
| V13 Zalo corrupt | Đã quarantine bằng stub compile-safe | Cần quyết định restore legacy hay chuyển hẳn sang V14 |
| V13 Facebook | Đã harden script | Cần live UAT với Facebook session thật |
| AI sidecar | Đã có template và Gemini test script | Chưa có CLI analyzer tự động |
| Second brain | Đã có plan và templates | Chưa có manifest writer/sync flow |
| Hub/Portal | Đã sửa docs không claim completed | Chưa implement `hub_server.py` hoặc Portal |

---

## 3. Thứ tự chạy khuyến nghị

1. `remaining_01_v13_facebook_live_uat_20260527.md`
2. `remaining_02_v10_uat_and_ai_contract_20260527.md`
3. `remaining_03_v11_sharepoint_decision_20260527.md`
4. `remaining_04_v13_zalo_decision_20260527.md`
5. `remaining_05_ai_cli_analyzer_20260527.md`
6. `remaining_06_second_brain_manifest_storage_20260527.md`
7. `remaining_07_v14_zalo_media_completion_20260527.md`
8. `remaining_08_hub_server_portal_future_20260527.md`
9. `remaining_09_stale_plan_cleanup_20260527.md`

Lý do thứ tự:

- V13 Facebook và V10 là các module có thể UAT nhanh nhất sau khi đã sửa config/hardening.
- V11/V13 Zalo là quyết định scope: restore, rebuild, hoặc giữ limitation.
- AI CLI và manifest nên làm trước Hub/Portal để có output thật cho platform index.
- V14 cần UAT desktop Zalo thật nên để sau khi shared Zalo/AI/storage contract rõ hơn.
- Hub/Portal chỉ nên làm khi local engine, AI sidecar và manifest đã ổn.

---

## 4. Quy tắc chung cho mọi agent

- Trước khi sửa, chạy `git status --short --branch`.
- Không stage raw capture, screenshot chat, media riêng tư, hoặc AI sidecar chứa nội dung riêng tư.
- Không upload Zalo/Facebook data lên Gemini, Google Drive, NotebookLM nếu chưa có approval rõ.
- Không gọi module là `production-ready` nếu chưa có UAT note và artifact thật.
- Nếu dùng PyAutoGUI hoặc điều khiển desktop, phải báo rõ cửa sổ nào sẽ bị thao tác.
- Sau khi làm xong, cập nhật ít nhất một trong các file status/docs tương ứng: `PROJECT_STATUS.md`, `README.md`, incident liên quan, hoặc UAT note.
- Nếu có code change, chạy compile check tối thiểu với portable Python nếu môi trường chính thiếu dependency.

---

## 5. Bằng chứng hiện tại cần giữ nguyên

- `PROJECT_STATUS.md` là nguồn trạng thái hiện tại.
- `README.md` đã ghi raw captures và AI analysis riêng tư không commit lên GitHub.
- `.gitignore` đã ignore `downloads/`, `outputs/`, `zalo_captures/`, `*_AI_ANALYSIS.md`, `*_AI_ANALYSIS.json`.
- Commit hiện tại trên nhánh: `7e1eb4a stabilize CES automation and add AI sidecar plans`.
- Hai file plan cũ đang untracked:
  - `Project_V13_Media_Downloader/implementation_plan_20260419_UAT_V13_FB.md`
  - `Project_V13_Media_Downloader/implementation_plan_20260419_V13_Timeline.md`

---

## 6. Mẫu phản hồi cuối cho agent

Agent khác sau khi chạy xong nên trả lời theo mẫu:

```text
Đã chạy plan: <tên file handoff>

Kết quả:
- PASS/FAIL/PARTIAL:
- Artifact tạo ra:
- File đã sửa:
- Lệnh verify đã chạy:
- Việc chưa làm được:
- Rủi ro còn lại:

Không upload dữ liệu riêng tư ra ngoài: Có/Không, chi tiết.
Git status cuối: <kết quả ngắn>
```
