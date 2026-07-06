#!/usr/bin/env python3
"""Serve the Whole Earth static site with a local LLM issue-agent API."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data/issue_agents/wholeearthepilog00unse"
DEFAULT_PORT = 8765


def load_env() -> None:
    for name in [".env.local", ".env"]:
        path = ROOT / name
        if not path.exists():
            continue
        for raw_line in path.read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def tokens(text: str) -> list[str]:
    lowered = text.lower()
    latin = re.findall(r"[a-z0-9][a-z0-9'._-]{1,}", lowered)
    cjk_runs = re.findall(r"[\u4e00-\u9fff]{2,}", lowered)
    cjk_pairs = []
    for run in cjk_runs:
        cjk_pairs.extend(run[index : index + 2] for index in range(max(0, len(run) - 1)))
    return latin + cjk_runs + cjk_pairs


def latin_phrases(text: str) -> list[str]:
    phrases = re.findall(r"[A-Za-z0-9][A-Za-z0-9'._-]*(?:\s+[A-Za-z0-9][A-Za-z0-9'._-]*)+", text)
    return [phrase.lower() for phrase in phrases if len(phrase.split()) >= 2]


def score_unit(question: str, question_tokens: set[str], unit: dict[str, Any]) -> float:
    title = unit.get("title") or ""
    title_lower = title.lower()
    haystack = "\n".join([title, unit.get("section") or "", unit.get("text") or "", " ".join(unit.get("key_terms") or [])]).lower()
    score = 0.0
    if question.lower() in haystack:
        score += 20
    for phrase in latin_phrases(question):
        if phrase in title_lower:
            score += 30
        elif phrase in haystack:
            score += 12
    for token in question_tokens:
        if token in title_lower:
            score += 3 + min(3, len(token) / 6)
        elif token in haystack:
            score += 1 + min(2, len(token) / 8)
    if unit.get("source_type") == "chapter":
        score *= 1.08
    if unit.get("source_type") == "bibliography":
        score *= 1.05
    return score


def retrieve(question: str, limit: int = 6) -> list[dict[str, Any]]:
    units = load_jsonl(BUNDLE / "retrieval_units.jsonl")
    question_tokens = set(tokens(question))
    ranked = []
    for unit in units:
        score = score_unit(question, question_tokens, unit)
        if score > 0:
            item = dict(unit)
            item["score"] = round(score, 3)
            ranked.append(item)
    ranked.sort(key=lambda item: (-item["score"], item["unit_id"]))
    return ranked[:limit]


def compact_context(units: list[dict[str, Any]]) -> str:
    blocks = []
    for index, unit in enumerate(units, 1):
        scan = (unit.get("scan_urls") or [""])[0]
        leaf = unit.get("leaf_start")
        leaf_end = unit.get("leaf_end")
        leaf_label = f"leaf {leaf}-{leaf_end}" if leaf and leaf_end and leaf_end != leaf else f"leaf {leaf or 'n/a'}"
        blocks.append(
            "\n".join(
                [
                    f"[{index}] {unit.get('title')} | {unit.get('source_type')} | {leaf_label}",
                    f"source_record_id: {unit.get('source_record_id')}",
                    f"scan_url: {scan}",
                    f"citation_hint: {unit.get('citation_hint')}",
                    (unit.get("text") or "")[:2200],
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)


def evidence_units(question: str, units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    phrases = latin_phrases(question)
    if not phrases:
        return units[:4]
    filtered = [
        unit
        for unit in units
        if any(phrase in f"{unit.get('title') or ''}\n{unit.get('text') or ''}".lower() for phrase in phrases)
    ]
    return (filtered or units)[:4]


def call_llm(question: str, context: str) -> str:
    api_key = os.environ.get("LLM_API_KEY")
    base_url = os.environ.get("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1").rstrip("/")
    model = os.environ.get("LLM_MODEL", "qwen3.7-plus")
    if not api_key:
        raise RuntimeError("LLM_API_KEY is not set")

    system_prompt = (BUNDLE / "system_prompt.md").read_text()
    user_prompt = f"""问题：{question}

只根据下面资料回答。回答要短，直接面向中文读者。必须给出 leaf；有 scan_url 时给出 scan_url。资料不足就说不足。不要使用 Markdown。

资料：
{context}
"""
    body: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }
    if os.environ.get("LLM_ENABLE_THINKING", "").lower() in {"true", "false"}:
        body["enable_thinking"] = os.environ["LLM_ENABLE_THINKING"].lower() == "true"

    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")
        raise RuntimeError(f"LLM API HTTP {error.code}: {detail[:500]}") from error
    return payload["choices"][0]["message"]["content"].strip()


def module_for_unit(unit: dict[str, Any] | None) -> str | None:
    if not unit:
        return None
    text = f"{unit.get('section') or ''} {unit.get('text') or ''}"
    patterns = [
        ("method", r"Front Matter|入口|Method"),
        ("systems", r"Whole Systems|整体系统|Bateson|Odum"),
        ("land", r"Land Use|土地使用"),
        ("shelter", r"Shelter|住所"),
        ("soft", r"Soft Technology|软技术"),
        ("craft", r"Craft|手艺"),
        ("community", r"Community|共同体"),
        ("nomadics", r"Nomadics|游牧"),
        ("communications", r"Communications|通信"),
        ("learning", r"Learning|学习"),
        ("business", r"Business|Index|出版业务|索引|封底"),
    ]
    for module, pattern in patterns:
        if re.search(pattern, text):
            return module
    return None


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self) -> None:
        if self.path.startswith("/api/"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_POST(self) -> None:
        if self.path != "/api/issue-agent":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            question = str(payload.get("question") or "").strip()
            if not question:
                raise ValueError("question is required")
            matches = retrieve(question)
            answer = call_llm(question, compact_context(matches))
            response = {
                "answer": answer,
                "evidence": [
                    {
                        "title": item.get("title"),
                        "source_type": item.get("source_type"),
                        "leaf_start": item.get("leaf_start"),
                        "leaf_end": item.get("leaf_end"),
                        "scan_url": (item.get("scan_urls") or [None])[0],
                        "source_record_id": item.get("source_record_id"),
                    }
                    for item in evidence_units(question, matches)
                ],
                "module": module_for_unit(matches[0] if matches else None),
            }
            self.send_json(200, response)
        except Exception as error:
            self.send_json(500, {"error": str(error)})

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    load_env()
    mimetypes.add_type("text/javascript", ".js")
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Serving http://{args.host}:{args.port}/content/maps/1974_epilog_access_atlas.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
