# Master Plan: Ổn Định CES Academy Automation Và Đưa AI Lên Sớm

**Ngày:** 2026-05-27
**Phạm vi:** Lập kế hoạch trước khi sửa code. File này không tự động approve implementation.
**Nguồn chính:** `BAO_CAO_TONG_HOP_DU_AN.md` cộng với kiểm tra trực tiếp repo hiện tại.

---

## 1. Tóm Tắt Điều Hành

Dự án CES Academy Automation có chuỗi phát triển rõ từ V10 đến V14, nhưng repo hiện tại đang có ba nhóm vấn đề:

1. Một số tính năng trong tài liệu không khớp code thật.
2. Nhiều script phụ thuộc hardcoded path, UI state, hoặc dependency chưa được chuẩn hóa.
3. Ít nhất một source file bị corrupt và không compile được.

Hướng mới từ người dùng: không để AI ở Sprint 4 dài hạn nữa. Sau khi xử lý các blocker P0, cần đưa AI analysis lên sớm dưới dạng **AI sidecar** cho mọi artifact của V10-V14. AI trước mắt không cần full Hub/Portal; mỗi output capture/download nên có file phân tích đi kèm để biến dữ liệu thô thành tri thức dùng lại được.

---

## 2. Giải Thích Thuật Ngữ

- **Incident**: một vấn đề riêng có triệu chứng, nguyên nhân, kế hoạch xử lý và tiêu chí kiểm định.
- **Master plan**: kế hoạch tổng gom thứ tự ưu tiên và liên kết giữa các incident.
- **Verify**: kiểm tra xác nhận bằng command, log, file, runtime output hoặc UAT.
- **Hardcode**: ghi cứng đường dẫn, số trang, tọa độ, port hoặc cấu hình vào code.
- **Checkpoint**: điểm lưu trạng thái để có thể resume nếu chạy lỗi/dừng giữa chừng.
- **Hub Server**: server local để Portal gọi các script Python.
- **Spec-code drift**: tình trạng tài liệu/spec và code thực tế bị lệch nhau.
- **AI sidecar**: file phân tích AI đi kèm artifact gốc, ví dụ `*_AI_ANALYSIS.md`.
- **OCR**: nhận diện chữ từ ảnh hoặc PDF.
- **Second brain**: kho tri thức cá nhân có thể tìm lại, hỏi lại và liên kết về sau.

---

## 3. Hiện Trạng Kỹ Thuật

Đã xác nhận từ repo:

- Không có `AGENTS.md` ở project root hoặc parent trực tiếp.
- Git worktree đang dirty, có cả modified và untracked files.
- `Implementation Plan/` đã tồn tại.
- Chưa có `requirements.txt`.
- Không có `hub_server.py`, dù `TECHNICAL_SPEC_UNIFIED_HUB.md` từng claim Phase 2 đã hoàn thành.
- `Project_V13_Media_Downloader/v13_zalo_media_downloader.py` không compile được vì null bytes.
- V12 timestamp bug đã được sửa trong code hiện tại.
- Đã có V12 run đã validate và có AI sidecar mẫu: `zalo_captures/Zalo_Chat_History_20260527_103203_AI_ANALYSIS.md`.

Chưa xác minh:

- Live Facebook Group download behavior.
- Live SharePoint behavior.
- Live V14 Zalo media workflow.
- Gemini API key/model trong môi trường hiện tại.
- Chính sách upload dữ liệu riêng tư lên Google Drive/NotebookLM/cloud AI.

---

## 4. Bằng Chứng Đã Thu Thập

Các nhóm command đã chạy:

```powershell
rg --files
git status --short --branch
python -m py_compile ...
rg -n "timestamp|strftime" Project_V12_Zalo_Screenshot\capture_v12_zalo_pro.py
rg -n "hub_server" .
rg -n "except|pass|requests|websockets" Project_V13_Media_Downloader
```

Bằng chứng chính:

- V13 Zalo file compile lỗi null bytes.
- V12 code hiện dùng `%Y%m%d_%H%M%S`.
- V11 chỉ là screenshot loop, chưa thấy CV auto-stop/CSS injection/CDP.
- V13 main có silent exception.
- V17 có hardening tốt hơn.
- V14 mới ở mức diagnostic.
- `hub_server.py` không có trong repo.
- AI Brain đã có trong spec, nhưng trước đó bị đặt ở Sprint 4.

---

## 5. Danh Sách Incident

| Ưu tiên | File | Chủ đề | Trạng thái |
|---|---|---|---|
| P0 | `incident_01_v13_zalo_file_corrupt_20260527.md` | V13 Zalo file corrupt | Cần xử lý trước mọi Zalo media work |
| P0 | `incident_02_spec_code_drift_20260527.md` | Spec/code drift | Cần sửa trước khi tin roadmap |
| P1 | `incident_03_portability_and_launcher_paths_20260527.md` | Hardcoded path/launcher | Cần cho local use đáng tin |
| P1 | `incident_04_v11_sharepoint_production_gap_20260527.md` | V11 skeleton vs production claim | Cần trước khi gọi V11 production |
| P1 | `incident_05_v13_facebook_hardening_20260527.md` | V13 Facebook hardening | Cần giữ giá trị production |
| P1 | `incident_08_cross_version_ai_analysis_20260527.md` | AI analysis cho V10-V14 | Đưa AI lên sớm |
| P1 | `incident_09_second_brain_storage_architecture_20260527.md` | Google Drive/NotebookLM/database | Làm output tìm lại được |
| P2 | `incident_06_v14_zalo_desktop_completion_20260527.md` | V14 chưa hoàn thiện | Cần cho Zalo media automation |
| P2 | `incident_07_reproducible_environment_20260527.md` | Thiếu requirements/config/report | Nền tảng maintainability |

---

## 6. Thứ Tự Thực Thi Khuyến Nghị

1. Freeze trạng thái hiện tại.
   - Ghi lại git status.
   - Không ghi đè thay đổi của user.
   - Tách docs-only change khỏi source change.

2. Xử lý P0.
   - Restore/quarantine V13 Zalo corrupt file.
   - Sửa các claim tài liệu bị lệch repo thật.

3. Đưa AI sidecar lên sớm.
   - Chốt template `*_AI_ANALYSIS.md`.
   - Áp dụng cho V12 capture đã validate.
   - Mở rộng contract cho V10-V14.
   - Bổ sung các lens: nguyên văn, dàn ý, summary/CTA, tone, action items, second-brain links.

4. Thiết kế storage/second brain.
   - Local manifest trước.
   - NotebookLM source/prompt tách riêng.
   - Google Drive/database sync sau khi rõ privacy policy.

5. Ổn định local execution.
   - Bỏ hardcoded path.
   - Thêm config và requirements.
   - Thêm run summary.

6. Khôi phục/hoàn thiện module.
   - V11: restore hoặc downgrade docs.
   - V13: merge hardening.
   - V14: tiếp tục sau khi shared utilities ổn.

7. Hub Server/Portal để sau.
   - Chỉ xây khi local engine + AI sidecar + storage contract đã rõ.

---

## 7. Lựa Chọn Triển Khai

### Option A: AI-first stabilization

Xử lý P0, sau đó đưa AI sidecar vào các module đang chạy được.

Ưu điểm:

- Tạo giá trị ngay từ artifact hiện có.
- Không cần chờ full Portal.

Nhược điểm:

- Giai đoạn đầu có thể manual/agent-generated, chưa tự động hoàn toàn.

### Option B: Full local engine refactor

Chuẩn hóa config, logging, output, run report và AI sidecar cùng lúc.

Ưu điểm:

- Tốt cho maintain lâu dài.

Nhược điểm:

- Nhiều thay đổi hơn, cần review kỹ.

### Option C: Portal-first

Xây Hub/Portal trước rồi mới tích hợp AI.

Ưu điểm:

- UX cuối cùng đẹp hơn.

Nhược điểm:

- Không phù hợp ưu tiên hiện tại; dễ xây platform trước khi local output đáng tin.

Khuyến nghị: Option A trước, rồi chọn một phần Option B.

---

## 8. Rủi Ro Và Giảm Thiểu

| Rủi ro | Tác động | Cách giảm thiểu |
|---|---|---|
| UI automation phụ thuộc màn hình thật | Run flaky | Preflight + hướng dẫn rõ trước khi chạy |
| Facebook/Zalo UI thay đổi | Selector/template hỏng | Diagnostic + discovery bền hơn |
| Worktree dirty có thay đổi của user | Ghi đè nhầm | Luôn xem diff trước khi sửa |
| Spec overclaim | Agent tin sai | Đối chiếu repo thật và gắn status label rõ |
| Thiếu dependency | Không chạy được máy mới | `requirements.txt` + setup guide |
| AI sidecar chứa dữ liệu riêng tư | Rủi ro privacy | Local-only mặc định, hỏi trước khi upload |
| OCR/AI suy diễn sai | Summary gây hiểu nhầm | Nguyên văn + confidence + limitations |

---

## 9. Output Mong Đợi Sau Khi Duyệt

- V13 Zalo được restore hoặc quarantine rõ.
- Docs không còn claim sai về V12/V11/Hub Server.
- V10/launcher bỏ hardcoded path quan trọng.
- V13 Facebook có visible error và summary.
- Có `requirements.txt` và `config.py`.
- Có AI sidecar contract cho V10-V14.
- Có V12 AI analysis mẫu đã validate.
- Có NotebookLM source/prompt templates.
- Có second-brain storage plan: local, Google Drive, NotebookLM, database/index.

---

## 10. Tiêu Chí Kiểm Định

- `python -m py_compile` pass cho mọi Python file usable.
- V13 Zalo không còn null bytes hoặc được quarantine rõ.
- V11 docs khớp behavior thật.
- Specs không claim `hub_server.py` tồn tại nếu file chưa có.
- Mỗi artifact có thể tạo hoặc nhận `*_AI_ANALYSIS.md`.
- AI sidecar có source path, phạm vi nội dung, bóc tách nguyên văn, dàn ý, summary/CTA, tone, action items, storage links, confidence và limitations.

---

## 11. Câu Hỏi Còn Mở

1. V13 Zalo restore từ history hay chuyển hẳn sang V14?
2. V17 merge vào V13 main hay giữ riêng?
3. Gemini API dùng ngay hay bắt đầu bằng manual/agent sidecar?
4. AI sidecar có commit Git không hay local-only?
5. NotebookLM nhận raw capture, curated source pack, hay chỉ AI sidecar?
6. Google Drive sync manual trước hay tự động ngay?

---

## 12. Ghi Chú Cho Agent Khác

- Không tin `BAO_CAO_TONG_HOP_DU_AN.md` một cách tuyệt đối; phải đối chiếu repo thật.
- Không chạy PyAutoGUI nếu chưa cảnh báo user.
- Không upload Zalo/Facebook private data nếu chưa được duyệt rõ.
- Với NotebookLM, source file và prompt file phải tách riêng.
- Thuật ngữ chuyên môn có thể giữ tiếng Anh, nhưng phải giải nghĩa tiếng Việt có dấu.

---

## 13. Đánh Giá Cuối

Nên duyệt hướng: xử lý P0 trước, sau đó đưa AI sidecar lên sớm cho V10-V14, đồng thời thiết kế storage/second brain. Không nên xây full Hub/Portal trước khi local engine, AI output và storage contract đã vững.
