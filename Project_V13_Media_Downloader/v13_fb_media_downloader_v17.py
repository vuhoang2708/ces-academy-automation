import asyncio
import json
import os
import re
import sys
import time

import requests
import websockets

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "v13_fb_downloads_v17")
DEBUG_URL = "http://localhost:9222/json"


class CDPError(Exception):
    pass


class CDPTimeout(CDPError):
    pass


class CDPClient:
    def __init__(self):
        self._id_counter = 1

    async def call(self, ws, method, params=None, timeout=12):
        current_id = self._id_counter
        self._id_counter += 1
        await ws.send(
            json.dumps(
                {
                    "id": current_id,
                    "method": method,
                    "params": params or {},
                }
            )
        )

        deadline = time.time() + timeout
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise CDPTimeout(f"Timeout waiting for {method} (id={current_id})")

            try:
                message = await asyncio.wait_for(ws.recv(), timeout=remaining)
            except asyncio.TimeoutError as exc:
                raise CDPTimeout(f"Timeout waiting for {method} (id={current_id})") from exc
            except websockets.exceptions.ConnectionClosed as exc:
                raise CDPError("WebSocket connection closed unexpectedly.") from exc

            data = json.loads(message)
            if data.get("id") != current_id:
                continue
            if "error" in data:
                raise CDPError(f"{method} failed: {data['error'].get('message')}")
            return data.get("result", {})


def sanitize_folder_name(text, max_len=48):
    clean_text = re.sub(r'[\\/*?:"<>|]', "", text)
    clean_text = re.sub(r"\s+", "_", clean_text.strip())
    clean_text = clean_text[:max_len].strip("_")
    return clean_text or f"post_{int(time.time())}"


async def eval_value(ws, cdp, expression, timeout=12):
    result = await cdp.call(
        ws,
        "Runtime.evaluate",
        {
            "expression": expression,
            "returnByValue": True,
        },
        timeout=timeout,
    )
    return result["result"]["value"]


async def collect_page_state(ws, cdp):
    return await eval_value(
        ws,
        cdp,
        """
        (() => {
            const scrollRoot = document.scrollingElement || document.documentElement || document.body;
            const articles = document.querySelectorAll('div[role="article"]').length;
            const preview = (document.body?.innerText || '').slice(0, 160).replace(/\\n/g, ' ');
            return {
                articleCount: articles,
                scrollY: window.scrollY || 0,
                scrollHeight: scrollRoot ? scrollRoot.scrollHeight : 0,
                viewportHeight: window.innerHeight || 0,
                preview: preview
            };
        })()
        """,
    )


async def js_scroll_feed(ws, cdp):
    return await eval_value(
        ws,
        cdp,
        """
        (() => {
            const candidates = Array.from(document.querySelectorAll('div, main, section, body, html'));
            let best = null;
            for (const el of candidates) {
                const style = window.getComputedStyle(el);
                const canScroll = el.scrollHeight > el.clientHeight + 100;
                const visible = el.clientHeight > 200 && el.clientWidth > 200;
                const overflowOk = /(auto|scroll)/.test(style.overflowY || '');
                if (!canScroll || !visible) continue;
                if (!best || el.scrollHeight > best.scrollHeight || overflowOk) {
                    best = el;
                }
            }

            const target = best || document.scrollingElement || document.documentElement || document.body;
            const before = target.scrollTop || window.scrollY || 0;
            const amount = Math.max(700, Math.floor((target.clientHeight || window.innerHeight || 800) * 0.9));

            if (target === document.body || target === document.documentElement || target === document.scrollingElement) {
                window.scrollBy(0, amount);
            } else {
                target.scrollTop = before + amount;
            }

            const after = target.scrollTop || window.scrollY || 0;
            return {
                tag: target.tagName,
                delta: after - before,
                before: before,
                after: after
            };
        })()
        """,
    )


async def dispatch_page_down(ws, cdp):
    for event_type in ("keyDown", "keyUp"):
        await cdp.call(
            ws,
            "Input.dispatchKeyEvent",
            {
                "type": event_type,
                "windowsVirtualKeyCode": 34,
                "nativeVirtualKeyCode": 34,
                "code": "PageDown",
                "key": "PageDown",
            },
        )


async def validate_and_scroll(ws, cdp, steps=4):
    print("[*] Checking whether the Facebook feed can actually scroll...")
    before = await collect_page_state(ws, cdp)
    viewport = await eval_value(
        ws,
        cdp,
        "({x: Math.floor(window.innerWidth / 2), y: Math.floor(window.innerHeight / 2)})",
    )

    deltas = []
    for _ in range(steps):
        deltas.append(await js_scroll_feed(ws, cdp))
        await cdp.call(
            ws,
            "Input.dispatchMouseEvent",
            {
                "type": "mouseWheel",
                "x": viewport["x"],
                "y": viewport["y"],
                "deltaX": 0,
                "deltaY": 1000,
            },
        )
        await asyncio.sleep(1.0)

    after_wheel = await collect_page_state(ws, cdp)
    article_delta = after_wheel["articleCount"] - before["articleCount"]
    height_delta = after_wheel["scrollHeight"] - before["scrollHeight"]
    scroll_delta = after_wheel["scrollY"] - before["scrollY"]
    js_delta = max((item.get("delta", 0) for item in deltas), default=0)

    if article_delta > 0 or height_delta > 0 or scroll_delta > 0 or js_delta > 0:
        print(
            f"[*] Feed reacted to wheel: articleDelta={article_delta}, "
            f"heightDelta={height_delta}, scrollYDelta={scroll_delta}, jsDelta={js_delta}"
        )
        return after_wheel

    print("[*] Wheel was not enough. Falling back to PageDown...")
    for _ in range(3):
        await dispatch_page_down(ws, cdp)
        await asyncio.sleep(1.0)

    after_key = await collect_page_state(ws, cdp)
    article_delta = after_key["articleCount"] - before["articleCount"]
    height_delta = after_key["scrollHeight"] - before["scrollHeight"]
    scroll_delta = after_key["scrollY"] - before["scrollY"]
    print(
        f"[*] Scroll diagnostics: articleDelta={article_delta}, "
        f"heightDelta={height_delta}, scrollYDelta={scroll_delta}"
    )
    if article_delta <= 0 and height_delta <= 0 and scroll_delta <= 0:
        print(f"[*] Page preview: {after_key['preview']}")
    return after_key


def smart_download(url, dest):
    try:
        with requests.get(url, timeout=15, stream=True) as response:
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}"

            content_type = response.headers.get("Content-Type", "")
            if "image" not in content_type and "octet-stream" not in content_type:
                return False, f"MIME {content_type}"

            with open(dest, "wb") as file_obj:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file_obj.write(chunk)
        return True, "OK"
    except Exception as exc:
        return False, str(exc)


async def run():
    print("[*] Starting experimental Facebook downloader clone...")
    print(f"[*] Output directory: {OUTPUT_DIR}")
    cdp = CDPClient()

    response = requests.get(DEBUG_URL, timeout=10).json()
    target = next((item for item in response if "facebook.com" in item.get("url", "")), None)
    if not target:
        raise CDPError("No Facebook tab found on debug port 9222.")

    async with websockets.connect(target["webSocketDebuggerUrl"]) as ws:
        print(f"[*] Connected to tab: {target.get('title')}")
        await cdp.call(ws, "Page.bringToFront")
        state = await validate_and_scroll(ws, cdp)

        print("[*] Extracting article snapshots...")
        payload = await eval_value(
            ws,
            cdp,
            """
            (() => {
                const posts = [];
                document.querySelectorAll('div[role="article"]').forEach((article) => {
                    const msg = article.querySelector('[data-ad-comet-preview="message"]');
                    const text = (msg ? msg.innerText : article.innerText || '').trim();
                    const lines = text.split('\\n').map(line => line.trim()).filter(line => line.length > 2);
                    const finalText = lines.slice(0, 20).join('\\n').trim();

                    const images = [];
                    article.querySelectorAll('img').forEach((img) => {
                        if (img.src && img.src.includes('fbcdn.net') && img.width > 180) {
                            images.push(img.src);
                        }
                    });

                    if (finalText.length > 40 || images.length > 0) {
                        posts.push({
                            text: finalText,
                            media: [...new Set(images)]
                        });
                    }
                });
                return {
                    items: posts,
                    articleCount: document.querySelectorAll('div[role="article"]').length
                };
            })()
            """,
        )

        posts = payload["items"]
        print(f"[*] Found {len(posts)} candidate posts from {payload['articleCount']} article nodes.")
        if not posts:
            print(
                f"[*] Diagnostics: articleCount={state['articleCount']}, "
                f"scrollHeight={state['scrollHeight']}, preview={state['preview']}"
            )
            return

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        for index, post in enumerate(posts[:10], start=1):
            folder_name = f"Post_{index:02d}_{sanitize_folder_name(post['text'])}"
            folder_path = os.path.join(OUTPUT_DIR, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            with open(os.path.join(folder_path, "content.txt"), "w", encoding="utf-8") as file_obj:
                file_obj.write(post["text"])

            print(f"[*] Saved post {index}: {folder_name}")
            for image_index, url in enumerate(post["media"][:5], start=1):
                image_path = os.path.join(folder_path, f"image_{image_index}.jpg")
                ok, message = smart_download(url, image_path)
                if not ok:
                    print(f"    [!] Image {image_index} skipped: {message}")

        print(f"[+] Finished. Results are in: {OUTPUT_DIR}")


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as exc:
        print(f"[!] Fatal error: {exc}")
