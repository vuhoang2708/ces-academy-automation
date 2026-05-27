# BÁO CÁO TỔNG HỢP DỰ ÁN: CES Academy Automation Platform

**Ngày báo cáo:** 27/05/2026 | **Phiên bản:** 2.0 (Đầy đủ V10 → V14)

---

> **Cập nhật trạng thái repo hiện tại sau audit/implementation 27/05/2026:** Một số claim trong báo cáo gốc là lịch sử hoặc đã stale. V12 timestamp đã được sửa; V13 Zalo corrupt đã được thay bằng quarantine stub; `hub_server.py` chưa có trong repo hiện tại; AI analysis được đẩy lên P1 sớm dưới dạng sidecar cho V10-V14.

---

## I. LỊCH SỬ PHÁT TRIỂN ĐẦY ĐỦ (V10 → V14)

Dự án không bắt đầu từ V11 mà có nguồn gốc từ **V10 — CES Academy Web Capture**, và toàn bộ chuỗi phát triển có logic tiến hóa rõ ràng:

```
V10 (Web Viewer)
  └─ Playwright + CDP → Chụp 81 trang PDF từ CES Academy viewer
       │
       ▼ Nhu cầu mở rộng: SharePoint/Teams
V11 (SharePoint)
  └─ PyAutoGUI + img2pdf → Cào tài liệu Microsoft, tự nhận diện đáy trang
       │
       ▼ Nhu cầu mở rộng: App Desktop (Zalo)
V12 (Zalo Screenshot Pro)
  └─ PyAutoGUI + Pillow → Chụp chat Zalo, crop sạch, ghép PDF
       │
       ▼ Nhu cầu mở rộng: Tải file/ảnh gốc, không chỉ chụp màn hình
V13 (Media Downloader)
  └─ CDP (Facebook) + OpenCV (Zalo) → Tải media gốc từ FB Group & Zalo
       │
       ▼ Nhu cầu mở rộng: Tự động hóa hoàn toàn Zalo Desktop
V14 (Zalo Desktop - In Dev)
  └─ OpenCV template matching → Tìm và click nút download tự động
```

---

## II. KIẾN TRÚC TỔNG THỂ (3 LỚP)

```
┌─────────────────────────────────────────────────────────┐
│  THE AI BRAIN (Gemini 3)                                │
│  OCR, Tóm tắt, Nhận diện thực thể                      │
└────────────────────┬────────────────────────────────────┘
                     │ Upload Artifacts
┌────────────────────▼────────────────────────────────────┐
│  THE CLOUD PORTAL (Next.js / Vercel)                    │
│  Dashboard, Gallery, Version Management                 │
└────────────────────┬────────────────────────────────────┘
                     │ Download Launcher / Sync Data
┌────────────────────▼────────────────────────────────────┐
│  THE LOCAL ENGINE (Python Portable)                     │
│  V10 CES │ V11 SharePoint │ V12 Zalo │ V13 FB │ V14    │
└─────────────────────────────────────────────────────────┘
```

---

## III. PHÂN TÍCH CHI TIẾT TỪNG MODULE

### V10 — CES Academy Web Capture (`capture_antigravity.py`)

**Công nghệ:** Playwright async API + CDP qua port `9333`

**Chức năng:**
- Kết nối Chrome đang mở qua CDP (`http://localhost:9333`)
- Điều hướng đến URL viewer CES Academy cụ thể
- Chụp 81 trang bằng `ArrowRight` + `page.screenshot()`
- Ghép tất cả PNG thành PDF bằng `img2pdf`
- Output: `Lam_Chu_ANTIGRAVITY_30_Ngay.pdf`

**Vấn đề kỹ thuật:**
- Hardcode `TOTAL_PAGES = 81` và URL viewer cụ thể — không tái sử dụng được
- Output path hardcode sang `G:\My Drive\...` — chỉ chạy được trên máy có Google Drive mount
- Không có logic retry nếu trang load chậm (chỉ `asyncio.sleep(3)` cố định)
- Xóa toàn bộ ảnh cũ khi chạy lại — không có cơ chế resume

> Đây là module gốc, là lý do dự án tồn tại. Tên "CES Academy Automation" xuất phát từ đây.

---

### V11 — SharePoint PDF Extractor (`capture_v11_sharepoint.py`)

**Công nghệ:** PyAutoGUI + img2pdf

**Chức năng:**
- Chụp toàn màn hình theo từng trang
- Nhấn `PageDown` để chuyển trang
- Ghép PDF

**Điểm nổi bật từ lịch sử phát triển:**
- Phiên bản production có thêm **Computer Vision (Pillow ImageChops/ImageStat)** để tự nhận diện khi đã chạm đáy tài liệu
- Đã từng hỗ trợ kết nối CDP đa cổng (9222 và 9333)
- Đã có CSS Injection để ẩn thanh công cụ Microsoft (`.od-TopBar`, `.CommandBar`, `#O365_NavHeader_Shell`)
- Đã test thành công với tài liệu LPBank 11 trang

> **Khoảng cách giữa spec và code hiện tại:** Bản V11 trong repo chỉ là skeleton 33 dòng, thiếu hoàn toàn các tính năng nâng cao đã được mô tả trong tài liệu.

---

### V12 — Zalo Screenshot Pro (`capture_v12_zalo_pro.py`)

**Công nghệ:** PyAutoGUI + pygetwindow + Pillow + img2pdf

**Chức năng:**
- Tìm cửa sổ Zalo chính xác (lọc bỏ PDF viewer, Chrome)
- Click vào header để lấy focus an toàn
- Cuộn bằng phím `Down` × 18 lần mỗi trang
- Crop: left=34%, top=120px, right=width-10, bottom=height-125
- Ghép PDF với timestamp trong tên file

**Lịch sử debug quan trọng:**

| Vấn đề gặp phải | Giải pháp đã áp dụng |
|----------------|---------------------|
| Trang 2 và 3 trùng nhau | Chuyển từ `PageDown` sang `Down` × 18 |
| Click nhầm vào biểu tượng thả tim | Dịch điểm click sang 45% width |
| Script chụp nhầm file PDF đang mở | Thêm filter loại bỏ `.pdf`, `.png`, Chrome |
| Click vào header không cuộn được | Chuyển click sang 31% width (vùng chat) |
| Vẫn click nhầm link trong chat | Dịch click sang 40% width |
| Lỗi Permission Denied khi ghi PDF | Thêm timestamp vào tên file |

**Bug còn tồn tại:**
```python
# Dòng 53 — format sai (%M là phút, %D không tồn tại trong Python)
timestamp = datetime.now().strftime("%Y%M%D_%H%M%S")

# Đúng phải là:
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
```

---

### V13 — Facebook Media Downloader

**Công nghệ:** CDP/WebSocket + requests

**Phiên bản hiện tại:** V13.9 (Deep Scan Edition) — Production stable

**Kiến trúc lõi:**
- **CDP Engine:** Quản lý luồng WebSocket đồng bộ với ID matching
- **Dynamic Discovery Algorithm:** Truy vết bài viết qua text indicators ("Thích", "Bình luận") thay vì CSS class cố định
- **Indestructible Scroll:** `Input.dispatchKeyEvent(PageDown)` thay vì `window.scrollBy`
- **MIME Validation:** Kiểm tra `Content-Type` trước khi lưu file

**So sánh V13 gốc vs V17 (experimental):**

| Tiêu chí | V13 (gốc) | V17 (experimental) |
|----------|-----------|---------------------|
| Error handling | `except: pass` | `CDPError`, `CDPTimeout` riêng biệt |
| Timeout | Không có | 12s per call |
| Scroll validation | Không | Có (delta check) |
| Sanitize tên folder | Regex cơ bản | Regex + underscore normalization |
| Streaming download | Không | Có (`iter_content`) |
| Code quality | Compact, khó đọc | Clean, có type hints |

**Kết quả thực tế:** Thư mục `v13_fb_downloads/` chứa 11 bài viết đã được trích xuất thành công.

**File `v13_zalo_media_downloader.py`:** Bị corrupt (encoding lỗi), không đọc được.

**File `v13_template_extractor.py`:** Hardcode tọa độ pixel `(554, 411, 578, 435)` — sẽ sai nếu độ phân giải màn hình khác.

---

### V14 — Zalo Desktop Media Downloader (`zalo_media_v14.py`)

**Công nghệ:** PyAutoGUI + OpenCV + pygetwindow

**Trạng thái:** Early development — chỉ có diagnostic capture mode

**Lộ trình hoàn thiện:**
```
Bước 1: Diagnostic capture (✅ đã có)
Bước 2: OpenCV template matching để tìm nút "Ảnh/Video"
Bước 3: Click vào panel Media, scroll để load hết ảnh
Bước 4: Template match nút download từng ảnh
Bước 5: Xử lý Save As dialog tự động
```

---

### Launcher GUI (`launcher_gui.py`)

**Công nghệ:** Tkinter

**Vấn đề:**
- Hardcode đường dẫn Python portable và project dir
- `chrome.exe` gọi không có đường dẫn đầy đủ — phụ thuộc PATH
- Không có trạng thái "đang chạy" / "đã hoàn thành"
- Thiếu nút V14 Zalo Desktop

---

## IV. KIỂM KÊ ĐẦY ĐỦ CÁC FILE

| File | Vị trí | Trạng thái | Ghi chú |
|------|--------|------------|---------|
| `capture_antigravity.py` | Root | Functional | V10 — hardcode G: Drive path |
| `launcher_gui.py` | Root | Functional | Thiếu nút V14, hardcode paths |
| `capture_v11_sharepoint.py` | V11/ | Skeleton | Thiếu CV auto-stop, CSS injection |
| `capture_v12_zalo_pro.py` | V12/ | Functional (có bug) | Bug timestamp format dòng 53 |
| `v13_fb_media_downloader.py` | V13/ | Production | V13.7 (tên hàm), stable |
| `v13_fb_media_downloader_v17.py` | V13/ | Experimental | Code quality tốt hơn |
| `v13_zalo_media_downloader.py` | V13/ | **Corrupt** | Encoding lỗi, không đọc được |
| `v13_template_extractor.py` | V13/ | Functional | Hardcode tọa độ pixel |
| `zalo_media_v14.py` | V14/ | Diagnostic only | Chưa có CV matching |
| `MASTER_SPECIFICATION.md` | Root | Up to date | |
| `TECHNICAL_SPEC_UNIFIED_HUB.md` | Root | Up to date | |
| `TECHNICAL_SPEC_V13.md` | V13/ | Up to date | |
| `UAT_V13_FB_GUIDE.md` | V13/ | Up to date | |

---

## V. AUDIT TOÀN DIỆN — CÁC VẤN ĐỀ CỤ THỂ

### Bugs xác nhận (cần fix ngay)

**Bug 1 — Timestamp sai trong V12** (`capture_v12_zalo_pro.py:53`)
```python
# SAI:
timestamp = datetime.now().strftime("%Y%M%D_%H%M%S")
# ĐÚNG:
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
```

**Bug 2 — File V13 Zalo bị corrupt** (`v13_zalo_media_downloader.py`)
Encoding lỗi, cần restore từ git history hoặc viết lại.

**Bug 3 — V10 hardcode output path** (`capture_antigravity.py:7-8`)
```python
# Chỉ chạy được trên máy có Google Drive mount tại G:
OUTPUT_FOLDER = r"g:\My Drive\antigravity\ces-academy-automation\screenshots_high_res"
FINAL_PDF = r"g:\My Drive\antigravity\ces-academy-automation\Lam_Chu_ANTIGRAVITY_30_Ngay.pdf"
```

**Bug 4 — Launcher hardcode Python path** (`launcher_gui.py:8`)
```python
# Không portable sang máy khác:
executable = r"C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
```

**Bug 5 — V11 thiếu tính năng production**
File hiện tại chỉ là skeleton, thiếu Computer Vision auto-stop và CSS injection đã được mô tả trong tài liệu.

### Rủi ro kỹ thuật

| Rủi ro | Vị trí | Mức độ | Khuyến nghị |
|--------|--------|--------|-------------|
| `except: pass` nuốt lỗi im lặng | V13 dòng 131 | Cao | Log lỗi tối thiểu, đếm success/fail |
| Không có rate limiting | V13 scroll loop | Trung bình | Thêm `random.uniform(0.8, 1.5)` vào sleep |
| Không có dedup | V13 output folder | Trung bình | Kiểm tra folder tồn tại trước khi tạo |
| Không có checkpoint | Tất cả modules | Trung bình | Lưu trạng thái để resume khi crash |
| Hardcode tọa độ pixel | V13 template extractor | Thấp | Dùng tỉ lệ % thay vì pixel cứng |
| Không có logging framework | Tất cả modules | Thấp | Thay `print()` bằng `logging` |

### Rủi ro vận hành

- **Phụ thuộc Chrome profile thủ công:** Người dùng phải tự đăng nhập Facebook trên debug profile
- **Không có `requirements.txt`:** Không thể tái tạo môi trường trên máy mới
- **Hub Server chưa tồn tại:** `hub_server.py` được đề cập trong spec nhưng không có trong repo

---

## VI. HƯỚNG ĐỀ XUẤT PHÁT TRIỂN

### Sprint 0 — Fix bugs ngay (1-2 ngày)

1. Fix timestamp format trong V12 (`%Y%m%d_%H%M%S`)
2. Restore/rewrite `v13_zalo_media_downloader.py` (file corrupt)
3. Fix V10 output path dùng `os.path.join(SCRIPT_DIR, ...)`
4. Fix Launcher dùng relative path từ `__file__`

### Sprint 1 — Chuẩn hóa codebase (1 tuần)

5. Tạo `config.py` tập trung:
```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CDP_PORT = int(os.getenv("CDP_PORT", 9222))
OUTPUT_BASE = os.path.join(BASE_DIR, "downloads")
PYTHON_EXE = os.getenv("PYTHON_EXE", "python")
```

6. Thêm `requirements.txt` với pinned versions:
```
websockets==12.0
requests==2.31.0
pyautogui==0.9.54
opencv-python==4.9.0.80
img2pdf==0.5.1
pygetwindow==0.0.9
Pillow==10.3.0
playwright==1.44.0
```

7. Hợp nhất V13 + V17 thành bản stable duy nhất (lấy error handling của V17, giữ Dynamic Discovery của V13)
8. Khôi phục V11 đầy đủ tính năng (CV auto-stop + CSS injection)
9. Thêm dedup logic: kiểm tra folder tồn tại trước khi tạo, skip nếu đã có `content.txt`
10. Thêm summary report cuối mỗi run: tổng số bài, số ảnh tải thành công/thất bại

### Sprint 2 — Hoàn thiện V14 Zalo (2-3 tuần)

11. Implement OpenCV template matching cho Zalo download button
12. Xử lý Save As dialog tự động
13. Tích hợp V14 vào Launcher GUI

### Sprint 3 — Hub Server (2-3 tuần)

14. Xây dựng `hub_server.py` (Flask/FastAPI):
```python
@app.route("/api/launch/<module>", methods=["POST"])
def launch_module(module): ...

@app.route("/api/status", methods=["GET"])
def get_status(): ...

@app.route("/api/sync", methods=["POST"])
def sync_data(): ...
```

15. Kết nối với Next.js Portal (Phase 4 theo TECHNICAL_SPEC_UNIFIED_HUB.md)

### Sprint 4 — AI Integration (dài hạn)

16. Gemini API cho OCR ảnh Zalo/Facebook
17. Tóm tắt nội dung bài viết tự động
18. Phân loại sự kiện tự động (họp, thông báo, sự kiện...)
19. Cross-platform query: "Tóm tắt nội dung tuần này từ cả Facebook và Zalo"

### Roadmap tổng thể

| Thời gian | Sprint | Mục tiêu |
|-----------|--------|----------|
| Tháng 6/2026 | Sprint 0+1 | Fix bugs + Chuẩn hóa codebase |
| Tháng 7/2026 | Sprint 2 | Hoàn thiện V14 Zalo |
| Tháng 8/2026 | Sprint 3 | Hub Server + Next.js Portal Phase 4 |
| Tháng 9/2026 | Sprint 4 | Gemini AI integration |
| Tháng 10/2026 | Release | Unified Hub v1.0 |

---

## VII. ĐÁNH GIÁ TỔNG THỂ

| Tiêu chí | Điểm | Nhận xét |
|----------|------|----------|
| Tính năng cốt lõi (V13 FB) | 9/10 | Hoạt động production, có kết quả thực tế |
| Độ đầy đủ của bộ công cụ | 6/10 | V11 skeleton, V13 Zalo corrupt, V14 chưa xong |
| Chất lượng code | 5/10 | Bug timestamp, silent failures, hardcode paths |
| Tài liệu hóa | 8/10 | Tốt, nhưng spec vượt xa code thực tế |
| Khả năng portable | 3/10 | Nhiều hardcode paths, thiếu requirements.txt |
| Lịch sử phát triển | 9/10 | Export logs chi tiết, trace lại được mọi quyết định |
| Khả năng mở rộng | 5/10 | Thiếu config tập trung, thiếu Hub Server |
| **Tổng thể** | **6.4/10** | Nền tảng tốt, cần chuẩn hóa và hoàn thiện |

---

## VIII. KẾT LUẬN

Dự án có lịch sử phát triển rõ ràng từ V10 đến V14, mỗi version giải quyết một nhu cầu thực tế cụ thể. Điểm mạnh là CDP approach đúng hướng, Dynamic Discovery bền vững, và tài liệu hóa tốt hơn mức trung bình của dự án cá nhân.

Điểm yếu lớn nhất hiện tại là **khoảng cách giữa spec và code** (V11 thiếu tính năng, V13 Zalo corrupt), cộng với **hardcode paths** làm giảm khả năng portable.

**Ưu tiên ngay:** Fix 5 bugs đã xác nhận, thêm `requirements.txt`, hợp nhất V13+V17. Sau đó chuẩn hóa codebase trước khi phát triển thêm tính năng mới.

---

*Báo cáo được tổng hợp bởi Claude (Anthropic) dựa trên toàn bộ source code, tài liệu kỹ thuật và export logs của dự án.*
*Cập nhật: 27/05/2026*
