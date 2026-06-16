# Incident 09: Kiến Trúc Lưu Trữ Second Brain Cho AI Output

**Ngày:** 2026-05-27
**Mức độ ưu tiên:** P1
**Trạng thái:** Planning item mới
**Phạm vi:** Local archive, Google Drive, NotebookLM, database/index

---

## 1. Tóm Tắt Điều Hành

AI analysis chỉ có giá trị dài hạn nếu có thể lưu, link, tìm lại và tái sử dụng. Người dùng muốn output được liên kết với Google Drive hoặc database khác, đồng thời có khả năng đưa vào NotebookLM để xây second brain trong tương lai.

Kiến trúc đề xuất là lưu trữ nhiều lớp:

1. Local artifact là nguồn gốc ngay sau khi capture.
2. Mỗi artifact có AI sidecar Markdown và tùy chọn JSON.
3. Manifest/index lưu path, hash, timestamp, tag, storage ID.
4. Source pack sạch được sync lên Google Drive và có thể import vào NotebookLM.
5. Database lưu metadata/search index; không nhất thiết lưu toàn bộ raw private content.

---

## 2. Giải Thích Thuật Ngữ

- **Second brain**: kho tri thức cá nhân có thể tìm lại, hỏi lại, và liên kết về sau.
- **Manifest**: file mục lục chứa metadata của artifact và analysis.
- **Storage ID**: mã hoặc link file/record trong Google Drive, database, hoặc NotebookLM pack.
- **NotebookLM source pack**: file nội dung đã làm sạch để import vào NotebookLM.
- **Prompt file**: file riêng chứa instruction cho NotebookLM, không trộn với source.
- **Index**: lớp dữ liệu giúp tìm kiếm/lọc theo tag, người, chủ đề, ngày, source.

---

## 3. Mục Tiêu Người Dùng

Sau khi chạy bất kỳ module V10-V14 nào, người dùng cần biết:

- Raw capture nằm ở đâu?
- AI analysis nằm ở đâu?
- Đã sync Google Drive chưa?
- Có source file sẵn cho NotebookLM chưa?
- Artifact liên quan tới tag/người/chủ đề nào?
- Hub hoặc database tương lai có tìm lại được không?

---

## 4. Hiện Trạng Kỹ Thuật

Đã xác nhận:

- AI sidecar template đã có phần Storage and Second-Brain Links.
- Có V12 analysis sample: `zalo_captures/Zalo_Chat_History_20260527_103203_AI_ANALYSIS.md`.
- Repo chưa có database/index schema.
- Repo chưa có Google Drive sync implementation.
- Repo chưa có NotebookLM source-pack generator.

Kinh nghiệm đã chốt từ workflow NotebookLM trước đây:

- Nên tách thành hai artifact: một source file sạch để import và một prompt/instruction file riêng.

Chưa xác minh:

- Có nên dùng connector Google Drive trực tiếp cho repo này hay không.
- NotebookLM ingestion có tự động hóa được không, hay vẫn manual import.
- Database nên là SQLite, JSONL manifest, Google Sheets, hay vector DB.

---

## 5. Mô Hình Lưu Trữ Đề Xuất

Cấu trúc local khuyến nghị:

```text
outputs/
  v12_zalo/
    20260527_103203/
      artifact.pdf
      pages/
        page_001.png
      analysis/
        artifact_AI_ANALYSIS.md
        artifact_AI_ANALYSIS.json
      notebooklm/
        artifact_NOTEBOOKLM_SOURCE.md
        artifact_NOTEBOOKLM_PROMPT.md
      manifest.json
```

Repo hiện tại có thể áp dụng dần, không cần di chuyển ngay toàn bộ file cũ.

---

## 6. Manifest Contract

Mỗi run nên ghi hoặc cập nhật một manifest record:

```json
{
  "artifact_id": "v12_zalo_20260527_103203",
  "version": "V12",
  "source_type": "zalo_chat_capture",
  "created_at": "2026-05-27T10:32:03+07:00",
  "local_sources": [],
  "analysis_md": "",
  "analysis_json": "",
  "notebooklm_source": "",
  "notebooklm_prompt": "",
  "google_drive_links": [],
  "database_id": "",
  "tags": [],
  "people": [],
  "projects": [],
  "privacy_level": "private",
  "sync_status": "local_only"
}
```

---

## 7. Workflow NotebookLM

Không import raw output nhiễu vào NotebookLM theo mặc định.

Luồng khuyến nghị:

1. Tạo `*_NOTEBOOKLM_SOURCE.md`
   - nội dung sạch;
   - đúng phạm vi;
   - đủ bối cảnh;
   - loại bỏ lặp/nhiễu/raw dump.

2. Tạo `*_NOTEBOOKLM_PROMPT.md`
   - instruction riêng;
   - yêu cầu output cụ thể như Video Overview, FAQ, briefing, timeline, study guide.

3. Import source vào NotebookLM thủ công hoặc bán tự động.

4. Lưu NotebookLM notebook URL/manual ID vào manifest khi có.

---

## 8. Workflow Google Drive

### Phase 1: Manual link field

Sidecar có trường Google Drive link ở trạng thái `planned`. Người dùng upload thủ công nếu cần.

### Phase 2: Drive sync script

Thêm script sync artifact đã chọn và ghi link/ID trả về vào manifest.

### Phase 3: Drive folder taxonomy

Folder đề xuất:

```text
CES Academy Automation/
  01_Raw_Captures/
  02_AI_Analysis/
  03_NotebookLM_Source_Packs/
  04_Exports_For_Sharing/
```

---

## 9. Lựa Chọn Database

| Option | Phù hợp nhất cho | Tradeoff |
|---|---|---|
| JSONL manifest | Bắt đầu nhanh local | Query/search còn hạn chế |
| SQLite | Local index bền hơn | Cần schema/migration |
| Google Sheets | Dễ review bằng mắt | Yếu với dữ liệu lớn/riêng tư |
| Vector DB | Semantic search | Tăng độ phức tạp và câu hỏi privacy |

Khuyến nghị: bắt đầu với JSONL manifest, sau đó thêm SQLite nếu schema ổn.

---

## 10. Rủi Ro Và Giảm Thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| Upload nhầm chat riêng tư | Mặc định `privacy_level=private`, `sync_status=local_only` |
| NotebookLM bị nhiễu raw data | Chỉ import curated source pack |
| Link bị đổi/mất | Lưu cả local hash và Drive file ID |
| Database quan trọng hơn file gốc | Local artifact + manifest vẫn là source of truth |
| Git track nhầm private output | Thêm `.gitignore` policy trước khi scale |

---

## 11. Output Mong Đợi

Sau khi duyệt:

- `outputs_manifest.jsonl` hoặc local index tương đương.
- AI sidecar template có storage fields.
- NotebookLM source/prompt template pair.
- Storage policy: cái gì local-only, cái gì được sync Drive.
- Per-artifact status: `local_only`, `drive_synced`, `notebooklm_ready`, `notebooklm_imported`, `db_indexed`.

---

## 12. Kế Hoạch Thực Thi Sau Khi Duyệt

1. Chốt manifest fields.
2. Tạo NotebookLM source/prompt templates.
3. Áp cấu trúc này cho V12 capture hiện tại làm pilot.
4. Chốt privacy policy.
5. Thêm Google Drive sync sau khi chính sách rõ.
6. Thêm SQLite/JSONL indexing sau vài pilot artifact.

---

## 13. Câu Hỏi Còn Mở

1. Google Drive sync làm manual trước hay automate ngay?
2. NotebookLM pack tạo cho mọi capture hay chỉ capture quan trọng?
3. Upload raw screenshots/PDF hay chỉ upload AI summary/source pack?
4. Database nằm trong repo, Google Drive, hay folder Hub Server tương lai?

---

## 14. Ghi Chú Cho Agent Khác

- Giữ NotebookLM source và prompt tách riêng.
- Không upload dữ liệu Zalo/Facebook riêng tư nếu chưa được duyệt rõ.
- Lưu cả local path và cloud ID.
- Ưu tiên manifest-first trước khi xây database lớn.

---

## 15. Đánh Giá Cuối

Nên duyệt storage layer cho second brain như một phần của early AI scope. Bắt đầu từ local manifest và curated NotebookLM pack, sau đó mới thêm Google Drive/database sync.
