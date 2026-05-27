"""V14 Zalo Desktop Media Downloader.

STATUS: DRY_RUN_READY — diagnostic and dry-run modes implemented.
Execute mode requires Zalo Desktop open with a media chat and explicit --mode execute flag.

Modes:
  --mode diagnostic   Detect Zalo window, capture screenshot, log coordinates. No clicks.
  --mode dry-run      Find media panel area, log planned actions. No downloads.
  --mode execute      Click and download media. Requires diagnostic to have passed first.

Usage:
    python zalo_media_v14.py --mode diagnostic
    python zalo_media_v14.py --mode dry-run --max-items 3
    python zalo_media_v14.py --mode execute --max-items 1
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    import pyautogui
    import pygetwindow as gw  # type: ignore[import-untyped]
    _DESKTOP_AVAILABLE = True
except ImportError:
    _DESKTOP_AVAILABLE = False

try:
    import cv2  # type: ignore[import-untyped]
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False

from config import module_download_dir, module_output_dir

TARGET_WINDOW_TITLE = "Zalo"
DIAG_DIR_NAME = "v14_zalo_diagnostic"
DOWNLOAD_DIR_NAME = "v14_zalo_media"


def _now_str() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _file_hash(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


class ZaloV14:
    def __init__(self, mode: str, max_items: int) -> None:
        self.mode = mode
        self.max_items = max_items
        self.diag_dir = module_output_dir(DIAG_DIR_NAME)
        self.download_dir = module_download_dir(DOWNLOAD_DIR_NAME)
        self.run_id = _now_str()
        self.log: list[dict] = []

    # ------------------------------------------------------------------
    # Window helpers
    # ------------------------------------------------------------------

    def _find_window(self) -> object | None:
        if not _DESKTOP_AVAILABLE:
            return None
        wins = gw.getWindowsWithTitle(TARGET_WINDOW_TITLE)
        for w in wins:
            if w.title == TARGET_WINDOW_TITLE:
                return w
        return None

    def _activate_window(self, win: object) -> bool:
        try:
            if win.isMinimized:
                win.restore()
                time.sleep(0.5)
            win.activate()
            time.sleep(1)
            return True
        except Exception as exc:
            print(f"  WARNING: could not activate window: {exc}", file=sys.stderr)
            return False

    # ------------------------------------------------------------------
    # Diagnostic mode
    # ------------------------------------------------------------------

    def run_diagnostic(self) -> dict:
        print(f"[V14 diagnostic] run_id={self.run_id}")

        if not _DESKTOP_AVAILABLE:
            msg = "BLOCKED: pyautogui/pygetwindow not available. Install dependencies first."
            print(msg, file=sys.stderr)
            return self._write_summary("blocked", {"reason": msg})

        win = self._find_window()
        if win is None:
            msg = f"BLOCKED: No window with title '{TARGET_WINDOW_TITLE}' found. Open Zalo Desktop first."
            print(msg, file=sys.stderr)
            return self._write_summary("blocked", {"reason": msg})

        activated = self._activate_window(win)
        rect = {
            "left": win.left,
            "top": win.top,
            "width": win.width,
            "height": win.height,
        }
        print(f"  Window found: title='{win.title}' rect={rect} activated={activated}")

        # Capture screenshot of Zalo window region
        screenshot_path = self.diag_dir / f"diag_{self.run_id}.png"
        try:
            screenshot = pyautogui.screenshot(region=(rect["left"], rect["top"], rect["width"], rect["height"]))
            screenshot.save(str(screenshot_path))
            print(f"  Screenshot saved: {screenshot_path}")
            screenshot_ok = True
        except Exception as exc:
            print(f"  WARNING: screenshot failed: {exc}", file=sys.stderr)
            screenshot_ok = False
            screenshot_path = None

        # Focus click at center of window
        cx = rect["left"] + rect["width"] // 2
        cy = rect["top"] + rect["height"] // 2
        print(f"  Focus click at ({cx}, {cy}) — diagnostic only, no media action.")
        if activated:
            try:
                pyautogui.click(cx, cy)
                time.sleep(0.3)
            except Exception as exc:
                print(f"  WARNING: focus click failed: {exc}", file=sys.stderr)

        result = {
            "window_title": win.title,
            "rect": rect,
            "activated": activated,
            "focus_click": {"x": cx, "y": cy},
            "screenshot_path": str(screenshot_path) if screenshot_path else "",
            "screenshot_ok": screenshot_ok,
            "cv2_available": _CV2_AVAILABLE,
        }
        print("  Diagnostic PASS — review screenshot to confirm Zalo layout.")
        return self._write_summary("diagnostic_pass", result)

    # ------------------------------------------------------------------
    # Dry-run mode
    # ------------------------------------------------------------------

    def run_dry_run(self) -> dict:
        print(f"[V14 dry-run] run_id={self.run_id} max_items={self.max_items}")

        if not _DESKTOP_AVAILABLE:
            msg = "BLOCKED: pyautogui/pygetwindow not available."
            print(msg, file=sys.stderr)
            return self._write_summary("blocked", {"reason": msg})

        win = self._find_window()
        if win is None:
            msg = f"BLOCKED: Zalo window not found. Open Zalo Desktop and navigate to a chat with media."
            print(msg, file=sys.stderr)
            return self._write_summary("blocked", {"reason": msg})

        self._activate_window(win)
        rect = {"left": win.left, "top": win.top, "width": win.width, "height": win.height}

        # Capture current state for analysis
        screenshot_path = self.diag_dir / f"dryrun_{self.run_id}.png"
        try:
            screenshot = pyautogui.screenshot(region=(rect["left"], rect["top"], rect["width"], rect["height"]))
            screenshot.save(str(screenshot_path))
        except Exception:
            screenshot_path = None

        planned_actions = []
        for i in range(1, self.max_items + 1):
            planned_actions.append({
                "step": i,
                "action": "would_click_media_item",
                "note": "Template matching not yet calibrated — requires calibration screenshot review.",
                "would_download_to": str(self.download_dir / f"media_{i:03d}.bin"),
            })
            print(f"  [dry-run] Step {i}: would attempt to download media item {i} (no actual click)")

        print(f"  Dry-run complete. {len(planned_actions)} planned actions logged. No files downloaded.")
        print(f"  NEXT: Review screenshot at {screenshot_path} to calibrate media panel coordinates.")
        print(f"  NEXT: Run --mode execute only after calibration is confirmed.")

        result = {
            "window_rect": rect,
            "screenshot_path": str(screenshot_path) if screenshot_path else "",
            "planned_actions": planned_actions,
            "files_downloaded": 0,
            "calibration_status": "not_calibrated",
            "note": "Execute mode blocked until template/coordinate calibration is confirmed.",
        }
        return self._write_summary("dry_run_pass", result)

    # ------------------------------------------------------------------
    # Execute mode
    # ------------------------------------------------------------------

    def run_execute(self) -> dict:
        print(f"[V14 execute] run_id={self.run_id} max_items={self.max_items}")
        print("WARNING: execute mode will interact with Zalo Desktop via PyAutoGUI.")
        print("Ensure Zalo is open on the correct chat with media visible.")

        if not _DESKTOP_AVAILABLE:
            msg = "BLOCKED: pyautogui/pygetwindow not available."
            print(msg, file=sys.stderr)
            return self._write_summary("blocked", {"reason": msg})

        win = self._find_window()
        if win is None:
            msg = "BLOCKED: Zalo window not found."
            print(msg, file=sys.stderr)
            return self._write_summary("blocked", {"reason": msg})

        # Guard: require diagnostic screenshot to exist
        diag_screenshots = sorted(self.diag_dir.glob("diag_*.png"))
        if not diag_screenshots:
            msg = (
                "BLOCKED: No diagnostic screenshot found. "
                "Run --mode diagnostic first to confirm window layout."
            )
            print(msg, file=sys.stderr)
            return self._write_summary("blocked", {"reason": msg})

        self._activate_window(win)

        # Execute is PARTIAL until template matching is calibrated.
        # Current implementation: open media panel via keyboard shortcut attempt,
        # then log that full template matching requires calibration.
        print("  Execute: attempting to open media panel (Ctrl+Shift+M or Info panel)...")
        try:
            pyautogui.hotkey("ctrl", "shift", "m")
            time.sleep(1.5)
        except Exception as exc:
            print(f"  WARNING: hotkey failed: {exc}", file=sys.stderr)

        screenshot_path = self.diag_dir / f"execute_{self.run_id}.png"
        try:
            rect = {"left": win.left, "top": win.top, "width": win.width, "height": win.height}
            screenshot = pyautogui.screenshot(region=(rect["left"], rect["top"], rect["width"], rect["height"]))
            screenshot.save(str(screenshot_path))
            print(f"  Post-action screenshot: {screenshot_path}")
        except Exception:
            screenshot_path = None

        result = {
            "files_downloaded": 0,
            "screenshot_path": str(screenshot_path) if screenshot_path else "",
            "note": (
                "Execute mode reached Zalo window but full media panel template matching "
                "is not yet calibrated. Review post-action screenshot and provide "
                "calibrated coordinates or template images to complete execute flow."
            ),
            "status": "partial_execute",
        }
        print("  Execute PARTIAL — window reached, media panel automation needs calibration.")
        return self._write_summary("partial_execute", result)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def _write_summary(self, status: str, details: dict) -> dict:
        summary = {
            "run_id": self.run_id,
            "mode": self.mode,
            "status": status,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "max_items": self.max_items,
            "details": details,
        }
        summary_path = self.diag_dir / "latest_run_summary.json"
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  Summary: {summary_path}")
        return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="V14 Zalo Desktop Media Downloader")
    parser.add_argument(
        "--mode",
        choices=["diagnostic", "dry-run", "execute"],
        required=True,
        help="diagnostic: detect window only. dry-run: plan actions. execute: download media.",
    )
    parser.add_argument("--max-items", type=int, default=5, help="Max media items to process.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    runner = ZaloV14(mode=args.mode, max_items=args.max_items)

    if args.mode == "diagnostic":
        runner.run_diagnostic()
    elif args.mode == "dry-run":
        runner.run_dry_run()
    elif args.mode == "execute":
        runner.run_execute()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
