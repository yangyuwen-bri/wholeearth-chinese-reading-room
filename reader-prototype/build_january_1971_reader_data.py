#!/usr/bin/env python3
"""Build the January 1971 Chinese reading-room payload."""

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
TRANSLATION_ROOT = ROOT / "content" / "translations" / "wholeearthcatalo00unse_3"
STATUS_PATH = TRANSLATION_ROOT / "status.jsonl"
LEAF_DIR = TRANSLATION_ROOT / "leaves"
OUT = HERE / "data" / "january_1971_reader.json"
sys.path.insert(0, str(TRANSLATION_ROOT / "tools"))
from validate_release import validate_issue  # noqa: E402


CHAPTERS = [
    {
        "title": "序 · 封面、权力与肯·凯西",
        "leaf_start": 0,
        "leaf_end": 3,
        "summary": "从真假判断题、施佩尔的技术政治反思，到肯·凯西的完整访谈，本期开篇把个人自由、权力与媒介放在同一张试卷上。",
    },
    {
        "title": "一、金钱、组织与公共行动",
        "leaf_start": 4,
        "leaf_end": 10,
        "summary": "代币经济、银行、人民资本、通货膨胀、非营利组织与公民投诉表，把制度问题拆成可以检查、联络和试验的具体工具。",
    },
    {
        "title": "二、生态生活、健康与合作",
        "leaf_start": 11,
        "leaf_end": 17,
        "summary": "从鸡粪燃料、清洁剂和活体住宅，到日常医疗、法律自保与合作社资料，这一组页面把生活技术放回成本、风险和共同组织之中。",
    },
    {
        "title": "三、土地、食物、音乐与手艺",
        "leaf_start": 18,
        "leaf_end": 24,
        "summary": "农场、边远地区生活、食品成本、乐器、园艺资料与泥土餐具共同展示知识如何在土地、材料、供应和亲手实践之间流动。",
    },
    {
        "title": "四、意识、游戏、飞行与移动",
        "leaf_start": 25,
        "leaf_end": 30,
        "summary": "药物资料、围棋、飞行、人力飞机、靴子、印刷、化粪池和雪鞋并列出现，持续追问自由探索所需的训练、装备与风险判断。",
    },
    {
        "title": "五、通信、原住民知识与勘误",
        "leaf_start": 31,
        "leaf_end": 39,
        "summary": "书信、更正、土壤书、Navajo 知识、原住民出版、Arcosanti 工作坊与全书勘误，构成一套由读者反馈维持的知识网络。",
    },
    {
        "title": "六、沙漠中的制作实验",
        "leaf_start": 40,
        "leaf_end": 44,
        "summary": "编辑团队把一期杂志搬到沙漠中制作；牵引器、充气结构、锚固、风暴、工作环境、成本与人员分工都作为实验记录完整公开。",
    },
    {
        "title": "七、发行、订阅与机构",
        "leaf_start": 45,
        "leaf_end": 47,
        "summary": "最后三页公开 Random House 发行谈判、订阅表、历届编辑、Portola Institute 项目与完整订户名录，并以沙漠制作现场收束。",
    },
]


PREFACE = [
    {
        "title": "这是什么",
        "html": (
            "<p>这是 1971 年 1 月《全球概览》的中文对照阅读室，共 48 个公开扫描叶。"
            "Internet Archive 的条目路径沿用 <em>Difficult But Possible Supplement</em>，"
            "但原刊封面直接印作 <em>Whole Earth Catalog · January 1971</em>；阅读室以封面题名显示。</p>"
            "<p>右侧逐页呈现完整中文译文，左侧保留原扫描。书信、文章、图注、表格、表单、"
            "尺寸、价格、地址和订户名录均按原页保留，没有用总结性描述替代正文。</p>"
        ),
    },
    {
        "title": "怎样读",
        "html": (
            "<p>可以按顶部章节顺读，也可以展开章节目录直接跳到某个扫描叶。每页译文都有“看原页”入口，"
            "便于把中文放回原来的多栏版面、图像与历史语境中核对。</p>"
            "<p>书中的医疗、法律、金融、药物和户外技术信息属于 1971 年的历史材料，不应直接当作今天的专业建议。</p>"
        ),
    },
    {
        "title": "校订说明",
        "html": (
            "<p>全书 48 页均完成源页清点、忠实全文翻译、原始高清扫描复核和独立审校。"
            "发布门禁检查正文完整性、审校证据、状态一致性、未决占位符和摘要漂移；当前 48 页全部 accepted。</p>"
        ),
    },
]


def load_rows() -> list[dict]:
    rows = [json.loads(line) for line in STATUS_PATH.read_text().splitlines() if line.strip()]
    rows.sort(key=lambda row: row["leaf"])
    if [row["leaf"] for row in rows] != list(range(48)):
        raise ValueError("expected contiguous leaves 000-047")
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
        sections = []
        for row in rows[definition["leaf_start"] : definition["leaf_end"] + 1]:
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
                **definition,
                "id": chapter_id,
                "sections": sections,
                "toc": [
                    {
                        "title": item["title"],
                        "target_id": item["id"],
                        "leaf": item["leaf"],
                        "leaf_start": item["leaf"],
                        "leaf_end": item["leaf"],
                        "printed_page": item["printed_page"],
                    }
                    for item in sections
                ],
                "source_toc_sections": [],
            }
        )

    counts = Counter(row["status"] for row in rows)
    return {
        "issue_id": "wholeearthcatalo00unse_3",
        "title": "Difficult But Possible Supplement to the Whole Earth Catalog, January 1971",
        "display_title": "全球概览 · 1971 年 1 月号",
        "subtitle": "中文对照阅读室 · 48 页忠实全文翻译 · 全册高清复核完成",
        "scan_url": "https://archive.org/download/wholeearthcatalo00unse_3/page/n{leaf}_w500.jpg",
        "archive_page_url": "https://archive.org/details/wholeearthcatalo00unse_3/page/n{leaf}",
        "leaf_min": 0,
        "leaf_total": 47,
        "printed_page_rules": [{"leaf_start": 3, "leaf_end": 47, "printed_start": 4}],
        "printed_pages": {
            str(row["leaf"]): printed_page(row)
            for row in rows
            if printed_page(row) is not None
        },
        "translation_source": "content/translations/wholeearthcatalo00unse_3",
        "translation_status_counts": dict(counts),
        "preface": {"title": "导读", "sections": PREFACE},
        "chapters": chapters,
        "lenses": [],
        "modules": {},
    }


def main() -> None:
    errors = validate_issue()
    if errors:
        preview = "\n".join(f"- {error}" for error in errors[:20])
        raise SystemExit(f"January 1971 release gate failed ({len(errors)} issues):\n{preview}")
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
