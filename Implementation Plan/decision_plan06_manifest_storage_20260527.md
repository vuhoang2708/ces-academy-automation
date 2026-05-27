# Decision Note: Plan 06 — Second Brain Manifest Storage

**Ngày:** 2026-05-27  
**Handoff gốc:** `Agent Handoff/remaining_06_second_brain_manifest_storage_20260527.md`  
**Verdict:** **IMPLEMENTED**

---

## Quyết định

Tạo `record_artifact.py` riêng biệt (không tích hợp vào `analyze_artifact.py`) vì:
- `analyze_artifact.py` đã có scope rõ (tạo sidecar Markdown/JSON).
- Manifest writer cần chạy độc lập, không phụ thuộc vào sidecar.
- Tách biệt giúp dễ test và dễ gọi từ Hub Server sau này.

---

## Thay đổi đã thực hiện

| File | Thay đổi |
|---|---|
| `record_artifact.py` | Tạo mới — manifest writer JSONL |
| `outputs_manifest.jsonl` | Tạo tự động khi chạy (local-only, trong .gitignore) |

---

## Schema manifest record

```json
{
  "artifact_id": "...",
  "version": "...",
  "source_paths": [...],
  "artifact_paths": [...],
  "ai_markdown_path": "",
  "ai_json_path": "",
  "notebooklm_source_path": "",
  "notebooklm_prompt_path": "",
  "google_drive_url": "",
  "database_id": "",
  "privacy_classification": "unknown|private|internal|shareable",
  "created_at": "ISO8601",
  "sha256": "...",
  "tags": [...],
  "status": "registered|analyzed|notebooklm_ready|drive_uploaded|archived"
}
```

---

## Lệnh verify đã chạy

```powershell
# Compile
python -m py_compile record_artifact.py  → exit 0

# Dry-run với artifact test public
python record_artifact.py --artifact .\outputs\test_ai\sample_public.txt \
  --version TEST --privacy shareable --dry-run
→ In record JSON, không ghi file

# Ghi thật
python record_artifact.py --artifact .\outputs\test_ai\sample_public.txt \
  --version TEST --privacy shareable --tags "test,public,dummy"
→ Registered: sample_public (shareable)

# Kiểm tra JSONL
Get-Content .\outputs_manifest.jsonl -Encoding UTF8 | Select-Object -Last 3
→ Record hợp lệ với đủ fields
```

---

## Tiêu chí PASS

- [x] Manifest writer tồn tại và compile
- [x] Có ít nhất một record test không riêng tư
- [x] Schema có privacy_classification và storage status fields
- [x] `outputs_manifest.jsonl` trong `.gitignore`
- [x] Dry-run mode hoạt động
- [ ] NotebookLM source/prompt tự động tạo: **PENDING** — templates có sẵn, chưa tích hợp vào record_artifact.py (cần user xác nhận artifact nào cần NotebookLM pack)
- [ ] Google Drive sync: **DEFERRED** — field có trong schema, chưa implement (manual-first theo handoff)

---

## Chưa xác minh được

- Manifest với path private thật: chưa test (đúng — không nên test với data riêng tư).
- NotebookLM source-pack generator: chưa implement, templates có sẵn.
- Google Drive connector: chưa implement, field placeholder trong schema.
