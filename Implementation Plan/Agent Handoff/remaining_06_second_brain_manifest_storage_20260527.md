# Handoff 06: Manifest Và Storage Cho Second Brain

**Ưu tiên:** P1
**Loại việc:** local storage contract + optional sync
**Plan gốc:** `incident_09_second_brain_storage_architecture_20260527.md`

---

## 1. Mục tiêu

Làm lớp lưu trữ tối thiểu để mọi artifact và AI sidecar có thể tìm lại về sau:

- Manifest local dạng JSONL hoặc SQLite.
- Link tới artifact gốc, AI Markdown, AI JSON.
- Trạng thái Google Drive/NotebookLM/database.
- Privacy classification.

Chưa cần tự động upload Google Drive ngay nếu privacy policy chưa rõ.

---

## 2. Trạng thái hiện tại đã xác nhận

- Có template manifest: `templates/manifest_record_template.json`.
- Có templates NotebookLM:
  - `templates/notebooklm_source_template.md`
  - `templates/notebooklm_prompt_template.md`
- Repo chưa có Google Drive sync implementation.
- Repo chưa có NotebookLM source-pack generator.

---

## 3. Thiết kế tối thiểu

Tạo script:

```text
record_artifact.py
```

Hoặc tích hợp vào `analyze_artifact.py` nếu Handoff 05 đã hoàn thành.

Output local:

```text
outputs_manifest.jsonl
```

Mỗi dòng là một record JSON gồm:

- `artifact_id`
- `version`
- `source_paths`
- `artifact_paths`
- `ai_markdown_path`
- `ai_json_path`
- `notebooklm_source_path`
- `notebooklm_prompt_path`
- `google_drive_url`
- `database_id`
- `privacy_classification`
- `created_at`
- `sha256`
- `tags`
- `status`

---

## 4. NotebookLM source-pack flow

Không import raw dump mặc định.

Với mỗi artifact quan trọng:

1. Tạo source file từ `templates/notebooklm_source_template.md`.
2. Chỉ giữ nội dung sạch, đúng phạm vi.
3. Tạo prompt file riêng từ `templates/notebooklm_prompt_template.md`.
4. Ghi cả hai path vào manifest.
5. Nếu user tự import vào NotebookLM, agent cập nhật notebook URL/manual ID vào manifest sau.

---

## 5. Google Drive flow

Giai đoạn 1: manual-first.

- Manifest có field `google_drive_url` nhưng để trống hoặc `planned`.
- Không dùng connector/upload tự động khi chưa có approval dữ liệu riêng tư.
- Nếu user duyệt upload một source pack đã cắt riêng tư, ghi rõ file nào được upload và link nào nhận về.

Giai đoạn 2: automate sau khi có policy.

- Có thể thêm script sync riêng.
- Chỉ sync curated source pack/AI summary, không sync raw screenshot mặc định.

---

## 6. Lệnh validation

Nếu tạo `record_artifact.py`:

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\record_artifact.py
& $py .\record_artifact.py --artifact .\outputs\test_ai\sample_public.txt --version TEST --privacy shareable --dry-run
```

Kiểm tra JSONL:

```powershell
Get-Content .\outputs_manifest.jsonl -Encoding UTF8 | Select-Object -Last 3
```

Nếu `outputs_manifest.jsonl` chứa đường dẫn private thật, phải để local-only và không commit.

---

## 7. Tiêu chí PASS

PASS khi:

- Có manifest writer hoặc quy trình ghi manifest rõ.
- Có ít nhất một record test không riêng tư.
- NotebookLM source/prompt được tạo tách riêng.
- Manifest có privacy fields và storage status.
- `.gitignore` vẫn bảo vệ manifest nếu có dữ liệu riêng tư.

FAIL khi:

- Trộn prompt instruction vào NotebookLM source.
- Upload raw data riêng tư lên Drive/NotebookLM không có approval.
- Commit manifest chứa path/nội dung riêng tư.

---

## 8. File được phép sửa/tạo

- `record_artifact.py` hoặc tích hợp `analyze_artifact.py`
- `templates/manifest_record_template.json`
- `templates/notebooklm_source_template.md`
- `templates/notebooklm_prompt_template.md`
- `README.md`
- `PROJECT_STATUS.md`
