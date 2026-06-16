from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_BASE = Path(os.getenv("CES_OUTPUT_BASE", BASE_DIR / "outputs")).resolve()
DOWNLOAD_BASE = Path(os.getenv("CES_DOWNLOAD_BASE", BASE_DIR / "downloads")).resolve()
ZALO_CAPTURES_DIR = Path(os.getenv("CES_ZALO_CAPTURES_DIR", BASE_DIR / "zalo_captures")).resolve()

FB_CDP_PORT = int(os.getenv("CES_FB_CDP_PORT", "9222"))
VIEWER_CDP_PORT = int(os.getenv("CES_VIEWER_CDP_PORT", "9333"))
FB_DEBUG_URL = os.getenv("CES_FB_DEBUG_URL", f"http://localhost:{FB_CDP_PORT}/json")
VIEWER_CDP_URL = os.getenv("CES_VIEWER_CDP_URL", f"http://localhost:{VIEWER_CDP_PORT}")

PYTHON_EXE = os.getenv("CES_PYTHON_EXE", sys.executable)
CHROME_EXE = os.getenv("CES_CHROME_EXE", "")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def module_output_dir(name: str) -> Path:
    return ensure_dir(OUTPUT_BASE / name)


def module_download_dir(name: str) -> Path:
    return ensure_dir(DOWNLOAD_BASE / name)


def find_chrome() -> str | None:
    if CHROME_EXE and Path(CHROME_EXE).exists():
        return CHROME_EXE

    from_path = shutil.which("chrome") or shutil.which("chrome.exe")
    if from_path:
        return from_path

    candidates = [
        Path(os.environ.get("PROGRAMFILES", "")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/Application/chrome.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None
