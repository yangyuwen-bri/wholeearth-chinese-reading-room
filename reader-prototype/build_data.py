#!/usr/bin/env python3
"""Build reader JSON for the 1974 Epilog 对照阅读器.

Read-only inputs (never modified):
- content/readings/1974_whole_earth_epilog_chapter_translation_zh.md
- content/readings/1974_whole_earth_epilog_reader_chinese.md

Output:
- data/epilog_reader.json
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def readings_dir() -> Path:
    in_repo = HERE.parent / "content" / "readings"
    if in_repo.exists():
        return in_repo
    return HERE.parent / "ai-https-wholeearth-info" / "content" / "readings"


SRC = readings_dir()
TRANSLATION = SRC / "1974_whole_earth_epilog_chapter_translation_zh.md"
PREFACE = SRC / "1974_whole_earth_epilog_reader_chinese.md"
OUT = HERE / "data" / "epilog_reader.json"

CHAPTER_LEAVES = {
    "译者说明": None,
    "封面、开篇引文与使用说明": (0, 4),
    "一、整体系统": (5, 25),
    "二、土地使用": (26, 57),
    "三、住所": (58, 77),
    "四、软技术": (78, 97),
    "五、手艺": (98, 127),
    "六、共同体": (128, 185),
    "七、游牧": (186, 221),
    "八、通信": (222, 261),
    "九、学习": (262, 301),
    "十、出版业务、索引与封底": (302, 321),
}

MODULE_CHAPTERS = {
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


def inline_md(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def blocks_to_html(lines: list[str]) -> str:
    out: list[str] = []
    paragraph: list[str] = []
    quote: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append(f"<p>{inline_md(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_quote() -> None:
        if quote:
            body = "".join(f"<p>{inline_md(q)}</p>" for q in quote)
            out.append(f"<blockquote>{body}</blockquote>")
            quote.clear()

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_paragraph()
            flush_quote()
            continue
        if line.startswith("> "):
            flush_paragraph()
            quote.append(line[2:].strip())
            continue
        if line.startswith("- "):
            flush_paragraph()
            flush_quote()
            out.append(f"<p class='li'>· {inline_md(line[2:].strip())}</p>")
            continue
        flush_quote()
        paragraph.append(line.strip())
    flush_paragraph()
    flush_quote()
    return "".join(out)


def parse_markdown(path: Path) -> list[dict]:
    chapters: list[dict] = []
    chapter: dict | None = None
    section: dict | None = None
    for raw in path.read_text().splitlines():
        if raw.startswith("# "):
            continue
        if raw.startswith("## "):
            chapter = {"title": raw[3:].strip(), "sections": []}
            chapters.append(chapter)
            section = None
            continue
        if raw.startswith("### "):
            if chapter is None:
                continue
            section = {"title": raw[4:].strip(), "lines": []}
            chapter["sections"].append(section)
            continue
        if chapter is None:
            continue
        if section is None:
            if not raw.strip():
                continue
            section = {"title": chapter["title"], "lines": [], "implicit": True}
            chapter["sections"].append(section)
        section["lines"].append(raw)
    for chap in chapters:
        for sec in chap["sections"]:
            sec["html"] = blocks_to_html(sec.pop("lines"))
        chap["sections"] = [s for s in chap["sections"] if s["html"]]
    return chapters


def assign_leaves(chapters: list[dict]) -> None:
    for index, chap in enumerate(chapters):
        span = CHAPTER_LEAVES.get(chap["title"])
        chap["id"] = f"ch{index:02d}"
        if span is None:
            chap["leaf_start"] = None
            chap["leaf_end"] = None
            for sec in chap["sections"]:
                sec["leaf"] = None
            continue
        start, end = span
        chap["leaf_start"] = start
        chap["leaf_end"] = end
        count = max(len(chap["sections"]), 1)
        for i, sec in enumerate(chap["sections"]):
            sec["leaf"] = start + round((end - start) * i / max(count - 1, 1))
        if chap["title"] == "十、出版业务、索引与封底":
            for sec in chap["sections"]:
                if sec["title"].startswith("封底") and not sec.get("implicit"):
                    sec["leaf"] = 321
    for chap in chapters:
        for j, sec in enumerate(chap["sections"]):
            sec["id"] = f"{chap['id']}-s{j:02d}"


def main() -> None:
    chapters = parse_markdown(TRANSLATION)
    assign_leaves(chapters)

    preface_chapters = parse_markdown(PREFACE)
    preface_sections = []
    for chap in preface_chapters:
        for sec in chap["sections"]:
            title = sec["title"] if not sec.get("implicit") else chap["title"]
            preface_sections.append({"title": title, "html": sec["html"]})

    chapter_ids = {chap["title"]: chap["id"] for chap in chapters}
    modules = {}
    for module_id, chapter_title in MODULE_CHAPTERS.items():
        chap = next(c for c in chapters if c["title"] == chapter_title)
        modules[module_id] = {
            "chapter_id": chapter_ids[chapter_title],
            "title": chap["title"],
            "leaf_start": chap["leaf_start"],
            "leaf_end": chap["leaf_end"],
            "lens_focus": LENS_FOCUS.get(module_id, {}),
        }

    payload = {
        "issue_id": "wholeearthepilog00unse",
        "title": "Whole Earth Epilog, October 1974",
        "scan_url": "https://archive.org/download/wholeearthepilog00unse/page/n{leaf}_w500.jpg",
        "archive_page_url": "https://archive.org/details/wholeearthepilog00unse/page/n{leaf}",
        "leaf_min": 0,
        "leaf_total": 321,
        "printed_page_offset": 449,
        "preface": {"title": "导读", "sections": preface_sections},
        "chapters": chapters,
        "lenses": LENSES,
        "modules": modules,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False))
    section_count = sum(len(c["sections"]) for c in chapters)
    print(f"chapters={len(chapters)} sections={section_count} preface_sections={len(preface_sections)}")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
