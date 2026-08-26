#!/usr/bin/env python3
"""Initialize the 148-leaf Fall 1970 status ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ISSUE_ID = "wholeearthcatalo00unse_0"
ISSUE_ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ISSUE_ROOT / "status.jsonl"
SOURCE_PACK_ROOT = ISSUE_ROOT / "_local" / "source_packs"

SECTIONS = (
    (0, 4, "Front Matter"),
    (5, 18, "Whole Systems"),
    (19, 42, "Shelter and Land Use"),
    (43, 62, "Community"),
    (63, 82, "Communications"),
    (83, 102, "Industry and Craft"),
    (103, 120, "Nomadics"),
    (121, 143, "Learning"),
    (144, 147, "Back Matter"),
)


def section_for(leaf: int) -> str:
    for start, end, section in SECTIONS:
        if start <= leaf <= end:
            return section
    raise ValueError(f"leaf outside verified issue range: {leaf}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing non-template ledger",
    )
    args = parser.parse_args()

    if STATUS_PATH.exists() and not args.force:
        current = STATUS_PATH.read_text(encoding="utf-8")
        if "<issue_id>" not in current:
            raise SystemExit(
                f"{STATUS_PATH} is already initialized; pass --force only if "
                "you intend to reset every leaf to pending"
            )

    manifest_path = SOURCE_PACK_ROOT / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(
            "source packs are missing; run tools/build_source_materials.py first"
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("access_leaf_count") != 148:
        raise SystemExit("source-pack manifest must contain 148 access leaves")

    records = []
    for leaf in range(148):
        pack = json.loads(
            (SOURCE_PACK_ROOT / f"leaf_{leaf:03d}.json").read_text(
                encoding="utf-8"
            )
        )
        flags = []
        if pack["page_type"] in {"Cover", "Copyright", "Contents", "Title"}:
            flags.append("cover_or_back_matter" if leaf in {0, 147} else "layout_risk")
        elif int(pack["ocr_word_count"]) >= 500:
            flags.append("layout_risk")
        if int(pack["ocr_word_count"]) < 50:
            flags.append("ocr_sparse")
        records.append(
            {
                "leaf": leaf,
                "printed_page": pack["printed_page"],
                "section": section_for(leaf),
                "status": "source_ready",
                "translation_exists": True,
                "translation_path": (
                    f"content/translations/{ISSUE_ID}/leaves/"
                    f"leaf_{leaf:03d}.md"
                ),
                "review_exists": True,
                "review_path": (
                    f"content/translations/{ISSUE_ID}/reviews/"
                    f"leaf_{leaf:03d}.review.md"
                ),
                "qa_flags": flags,
                "scan_url": pack["scan_url"],
                "word_count": pack["ocr_word_count"],
            }
        )

    STATUS_PATH.write_text(
        "\n".join(
            json.dumps(record, ensure_ascii=False, separators=(",", ":"))
            for record in records
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"initialized {len(records)} source-ready leaves in {STATUS_PATH}")


if __name__ == "__main__":
    main()
