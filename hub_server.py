"""CES Academy Automation Hub Server — minimal local backend.

Endpoints:
  GET /health        — liveness check
  GET /modules       — module status from PROJECT_STATUS.md
  GET /artifacts     — recent manifest records from outputs_manifest.jsonl
  POST /run/<module> — NOT implemented; returns 501 with safety warning

Run:
    python hub_server.py [--port 8765]

Access:
    http://localhost:8765/health
    http://localhost:8765/modules
    http://localhost:8765/artifacts

IMPORTANT: Server binds to 127.0.0.1 only. Do NOT expose to network.
Desktop automation modules (V12, V14) are NOT runnable via this API.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_STATUS_FILE = BASE_DIR / "PROJECT_STATUS.md"
MANIFEST_FILE = BASE_DIR / "outputs_manifest.jsonl"

BIND_HOST = "127.0.0.1"

# Modules that must never be auto-run via API (desktop automation)
DESKTOP_AUTOMATION_MODULES = {"v11", "v12", "v14"}


def _parse_status_table() -> list[dict]:
    """Parse the module status table from PROJECT_STATUS.md."""
    if not PROJECT_STATUS_FILE.exists():
        return [{"error": "PROJECT_STATUS.md not found"}]

    text = PROJECT_STATUS_FILE.read_text(encoding="utf-8")
    rows: list[dict] = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("| Module") or stripped.startswith("|---|"):
            in_table = True
            continue
        if in_table:
            if not stripped.startswith("|"):
                break
            parts = [p.strip() for p in stripped.strip("|").split("|")]
            if len(parts) >= 2:
                rows.append({
                    "module": parts[0],
                    "status": parts[1],
                    "notes": parts[2] if len(parts) > 2 else "",
                })
    return rows


def _read_manifest(limit: int = 20) -> list[dict]:
    """Read last N records from outputs_manifest.jsonl."""
    if not MANIFEST_FILE.exists():
        return []
    lines = MANIFEST_FILE.read_text(encoding="utf-8").splitlines()
    records: list[dict] = []
    for line in reversed(lines[-limit:]):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return list(reversed(records))


def _json_response(handler: BaseHTTPRequestHandler, status: int, data: object) -> None:
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class HubHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:  # noqa: D102
        print(f"[hub] {self.address_string()} {fmt % args}")

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?")[0].rstrip("/")

        if path == "/health":
            _json_response(self, 200, {
                "status": "ok",
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "server": "CES Academy Hub",
                "note": "Local-only. Do not expose to network.",
            })

        elif path == "/modules":
            modules = _parse_status_table()
            _json_response(self, 200, {
                "source": str(PROJECT_STATUS_FILE),
                "retrieved_at": datetime.now().isoformat(timespec="seconds"),
                "modules": modules,
                "warning": "Status reflects PROJECT_STATUS.md — not live runtime state.",
            })

        elif path == "/artifacts":
            records = _read_manifest()
            _json_response(self, 200, {
                "source": str(MANIFEST_FILE),
                "retrieved_at": datetime.now().isoformat(timespec="seconds"),
                "count": len(records),
                "artifacts": records,
            })

        else:
            _json_response(self, 404, {"error": f"Not found: {path}"})

    def do_POST(self) -> None:  # noqa: N802
        path = self.path.split("?")[0].rstrip("/")

        # /run/<module> — intentionally not implemented
        if re.match(r"^/run/", path):
            module_name = path.split("/run/", 1)[-1].lower()
            if module_name in DESKTOP_AUTOMATION_MODULES:
                _json_response(self, 403, {
                    "error": "Desktop automation modules cannot be triggered via API.",
                    "module": module_name,
                    "reason": (
                        "V11/V12/V14 use PyAutoGUI and require a focused desktop window. "
                        "Run them manually from the launcher or CLI."
                    ),
                })
            else:
                _json_response(self, 501, {
                    "error": "Run API not implemented.",
                    "module": module_name,
                    "reason": (
                        "POST /run/<module> is reserved for future implementation. "
                        "All runs must be triggered manually until run logging and "
                        "confirmation guards are in place."
                    ),
                })
        else:
            _json_response(self, 404, {"error": f"Not found: {path}"})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CES Academy Hub Server (local only)")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on (default 8765).")
    return parser.parse_args()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    args = parse_args()
    server = HTTPServer((BIND_HOST, args.port), HubHandler)
    print(f"Hub server running at http://{BIND_HOST}:{args.port}/")
    print("Endpoints: /health  /modules  /artifacts")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
