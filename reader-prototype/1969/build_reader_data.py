#!/usr/bin/env python3
"""Build the Spring 1969 Chinese reading-room data from accepted leaf translations."""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ISSUE_ID = "wholeearthcatalo00unse_10"
TRANSLATION_ROOT = ROOT / "content" / "translations" / ISSUE_ID
STATUS_PATH = TRANSLATION_ROOT / "status.jsonl"
LEAF_DIR = TRANSLATION_ROOT / "leaves"
OUT = HERE / "data" / "reader.json"

SECTION_TITLES = {
    "Front Matter": "封面、目录与运作办法",
    "Understanding Whole Systems": "整体系统",
    "Shelter and Land Use": "庇护所与土地利用",
    "Industry and Craft": "工业与手艺",
    "Communications": "传播",
    "Community": "共同体",
    "Nomadics": "游牧",
    "Learning": "学习",
    "Back Matter": "广告、表单与封底",
}
SECTION_ORDER = list(SECTION_TITLES)

NAV_TITLES = {
    "Front Matter": "封面与办法",
    "Understanding Whole Systems": "整体系统",
    "Shelter and Land Use": "庇护所与土地利用",
    "Industry and Craft": "工业与手艺",
    "Communications": "传播",
    "Community": "共同体",
    "Nomadics": "游牧",
    "Learning": "学习",
    "Back Matter": "表单与封底",
}

CHAPTER_SUMMARIES = {
    "Front Matter": "封面、功能与宗旨、原刊总目录和《概览》运作办法。这里明确第二期如何筛选工具、接受评介、处理订阅、广告和供应商关系。",
    "Understanding Whole Systems": "从富勒、人口与粮食、阿波罗 8 号地球影像进入地质、形态、控制论和未来研究，建立观察整颗地球的尺度。",
    "Shelter and Land Use": "从空间网格、张力结构和自建住宅，走向乡村技术、气候、园艺、食物、养蜂、风能、圆顶与材料实验。",
    "Industry and Craft": "把工程设计、太阳能、人因与制造业资料，同木工、机械、陶艺、玻璃、制琴、绳结、编织和织机放在同一条实践链上。",
    "Communications": "从生物计算机、媒介与控制论出发，经过数学、计算器、地图、电影电视、电子设备、印刷复制和图书检索。",
    "Community": "将意向社区、土地信息、医疗与药物参考、消费者资料、政府出版物、采购渠道和社会实验组织成可使用的共同体基础设施。",
    "Nomadics": "围绕隐退、生存、露营、背包、户外装备、旅行、温泉、地理探索与自然观察，讨论离开固定住所之后的判断和自持能力。",
    "Learning": "从教育理论、校舍与实验材料进入游戏、计算机、感官训练、心理学、意识研究、瑜伽和创造力，强调亲手试验的学习。",
    "Back Matter": "广告、制作成本、全球卡车商店、重复订阅表、旋转订购单、波托拉研究所说明和封底，共同展示这本目录如何被生产、寄送和继续使用。",
}

READER_GUIDE_SECTIONS = [
    {
        "title": "这是哪一本",
        "html": (
            "<p>这是 1969 年春季出版的第二期 <em>Whole Earth Catalog</em> 中文阅读室。"
            "页面按原书 134 个 access leaf 和本期原刊栏目顺序组织，不套用 1974 年 <em>Epilog</em> 的章节结构。</p>"
        ),
    },
    {
        "title": "第二期在讨论什么",
        "html": (
            "<p>第二期继续从“让个人取得工具”出发，却明显扩大了尺度：阿波罗 8 号的地球影像、人口与粮食危机、"
            "系统论和控制论与住所、土地、乡村技术、工程和手艺并置；计算机、媒介、共同体资源、户外生存、"
            "教育实验和意识探索也都成为同一套个人能力的组成部分。</p>"
        ),
    },
    {
        "title": "怎样使用",
        "html": (
            "<p>右侧呈现经过翻译与独立复核的完整中文内容，左侧保留 Internet Archive 扫描页。"
            "滚动正文或点击“看原页”，扫描页会跟随切换，便于核对版面、图片、表格和上下文。</p>"
            "<p>顶部栏目来自 1969 年春季号自己的原刊目录。每栏可展开 leaf 目录直接跳转；原刊目录页、价格、地址、表格和刊末表单均按验收译稿保留。</p>"
        ),
    },
]

PRINTED_PAGE_RULES = [
    {"leaf_start": 2, "leaf_end": 133, "printed_start": 1},
]

TITLE_OVERRIDES = {
    2: "原刊总目录",
}


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


def inline_md(text: str) -> str:
    breaks: list[str] = []

    def save_break(match: re.Match[str]) -> str:
        breaks.append(match.group(0))
        return f"@@BR{len(breaks) - 1}@@"

    protected = re.sub(r"<br\s*/?>", save_break, text, flags=re.I)
    escaped = html.escape(protected, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    for index in range(len(breaks)):
        escaped = escaped.replace(f"@@BR{index}@@", "<br>")
    return escaped


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_table(lines: list[str]) -> str | None:
    if len(lines) < 2:
        return None
    header = table_cells(lines[0])
    divider = table_cells(lines[1])
    if len(header) != len(divider) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in divider):
        return None
    head = "".join(f"<th>{inline_md(cell)}</th>" for cell in header)
    rows = []
    for line in lines[2:]:
        cells = table_cells(line)
        cells += [""] * (len(header) - len(cells))
        rows.append("<tr>" + "".join(f"<td>{inline_md(cell)}</td>" for cell in cells[: len(header)]) + "</tr>")
    return (
        "<div class='table-wrap'><table><thead><tr>"
        + head
        + "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    quote: list[str] = []
    code: list[str] = []
    ul_open = False
    ol_open = False
    in_code = False
    index = 0

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

    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()

        if in_code:
            if stripped.startswith("```"):
                out.append("<pre><code>" + html.escape("\n".join(code), quote=False) + "</code></pre>")
                code.clear()
                in_code = False
            else:
                code.append(line)
            index += 1
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            flush_quote()
            close_lists()
            in_code = True
            index += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            cursor = index
            while cursor < len(lines) and lines[cursor].strip().startswith("|"):
                table_lines.append(lines[cursor].strip())
                cursor += 1
            table_html = render_table(table_lines)
            if table_html:
                flush_paragraph()
                flush_quote()
                close_lists()
                out.append(table_html)
                index = cursor
                continue

        if not stripped:
            flush_paragraph()
            flush_quote()
            close_lists()
            index += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_quote()
            close_lists()
            level = min(max(len(heading.group(1)) + 2, 3), 5)
            out.append(f"<h{level}>{inline_md(heading.group(2).strip())}</h{level}>")
            index += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            close_lists()
            quote.append(stripped[1:].strip())
            index += 1
            continue

        if re.match(r"^[-*+]\s+", stripped):
            flush_paragraph()
            flush_quote()
            if ol_open:
                out.append("</ol>")
                ol_open = False
            if not ul_open:
                out.append("<ul>")
                ul_open = True
            item = re.sub(r"^[-*+]\s+", "", stripped)
            out.append(f"<li>{inline_md(item)}</li>")
            index += 1
            continue

        numbered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if numbered:
            flush_paragraph()
            flush_quote()
            if ul_open:
                out.append("</ul>")
                ul_open = False
            if not ol_open:
                out.append("<ol>")
                ol_open = True
            out.append(f"<li>{inline_md(numbered.group(1))}</li>")
            index += 1
            continue

        flush_quote()
        close_lists()
        paragraph.append(stripped[:-1] + "<br>" if stripped.endswith("\\") else stripped)
        index += 1

    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code), quote=False) + "</code></pre>")
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
    expected = list(range(134))
    actual = [row["leaf"] for row in rows]
    if actual != expected:
        raise ValueError(f"expected leaves 0-133, got {actual}")
    unaccepted = [row["leaf"] for row in rows if row.get("status") != "accepted"]
    if unaccepted:
        raise ValueError(f"reader data requires accepted translations; blocked leaves: {unaccepted}")
    return rows


def toc_entry(section: dict) -> dict:
    return {
        "title": section["title"],
        "target_id": section["id"],
        "leaf": section["leaf"],
        "printed_page": section["printed_page"],
    }


def build_payload(rows: list[dict]) -> dict:
    grouped: dict[str, list[dict]] = {key: [] for key in SECTION_ORDER}
    for row in rows:
        if row["section"] not in grouped:
            raise ValueError(f"unknown source section: {row['section']}")
        grouped[row["section"]].append(row)

    chapters = []
    for index, source_section in enumerate(SECTION_ORDER):
        items = grouped[source_section]
        if not items:
            continue
        chapter_id = f"ch{index + 1:02d}"
        sections = []
        for row in items:
            leaf = row["leaf"]
            path = LEAF_DIR / f"leaf_{leaf:03d}.md"
            raw_body = final_translation(path.read_text(), leaf)
            if leaf in TITLE_OVERRIDES:
                title, body = TITLE_OVERRIDES[leaf], raw_body
            else:
                title, body = split_display_title(raw_body, f"leaf {leaf}")
            sections.append(
                {
                    "title": title,
                    "html": markdown_to_html(body),
                    "leaf": leaf,
                    "leaf_start": leaf,
                    "leaf_end": leaf,
                    "printed_page": printed_page(leaf),
                    "id": f"{chapter_id}-leaf-{leaf:03d}",
                    "translation_status": row["status"],
                    "qa_flags": row.get("qa_flags", []),
                    "review_path": row.get("review_path"),
                    "translation_path": row.get("translation_path"),
                }
            )
        chapters.append(
            {
                "title": SECTION_TITLES[source_section],
                "nav_title": NAV_TITLES[source_section],
                "source_section": source_section,
                "summary": CHAPTER_SUMMARIES[source_section],
                "sections": sections,
                "toc": [toc_entry(section) for section in sections],
                "id": chapter_id,
                "leaf_start": items[0]["leaf"],
                "leaf_end": items[-1]["leaf"],
            }
        )

    status_counts = Counter(row["status"] for row in rows)
    return {
        "issue_id": ISSUE_ID,
        "title": "Whole Earth Catalog, Spring 1969",
        "scan_url": f"https://archive.org/download/{ISSUE_ID}/page/n{{leaf}}_w500.jpg",
        "archive_page_url": f"https://archive.org/details/{ISSUE_ID}/page/n{{leaf}}",
        "leaf_min": 0,
        "leaf_total": 133,
        "printed_page_rules": PRINTED_PAGE_RULES,
        "translation_source": f"content/translations/{ISSUE_ID}",
        "translation_status_counts": dict(status_counts),
        "preface": {"title": "导读", "sections": READER_GUIDE_SECTIONS},
        "chapters": chapters,
    }


def main() -> None:
    output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else OUT
    payload = build_payload(load_status())
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    section_count = sum(len(chapter["sections"]) for chapter in payload["chapters"])
    print(f"chapters={len(payload['chapters'])} sections={section_count}")
    print(f"statuses={payload['translation_status_counts']}")
    print(f"wrote {output} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
