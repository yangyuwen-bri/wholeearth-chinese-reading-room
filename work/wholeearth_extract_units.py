#!/usr/bin/env python3
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work" / "wholeearth"
OUT = ROOT / "outputs"
TEXT = WORK / "wholeearthsoftwa00unse_3_djvu.txt"


def log(msg: str) -> None:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S %Z')}] {msg}", flush=True)


SECTION_LINES = [
    ("Front Matter", 1, 4799),
    ("Playing", 4800, 8350),
    ("Writing", 8351, 12080),
    ("Analyzing", 12081, 15060),
    ("Organizing", 15061, 18700),
    ("Accounting", 18701, 21820),
    ("Managing", 21821, 24970),
    ("Drawing", 24971, 28800),
    ("Telecommunicating", 28801, 33250),
    ("Programming", 33251, 37150),
    ("Learning", 37151, 40750),
    ("Etc.", 40751, 43800),
    ("Indexes and Supplement", 43801, 999999),
]


def normalize(line: str) -> str:
    line = re.sub(r"\s+", " ", line.strip())
    return line


def is_heading(line: str) -> bool:
    if not line or len(line) < 4 or len(line) > 90:
        return False
    if re.search(r"[@$]{2,}|https?://|^\d+$", line):
        return False
    letters = re.findall(r"[A-Za-z]", line)
    if len(letters) < 4:
        return False
    upper = sum(1 for c in letters if c.isupper())
    ratio = upper / len(letters)
    # Product/title headings in this OCR are mostly all caps, but allow title questions.
    return ratio >= 0.72 or line.endswith("?")


def main():
    round_id = sys.argv[1] if len(sys.argv) > 1 else "002"
    log(f"start round={round_id}")
    lines = TEXT.read_text(encoding="utf-8", errors="replace").splitlines()
    log(f"loaded lines={len(lines)}")
    units = []
    for section, start, end in SECTION_LINES:
        seen = set()
        section_units = []
        for idx in range(start - 1, min(end, len(lines))):
            line = normalize(lines[idx])
            if not is_heading(line):
                continue
            key = re.sub(r"[^A-Z0-9? ]", "", line.upper())
            if key in seen:
                continue
            seen.add(key)
            section_units.append({"line": idx + 1, "title": line})
        units.append({"section": section, "candidate_count": len(section_units), "candidates": section_units[:120]})
        log(f"{section}: candidates={len(section_units)}")
    out_json = OUT / "whole_earth_software_catalog_1985_unit_candidates.json"
    out_md = OUT / "whole_earth_software_catalog_1985_unit_candidates.md"
    out_json.write_text(json.dumps(units, ensure_ascii=False, indent=2), encoding="utf-8")
    md = ["# Whole Earth Software Catalog 2.0 单元候选", ""]
    for section in units:
        md.append(f"## {section['section']} ({section['candidate_count']})")
        for item in section["candidates"]:
            md.append(f"- L{item['line']}: {item['title']}")
        md.append("")
    out_md.write_text("\n".join(md), encoding="utf-8")
    log(f"wrote {out_json}")
    log(f"wrote {out_md}")
    log("done")


if __name__ == "__main__":
    main()
