#!/usr/bin/env python3
"""Query a local issue-agent knowledge bundle.

This is a lightweight retrieval smoke-test for the per-issue agent data layer.
It does not call an LLM. A future chat runtime can use the same bundle files,
then pass retrieved records plus the issue `system_prompt.md` to the model.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AGENT_ROOT = ROOT / "data/issue_agents"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retrieve context from an issue-agent bundle.")
    parser.add_argument("query", help="Reader question or search phrase.")
    parser.add_argument("--issue", default="wholeearthepilog00unse", help="Internet Archive issue identifier.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of retrieval units to print.")
    parser.add_argument("--agent-root", type=Path, default=DEFAULT_AGENT_ROOT, help="Root directory for issue bundles.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON instead of text.")
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def tokens(text: str) -> list[str]:
    lowered = text.lower()
    latin = re.findall(r"[a-z0-9][a-z0-9'._-]{1,}", lowered)
    cjk = re.findall(r"[\u4e00-\u9fff]{2,}", lowered)
    cjk_pairs = []
    for item in cjk:
        cjk_pairs.extend(item[index : index + 2] for index in range(max(0, len(item) - 1)))
    return latin + cjk + cjk_pairs


def latin_phrases(text: str) -> list[str]:
    phrases = re.findall(r"[A-Za-z0-9][A-Za-z0-9'._-]*(?:\s+[A-Za-z0-9][A-Za-z0-9'._-]*)+", text)
    return [phrase.lower() for phrase in phrases if len(phrase.split()) >= 2]


def score_unit(query: str, query_tokens: set[str], unit: dict[str, Any]) -> float:
    title = unit.get("title") or ""
    haystack = "\n".join(
        [
            title,
            unit.get("section") or "",
            unit.get("text") or "",
            " ".join(unit.get("key_terms") or []),
        ]
    ).lower()
    title_lower = title.lower()
    score = 0.0
    if query.lower() in haystack:
        score += 20.0
    for phrase in latin_phrases(query):
        if phrase in title_lower:
            score += 30.0
        elif phrase in haystack:
            score += 12.0
    for token in query_tokens:
        if token in title_lower:
            score += 3.0 + min(3.0, len(token) / 6)
        elif token in haystack:
            score += 1.0 + min(2.0, len(token) / 8)
    if unit.get("source_type") == "chapter":
        score *= 1.08
    if unit.get("source_type") == "bibliography":
        score *= 1.05
    return score


def retrieve(bundle_dir: Path, query: str, limit: int) -> list[dict[str, Any]]:
    units = load_jsonl(bundle_dir / "retrieval_units.jsonl")
    query_tokens = set(tokens(query))
    ranked = []
    for unit in units:
        score = score_unit(query, query_tokens, unit)
        if score > 0:
            ranked.append((score, unit))
    ranked.sort(key=lambda item: (-item[0], item[1]["unit_id"]))
    results = []
    for score, unit in ranked[:limit]:
        item = dict(unit)
        item["score"] = round(score, 3)
        results.append(item)
    return results


def compact(text: str, limit: int = 700) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def print_text(issue: str, query: str, results: list[dict[str, Any]]) -> None:
    print(f"Issue: {issue}")
    print(f"Query: {query}")
    print(f"Matches: {len(results)}")
    for index, result in enumerate(results, 1):
        print()
        print(f"## {index}. {result['title']} [{result['source_type']}] score={result['score']}")
        print(f"- unit_id: {result['unit_id']}")
        print(f"- source_record_id: {result['source_record_id']}")
        print(f"- section: {result.get('section') or 'n/a'}")
        print(f"- leaf: {result.get('leaf_start') or 'n/a'}-{result.get('leaf_end') or result.get('leaf_start') or 'n/a'}")
        if result.get("scan_urls"):
            print(f"- scan: {result['scan_urls'][0]}")
        print(f"- citation: {result.get('citation_hint') or 'n/a'}")
        print()
        print(compact(result.get("text") or ""))


def main() -> None:
    args = parse_args()
    bundle_dir = args.agent_root / args.issue
    if not bundle_dir.exists():
        raise SystemExit(f"Bundle not found: {bundle_dir}")
    results = retrieve(bundle_dir, args.query, args.limit)
    if args.json:
        print(json.dumps({"issue": args.issue, "query": args.query, "results": results}, ensure_ascii=False, indent=2))
    else:
        print_text(args.issue, args.query, results)


if __name__ == "__main__":
    main()
