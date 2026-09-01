#!/usr/bin/env python3
"""Generate source-pack leaves and initial status for the January 1971 issue."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ISSUE_ID = "wholeearthcatalo00unse_3"
PACKAGE = ROOT / "content" / "translations" / ISSUE_ID
SOURCE_ROOT = ROOT.parents[1] / "ai-https-wholeearth-info" / "_local" / "legacy" / "work" / "wholeearth" / "page_xml"
DJVU_XML = SOURCE_ROOT / f"{ISSUE_ID}_djvu.xml"
SCANDATA_XML = SOURCE_ROOT / f"{ISSUE_ID}_scandata.xml"


def text_lines(obj: ET.Element) -> list[str]:
    lines = []
    for line in obj.findall(".//LINE"):
        words = [word.text or "" for word in line.findall("WORD")]
        value = " ".join(word for word in words if word).strip()
        if value:
            lines.append(value)
    return lines


def page_records() -> list[dict[str, object]]:
    objects = ET.parse(DJVU_XML).getroot().findall(".//OBJECT")
    physical_pages = ET.parse(SCANDATA_XML).getroot().findall(".//pageData/page")
    access_pages = [
        page
        for page in physical_pages
        if page.findtext("addToAccessFormats", "true").strip().lower() != "false"
    ]
    if len(objects) != 48 or len(access_pages) != 48:
        raise RuntimeError(
            f"Expected 48 OCR objects and 48 access pages; got {len(objects)} and {len(access_pages)}"
        )

    records = []
    for leaf, (obj, page) in enumerate(zip(objects, access_pages, strict=True)):
        lines = text_lines(obj)
        printed = page.findtext("pageNumber")
        physical = int(page.attrib["leafNum"])
        page_type = page.findtext("pageType") or "Normal"
        section = "Front Matter" if leaf == 0 else "Back Matter" if leaf == 47 else "Supplement"
        flags = ["scan_required", "layout_risk"]
        word_count = sum(len(line.split()) for line in lines)
        if word_count > 1600:
            flags.append("dense_ocr_page")
        if word_count < 80:
            flags.append("short_text_or_image_page")
        records.append(
            {
                "leaf": leaf,
                "physical": physical,
                "printed": printed,
                "page_type": page_type,
                "hand_side": page.findtext("handSide") or "unknown",
                "lines": lines,
                "word_count": word_count,
                "section": section,
                "flags": flags,
            }
        )
    return records


def leaf_markdown(record: dict[str, object]) -> str:
    leaf = int(record["leaf"])
    printed = record["printed"] or "none"
    transcript = "\n".join(record["lines"]) or "[official OCR blank]"
    flags = ", ".join(f"`{flag}`" for flag in record["flags"])
    return f"""# Leaf {leaf:03d} Translation

## Source Pack

- Issue ID: `{ISSUE_ID}`
- Access leaf: `n{leaf}`; canonical physical scan leaf: `{record['physical']}`.
- Printed page: `{printed}`; page type: `{record['page_type']}`; hand side: `{record['hand_side']}`.
- Scan URL: https://archive.org/download/{ISSUE_ID}/page/n{leaf}_w500.jpg
- High-resolution scan URL: https://archive.org/download/{ISSUE_ID}/page/n{leaf}_w2000.jpg
- OCR source: official Internet Archive DjVu XML; {record['word_count']} OCR words. No supplemental OCR used.
- OCR risk flags: {flags}.
- Scan verification: required before orchestrator acceptance.

### Official OCR Line Transcript

The following is source evidence only. It preserves official OCR line order
and errors; it is not an approved reading order or a translation.

~~~text
{transcript}
~~~

## Context Notes

- Source pack generated from the verified public-access/DjVu/scandata mapping.
- Inventory every visible entry, excerpt, caption, diagram, table, signature,
  form label, and order/access field against the scan before translation.
- Do not treat OCR line order as page reading order on multi-column layouts.

## Glossary Updates


## Final Translation


## Omitted Bibliographic/Order Info

- Pending translation.

## OCR / Uncertainty Notes

- High-resolution scan verification pending.

## Self Critique

- Pending translation.
"""


def main() -> None:
    existing_leaves = sorted((PACKAGE / "leaves").glob("leaf_*.md"))
    status_path = PACKAGE / "status.jsonl"
    initialized_status = status_path.exists() and "<issue_id>" not in status_path.read_text()
    if existing_leaves or initialized_status:
        raise RuntimeError(
            "Translation package is already initialized; refusing to overwrite issue work"
        )
    records = page_records()
    leaves_dir = PACKAGE / "leaves"
    leaves_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        leaf = int(record["leaf"])
        (leaves_dir / f"leaf_{leaf:03d}.md").write_text(leaf_markdown(record))

    status_records = []
    for record in records:
        leaf = int(record["leaf"])
        printed = record["printed"]
        status_records.append(
            {
                "leaf": leaf,
                "printed_page": printed,
                "section": record["section"],
                "status": "source_ready",
                "translation_exists": False,
                "translation_path": f"content/translations/{ISSUE_ID}/leaves/leaf_{leaf:03d}.md",
                "review_exists": False,
                "review_path": f"content/translations/{ISSUE_ID}/reviews/leaf_{leaf:03d}.review.md",
                "qa_flags": record["flags"],
                "scan_url": f"https://archive.org/download/{ISSUE_ID}/page/n{leaf}_w500.jpg",
                "word_count": 0,
            }
        )
    status_path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in status_records)
    )


if __name__ == "__main__":
    main()
