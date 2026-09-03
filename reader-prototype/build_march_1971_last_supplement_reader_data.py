#!/usr/bin/env python3
"""Build the March 1971 Last Supplement Chinese reading-room payload."""

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
TRANSLATION_ROOT = ROOT / "content" / "translations" / "lastsupplementto00unse"
STATUS_PATH = TRANSLATION_ROOT / "status.jsonl"
LEAF_DIR = TRANSLATION_ROOT / "leaves"
OUT = HERE / "data" / "march_1971_last_supplement_reader.json"
sys.path.insert(0, str(TRANSLATION_ROOT / "tools"))
from validate_release import validate_issue  # noqa: E402


CHAPTERS = [
    {
        "title": "序 · 最后一期增刊与反文化自省",
        "leaf_start": 0,
        "leaf_end": 13,
        "summary": "封面、献词、漫画、药物与意识讨论共同追问：反文化怎样面对自身的权力、欲望、神话和终结。",
    },
    {
        "title": "一、直接行动、法律与计算机",
        "leaf_start": 14,
        "leaf_end": 25,
        "summary": "征兵档案行动的访谈与辩论，延伸到法律工具、证据规则和计算机权力，完整保留行动者之间的分歧。",
    },
    {
        "title": "二、精神实践、占星与另类教育",
        "leaf_start": 26,
        "leaf_end": 42,
        "summary": "从耶稣祈祷、苏菲主义、瑜伽与占星，到意识地图和实验学校，这组材料并置实践方法、个人经验与制度批评。",
    },
    {
        "title": "三、公共媒体、身体与生态生活",
        "leaf_start": 43,
        "leaf_end": 64,
        "summary": "教育改革、公共广播、公平原则、癌症争论、食物、乳品、禅修和家庭生态，把公共信息与身体经验接在一起。",
    },
    {
        "title": "四、书、诗、图像与工具箱",
        "leaf_start": 65,
        "leaf_end": 86,
        "summary": "布伯、小说、诗歌、木刻、音乐、迷幻经验和编辑私人的工具箱轮番出现，形成一段密集的阅读与文化漫游。",
    },
    {
        "title": "五、未来、社会冲突与公共健康",
        "leaf_start": 87,
        "leaf_end": 108,
        "summary": "未来研究、技术政治、族群经验、惩罚制度、宗教性药物、环境毒物与毒品政策在同一组历史材料中相互碰撞。",
    },
    {
        "title": "六、教育替代方案与读者来信",
        "leaf_start": 109,
        "leaf_end": 113,
        "summary": "替代高中、规划建设、教师实践和读者来信把宏观教育批评落到可运行的学校、课程与共同体实验。",
    },
    {
        "title": "七、订户名录、告别与终结派对",
        "leaf_start": 114,
        "leaf_end": 131,
        "summary": "公开订户名录之后，是读者信息、最后一期目录预告、终结派对邀请与封底广告；出版物以自己的社群和退场方式收束。",
    },
]


PREFACE = [
    {
        "title": "这是什么",
        "html": (
            "<p>这是 1971 年 3 月《最后一期〈全球概览〉增刊》的中文对照阅读室，共 132 个公开扫描叶。"
            "右侧逐页呈现完整中文译文，左侧保留 Internet Archive 原扫描。</p>"
            "<p>访谈、文章、诗歌、书信、漫画文字、图注、广告、价格、地址和订户名录均按原页保留；"
            "没有用总结性描述替代正文。</p>"
        ),
    },
    {
        "title": "怎样读",
        "html": (
            "<p>可以按顶部章节顺读，也可以展开章节目录直接跳到某个扫描叶。每页译文都有“看原页”入口，"
            "便于把中文放回原来的多栏版面、图像和历史语境中核对。</p>"
            "<p>书中的医疗、法律、药物、政治行动和户外技术信息属于 1971 年的历史材料，"
            "不应直接当作今天的专业建议。</p>"
        ),
    },
    {
        "title": "校订说明",
        "html": (
            "<p>全书 132 页均完成源页清点、忠实全文翻译、高清扫描复核和独立审校。"
            "发布门禁逐页检查正文完整性、审校证据、状态一致性、专名与数字保留、未决占位符和摘要漂移；"
            "当前 132 页全部 accepted。</p>"
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
        "issue_id": "lastsupplementto00unse",
        "title": "The Last Supplement to The Whole Earth Catalog, March 1971",
        "display_title": "最后一期《全球概览》增刊 · 1971 年 3 月",
        "subtitle": "中文对照阅读室 · 132 页忠实全文翻译 · 全册高清复核完成",
        "scan_url": "https://archive.org/download/lastsupplementto00unse/page/n{leaf}_w500.jpg",
        "archive_page_url": "https://archive.org/details/lastsupplementto00unse/page/n{leaf}",
        "leaf_min": 0,
        "leaf_total": 131,
        "printed_page_rules": [{"leaf_start": 2, "leaf_end": 129, "printed_start": 1}],
        "printed_pages": {
            str(row["leaf"]): printed_page(row)
            for row in rows
            if printed_page(row) is not None
        },
        "translation_source": "content/translations/lastsupplementto00unse",
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
        raise SystemExit(f"March 1971 release gate failed ({len(errors)} issues):\n{preview}")
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
