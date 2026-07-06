#!/usr/bin/env python3
"""Build browser-loadable data for the Epilog page agent."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data/issue_agents/wholeearthepilog00unse"
OUT = ROOT / "content/maps/1974_epilog_agent_data.js"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> None:
    manifest = json.loads((BUNDLE / "manifest.json").read_text())
    eval_questions = json.loads((BUNDLE / "eval_questions.json").read_text())
    retrieval_units = load_jsonl(BUNDLE / "retrieval_units.jsonl")
    prompts = [
        question["question_zh"]
        for question in eval_questions
        if question["category"] in {"quote", "section", "bibliography", "navigation"}
    ][:8]
    data = {
        "schema_version": manifest["schema_version"],
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "issue_id": manifest["issue_id"],
        "title": manifest["title"],
        "record_counts": manifest["record_counts"],
        "prompts": prompts,
        "units": [
            {
                "unit_id": unit["unit_id"],
                "source_type": unit["source_type"],
                "source_record_id": unit["source_record_id"],
                "title": unit["title"],
                "section": unit.get("section"),
                "leaf_start": unit.get("leaf_start"),
                "leaf_end": unit.get("leaf_end"),
                "scan_urls": unit.get("scan_urls") or [],
                "text": unit["text"],
                "key_terms": unit.get("key_terms") or [],
                "qa_flags": unit.get("qa_flags") or [],
                "citation_hint": unit.get("citation_hint"),
            }
            for unit in retrieval_units
        ],
    }
    OUT.write_text("window.EPILOG_AGENT_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(json.dumps({"output": str(OUT), "units": len(data["units"]), "prompts": len(prompts)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
