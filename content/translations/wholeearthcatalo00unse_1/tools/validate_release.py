#!/usr/bin/env python3
"""Reject Spring 1970 releases with missing coverage evidence or summary drift."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATUS_PATH = ROOT / "status.jsonl"
LEAF_DIR = ROOT / "leaves"
REVIEW_DIR = ROOT / "reviews"

REQUIRED_EVIDENCE = (
    "Source inventory:",
    "Translation coverage:",
    "Permitted omissions:",
)
SUMMARY_DRIFT = re.compile(
    r"本页(?:介绍|展示|聚焦|讨论|主要)|"
    r"这一页(?:介绍|展示|聚焦|讨论)|"
    r"(?:书评|评论)(?:介绍|认为|称|指出)|"
    r"文本(?:强调|指出|语气)|"
    r"文中(?:出现|提到)|"
    r"(?:选段|摘录)(?:引用|说明|指出|强调)|"
    r"(?:该页|全页|页面)(?:还|主要|包含|信息|文字|内容)|"
    r"(?:作为主框架|说明性翻译|核心要点|主题总结)|"
    r"正文节选自|"
    r"条目(?:介绍|概述)"
)
NO_OMISSION = re.compile(r"^(?:[-*]\s*)?(?:无|none\b|n/a\b)", re.IGNORECASE)
IRRECOVERABLE_SOURCE = re.compile(
    r"物理(?:裁掉|裁切|缺失)|不可恢复|无法(?:可靠)?辨认|"
    r"physically (?:cropped|absent)|irrecoverable|unreadable",
    re.IGNORECASE,
)


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def source_word_count(text: str, fallback: int) -> int:
    match = re.search(r"(?:OCR recovery:|OCR recovered)\s*([\d,]+)\s+words", text)
    return int(match.group(1).replace(",", "")) if match else fallback


def validate_issue(require_accepted: bool = True) -> list[str]:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    rows.sort(key=lambda row: row["leaf"])
    errors: list[str] = []
    reason_groups: dict[str, list[int]] = defaultdict(list)

    if [row["leaf"] for row in rows] != list(range(148)):
        errors.append("status.jsonl must contain contiguous leaves 000-147")

    for row in rows:
        leaf = row["leaf"]
        leaf_path = LEAF_DIR / f"leaf_{leaf:03d}.md"
        review_path = REVIEW_DIR / f"leaf_{leaf:03d}.review.md"
        if not leaf_path.exists() or not review_path.exists():
            errors.append(f"leaf {leaf:03d}: translation or review file missing")
            continue

        leaf_text = leaf_path.read_text()
        review_text = review_path.read_text()
        final = section(leaf_text, "Final Translation")
        omitted = section(leaf_text, "Omitted Bibliographic/Order Info")
        evidence = section(review_text, "Coverage Evidence")
        reasons = " ".join(section(review_text, "Reasons").split())
        required_fixes = section(review_text, "Required Fixes")
        conclusion = re.search(
            r"^## Conclusion\s*\n\s*([^\n]+)", review_text, re.MULTILINE
        )
        reason_groups[reasons].append(leaf)

        if require_accepted and row["status"] != "accepted":
            errors.append(f"leaf {leaf:03d}: status is {row['status']}, not accepted")
        if not final:
            errors.append(f"leaf {leaf:03d}: Final Translation is empty")
        if not omitted:
            errors.append(f"leaf {leaf:03d}: omission audit section is empty")
        elif not NO_OMISSION.search(omitted) and not IRRECOVERABLE_SOURCE.search(omitted):
            errors.append(
                f"leaf {leaf:03d}: accepted text records an omission without "
                "irrecoverable-source evidence"
            )
        if not evidence or any(label not in evidence for label in REQUIRED_EVIDENCE):
            errors.append(f"leaf {leaf:03d}: review lacks concrete Coverage Evidence")
        if not conclusion or conclusion.group(1).strip() != "accepted":
            errors.append(f"leaf {leaf:03d}: review conclusion is not accepted")
        accepted_claim = row["status"] == "accepted" or bool(
            conclusion and conclusion.group(1).strip() == "accepted"
        )
        if (
            accepted_claim
            and required_fixes
            and not re.fullmatch(r"-?\s*无[。.]?", required_fixes)
        ):
            errors.append(f"leaf {leaf:03d}: accepted review still contains required fixes")
        if SUMMARY_DRIFT.search(final):
            errors.append(f"leaf {leaf:03d}: reader text contains summary/page-description language")

        words = source_word_count(leaf_text, int(row.get("word_count") or 0))
        han = len(re.findall(r"[\u3400-\u9fff]", final))
        ratio = han / words if words else 1.0
        if words >= 800 and ratio < 0.35 and "Coverage exception:" not in evidence:
            errors.append(
                f"leaf {leaf:03d}: possible summary drift "
                f"({han} Chinese chars / {words} OCR words)"
            )

    for reasons, leaves in reason_groups.items():
        if reasons and len(leaves) >= 3:
            joined = ", ".join(f"{leaf:03d}" for leaf in leaves)
            errors.append(f"generic duplicate review reasons on leaves: {joined}")

    return errors


def main() -> None:
    errors = validate_issue()
    if errors:
        print(f"release blocked: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("release gate passed: 148 leaves have concrete coverage evidence")


if __name__ == "__main__":
    main()
