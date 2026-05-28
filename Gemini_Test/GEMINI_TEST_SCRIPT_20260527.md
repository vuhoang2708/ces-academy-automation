# Kịch Bản Test Gemini: Cross-Version AI Sidecar

**Ngày:** 2026-05-27
**Mục tiêu:** Kiểm tra Gemini có tạo được AI sidecar nhiều góc độ cho artifact của V10-V14 hay không.
**Trạng thái:** Script test thủ công/bán tự động. Chưa gọi API trong repo.

---

## 1. Nguyên Tắc Test

- Không upload dữ liệu Zalo/Facebook riêng tư nếu chưa được duyệt rõ.
- Nếu dùng dữ liệu thật, chạy local/manual trước và kiểm tra kỹ output.
- Gemini phải tách rõ phần nguyên văn, phần tóm tắt và phần suy luận.
- Gemini không được claim đã phân tích toàn bộ nếu input chỉ là vài screenshot hoặc một phần PDF.

---

## 2. Input Chuẩn Bị

Mỗi test case nên có:

1. Artifact gốc: PDF, PNG folder, post folder hoặc media folder.
2. Context ngắn: module nào tạo ra, thời gian, mục tiêu capture.
3. Privacy level: `private`, `internal`, hoặc `shareable`.
4. Template output: `templates/ai_analysis_sidecar_template.md`.

---

## 3. Prompt Chính Cho Gemini

```text
Bạn là lớp AI Analysis cho dự án CES Academy Automation.

Hãy đọc artifact được cung cấp và tạo một AI sidecar theo template sau:
- Bóc tách nguyên văn những phần đọc được.
- Lập dàn ý chi tiết theo luồng nội dung.
- Viết tóm tắt ngắn và CTA nếu có.
- Phân tích ngữ điệu/cách tiếp cận của từng người hoặc từng nguồn.
- Rút key points, entities, action items, follow-up questions.
- Thêm các lens phù hợp: decision log, risks/blockers, opportunity map, content repurposing, knowledge graph tags, second-brain value.
- Ghi rõ source files, content range, confidence và limitations.
- Không suy diễn quá mức. Nếu không thấy dữ liệu, ghi là không thấy.
- Nếu dữ liệu riêng tư, thêm privacy note và không viết bản shareable public.

Output bằng tiếng Việt. Thuật ngữ chuyên môn có thể giữ tiếng Anh nhưng phải giải nghĩa ngắn bằng tiếng Việt ở lần xuất hiện đầu tiên.
```

---

## 4. Test Case V12 Zalo Capture

**Input:** `zalo_captures/page_001.png` đến `page_005.png` hoặc PDF tương ứng.
**Expected output:** `*_AI_ANALYSIS.md` có đủ:

- nguyên văn theo thứ tự thời gian;
- dàn ý chi tiết;
- short summary + CTA;
- tone theo từng người;
- action items;
- storage/second-brain status;
- limitations nói rõ chỉ đọc 5 ảnh capture.

**Pass criteria:**

- Không bịa thêm nội dung ngoài ảnh.
- Không bỏ qua CTA/follow-up.
- Không gọi output là public/shareable nếu chưa được duyệt.

---

## 5. Test Case V13 Facebook

**Input:** một folder post có `content.txt` và ảnh/media đi kèm.
**Expected output:**

- post digest;
- CTA nếu có;
- audience/context signal nếu nhìn thấy;
- media inventory;
- repurposing opportunities;
- tags cho second brain.

---

## 6. Test Case V10/V11 PDF

**Input:** một PDF tài liệu capture.
**Expected output:**

- outline theo chương/trang;
- key lessons;
- glossary;
- câu hỏi còn mở;
- action item nếu tài liệu có giao việc.

---

## 7. Scoring Rubric

| Tiêu chí | Pass |
|---|---|
| Grounding | Mọi ý quan trọng đều bám source |
| Coverage | Có đủ các section bắt buộc |
| Vietnamese quality | Tiếng Việt rõ, thuật ngữ tiếng Anh có giải nghĩa |
| Privacy | Có privacy note đúng mức |
| Actionability | Có action items/follow-up khi nội dung hỗ trợ |
| Limitations | Nói rõ phần chưa nhìn thấy/chưa xác minh |

---

## 8. Kết Quả Cần Lưu

Sau mỗi test, lưu:

- input artifact path;
- Gemini output file;
- pass/fail theo rubric;
- lỗi cần sửa trong prompt/template;
- link Google Drive/NotebookLM/database nếu đã sync.

---

## 9. Test Bổ Sung Sau UAT V10/V13

Hai plan đầu đã được chạy ở mức PARTIAL ngày 2026-05-27:

- V13 Facebook bị chặn vì thiếu Chrome debug `9222`.
- V10 CES bị chặn vì redirect về login.

Dùng kịch bản riêng để Gemini review phần UAT kỹ thuật trước khi phân tích nội dung:

```text
Gemini_Test/GEMINI_TEST_SCRIPT_20260527_V10_V13_PARTIAL_UAT.md
```

---

## 10. Browser UAT Cho Các Blocker Còn Mở

Nếu Gemini/agent có browser và user có thể đăng nhập CES/Facebook trong browser đó, dùng kịch bản:

```text
Gemini_Test/GEMINI_BROWSER_UAT_SCRIPT_20260528_OPEN_BLOCKERS.md
```

Kịch bản này tập trung vào:

- V10 CES live capture với session đã đăng nhập.
- V13 Facebook live downloader với tab Facebook trên CDP port `9222`.
- V14 browser-assisted calibration và Hub browser smoke test.
