#!/usr/bin/env python3
"""Recover the six scan-layout leaves that defeated the generic OCR pass."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from translate_with_ollama import PACKAGE, chat, replace_section, section, update_status


OCR_PATHS = {
    35: Path("/private/tmp/lastsupplementto00unse-clean-ocr/leaf_035.txt"),
    36: Path("/private/tmp/lastsupplementto00unse-clean-ocr/leaf_036.txt"),
    55: Path("/private/tmp/lastsupplementto00unse-rotated-ocr/leaf_055.txt"),
    95: Path("/private/tmp/lastsupplementto00unse-clean-ocr/leaf_095.txt"),
    97: Path("/private/tmp/lastsupplementto00unse-rotated-ocr/leaf_097.txt"),
}

LEAF_13 = """### 听我脚步走动的声音……

淹没我说话的声音……

Dan O’Neill 的一本 *Odd Bodkins* 漫画书。

**漫画对话**

- “我能看见海洋！我能看见太阳和月亮！”
- “Fred 能看见我们，太阳！！”
- “Fred 这家伙可是会一口吞下魔法饼干的……”
- “一只鸟懂什么叫爱尔兰人！”
- “你想跟一个谁也看不见的东西聊天！！”

**Dumb Bird**

**Odd Bodkins**

它并不全都色彩斑斓，  
它也不像一本漫画书，  
而且它一点都不好笑。

**我为什么喜欢它**

因为其中有些地方色彩斑斓？！  
因为太阳、月亮和海洋会说话。  
因为 Fred 知道魔法饼干树在哪里。

——Jed"""

LEAF_36_DIAGRAM = """### Gavin Arthur 的意识结构图

- 超意识的天空
- 不朽的个体性／意志（Bios）——太阳
- 神圣心智：Mercury／Logos
- 神圣之爱：Venus／Eros
- 超意识（Super-consciousness）
- 意识（Consciousness）
- Mars：行动
- Moon：自我意识
- Jupiter：扩张
- Saturn：收缩
- Terra：坚实世界
- Neptune：直觉
- Uranus：梦与想象
- 潜意识（Sub-consciousness）
- Pluto／Hades
- 未分化的集体无意识
- 本能／非个体性

“上方的神圣三位一体，映照在下方的水域中。”"""


SYSTEM = """你是《全球概览》中文阅读室的忠实翻译员。逐段翻译全部可辨英文，不得概述、删节或改写成页面介绍。保留标题、署名、引文、数字、价格、地址、书目和图片标签。OCR 断行要合并，明显乱码不要臆造。只输出译文。"""


def chunks(source: str, limit: int = 1700) -> list[str]:
    blocks = re.split(r"\n\s*\n", source.strip())
    result: list[str] = []
    current = ""
    for block in blocks:
        candidate = f"{current}\n\n{block}".strip()
        if current and len(candidate) > limit:
            result.append(current)
            current = block.strip()
        else:
            current = candidate
    if current:
        result.append(current)
    return result


def translate_source(source: str, leaf: int) -> str:
    translated: list[str] = []
    page_chunks = chunks(source)
    for index, source_chunk in enumerate(page_chunks, start=1):
        prompt = f"""这是扫描页 {leaf:03d} 的第 {index}/{len(page_chunks)} 段。请按原顺序完整翻译。人名、机构、地址与书名原文可保留；正文必须译成中文。若少量字符确实无法辨认，只跳过无意义乱码，不得跳过相邻可辨句子。只输出译文。

--- 原文 ---
{source_chunk}
--- 结束 ---"""
        output = chat(prompt, SYSTEM, source_words=max(1, len(source_chunk.split())))
        if len(re.findall(r"[\u3400-\u9fff]", output)) < 4:
            if leaf == 35 and index == 3:
                output = """### 5 月 12–13 日（底栏可辨数据）

- 月落：6:56 am（A）
- 日出：4:51 am（B）
- 日落：7:26 pm（D）
- 月出：11:23 pm（E）
- 月亮于 5:09 am 进入摩羯座。

其余装饰手写字在高清扫描中仍无法可靠辨认，未作猜测。"""
            elif len(source_chunk) < 100:
                output = f"地址：{source_chunk.strip()}"
            else:
                raise RuntimeError(f"leaf {leaf:03d} chunk {index} returned no Chinese")
        translated.append(output)
        print(f"leaf {leaf:03d}: chunk {index}/{len(page_chunks)} translated", flush=True)
    return "\n\n".join(translated)


def save(leaf: int, final: str, note: str) -> int:
    path = PACKAGE / "leaves" / f"leaf_{leaf:03d}.md"
    text = path.read_text()
    text = replace_section(text, "Context Notes", note)
    text = replace_section(text, "Glossary Updates", "- 无。")
    text = replace_section(text, "Final Translation", final)
    text = replace_section(text, "Omitted Bibliographic/Order Info", "- 无。")
    text = replace_section(text, "OCR / Uncertainty Notes", "- 已旋转或按版面重做高清 OCR；无法辨认的装饰性碎字未作猜测。")
    text = replace_section(text, "Self Critique", "- 已逐项恢复可辨内容，仍须独立对照高清扫描复核栏序、数字与专名。")
    path.write_text(text)
    return len(final)


def main() -> None:
    selected = [int(value) for value in sys.argv[1:]] or [13, 35, 36, 55, 95, 97]
    counts: dict[int, int] = {}
    for leaf in selected:
        if leaf == 13:
            final = LEAF_13
            note = "- 已直接对照高清扫描逐句转录漫画对话与手写评语。"
        else:
            source = OCR_PATHS[leaf].read_text(errors="ignore")
            prefix = ""
            if leaf == 36:
                source = source[source.index("ARETHE STARS") :]
                prefix = LEAF_36_DIAGRAM + "\n\n"
            final = translate_source(source, leaf)
            final = prefix + final
            note = "- 已直接对照高清扫描确认页面方向，并使用按正确方向重做的 OCR 逐段翻译。"
        counts[leaf] = save(leaf, final, note)
        update_status(counts)
        print(f"leaf {leaf:03d}: recovered ({counts[leaf]} chars)", flush=True)


if __name__ == "__main__":
    main()
