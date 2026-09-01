#!/usr/bin/env python3
"""Draft one or more source-ready leaves with a local translation model.

The script deliberately stops at ``needs_highres_scan``. Scan comparison,
independent review, and final acceptance remain separate release gates.
"""

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

SYSTEM = """你是《全球概览》中文阅读室的忠实翻译员。你翻译的是 1971 年 3 月《The Last Supplement to The Whole Earth Catalog》的单个扫描页。

硬性规则：
1. 逐项、逐段翻译证据中的全部可恢复英文，不得总结、概述、合并或删节。
2. 必须保留标题、署名、引文、诗行、对话、价格、邮资、编号、页数、地址、表格项、表单字段、图片说明和有意义的标签。重复内容也不能压缩。
3. 不补写背景知识，不把页面改写成百科介绍，不写“本页介绍/右栏展示/正文节选自”之类页面描述。
4. OCR 明显损坏而无法可靠恢复的片段放进 uncertainty_notes，不猜测；不要把不确定占位符写进 final_translation。
5. 中文应自然可读，但原文的论证次序、语气、讽刺、粗话、犹疑和历史用语都要保留。
6. 作品名第一次出现写中文译名（English Original）；人名可保留英文并给常用中译。
7. 输出必须是严格 JSON，不要 Markdown 代码围栏，不要分析过程。
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "context_notes": {"type": "array", "items": {"type": "string"}},
        "glossary_updates": {"type": "array", "items": {"type": "string"}},
        "final_translation": {"type": "string"},
        "uncertainty_notes": {"type": "array", "items": {"type": "string"}},
        "self_critique": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "context_notes",
        "glossary_updates",
        "final_translation",
        "uncertainty_notes",
        "self_critique",
    ],
}


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def call_model(source_pack: str, leaf: int) -> dict[str, object]:
    tesseract_path = TESSERACT_ROOT / f"leaf_{leaf:03d}.txt"
    tesseract = tesseract_path.read_text(errors="ignore") if tesseract_path.exists() else "[not available]"
    prompt = f"""扫描页：access leaf n{leaf}。

下面先给出官方 Internet Archive DjVu XML 证据，再给出对 2734 像素宽高清扫描运行的独立 Tesseract OCR。两份 OCR 的行序都可能受多栏版式影响；第二份只用于补证，若冲突则不得猜测。请先识别独立文本单元，再完整翻译。final_translation 中可以用 `###` 分隔独立条目，但不要写页面说明或 QA 话语。

### 官方 DjVu XML
{source_pack}

### 高清扫描 Tesseract OCR
~~~text
{tesseract}
~~~
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
            "options": {
                "temperature": 0.1,
                "num_ctx": 32768,
                "num_predict": 12000,
            },
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


def replace_section(text: str, heading: str, body: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(heading)}\s*\n)(.*?)(?=\n## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if not pattern.search(text):
        raise RuntimeError(f"Missing section: {heading}")
    return pattern.sub(lambda match: f"{match.group(1)}\n{body.strip()}\n", text, count=1)


def render(path: Path, result: dict[str, object]) -> int:
    text = path.read_text()
    final = str(result["final_translation"]).strip()
    if len(final) < 20:
        raise RuntimeError(f"Model returned implausibly short translation for {path.name}")
    text = replace_section(text, "Context Notes", bullets(result["context_notes"], "无补充。"))
    text = replace_section(text, "Glossary Updates", bullets(result["glossary_updates"], "无。"))
    text = replace_section(text, "Final Translation", final)
    text = replace_section(text, "Omitted Bibliographic/Order Info", "- 无。")
    text = replace_section(
        text,
        "OCR / Uncertainty Notes",
        bullets(result["uncertainty_notes"], "官方 OCR 未见无法处理的残缺；仍须对照高清扫描。"),
    )
    text = replace_section(text, "Self Critique", bullets(result["self_critique"], "已逐项自检；待独立复核。"))
    path.write_text(text)
    return len(final)


def update_status(counts: dict[int, int]) -> None:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    for row in rows:
        leaf = int(row["leaf"])
        if leaf in counts:
            row["status"] = "needs_highres_scan"
            row["translation_exists"] = True
            row["word_count"] = counts[leaf]
    STATUS_PATH.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("leaves", nargs="+", type=int)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    counts: dict[int, int] = {}
    for leaf in args.leaves:
        path = PACKAGE / "leaves" / f"leaf_{leaf:03d}.md"
        text = path.read_text()
        current = section(text, "Final Translation")
        if current and not args.force:
            print(f"leaf {leaf:03d}: already drafted; skipped", flush=True)
            continue
        result = call_model(section(text, "Source Pack"), leaf)
        counts[leaf] = render(path, result)
        update_status(counts)
        print(f"leaf {leaf:03d}: drafted ({counts[leaf]} chars)", flush=True)


if __name__ == "__main__":
    main()
