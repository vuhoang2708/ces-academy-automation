# Handoff 05: Triển Khai CLI AI Analyzer Cho V10-V14

**Ưu tiên:** P1
**Loại việc:** implementation sau khi đã có template
**Module đề xuất:** `analyze_artifact.py` hoặc `tools/analyze_artifact.py`
**Plan gốc:** `incident_08_cross_version_ai_analysis_20260527.md`

---

## 1. Mục tiêu

Tạo CLI analyzer nhận một file/folder artifact và sinh ra:

```text
<artifact_base>_AI_ANALYSIS.md
<artifact_base>_AI_ANALYSIS.json
```

Analyzer phải áp dụng cùng contract cho V10-V14:

1. Bóc tách nguyên văn.
2. Dàn ý chi tiết.
3. Tóm tắt ngắn và CTA nếu có.
4. Phân tích ngữ điệu/cách tiếp cận của từng đối tượng.
5. Các lens bổ sung: entity, action item, timeline, risk, follow-up, repurpose, second-brain tags.

---

## 2. Trạng thái hiện tại đã xác nhận

- Đã có template: `templates/ai_analysis_sidecar_template.md`.
- Đã có Gemini test script: `Gemini_Test/GEMINI_TEST_SCRIPT_20260527.md`.
- `.gitignore` đang ignore `*_AI_ANALYSIS.md` và `*_AI_ANALYSIS.json` để tránh commit dữ liệu riêng tư.
- Chưa có Gemini API key/model được xác minh.

---

## 3. Quy tắc privacy bắt buộc

Mặc định analyzer chạy local-only.

Không được gửi artifact lên Gemini/cloud API nếu chưa có approval rõ từ user trong chính lượt làm việc đó.

CLI phải có flag rõ:

```text
--mode manual
--mode local-ocr
--mode gemini
```

Với `--mode gemini`, nếu không có `--allow-cloud-upload`, script phải dừng và in cảnh báo.

---

## 4. Interface đề xuất

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py .\analyze_artifact.py --input ".\outputs\v10_ces_web_capture\sample.pdf" --version V10 --mode manual
```

Với folder screenshots:

```powershell
& $py .\analyze_artifact.py --input ".\zalo_captures" --version V12 --mode manual --private
```

Với Gemini, chỉ sau approval:

```powershell
& $py .\analyze_artifact.py --input "<artifact>" --version V13 --mode gemini --allow-cloud-upload
```

---

## 5. Thiết kế tối thiểu

CLI cần:

- Detect input là file hay folder.
- Tính hash SHA256 cho source artifact.
- Tạo output path cạnh artifact hoặc trong `outputs/ai_analysis/`.
- Load template Markdown từ `templates/ai_analysis_sidecar_template.md`.
- Ghi JSON theo keys trong `incident_08`.
- Ghi `confidence` và `limitations`.
- Ghi privacy status: `private`, `shareable`, hoặc `unknown`.
- Không overwrite file cũ nếu chưa có `--force`.

---

## 6. JSON schema tối thiểu

```json
{
  "sources": [],
  "version": "",
  "content_range": "",
  "verbatim_extraction": [],
  "detailed_outline": [],
  "summary": "",
  "cta": "",
  "tone_analysis": [],
  "key_points": [],
  "entities": [],
  "action_items": [],
  "analysis_lenses": {},
  "follow_up_questions": [],
  "storage_links": {},
  "confidence": "",
  "limitations": [],
  "privacy": {
    "classification": "unknown",
    "cloud_upload_allowed": false
  }
}
```

---

## 7. Validation

Compile:

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\analyze_artifact.py
```

Dry-run với dummy text không riêng tư:

```powershell
New-Item -ItemType Directory -Force .\outputs\test_ai | Out-Null
Set-Content -Path .\outputs\test_ai\sample_public.txt -Value "Test public artifact. CTA: follow up tomorrow." -Encoding UTF8
& $py .\analyze_artifact.py --input .\outputs\test_ai\sample_public.txt --version TEST --mode manual --force
Get-ChildItem .\outputs\test_ai
```

PASS khi:

- Tạo Markdown và JSON.
- JSON parse được.
- Markdown có đủ các section bắt buộc.
- Không gọi cloud khi thiếu `--allow-cloud-upload`.
- Không commit output AI chứa dữ liệu riêng tư.

---

## 8. File được phép sửa/tạo

- `analyze_artifact.py` hoặc `tools/analyze_artifact.py`
- `templates/ai_analysis_sidecar_template.md` nếu cần bổ sung placeholder
- `README.md`
- `PROJECT_STATUS.md`
- `requirements.txt` nếu thêm dependency OCR/API
- Test/dummy artifact không riêng tư dưới `outputs/test_ai/` nếu đã ignore

Không dùng V12 chat private làm test public.
