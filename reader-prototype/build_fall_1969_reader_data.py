#!/usr/bin/env python3
"""Build the Fall 1969 Chinese reading-room payload."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from build_translation_reader_data import (
    final_translation,
    markdown_to_html,
    split_display_title,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TRANSLATION_ROOT = ROOT / "content" / "translations" / "wholeearthcatalo00unse_7"
STATUS_PATH = TRANSLATION_ROOT / "status.jsonl"
LEAF_DIR = TRANSLATION_ROOT / "leaves"
OUT = HERE / "data" / "fall_1969_reader.json"
sys.path.insert(0, str(TRANSLATION_ROOT / "tools"))
from validate_release import validate_issue  # noqa: E402

CHAPTERS = [
    {
        "title": "序 · 怎样使用这份目录",
        "leaf_start": 0,
        "leaf_end": 3,
        "summary": "封面、编辑说明与使用办法把《全球概览》定义成一件工具：不是替读者做判断，而是让人找到并掌握值得使用的资源。",
    },
    {
        "title": "一、整体系统",
        "leaf_start": 4,
        "leaf_end": 18,
        "summary": "从富勒、控制论和生态模型出发，这一章训练一种整体眼光：判断工具时，同时看尺度、反馈、资源边界和长期后果。",
    },
    {
        "title": "二、住所、土地与能源",
        "leaf_start": 19,
        "leaf_end": 46,
        "summary": "住所不只是建筑形式，而是材料、气候、土地、水、火、能源和维护共同组成的生活系统。",
    },
    {
        "title": "三、工业、手艺与视觉",
        "leaf_start": 47,
        "leaf_end": 60,
        "summary": "工具目录、纺织、木工、塑料、摄影和视觉语言在这里相遇：知识必须能够落到手、材料与制作过程上。",
    },
    {
        "title": "四、通信、媒介与心智",
        "leaf_start": 61,
        "leaf_end": 78,
        "summary": "宇宙通信、诗歌、图像、声音、电脑、教育技术与意识研究，共同追问信息如何被编码、传播和理解。",
    },
    {
        "title": "五、共同体与生活系统",
        "leaf_start": 79,
        "leaf_end": 96,
        "summary": "食物、健康、法律、合作购买、家庭与共同生活被当作可运行的社会基础设施，而不是抽象口号。",
    },
    {
        "title": "六、游牧",
        "leaf_start": 97,
        "leaf_end": 110,
        "summary": "背包、帐篷、靴子、地图、攀登和车辆构成移动生活的技术链，也不断提醒读者衡量重量、风险与可维修性。",
    },
    {
        "title": "七、学习",
        "leaf_start": 111,
        "leaf_end": 127,
        "summary": "学习被放回儿童、游戏、动手制作、身体经验与自我教育；课程只是入口，真正的理解来自持续试验。",
    },
    {
        "title": "八、出版、仓储与封底",
        "leaf_start": 128,
        "leaf_end": 131,
        "summary": "全书最后公开出版规模、成本、订购与仓储方式，让《全球概览》自己的生产机制也成为可检查、可学习的工具。",
    },
]

PREFACE = [
    {
        "title": "这是什么",
        "html": (
            "<p>这是 1969 年秋季《全球概览》的中文精读室，共 132 个扫描叶。"
            "右侧中文按原书页序整理，左侧保留 Internet Archive 原扫描，正文滚动时会自动跟随。</p>"
            "<p>它既不是逐字 OCR，也不是脱离原页的内容摘要。译文保留书评、编辑判断、人物署名、关键规格与历史价格；"
            "遇到跨栏、小字和图注，则以高清扫描核对后的可确认边界为准。</p>"
        ),
    },
    {
        "title": "怎样读",
        "html": (
            "<p>可以沿顶部章节顺读，也可以展开每章的条目目录直接跳转。每条译文都提供“看原页”，"
            "便于把中文判断放回 1969 年的版面、图像和上下文中检查。</p>"
            "<p>书中的产品价格、医疗知识和户外安全建议属于历史材料，不应直接当作今天的购买或操作指南。</p>"
        ),
    },
    {
        "title": "校订说明",
        "html": (
            "<p>本版 132 页均已完成独立复核。原先标记为需要高清扫描的 29 页已逐页闭环；"
            "终检又发现并重译了 7 页虽被旧标签接受、但仍残留机器转写的内容。</p>"
        ),
    },
]


def load_rows() -> list[dict]:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    rows.sort(key=lambda row: row["leaf"])
    if [row["leaf"] for row in rows] != list(range(132)):
        raise ValueError("expected contiguous leaves 000-131")
    if any(row["status"] != "accepted" for row in rows):
        raise ValueError("reader release requires all leaves to be accepted")
    return rows


def printed_page(leaf: int) -> int | None:
    return leaf - 2 if 3 <= leaf <= 131 else None


def build_payload(rows: list[dict]) -> dict:
    chapters = []
    for index, definition in enumerate(CHAPTERS, start=1):
        chapter_id = f"ch{index:02d}"
        sections = []
        for row in rows[definition["leaf_start"] : definition["leaf_end"] + 1]:
            leaf = row["leaf"]
            source = LEAF_DIR / f"leaf_{leaf:03d}.md"
            raw_body = final_translation(source.read_text(), leaf)
            fallback = f"原书第 {printed_page(leaf)} 页" if printed_page(leaf) else f"扫描叶 {leaf:03d}"
            title, body = split_display_title(raw_body, fallback)
            section = {
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
                "review_path": row["review_path"],
                "translation_path": row["translation_path"],
            }
            sections.append(section)

        chapters.append(
            {
                **definition,
                "id": chapter_id,
                "sections": sections,
                "toc": [
                    {
                        "title": section["title"],
                        "target_id": section["id"],
                        "leaf": section["leaf"],
                        "leaf_start": section["leaf"],
                        "leaf_end": section["leaf"],
                        "printed_page": section["printed_page"],
                    }
                    for section in sections
                ],
                "source_toc_sections": [],
            }
        )

    counts = Counter(row["status"] for row in rows)
    return {
        "issue_id": "wholeearthcatalo00unse_7",
        "title": "Whole Earth Catalog, Fall 1969",
        "display_title": "全球概览 · 1969 年秋季号",
        "subtitle": "中文精读室 · 132 页扫描对照 · 全册复核完成",
        "scan_url": "https://archive.org/download/wholeearthcatalo00unse_7/page/n{leaf}_w500.jpg",
        "archive_page_url": "https://archive.org/details/wholeearthcatalo00unse_7/page/n{leaf}",
        "leaf_min": 0,
        "leaf_total": 131,
        "printed_page_rules": [{"leaf_start": 3, "leaf_end": 131, "printed_start": 1}],
        "translation_source": "content/translations/wholeearthcatalo00unse_7",
        "translation_status_counts": dict(counts),
        "preface": {"title": "导读", "sections": PREFACE},
        "chapters": chapters,
        "lenses": [],
        "modules": {},
    }


def main() -> None:
    gate_errors = validate_issue()
    if gate_errors:
        preview = "\n".join(f"- {error}" for error in gate_errors[:20])
        raise SystemExit(
            f"Fall 1969 release gate failed ({len(gate_errors)} issues):\n{preview}"
        )
    rows = load_rows()
    payload = build_payload(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False))
    section_count = sum(len(chapter["sections"]) for chapter in payload["chapters"])
    print(f"chapters={len(payload['chapters'])} sections={section_count}")
    print(f"statuses={payload['translation_status_counts']}")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
