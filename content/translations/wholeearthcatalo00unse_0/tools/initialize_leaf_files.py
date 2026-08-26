#!/usr/bin/env python3
"""Create source-ready translation and review files for Fall 1970."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ISSUE_ID = "wholeearthcatalo00unse_0"
ISSUE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACK_ROOT = ISSUE_ROOT / "_local" / "source_packs"
LEAF_ROOT = ISSUE_ROOT / "leaves"
REVIEW_ROOT = ISSUE_ROOT / "reviews"


def printed_page_label(value: object) -> str:
    return "none" if value in {None, ""} else str(value)


def leaf_text(pack: dict[str, object]) -> str:
    leaf = int(pack["access_leaf"])
    transcript = "\n".join(
        str(line["text"]) for line in pack["ocr_lines"]  # type: ignore[index]
    )
    return f"""# Leaf {leaf:03d} Translation

## Source Pack

- Issue ID: `{ISSUE_ID}`
- Access leaf: `n{leaf}`; canonical physical scan leaf: `{pack['physical_leaf']}` (`{pack['canonical_object']}`).
- Printed page: `{printed_page_label(pack['printed_page'])}`; page type: `{pack['page_type']}`; hand side: `{pack['hand_side']}`.
- Scan URL: {pack['scan_url']}
- High-resolution scan URL: {pack['highres_scan_url']}
- OCR source: official Internet Archive DjVu XML at `{pack['ocr_source']}`; {pack['ocr_word_count']} OCR words / {pack['ocr_line_count']} OCR lines. No supplemental OCR used.
- Scan verification: required before orchestrator acceptance.

### Official OCR Line Transcript

The following is source evidence only. It preserves official OCR line order
and errors; it is not an approved reading order or a translation.

~~~text
{transcript}
~~~

## Context Notes

- Source pack generated from the verified public-access/DjVu/scandata mapping.
- Identify every visible entry, excerpt, caption, diagram, table, signature,
  and meaningful order/access field against the scan before translation.
- Do not treat OCR line order as page reading order on multi-column layouts.

## Glossary Updates


## Final Translation


## Omitted Bibliographic/Order Info

- None recorded at source-preparation stage.

## OCR / Uncertainty Notes

- Translation and high-resolution scan review pending.

## Self Critique

- Pending translation.
"""


def review_text(pack: dict[str, object]) -> str:
    leaf = int(pack["access_leaf"])
    return f"""# Leaf {leaf:03d} Independent Review

## Conclusion

source_ready

## Coverage Evidence

- Source inventory: pending translation and scan-backed inventory.
- Translation coverage: pending.
- Permitted omissions: pending.

## Reasons

- Official OCR source pack is available; translation and independent review
  have not yet been completed.

## Required Fixes

- Complete full translation and scan-backed independent review.

## Residual Risks

- Multi-column reading order, small type, captions, diagrams, tables, and OCR
  errors remain unverified until the high-resolution scan pass.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace existing source-ready skeletons",
    )
    args = parser.parse_args()

    manifest_path = SOURCE_PACK_ROOT / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(
            "source packs are missing; run tools/build_source_materials.py first"
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("access_leaf_count") != 148:
        raise SystemExit("source-pack manifest must contain 148 access leaves")

    LEAF_ROOT.mkdir(parents=True, exist_ok=True)
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    written = 0
    for leaf in range(148):
        pack = json.loads(
            (SOURCE_PACK_ROOT / f"leaf_{leaf:03d}.json").read_text(
                encoding="utf-8"
            )
        )
        paths = (
            (LEAF_ROOT / f"leaf_{leaf:03d}.md", leaf_text(pack)),
            (REVIEW_ROOT / f"leaf_{leaf:03d}.review.md", review_text(pack)),
        )
        for path, content in paths:
            if path.exists() and not args.force:
                raise SystemExit(
                    f"{path} already exists; pass --force only for untouched "
                    "source-ready skeletons"
                )
            path.write_text(content, encoding="utf-8")
            written += 1
    print(f"initialized {written} source-ready leaf and review files")


if __name__ == "__main__":
    main()
