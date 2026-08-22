#!/usr/bin/env python3
"""Initialize the 134-leaf Spring 1969 status ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ISSUE_ID = "wholeearthcatalo00unse_10"
ISSUE_ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ISSUE_ROOT / "status.jsonl"

SECTIONS = (
    (0, 3, "Front Matter"),
    (4, 18, "Understanding Whole Systems"),
    (19, 40, "Shelter and Land Use"),
    (41, 60, "Industry and Craft"),
    (61, 78, "Communications"),
    (79, 94, "Community"),
    (95, 108, "Nomadics"),
    (109, 126, "Learning"),
    (127, 133, "Back Matter"),
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

    records = []
    for leaf in range(134):
        records.append(
            {
                "leaf": leaf,
                "printed_page": None if leaf < 2 else leaf - 1,
                "section": section_for(leaf),
                "status": "pending",
                "translation_exists": False,
                "translation_path": (
                    f"content/translations/{ISSUE_ID}/leaves/"
                    f"leaf_{leaf:03d}.md"
                ),
                "review_exists": False,
                "review_path": (
                    f"content/translations/{ISSUE_ID}/reviews/"
                    f"leaf_{leaf:03d}.review.md"
                ),
                "qa_flags": [],
                "scan_url": (
                    f"https://archive.org/download/{ISSUE_ID}/page/"
                    f"n{leaf}_w500.jpg"
                ),
                "word_count": 0,
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
    print(f"initialized {len(records)} pending leaves in {STATUS_PATH}")


if __name__ == "__main__":
    main()
