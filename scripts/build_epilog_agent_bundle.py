#!/usr/bin/env python3
"""Build the issue-agent knowledge bundle for Whole Earth Epilog.

The bundle is a structured, reader-facing reference layer for a future chat
agent. It does not call a model or create embeddings. It normalizes the existing
Epilog editorial work into page, chapter, bibliography, and retrieval records
with stable IDs and source citations.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ISSUE_ID = "wholeearthepilog00unse"
ISSUE_TITLE = "Whole Earth Epilog, October 1974"
SCHEMA_VERSION = "issue-agent-bundle-v1"
PRINTED_PAGE_OFFSET = 449
CONTENT_LEAF_MAX = 321

AGENT_ROOT = ROOT / "data/issue_agents"
BUNDLE_DIR = AGENT_ROOT / ISSUE_ID
SCHEMA_DIR = AGENT_ROOT / "_schemas"

CHAPTER_SOURCE = ROOT / "content/readings/1974_whole_earth_epilog_chapter_translation_zh.md"
PAGE_SOURCE = ROOT / "content/readings/1974_whole_earth_epilog_page_level_chinese_reading.md"
BIB_SOURCE = ROOT / "data/bibliography/1974_whole_earth_epilog_links.json"
DOSSIER_SOURCE = ROOT / "_local/legacy/outputs/wholeearth_page_dossiers/wholeearthepilog00unse/pages.json"
EVIDENCE_DOSSIER_SOURCE = ROOT / "data/evidence_dossiers/issues/whole-earth-epilog-october-1974.json"

OUTPUTS = {
    "manifest": BUNDLE_DIR / "manifest.json",
    "system_prompt": BUNDLE_DIR / "system_prompt.md",
    "issue_profile": BUNDLE_DIR / "issue_profile.json",
    "pages": BUNDLE_DIR / "pages.jsonl",
    "chapters": BUNDLE_DIR / "chapters.jsonl",
    "bibliography": BUNDLE_DIR / "bibliography.jsonl",
    "retrieval_units": BUNDLE_DIR / "retrieval_units.jsonl",
    "eval_questions": BUNDLE_DIR / "eval_questions.json",
    "qa_report": BUNDLE_DIR / "qa_report.md",
}

SECTION_RANGES = [
    ("Front Matter", "入口与方法", 0, 4),
    ("Whole Systems", "整体系统", 5, 25),
    ("Land Use", "土地使用", 26, 57),
    ("Shelter", "住所", 58, 77),
    ("Soft Technology", "软技术", 78, 97),
    ("Craft", "手艺", 98, 127),
    ("Community", "共同体", 128, 185),
    ("Nomadics", "游牧", 186, 221),
    ("Communications", "通信", 222, 261),
    ("Learning", "学习", 262, 301),
    ("Business / Index", "出版业务、索引与封底", 302, 321),
]

QA_PATTERNS = {
    "ocr_risk": re.compile(r"OCR|噪声|误读|截断"),
    "layout_risk": re.compile(r"多栏|表格|矩阵|索引|地址|价格|小字|图注|漫画|图片文字|版面"),
    "cover_or_back_matter": re.compile(r"封面|封底|内封|版权|档案"),
    "scan_required": re.compile(r"需回看扫描页|回到扫描图|核对扫描|风险"),
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records))


def slugify(text: str) -> str:
    text = text.lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-") or "section"


def section_for_leaf(leaf: int) -> dict[str, Any]:
    for section_en, section_zh, start, end in SECTION_RANGES:
        if start <= leaf <= end:
            return {
                "section": section_en,
                "section_zh": section_zh,
                "leaf_start": start,
                "leaf_end": end,
            }
    return {"section": "Unknown", "section_zh": "未知", "leaf_start": None, "leaf_end": None}


def printed_page_for_leaf(leaf: int) -> str | None:
    if 5 <= leaf <= 320:
        return str(leaf + PRINTED_PAGE_OFFSET)
    return None


def compact_text(text: str, limit: int | None = None) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    text = re.sub(r"[ \t]+", " ", text)
    if limit and len(text) > limit:
        return text[: limit - 1].rstrip() + "…"
    return text


def extract_headings(lines: list[str]) -> list[str]:
    headings = []
    for line in lines:
        clean = line.strip()
        if not clean or len(clean) > 90:
            continue
        uppercase = sum(1 for char in clean if char.isupper())
        letters = sum(1 for char in clean if char.isalpha())
        if letters and uppercase / letters > 0.55:
            headings.append(clean)
        elif re.match(r"^[A-Z][A-Za-z0-9 .,&'’:/!-]{3,}$", clean):
            headings.append(clean)
    return headings[:12]


def qa_flags_for_text(text: str, raw_lines: list[str]) -> list[str]:
    flags = [name for name, pattern in QA_PATTERNS.items() if pattern.search(text)]
    if len(raw_lines) <= 3:
        flags.append("short_text_or_image_page")
    if len(" ".join(raw_lines)) > 9000:
        flags.append("dense_ocr_page")
    return sorted(set(flags))


def parse_page_level_reading() -> tuple[dict[int, dict[str, Any]], dict[int, str]]:
    text = PAGE_SOURCE.read_text()
    h2_matches = list(re.finditer(r"^## (.+)$", text, flags=re.MULTILINE))
    h3_matches = list(re.finditer(r"^### (.+?) / leaf (\d+)\s*$", text, flags=re.MULTILINE))
    h2_by_start = [(match.start(), match.group(1).strip()) for match in h2_matches]

    def current_h2(position: int) -> str:
        current = ""
        for start, heading in h2_by_start:
            if start < position:
                current = heading
            else:
                break
        return current

    page_notes: dict[int, dict[str, Any]] = {}
    leaf_to_heading: dict[int, str] = {}
    for index, match in enumerate(h3_matches):
        leaf = int(match.group(2))
        start = match.end()
        next_h3 = h3_matches[index + 1].start() if index + 1 < len(h3_matches) else len(text)
        next_h2 = next((h2.start() for h2 in h2_matches if h2.start() > match.start()), len(text))
        end = min(next_h3, next_h2)
        body = text[start:end].strip()
        scan_match = re.search(r"扫描图[:：]\s*(\S+)", body)
        clue_match = re.search(r"页面线索[:：]\s*(.+)", body)
        scan_url = scan_match.group(1).strip() if scan_match else f"https://archive.org/download/{ISSUE_ID}/page/n{leaf}_w500.jpg"
        clues = [item.strip(" `；;") for item in (clue_match.group(1).split("；") if clue_match else []) if item.strip()]
        reading = re.sub(r"扫描图[:：]\s*\S+", "", body)
        reading = re.sub(r"页面线索[:：].+", "", reading).strip()
        heading = match.group(1).strip()
        page_notes[leaf] = {
            "page_heading": heading,
            "section_heading": current_h2(match.start()),
            "scan_url": scan_url,
            "clues": clues,
            "zh_page_reading": compact_text(reading),
        }
        leaf_to_heading[leaf] = heading
    return page_notes, leaf_to_heading


def build_pages() -> list[dict[str, Any]]:
    page_notes, _ = parse_page_level_reading()
    source_pages = {
        int(page["leaf"]): page
        for page in read_json(DOSSIER_SOURCE)["pages"]
        if int(page["leaf"]) <= CONTENT_LEAF_MAX
    }
    records = []
    for leaf in sorted(set(source_pages) | set(page_notes)):
        if leaf > CONTENT_LEAF_MAX:
            continue
        page = source_pages.get(leaf, {"leaf": leaf, "lines": []})
        note = page_notes.get(leaf, {})
        lines = page.get("lines") or []
        raw_ocr = "\n".join(lines).strip()
        section = section_for_leaf(leaf)
        printed_page = printed_page_for_leaf(leaf)
        scan_url = note.get("scan_url") or page.get("image_url") or f"https://archive.org/download/{ISSUE_ID}/page/n{leaf}_w500.jpg"
        zh_reading = note.get("zh_page_reading") or ""
        record = {
            "schema_version": SCHEMA_VERSION,
            "record_id": f"{ISSUE_ID}:page:{leaf:03d}",
            "issue": {
                "issue_id": ISSUE_ID,
                "title": ISSUE_TITLE,
                "source": "internet_archive",
            },
            "page": {
                "leaf": leaf,
                "access_index": page.get("access_index"),
                "printed_page": printed_page,
                "scan_url": scan_url,
                **section,
            },
            "ocr": {
                "raw_ocr": raw_ocr,
                "clean_en": compact_text(raw_ocr),
                "headings": extract_headings(lines),
                "line_count": len(lines),
                "word_count": len(raw_ocr.split()),
                "needs_review": bool(qa_flags_for_text(zh_reading, lines)),
                "qa_flags": qa_flags_for_text(zh_reading, lines),
            },
            "zh_reading": {
                "status": "page_evidence_workbench",
                "page_heading": note.get("page_heading"),
                "section_heading": note.get("section_heading"),
                "clues": note.get("clues") or [],
                "reading_zh": zh_reading,
                "main_claim_zh": first_sentence(zh_reading),
                "why_it_matters_zh": why_it_matters(zh_reading),
            },
            "evidence": {
                "scan_url": scan_url,
                "source_paths": {
                    "page_dossier": str(DOSSIER_SOURCE.relative_to(ROOT)),
                    "page_level_reading": str(PAGE_SOURCE.relative_to(ROOT)),
                },
            },
            "agent_notes": {
                "agent_summary_zh": first_sentence(zh_reading) or f"leaf {leaf} 的 OCR 需要结合扫描页阅读。",
                "key_terms": extract_terms(raw_ocr + "\n" + zh_reading),
                "limitations": [
                    "Use scan_url for final verification before quoting the original.",
                    "This page-level Chinese reading is an evidence workbench, not a diplomatic full-text translation.",
                ],
            },
        }
        records.append(record)
    return records


def first_sentence(text: str) -> str:
    if not text:
        return ""
    normalized = " ".join(text.split())
    match = re.search(r"(.{20,260}?[。！？])", normalized)
    if match:
        return match.group(1)
    match = re.search(r"(.{20,220}?[.!?])", normalized)
    return match.group(1) if match else normalized[:220]


def why_it_matters(text: str) -> str:
    if not text:
        return ""
    for sentence in re.split(r"(?<=[。！？.!?])\s*", " ".join(text.split())):
        if any(token in sentence for token in ["重要", "说明", "体现", "关键", "入口", "Whole Earth"]):
            return sentence[:260]
    return first_sentence(text)


def extract_terms(text: str) -> list[str]:
    terms: list[str] = []
    for match in re.findall(r"《([^》]{2,80})》", text):
        terms.append(match.strip())
    for match in re.findall(r"\b[A-Z][A-Za-z0-9'’&.-]*(?:\s+[A-Z][A-Za-z0-9'’&.-]*){0,5}\b", text):
        if len(match) > 2 and not match.isupper():
            terms.append(match.strip())
    seen = set()
    cleaned = []
    for term in terms:
        key = term.lower()
        if key not in seen:
            seen.add(key)
            cleaned.append(term)
    return cleaned[:20]


def parse_markdown_sections(text: str) -> list[dict[str, Any]]:
    matches = list(re.finditer(r"^(##|###) (.+)$", text, flags=re.MULTILINE))
    records = []
    for index, match in enumerate(matches):
        level = 2 if match.group(1) == "##" else 3
        title = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        content = compact_text(text[start:end])
        if not content and level != 2:
            continue
        if not content:
            content = f"{title} 章节标题。"
        if title in {"译者说明"}:
            section = "Translator Note"
        else:
            section = title
        records.append(
            {
                "level": level,
                "title": title,
                "section": section,
                "content": content,
            }
        )
    return records


def build_chapters() -> list[dict[str, Any]]:
    sections = parse_markdown_sections(CHAPTER_SOURCE.read_text())
    records = []
    counters: Counter[str] = Counter()
    current_h2 = "front"
    for section in sections:
        if section["level"] == 2:
            current_h2 = section["title"]
        counters[current_h2] += 1
        leaf_range = leaf_range_for_chapter(current_h2)
        record_id = f"{ISSUE_ID}:chapter:{slugify(current_h2)}:{counters[current_h2]:03d}"
        if section["level"] == 2:
            record_id = f"{ISSUE_ID}:chapter:{slugify(section['title'])}:000"
        records.append(
            {
                "schema_version": SCHEMA_VERSION,
                "record_id": record_id,
                "issue_id": ISSUE_ID,
                "title": section["title"],
                "parent_section": current_h2 if section["level"] == 3 else None,
                "level": section["level"],
                "leaf_start": leaf_range[0],
                "leaf_end": leaf_range[1],
                "text_zh": section["content"],
                "summary_zh": first_sentence(section["content"]),
                "key_terms": extract_terms(section["content"]),
                "source_path": str(CHAPTER_SOURCE.relative_to(ROOT)),
            }
        )
    return records


def leaf_range_for_chapter(title: str) -> tuple[int | None, int | None]:
    for section_en, section_zh, start, end in SECTION_RANGES:
        if section_zh in title or section_en in title:
            return start, end
    if "封面" in title or "开篇" in title or "使用说明" in title:
        return 0, 4
    if "出版" in title or "索引" in title or "封底" in title:
        return 302, 321
    return None, None


def build_bibliography() -> list[dict[str, Any]]:
    items = read_json(BIB_SOURCE)["items"]
    records = []
    for item in items:
        mentions = item.get("source_mentions") or []
        first_mention = mentions[0] if mentions else {}
        leaf = first_mention.get("leaf")
        printed_page = printed_page_for_leaf(int(leaf)) if leaf is not None else None
        records.append(
            {
                "schema_version": SCHEMA_VERSION,
                "record_id": f"{ISSUE_ID}:bib:{slugify(item['title'])}",
                "issue_id": ISSUE_ID,
                "title": item["title"],
                "status": item["status"],
                "audit_note": item.get("audit_note"),
                "source": {
                    "leaf": leaf,
                    "printed_page": printed_page,
                    "section": first_mention.get("section"),
                    "scan_url": first_mention.get("image_url"),
                    "excerpt": first_mention.get("excerpt"),
                    "source_years": first_mention.get("source_years") or [],
                },
                "links": item.get("links") or [],
                "best_candidates": item.get("candidates") or [],
                "key_terms": extract_terms(item["title"] + "\n" + (first_mention.get("excerpt") or "")),
            }
        )
    return records


def split_text(text: str, max_chars: int = 3200) -> list[str]:
    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > max_chars:
            chunks.append(current)
            current = paragraph
        else:
            current = paragraph if not current else current + "\n\n" + paragraph
    if current:
        chunks.append(current)
    return chunks or ([text] if text else [])


def build_retrieval_units(
    pages: list[dict[str, Any]],
    chapters: list[dict[str, Any]],
    bibliography: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    units = []
    for page in pages:
        page_meta = page["page"]
        text = "\n\n".join(
            part
            for part in [
                f"页面: leaf {page_meta['leaf']} / printed page {page_meta.get('printed_page') or 'n/a'} / {page_meta.get('section_zh')}",
                page["zh_reading"].get("reading_zh") or "",
                "OCR 摘录:\n" + compact_text(page["ocr"].get("clean_en") or "", 1800),
            ]
            if part
        )
        units.append(
            retrieval_unit(
                unit_id=f"{page['record_id']}:retrieval",
                source_type="page",
                source_record_id=page["record_id"],
                title=page["zh_reading"].get("page_heading") or f"leaf {page_meta['leaf']}",
                text=text,
                leaf_start=page_meta["leaf"],
                leaf_end=page_meta["leaf"],
                section=page_meta.get("section"),
                scan_urls=[page_meta["scan_url"]],
                key_terms=page["agent_notes"].get("key_terms") or [],
                qa_flags=page["ocr"].get("qa_flags") or [],
            )
        )
    for chapter in chapters:
        for index, chunk in enumerate(split_text(chapter["text_zh"]), 1):
            units.append(
                retrieval_unit(
                    unit_id=f"{chapter['record_id']}:retrieval:{index:02d}",
                    source_type="chapter",
                    source_record_id=chapter["record_id"],
                    title=chapter["title"],
                    text=chunk,
                    leaf_start=chapter.get("leaf_start"),
                    leaf_end=chapter.get("leaf_end"),
                    section=chapter.get("parent_section") or chapter["title"],
                    scan_urls=[],
                    key_terms=chapter.get("key_terms") or [],
                    qa_flags=[],
                )
            )
    for item in bibliography:
        source = item["source"]
        links = "; ".join(link["url"] for link in item.get("links") or [])
        text = "\n".join(
            part
            for part in [
                f"书目/资料: {item['title']}",
                f"状态: {item['status']}",
                f"审核说明: {item.get('audit_note') or ''}",
                f"原书位置: leaf {source.get('leaf')}, printed page {source.get('printed_page') or 'n/a'}, section {source.get('section') or 'n/a'}",
                f"原书摘录: {source.get('excerpt') or ''}",
                f"链接: {links}" if links else "",
            ]
            if part
        )
        units.append(
            retrieval_unit(
                unit_id=f"{item['record_id']}:retrieval",
                source_type="bibliography",
                source_record_id=item["record_id"],
                title=item["title"],
                text=compact_text(text, 2800),
                leaf_start=source.get("leaf"),
                leaf_end=source.get("leaf"),
                section=source.get("section"),
                scan_urls=[source["scan_url"]] if source.get("scan_url") else [],
                key_terms=item.get("key_terms") or [],
                qa_flags=[] if item["status"] == "confirmed" else ["not_linked_after_audit"],
            )
        )
    return units


def retrieval_unit(
    unit_id: str,
    source_type: str,
    source_record_id: str,
    title: str,
    text: str,
    leaf_start: int | None,
    leaf_end: int | None,
    section: str | None,
    scan_urls: list[str],
    key_terms: list[str],
    qa_flags: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "unit_id": unit_id,
        "issue_id": ISSUE_ID,
        "source_type": source_type,
        "source_record_id": source_record_id,
        "title": title,
        "section": section,
        "leaf_start": leaf_start,
        "leaf_end": leaf_end,
        "scan_urls": scan_urls,
        "text": compact_text(text),
        "key_terms": key_terms,
        "qa_flags": qa_flags,
        "citation_hint": citation_hint(leaf_start, leaf_end, scan_urls),
    }


def citation_hint(leaf_start: int | None, leaf_end: int | None, scan_urls: list[str]) -> str:
    if leaf_start is None:
        return "Cite the source record and explain that no page leaf is attached."
    if leaf_end and leaf_end != leaf_start:
        return f"Cite leaves {leaf_start}-{leaf_end}; include scan URLs when available."
    scan = f"; scan: {scan_urls[0]}" if scan_urls else ""
    return f"Cite leaf {leaf_start}{scan}"


def build_issue_profile(pages: list[dict[str, Any]], bibliography: list[dict[str, Any]]) -> dict[str, Any]:
    evidence = read_json(EVIDENCE_DOSSIER_SOURCE)
    bib_counts = Counter(item["status"] for item in bibliography)
    return {
        "schema_version": SCHEMA_VERSION,
        "issue_id": ISSUE_ID,
        "title": ISSUE_TITLE,
        "year": 1974,
        "date_label": "October 1974",
        "internet_archive_identifier": ISSUE_ID,
        "archive_url": evidence.get("archive_url"),
        "pdf_url": evidence.get("pdf_url"),
        "local_pdf": "_local/pdf_sources/wholeearthepilog00unse.pdf",
        "page_count": len(pages),
        "leaf_range": [pages[0]["page"]["leaf"], pages[-1]["page"]["leaf"]] if pages else [None, None],
        "sections": [
            {"section": en, "section_zh": zh, "leaf_start": start, "leaf_end": end}
            for en, zh, start, end in SECTION_RANGES
        ],
        "source_paths": {
            "chapter_translation": str(CHAPTER_SOURCE.relative_to(ROOT)),
            "page_level_reading": str(PAGE_SOURCE.relative_to(ROOT)),
            "page_dossier": str(DOSSIER_SOURCE.relative_to(ROOT)),
            "bibliography_json": str(BIB_SOURCE.relative_to(ROOT)),
            "evidence_dossier": str(EVIDENCE_DOSSIER_SOURCE.relative_to(ROOT)),
        },
        "bibliography_status_counts": dict(sorted(bib_counts.items())),
        "editorial_status": {
            "page_coverage": "322/322 leaves",
            "chapter_translation": "full-issue chapter-structured Chinese source draft",
            "bibliography_audit": "216 references audited",
            "answer_policy": "Use Chinese reader-facing synthesis with leaf/page/scan citations; verify against scans before quoting original English.",
        },
    }


def build_manifest(
    pages: list[dict[str, Any]],
    chapters: list[dict[str, Any]],
    bibliography: list[dict[str, Any]],
    retrieval_units: list[dict[str, Any]],
) -> dict[str, Any]:
    generated_at = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    review_records = sum(1 for page in pages if page["ocr"].get("needs_review"))
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "issue_id": ISSUE_ID,
        "title": ISSUE_TITLE,
        "bundle_path": str(BUNDLE_DIR.relative_to(ROOT)),
        "record_counts": {
            "pages": len(pages),
            "chapters": len(chapters),
            "bibliography": len(bibliography),
            "retrieval_units": len(retrieval_units),
            "page_review_records": review_records,
        },
        "outputs": {name: str(path.relative_to(ROOT)) for name, path in OUTPUTS.items()},
        "source_paths": {
            "chapter_translation": str(CHAPTER_SOURCE.relative_to(ROOT)),
            "page_level_reading": str(PAGE_SOURCE.relative_to(ROOT)),
            "page_dossier": str(DOSSIER_SOURCE.relative_to(ROOT)),
            "bibliography_json": str(BIB_SOURCE.relative_to(ROOT)),
            "evidence_dossier": str(EVIDENCE_DOSSIER_SOURCE.relative_to(ROOT)),
        },
        "runtime_notes": [
            "This bundle is the standard reference layer for an Epilog issue agent.",
            "Embeddings, vector caches, and chat transcripts should be generated outside this tracked bundle, normally under _local/.",
            "The agent must cite leaf/page/scan evidence and must not represent Chinese reading notes as a verbatim full-text translation.",
        ],
    }


def build_system_prompt() -> str:
    return """# Whole Earth Epilog Issue Agent - System Prompt

You are the issue-specific reading agent for `Whole Earth Epilog, October 1974`.

Answer in Chinese by default. Your job is to help readers understand this issue's
contents, structure, tools, books, editorial judgments, and Whole Earth context.

Use the bundled records as the standard reference:

- `pages.jsonl` for page-level OCR, Chinese page reading, leaf/page/scan evidence.
- `chapters.jsonl` for reader-facing chapter-level interpretation.
- `bibliography.jsonl` for books, pamphlets, magazines, organizations, and audited external links.
- `retrieval_units.jsonl` as the combined retrieval surface.

Rules:

1. Cite concrete evidence whenever answering factual questions. Prefer `leaf`,
   printed page when available, and `scan_url`.
2. Distinguish three layers clearly: original OCR/scans, Chinese editorial
   reading, and external bibliography metadata.
3. Do not claim the Chinese notes are a diplomatic or complete line-by-line
   translation of the original English.
4. If the source record has `qa_flags`, mention scan verification when the user
   asks for exact wording, prices, addresses, tables, image text, or layout.
5. For bibliography questions, only present external links as confirmed when the
   bibliography record status is `confirmed`. For `not_linked_*`, explain the
   audit reason instead of inventing a link.
6. If retrieved context is insufficient, say what is missing and which leaf,
   section, or source record should be checked next.
7. Keep answers reader-facing: explain what the issue is doing and why it
   matters, not just where a keyword appears.
"""


def build_eval_questions() -> list[dict[str, Any]]:
    questions = [
        ("overview", "这本 Epilog 和普通商品目录有什么不同？", ["chapter", "page"], ["leaf 3", "access to tools"]),
        ("overview", "为什么开篇要引用《约伯记》？", ["chapter", "page"], ["leaf 2", "humility"]),
        ("quote", "Stay hungry. Stay foolish. 在哪一页？", ["page"], ["leaf 321", "封底"]),
        ("section", "Whole Systems 这一章的核心作用是什么？", ["chapter", "page"], ["Whole Systems", "Bateson"]),
        ("section", "Land Use 章如何把生态和具体工具连起来？", ["chapter", "page"], ["Land Use"]),
        ("section", "Shelter 章是不是只讲房子？", ["chapter", "page"], ["Shelter"]),
        ("section", "Soft Technology 在这本书里是什么意思？", ["chapter", "page"], ["Soft Technology"]),
        ("section", "Craft 章和现代 DIY 文化有什么关系？", ["chapter", "page"], ["Craft"]),
        ("section", "Community 章处理了哪些社会议题？", ["chapter", "page"], ["Community"]),
        ("section", "Nomadics 章为什么重要？", ["chapter", "page"], ["Nomadics"]),
        ("section", "Communications 章如何理解出版和媒介？", ["chapter", "page"], ["Communications"]),
        ("section", "Learning 章的教育观是什么？", ["chapter", "page"], ["Learning"]),
        ("bibliography", "《Steps to an Ecology of Mind》在书中承担什么角色？", ["bibliography", "chapter"], ["confirmed", "Bateson"]),
        ("bibliography", "Small is Beautiful 有没有外部链接？", ["bibliography"], ["confirmed"]),
        ("bibliography", "Acres, U.S.A. 为什么没有挂链接？", ["bibliography"], ["not_linked"]),
        ("bibliography", "哪些书目是确认链接，哪些是不挂链接？", ["bibliography"], ["status counts"]),
        ("risk", "如果我要引用原英文原句，需要注意什么？", ["page"], ["scan verification", "OCR risk"]),
        ("risk", "多栏和索引页为什么不适合直接按 OCR 回答？", ["page"], ["qa_flags"]),
        ("cross", "Bateson、Buber 和 Whole Earth 的工具观有什么关系？", ["chapter", "bibliography"], ["Whole Systems"]),
        ("cross", "这本书如何把'像神一样'这句话变得不那么傲慢？", ["chapter", "page"], ["purpose", "Job"]),
        ("navigation", "我想从生态/土地使用开始读，应该从哪些 leaf 进入？", ["page"], ["leaf 26", "leaf 57"]),
        ("navigation", "我想查一本册子或书，智能体应该怎么回答？", ["bibliography"], ["confirmed", "not_linked"]),
        ("boundary", "你能给我逐字翻译整本书吗？", ["system"], ["refuse full-text claim", "reading guide"]),
        ("boundary", "这本书里的邮购地址今天还能用吗？", ["bibliography", "system"], ["historical", "do not treat as current"]),
    ]
    return [
        {
            "id": f"epilog-eval-{index:03d}",
            "category": category,
            "question_zh": question,
            "required_sources": required_sources,
            "expected_evidence": expected_evidence,
            "answer_policy": "Answer in Chinese; cite leaf/page/scan when factual; state uncertainty when retrieval context is insufficient.",
        }
        for index, (category, question, required_sources, expected_evidence) in enumerate(questions, 1)
    ]


def build_readme() -> str:
    return """# Issue Agent Knowledge Bundles

This directory contains structured knowledge bundles for per-issue Whole Earth
reading agents.

Each issue gets one folder named by its Internet Archive identifier:

```text
data/issue_agents/{internet_archive_identifier}/
```

Bundle layers:

- `manifest.json`: bundle entry point, source paths, counts, QA status.
- `issue_profile.json`: issue metadata, section map, source locations.
- `pages.jsonl`: page-level OCR, Chinese page reading, scan evidence.
- `chapters.jsonl`: chapter/topic-level Chinese interpretation chunks.
- `bibliography.jsonl`: audited books, pamphlets, periodicals, and links.
- `retrieval_units.jsonl`: combined RAG retrieval surface.
- `system_prompt.md`: answer policy and source-boundary rules.
- `eval_questions.json`: regression questions for smoke testing the issue agent.
- `qa_report.md`: structural QA summary for the bundle.

Runtime artifacts do not belong here. Embeddings, vector stores, model replies,
and chat transcripts should be generated under `_local/`.
"""


def build_schemas() -> dict[str, dict[str, Any]]:
    return {
        "manifest.schema.json": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Issue Agent Manifest",
            "type": "object",
            "required": ["schema_version", "issue_id", "title", "record_counts", "outputs"],
            "properties": {
                "schema_version": {"type": "string"},
                "generated_at": {"type": "string"},
                "issue_id": {"type": "string"},
                "title": {"type": "string"},
                "bundle_path": {"type": "string"},
                "record_counts": {"type": "object"},
                "outputs": {"type": "object"},
                "source_paths": {"type": "object"},
                "runtime_notes": {"type": "array", "items": {"type": "string"}},
            },
        },
        "retrieval_unit.schema.json": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Issue Agent Retrieval Unit",
            "type": "object",
            "required": ["schema_version", "unit_id", "issue_id", "source_type", "source_record_id", "title", "text"],
            "properties": {
                "schema_version": {"type": "string"},
                "unit_id": {"type": "string"},
                "issue_id": {"type": "string"},
                "source_type": {"enum": ["page", "chapter", "bibliography"]},
                "source_record_id": {"type": "string"},
                "title": {"type": "string"},
                "section": {"type": ["string", "null"]},
                "leaf_start": {"type": ["integer", "null"]},
                "leaf_end": {"type": ["integer", "null"]},
                "scan_urls": {"type": "array", "items": {"type": "string"}},
                "text": {"type": "string"},
                "key_terms": {"type": "array", "items": {"type": "string"}},
                "qa_flags": {"type": "array", "items": {"type": "string"}},
                "citation_hint": {"type": "string"},
            },
        },
        "eval_question.schema.json": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Issue Agent Eval Question",
            "type": "object",
            "required": ["id", "category", "question_zh", "required_sources", "expected_evidence", "answer_policy"],
            "properties": {
                "id": {"type": "string"},
                "category": {"type": "string"},
                "question_zh": {"type": "string"},
                "required_sources": {"type": "array", "items": {"type": "string"}},
                "expected_evidence": {"type": "array", "items": {"type": "string"}},
                "answer_policy": {"type": "string"},
            },
        },
    }


def build_qa_report(
    pages: list[dict[str, Any]],
    chapters: list[dict[str, Any]],
    bibliography: list[dict[str, Any]],
    retrieval_units: list[dict[str, Any]],
) -> str:
    page_leaves = [page["page"]["leaf"] for page in pages]
    missing_leaves = sorted(set(range(1, 323)) - set(page_leaves))
    duplicate_leaves = [leaf for leaf, count in Counter(page_leaves).items() if count > 1]
    bib_counts = Counter(item["status"] for item in bibliography)
    retrieval_counts = Counter(unit["source_type"] for unit in retrieval_units)
    qa_flags = Counter(flag for page in pages for flag in page["ocr"]["qa_flags"])
    broken_scan_records = [
        page["record_id"]
        for page in pages
        if not page["page"].get("scan_url", "").startswith(f"https://archive.org/download/{ISSUE_ID}/page/")
    ]
    lines = [
        "# Whole Earth Epilog Issue Agent Bundle - QA Report",
        "",
        f"- issue_id: `{ISSUE_ID}`",
        f"- schema_version: `{SCHEMA_VERSION}`",
        f"- pages: {len(pages)}",
        f"- leaf range: {min(page_leaves)}-{max(page_leaves)}",
        f"- missing leaves: {missing_leaves or 'none'}",
        f"- duplicate leaves: {duplicate_leaves or 'none'}",
        f"- chapter records: {len(chapters)}",
        f"- bibliography records: {len(bibliography)}",
        f"- retrieval units: {len(retrieval_units)}",
        f"- retrieval unit counts: {dict(sorted(retrieval_counts.items()))}",
        f"- bibliography status counts: {dict(sorted(bib_counts.items()))}",
        f"- page QA flags: {dict(sorted(qa_flags.items()))}",
        f"- scan URL format issues: {broken_scan_records or 'none'}",
        "",
        "## Source Boundary",
        "",
        "- `pages.jsonl` combines local OCR, scan URL evidence, and the page-level Chinese evidence workbench.",
        "- `chapters.jsonl` comes from the reader-facing chapter translation draft.",
        "- `bibliography.jsonl` comes from the audited bibliography/link JSON.",
        "- Runtime chat transcripts, model outputs, vector caches, and embeddings are intentionally excluded from this tracked bundle.",
        "",
        "## Agent Use",
        "",
        "The chat agent should retrieve from `retrieval_units.jsonl`, then cite the underlying source record and scan leaf. For exact original wording, especially on OCR-risk pages, the answer must ask the reader to verify against the scan URL.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    AGENT_ROOT.mkdir(parents=True, exist_ok=True)
    BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)

    pages = build_pages()
    chapters = build_chapters()
    bibliography = build_bibliography()
    retrieval_units = build_retrieval_units(pages, chapters, bibliography)
    issue_profile = build_issue_profile(pages, bibliography)
    manifest = build_manifest(pages, chapters, bibliography, retrieval_units)
    eval_questions = build_eval_questions()

    (AGENT_ROOT / "README.md").write_text(build_readme())
    for filename, schema in build_schemas().items():
        write_json(SCHEMA_DIR / filename, schema)

    write_json(OUTPUTS["manifest"], manifest)
    OUTPUTS["system_prompt"].write_text(build_system_prompt())
    write_json(OUTPUTS["issue_profile"], issue_profile)
    write_jsonl(OUTPUTS["pages"], pages)
    write_jsonl(OUTPUTS["chapters"], chapters)
    write_jsonl(OUTPUTS["bibliography"], bibliography)
    write_jsonl(OUTPUTS["retrieval_units"], retrieval_units)
    write_json(OUTPUTS["eval_questions"], eval_questions)
    OUTPUTS["qa_report"].write_text(build_qa_report(pages, chapters, bibliography, retrieval_units))

    print(
        json.dumps(
            {
                "bundle": str(BUNDLE_DIR),
                "pages": len(pages),
                "chapters": len(chapters),
                "bibliography": len(bibliography),
                "retrieval_units": len(retrieval_units),
                "eval_questions": len(eval_questions),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
