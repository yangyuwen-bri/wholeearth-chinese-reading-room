#!/usr/bin/env python3
"""Release gate for the March 1971 Chinese translation package."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATUS_PATH = ROOT / "status.jsonl"
LEAF_DIR = ROOT / "leaves"
REVIEW_DIR = ROOT / "reviews"
EXPECTED_LEAVES = 132

REQUIRED_EVIDENCE = ("Translation coverage:", "Permitted omissions:")
SUMMARY_DRIFT = re.compile(
    r"^(?:本页|这一页)(?:主要)?(?:介绍|展示|聚焦|讨论|概述|总结)"
    r"|^正文节选自"
    r"|^\[(?:本页|页面|正文).*(?:概述|总结|简介)"
    r"|^［(?:本页|页面|正文).*(?:概述|总结|简介)",
    re.MULTILINE,
)
UNRESOLVED_PLACEHOLDER = re.compile(
    r"［[^］]*(?:字形不清|姓名不清|待高分辨率|待扫描|无法辨认)[^］]*］"
)


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def final_translation(text: str) -> str:
    marker = "## Final Translation\n"
    end_marker = "## Omitted Bibliographic"
    if marker not in text or end_marker not in text:
        return ""
    return text.split(marker, 1)[1].split(end_marker, 1)[0]


def final_character_count(text: str) -> int:
    return len(final_translation(text))


def ocr_word_count(text: str) -> int:
    match = re.search(r";\s*([\d,]+) OCR words", text)
    return int(match.group(1).replace(",", "")) if match else 0


def validate_issue() -> list[str]:
    rows = [
        json.loads(line)
        for line in STATUS_PATH.read_text().splitlines()
        if line.strip()
    ]
    rows.sort(key=lambda row: row["leaf"])
    errors: list[str] = []

    if [row["leaf"] for row in rows] != list(range(EXPECTED_LEAVES)):
        errors.append("status.jsonl must contain contiguous leaves 000-131")

    for row in rows:
        leaf = row["leaf"]
        leaf_path = LEAF_DIR / f"leaf_{leaf:03d}.md"
        review_path = REVIEW_DIR / f"leaf_{leaf:03d}.review.md"
        if not leaf_path.exists() or not review_path.exists():
            errors.append(f"leaf {leaf:03d}: translation or review file missing")
            continue

        leaf_text = leaf_path.read_text()
        review_text = review_path.read_text()
        final = final_translation(leaf_text)
        evidence = section(review_text, "Coverage Evidence")
        required_fixes = section(review_text, "Required Fixes")
        conclusion = re.search(
            r"^## Conclusion\s*\n\s*([^\n]+)", review_text, re.MULTILINE
        )

        if row["status"] != "accepted":
            errors.append(f"leaf {leaf:03d}: status is {row['status']}, not accepted")
        if not final:
            errors.append(f"leaf {leaf:03d}: Final Translation is empty")
        has_inventory = "Source inventory:" in evidence or "Visual inventory:" in evidence
        if (
            not evidence
            or not has_inventory
            or any(label not in evidence for label in REQUIRED_EVIDENCE)
        ):
            errors.append(f"leaf {leaf:03d}: review lacks concrete coverage evidence")
        if not conclusion or conclusion.group(1).strip() != "accepted":
            errors.append(f"leaf {leaf:03d}: review conclusion is not accepted")
        if required_fixes and not re.match(
            r"^-?\s*(?:无|None)(?:\b|[。.])",
            required_fixes,
            re.IGNORECASE,
        ):
            errors.append(f"leaf {leaf:03d}: accepted review still has required fixes")
        if SUMMARY_DRIFT.search(final):
            errors.append(f"leaf {leaf:03d}: reader text contains page-summary language")
        if UNRESOLVED_PLACEHOLDER.search(final):
            errors.append(f"leaf {leaf:03d}: reader text contains unresolved placeholder")

        actual_count = final_character_count(leaf_text)
        recorded_count = int(row.get("word_count") or 0)
        if actual_count != recorded_count:
            errors.append(
                f"leaf {leaf:03d}: status character count {recorded_count} "
                f"does not match translation {actual_count}"
            )

        source_words = ocr_word_count(leaf_text)
        if source_words >= 800 and actual_count / source_words < 1.0:
            errors.append(
                f"leaf {leaf:03d}: possible summary drift "
                f"({actual_count} translation chars / {source_words} OCR words)"
            )

    return errors


def main() -> None:
    errors = validate_issue()
    if errors:
        print(f"release blocked: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("release gate passed: 132 leaves are complete, reviewed, and accepted")


if __name__ == "__main__":
    main()
