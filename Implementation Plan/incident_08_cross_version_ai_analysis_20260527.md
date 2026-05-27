# Incident 08: Đẩy lớp AI Analysis lên sớm và áp dụng cho V10-V14

**Ngày:** 2026-05-27
**Mức độ ưu tiên:** P1
**Trạng thái:** Hướng mới từ người dùng, đang ở bước lập kế hoạch để duyệt
**Phạm vi:** Artifact đầu ra của V10, V11, V12, V13, V14

---

## 1. Tóm tắt điều hành

Roadmap ban đầu đặt phần Gemini/OCR analysis ở sprint dài hạn. Người dùng đã đổi hướng: cần đưa AI lên sớm và áp dụng cho tất cả phiên bản, không chỉ để cuối dự án.

Thiết kế đề xuất là một lớp **AI sidecar** nhẹ: mỗi module vẫn tạo artifact gốc như PDF, PNG, media, hoặc text; sau đó hệ thống tạo thêm một file phân tích AI đi kèm artifact đó. Cách này giúp có giá trị ngay mà không phải chờ hoàn thiện Hub Server hoặc Next.js Portal.

Mục tiêu của AI không chỉ là “tóm tắt”, mà là phân tích nhiều lớp:

1. Bóc tách nguyên văn.
2. Lập dàn ý chi tiết.
3. Tóm tắt ngắn và CTA nếu có.
4. Phân tích ngữ điệu, cách tiếp cận của từng đối tượng.
5. Rút thêm các góc nhìn phục vụ second brain, content reuse, decision log, action items, và truy xuất về sau.

---

## 2. Giải thích thuật ngữ

- **AI sidecar**: file phân tích AI đi kèm artifact gốc, ví dụ `*_AI_ANALYSIS.md`.
- **OCR**: nhận diện chữ từ ảnh hoặc PDF.
- **Artifact**: file đầu ra của automation, ví dụ PDF, PNG, media, hoặc `content.txt`.
- **Entity extraction**: nhận diện thực thể như người, tổ chức, chủ đề, thời gian, việc cần làm.
- **CTA**: lời kêu gọi hành động hoặc bước tiếp theo nên làm.
- **Second brain**: kho tri thức cá nhân có thể tìm lại, hỏi lại, và kết nối về sau.
- **Manifest**: file mục lục metadata, dùng để lưu đường dẫn, tag, hash, trạng thái sync, link Google Drive, database ID.
- **Confidence**: mức độ chắc chắn của phân tích; có thể giữ thuật ngữ tiếng Anh vì đây là nhãn thường dùng trong AI output.
- **Hub/Portal**: lớp giao diện hoặc server điều phối trong tương lai, chưa cần có ngay để bắt đầu AI sidecar.

---

## 3. Triệu chứng người dùng nhìn thấy

Hiện tại các output capture đã hữu ích nhưng vẫn còn “thụ động”:

- V10/V11/V12 tạo PDF hoặc screenshot nhưng người dùng vẫn phải tự đọc.
- V13 Facebook tải được post/media nhưng chưa tự rút ý nghĩa, CTA, insight, hoặc action item.
- V14 khi hoàn thiện sẽ tải media Zalo, nhưng media đó vẫn cần OCR/caption/tóm tắt để dùng lại.

Người dùng muốn mỗi lần capture xong, hệ thống trả lời được nhiều lớp câu hỏi:

1. Nguyên văn nội dung là gì?
2. Nội dung đó có cấu trúc/dàn ý ra sao?
3. Ý chính ngắn gọn và CTA là gì?
4. Từng người hoặc từng nguồn đang dùng ngữ điệu/cách tiếp cận nào?
5. Có góc nhìn nào đáng lưu cho second brain, nội dung, học tập, hay hành động tiếp theo?

---

## 4. Hiện trạng kỹ thuật

Đã xác nhận:

- `MASTER_SPECIFICATION.md` đã có khái niệm AI Brain dùng Gemini/API cho OCR, tóm tắt và nhận diện thực thể.
- `TECHNICAL_SPEC_UNIFIED_HUB.md` có nhắc Gemini phân tích artifact đã scan.
- `BAO_CAO_TONG_HOP_DU_AN.md` đang để AI Integration ở Sprint 4.
- Đã có mẫu phân tích thủ công cho V12: `zalo_captures/Zalo_Chat_History_20260527_103203_AI_ANALYSIS.md`.
- Đã có template phân tích mới: `templates/ai_analysis_sidecar_template.md`.
- Đã có template NotebookLM source/prompt riêng:
  - `templates/notebooklm_source_template.md`
  - `templates/notebooklm_prompt_template.md`

Chưa xác minh:

- Có Gemini API key hoặc model mặc định trong môi trường hiện tại hay chưa.
- Có được phép gửi dữ liệu riêng tư từ Zalo/Facebook lên cloud AI API theo mặc định hay không.
- Output AI sidecar nên được commit vào Git hay giữ local-only vì có thể chứa dữ liệu riêng tư.
- NotebookLM nên nhận mọi capture hay chỉ nhận các source pack đã được chọn lọc.

---

## 5. Bằng chứng đã thu thập

Bằng chứng từ tài liệu:

```text
MASTER_SPECIFICATION.md:20-22
AI Brain: Gemini 3 Integration, OCR, summarization, entity/trend extraction.

TECHNICAL_SPEC_UNIFIED_HUB.md:21
AI Brain: Gemini 3 analyzes artifacts scanned by Hub.

BAO_CAO_TONG_HOP_DU_AN.md:319-324
Sprint 4: Gemini API for OCR, auto summary, event classification, cross-platform query.
```

Bằng chứng prototype:

```text
zalo_captures/Zalo_Chat_History_20260527_103203_AI_ANALYSIS.md
```

File prototype này chứng minh hướng phân tích đầu tiên: có source path, khoảng thời gian nhìn thấy, bóc tách nội dung, tóm tắt, insight, action item, câu hỏi follow-up và giới hạn phân tích. Template mới đã mở rộng thành multi-lens analysis, tức phân tích nhiều góc.

---

## 6. Nguyên nhân gốc

Nguyên nhân trực tiếp:

- AI ban đầu được đặt như một tính năng platform dài hạn, thay vì một bước hậu xử lý đơn giản có thể dùng ngay sau mỗi lần capture.

Nguyên nhân rộng hơn:

- Kiến trúc cũ đang tách “capture trước” và “intelligence sau”. Hướng mới của người dùng là “capture xong phải hiểu được ngay”.

---

## 7. Mẫu lỗi thiết kế tổng quát

Nền tảng hiện đang tối ưu cho việc thu thập artifact, nhưng chưa tối ưu cho việc tiêu thụ tri thức từ artifact đó.

Thiết kế bền hơn nên là:

1. Capture hoặc download artifact.
2. Tạo manifest máy đọc được.
3. Tạo AI sidecar analysis.
4. Lưu link/local path/database ID để Hub/Portal hoặc second brain có thể index về sau.

---

## 8. Hợp đồng AI chung cho V10-V14

Mỗi module nên tạo hoặc chấp nhận file:

```text
<artifact_base>_AI_ANALYSIS.md
```

Các phần tối thiểu:

1. Artifact nguồn: file hoặc folder gốc được đem đi phân tích.
2. Time/content range: khoảng thời gian, trang, post hoặc media đã phân tích.
3. Verbatim extraction: bóc tách nguyên văn.
4. Detailed outline: dàn ý chi tiết.
5. Short summary and CTA: tóm tắt ngắn và CTA.
6. Tone and approach by participant/source: ngữ điệu và cách tiếp cận theo từng người/nguồn.
7. Key points: ý chính.
8. Extracted entities: thực thể được nhận diện.
9. Action items: việc cần làm.
10. Additional analysis lenses: các góc phân tích thêm.
11. Suggested follow-up questions: câu hỏi follow-up.
12. Storage and second-brain links: link lưu trữ và second brain.
13. Độ chắc chắn và giới hạn: mức tin cậy của phân tích và phần chưa nhìn thấy/chưa xác minh.
14. Privacy/shareability note: ghi chú riêng tư/chia sẻ.

File máy đọc được có thể đi kèm:

```text
<artifact_base>_AI_ANALYSIS.json
```

Schema JSON đề xuất:

```json
{
  "sources": [],
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
  "limitations": []
}
```

---

## 9. Áp dụng theo từng version

| Version | Artifact | AI output sớm |
|---|---|---|
| V10 CES Web Capture | PDF từ CES Academy viewer | OCR, tóm tắt chương/bài, index chủ đề, bài học chính, câu hỏi còn mở |
| V11 SharePoint | PDF/screenshot từ SharePoint hoặc Teams | Tóm tắt tài liệu/cuộc họp, quyết định, owner, deadline |
| V12 Zalo Screenshot | Screenshot/PDF chat | Bóc tách chat, dàn ý, tone, relationship context, action item, follow-up |
| V13 Facebook | Post text/media đã tải | Digest bài viết, CTA, cụm chủ đề, phản ứng audience, gợi ý tái sử dụng nội dung |
| V14 Zalo Desktop Media | Media gốc sau khi tải | OCR/caption, mô tả media, nhận diện sự kiện/người, gom duplicate, tag tìm kiếm |

Các lens quan trọng theo loại nguồn:

- **V10/V11:** dàn ý, khái niệm, quyết định, nhiệm vụ, glossary, reusable lesson notes.
- **V12:** nguyên văn chat, tone/relationship, action items, follow-up questions.
- **V13:** post taxonomy, CTA, audience response, media inventory, repurposing opportunities.
- **V14:** media OCR/caption, event/person extraction, duplicate grouping, searchable tags.

---

## 10. Các lựa chọn triển khai

### Option A: Manual Sidecar First

Dùng screenshot/PDF hiện có và tạo Markdown analysis thủ công hoặc bằng agent.

Ưu điểm:

- Làm được ngay.
- Phù hợp để chốt format output.
- Không cần API key.

Nhược điểm:

- Chưa tự động.
- Phụ thuộc người/agent đọc ảnh và viết phân tích.

### Option B: Local CLI Analyzer

Tạo script như `analyze_artifact.py`, nhận đường dẫn file/folder và ghi ra `*_AI_ANALYSIS.md`.

Ưu điểm:

- Dùng được trước khi có Hub/Portal.
- Áp dụng cho tất cả version.
- Có thể chạy lại trên artifact cũ.

Nhược điểm:

- Cần quyết định model/API/OCR.
- Cần chính sách riêng tư trước khi gửi dữ liệu lên cloud.

### Option C: Hub-Integrated AI

Chờ `hub_server.py` và Portal để trigger phân tích tự động.

Ưu điểm:

- UX tốt nhất về lâu dài.
- Dễ quản lý trạng thái, link, database.

Nhược điểm:

- Quá muộn so với ưu tiên mới.
- Có nguy cơ xây platform trước khi output AI thật sự hữu ích.

Khuyến nghị: Option A ngay, Option B tiếp theo, Option C để sau.

---

## 11. Rủi ro và giảm thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| Dữ liệu chat/media riêng tư bị gửi ra cloud | Mặc định local-only; hỏi rõ trước khi dùng cloud AI API |
| AI hallucination, tức AI bịa hoặc suy diễn quá mức | Luôn có source path, trích đoạn nguyên văn, confidence và limitations |
| OCR đọc sai tiếng Việt | Dùng ảnh/PDF gốc cộng human review ở giai đoạn đầu |
| Quá nhiều format khác nhau giữa V10-V14 | Ép dùng chung một template sidecar |
| Analysis file bị commit nhầm lên Git | Thêm privacy note và cân nhắc `.gitignore` cho raw capture/sidecar riêng tư |
| NotebookLM bị nhồi raw data quá nhiễu | Tạo source pack sạch, không import raw dump mặc định |

---

## 12. Output mong đợi

Sau khi được duyệt:

- `templates/ai_analysis_sidecar_template.md`
- `zalo_captures/Zalo_Chat_History_20260527_103203_AI_ANALYSIS.md` làm ví dụ đã validate đầu tiên.
- `templates/notebooklm_source_template.md`
- `templates/notebooklm_prompt_template.md`
- Master plan cập nhật AI là P1 early-scope.
- Script tương lai tùy chọn: `analyze_artifact.py`.
- Manifest hoặc database record để lưu local path, Google Drive link, NotebookLM source/prompt, tag và privacy status.

---

## 13. Kế hoạch thực thi sau khi duyệt

1. Chốt template AI sidecar.
2. Áp template cho capture V12 hiện tại.
3. Thêm ghi chú theo từng loại artifact của V10-V14.
4. Thêm trường storage/second-brain cho Google Drive, NotebookLM và database.
5. Quyết định local-only hay dùng Gemini API.
6. Nếu duyệt Gemini, triển khai CLI analyzer nhận artifact path và xuất Markdown/JSON sidecar.
7. Thêm tiêu chí kiểm định chất lượng output AI.

---

## 14. Tiêu chí kiểm định

Một output AI chỉ đạt yêu cầu nếu:

- Ghi rõ source file.
- Ghi rõ phạm vi nội dung đã thấy: thời gian, trang, post, hoặc media.
- Có bóc tách nguyên văn, hoặc giải thích rõ vì sao không thể bóc tách nguyên văn.
- Có dàn ý chi tiết, tóm tắt ngắn/CTA, và phân tích tone/cách tiếp cận khi phù hợp.
- Tách nội dung quan sát được khỏi phần suy luận.
- Có confidence và limitations.
- Không claim đã phân tích toàn bộ nếu chỉ có screenshot/PDF một phần.
- Có action items khi nội dung hỗ trợ.
- Có trạng thái storage/second-brain, kể cả khi sync vẫn là `planned`.

---

## 15. Câu hỏi còn mở

1. Có dùng Gemini API ngay không, hay giai đoạn đầu giữ manual/agent-generated sidecar?
2. AI sidecar có được commit vào Git không, hay giữ local-only vì có dữ liệu riêng tư?
3. Ngôn ngữ output mặc định là tiếng Việt, tiếng Anh, hay theo ngôn ngữ nguồn?
4. Mỗi module chỉ ghi Markdown, hay ghi cả Markdown và JSON để Hub index về sau?
5. NotebookLM nhận mọi capture, hay chỉ nhận source pack đã được chọn lọc và cắt nhiễu?
6. Google Drive sync nên làm thủ công trước hay tự động ngay?

---

## 16. Ghi chú cho agent khác

- AI hiện là scope sớm, nhưng không được xây full Portal chỉ để bắt đầu AI.
- Hãy coi sidecar analysis là bước hậu xử lý sau mỗi artifact.
- Với dữ liệu riêng tư từ Zalo/Facebook, phải hỏi trước khi upload lên external API.
- Luôn ghi limitations nếu capture chỉ là một phần.
- Với NotebookLM, giữ source file và prompt file tách riêng: source là nội dung sạch để import, prompt là instruction yêu cầu NotebookLM tạo output.
- Thuật ngữ chuyên môn có thể giữ tiếng Anh, nhưng phải giải nghĩa bằng tiếng Việt có dấu ở phần thuật ngữ hoặc lần xuất hiện đầu tiên.

---

## 17. Đánh giá cuối

Nên duyệt việc đưa AI lên sớm dưới dạng cross-version sidecar layer. Hướng này tạo giá trị ngay, vẫn giữ an toàn vì chưa phụ thuộc vào Hub Server hoặc Cloud Portal, và đặt nền cho second brain trong tương lai.
