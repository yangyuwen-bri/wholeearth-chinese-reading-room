#!/usr/bin/env python3
"""Accept one leaf only after its concrete coverage review passes."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_release import PAGE_DESCRIPTION, REQUIRED_EVIDENCE, section, source_word_count


ROOT = Path(__file__).resolve().parent.parent
STATUS_PATH = ROOT / "status.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("leaf", type=int)
    parser.add_argument("--printed-page")
    args = parser.parse_args()

    leaf_path = ROOT / "leaves" / f"leaf_{args.leaf:03d}.md"
    review_path = ROOT / "reviews" / f"leaf_{args.leaf:03d}.review.md"
    leaf_text = leaf_path.read_text()
    review_text = review_path.read_text()
    final = section(leaf_text, "Final Translation")
    evidence = section(review_text, "Coverage Evidence")
    conclusion = re.search(
        r"^## Conclusion\s*\n\s*([^\n]+)", review_text, re.MULTILINE
    )
    if not conclusion or conclusion.group(1).strip() != "accepted":
        raise SystemExit("review conclusion is not accepted")
    if not evidence or any(label not in evidence for label in REQUIRED_EVIDENCE):
        raise SystemExit("review lacks concrete Coverage Evidence")
    if PAGE_DESCRIPTION.search(final):
        raise SystemExit("Final Translation contains summary/page-description language")

    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    row = next(row for row in rows if row["leaf"] == args.leaf)
    words = source_word_count(leaf_text, int(row.get("word_count") or 0))
    han = len(re.findall(r"[\u3400-\u9fff]", final))
    if words >= 800 and han / words < 0.35 and "Coverage exception:" not in evidence:
        raise SystemExit(f"possible summary drift: {han} Chinese chars / {words} OCR words")

    row["status"] = "accepted"
    if args.printed_page is not None:
        row["printed_page"] = args.printed_page
    row["qa_flags"] = [
        flag for flag in row.get("qa_flags", []) if flag != "coverage_review_required"
    ]
    STATUS_PATH.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    )
    print(f"accepted leaf {args.leaf:03d}: {han} Chinese chars / {words} OCR words")


if __name__ == "__main__":
    main()
