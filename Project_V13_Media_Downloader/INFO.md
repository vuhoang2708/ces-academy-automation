# PROJECT V13 - FACEBOOK MEDIA DOWNLOADER

## Hiện Trạng

- **V13 Facebook:** hardened script, cần live UAT với Chrome debug/Facebook tab.
- **V13 Zalo:** quarantined/unavailable vì source cũ corrupt/null bytes.
- **Output mặc định:** `downloads/v13_facebook/`.

## Tính Năng Chính Của V13 Facebook

- Dynamic discovery dựa trên text indicators như `Thích`, `Bình luận`.
- CDP/WebSocket client có timeout và lỗi rõ.
- Download media có MIME validation và streaming.
- Có `latest_run_summary.json` sau mỗi run.
- Có giới hạn qua env var:
  - `CES_V13_MAX_POSTS`
  - `CES_V13_MAX_MEDIA_PER_POST`
  - `CES_FORCE_DOWNLOAD`

## Lưu Ý Vận Hành

1. Mở Chrome bằng debug port trước khi chạy.
2. Đăng nhập Facebook trong cửa sổ Chrome debug.
3. Mở đúng Facebook Group/tab cần scrape.
4. Không commit folder output vì có thể chứa dữ liệu riêng tư.

---
*Cập nhật: 27/05/2026*
