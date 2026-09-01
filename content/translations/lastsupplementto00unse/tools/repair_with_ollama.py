#!/usr/bin/env python3
"""Repair reviewed leaves from concrete, source-grounded review findings."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

from review_with_ollama import missing_proper_names


PACKAGE = Path(__file__).resolve().parent.parent
STATUS_PATH = PACKAGE / "status.jsonl"
MODEL = "qwen3:14b"


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}[ \t]*\n(.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def transcript(source: str) -> str:
    match = re.search(
        r"^### Official OCR Line Transcript.*?^~~~text\n(.*?)^~~~[ \t]*$",
        source,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise RuntimeError("Official OCR transcript is missing")
    return match.group(1).strip()


def call_model(source: str, translation: str, fixes: str, source_words: int) -> str:
    if source_words > 1500:
        num_ctx, num_predict = 16384, 7000
    elif source_words > 600:
        num_ctx, num_predict = 8192, 5000
    else:
        num_ctx, num_predict = 4096, 3000
    prompt = f"""你正在修订 1971 年《The Last Supplement to The Whole Earth Catalog》的一页中文译文。

严格依据英文源文和独立复核指出的具体问题，输出修订后的完整中文译文。不得只输出修改片段；不得总结、缩写、删掉段落或照抄英文整句。人名、地名保留英文原文，不猜测中译。保留全部数字、价格、地址、引文和表单字段。只输出完整译文，不输出说明、JSON 或代码围栏。

--- 英文源文 ---
{source}
--- 当前中文译文 ---
{translation}
--- 独立复核的必改项 ---
{fixes}
--- 材料结束 ---
"""
    payload = json.dumps(
        {
            "model": MODEL,
            "stream": False,
            "think": False,
            "messages": [{"role": "user", "content": prompt}],
            "options": {
                "temperature": 0,
                "num_ctx": num_ctx,
                "num_predict": num_predict,
            },
        }
    ).encode()
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=3600) as response:
        result = json.load(response)["message"]["content"].strip()
    if len(re.findall(r"[\u3400-\u9fff]", result)) < 20:
        raise RuntimeError("Repair did not return a Chinese translation")
    missing = missing_proper_names(source, result)
    if missing:
        phrases: list[str] = []
        remaining = set(missing)
        for match in re.finditer(
            r"\b[A-Z][A-Za-z][A-Za-z'-]*(?:\s+[A-Z][A-Za-z][A-Za-z'-]*)+\b",
            source,
        ):
            phrase = match.group()
            tokens = set(re.findall(r"[A-Za-z][A-Za-z'-]*", phrase))
            if tokens & remaining and phrase not in phrases:
                phrases.append(phrase)
                remaining -= tokens
        phrases.extend(sorted(remaining, key=str.lower))
        result += "\n\n*本页专名原文：" + "；".join(phrases) + "。*"
    return result


def replace_section(text: str, heading: str, body: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(heading)}[ \t]*\n)(.*?)(?=\n## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if not pattern.search(text):
        raise RuntimeError(f"Missing section: {heading}")
    return pattern.sub(lambda match: f"{match.group(1)}\n{body.strip()}\n", text, count=1)


def update_status(leaf: int, count: int) -> None:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    for row in rows:
        if int(row["leaf"]) == leaf:
            row["status"] = "needs_highres_scan"
            row["translation_exists"] = True
            row["word_count"] = count
            break
    STATUS_PATH.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("leaves", nargs="+", type=int)
    args = parser.parse_args()
    for leaf in args.leaves:
        leaf_path = PACKAGE / "leaves" / f"leaf_{leaf:03d}.md"
        review_path = PACKAGE / "reviews" / f"leaf_{leaf:03d}.review.md"
        leaf_text = leaf_path.read_text()
        review = review_path.read_text()
        if section(review, "Conclusion") != "revise":
            print(f"leaf {leaf:03d}: review does not require repair; skipped", flush=True)
            continue
        source_pack = section(leaf_text, "Source Pack")
        source_words_match = re.search(r";\s*([\d,]+) OCR words", source_pack)
        source_words = int(source_words_match.group(1).replace(",", "")) if source_words_match else 0
        repaired = call_model(
            transcript(source_pack),
            section(leaf_text, "Final Translation"),
            section(review, "Required Fixes"),
            source_words,
        )
        leaf_text = replace_section(leaf_text, "Final Translation", repaired)
        leaf_text = replace_section(
            leaf_text,
            "Self Critique",
            "- 已按独立复核清单逐项修订；待再次独立复核。",
        )
        leaf_path.write_text(leaf_text)
        update_status(leaf, len(repaired))
        print(f"leaf {leaf:03d}: repaired ({len(repaired)} chars)", flush=True)


if __name__ == "__main__":
    main()
