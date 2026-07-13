#!/usr/bin/env python3
"""Build reader JSON from leaf-level Epilog translations.

This is the production builder for the Chinese reading room. It uses the
faithful leaf translation workflow under content/translations instead of the
older summarized reading draft under content/readings.
"""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TRANSLATION_ROOT = ROOT / "content" / "translations" / "wholeearthepilog00unse"
STATUS_PATH = TRANSLATION_ROOT / "status.jsonl"
LEAF_DIR = TRANSLATION_ROOT / "leaves"
LINK_INDEX_PATH = ROOT / "data" / "bibliography" / "1974_whole_earth_epilog_links.json"
OUT = HERE / "data" / "epilog_reader.json"

SECTION_TITLES = {
    "Front Matter": "封面、开篇引文与使用说明",
    "Whole Systems": "一、整体系统",
    "Land Use": "二、土地使用",
    "Shelter": "三、住所",
    "Soft Technology": "四、软技术",
    "Craft": "五、手艺",
    "Community": "六、共同体",
    "Nomadics": "七、游牧",
    "Communications": "八、通信",
    "Learning": "九、学习",
    "Business / Index": "十、出版业务、索引与封底",
}

SECTION_ORDER = list(SECTION_TITLES)

READER_GUIDE_SECTIONS = [
    {
        "title": "怎样读这本书",
        "html": (
            "<p>《全球概览尾声》不是一本文字顺滑的普通书。它更像一张工具地图：书评、摘录、目录、图表、读者经验和编辑判断交错在一起，把 1974 年的 Whole Earth 世界摊开给读者。</p>"
            "<p>这个中文阅读室按原书页序组织译文。右侧是中文译稿，左侧保留 Internet Archive 扫描页；点击“看原页”或滚动正文时，可以回到原书图像，检查版面、图片和上下文。</p>"
            "<p>译文尽量保留原书中的评论、摘录、标题、署名、图注和论证节奏；价格、订购地址、库存编号等重复性交易信息会压缩处理。遇到图表、小字或手写标注时，后续还会继续用高分辨率扫描核对。</p>"
        ),
    },
    {
        "title": "阅读方式",
        "html": (
            "<p>每章开头有一段导读，帮助你先抓住这一章的主题。目录默认收起，展开后可以直接跳到本章条目。</p>"
            "<p>如果只想浏览，可以从章节导读和本章条目进入；如果想细读，可以顺着正文逐页读，并随时对照左侧扫描页。部分已核实的书籍和出版物会在条目下方提供外部书目链接。</p>"
        ),
    },
]

CHAPTER_SUMMARIES = {
    "Front Matter": (
        "这里交代《全球概览尾声》的入口方式：它是一套帮助读者判断、寻找并取得工具的装置。"
        "开篇引文把尺度拉到地球、宇宙和人的有限性，使用说明则说明这本书如何被翻阅、检索和继续修订。"
    ),
    "Whole Systems": (
        "本章从控制论、系统论和生态学进入全书的判断框架。贝特森、怀尔登、增长模型、能源账本和政治生态共同提出一个要求："
        "任何工具都不能只看局部效用，必须放回反馈、尺度、边界和长期后果中理解。"
    ),
    "Land Use": (
        "土地使用章把抽象的生态尺度落到土壤、水、植物、动物、园艺和农场实践。它关心怎样识别自然系统，也关心怎样修复已经被消耗的土地循环。"
    ),
    "Shelter": (
        "住所章把房子看作需要长期维护的生活系统，而不只是建筑造型。材料、火、通风、地震、旧料、工具和失败经验都进入判断。"
    ),
    "Soft Technology": (
        "软技术章讨论风、太阳、水、废物处理和替代能源。它并不把替代技术浪漫化，而是反复追问：能否交付、能否维护、净能量和风险是否说得清楚。"
    ),
    "Craft": (
        "手艺章集中在身体知识：织、缝、染、制陶、做鞋、修补和使用工具。它寻找那些真正能让人上手的书，而不是只提供漂亮照片的手艺消费品。"
    ),
    "Community": (
        "共同体章把社群理解为基础设施：热线、黄页、住房、医疗、法律、女性资源、黑人网络、中国资料和合作组织。它关心的是人们怎样找到彼此，并把互助变成可运行的通道。"
    ),
    "Nomadics": (
        "游牧章关于移动、导航和野外判断。自行车、汽车、船、飞行、攀岩、地图、天气和荒野技能在这里连接成一种离开固定地点后仍能自我维护的能力。"
    ),
    "Communications": (
        "传播章把出版、电话、无线电、影像、目录和计算机看作社会神经系统。它关心信息如何被写下、复制、装订、发送、检索和重新组织。"
    ),
    "Learning": (
        "学习章把教育放回实验、游戏、儿童、身体、治疗、意识训练和日常工作。它反对只把学习理解成课程，而强调材料、错误、他人经验和自我纪律。"
    ),
    "Business / Index": (
        "最后一章把出版机制本身摊开：编辑、成本、发行、索引、读者反馈和封底口号。它提醒读者，Whole Earth 不只是内容，也是一套可以被学习的出版工具。"
    ),
}

SOURCE_TOC_PATTERNS = ("章节目录", "本章目录", "本节目录")

MODULES = {
    "method": "封面、开篇引文与使用说明",
    "systems": "一、整体系统",
    "land": "二、土地使用",
    "shelter": "三、住所",
    "soft": "四、软技术",
    "craft": "五、手艺",
    "community": "六、共同体",
    "nomadics": "七、游牧",
    "communications": "八、通信",
    "learning": "九、学习",
    "business": "十、出版业务、索引与封底",
}

LENS_FOCUS = {
    "method": {
        "access": "这是全书的入口协议：读者不是被动阅读，而是学习判断什么值得取得、怎样取得。",
        "publishing": "这里已经把出版定义为工具系统，后面的索引、价格、地址和财务公开都从这里展开。",
    },
    "systems": {
        "scale": "在这条暗线下，它是全书的尺度校准器：之后每个工具都要被放回反馈、能源和生态边界里。",
        "risk": "它提示风险常来自系统延迟和隐藏输入，比如增长模型、核能和净能量下降。",
    },
    "land": {
        "scale": "它把生态尺度落到地貌、土壤、水和营养循环。",
        "maintenance": "维护在这里表现为修复循环：粪便、污水、土壤和花园重新接上。",
        "embodied": "识别鸟、足迹、蘑菇和植物，是用身体进入土地。",
    },
    "shelter": {
        "maintenance": "这条暗线下，房子是长期维护系统：结构、火、地震、通风、旧料和修补都同等重要。",
        "embodied": "建房不是看图纸消费，而是画、锯、搬、修、观察风和太阳。",
    },
    "soft": {
        "scale": "它把能源愿望放回净能量、天气、材料和维护成本。",
        "maintenance": "软技术只有在普通人能理解组件、修理失败、判断成本时才成立。",
        "risk": "漏水圆顶、吹走的风机、泡沫爆燃都属于技术判断，而不是题外话。",
    },
    "craft": {
        "embodied": "这条暗线下，它是全书最直接的身体学习章节。",
        "maintenance": "工具制作、缝纫、皮革和陶艺都把修补能力从商品系统里拿回来。",
    },
    "community": {
        "access": "在找入口视角下，黄页、热线、目录、黑人书目和中国资料是最重要的通道。",
        "community": "在组织社会视角下，它展示共同体需要钱、法律、医疗、食物、住房和出版网络。",
        "scale": "它把系统问题落到可运行的社会接口：谁接电话、谁给钱、谁懂法、谁出版。",
    },
    "nomadics": {
        "maintenance": "移动能力取决于链条、刹车、车锁、海图、天气、工具箱和临时修理。",
        "embodied": "地图、攀岩、航海和野外观察都要求身体判断。",
        "risk": "飞行、鹰猎、刀和荒野生存都在提醒：书能引路，但不能替代训练。",
    },
    "communications": {
        "access": "这里是 access 的媒体层：目录、电话、参考书、无线电和计算机让工具可找到、可复制、可传播。",
        "community": "小报、视频和自行出版让共同体能记录自己，而不是只被广播。",
        "publishing": "它把出版拆成书写、装订、设计、印刷、发行、参考工具和读者网络。",
    },
    "learning": {
        "embodied": "儿童、玩具、游戏、厨房、实验和摩托维修都把学习放回手和材料。",
        "risk": "药物、治疗、宗教和意识训练被纳入学习，但必须保持判断。",
        "access": "学习在这里不是课程，而是进入材料、他人经验、错误和工作的方法。",
    },
    "business": {
        "access": "索引和价格结构说明 access 也依赖检索、发行和成本。",
        "community": "POINT 和 Demise Party 把出版、赠款、公共事件和读者反馈接成社群机制。",
        "publishing": "这是全书的元工具层：出版不只承载内容，它自己也被做成可学习对象。",
    },
}

LENSES = [
    {
        "id": "access", "code": "ACCESS", "title": "找入口",
        "caption": "目录、地址、索引、热线、通信网络",
        "note": "这条线把 Epilog 看成 access machine：最重要的不是工具本身，而是找到、购买、检索、联系和继续追踪工具的通道。",
        "nodes": ["method", "community", "communications", "business"],
    },
    {
        "id": "scale", "code": "SCALE", "title": "看尺度",
        "caption": "地球、生态、能源、经济、反馈回路",
        "note": "这条线从系统尺度出发：工具进入生态、能源和制度边界后才显出真实成本。",
        "nodes": ["systems", "land", "soft", "community"],
    },
    {
        "id": "maintenance", "code": "MAINTAIN", "title": "会维护",
        "caption": "修房、土壤、水、车辆、组件、失败经验",
        "note": "这条线强调可修理性。Epilog 评价工具时，总会追问谁能维护、成本如何、失败经验是否可见。",
        "nodes": ["land", "shelter", "soft", "nomadics"],
    },
    {
        "id": "embodied", "code": "BODY", "title": "用身体学",
        "caption": "手艺、建造、园艺、导航、游戏和观察",
        "note": "这条线把知识放回身体：看、摸、做、错、修正，比单纯阅读更接近 Whole Earth 的学习观。",
        "nodes": ["land", "shelter", "craft", "nomadics", "learning"],
    },
    {
        "id": "community", "code": "SOCIAL", "title": "组织社会",
        "caption": "合作、健康、法律、出版、黑人网络、中国",
        "note": "这条线把共同体从情感词改成社会基础设施：医疗、法律、出版、资金和跨文化资料入口都在其中。",
        "nodes": ["community", "communications", "business"],
    },
    {
        "id": "risk", "code": "RISK", "title": "穿越风险",
        "caption": "蘑菇、核能、飞行、药物、荒野、宗教",
        "note": "这条线提醒自由不是姿态。蘑菇、核能、飞行、荒野和意识探索都要求风险账本。",
        "nodes": ["systems", "land", "soft", "nomadics", "learning"],
    },
    {
        "id": "publishing", "code": "PUBLISH", "title": "出版成工具",
        "caption": "成本、劳动、索引、读者反馈、封底",
        "note": "这条线看出版机制本身：目录、索引、电话、小报、成本和组织方式也是 Whole Earth 的工具。",
        "nodes": ["method", "communications", "business"],
    },
]

PRINTED_PAGE_RULES = [
    {"leaf_start": 2, "leaf_end": 2, "printed_start": 450},
    {"leaf_start": 3, "leaf_end": 319, "printed_start": 452},
]


def inline_md(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def final_translation(markdown: str, leaf: int) -> str:
    match = re.search(r"^## Final Translation\s*\n(.*?)(?=\n## |\Z)", markdown, re.S | re.M)
    if not match:
        raise ValueError(f"leaf {leaf:03d} has no Final Translation section")
    return match.group(1).strip()


def split_display_title(markdown: str, fallback: str) -> tuple[str, str]:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^#{1,6}\s+(.+)$", line.strip())
        if match:
            title = match.group(1).strip()
            body = "\n".join(lines[:index] + lines[index + 1 :]).strip()
            return title, body
    return fallback, markdown


def markdown_to_html(markdown: str) -> str:
    out: list[str] = []
    paragraph: list[str] = []
    quote: list[str] = []
    ul_open = False
    ol_open = False

    def flush_paragraph() -> None:
        if paragraph:
            out.append(f"<p>{inline_md(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_quote() -> None:
        if quote:
            body = "".join(f"<p>{inline_md(line)}</p>" for line in quote)
            out.append(f"<blockquote>{body}</blockquote>")
            quote.clear()

    def close_lists() -> None:
        nonlocal ul_open, ol_open
        if ul_open:
            out.append("</ul>")
            ul_open = False
        if ol_open:
            out.append("</ol>")
            ol_open = False

    for raw in markdown.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            flush_quote()
            close_lists()
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_quote()
            close_lists()
            level = min(max(len(heading.group(1)) + 2, 3), 5)
            out.append(f"<h{level}>{inline_md(heading.group(2).strip())}</h{level}>")
            continue
        if stripped.startswith("> "):
            flush_paragraph()
            close_lists()
            quote.append(stripped[2:].strip())
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            flush_quote()
            if ol_open:
                out.append("</ol>")
                ol_open = False
            if not ul_open:
                out.append("<ul>")
                ul_open = True
            out.append(f"<li>{inline_md(stripped[2:].strip())}</li>")
            continue
        numbered = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        if numbered:
            flush_paragraph()
            flush_quote()
            if ul_open:
                out.append("</ul>")
                ul_open = False
            if not ol_open:
                out.append("<ol>")
                ol_open = True
            out.append(f"<li>{inline_md(numbered.group(2).strip())}</li>")
            continue
        flush_quote()
        close_lists()
        paragraph.append(stripped)

    flush_paragraph()
    flush_quote()
    close_lists()
    return "".join(out)


def printed_page(leaf: int) -> int | None:
    for rule in PRINTED_PAGE_RULES:
        if rule["leaf_start"] <= leaf <= rule["leaf_end"]:
            return rule["printed_start"] + leaf - rule["leaf_start"]
    return None


def load_status() -> list[dict]:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    rows.sort(key=lambda row: row["leaf"])
    return rows


def provider_label(provider: str) -> str:
    labels = {
        "openlibrary": "Open Library",
        "internet_archive": "Internet Archive",
    }
    return labels.get(provider, provider)


def compact_links(links: list[dict]) -> list[dict]:
    compacted = []
    seen_urls = set()
    ia_count = 0
    sorted_links = sorted(links, key=lambda link: 0 if link.get("provider") == "openlibrary" else 1)
    for link in sorted_links:
        url = link.get("url")
        provider = link.get("provider", "")
        if not url or url in seen_urls:
            continue
        if provider == "internet_archive":
            ia_count += 1
            if ia_count > 2:
                continue
        seen_urls.add(url)
        compacted.append(
            {
                "provider": provider,
                "label": provider_label(provider),
                "url": url,
            }
        )
        if len(compacted) >= 3:
            break
    return compacted


def load_bibliography_links() -> dict[int, list[dict]]:
    if not LINK_INDEX_PATH.exists():
        return {}
    data = json.loads(LINK_INDEX_PATH.read_text())
    by_leaf: dict[int, list[dict]] = {}
    seen = set()
    for item in data.get("items", []):
        if item.get("status") != "confirmed" or not item.get("links"):
            continue
        links = compact_links(item["links"])
        if not links:
            continue
        for mention in item.get("source_mentions", []):
            leaf = mention.get("leaf")
            if leaf is None or mention.get("section") == "Business / Index":
                continue
            key = (leaf, item["title"])
            if key in seen:
                continue
            seen.add(key)
            by_leaf.setdefault(leaf, []).append(
                {
                    "title": item["title"],
                    "links": links,
                }
            )
    for items in by_leaf.values():
        items.sort(key=lambda item: item["title"].lower())
    return by_leaf


def is_source_toc(section: str, leaf: int, body: str) -> bool:
    if section == "Front Matter":
        return False
    if any(pattern in body for pattern in SOURCE_TOC_PATTERNS):
        return True
    return leaf in {3}


def toc_entry(section: dict) -> dict:
    return {
        "title": section["title"],
        "target_id": section["id"],
        "leaf": section["leaf"],
        "leaf_start": section["leaf_start"],
        "leaf_end": section["leaf_end"],
        "printed_page": printed_page(section["leaf"]),
    }


def build_payload(rows: list[dict]) -> dict:
    grouped: dict[str, list[dict]] = {key: [] for key in SECTION_ORDER}
    bibliography_by_leaf = load_bibliography_links()
    for row in rows:
        grouped.setdefault(row["section"], []).append(row)

    chapters = []
    for index, section in enumerate(SECTION_ORDER):
        items = grouped.get(section, [])
        if not items:
            continue
        chapter_id = f"ch{index + 1:02d}"
        sections = []
        source_toc_sections = []
        for row in items:
            leaf = row["leaf"]
            path = LEAF_DIR / f"leaf_{leaf:03d}.md"
            raw_body = final_translation(path.read_text(), leaf)
            title, body = split_display_title(raw_body, SECTION_TITLES[section])
            source_toc = is_source_toc(section, leaf, raw_body)
            section_payload = {
                "title": title,
                "html": markdown_to_html(body),
                "leaf": leaf,
                "leaf_start": leaf,
                "leaf_end": leaf,
                "printed_page": printed_page(leaf),
                "id": f"{chapter_id}-leaf-{leaf:03d}",
                "anchor_status": row["status"],
                "translation_status": row["status"],
                "qa_flags": row.get("qa_flags", []),
                "review_path": row.get("review_path"),
                "translation_path": row.get("translation_path"),
            }
            if not source_toc and bibliography_by_leaf.get(leaf):
                section_payload["bibliography_links"] = bibliography_by_leaf[leaf]
            if source_toc:
                source_toc_sections.append(section_payload)
            else:
                sections.append(section_payload)
        toc = [toc_entry(section_payload) for section_payload in sections]
        chapters.append(
            {
                "title": SECTION_TITLES[section],
                "sections": sections,
                "summary": CHAPTER_SUMMARIES.get(section, ""),
                "toc": toc,
                "source_toc_sections": source_toc_sections,
                "id": chapter_id,
                "leaf_start": items[0]["leaf"],
                "leaf_end": items[-1]["leaf"],
            }
        )

    chapter_by_title = {chapter["title"]: chapter for chapter in chapters}
    modules = {}
    for module_id, title in MODULES.items():
        chapter = chapter_by_title.get(title)
        if not chapter:
            continue
        modules[module_id] = {
            "chapter_id": chapter["id"],
            "title": title,
            "leaf_start": chapter["leaf_start"],
            "leaf_end": chapter["leaf_end"],
            "lens_focus": LENS_FOCUS.get(module_id, {}),
        }

    status_counts = Counter(row["status"] for row in rows)
    return {
        "issue_id": "wholeearthepilog00unse",
        "title": "Whole Earth Epilog, October 1974",
        "scan_url": "https://archive.org/download/wholeearthepilog00unse/page/n{leaf}_w500.jpg",
        "archive_page_url": "https://archive.org/details/wholeearthepilog00unse/page/n{leaf}",
        "leaf_min": 0,
        "leaf_total": 321,
        "printed_page_offset": 449,
        "printed_page_rules": PRINTED_PAGE_RULES,
        "translation_source": "content/translations/wholeearthepilog00unse",
        "translation_status_counts": dict(status_counts),
        "preface": {
            "title": "导读",
            "sections": READER_GUIDE_SECTIONS,
        },
        "chapters": chapters,
        "lenses": LENSES,
        "modules": modules,
    }


def main() -> None:
    output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else OUT
    rows = load_status()
    payload = build_payload(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False))
    section_count = sum(len(chapter["sections"]) for chapter in payload["chapters"])
    print(f"chapters={len(payload['chapters'])} sections={section_count}")
    print(f"statuses={payload['translation_status_counts']}")
    print(f"wrote {output} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
