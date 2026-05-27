# V11 SharePoint Capture — Module Info

**Status:** Basic/Skeleton — NOT production-ready
**Decision date:** 2026-05-27
**Decision:** Hướng A — giữ là basic screenshot extractor, docs đồng bộ với code thật.

---

## Tính năng hiện có

- Chụp toàn màn hình N lần liên tiếp (mặc định 5 trang).
- Nhấn PageDown giữa các lần chụp để cuộn trang.
- Ghép ảnh thành PDF bằng `img2pdf`.

## Tính năng CHƯA có (không được claim)

| Tính năng | Trạng thái |
|---|---|
| CV auto-stop (phát hiện trang trùng/cuối) | Chưa có |
| CSS injection / ẩn toolbar Microsoft | Chưa có |
| CDP / browser automation | Chưa có |
| Config.py integration | Chưa có |
| Output vào `outputs/v11_sharepoint/` | Chưa có |
| Run summary JSON | Chưa có |
| Duplicate detection | Chưa có |

## Điều kiện UAT tối thiểu

Để chạy thủ công:
1. Mở tài liệu SharePoint trong trình duyệt hoặc SharePoint Desktop.
2. Đảm bảo cửa sổ đang focus và hiển thị đầy màn hình.
3. Chạy script — script sẽ chụp `PAGES_TO_CAPTURE` trang.
4. Kiểm tra output trong `v11_captures/` và file PDF.

**Không có UAT tự động.** Kết quả phụ thuộc vào trạng thái cửa sổ lúc chạy.

## Hướng nâng cấp (nếu V11 trở thành ưu tiên)

Xem `Implementation Plan/Agent Handoff/remaining_03_v11_sharepoint_decision_20260527.md`
mục 6 (Hướng C: rebuild production) để biết thiết kế tối thiểu cần có.
