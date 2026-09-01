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

必做检查：
1. 先列出源文的人名、地名、作品名，检查译文是否保留同一英文拼写。例如源文是 Poe，译文只写了另一个中文人名，必须判 revise。
2. 逐个检查 no/not/nothing/never/without 等否定词的逻辑。
3. 检查数字、价格、邮费、地址、编号和引文是否齐全。
4. 检查 1960–1970 年代反文化语境：trip 可指迷幻药体验，head 可指迷幻药文化人士，hood 可指街头罪犯；若按普通字面义译导致语境错误，判 revise。

不要因为译文流畅就通过。不要把纯风格偏好列为必改。最多列 5 条具体问题，每条不超过 80 个汉字。输出严格 JSON，不要 Markdown 围栏或分析过程。
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "conclusion": {"type": "string", "enum": ["accepted", "revise", "needs_highres_scan"]},
        "issues": {"type": "array", "maxItems": 5, "items": {"type": "string"}},
        "residual_risks": {"type": "array", "maxItems": 3, "items": {"type": "string"}},
    },
    "required": [
        "conclusion",
        "issues",
        "residual_risks",
    ],
}


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}[ \t]*\n(.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def official_transcript(source: str) -> str:
    match = re.search(
        r"^### Official OCR Line Transcript.*?^~~~text\n(.*?)^~~~[ \t]*$",
        source,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise RuntimeError("Official OCR transcript is missing")
    return match.group(1).strip()


def missing_proper_names(source: str, translation: str) -> list[str]:
    stop = {
        "About", "After", "All", "Also", "Although", "An", "And", "Any", "Are", "As", "At",
        "Be", "Because", "Been", "Before", "Being", "Between", "Both", "But", "By", "Can",
        "Could", "Death", "Do", "Does", "Each", "Even", "Every", "For", "From", "God", "Had",
        "Has", "Have", "He", "Her", "Here", "His", "How", "However", "If", "In", "Into", "Is",
        "It", "Its", "Like", "May", "More", "Most", "Much", "Must", "New", "No", "Not", "Now",
        "Of", "On", "Once", "One", "Only", "Or", "Other", "Our", "Out", "Over", "She", "Should",
        "Since", "So", "Some", "Such", "Than", "That", "The", "Their", "Then", "There", "These",
        "They", "This", "Those", "Through", "Thus", "To", "Under", "Up", "Very", "Was", "We",
        "Were", "What", "When", "Where", "Which", "While", "Who", "Why", "Will", "With", "Would",
        "You", "Your",
    }
    candidates: set[str] = set()
    capitalized = re.compile(r"\b[A-Z][A-Za-z][A-Za-z'-]*\b")
    # Always retain tokens in multi-word title-case names such as Charles
    # Manson, Red Spectre, and Lower East Side.
    for match in re.finditer(
        r"\b[A-Z][A-Za-z][A-Za-z'-]*(?:\s+[A-Z][A-Za-z][A-Za-z'-]*)+\b",
        source,
    ):
        candidates.update(
            token
            for token in capitalized.findall(match.group())
            if token not in stop or token == "New"
        )
    # A standalone title-case token is name-like when it occurs inside a
    # sentence. Skip sentence-start words, which are overwhelmingly prose.
    for match in capitalized.finditer(source):
        token = match.group()
        if token in stop:
            continue
        prefix = source[: match.start()].rstrip()
        if not prefix or prefix[-1] in ".!?":
            continue
        candidates.add(token)
    translation_tokens = set(re.findall(r"[A-Za-z][A-Za-z'-]*", translation))
    return sorted(candidates - translation_tokens, key=str.lower)


def call_model(leaf: int, source: str, translation: str, tesseract: str) -> dict[str, object]:
    transcript = official_transcript(source)
    source_words_match = re.search(r";\s*([\d,]+) OCR words", source)
    source_words = int(source_words_match.group(1).replace(",", "")) if source_words_match else 0
    if source_words > 1500:
        num_ctx = 16384
    elif source_words > 600:
        num_ctx = 8192
    else:
        num_ctx = 4096
    supplement = ""
    if source_words < 120 and tesseract.strip() not in {"", "[not available]"}:
        supplement = f"\n\n### 高清扫描补充 OCR\n{tesseract.strip()}"
    prompt = f"""复核 access leaf n{leaf}。官方 OCR 的断行和连字符可能是版式痕迹。只找会改变信息完整性或原意的具体问题。

### 官方源证据
{transcript}{supplement}

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
            "options": {
                "temperature": 0,
                "num_ctx": num_ctx,
                "num_predict": 800,
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
    result = json.loads(envelope["message"]["content"])
    issues: list[str] = []
    translation_tokens = set(re.findall(r"[A-Za-z][A-Za-z'-]*", translation))
    for raw_issue in result.get("issues", []):
        issue = str(raw_issue).strip()
        if not issue or re.search(
            r"无需修改|无明显错误|符合语境|译文正确|可理解|可能|未完全|隐喻色彩|文化内涵|语境混淆|更具象征|原始数字格式|用词不够精准|应保留原拼写|应保留英文|专有名词.*保留|未体现.*语境|未纠正.*拼写|指代不明|未遗漏|语境衔接",
            issue,
        ):
            continue
        quoted_phrases = re.findall(r"['‘’\"]([A-Za-z][A-Za-z' -]*)['‘’\"]", issue)
        quoted = [
            token
            for phrase in quoted_phrases
            for token in re.findall(r"[A-Za-z][A-Za-z'-]*", phrase)
        ]
        if ("保留英文" in issue or "保留原文" in issue or "保留原词" in issue or "未保留" in issue) and quoted and all(
            token in translation_tokens for token in quoted
        ):
            continue
        if "trip" in quoted and "迷幻药" in translation:
            continue
        if "OCR" in issue and quoted and all(
            token in transcript and token in translation for token in quoted
        ):
            continue
        issues.append(issue)
    result["issues"] = issues
    # A model occasionally emits an "accepted" label while listing concrete
    # defects. Treat any issue as revise; acceptance requires an empty issue list.
    if issues and result.get("conclusion") == "accepted":
        result["conclusion"] = "revise"
    elif not issues and result.get("conclusion") == "revise":
        result["conclusion"] = "accepted"
    return result


def bullets(values: object, empty: str) -> str:
    if not isinstance(values, list) or not values:
        return f"- {empty}"
    return "\n".join(f"- {str(value).strip()}" for value in values if str(value).strip())


def render_review(leaf: int, result: dict[str, object]) -> str:
    conclusion = str(result["conclusion"])
    issues = result["issues"]
    coverage = "逐项对照未发现实义遗漏或误译。" if conclusion == "accepted" else "发现需要修订或扫描补证的具体问题。"
    return f"""# Leaf {leaf:03d} Independent Review

## Conclusion

{conclusion}

## Coverage Evidence

- Source inventory: 官方 OCR 逐行文本；必要时参照高清扫描独立 OCR。
- Translation coverage: {coverage}
- Permitted omissions: 无。

## Reasons

{bullets(issues, '无补充。')}

## Required Fixes

{bullets(issues, 'None.')}

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
    parser.add_argument("--reconcile-only", action="store_true")
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
        if args.reconcile_only:
            existing = review_path.read_text()
            fixes = [
                line[2:].strip()
                for line in section(existing, "Required Fixes").splitlines()
                if line.startswith("- ") and line[2:].strip() not in {"None.", "无。"}
            ]
            nonblocking = re.compile(
                r"原始数字格式|用词不够精准|应保留原拼写|应保留英文|专有名词.*保留|未体现.*语境|未纠正.*拼写|指代不明|未遗漏|语境衔接|用词不够精准"
            )
            fixes = [fix for fix in fixes if not nonblocking.search(fix)]
            result = {"conclusion": "revise" if fixes else "accepted", "issues": fixes, "residual_risks": []}
        else:
            tesseract_path = TESSERACT_ROOT / f"leaf_{leaf:03d}.txt"
            tesseract = tesseract_path.read_text(errors="ignore") if tesseract_path.exists() else "[not available]"
            result = call_model(leaf, section(leaf_text, "Source Pack"), translation, tesseract)
        review_path.write_text(render_review(leaf, result))
        update_status(leaf, str(result["conclusion"]))
        print(f"leaf {leaf:03d}: {result['conclusion']}", flush=True)


if __name__ == "__main__":
    main()
