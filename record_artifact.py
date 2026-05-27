"""Manifest writer for CES Academy Automation artifacts.

Appends one JSONL record to outputs_manifest.jsonl for each artifact registered.
Does NOT upload to Google Drive or NotebookLM — local-first only.

Usage:
    python record_artifact.py --artifact <path> --version <label> --privacy <level>
    python record_artifact.py --artifact <path> --version TEST --privacy shareable --dry-run

Privacy levels: unknown | private | internal | shareable
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

MANIFEST_FILE = Path(__file__).resolve().parent / "outputs_manifest.jsonl"

VALID_PRIVACY = ("unknown", "private", "internal", "shareable")
VALID_STATUS = ("registered", "analyzed", "notebooklm_ready", "drive_uploaded", "archived")


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_file():
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                digest.update(chunk)
    elif path.is_dir():
        for child in sorted(path.rglob("*")):
            if child.is_file():
                rel = child.relative_to(path).as_posix()
                digest.update(rel.encode())
                with child.open("rb") as fh:
                    for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                        digest.update(chunk)
    return digest.hexdigest()


def build_record(args: argparse.Namespace, artifact_path: Path) -> dict:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    artifact_id = args.artifact_id or artifact_path.stem

    source_paths: list[str] = []
    artifact_paths: list[str] = []
    if artifact_path.is_file():
        source_paths = [str(artifact_path)]
        artifact_paths = [str(artifact_path)]
    elif artifact_path.is_dir():
        source_paths = [str(artifact_path)]
        artifact_paths = [str(f) for f in sorted(artifact_path.rglob("*")) if f.is_file()][:50]

    sha = sha256_path(artifact_path)

    return {
        "artifact_id": artifact_id,
        "version": args.version,
        "source_paths": source_paths,
        "artifact_paths": artifact_paths,
        "ai_markdown_path": args.ai_markdown or "",
        "ai_json_path": args.ai_json or "",
        "notebooklm_source_path": "",
        "notebooklm_prompt_path": "",
        "google_drive_url": "",
        "database_id": "",
        "privacy_classification": args.privacy,
        "created_at": now,
        "sha256": sha,
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else [],
        "status": args.status,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register an artifact in outputs_manifest.jsonl.")
    parser.add_argument("--artifact", required=True, help="Path to artifact file or folder.")
    parser.add_argument("--version", required=True, help="Version label (e.g. V12, V13, TEST).")
    parser.add_argument(
        "--privacy",
        choices=VALID_PRIVACY,
        default="unknown",
        help="Privacy classification.",
    )
    parser.add_argument("--artifact-id", default="", help="Optional stable artifact ID.")
    parser.add_argument("--ai-markdown", default="", help="Path to existing AI sidecar .md file.")
    parser.add_argument("--ai-json", default="", help="Path to existing AI sidecar .json file.")
    parser.add_argument("--tags", default="", help="Comma-separated tags.")
    parser.add_argument(
        "--status",
        choices=VALID_STATUS,
        default="registered",
        help="Artifact status.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the record without writing to manifest.",
    )
    return parser.parse_args()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    args = parse_args()
    artifact_path = Path(args.artifact).resolve()

    if not artifact_path.exists():
        print(f"ERROR: artifact path does not exist: {artifact_path}", file=sys.stderr)
        return 1

    record = build_record(args, artifact_path)
    record_line = json.dumps(record, ensure_ascii=False)

    if args.dry_run:
        print("DRY-RUN: record NOT written to manifest.")
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return 0

    if args.privacy == "private":
        print(
            "WARNING: privacy=private. Record will be written to outputs_manifest.jsonl "
            "which is in .gitignore. Do NOT commit this file if it contains private paths.",
            file=sys.stderr,
        )

    with MANIFEST_FILE.open("a", encoding="utf-8") as fh:
        fh.write(record_line + "\n")

    print(f"Registered: {record['artifact_id']} ({record['privacy_classification']})")
    print(f"Manifest: {MANIFEST_FILE}")
    print(f"SHA256: {record['sha256'][:16]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
