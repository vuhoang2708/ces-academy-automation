# UAT Result: AI CLI Analyzer

**Ngày chạy:** 2026-05-27
**Người chạy:** Codex
**Kết quả:** PASS cho local scaffold, PARTIAL cho Gemini automation
**Module:** `analyze_artifact.py`

---

## 1. Mục tiêu

Thực hiện Handoff 05: tạo CLI analyzer nhận artifact file/folder và sinh sidecar:

```text
<artifact_base>_AI_ANALYSIS.md
<artifact_base>_AI_ANALYSIS.json
```

Analyzer phải mặc định local-only, không upload cloud khi chưa được duyệt.

---

## 2. Kết quả implementation

Đã tạo:

```text
analyze_artifact.py
```

Các mode:

- `manual`: tạo sidecar Markdown/JSON từ text đọc được và source inventory.
- `local-ocr`: tạo scaffold nhưng ghi rõ OCR engine chưa được cấu hình.
- `gemini`: bị chặn nếu thiếu `--allow-cloud-upload`; repo hiện chưa gọi Gemini API tự động.

---

## 3. Validation đã chạy

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\analyze_artifact.py
```

```powershell
New-Item -ItemType Directory -Force .\outputs\test_ai | Out-Null
Set-Content -Path .\outputs\test_ai\sample_public.txt -Value "Test public artifact. CTA: follow up tomorrow." -Encoding UTF8
& $py .\analyze_artifact.py --input .\outputs\test_ai\sample_public.txt --version TEST --mode manual --privacy shareable --force
```

```powershell
& $py -c "import json; json.load(open('outputs/test_ai/sample_public_AI_ANALYSIS.json', encoding='utf-8')); print('JSON_OK')"
```

Cloud guard:

```powershell
& $py .\analyze_artifact.py --input .\outputs\test_ai\sample_public.txt --version TEST --mode gemini
```

Expected: command exits blocked unless `--allow-cloud-upload` is explicitly provided.

---

## 4. Tiêu chí PASS

PASS khi:

- `py_compile` pass.
- Tạo được Markdown và JSON.
- JSON parse được.
- Markdown có source inventory, bóc tách nguyên văn, dàn ý, CTA, limitations và storage fields.
- Gemini mode không upload khi thiếu approval flag.
- Output test nằm dưới `outputs/` và không bị Git track.

---

## 5. Giới hạn còn lại

- Chưa tích hợp OCR thật cho PDF/ảnh/media.
- Chưa tích hợp Gemini API tự động.
- Analyzer hiện là scaffold có guard privacy, không thay thế human/Gemini review cho dữ liệu phức tạp.
