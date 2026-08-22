#!/usr/bin/env python3
"""Build the Fall 1968 Chinese reading-room data from accepted leaf translations."""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ISSUE_ID = "wholeearthcatalo00unse_8"
TRANSLATION_ROOT = ROOT / "content" / "translations" / ISSUE_ID
STATUS_PATH = TRANSLATION_ROOT / "status.jsonl"
LEAF_DIR = TRANSLATION_ROOT / "leaves"
OUT = HERE / "data" / "reader.json"

SECTION_TITLES = {
    "Front Matter": "封面、目录与使用说明",
    "Understanding Whole Systems": "整体系统",
    "Shelter and Land Use": "庇护所与土地利用",
    "Industry and Craft": "工业与手艺",
    "Communications": "传播",
    "Community": "共同体",
    "Nomadics": "游牧",
    "Learning": "学习",
    "Back Matter": "广告、索引与封底",
}
SECTION_ORDER = list(SECTION_TITLES)

NAV_TITLES = {
    "Front Matter": "封面与说明",
    "Understanding Whole Systems": "整体系统",
    "Shelter and Land Use": "庇护所与土地利用",
    "Industry and Craft": "工业与手艺",
    "Communications": "传播",
    "Community": "共同体",
    "Nomadics": "游牧",
    "Learning": "学习",
    "Back Matter": "索引与封底",
}

CHAPTER_SUMMARIES = {
    "Front Matter": "封面、编者声明、原刊总目录与使用说明。这里说明首刊如何选择工具、处理订购信息，以及读者怎样使用这份目录。",
    "Understanding Whole Systems": "从富勒、地球影像、地质学、系统论、形态与控制论出发，建立观察地球与复杂系统的尺度。",
    "Shelter and Land Use": "围绕结构、住宅、乡村技术、照明、土地、园艺、养蜂与食物生产，连接建造和土地实践。",
    "Industry and Craft": "从工程设计、人体尺度和制造业目录，延伸到工具、能源、摄影、玻璃、皮革、珠饰与纱线。",
    "Communications": "讨论生物计算机、信息论、电子设备、电影电视、维修手册、图书检索和艺术复制品等传播工具。",
    "Community": "汇集共同体实验、医疗参考、土地信息、消费者资料、政府出版物和采购渠道。",
    "Nomadics": "聚焦隐退、生存、露营、背包、户外装备、旅行、温泉、地理探索与自然经验。",
    "Learning": "从教育理论、实验材料、游戏与自制计算机，延伸到感官训练、禅修、心理学、瑜伽与创造力。",
    "Back Matter": "刊末的广告、订购信息、总索引、出版说明与封底内容；这些材料保留了首刊作为工具目录的实际使用方式。",
}

READER_GUIDE_SECTIONS = [
    {
        "title": "这是哪一本",
        "html": (
            "<p>这是 1968 年秋季出版的第一期 <em>Whole Earth Catalog</em> 中文阅读室。"
            "页面按原书 68 个 access leaf 和原刊栏目顺序组织，不把后来年份的章节结构套到首刊上。</p>"
        ),
    },
    {
        "title": "首刊在讨论什么",
        "html": (
            "<p>这本首刊从“让个人取得工具”出发：先借地球影像、地质学、系统论与控制论建立观察尺度，"
            "再进入住所建造、土地利用、乡村技术、工程工具与手艺；随后转向计算机、电子设备、影像和出版，"
            "并把共同体资源、户外生存、教育实验、游戏和意识探索纳入同一份目录。</p>"
        ),
    },
    {
        "title": "怎样使用",
        "html": (
            "<p>右侧呈现经过翻译与独立复核的完整中文内容，左侧保留 Internet Archive 扫描页。"
            "滚动正文或点击“看原页”，扫描页会跟随切换，便于核对版面、图片、表格和上下文。</p>"
            "<p>顶部栏目来自 1968 首刊自身的目录。每栏可展开 leaf 目录直接跳转；原刊目录页与总索引也作为正文完整保留。</p>"
        ),
    },
]

PRINTED_PAGE_RULES = [
    {"leaf_start": 4, "leaf_end": 67, "printed_start": 3},
]

TITLE_OVERRIDES = {
    2: "原刊总目录",
    65: "总索引",
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
        paragraph.append(stripped)
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
    expected = list(range(68))
    actual = [row["leaf"] for row in rows]
    if actual != expected:
        raise ValueError(f"expected leaves 0-67, got {actual}")
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
        "title": "Whole Earth Catalog, Fall 1968",
        "scan_url": f"https://archive.org/download/{ISSUE_ID}/page/n{{leaf}}_w500.jpg",
        "archive_page_url": f"https://archive.org/details/{ISSUE_ID}/page/n{{leaf}}",
        "leaf_min": 0,
        "leaf_total": 67,
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
