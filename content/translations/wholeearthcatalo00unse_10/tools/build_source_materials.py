#!/usr/bin/env python3
"""Build verified, leaf-addressed OCR source packs for Spring 1969."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ISSUE_ID = "wholeearthcatalo00unse_10"
ISSUE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
DJVU_XML = REPO_ROOT / "_local" / "page_xml" / f"{ISSUE_ID}_djvu.xml"
SCANDATA_XML = REPO_ROOT / "_local" / "page_xml" / f"{ISSUE_ID}_scandata.xml"
OUTPUT_ROOT = ISSUE_ROOT / "_local" / "source_packs"


def parse_scandata(path: Path) -> list[dict[str, object]]:
    pages = []
    root = ET.parse(path).getroot()
    for page in root.findall(".//page"):
        if page.findtext("addToAccessFormats") == "false":
            continue
        pages.append(
            {
                "physical_leaf": int(page.attrib["leafNum"]),
                "page_type": page.findtext("pageType") or "",
                "printed_page": page.findtext("pageNumber"),
                "hand_side": page.findtext("handSide") or "",
                "source_image": page.findtext("origFileName") or "",
            }
        )
    return pages


def parse_ocr_object(obj: ET.Element) -> tuple[list[dict[str, object]], int]:
    lines = []
    word_count = 0
    for line in obj.findall(".//LINE"):
        words = []
        for word in line.findall("WORD"):
            text = (word.text or "").strip()
            if not text:
                continue
            words.append(
                {
                    "text": text,
                    "coords": word.attrib.get("coords", ""),
                }
            )
        if not words:
            continue
        word_count += len(words)
        lines.append(
            {
                "text": " ".join(str(word["text"]) for word in words),
                "words": words,
            }
        )
    return lines, word_count


def physical_leaf_from_object(obj: ET.Element) -> tuple[str, int]:
    page_param = obj.find("PARAM[@name='PAGE']")
    if page_param is None:
        raise ValueError("DjVu OBJECT is missing its PAGE parameter")
    canonical_object = page_param.attrib.get("value", "")
    match = re.search(r"_(\d+)\.djvu$", canonical_object)
    if match is None:
        raise ValueError(f"unrecognized DjVu PAGE value: {canonical_object!r}")
    return canonical_object, int(match.group(1))


def build_packs(write: bool) -> list[dict[str, object]]:
    objects = ET.parse(DJVU_XML).getroot().findall(".//OBJECT")
    scan_pages = parse_scandata(SCANDATA_XML)
    if len(objects) != len(scan_pages):
        raise SystemExit(
            f"mapping mismatch: {len(objects)} OCR objects, "
            f"{len(scan_pages)} access-format scan pages"
        )

    packs = []
    for access_leaf, (obj, scan) in enumerate(zip(objects, scan_pages, strict=True)):
        canonical_object, object_physical_leaf = physical_leaf_from_object(obj)
        if object_physical_leaf != scan["physical_leaf"]:
            raise ValueError(
                f"leaf n{access_leaf}: DjVu object points to physical "
                f"{object_physical_leaf}, scandata access sequence points to "
                f"{scan['physical_leaf']}"
            )
        lines, word_count = parse_ocr_object(obj)
        pack = {
            "issue_id": ISSUE_ID,
            "access_leaf": access_leaf,
            "canonical_object": canonical_object,
            **scan,
            "scan_url": (
                f"https://archive.org/download/{ISSUE_ID}/page/"
                f"n{access_leaf}_w500.jpg"
            ),
            "highres_scan_url": (
                f"https://archive.org/download/{ISSUE_ID}/page/"
                f"n{access_leaf}_w2000.jpg"
            ),
            "ocr_source": str(DJVU_XML.relative_to(REPO_ROOT)),
            "ocr_line_count": len(lines),
            "ocr_word_count": word_count,
            "ocr_lines": lines,
        }
        packs.append(pack)

        if write:
            OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
            path = OUTPUT_ROOT / f"leaf_{access_leaf:03d}.json"
            path.write_text(
                json.dumps(pack, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    if write:
        manifest = {
            "issue_id": ISSUE_ID,
            "access_leaf_count": len(packs),
            "first_access_leaf": packs[0]["access_leaf"],
            "last_access_leaf": packs[-1]["access_leaf"],
            "mapping_rule": (
                "DjVu object index equals public access leaf; each object maps "
                "to the same-position scandata page after excluding pages with "
                "addToAccessFormats=false."
            ),
            "leaves": [
                {
                    key: pack[key]
                    for key in (
                        "access_leaf",
                        "canonical_object",
                        "physical_leaf",
                        "page_type",
                        "printed_page",
                        "ocr_line_count",
                        "ocr_word_count",
                    )
                }
                for pack in packs
            ],
        }
        (OUTPUT_ROOT / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return packs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="validate the mapping without writing ignored source packs",
    )
    args = parser.parse_args()
    packs = build_packs(write=not args.verify_only)
    total_words = sum(int(pack["ocr_word_count"]) for pack in packs)
    print(
        json.dumps(
            {
                "issue_id": ISSUE_ID,
                "access_leaf_count": len(packs),
                "leaf_range": [
                    packs[0]["access_leaf"],
                    packs[-1]["access_leaf"],
                ],
                "physical_leaf_range": [
                    packs[0]["physical_leaf"],
                    packs[-1]["physical_leaf"],
                ],
                "ocr_word_count": total_words,
                "wrote_source_packs": not args.verify_only,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
