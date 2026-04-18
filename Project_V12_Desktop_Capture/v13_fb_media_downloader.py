import json
import requests
import websockets
import os
import sys

# Cấu hình encoding cho Console Windows
sys.stdout.reconfigure(encoding='utf-8')

# --- CẤU HÌNH ---
DEBUG_URL = "http://localhost:9222/json"
OUTPUT_DIR = "v13_fb_downloads"

async def get_fb_media():
    try:
        resp = requests.get(DEBUG_URL).json()
        target_page = None
        for page in resp:
            if "facebook.com" in page.get("url", ""):
                target_page = page
                break
        
        if not target_page:
            print("❌ Không thấy trang Facebook đang mở trong Chrome/Edge (Port 9222)!")
            return

        ws_url = target_page.get("webSocketDebuggerUrl")
        async with websockets.connect(ws_url) as ws:
            # Script trích xuất ảnh và link file từ DOM Facebook
            js_script = """
            (function() {
                let media = [];
                // Tìm ảnh (thường nằm trong thẻ img với thuộc tính src đặc thù)
                document.querySelectorAll('img').forEach(img => {
                    if (img.src && img.src.includes('fbcdn.net')) {
                        media.append({type: 'image', url: img.src});
                    }
                });
                // Tìm link file (thường nằm trong các thẻ a chứa link download)
                document.querySelectorAll('a').forEach(a => {
                    if (a.href && a.href.includes('fbcdn.net')) {
                        media.append({type: 'file', url: a.href});
                    }
                });
                return media;
            })()
            """
            
            # Thực thi JS qua CDP
            cmd = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {"expression": js_script, "returnByValue": True}
            }
            await ws.send(json.dumps(cmd))
            result = await ws.recv()
            data = json.loads(result)
            
            items = data.get("result", {}).get("result", {}).get("value", [])
            print(f"✅ Đã tìm thấy {len(items)} Media items trên Facebook Group.")
            
            if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
            
            for i, item in enumerate(items):
                print(f"🔗 URL: {item['url'][:60]}...")
                # Lần lượt tải (Tùy chọn) hoặc chỉ liệt kê URLs cho user
                
    except Exception as e:
        print(f"❌ Lỗi CDP: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(get_fb_media())
