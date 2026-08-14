#!/usr/bin/env python3
"""Reopen the Fall 1969 issue after the summary-drift release failure."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATUS_PATH = ROOT / "status.jsonl"


def main() -> None:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    for row in rows:
        row["status"] = "self_checked"
        flags = row.setdefault("qa_flags", [])
        if "coverage_review_required" not in flags:
            flags.append("coverage_review_required")
    STATUS_PATH.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    )
    print(f"reopened {len(rows)} leaves for scan-level coverage review")


if __name__ == "__main__":
    main()

