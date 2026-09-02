#!/usr/bin/env python3
"""Build the subscriber-directory leaves without rewriting names or addresses."""

from __future__ import annotations

import re
from pathlib import Path

from translate_with_ollama import PACKAGE, official_transcript, replace_section, section, update_status


LEAF_114_COMIC = """### 漫画对话

“啊！你当年替日本人当间谍——后来又跟苏联间谍机关混在一起，现在又是中国红色分子！”
"""


LEAF_115_EDITORIAL = """### 《全球概览》邮寄名单（自愿公开）

1969 年 9 月，我们曾写道：

#### 《概览》只剩 20 个月的寿命

计划会变，但按我们写下这些话时的打算，我们将在 1971 年春停止出版《全球概览》。到那时，我们会汇集历期《概览》和《增刊》中最好的内容，出版一本不错的大型平装大众市场读物，很可能交由纽约的某家出版机构发行。

如果到那时，还没有人和想法能把这件事做得比我们更好，那我们就失败了：我们没能让别的东西取代自己。不过更可能的是，那时我们已经过时、成了障碍，我们的离开会引来松一口气的叹息和一场聚会。

Menlo Park 的 Truck Store 大概会继续运作，作为邮购服务，也作为已经“死去”的《概览》工作人员从事更古怪活动的基地。

有人把我们称为“印刷品上的社群”。我想这话是有所指的——或者等我们把这座城烧掉时，它就会显出意义。如果订户愿意，也许我们 1971 年的最后一期《增刊》可以就是我们的邮寄名单。

与此同时，稀少时的草总是更绿。当行动是有限的，突然之间，更多事情似乎都变得可能。如果我们的假说没错，按照新的时间表，《概览》和《增刊》应当会好上许多。冲天火箭的功用，就是在爆炸之前飞得尽可能高。

18 个月和许多传言之后，我们如约带来了这份古怪的东西：让愿意公开的订户的邮寄名单可以被免费取用。这里大约 2,000 人，占我们现有名单的约七分之一；他们在续订卡上表示愿意被刊出。其余订户名单不会被出售、赠送，也不会交给当局。

据我所知，以前没有人如此大规模地公布订户的姓名和地址，所以无论发生什么，都会成为一种新信息。请把情况告诉我们，好吗？我们会想个办法，报告你们的经历。

——SB
"""


def directory_body(leaf: int, source: str) -> str:
    if leaf == 114:
        listing = "\n".join(source.splitlines()[3:])
        listing = listing.replace("SUSTAINING SUBSCRIBERS", "赞助订户（SUSTAINING SUBSCRIBERS）")
        listing = listing.replace("RETAINING SUBSCRIBERS", "续订订户（RETAINING SUBSCRIBERS）")
        return f"{LEAF_114_COMIC}\n\n```text\n{listing}\n```"
    if leaf == 115:
        start = source.index("‘WHOLE EARTH CATALOG mailing list")
        end = source.index("—SB") + len("—SB")
        before = source[:start].strip()
        after = source[end:].strip()
        return (
            "### 邮寄名单——姓名与地址按扫描原样保留\n\n"
            f"```text\n{before}\n```\n\n{LEAF_115_EDITORIAL}\n\n```text\n{after}\n```"
        )
    return (
        "### 《全球概览》自愿公开邮寄名单\n\n"
        "以下姓名、机构、邮寄地址、州名缩写与邮编均按扫描文字原样保留，不改写专名或数字。\n\n"
        f"```text\n{source}\n```"
    )


def main() -> None:
    counts: dict[int, int] = {}
    for leaf in range(114, 126):
        path = PACKAGE / "leaves" / f"leaf_{leaf:03d}.md"
        text = path.read_text()
        source_pack = section(text, "Source Pack")
        final = directory_body(leaf, official_transcript(source_pack))
        text = replace_section(text, "Context Notes", "- 高密度名录页；姓名和邮寄地址按扫描原样保留，说明性文字译成中文。")
        text = replace_section(text, "Glossary Updates", "- 无。")
        text = replace_section(text, "Final Translation", final)
        text = replace_section(text, "Omitted Bibliographic/Order Info", "- 无。")
        text = replace_section(text, "OCR / Uncertainty Notes", "- 邮寄名单保留历史扫描 OCR 拼写；不擅自纠改人名或地址。")
        text = replace_section(text, "Self Critique", "- 已保留所有可恢复姓名、地址、机构和数字；待独立复核。")
        path.write_text(text)
        counts[leaf] = len(final)
        print(f"leaf {leaf:03d}: directory built ({len(final)} chars)")
    update_status(counts)


if __name__ == "__main__":
    main()
