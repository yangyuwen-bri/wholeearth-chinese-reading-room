#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import time
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / "_local"
WORK = LOCAL / "legacy" / "work" / "wholeearth"
GUIDES = ROOT / "data" / "issue_index.json"
EVIDENCE = ROOT / "data" / "evidence_dossiers"
ISSUES = EVIDENCE / "issues"
OCR_SUPPLEMENTS = ROOT / "data" / "ocr_supplements"

THEMES = {
    "software_computing": [
        "software",
        "computer",
        "program",
        "programming",
        "unix",
        "network",
        "telecommunicat",
        "database",
        "modem",
        "bbs",
        "online",
    ],
    "tools_craft": ["tool", "tools", "craft", "industry", "build", "building", "design", "shelter", "nomad"],
    "ecology_place": ["ecology", "ecological", "energy", "soil", "water", "garden", "farm", "food", "land", "place"],
    "learning_media": ["learning", "education", "school", "teacher", "children", "book", "media", "writing"],
    "community_politics": ["community", "politic", "war", "women", "cooperation", "network", "communication"],
}

NOISE = {
    "digitized by the internet archive",
    "https archive org",
    "creative commons",
    "copyright",
    "isbn",
    "contents",
    "index",
    "continued",
}


def clean(line: str) -> str:
    line = line.replace("\u2014", "-").replace("\u2013", "-")
    line = re.sub(r"\s+", " ", line).strip()
    return line


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "issue"


def ocr_path(identifier: str) -> Path | None:
    for path in [WORK / "ocr" / f"{identifier}_djvu.txt", WORK / f"{identifier}_djvu.txt"]:
        if path.exists():
            return path
    return None


def page_xml_path(identifier: str) -> Path | None:
    for path in [
        WORK / "page_xml" / f"{identifier}_djvu.xml",
        ROOT / "_local" / "page_xml" / f"{identifier}_djvu.xml",
    ]:
        if path.exists():
            return path
    return None


def significant_lines(text: str) -> list[tuple[int, str]]:
    rows = []
    for idx, raw in enumerate(text.splitlines(), start=1):
        line = clean(raw)
        if len(line) < 4:
            continue
        low = line.lower()
        if any(n in low for n in NOISE):
            continue
        if re.fullmatch(r"[\W_0-9]+", line):
            continue
        rows.append((idx, line))
    return rows


def heading_score(line: str) -> int:
    low = line.lower()
    score = 0
    letters = re.sub(r"[^A-Za-z]", "", line)
    if letters and sum(1 for c in letters if c.isupper()) / max(1, len(letters)) > 0.72:
        score += 3
    if re.match(r"^\d{1,3}\s+[A-Z][A-Z0-9 '&:.,-]{3,}$", line):
        score += 4
    if 5 <= len(line) <= 80:
        score += 1
    for word in ["program", "whole systems", "community", "learning", "ecology", "energy", "interview", "review", "communications", "shelter"]:
        if word in low:
            score += 2
    if re.search(r"\b(?:po box|street|avenue|isbn|\$|copyright)\b", low):
        score -= 3
    if len(line) > 110:
        score -= 2
    return score


def candidate_headings(rows: list[tuple[int, str]], limit: int = 80) -> list[dict]:
    seen = set()
    out = []
    for line_no, line in rows:
        score = heading_score(line)
        key = line.lower()
        if score < 3 or key in seen:
            continue
        seen.add(key)
        out.append({"line": line_no, "text": line, "score": score})
    out.sort(key=lambda item: (-item["score"], item["line"]))
    return out[:limit]


def snippets_for_terms(rows: list[tuple[int, str]], terms: list[str], limit: int = 12) -> list[dict]:
    out = []
    used = set()
    lower_terms = [t.lower() for t in terms]
    for pos, (line_no, line) in enumerate(rows):
        low = line.lower()
        hit = next((t for t in lower_terms if t in low), "")
        if not hit:
            continue
        start = max(0, pos - 2)
        end = min(len(rows), pos + 4)
        snippet = " ".join(row[1] for row in rows[start:end])
        key = snippet[:180].lower()
        if key in used:
            continue
        used.add(key)
        out.append({"line": line_no, "term": hit, "snippet": snippet[:900]})
        if len(out) >= limit:
            break
    return out


def page_markers(rows: list[tuple[int, str]], identifier: str, limit: int = 24) -> list[dict]:
    out = []
    seen = set()
    for line_no, line in rows:
        m = re.match(r"^(\d{1,3})\s+([A-Z][A-Z0-9 '&:.,_-]{3,})$", line)
        if not m:
            continue
        page = int(m.group(1))
        title = clean(m.group(2))
        if page in seen:
            continue
        seen.add(page)
        out.append(
            {
                "line": line_no,
                "page": page,
                "title": title,
                "image_url": None,
                "note": "Full-text OCR line heuristic only; not a verified Archive page anchor.",
            }
        )
        if len(out) >= limit:
            break
    return out


def page_ocr_audit(identifier: str) -> dict | None:
    xml_path = page_xml_path(identifier)
    if not xml_path:
        return None
    root = ET.parse(xml_path).getroot()
    pages = []
    for leaf, obj in enumerate(root.findall(".//OBJECT")):
        words = [word.text for word in obj.findall(".//WORD") if word.text]
        pages.append({"leaf": leaf, "word_count": len(words)})
    if not pages:
        return None
    empty = [page["leaf"] for page in pages if page["word_count"] == 0]
    short = [page for page in pages if page["word_count"] <= 50]
    supplements = []
    supplement_dir = OCR_SUPPLEMENTS / identifier
    if supplement_dir.exists():
        for supplement_path in sorted(supplement_dir.glob("leaf_*.txt")):
            m = re.search(r"leaf_(\d+)\.txt$", supplement_path.name)
            if not m:
                continue
            text = supplement_path.read_text(encoding="utf-8", errors="replace")
            supplements.append(
                {
                    "leaf": int(m.group(1)),
                    "path": str(supplement_path.relative_to(ROOT)),
                    "word_count": len(text.split()),
                }
            )
    return {
        "source": str(xml_path.relative_to(ROOT)),
        "coordinate_rule": "Internet Archive public page order: djvu.xml OBJECT index == /page/n{leaf}. Do not use PARAM PAGE as Archive leaf.",
        "page_count": len(pages),
        "total_words": sum(page["word_count"] for page in pages),
        "empty_leafs": empty,
        "short_leafs": short,
        "supplemental_ocr": supplements,
        "notes": [
            "Official OCR is suitable as translation draft input, but scan review is required for dense multi-column pages, index pages, tables, captions, and very short OCR pages.",
        ],
    }


def theme_counts(text: str) -> dict[str, int]:
    low = text.lower()
    return {name: sum(low.count(term) for term in terms) for name, terms in THEMES.items()}


def issue_terms(issue: dict) -> list[str]:
    terms = []
    for topic in issue.get("topics", []):
        if topic:
            terms.append(str(topic))
    terms.extend(
        [
            "whole systems",
            "community",
            "learning",
            "programming",
            "software",
            "ecology",
            "energy",
            "tools",
            "communications",
            "interview",
        ]
    )
    return terms


def make_issue_dossier(issue: dict) -> dict:
    ident = issue.get("identifier", "")
    path = ocr_path(ident)
    if not path:
        raise FileNotFoundError(ident)
    text = path.read_text(encoding="utf-8", errors="replace")
    rows = significant_lines(text)
    counts = theme_counts(text)
    top_themes = [name for name, value in sorted(counts.items(), key=lambda kv: -kv[1]) if value > 0][:3]
    return {
        "title": issue.get("title", ""),
        "identifier": ident,
        "year": issue.get("year"),
        "season": issue.get("season"),
        "collection": issue.get("collection"),
        "collection_zh": issue.get("collection_zh"),
        "pages": issue.get("pages"),
        "url": issue.get("url"),
        "archive_url": issue.get("archive_url"),
        "pdf_url": issue.get("pdf_url"),
        "cover_url": issue.get("cover_url"),
        "ocr_path": str(path.relative_to(ROOT)),
        "ocr_chars": len(text),
        "ocr_page_audit": page_ocr_audit(ident),
        "significant_line_count": len(rows),
        "theme_counts": counts,
        "top_themes": top_themes,
        "page_markers": page_markers(rows, ident),
        "candidate_headings": candidate_headings(rows),
        "snippets": snippets_for_terms(rows, issue_terms(issue)),
        "opening_lines": [{"line": n, "text": line} for n, line in rows[:40]],
    }


def write_markdown(dossier: dict, dest: Path) -> None:
    lines = [
        f"# {dossier['title']}",
        "",
        f"- identifier: `{dossier['identifier']}`",
        f"- year: {dossier.get('year')}",
        f"- collection: {dossier.get('collection_zh')}",
        f"- OCR: `{dossier['ocr_path']}`, {dossier['ocr_chars']} chars",
        f"- archive: {dossier.get('archive_url')}",
        "",
        "## OCR Page Audit",
    ]
    audit = dossier.get("ocr_page_audit")
    if audit:
        lines.extend(
            [
                f"- page OCR: `{audit['source']}`",
                f"- coordinate rule: {audit['coordinate_rule']}",
                f"- pages: {audit['page_count']}",
                f"- total OCR words: {audit['total_words']}",
                f"- empty leafs: {audit['empty_leafs']}",
                "- short leafs: "
                + ", ".join(f"leaf {item['leaf']} ({item['word_count']} words)" for item in audit["short_leafs"]),
                "- supplemental OCR: "
                + (
                    ", ".join(
                        f"leaf {item['leaf']} ({item['word_count']} words, `{item['path']}`)"
                        for item in audit.get("supplemental_ocr", [])
                    )
                    or "none"
                ),
                f"- note: {audit['notes'][0]}",
            ]
        )
    else:
        lines.append("- page-level OCR XML not found; use full-text OCR only for search, not page anchoring.")
    lines.extend(["", "## OCR Line Heuristics"])
    lines.append("These are full-text OCR line heuristics for search only; they are not verified page anchors.")
    for item in dossier["page_markers"][:16]:
        lines.append(f"- p.{item['page']} line {item['line']}: {item['title']} ({item['note']})")
    lines.extend(["", "## Candidate Headings"])
    for item in dossier["candidate_headings"][:30]:
        lines.append(f"- line {item['line']}: {item['text']}")
    lines.extend(["", "## Evidence Snippets"])
    for item in dossier["snippets"][:12]:
        lines.append(f"- line {item['line']} / {item['term']}: {item['snippet']}")
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if EVIDENCE.exists():
        shutil.rmtree(EVIDENCE)
    ISSUES.mkdir(parents=True, exist_ok=True)
    guides = json.loads(GUIDES.read_text(encoding="utf-8"))
    index = []
    start = time.time()
    for idx, issue in enumerate(guides, start=1):
        dossier = make_issue_dossier(issue)
        slug = slugify(issue.get("slug") or issue.get("title") or issue.get("identifier"))
        json_path = ISSUES / f"{slug}.json"
        md_path = ISSUES / f"{slug}.md"
        json_path.write_text(json.dumps(dossier, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(dossier, md_path)
        index.append(
            {
                "title": dossier["title"],
                "identifier": dossier["identifier"],
                "year": dossier["year"],
                "collection_zh": dossier["collection_zh"],
                "json": str(json_path.relative_to(EVIDENCE)),
                "markdown": str(md_path.relative_to(EVIDENCE)),
                "top_themes": dossier["top_themes"],
                "heading_count": len(dossier["candidate_headings"]),
                "snippet_count": len(dossier["snippets"]),
            }
        )
        if idx == 1 or idx % 10 == 0 or idx == len(guides):
            elapsed = max(0.01, time.time() - start)
            speed = idx / elapsed
            eta = (len(guides) - idx) / speed
            print(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S %Z')}] evidence_progress done={idx}/{len(guides)} speed={speed:.2f}_issues_per_sec eta_sec={eta:.0f}",
                flush=True,
            )
    summary = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "issues": len(index),
        "json_files": len(list(ISSUES.glob("*.json"))),
        "markdown_files": len(list(ISSUES.glob("*.md"))),
        "top_theme_distribution": Counter(theme for item in index for theme in item["top_themes"]),
        "index": index,
    }
    (EVIDENCE / "index.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "index"}, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
