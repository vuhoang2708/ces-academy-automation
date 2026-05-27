import asyncio
import json
import os
import re
import sys
from pathlib import Path

import requests
import websockets

sys.path.append(str(Path(__file__).resolve().parents[1]))
from config import FB_DEBUG_URL, module_download_dir


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


OUTPUT_DIR = module_download_dir("v13_facebook")
MAX_POSTS = int(os.getenv("CES_V13_MAX_POSTS", "50"))
MAX_MEDIA_PER_POST = int(os.getenv("CES_V13_MAX_MEDIA_PER_POST", "5"))
FORCE_DOWNLOAD = os.getenv("CES_FORCE_DOWNLOAD", "0") == "1"


class CDPError(Exception):
    pass


class CDPTimeout(CDPError):
    pass


class CDPClient:
    def __init__(self) -> None:
        self._id = 1

    async def call(self, ws, method: str, params: dict | None = None, timeout: float = 12.0) -> dict:
        current_id = self._id
        self._id += 1
        await ws.send(json.dumps({"id": current_id, "method": method, "params": params or {}}))

        while True:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
            except asyncio.TimeoutError as exc:
                raise CDPTimeout(f"Timeout waiting for {method} (id={current_id})") from exc

            data = json.loads(raw)
            if data.get("id") != current_id:
                continue
            if "error" in data:
                message = data["error"].get("message", "Unknown CDP error")
                raise CDPError(f"{method} failed: {message}")
            return data.get("result", {})


def sanitize_folder_name(text: str, max_len: int = 48) -> str:
    clean = re.sub(r"[\\/*?:\"<>|]", "", text.replace("\n", " "))
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean[:max_len].strip(" .") or "post"


def smart_download(url: str, dest: Path) -> tuple[bool, str]:
    if dest.exists() and not FORCE_DOWNLOAD:
        return True, "skipped_existing"

    try:
        with requests.get(url, timeout=20, stream=True) as response:
            if response.status_code != 200:
                return False, f"http_{response.status_code}"

            content_type = response.headers.get("Content-Type", "")
            if content_type and not (
                content_type.startswith("image/")
                or content_type.startswith("video/")
                or "octet-stream" in content_type
            ):
                return False, f"unexpected_content_type:{content_type}"

            with open(dest, "wb") as file_obj:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file_obj.write(chunk)
        return True, "downloaded"
    except Exception as exc:
        return False, f"exception:{exc}"


async def force_scroll(ws, cdp: CDPClient, steps: int = 20) -> None:
    print(f"[*] Deep scan: cuộn {steps} lần để load thêm bài viết...")
    for index in range(steps):
        await cdp.call(
            ws,
            "Input.dispatchKeyEvent",
            {"type": "rawKeyDown", "windowsVirtualKeyCode": 34, "nativeVirtualKeyCode": 34},
        )
        await cdp.call(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "windowsVirtualKeyCode": 34})
        await asyncio.sleep(1.2)
        if (index + 1) % 5 == 0:
            print(f"  [+] Đã cuộn {index + 1}/{steps} lần")


def get_facebook_target() -> dict | None:
    try:
        tabs = requests.get(FB_DEBUG_URL, timeout=3).json()
    except Exception as exc:
        print(f"❌ Không kết nối được Chrome debug tại {FB_DEBUG_URL}: {exc}")
        return None

    return next((tab for tab in tabs if "facebook.com" in tab.get("url", "")), None)


async def run_v13_facebook() -> None:
    print("🚀 V13 Facebook Media Downloader - Dynamic Discovery + Hardened Download")
    cdp = CDPClient()
    summary = {
        "posts_found": 0,
        "posts_saved": 0,
        "media_attempted": 0,
        "media_downloaded": 0,
        "media_failed": 0,
        "media_skipped": 0,
        "output_dir": str(OUTPUT_DIR),
        "errors": [],
    }

    target = get_facebook_target()
    if not target:
        print("⚠️ Không có tab Facebook đang mở trong Chrome debug.")
        return

    try:
        async with websockets.connect(target["webSocketDebuggerUrl"]) as ws:
            print(f"[*] Đã nhận diện tab: {target.get('title')}")
            await cdp.call(ws, "Page.bringToFront")
            await force_scroll(ws, cdp)

            js_extract = """
            (function() {
                const posts = [];
                const indicators = Array.from(document.querySelectorAll('span, div')).filter(el =>
                    el.innerText === 'Thích' || el.innerText === 'Bình luận'
                );
                const foundArticles = new Set();
                indicators.forEach(el => {
                    const article = el.closest('div[role="article"]') ||
                        el.closest('div[data-testid="post_container"]') ||
                        (el.parentElement && el.parentElement.closest('div.x1y1aw1k'));
                    if (article) foundArticles.add(article);
                });

                Array.from(foundArticles).forEach(article => {
                    const message = article.querySelector('[data-ad-comet-preview="message"], [dir="auto"]');
                    const rawText = message ? message.innerText : article.innerText;
                    const lines = rawText.split('\\n').map(line => line.trim()).filter(line => line.length > 2);
                    const text = lines.slice(0, 15).join('\\n').trim();
                    const media = [];
                    article.querySelectorAll('img').forEach(img => {
                        if (img.src.includes('fbcdn.net') && img.width > 200) media.push(img.src);
                    });
                    if (text.length > 30 || media.length > 0) {
                        posts.push({ text, media: Array.from(new Set(media)) });
                    }
                });

                return {
                    count: posts.length,
                    items: posts,
                    debug: document.body.innerText.substring(0, 150).replace(/\\n/g, ' ')
                };
            })()
            """

            result = await cdp.call(ws, "Runtime.evaluate", {"expression": js_extract, "returnByValue": True})
            payload = result["result"]["value"]
            posts = payload["items"]
            summary["posts_found"] = payload["count"]
            print(f"✅ Phát hiện {payload['count']} bài viết/sự kiện.")

            if not posts:
                print(f"Preview nội dung: {payload.get('debug', '')}")
                return

            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            for index, post in enumerate(posts[:MAX_POSTS], start=1):
                folder_name = f"Post_{index:02d}_{sanitize_folder_name(post['text'])}"
                folder_path = OUTPUT_DIR / folder_name
                folder_path.mkdir(parents=True, exist_ok=True)

                content_path = folder_path / "content.txt"
                if not content_path.exists() or FORCE_DOWNLOAD:
                    content_path.write_text(post["text"], encoding="utf-8")
                summary["posts_saved"] += 1

                print(f"📥 Post {index}: {folder_name}")
                for media_index, url in enumerate(post["media"][:MAX_MEDIA_PER_POST], start=1):
                    summary["media_attempted"] += 1
                    image_path = folder_path / f"img_{media_index}.jpg"
                    ok, message = smart_download(url, image_path)
                    if ok and message == "downloaded":
                        summary["media_downloaded"] += 1
                    elif ok and message == "skipped_existing":
                        summary["media_skipped"] += 1
                    else:
                        summary["media_failed"] += 1
                        summary["errors"].append({"url": url, "reason": message})
                        print(f"  ⚠️ Media {media_index} lỗi: {message}")
    except Exception as exc:
        summary["errors"].append({"reason": str(exc)})
        print(f"❌ Lỗi V13 Facebook: {exc}")
    finally:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        summary_path = OUTPUT_DIR / "latest_run_summary.json"
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"📊 Summary: {summary_path}")
        print(
            "✅ Hoàn tất: "
            f"{summary['posts_saved']} posts, "
            f"{summary['media_downloaded']} media tải mới, "
            f"{summary['media_skipped']} skipped, "
            f"{summary['media_failed']} lỗi."
        )


if __name__ == "__main__":
    asyncio.run(run_v13_facebook())
