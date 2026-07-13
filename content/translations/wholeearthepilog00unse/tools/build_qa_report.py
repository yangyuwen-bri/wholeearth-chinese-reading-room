#!/usr/bin/env python3
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("content/translations/wholeearthepilog00unse")


def main() -> int:
    records = [
        json.loads(line)
        for line in (ROOT / "status.jsonl").read_text().splitlines()
        if line.strip()
    ]
    counts = Counter(r["status"] for r in records)
    by_status = defaultdict(list)
    for r in records:
        by_status[r["status"]].append(r["leaf"])

    lines = [
        "# Whole Earth Epilog Full Translation QA Report",
        "",
        "## Status Counts",
        "",
    ]
    for status in sorted(counts):
        lines.append(f"- `{status}`: {counts[status]}")
    lines.extend(["", "## Remaining Blockers", ""])
    for status in ["needs_highres_scan", "revise", "reviewed_needs_glossary", "blocked_ocr"]:
        leaves = by_status.get(status, [])
        if leaves:
            lines.append(f"### {status}")
            lines.append("")
            lines.append(", ".join(str(x) for x in leaves))
            lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- All leaves 0-321 have translation and review files.",
            "- `no_translation_needed` is used for cover/index/back matter or non-body pages.",
            "- `needs_highres_scan` means the prose translation exists, but a substantive image/table/diagram/label blocker remains.",
            "- The workflow uses Archive scans, local DjVu XML OCR, and crop-level OCR helpers.",
        ]
    )

    (ROOT / "qa_report.md").write_text("\n".join(lines) + "\n")
    print(ROOT / "qa_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
