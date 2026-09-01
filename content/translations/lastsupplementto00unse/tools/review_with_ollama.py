#!/usr/bin/env python3
"""Run a fresh, source-grounded fidelity review over drafted leaves."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent.parent
STATUS_PATH = PACKAGE / "status.jsonl"
TESSERACT_ROOT = Path("/private/tmp/lastsupplementto00unse-tesseract")
MODEL = "qwen3:14b"

SYSTEM = """你是独立的《全球概览》中文翻译复核员。你没有参与初译。请把源 OCR 与中文译文逐项比对，首要检查遗漏、总结性改写、误译、OCR 猜测、拆栏顺序错误和交易信息缺失。

判定标准：
- accepted：每个可恢复的正文段落、标题、署名、引文、诗行、对话、价格、编号、地址、名单项、表格项、说明和标签都在译文中出现；没有以概述代替原文。
- revise：发现任何可具体指出的遗漏、压缩、错译、添加或顺序错误。
- needs_highres_scan：两套 OCR 冲突到无法判断，或明显存在未被两套 OCR 恢复的可见小字/图表标签。

不要因为译文流畅就通过。不要把纯风格偏好列为必改。输出严格 JSON，不要 Markdown 围栏或分析过程。
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "conclusion": {"type": "string", "enum": ["accepted", "revise", "needs_highres_scan"]},
        "source_inventory": {"type": "array", "items": {"type": "string"}},
        "translation_coverage": {"type": "string"},
        "permitted_omissions": {"type": "string"},
        "reasons": {"type": "array", "items": {"type": "string"}},
        "required_fixes": {"type": "array", "items": {"type": "string"}},
        "residual_risks": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "conclusion",
        "source_inventory",
        "translation_coverage",
        "permitted_omissions",
        "reasons",
        "required_fixes",
        "residual_risks",
    ],
}


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def call_model(leaf: int, source: str, translation: str, tesseract: str) -> dict[str, object]:
    prompt = f"""复核 access leaf n{leaf}。官方 OCR 与高清扫描 Tesseract OCR 可能各有错误；共同出现的文字是强证据，差异必须谨慎处理。

### 官方源证据
{source}

### 高清扫描 Tesseract OCR
~~~text
{tesseract}
~~~

### 待复核中文译文
{translation}
"""
    payload = json.dumps(
        {
            "model": MODEL,
            "stream": False,
            "think": False,
            "format": SCHEMA,
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt},
            ],
            "options": {"temperature": 0, "num_ctx": 32768, "num_predict": 2500},
        }
    ).encode()
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=3600) as response:
        envelope = json.load(response)
    return json.loads(envelope["message"]["content"])


def bullets(values: object, empty: str) -> str:
    if not isinstance(values, list) or not values:
        return f"- {empty}"
    return "\n".join(f"- {str(value).strip()}" for value in values if str(value).strip())


def render_review(leaf: int, result: dict[str, object]) -> str:
    return f"""# Leaf {leaf:03d} Independent Review

## Conclusion

{result['conclusion']}

## Coverage Evidence

- Source inventory: {'; '.join(str(value).strip() for value in result['source_inventory'])}
- Translation coverage: {result['translation_coverage']}
- Permitted omissions: {result['permitted_omissions']}

## Reasons

{bullets(result['reasons'], '无补充。')}

## Required Fixes

{bullets(result['required_fixes'], 'None.')}

## Residual Risks

{bullets(result['residual_risks'], 'None.')}
"""


def update_status(leaf: int, conclusion: str) -> None:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    for row in rows:
        if int(row["leaf"]) == leaf:
            row["review_exists"] = True
            row["status"] = conclusion
            break
    STATUS_PATH.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("leaves", nargs="+", type=int)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    for leaf in args.leaves:
        review_path = PACKAGE / "reviews" / f"leaf_{leaf:03d}.review.md"
        if review_path.exists() and not args.force:
            print(f"leaf {leaf:03d}: already reviewed; skipped", flush=True)
            continue
        leaf_text = (PACKAGE / "leaves" / f"leaf_{leaf:03d}.md").read_text()
        translation = section(leaf_text, "Final Translation")
        if not translation:
            raise RuntimeError(f"leaf {leaf:03d}: translation is empty")
        tesseract_path = TESSERACT_ROOT / f"leaf_{leaf:03d}.txt"
        tesseract = tesseract_path.read_text(errors="ignore") if tesseract_path.exists() else "[not available]"
        result = call_model(leaf, section(leaf_text, "Source Pack"), translation, tesseract)
        review_path.write_text(render_review(leaf, result))
        update_status(leaf, str(result["conclusion"]))
        print(f"leaf {leaf:03d}: {result['conclusion']}", flush=True)


if __name__ == "__main__":
    main()
