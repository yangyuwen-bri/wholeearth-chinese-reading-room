#!/usr/bin/env python3
"""Build the Fall 1970 Chinese reading-room payload."""

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
TRANSLATION_ROOT = ROOT / "content" / "translations" / "wholeearthcatalo00unse_0"
STATUS_PATH = TRANSLATION_ROOT / "status.jsonl"
LEAF_DIR = TRANSLATION_ROOT / "leaves"
OUT = HERE / "data" / "fall_1970_reader.json"
sys.path.insert(0, str(TRANSLATION_ROOT / "tools"))
from validate_release import validate_issue  # noqa: E402

CHAPTERS = [
    {
        "title": "序 · 使用说明与全书索引",
        "section": "Front Matter",
        "summary": "封面、编辑说明与目录交代这份目录的用法：帮助读者判断什么值得取得，以及到哪里、用什么方法取得。",
    },
    {
        "title": "一、整体系统",
        "section": "Whole Systems",
        "summary": "系统论、生态学、宗教与宇宙尺度共同构成判断框架：任何工具都要放回反馈、资源边界和长期后果中理解。",
    },
    {
        "title": "二、住所与土地利用",
        "section": "Shelter and Land Use",
        "summary": "建筑、土地、水、园艺、动物和能源被连成一套生活系统，重点落在材料、维护和亲手实践。",
    },
    {
        "title": "三、共同体",
        "section": "Community",
        "summary": "食物、健康、消费、合作组织和地方行动构成共同生活的基础设施，同时保留具体的价格、来源和获取办法。",
    },
    {
        "title": "四、通信",
        "section": "Communications",
        "summary": "语言、图像、声音、电影、出版和电子媒介在这里成为表达、复制、传播与重新组织经验的工具。",
    },
    {
        "title": "五、工业与手艺",
        "section": "Industry and Craft",
        "summary": "木工、陶艺、纺织、金工、材料和供应目录把知识落实到工具型号、尺寸、价格与制作过程。",
    },
    {
        "title": "六、游牧",
        "section": "Nomadics",
        "summary": "车辆、船、飞行、攀登、地图与野外技能构成移动生活的技术链，也持续要求读者衡量风险和可维修性。",
    },
    {
        "title": "七、学习",
        "section": "Learning",
        "summary": "教育被放回儿童、游戏、身体、材料、宗教和自我训练；理解来自试验、错误、修正与他人的经验。",
    },
    {
        "title": "八、出版、索引与封底",
        "section": "Back Matter",
        "summary": "订阅、库存、出版信息、索引和封底让《全球概览》自身的生产与流通机制也成为可检查的工具。",
    },
]

PREFACE = [
    {
        "title": "这是什么",
        "html": (
            "<p>这是 1970 年秋季《全球概览》的中文对照阅读室，共 148 个公开扫描叶。"
            "右侧逐叶呈现完整中文译文，左侧保留 Internet Archive 原扫描，正文滚动时自动跟随。</p>"
            "<p>阅读室正文只来自经过扫描核对和独立复核的 leaf 级译稿。书评、引文、图注、表格、规格、"
            "价格、邮资、型号和订购地址均按原页保留；没有用总结性描述替代原文。</p>"
        ),
    },
    {
        "title": "怎样读",
        "html": (
            "<p>可以沿顶部章节顺读，也可以展开每章目录直接跳到某个扫描叶。每页译文都提供“看原页”，"
            "方便把中文重新放回 1970 年的版面、图像和上下文中核查。</p>"
            "<p>书中的价格、医疗知识、卫生方法、宗教观念和户外安全建议属于历史材料，不应直接当作今天的购买、"
            "诊疗或操作指南。</p>"
        ),
    },
    {
        "title": "校订说明",
        "html": (
            "<p>全书 148 页均已完成源页清点、忠实全文翻译、高清扫描复核和独立审校。发布门禁逐页检查"
            "正文存在性、覆盖证据、审校结论与状态一致性；当前全部为 accepted。</p>"
        ),
    },
]


def load_rows() -> list[dict]:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    rows.sort(key=lambda row: row["leaf"])
    if [row["leaf"] for row in rows] != list(range(148)):
        raise ValueError("expected contiguous leaves 000-147")
    if any(row["status"] != "accepted" for row in rows):
        raise ValueError("reader release requires all leaves to be accepted")
    return rows


def printed_page(row: dict) -> int | None:
    value = row.get("printed_page")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def build_payload(rows: list[dict]) -> dict:
    chapters = []
    for index, definition in enumerate(CHAPTERS, start=1):
        chapter_id = f"ch{index:02d}"
        chapter_rows = [row for row in rows if row.get("section") == definition["section"]]
        sections = []
        for row in chapter_rows:
            leaf = row["leaf"]
            source = LEAF_DIR / f"leaf_{leaf:03d}.md"
            raw_body = final_translation(source.read_text(), leaf)
            page = printed_page(row)
            fallback = f"原书第 {page} 页" if page is not None else f"扫描叶 {leaf:03d}"
            title, body = split_display_title(raw_body, fallback)
            sections.append(
                {
                    "title": title,
                    "html": markdown_to_html(body),
                    "leaf": leaf,
                    "leaf_start": leaf,
                    "leaf_end": leaf,
                    "printed_page": page,
                    "id": f"{chapter_id}-leaf-{leaf:03d}",
                    "anchor_status": row["status"],
                    "translation_status": row["status"],
                    "qa_flags": row.get("qa_flags", []),
                    "review_path": row["review_path"],
                    "translation_path": row["translation_path"],
                }
            )

        chapters.append(
            {
                "title": definition["title"],
                "section": definition["section"],
                "summary": definition["summary"],
                "leaf_start": chapter_rows[0]["leaf"],
                "leaf_end": chapter_rows[-1]["leaf"],
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
        "issue_id": "wholeearthcatalo00unse_0",
        "title": "Whole Earth Catalog, Fall 1970",
        "display_title": "全球概览 · 1970 年秋季号",
        "subtitle": "中文对照阅读室 · 148 页忠实全文翻译 · 全册复核完成",
        "scan_url": "https://archive.org/download/wholeearthcatalo00unse_0/page/n{leaf}_w500.jpg",
        "archive_page_url": "https://archive.org/details/wholeearthcatalo00unse_0/page/n{leaf}",
        "leaf_min": 0,
        "leaf_total": 147,
        "printed_page_rules": [{"leaf_start": 2, "leaf_end": 147, "printed_start": 1}],
        "printed_pages": {
            str(row["leaf"]): printed_page(row)
            for row in rows
            if printed_page(row) is not None
        },
        "translation_source": "content/translations/wholeearthcatalo00unse_0",
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
            f"Fall 1970 release gate failed ({len(gate_errors)} issues):\n{preview}"
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
