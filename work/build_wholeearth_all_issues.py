#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work" / "wholeearth"
OUT = ROOT / "outputs"
WORK.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

INDEX_URL = "https://wholeearth.info/"
OUT_JSON = OUT / "wholeearth_all_issues_guides.json"
OUT_DETAIL_JSON = OUT / "wholeearth_all_issues_content_maps.json"
OUT_HTML = OUT / "wholeearth_all_issues_reading_room.html"
OCR = WORK / "ocr"
OCR.mkdir(parents=True, exist_ok=True)

COLLECTION_ZH = {
    "Whole Earth Catalogs": "Whole Earth 目录系列",
    "Whole Earth Catalog": "Whole Earth 目录系列",
    "CoEvolution Quarterly": "共同进化季刊",
    "Whole Earth Software Review": "软件目录与评论",
    "Whole Earth Review": "Whole Earth Review",
    "Whole Earth Magazine": "Whole Earth Magazine",
    "Special Publications": "专题出版物",
}

COLLECTION_HINTS = {
    "Whole Earth Catalogs": "工具、书籍、技术与生活实践的总目录",
    "Whole Earth Catalog": "工具、书籍、技术与生活实践的总目录",
    "CoEvolution Quarterly": "生态、系统思想、文化实验与长期主义",
    "Whole Earth Software Review": "个人电脑软件、硬件、在线服务和工具评测",
    "Whole Earth Review": "工具文化、环境、电脑时代与社会议题",
    "Whole Earth Magazine": "专题化的生态、地方、教育、设计和社会观察",
    "Special Publications": "围绕单一主题展开的特别册或专题书",
}

KEYWORDS = [
    ("computer", "计算机"),
    ("software", "软件"),
    ("network", "网络"),
    ("internet", "互联网"),
    ("cyber", "控制论/网络文化"),
    ("ecology", "生态"),
    ("energy", "能源"),
    ("design", "设计"),
    ("learning", "学习"),
    ("education", "教育"),
    ("tools", "工具"),
    ("community", "社区"),
    ("place", "地方"),
    ("food", "食物"),
    ("soil", "土壤"),
    ("water", "水"),
    ("fire", "火"),
    ("gaia", "盖亚"),
    ("green", "绿色运动"),
    ("future", "未来"),
    ("building", "建造"),
    ("health", "健康"),
    ("women", "女性"),
    ("war", "战争"),
    ("communication", "通信"),
]

TOPIC_LENSES = {
    "计算机": "计算机如何从专业机器变成个人工具",
    "软件": "软件如何塑造新的工作、学习和审美实践",
    "网络": "网络连接怎样改变协作和知识流动",
    "互联网": "早期互联网文化与公共知识空间",
    "控制论/网络文化": "控制论、反馈和网络社会想象",
    "生态": "生态系统、地方知识和长期实践",
    "能源": "能源选择与日常生活技术",
    "设计": "设计作为工具、环境和生活方式的组织方法",
    "学习": "自学、教育实验和开放知识",
    "教育": "学校之外的学习路径",
    "工具": "工具如何扩大个人和社区的行动能力",
    "社区": "社区组织、互助和地方实践",
    "地方": "地点、土地和真实生活场景",
    "食物": "食物生产、饮食和生态关系",
    "土壤": "土壤、农业和修复性实践",
    "水": "水资源、环境和基础设施",
    "火": "火、能源和风险治理",
    "盖亚": "盖亚假说与整体系统视角",
    "绿色运动": "绿色运动的工具、伦理和实践",
    "未来": "未来想象与可操作的改变",
    "建造": "建造、居住和材料实践",
    "健康": "身体、健康和替代性照护",
    "女性": "女性经验、劳动与社会结构",
    "战争": "战争、技术和公共伦理",
    "通信": "通信工具与社会组织方式",
}

TOC_HINTS = [
    ("computer", "计算机"),
    ("software", "软件"),
    ("program", "编程"),
    ("network", "网络"),
    ("online", "在线社区"),
    ("ecolog", "生态"),
    ("energy", "能源"),
    ("design", "设计"),
    ("tool", "工具"),
    ("build", "建造"),
    ("garden", "园艺"),
    ("farm", "农业"),
    ("food", "食物"),
    ("water", "水"),
    ("health", "健康"),
    ("education", "教育"),
    ("learning", "学习"),
    ("community", "社区"),
    ("future", "未来"),
    ("review", "评论"),
    ("interview", "访谈"),
]

DETAIL_KEYWORDS = [
    ("program", "编程", "把规则、流程和表达方式组织成可执行的工具"),
    ("software", "软件", "软件选择、使用经验和个人电脑生态"),
    ("computer", "计算机", "个人计算机如何进入工作、学习和日常生活"),
    ("network", "网络", "远程连接、社群通信和信息流动"),
    ("telecommunicat", "通信", "电脑作为通信设备和协作媒介"),
    ("writing", "写作", "文字处理、出版和文本工作方式"),
    ("learning", "学习", "自学、儿童教育和可试错的学习环境"),
    ("education", "教育", "学校之外的知识组织与学习实验"),
    ("design", "设计", "设计如何组织工具、环境和行动"),
    ("drawing", "绘图", "图像、制图和视觉思考"),
    ("database", "数据库", "信息保存、检索和组织的代价"),
    ("organizing", "组织", "在信息过载中建立秩序"),
    ("energy", "能源", "能源工具、替代技术和生活基础设施"),
    ("ecolog", "生态", "生态系统、环境伦理和长期尺度"),
    ("garden", "园艺", "种植、土地照料和日常实践"),
    ("farm", "农业", "农业工具、食物生产和土地关系"),
    ("food", "食物", "食物系统、家庭实践和地方经验"),
    ("health", "健康", "身体、照护和替代性健康资源"),
    ("shelter", "居住", "住所、土地使用和建造实践"),
    ("building", "建造", "材料、结构和自己动手的建造方法"),
    ("community", "社区", "共同生活、地方组织和互助网络"),
    ("politic", "政治", "公共生活、制度和行动策略"),
    ("women", "女性", "女性经验、劳动和社会结构"),
    ("war", "战争", "技术、战争和公共伦理"),
    ("review", "评论", "对工具、书籍或软件的判断与推荐"),
    ("interview", "访谈", "通过人物经验进入一个议题"),
]

CATALOG_ANCHORS = [
    "Whole Systems",
    "Shelter and Land Use",
    "Community",
    "Communications",
    "Industry and Craft",
    "Nomadics",
    "Learning",
]

GENERIC_OCR_HEADINGS = {
    "function",
    "purpose",
    "good",
    "goodbye",
    "riddance",
    "dany",
    "contents",
    "index",
    "continued",
    "advertisement",
    "subscription",
    "page",
}


class Logger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = self.path.open("w", encoding="utf-8")

    def log(self, msg: str) -> None:
        line = f"[{time.strftime('%Y-%m-%d %H:%M:%S %Z')}] {msg}"
        print(line, flush=True)
        self.fh.write(line + "\n")
        self.fh.flush()

    def close(self) -> None:
        self.fh.close()


def fetch(url: str, dest: Path, log: Logger) -> str:
    log.log(f"fetch url={url}")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as r:
        data = r.read()
    dest.write_bytes(data)
    text = data.decode("utf-8", errors="replace")
    log.log(f"wrote path={dest} bytes={len(data)}")
    return text


def fetch_archive_text(identifier: str, log: Logger) -> str:
    if not identifier:
        return ""
    dest = OCR / f"{identifier}_djvu.txt"
    if dest.exists() and dest.stat().st_size > 2000:
        return dest.read_text(encoding="utf-8", errors="replace")
    url = f"https://archive.org/download/{identifier}/{identifier}_djvu.txt"
    log.log(f"fetch_ocr identifier={identifier}")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=45) as r:
            data = r.read()
    except (HTTPError, URLError, TimeoutError) as exc:
        log.log(f"ocr_unavailable identifier={identifier} error={type(exc).__name__}")
        return ""
    dest.write_bytes(data)
    log.log(f"wrote_ocr path={dest} bytes={len(data)}")
    return data.decode("utf-8", errors="replace")


def extract_next_json(index_html: str) -> dict:
    match = re.search(
        r'<script\b[^>]*\bid=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>',
        index_html,
        re.S,
    )
    if not match:
        raise RuntimeError("Could not find __NEXT_DATA__ payload in wholeearth.info index")
    return json.loads(html.unescape(match.group(1)))


def find_issue_list(payload: object):
    best = []

    def walk(node):
        nonlocal best
        if isinstance(node, list):
            issue_like = [
                item for item in node
                if isinstance(item, dict) and "title" in item and "slug" in item and ("identifier" in item or "link" in item)
            ]
            if len(issue_like) > len(best):
                best = issue_like
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)

    walk(payload)
    if not best:
        raise RuntimeError("Could not locate issue list in Next.js payload")
    return best


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def issue_url(issue: dict) -> str:
    slug = issue.get("slug")
    return f"https://wholeearth.info/p/{slug}" if slug else INDEX_URL


def cover_url(issue: dict) -> str:
    ident = issue.get("identifier")
    if ident:
        return f"https://archive.org/download/{ident}/page/cover_w500.jpg"
    link = issue.get("link", "")
    ident = link.rstrip("/").split("/")[-1] if "archive.org/details/" in link else ""
    return f"https://archive.org/download/{ident}/page/cover_w500.jpg" if ident else ""


def extract_topics(issue: dict) -> list[str]:
    text = " ".join([
        issue.get("title", ""),
        issue.get("summary", ""),
        issue.get("toc", ""),
        issue.get("collection", ""),
    ]).lower()
    topics = [zh for en, zh in KEYWORDS if en in text]
    if not topics:
        collection = issue.get("collection", "")
        if collection in COLLECTION_HINTS:
            topics.append(COLLECTION_HINTS[collection].split("、")[0])
    return topics[:4]


def toc_lines(issue: dict) -> list[str]:
    toc = strip_tags(issue.get("toc", ""))
    if not toc:
        return []
    parts = [p.strip() for p in re.split(r"\\n|\n|;", toc) if p.strip()]
    return parts[:8]


def toc_hint(line: str) -> str:
    lowered = line.lower()
    hits = [zh for en, zh in TOC_HINTS if en in lowered]
    if hits:
        return "中文线索：" + "、".join(dict.fromkeys(hits[:3])) + "。原目录题名：" + line[:96]
    return "中文线索：这是一条需结合原扫描细读的目录项。原目录题名：" + line[:96]


def detail_focus(title: str, fallback_topics: list[str]) -> tuple[str, str]:
    lowered = title.lower()
    hits = [(zh, lens) for key, zh, lens in DETAIL_KEYWORDS if key in lowered]
    if hits:
        zh, lens = hits[0]
        return zh, lens
    if fallback_topics:
        topic = fallback_topics[0]
        return topic, TOPIC_LENSES.get(topic, topic)
    return "工具文化", "工具、经验和时代议题之间的关系"


def clean_heading(line: str) -> str:
    line = html.unescape(line)
    line = re.sub(r"\s+", " ", line.strip())
    line = re.sub(r"^[^\w\u4e00-\u9fff]+|[^\w\u4e00-\u9fff?.!:'’\")]+$", "", line)
    return line.strip()


def is_ocr_heading(line: str) -> bool:
    line = clean_heading(line)
    if len(line) < 4 or len(line) > 96:
        return False
    if line.startswith(("_", ".", ",")):
        return False
    if re.fullmatch(r"[\d\s.,:/-]+", line):
        return False
    if re.search(r"https?://|www\.|@|ISBN|^\d+$|Digitized by|Internet Archive|Creative Commons", line, re.I):
        return False
    if re.search(r"__|={2,}|[<>]|[{}]|\b(?:poh|pra|maint|als)\b", line, re.I):
        return False
    if len(re.findall(r"[^A-Za-z0-9\u4e00-\u9fff\s'&.,:;!?()/-]", line)) > 2:
        return False
    letters = re.findall(r"[A-Za-z]", line)
    if len(letters) < 4:
        return False
    words = re.findall(r"[A-Za-z][A-Za-z'&.-]*", line)
    if not words or len(words) > 12:
        return False
    if line.lower().strip(" .!?") in GENERIC_OCR_HEADINGS:
        return False
    if len(words) == 1 and words[0].isupper():
        return False
    if len(words) <= 3 and re.match(r"^\d", line):
        return False
    upper_ratio = sum(1 for c in letters if c.isupper()) / max(1, len(letters))
    title_case_words = sum(1 for w in words if w[:1].isupper())
    if upper_ratio >= 0.58:
        return True
    if title_case_words >= max(2, int(len(words) * 0.62)) and len(words) <= 8:
        return True
    if line.endswith("?") and len(words) <= 10:
        return True
    return False


def split_toc_entries(toc: list[str]) -> list[str]:
    entries = []
    for line in toc:
        found = re.findall(r"([A-Za-z][A-Za-z0-9 '&/.,!?-]{2,}?):\s*\d{1,4}", line)
        if found:
            entries.extend(clean_heading(x) for x in found)
            continue
        parts = [clean_heading(x) for x in re.split(r"\s{2,}|;| / ", line) if clean_heading(x)]
        entries.extend(parts)
    return [x for x in entries if x][:24]


def ocr_headings(text: str, collection: str) -> list[dict]:
    if not text:
        return []
    anchors = []
    lowered = text.lower()
    if "Catalog" in collection:
        for anchor in CATALOG_ANCHORS:
            if anchor.lower() in lowered:
                anchors.append(anchor)
    seen = set()
    headings = []
    for raw in text.splitlines():
        line = clean_heading(raw)
        if not is_ocr_heading(line):
            continue
        key = re.sub(r"[^a-z0-9]+", "", line.lower())
        if key in seen:
            continue
        seen.add(key)
        headings.append(line)
        if len(headings) >= 80:
            break
    merged = []
    merged_keys = set()
    for title in anchors + headings:
        key = re.sub(r"[^a-z0-9]+", "", title.lower())
        if key and key not in merged_keys:
            merged.append(title)
            merged_keys.add(key)
    return [{"title": x, "source": "ocr"} for x in merged[:18]]


def make_content_map(guide: dict, ocr_text: str = "") -> list[dict]:
    entries = [{"title": x, "source": "toc"} for x in split_toc_entries(guide.get("toc", []))]
    if len(entries) < 8:
        entries.extend(ocr_headings(ocr_text, guide.get("collection", "")))
    units = []
    seen = set()
    for item in entries:
        title = clean_heading(item["title"])
        key = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", title.lower())
        if not key or key in seen:
            continue
        seen.add(key)
        topic, lens = detail_focus(title, guide.get("topics", []))
        source_zh = "目录" if item["source"] == "toc" else "OCR 标题"
        units.append({
            "title": title,
            "source": item["source"],
            "topic": topic,
            "summary_zh": f"从这个入口可以看“{lens}”。先看标题在提出什么问题，再回到扫描页看它旁边的图片、边栏、推荐语和地址信息。",
            "reading_note": "重点问：它解决什么实际问题？它依赖怎样的社区、媒介或生活方式？今天还剩下什么启发？",
        })
        if len(units) >= 16:
            break
    if not units:
        topic, lens = detail_focus(guide["title"], guide.get("topics", []))
        units.append({
            "title": "本期整体内容",
            "source": "metadata",
            "topic": topic,
            "summary_zh": f"这一期适合先整体浏览，把它看作关于“{lens}”的资料包。",
            "reading_note": "重点记录：反复出现的工具类型、推荐语气、图片材料和读者行动入口。",
        })
    return units


def source_label(source: str) -> str:
    labels = {
        "toc+ocr": "目录 + OCR",
        "toc": "目录",
        "ocr": "OCR 标题",
        "metadata": "元数据",
    }
    return labels.get(source, source or "内容线索")


def pick_preview_units(units: list[dict]) -> list[dict]:
    preferred = []
    fallback = []
    for unit in units:
        title = unit.get("title", "")
        if re.search(r"\b(?:Introduction|Programming|Learning|Whole Systems|Shelter|Community|Communications|Writing|Telecommunicating|Ecology|Tools|Design|Interview)\b", title, re.I):
            preferred.append(unit)
        else:
            fallback.append(unit)
    picked = []
    seen = set()
    for unit in preferred + fallback:
        key = re.sub(r"[^a-z0-9]+", "", unit.get("title", "").lower())
        if key in seen:
            continue
        seen.add(key)
        picked.append(unit)
        if len(picked) == 4:
            break
    return picked


def issue_lens(collection: str, topics: list[str]) -> str:
    if topics:
        picked = topics[:3]
        lenses = [TOPIC_LENSES.get(topic, topic) for topic in picked]
        return "；".join(lenses)
    return COLLECTION_HINTS.get(collection, "Whole Earth 式工具文化和实践知识")


def make_guide(issue: dict) -> dict:
    collection = issue.get("collection", "Unknown")
    summary = strip_tags(issue.get("summary", ""))
    topics = extract_topics(issue)
    toc = toc_lines(issue)
    year = issue.get("year")
    season = issue.get("season") or ""
    pages = issue.get("pages")
    zh_collection = COLLECTION_ZH.get(collection, collection)
    title = strip_tags(issue.get("title", "Untitled"))
    period = " ".join(str(x) for x in [season, year] if x).strip()

    lead_bits = []
    if period:
        lead_bits.append(f"出版时间：{period}")
    lead_bits.append(f"系列：{zh_collection}")
    if pages:
        lead_bits.append(f"页数：约 {pages} 页")
    lead = "；".join(lead_bits) + "。"

    lens_text = issue_lens(collection, topics)
    if toc:
        lens = "阅读顺序建议：先看封面和目录，再围绕这些中文线索进入：" + "；".join(toc_hint(item).split("。", 1)[0].replace("中文线索：", "") for item in toc[:4]) + "。"
    elif summary:
        lens = f"阅读顺序建议：先把它看作一张关于“{lens_text}”的时代切片，再打开原扫描核对图片、版式和语境。"
    else:
        lens = f"本期缺少摘要和目录，建议从封面、页数和 {zh_collection} 的系列脉络进入。"

    if topics:
        topic_sentence = "主题标签：" + "、".join(topics) + "。"
    else:
        topic_sentence = "主题标签：待从原始扫描细读补充。"

    guide = f"{lead}{topic_sentence}本期的中文读法：{lens_text}。{lens}"
    return {
        "title": title,
        "slug": issue.get("slug", ""),
        "identifier": issue.get("identifier", ""),
        "collection": collection,
        "collection_zh": zh_collection,
        "year": year,
        "season": season,
        "pages": pages,
        "editor": strip_tags(issue.get("editor", "")),
        "summary": summary,
        "summary_zh": f"中文摘要：本期属于{zh_collection}，核心可读作“{lens_text}”。它的价值不是单篇知识点，而是把工具、实践经验、图片和时代议题组织成一张可漫游的阅读地图。",
        "toc": toc,
        "toc_zh": [toc_hint(item) for item in toc],
        "topics": topics,
        "guide_zh": guide,
        "url": issue_url(issue),
        "archive_url": issue.get("link", ""),
        "pdf_url": f"https://archive.org/download/{issue.get('identifier')}/{issue.get('identifier')}.pdf" if issue.get("identifier") else "",
        "cover_url": cover_url(issue),
    }


def enrich_guides_with_content_maps(guides: list[dict], log: Logger, fetch_ocr: bool) -> list[dict]:
    total = len(guides)
    start = time.time()
    for idx, guide in enumerate(guides, start=1):
        text = fetch_archive_text(guide["identifier"], log) if fetch_ocr else ""
        guide["content_map"] = make_content_map(guide, text)
        guide["content_source"] = (
            "toc+ocr" if guide.get("toc") and text else
            "toc" if guide.get("toc") else
            "ocr" if text else
            "metadata"
        )
        if idx == 1 or idx % 10 == 0 or idx == total:
            elapsed = max(0.01, time.time() - start)
            speed = idx / elapsed
            remaining = (total - idx) / speed if speed else 0
            log.log(f"content_progress done={idx}/{total} speed={speed:.2f}_issues_per_sec eta_sec={remaining:.0f}")
    return guides


def render_html(guides: list[dict], log: Logger) -> str:
    collections = Counter(g["collection_zh"] for g in guides)
    years = [g["year"] for g in guides if isinstance(g.get("year"), int)]
    min_year = min(years) if years else ""
    max_year = max(years) if years else ""
    collection_options = "\n".join(
        f'<button class="filter-chip" type="button" data-collection="{html.escape(name)}">{html.escape(name)} <span>{count}</span></button>'
        for name, count in collections.most_common()
    )

    collection_sections = []
    by_collection = defaultdict(list)
    for guide in guides:
        by_collection[guide["collection_zh"]].append(guide)
    for name, items in sorted(by_collection.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        collection_sections.append(
            f'<article class="series-item reveal"><div><strong>{html.escape(name)}</strong><span>{len(items)} 本</span></div>'
            f'<p>{html.escape(COLLECTION_HINTS.get(items[0]["collection"], "这一组刊物需要按封面、目录和原始扫描继续细读。"))}</p></article>'
        )

    cards = []
    for idx, g in enumerate(guides):
        topics = "".join(f'<span class="topic">{html.escape(t)}</span>' for t in g["topics"])
        search_text = " ".join([
            g["title"],
            g["guide_zh"],
            " ".join(g["topics"]),
            " ".join(unit["title"] + " " + unit.get("summary_zh", "") for unit in g.get("content_map", [])),
        ]).lower()
        toc = ""
        if g["toc"]:
            toc_items = "".join(f"<li>{html.escape(item)}</li>" for item in g.get("toc_zh", [])[:5])
            toc = f"<details><summary>目录线索</summary><ul>{toc_items}</ul></details>"
        content_units = g.get("content_map", [])
        content_cards = ""
        if content_units:
            preview_items = []
            for unit in pick_preview_units(content_units):
                preview_items.append(
                    f'<li><span>{html.escape(unit.get("topic", "入口"))}</span>'
                    f'<div><strong>{html.escape(unit["title"])}</strong>'
                    f'<p>{html.escape(unit["summary_zh"])}</p></div></li>'
                )
            unit_html = []
            for unit in content_units:
                unit_html.append(
                    f'<li><div><span>{html.escape(unit.get("topic", "内容"))}</span>'
                    f'<strong>{html.escape(unit["title"])}</strong></div>'
                    f'<p>{html.escape(unit["summary_zh"])}</p>'
                    f'<p class="reading-note">{html.escape(unit["reading_note"])}</p></li>'
                )
            content_cards = (
                f'<section class="reading-path"><div class="path-head"><span>建议先看</span><strong>{len(preview_items)} 个入口</strong></div>'
                f'<ol>{"".join(preview_items)}</ol></section>'
                f'<details class="content-map">'
                f'<summary>展开完整内容地图 <span>{len(content_units)} 个板块/条目线索 · {html.escape(source_label(g.get("content_source", "metadata")))}</span></summary>'
                f'<ol>{"".join(unit_html)}</ol></details>'
            )
        summary = f'<p class="summary">{html.escape(g["summary_zh"])}</p>' if g.get("summary_zh") else ""
        editor = f'<span>Editor: {html.escape(g["editor"])}</span>' if g["editor"] else ""
        cards.append(f"""
        <article class="issue-card reveal" style="--index:{idx % 12}" data-collection="{html.escape(g["collection_zh"])}" data-year="{g.get("year") or ""}" data-text="{html.escape(search_text)}">
          <a class="cover" href="{html.escape(g["url"])}" target="_blank" rel="noreferrer"><img loading="lazy" src="{html.escape(g["cover_url"])}" alt="{html.escape(g["title"])} cover"></a>
          <div class="issue-body">
            <div class="meta"><span>{html.escape(g["collection_zh"])}</span><span>{html.escape(str(g.get("year") or ""))}</span>{editor}</div>
            <h3>{html.escape(g["title"])}</h3>
            <p class="guide">{html.escape(g["guide_zh"])}</p>
            {summary}
            <div class="topics">{topics}</div>
            {toc}
            {content_cards}
            <div class="links"><a href="{html.escape(g["url"])}" target="_blank" rel="noreferrer">Whole Earth 页面</a><a href="{html.escape(g["archive_url"])}" target="_blank" rel="noreferrer">Internet Archive</a></div>
          </div>
        </article>
        """)

    css = r"""
    :root {
      --canvas: #F4F2ED;
      --surface: #FFFFFF;
      --soft: #FAFAF7;
      --ink: #272B2D;
      --heading: #151719;
      --muted: #6F7477;
      --border: #DBD8CF;
      --rule: rgba(21,23,25,.11);
      --accent-bg: #E8EFEA;
      --accent-text: #315A42;
      --blue-bg: #E8EEF4;
      --blue-text: #36546D;
      --yellow-bg: #F3E8C9;
      --yellow-text: #725719;
      --sans: "Avenir Next", "SF Pro Display", "Geist Sans", "Helvetica Neue", "Microsoft YaHei", sans-serif;
      --serif: "Newsreader", "Lyon Text", "Songti SC", "SimSun", Georgia, serif;
      --mono: "Geist Mono", "SF Mono", "JetBrains Mono", "Courier New", monospace;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: var(--canvas);
      color: var(--ink);
      font-family: var(--sans);
      letter-spacing: 0;
    }
    a { color: inherit; }
    .shell { max-width: 1360px; margin: 0 auto; padding: 0 24px 64px; }
    .hero {
      display: none;
    }
    .topbar {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 18px;
      align-items: center;
      min-height: 56px;
      padding: 10px 0;
      border-bottom: 1px solid var(--rule);
    }
    .brand {
      display: flex;
      align-items: baseline;
      gap: 12px;
      min-width: 0;
    }
    .brand strong {
      color: var(--heading);
      font: 700 16px/1 var(--sans);
    }
    .brand span {
      color: var(--muted);
      font: 12px/1.3 var(--mono);
    }
    .reader-layout {
      display: grid;
      grid-template-columns: 286px minmax(0, 1fr);
      gap: 30px;
      align-items: start;
    }
    .reader-rail {
      position: sticky;
      top: 0;
      max-height: 100dvh;
      overflow: auto;
      padding: 16px 0 24px;
      border-right: 1px solid var(--border);
    }
    .eyebrow, .tag, .topic {
      width: fit-content;
      border-radius: 9999px;
      padding: 6px 10px;
      font: 700 11px/1 var(--mono);
      letter-spacing: .05em;
      text-transform: uppercase;
    }
    .eyebrow { background: var(--yellow-bg); color: var(--yellow-text); }
    .tag { background: var(--blue-bg); color: var(--blue-text); }
    h1 {
      margin: 14px 0 10px;
      max-width: 680px;
      color: var(--heading);
      font-family: var(--serif);
      font-size: clamp(34px, 4.5vw, 56px);
      line-height: 1;
      letter-spacing: -.025em;
      font-weight: 500;
      text-wrap: balance;
    }
    .lede { max-width: 700px; margin: 0; color: var(--ink); font-size: 16px; line-height: 1.75; text-wrap: pretty; }
    .stats {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: 8px 14px;
      max-width: 440px;
    }
    .panel { border: 1px solid var(--border); border-radius: 8px; background: var(--surface); }
    .stat {
      min-width: 82px;
      padding: 0;
      color: var(--muted);
      font-size: 12px;
      text-align: right;
    }
    .stat strong { display: inline; margin: 0 5px 0 0; color: var(--heading); font: 700 15px/1 var(--mono); font-variant-numeric: tabular-nums; }
    .panel { padding: 24px; }
    .controls {
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
      padding: 0 16px 14px 0;
      background: transparent;
      border-bottom: 1px solid var(--border);
    }
    .controls input {
      min-width: 0;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      padding: 13px 14px;
      color: var(--ink);
      font: 15px/1.4 var(--sans);
    }
    .controls input:focus {
      outline: 2px solid rgba(17,17,17,.16);
      outline-offset: 2px;
    }
    .controls button, .filter-chip {
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--surface);
      color: var(--ink);
      padding: 11px 13px;
      font: 13px/1 var(--sans);
      cursor: pointer;
    }
    .controls button.primary {
      border-color: var(--border);
      background: transparent;
      color: var(--heading);
    }
    .controls button:focus-visible, .filter-chip:focus-visible, .links a:focus-visible {
      outline: 2px solid rgba(17,17,17,.18);
      outline-offset: 2px;
    }
    .filter-row { display: grid; gap: 8px; margin: 14px 16px 16px 0; }
    .filter-chip.active { background: var(--accent-bg); color: var(--accent-text); }
    .filter-chip span { color: var(--muted); font-family: var(--mono); margin-left: 4px; }
    .series-strip {
      display: grid;
      gap: 0;
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      background: transparent;
      margin: 0 16px 0 0;
    }
    .series-item {
      min-width: 0;
      background: transparent;
      padding: 12px 8px 12px 0;
      border-bottom: 1px solid var(--border);
    }
    .series-item div {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 10px;
    }
    .series-item strong {
      color: var(--heading);
      font: 600 14px/1.25 var(--sans);
    }
    .series-item span {
      color: var(--muted);
      font: 12px/1 var(--mono);
      white-space: nowrap;
    }
    .series-item p {
      margin: 9px 0 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.55;
    }
    .issue-grid { display: grid; gap: 0; padding-top: 4px; }
    .issue-card {
      display: grid;
      grid-template-columns: 96px minmax(0, 1fr);
      gap: 20px;
      padding: 22px 0;
      border: 0;
      border-bottom: 1px solid var(--border);
      border-radius: 0;
      background: transparent;
      transition: transform 200ms ease, box-shadow 200ms ease;
    }
    .issue-card:hover { transform: none; box-shadow: none; }
    .issue-card.hidden { display: none; }
    .cover {
      display: block;
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: 4px;
      background: var(--soft);
      aspect-ratio: 3 / 4;
    }
    .cover img {
      display: block;
      width: 100%;
      height: 100%;
      object-fit: cover;
      filter: grayscale(.18) saturate(.72) contrast(1.02);
    }
    .meta { display: flex; flex-wrap: wrap; gap: 10px; color: var(--muted); font: 12px/1.3 var(--mono); }
    .issue-card h3 {
      margin: 8px 0 10px;
      color: var(--heading);
      font: 500 clamp(23px, 2.5vw, 30px)/1.12 var(--serif);
      letter-spacing: -.02em;
    }
    .guide, .summary { margin: 0 0 12px; max-width: 76ch; line-height: 1.72; }
    .summary { color: var(--muted); }
    .topics { display: flex; flex-wrap: wrap; gap: 6px; margin: 14px 0; }
    .topic { background: var(--blue-bg); color: var(--blue-text); font-size: 10px; }
    details {
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      padding: 10px 0;
      margin: 12px 0;
    }
    summary { cursor: pointer; color: var(--heading); font-weight: 600; }
    details ul { margin: 10px 0 0; padding-left: 18px; color: var(--muted); line-height: 1.7; }
    .reading-path {
      border-top: 1px solid var(--border);
      padding-top: 12px;
      margin: 14px 0;
    }
    .path-head {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 6px;
    }
    .path-head span {
      color: var(--muted);
      font: 700 11px/1 var(--mono);
      letter-spacing: .05em;
      text-transform: uppercase;
    }
    .path-head strong {
      color: var(--heading);
      font: 600 14px/1 var(--sans);
    }
    .reading-path ol {
      display: grid;
      gap: 0;
      margin: 0;
      padding: 0;
      list-style: none;
      border-top: 1px solid var(--border);
    }
    .reading-path li {
      display: grid;
      grid-template-columns: 72px minmax(0, 1fr);
      gap: 12px;
      min-width: 0;
      padding: 10px 0;
      border-bottom: 1px solid var(--border);
    }
    .reading-path li span {
      width: fit-content;
      height: fit-content;
      color: var(--accent-text);
      background: var(--accent-bg);
      border-radius: 4px;
      padding: 5px 7px;
      font: 700 10px/1 var(--mono);
      letter-spacing: .05em;
      text-transform: uppercase;
    }
    .reading-path li strong {
      display: block;
      color: var(--heading);
      font: 600 16px/1.25 var(--sans);
    }
    .reading-path li p {
      margin: 6px 0 0;
      color: var(--ink);
      font-size: 13px;
      line-height: 1.58;
    }
    .content-map {
      background: transparent;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px 12px;
      margin: 12px 0;
    }
    .content-map summary {
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      gap: 8px;
      list-style: none;
    }
    .content-map summary::-webkit-details-marker { display: none; }
    .content-map summary span {
      color: var(--muted);
      font: 12px/1.2 var(--mono);
    }
    .content-map ol {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px 14px;
      margin: 14px 0 0;
      padding: 0;
      list-style: none;
    }
    .content-map li {
      min-width: 0;
      border: 0;
      border-top: 1px solid var(--border);
      border-radius: 0;
      background: transparent;
      padding: 10px 0;
    }
    .content-map li span {
      display: inline-block;
      margin-bottom: 8px;
      color: var(--accent-text);
      background: var(--accent-bg);
      border-radius: 9999px;
      padding: 4px 7px;
      font: 700 10px/1 var(--mono);
      letter-spacing: .05em;
      text-transform: uppercase;
    }
    .content-map li strong {
      display: block;
      color: var(--heading);
      font: 600 16px/1.25 var(--sans);
    }
    .content-map li p {
      margin: 8px 0 0;
      color: var(--ink);
      font-size: 13px;
      line-height: 1.65;
    }
    .content-map .reading-note {
      color: var(--muted);
    }
    .links { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px; }
    .links a {
      color: var(--blue-text);
      text-decoration: none;
      font: 700 12px/1 var(--mono);
    }
    .empty { display: none; margin: 36px 0; padding: 24px; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); color: var(--muted); }
    .empty.show { display: block; }
    .reveal { opacity: 0; transform: translateY(12px); transition: opacity 600ms cubic-bezier(.16,1,.3,1), transform 600ms cubic-bezier(.16,1,.3,1); transition-delay: calc(var(--index, 0) * 35ms); }
    .reveal.visible { opacity: 1; transform: translateY(0); }
    footer { margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--border); color: var(--muted); font-size: 13px; line-height: 1.7; }
    @media (max-width: 900px) {
      .shell { padding: 32px 18px 72px; }
      .topbar { grid-template-columns: 1fr; }
      .stats { justify-content: flex-start; }
      .reader-layout { grid-template-columns: 1fr; }
      .reader-rail { position: static; max-height: none; border-right: 0; border-bottom: 1px solid var(--border); }
      .controls { grid-template-columns: 1fr; }
      .issue-card { grid-template-columns: 88px minmax(0, 1fr); gap: 14px; }
      .content-map ol { grid-template-columns: 1fr; }
    }
    @media (max-width: 560px) {
      .stats { grid-template-columns: 1fr; }
      .issue-card { grid-template-columns: 1fr; }
      .cover { width: 108px; }
      .reading-path li { grid-template-columns: 1fr; gap: 8px; }
      h1 { font-size: clamp(38px, 12vw, 58px); }
    }
    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      .reveal { opacity: 1; transform: none; transition: none; }
    }
    """

    js = r"""
    const cards = Array.from(document.querySelectorAll('.issue-card'));
    const search = document.querySelector('#search');
    const reset = document.querySelector('#reset');
    const empty = document.querySelector('.empty');
    const chips = Array.from(document.querySelectorAll('.filter-chip'));
    const count = document.querySelector('#visible-count');
    let activeCollection = '';

    function applyFilters() {
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      cards.forEach(card => {
        const collectionMatch = !activeCollection || card.dataset.collection === activeCollection;
        const queryMatch = !query || card.dataset.text.includes(query);
        const show = collectionMatch && queryMatch;
        card.classList.toggle('hidden', !show);
        if (show) visible += 1;
      });
      count.textContent = String(visible);
      empty.classList.toggle('show', visible === 0);
    }

    search.addEventListener('input', applyFilters);
    reset.addEventListener('click', () => {
      activeCollection = '';
      search.value = '';
      chips.forEach(chip => chip.classList.remove('active'));
      applyFilters();
      search.focus();
    });
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        activeCollection = chip.dataset.collection === activeCollection ? '' : chip.dataset.collection;
        chips.forEach(item => item.classList.toggle('active', item === chip && activeCollection));
        applyFilters();
      });
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    document.querySelectorAll('.reveal').forEach(item => observer.observe(item));
    applyFilters();
    """

    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Whole Earth 全刊物中文阅读地图</title>
  <style>{css}</style>
</head>
<body>
  <main class="shell">
    <header class="hero">
      <div class="reveal">
        <div class="eyebrow">Whole Earth Index</div>
        <h1>全刊物中文阅读地图</h1>
        <p class="lede">给中文读者的一张 Whole Earth 阅读地图：每本先看“为什么值得读”和 4 个入口，再按需要展开完整内容地图。这里提供导读、释义和原扫描入口，不做全文替代翻译。</p>
      </div>
      <div class="stats reveal">
        <div class="stat"><strong>{len(guides)}</strong>本刊物</div>
        <div class="stat"><strong>{len(collections)}</strong>个系列</div>
        <div class="stat"><strong>{min_year}-{max_year}</strong>年份跨度</div>
        <div class="stat"><strong id="visible-count">{len(guides)}</strong>当前显示</div>
      </div>
    </header>
    <section class="controls">
      <input id="search" type="search" placeholder="搜索：software、生态、通信、学习、Whole Earth Review" aria-label="搜索刊物导读">
      <button class="primary" id="reset" type="button">重置筛选</button>
    </section>
    <div class="filter-row">{collection_options}</div>
    <section class="series-strip">{''.join(collection_sections)}</section>
    <section class="issue-grid">{''.join(cards)}</section>
    <div class="empty">没有匹配的刊物。换一个关键词或重置筛选。</div>
    <footer>数据来自 wholeearth.info 当前索引与 Internet Archive 链接。中文内容为导读、结构化摘要和阅读线索；由于版权限制，没有生成整本刊物的完整中文替代译本。生成时间：{time.strftime('%Y-%m-%d %H:%M:%S %Z')}。</footer>
  </main>
  <script>{js}</script>
</body>
</html>
"""
    log.log(f"rendered html chars={len(doc)} cards={len(cards)} collections={len(collections)}")
    return doc


def qa(guides: list[dict], log: Logger) -> dict:
    issues = len(guides)
    collections = len(set(g["collection_zh"] for g in guides))
    with_url = sum(1 for g in guides if g["url"])
    with_archive = sum(1 for g in guides if g["archive_url"])
    with_chinese = sum(1 for g in guides if re.search(r"[\u4e00-\u9fff]", g["guide_zh"]))
    with_topic = sum(1 for g in guides if g["topics"])
    with_summary_or_toc = sum(1 for g in guides if g["summary"] or g["toc"])
    with_content_map = sum(1 for g in guides if g.get("content_map"))
    content_units = sum(len(g.get("content_map", [])) for g in guides)
    with_ocr_source = sum(1 for g in guides if "ocr" in g.get("content_source", ""))
    html_text = OUT_HTML.read_text(encoding="utf-8") if OUT_HTML.exists() else ""
    result = {
        "issues": issues,
        "collections": collections,
        "with_url": with_url,
        "with_archive": with_archive,
        "with_chinese": with_chinese,
        "with_topic": with_topic,
        "with_summary_or_toc": with_summary_or_toc,
        "with_content_map": with_content_map,
        "content_units": content_units,
        "with_ocr_source": with_ocr_source,
        "html_cards": html_text.count('class="issue-card'),
        "html_content_maps": html_text.count('class="content-map"'),
        "html_has_search": 'id="search"' in html_text,
        "html_has_filters": 'class="filter-chip"' in html_text,
        "status": "PASS",
    }
    if (
        issues < 100
        or with_chinese != issues
        or result["html_cards"] != issues
        or with_content_map != issues
        or result["html_content_maps"] != issues
        or not result["html_has_search"]
    ):
        result["status"] = "FAIL"
    log.log("qa " + json.dumps(result, ensure_ascii=False, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", default="001")
    parser.add_argument("--log", required=True)
    parser.add_argument("--with-content-details", action="store_true")
    parser.add_argument("--skip-ocr", action="store_true")
    args = parser.parse_args()
    logger = Logger(Path(args.log))
    start = time.time()
    try:
        logger.log(f"start round={args.round} pid={os.getpid()} log={args.log}")
        index_path = WORK / f"wholeearth_index_round_{args.round}.html"
        index_html = fetch(INDEX_URL, index_path, logger)
        payload = extract_next_json(index_html)
        issues_raw = find_issue_list(payload)
        logger.log(f"parsed raw_issues={len(issues_raw)}")
        guides = [make_guide(issue) for issue in issues_raw]
        guides.sort(key=lambda g: ((g["year"] if isinstance(g.get("year"), int) else 9999), g["collection_zh"], g["title"]))
        if args.with_content_details:
            guides = enrich_guides_with_content_maps(guides, logger, fetch_ocr=not args.skip_ocr)
        OUT_JSON.write_text(json.dumps(guides, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.log(f"wrote json={OUT_JSON} issues={len(guides)}")
        if args.with_content_details:
            content_maps = [
                {
                    "title": g["title"],
                    "identifier": g["identifier"],
                    "collection_zh": g["collection_zh"],
                    "year": g["year"],
                    "source": g.get("content_source"),
                    "content_map": g.get("content_map", []),
                }
                for g in guides
            ]
            OUT_DETAIL_JSON.write_text(json.dumps(content_maps, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.log(f"wrote detail_json={OUT_DETAIL_JSON} issues={len(content_maps)}")
        html_text = render_html(guides, logger)
        OUT_HTML.write_text(html_text, encoding="utf-8")
        logger.log(f"wrote html={OUT_HTML} bytes={OUT_HTML.stat().st_size}")
        result = qa(guides, logger)
        elapsed = time.time() - start
        logger.log(f"done elapsed_sec={elapsed:.2f} status={result['status']}")
        return 0 if result["status"] == "PASS" else 2
    except Exception as exc:
        logger.log(f"ERROR {type(exc).__name__}: {exc}")
        return 1
    finally:
        logger.close()


if __name__ == "__main__":
    sys.exit(main())
