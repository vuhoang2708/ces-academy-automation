# Handoff 02: UAT V10 CES Web Capture Và Gắn AI Contract

**Ưu tiên:** P1
**Loại việc:** UAT + output contract
**Module:** `capture_antigravity.py`
**Plan liên quan:** `incident_03_portability_and_launcher_paths_20260527.md`, `incident_08_cross_version_ai_analysis_20260527.md`

---

## 1. Mục tiêu

Chạy lại V10 sau khi bỏ hardcoded Google Drive path để xác nhận:

- Output đi vào `outputs/v10_ces_web_capture/`.
- Script vẫn capture được viewer CES bằng CDP.
- Artifact V10 có thể đi kèm AI sidecar theo template chung.

---

## 2. Trạng thái hiện tại đã xác nhận

- `capture_antigravity.py` đã dùng `config.module_output_dir("v10_ces_web_capture")`.
- `PROJECT_STATUS.md` ghi V10 functional nhưng cần UAT lại.
- AI sidecar template đã có: `templates/ai_analysis_sidecar_template.md`.
- Chưa có script tự động tạo AI sidecar, nên bước AI có thể làm manual/agent-generated trước.

---

## 3. Điều kiện vào việc

1. User đã mở CES Academy viewer đúng tài liệu cần capture.
2. Chrome viewer có CDP port theo `config.VIEWER_CDP_URL`, mặc định `http://localhost:9333/json`.
3. User duyệt số trang test nhỏ trước, không chạy full nếu chưa cần.

---

## 4. Lệnh chuẩn bị

```powershell
git status --short --branch
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\capture_antigravity.py .\config.py
```

Kiểm tra config nhanh:

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -c "import config; print(config.OUTPUT_BASE); print(config.VIEWER_CDP_URL)"
```

---

## 5. Lệnh chạy test nhỏ

Nếu script hỗ trợ env `CES_V10_TOTAL_PAGES`, chạy 3-5 trang trước:

```powershell
$env:CES_V10_TOTAL_PAGES = "5"
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py .\capture_antigravity.py
```

Nếu script chưa đọc env đúng, agent cần sửa nhẹ để dùng `CES_V10_TOTAL_PAGES` rồi compile lại.

---

## 6. Kiểm tra output

```powershell
Get-ChildItem .\outputs\v10_ces_web_capture -Recurse -Force
git check-ignore -v .\outputs\v10_ces_web_capture
```

Mở 1-2 file output để xác nhận:

- Không bị blank.
- Không crop sai viewer.
- Không có toolbar/overlay che nội dung quan trọng.
- Số trang đúng với test nhỏ.

---

## 7. Gắn AI contract cho V10

Tạo sidecar mẫu cạnh artifact hoặc trong output folder theo tên:

```text
<artifact_base>_AI_ANALYSIS.md
```

Sidecar V10 phải có ít nhất:

- Source artifact.
- Phạm vi trang hoặc bài học.
- Bóc tách nguyên văn nếu OCR/đọc được.
- Dàn ý bài học.
- Tóm tắt ngắn và CTA nếu tài liệu có yêu cầu hành động.
- Khái niệm chính, glossary, câu hỏi còn mở.
- Confidence và limitations.
- Storage/second-brain status.

Nếu chưa dùng Gemini/OCR:

- Ghi `Phương pháp: manual/agent-generated từ ảnh/PDF`.
- Không claim full transcription nếu chỉ xem vài trang.

---

## 8. Tiêu chí PASS

PASS khi:

- V10 chạy test nhỏ thành công.
- Output nằm trong `outputs/v10_ces_web_capture/`, không còn phụ thuộc `G:\My Drive`.
- Có UAT note hoặc cập nhật `PROJECT_STATUS.md`.
- Có ít nhất một sidecar mẫu hoặc ghi rõ AI sidecar chờ `analyze_artifact.py`.

FAIL khi:

- Script vẫn ghi vào path hardcoded ngoài repo.
- Capture ra file blank/sai nội dung.
- Docs claim V10 verified full run dù mới test nhỏ.

---

## 9. File được phép sửa

- `capture_antigravity.py`
- `config.py` nếu chỉ sửa config discovery
- `PROJECT_STATUS.md`
- `README.md`
- UAT note mới trong `Implementation Plan/`

Không commit:

- `outputs/`
- PDF/screenshot chứa nội dung học liệu riêng tư nếu chưa duyệt.

---

## 10. Lượt chạy Codex 2026-05-27

Kết quả: PARTIAL.

- Compile pass.
- Test dùng Chrome debug riêng tại `http://localhost:9444`.
- CES redirect về `https://academy.cesglobal.com.vn/login.html`, nên chưa capture được giáo trình thật.
- Script đã được sửa để ghi `outputs/v10_ces_web_capture/latest_run_summary.json` với status `blocked_login` và không tạo PDF giả thành công.
- Xem chi tiết: `Implementation Plan/uat_v10_ces_web_capture_partial_20260527.md`.
