from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parent))


try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


TEXT_SUFFIXES = {
    ".txt",
    ".md",
    ".markdown",
    ".json",
    ".jsonl",
    ".csv",
    ".tsv",
    ".log",
}
IGNORED_ANALYSIS_SUFFIXES = ("_AI_ANALYSIS.md", "_AI_ANALYSIS.json")
MAX_TEXT_CHARS = 12000


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_source_files(input_path: Path, max_files: int) -> list[Path]:
    if input_path.is_file():
        return [input_path]

    files: list[Path] = []
    for path in sorted(input_path.rglob("*")):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        if path.name.endswith(IGNORED_ANALYSIS_SUFFIXES):
            continue
        files.append(path)
        if len(files) >= max_files:
            break
    return files


def aggregate_hash(input_path: Path, files: list[Path]) -> str:
    if input_path.is_file():
        return sha256_file(input_path)

    digest = hashlib.sha256()
    for file_path in files:
        relative = file_path.relative_to(input_path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(sha256_file(file_path).encode("utf-8"))
    return digest.hexdigest()


def read_text_sample(path: Path, remaining_chars: int) -> str:
    if path.suffix.lower() not in TEXT_SUFFIXES or remaining_chars <= 0:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff")[:remaining_chars]
    except Exception:
        return ""


def collect_text(files: list[Path], root: Path) -> tuple[str, list[dict[str, str]]]:
    parts: list[str] = []
    snippets: list[dict[str, str]] = []
    remaining = MAX_TEXT_CHARS

    for file_path in files:
        sample = read_text_sample(file_path, remaining)
        if not sample:
            continue
        label = file_path.name if root.is_file() else file_path.relative_to(root).as_posix()
        parts.append(f"--- {label} ---\n{sample.strip()}")
        snippets.append({"source": str(file_path), "text": sample.strip()})
        remaining -= len(sample)
        if remaining <= 0:
            break

    return "\n\n".join(parts).strip(), snippets


def compact_lines(text: str, limit: int = 8) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[:limit]


def detect_cta(text: str) -> str:
    if not text:
        return "Không thấy CTA trực tiếp trong phần text đọc được."

    patterns = [
        r"(?im)^.*\bCTA\b.*$",
        r"(?im)^.*follow up.*$",
        r"(?im)^.*next step.*$",
        r"(?im)^.*vui lòng.*$",
        r"(?im)^.*hãy .*$",
        r"(?im)^.*đăng ký.*$",
        r"(?im)^.*liên hệ.*$",
        r"(?im)^.*mong .*phản hồi.*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()
    return "Không thấy CTA trực tiếp trong phần text đọc được."


def detect_dates(text: str) -> list[str]:
    patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{1,2}:\d{2}\b",
    ]
    found: list[str] = []
    for pattern in patterns:
        found.extend(re.findall(pattern, text))
    return sorted(set(found))[:20]


def table_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def source_rows(files: list[Path], root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for file_path in files:
        label = file_path.name if root.is_file() else file_path.relative_to(root).as_posix()
        try:
            size = file_path.stat().st_size
        except OSError:
            size = 0
        rows.append(
            {
                "path": str(file_path),
                "label": label,
                "type": file_path.suffix.lower().lstrip(".") or "file",
                "size_bytes": size,
                "sha256": sha256_file(file_path),
            }
        )
    return rows


def build_payload(args: argparse.Namespace, input_path: Path, files: list[Path]) -> dict[str, Any]:
    text, snippets = collect_text(files, input_path)
    analysis_text = "\n\n".join(snippet["text"].lstrip("\ufeff") for snippet in snippets).strip()
    now = datetime.now().astimezone()
    readable_lines = compact_lines(analysis_text)
    cta = detect_cta(analysis_text)
    dates = detect_dates(analysis_text)

    if analysis_text:
        summary = " ".join(readable_lines[:3])
        confidence = "trung bình"
        limitations = [
            "Phân tích này được tạo bằng mode manual/local scaffold, chưa phải phân tích Gemini tự động.",
            "Chỉ bóc tách chắc chắn các file text đọc được; ảnh/PDF/media cần OCR hoặc review riêng.",
        ]
    else:
        summary = "Artifact đã được lập chỉ mục nguồn, nhưng chưa có text đọc được để phân tích nội dung."
        confidence = "thấp"
        limitations = [
            "Không tìm thấy text đọc được trong artifact bằng analyzer hiện tại.",
            "Cần OCR, Gemini review, hoặc human review để bóc tách nguyên văn từ ảnh/PDF/media.",
        ]

    if args.mode == "local-ocr":
        limitations.append("Mode local-ocr đã được yêu cầu nhưng repo chưa cấu hình OCR engine.")

    outline = []
    for index, line in enumerate(readable_lines[:5], start=1):
        outline.append({"title": f"Ý {index}", "detail": line, "evidence": "Text sample"})
    if not outline:
        outline.append(
            {
                "title": "Source inventory",
                "detail": f"Đã ghi nhận {len(files)} source file.",
                "evidence": "Filesystem metadata",
            }
        )

    verbatim = []
    for snippet in snippets[:5]:
        excerpt = snippet["text"][:1200]
        verbatim.append(
            {
                "source": snippet["source"],
                "speaker_or_author": "",
                "time_or_page": "",
                "text": excerpt,
            }
        )

    entities = []
    for date_value in dates:
        entities.append({"type": "Thời gian/Ngày", "name": date_value, "evidence": "Regex from text"})

    artifact_id = args.artifact_id or (input_path.stem if input_path.is_file() else input_path.name)
    return {
        "artifact_id": artifact_id,
        "version": args.version,
        "source_type": "folder" if input_path.is_dir() else input_path.suffix.lower().lstrip(".") or "file",
        "created_at": now.isoformat(timespec="seconds"),
        "analysis_mode": args.mode,
        "sources": source_rows(files, input_path),
        "source_hash": aggregate_hash(input_path, files),
        "content_range": args.content_range
        or "Chưa xác định tự động; cần reviewer bổ sung nếu artifact là capture nhiều trang/thời điểm.",
        "verbatim_extraction": verbatim,
        "detailed_outline": outline,
        "summary": summary[:1500],
        "cta": cta,
        "tone_analysis": [
            {
                "subject": "Chưa xác định",
                "tone": "Chưa phân tích tự động",
                "approach": "Cần Gemini/human review nếu artifact có hội thoại hoặc nhiều tác giả.",
                "evidence": "",
            }
        ],
        "key_points": readable_lines[:5] if readable_lines else ["Đã tạo source inventory; chưa có nội dung text để rút ý chính."],
        "entities": entities,
        "action_items": [],
        "analysis_lenses": {
            "decision_log": [],
            "risks_or_blockers": limitations,
            "opportunity_map": [],
            "content_repurposing": [],
            "knowledge_graph_tags": [args.version, input_path.name],
            "second_brain_value": "Có thể dùng làm record khởi đầu để gắn artifact, AI sidecar và storage link.",
        },
        "follow_up_questions": [
            "Artifact này có được phép gửi lên Gemini/cloud API không?",
            "Phạm vi nội dung cần phân tích đầy đủ là file hiện tại hay cả folder liên quan?",
            "Có cần tạo NotebookLM source pack riêng không?",
        ],
        "storage_links": {
            "local_artifact": str(input_path),
            "google_drive": "",
            "notebooklm_source_file": "",
            "notebooklm_prompt_file": "",
            "database_record": "",
        },
        "confidence": confidence,
        "limitations": limitations,
        "privacy": {
            "classification": args.privacy,
            "cloud_upload_allowed": bool(args.allow_cloud_upload and args.mode == "gemini"),
        },
    }


def render_markdown(payload: dict[str, Any], input_path: Path) -> str:
    source_table = "\n".join(
        f"| {table_escape(item['label'])} | {table_escape(item['type'])} | {item['size_bytes']} | `{item['sha256'][:12]}` |"
        for item in payload["sources"]
    )
    if not source_table:
        source_table = "| Không có source file |  |  |  |"

    verbatim_rows = "\n".join(
        "| {source} | {author} | {time} | {text} |".format(
            source=table_escape(Path(item["source"]).name),
            author=table_escape(item.get("speaker_or_author", "")),
            time=table_escape(item.get("time_or_page", "")),
            text=table_escape(item.get("text", "")[:600]),
        )
        for item in payload["verbatim_extraction"]
    )
    if not verbatim_rows:
        verbatim_rows = "| Chưa có text đọc được |  |  | Cần OCR/Gemini/human review. |"

    outline_lines = "\n".join(
        f"{index}. {item['title']}: {item['detail']}\n   - Bằng chứng: {item['evidence']}"
        for index, item in enumerate(payload["detailed_outline"], start=1)
    )

    entity_rows = "\n".join(
        f"| {table_escape(item['type'])} | {table_escape(item['name'])} | {table_escape(item['evidence'])} |"
        for item in payload["entities"]
    )
    if not entity_rows:
        entity_rows = "| Chưa xác định |  | Cần phân tích thêm. |"

    key_points = "\n".join(f"{index}. {point}" for index, point in enumerate(payload["key_points"], start=1))
    questions = "\n".join(f"{index}. {question}" for index, question in enumerate(payload["follow_up_questions"], start=1))
    limitations = "\n".join(f"- {item}" for item in payload["limitations"])

    return f"""# AI Analysis: {input_path.name}

**Artifact nguồn:** `{payload['storage_links']['local_artifact']}`
**Phiên bản:** `{payload['version']}`
**Phạm vi nội dung:** {payload['content_range']}
**Ngày phân tích:** {payload['created_at']}
**Phương pháp:** `{payload['analysis_mode']}`
**Mức riêng tư:** `{payload['privacy']['classification']}`

---

## 1. Tóm Tắt Điều Hành

{payload['summary']}

---

## 2. Source Inventory

| Nguồn | Loại | Size bytes | SHA256 prefix |
|---|---|---:|---|
{source_table}

---

## 3. Bóc Tách Nguyên Văn

| Nguồn | Người nói/Tác giả | Thời gian/Trang | Nguyên văn |
|---|---|---|---|
{verbatim_rows}

---

## 4. Dàn Ý Chi Tiết

{outline_lines}

---

## 5. Tóm Tắt Ngắn Và CTA

**Tóm tắt ngắn:** {payload['summary']}

**CTA / bước tiếp theo:** {payload['cta']}

---

## 6. Ngữ Điệu Và Cách Tiếp Cận Theo Từng Đối Tượng

Chưa phân tích tự động ở mức đáng tin cậy. Cần Gemini hoặc human review nếu artifact có hội thoại, nhiều người nói, hoặc nhiều nguồn.

---

## 7. Ý Chính

{key_points}

---

## 8. Thực Thể Được Nhận Diện

| Loại | Tên | Bằng chứng |
|---|---|---|
{entity_rows}

---

## 9. Việc Cần Làm

| Người phụ trách | Việc cần làm | Ưu tiên | Bằng chứng |
|---|---|---|---|
| Reviewer | Kiểm tra lại sidecar này bằng Gemini/human review nếu cần phân tích đầy đủ. | P1 | Analyzer hiện là scaffold local-only. |

---

## 10. Các Góc Phân Tích Thêm

- **Decision log:** Chưa xác định tự động.
- **Rủi ro và điểm nghẽn:** Xem phần giới hạn bên dưới.
- **Opportunity map:** Cần reviewer bổ sung sau khi có nội dung đọc được.
- **Content repurposing:** Cần reviewer xác định sau khi phân tích nội dung.
- **Knowledge graph tags:** `{', '.join(payload['analysis_lenses']['knowledge_graph_tags'])}`
- **Second-brain value:** {payload['analysis_lenses']['second_brain_value']}

---

## 11. Câu Hỏi Follow-Up

{questions}

---

## 12. Link Lưu Trữ Và Second Brain

| Đích lưu trữ | Link/ID | Trạng thái | Ghi chú |
|---|---|---|---|
| Local artifact | `{payload['storage_links']['local_artifact']}` | local | Source gốc. |
| Google Drive |  | planned | Chỉ sync sau khi được duyệt privacy. |
| NotebookLM source file |  | planned | Source cần sạch và đúng phạm vi. |
| NotebookLM prompt file |  | planned | Prompt/instruction phải tách khỏi source. |
| Database record |  | planned | Nên lưu metadata trước, không nhất thiết lưu nội dung riêng tư. |

---

## 13. Độ Chắc Chắn Và Giới Hạn

- **Độ chắc chắn:** {payload['confidence']}
{limitations}
- **Ghi chú riêng tư:** Không commit, share, hoặc upload nếu source chứa dữ liệu riêng tư.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate local AI sidecar Markdown/JSON for an artifact.")
    parser.add_argument("--input", required=True, help="Artifact file or folder to analyze.")
    parser.add_argument("--version", required=True, help="Version label such as V10, V12, V13, TEST.")
    parser.add_argument("--mode", choices=["manual", "local-ocr", "gemini"], default="manual")
    parser.add_argument("--privacy", choices=["unknown", "private", "internal", "shareable"], default="unknown")
    parser.add_argument("--private", action="store_true", help="Shortcut for --privacy private.")
    parser.add_argument("--allow-cloud-upload", action="store_true", help="Required for gemini mode.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing sidecar outputs.")
    parser.add_argument("--output-dir", help="Optional output directory. Defaults beside the artifact or inside folder.")
    parser.add_argument("--artifact-id", default="", help="Optional stable artifact id.")
    parser.add_argument("--content-range", default="", help="Optional content range label.")
    parser.add_argument("--max-files", type=int, default=200, help="Maximum files to index for folder input.")
    return parser.parse_args()


def output_paths(input_path: Path, output_dir: str | None) -> tuple[Path, Path]:
    base_name = input_path.stem if input_path.is_file() else input_path.name
    target_dir = Path(output_dir).resolve() if output_dir else (input_path.parent if input_path.is_file() else input_path)
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / f"{base_name}_AI_ANALYSIS.md", target_dir / f"{base_name}_AI_ANALYSIS.json"


def main() -> int:
    args = parse_args()
    if args.private:
        args.privacy = "private"

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"ERROR: input does not exist: {input_path}", file=sys.stderr)
        return 1

    if args.mode == "gemini" and not args.allow_cloud_upload:
        print(
            "BLOCKED: gemini mode would require cloud upload. Re-run only with --allow-cloud-upload after explicit approval.",
            file=sys.stderr,
        )
        return 2

    if args.mode == "gemini":
        print(
            "BLOCKED: Gemini API execution is not implemented in this repo yet. Use Gemini_Test scripts for manual review.",
            file=sys.stderr,
        )
        return 2

    template_path = Path(__file__).resolve().parent / "templates" / "ai_analysis_sidecar_template.md"
    if not template_path.exists():
        print(f"ERROR: missing template: {template_path}", file=sys.stderr)
        return 1
    template_path.read_text(encoding="utf-8")

    files = iter_source_files(input_path, args.max_files)
    if not files:
        print(f"ERROR: no source files found under: {input_path}", file=sys.stderr)
        return 1

    md_path, json_path = output_paths(input_path, args.output_dir)
    if not args.force and (md_path.exists() or json_path.exists()):
        print(f"ERROR: output exists. Use --force to overwrite: {md_path} / {json_path}", file=sys.stderr)
        return 1

    payload = build_payload(args, input_path, files)
    payload["storage_links"]["analysis_markdown"] = str(md_path)
    payload["storage_links"]["analysis_json"] = str(json_path)

    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload, input_path), encoding="utf-8")

    print(f"AI sidecar Markdown: {md_path}")
    print(f"AI sidecar JSON: {json_path}")
    print(f"Privacy: {payload['privacy']['classification']}")
    print(f"Mode: {payload['analysis_mode']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
