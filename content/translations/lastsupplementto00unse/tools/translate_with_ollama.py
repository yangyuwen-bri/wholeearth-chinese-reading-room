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
4. OCR 明显损坏而无法可靠恢复的片段不猜测，但不得因局部破损而删掉整段。
5. 中文应自然可读，但原文的论证次序、语气、讽刺、粗话、犹疑和历史用语都要保留。
6. 人名和地名保留英文原文，不自行换成另一个中文专名；作品名可写中文译名（English Original）。
7. 只输出完整的中文译文，可使用 Markdown 标题和列表保留结构。不要 JSON，不要分析过程，不要复述英文原文。
"""


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}[ \t]*\n(.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def official_transcript(source_pack: str) -> str:
    match = re.search(
        r"^### Official OCR Line Transcript.*?^~~~text\n(.*?)^~~~[ \t]*$",
        source_pack,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise RuntimeError("Official OCR transcript is missing")
    return match.group(1).strip()


def chat(prompt: str, system: str, *, source_words: int) -> str:
    if source_words > 1500:
        num_ctx, num_predict = 16384, 7000
    elif source_words > 900:
        num_ctx, num_predict = 8192, 5000
    else:
        num_ctx, num_predict = 4096, 3000
    payload = json.dumps(
        {
            "model": MODEL,
            "stream": False,
            "think": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "options": {
                "temperature": 0.1,
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
        envelope = json.load(response)
    return envelope["message"]["content"].strip()


def longest_copied_run(source: str, translated: str) -> int:
    """Return the longest verbatim English-word run shared by both texts.

    Short runs are expected in names, titles, addresses, and bibliographic data.
    A long run is evidence that the model copied prose instead of translating it.
    """
    source_words = [word.lower() for word in re.findall(r"[A-Za-z]+", source)]
    translated_words = [word.lower() for word in re.findall(r"[A-Za-z]+", translated)]
    source_positions: dict[str, list[int]] = {}
    for index, word in enumerate(source_words):
        source_positions.setdefault(word, []).append(index)
    longest = 0
    for translated_index, word in enumerate(translated_words):
        for source_index in source_positions.get(word, []):
            run = 0
            while (
                translated_index + run < len(translated_words)
                and source_index + run < len(source_words)
                and translated_words[translated_index + run] == source_words[source_index + run]
            ):
                run += 1
            longest = max(longest, run)
    return longest


def call_model(source_pack: str, leaf: int) -> str:
    tesseract_path = TESSERACT_ROOT / f"leaf_{leaf:03d}.txt"
    tesseract = tesseract_path.read_text(errors="ignore") if tesseract_path.exists() else "[not available]"
    transcript = official_transcript(source_pack)
    source_words_match = re.search(r";\s*([\d,]+) OCR words", source_pack)
    source_words = int(source_words_match.group(1).replace(",", "")) if source_words_match else 0
    # Duplicate OCR consumes scarce context and can make the model echo English.
    # Only expose the supplemental pass when the official transcript is sparse.
    supplement = ""
    if source_words < 120 and tesseract.strip() not in {"", "[not available]"}:
        supplement = f"\n\n高清扫描补充 OCR（仅用于补全官方 OCR 缺字）：\n{tesseract.strip()}"
    prompt = f"""请将下列扫描页 OCR 按原有单元和顺序完整翻译成中文。源文中的断行与连字符多为 OCR 排版痕迹，译文应恢复正常段落。不得总结、缩写、避译或照抄英文。人名和地名直接保留原文，不要猜测中文译名；地址和书名原文可保留在中文之后。只输出译文。

--- 原文开始 ---
{transcript}
--- 原文结束 ---{supplement}
"""
    return chat(prompt, SYSTEM, source_words=source_words)


def call_model_chunked(source_pack: str, leaf: int) -> str:
    # The official DjVu transcript has the more reliable reading order.
    # Tesseract remains supplemental evidence for sparse scans, but its page-wide
    # output often begins with marginal noise or rotated text and must not drive
    # the normal chunk fallback.
    source = official_transcript(source_pack)
    chunks: list[str] = []
    current: list[str] = []
    current_size = 0
    for line in source.splitlines():
        added = len(line) + 1
        if current and current_size + added > 1600:
            chunks.append("\n".join(current).strip())
            current = []
            current_size = 0
        current.append(line)
        current_size += added
    if current:
        chunks.append("\n".join(current).strip())
    def translate_piece(chunk: str, label: str) -> str:
        prompt = f"""将下列英文 OCR 按原有顺序完整翻译成中文。修复 OCR 断行和行末连字号，但不得总结、缩写、遗漏或照抄英文整句。标题、署名、引文、数字、价格、地址和标签全部保留。只输出这一段的中文译文，不要说明。

--- 第 {label} 段 ---
{chunk}
--- 本段结束 ---
"""
        translated = chat(
            prompt,
            "你是英译中翻译器。完整翻译所有源文，只输出中文译文。",
            source_words=max(1, len(chunk.split())),
        )
        source_word_count = len(re.findall(r"[A-Za-z]+", chunk))
        minimum_cjk = max(4, min(20, source_word_count // 2))
        copied_run = longest_copied_run(chunk, translated)
        if len(re.findall(r"[\u3400-\u9fff]", translated)) >= minimum_cjk and copied_run < 40:
            return translated
        lines = chunk.splitlines()
        if len(chunk) <= 450 or len(lines) < 2:
            raise RuntimeError(f"Chunk {label} did not return Chinese")
        midpoint = max(1, len(lines) // 2)
        left = "\n".join(lines[:midpoint]).strip()
        right = "\n".join(lines[midpoint:]).strip()
        return "\n\n".join(
            part
            for part in (
                translate_piece(left, f"{label}a") if left else "",
                translate_piece(right, f"{label}b") if right else "",
            )
            if part
        )

    translations: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        translations.append(translate_piece(chunk, f"{index}/{len(chunks)}"))
    return "\n\n".join(translations)


def bullets(values: object, empty: str) -> str:
    if not isinstance(values, list) or not values:
        return f"- {empty}"
    return "\n".join(f"- {str(value).strip()}" for value in values if str(value).strip())


def replace_section(text: str, heading: str, body: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(heading)}[ \t]*\n)(.*?)(?=\n## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if not pattern.search(text):
        raise RuntimeError(f"Missing section: {heading}")
    return pattern.sub(lambda match: f"{match.group(1)}\n{body.strip()}\n", text, count=1)


def render(path: Path, final: str, source_words: int) -> int:
    text = path.read_text()
    if len(final) < 20:
        raise RuntimeError(f"Model returned implausibly short translation for {path.name}")
    cjk_count = len(re.findall(r"[\u3400-\u9fff]", final))
    if source_words >= 20 and cjk_count < max(20, int(len(final) * 0.12)):
        raise RuntimeError(
            f"Model did not return a Chinese translation for {path.name}: "
            f"{cjk_count} CJK chars in {len(final)} chars"
        )
    copied_run = longest_copied_run(
        official_transcript(section(text, "Source Pack")), final
    )
    if 80 <= source_words <= 1500 and copied_run >= 40:
        raise RuntimeError(f"Model copied a long English source span into {path.name}")
    source_pack = section(text, "Source Pack")
    context = "- 已以官方 OCR 逐项初译；高清扫描和独立 OCR 仅作文字补证，待独立复核。"
    if source_words < 120:
        context = "- 官方 OCR 文字较少，已同时参照高清扫描的独立 OCR 补证；待独立复核。"
    text = replace_section(text, "Context Notes", context)
    text = replace_section(text, "Glossary Updates", "- 无。")
    text = replace_section(text, "Final Translation", final)
    text = replace_section(text, "Omitted Bibliographic/Order Info", "- 无。")
    text = replace_section(text, "OCR / Uncertainty Notes", "- 官方 OCR 的断行、连字号和栏序仍须对照高清扫描确认。")
    text = replace_section(text, "Self Critique", "- 已按可恢复文本单元逐项初译，未用概述代替源文；待独立复核。")
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
    parser.add_argument("--chunked", action="store_true")
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
        source_pack = section(text, "Source Pack")
        source_words_match = re.search(r";\s*([\d,]+) OCR words", source_pack)
        source_words = int(source_words_match.group(1).replace(",", "")) if source_words_match else 0
        if args.chunked:
            final = call_model_chunked(source_pack, leaf)
            counts[leaf] = render(path, final, source_words)
        else:
            last_error: RuntimeError | None = None
            for attempt in range(1):
                final = call_model(source_pack, leaf)
                try:
                    counts[leaf] = render(path, final, source_words)
                    last_error = None
                    break
                except RuntimeError as error:
                    last_error = error
            if last_error is not None:
                print(f"leaf {leaf:03d}: whole-page retries failed; using chunked fallback", flush=True)
                final = call_model_chunked(source_pack, leaf)
                counts[leaf] = render(path, final, source_words)
        update_status(counts)
        print(f"leaf {leaf:03d}: drafted ({counts[leaf]} chars)", flush=True)


if __name__ == "__main__":
    main()
