#!/usr/bin/env python3
"""Synchronize the Fall 1969 release status from leaf reviews."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATUS_PATH = ROOT / "status.jsonl"
LEAF_DIR = ROOT / "leaves"
REVIEW_DIR = ROOT / "reviews"


def review_conclusion(path: Path) -> str:
    match = re.search(
        r"^## Conclusion\s*\n\s*([^\n]+)",
        path.read_text(),
        re.MULTILINE,
    )
    if not match:
        raise ValueError(f"missing review conclusion: {path}")
    return match.group(1).strip()


def main() -> None:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    rows.sort(key=lambda row: row["leaf"])
    if [row["leaf"] for row in rows] != list(range(132)):
        raise ValueError("status.jsonl must contain exactly leaves 000-131")

    for row in rows:
        leaf = row["leaf"]
        translation = LEAF_DIR / f"leaf_{leaf:03d}.md"
        review = REVIEW_DIR / f"leaf_{leaf:03d}.review.md"
        if not translation.exists() or not review.exists():
            raise FileNotFoundError(f"missing leaf or review for {leaf:03d}")
        conclusion = review_conclusion(review)
        if conclusion != "accepted":
            raise ValueError(f"leaf {leaf:03d} is not accepted: {conclusion}")
        row["status"] = conclusion
        row["translation_exists"] = True
        row["review_exists"] = True
        row["qa_flags"] = [flag for flag in row.get("qa_flags", []) if flag != "scan_required"]

    STATUS_PATH.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    )
    print("synchronized 132 accepted leaves")


if __name__ == "__main__":
    main()
