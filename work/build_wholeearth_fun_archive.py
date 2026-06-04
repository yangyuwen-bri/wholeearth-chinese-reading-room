#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
SITE = OUT / "wholeearth_fun_archive"
ISSUES_DIR = SITE / "issues"
ROUTES_DIR = SITE / "routes"
LOG_DIR = SITE / "logs"

GUIDES_JSON = OUT / "wholeearth_all_issues_guides.json"
MAPS_JSON = OUT / "wholeearth_all_issues_content_maps.json"

ROUTES = [
    {
        "slug": "programming-is-aesthetic",
        "name": "编程也可以是审美活动",
        "short": "从 1985 的 Programming 进入软件文化",
        "keywords": ["编程", "软件", "programming", "program", "software", "Do It Yourself Software", "language"],
        "color": "red",
    },
    {
        "slug": "tools-for-action",
        "name": "工具如何扩大行动力",
        "short": "Whole Earth 最核心的工具传统",
        "keywords": ["工具", "tool", "craft", "industry", "nomadics", "建造", "设计"],
        "color": "green",
    },
    {
        "slug": "ecology-and-place",
        "name": "生态、土地和地方生活",
        "short": "把技术放回环境和日常实践",
        "keywords": ["生态", "ecolog", "energy", "能源", "water", "soil", "food", "garden", "farm", "地方"],
        "color": "blue",
    },
    {
        "slug": "learning-outside-school",
        "name": "学校之外的学习",
        "short": "自学、儿童教育和开放知识",
        "keywords": ["学习", "教育", "learning", "education", "school", "LOGO"],
        "color": "yellow",
    },
    {
        "slug": "community-networks",
        "name": "社区、网络和通信",
        "short": "从社区通讯到前互联网想象",
        "keywords": ["社区", "通信", "network", "telecommunicat", "online", "BBS", "community"],
        "color": "dark",
    },
    {
        "slug": "future-and-counterculture",
        "name": "未来想象和反主流文化",
        "short": "控制论、绿色运动、战争和公共伦理",
        "keywords": ["未来", "future", "war", "战争", "控制论", "cyber", "女性", "green"],
        "color": "purple",
    },
]


def clean_text(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("—", "-").replace("–", "-").replace("·", "/")


def esc(value: object) -> str:
    return html.escape(clean_text(value), quote=True)


def slugify(value: str) -> str:
    value = clean_text(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "issue"


def issue_slug(issue: dict, used: set[str]) -> str:
    base = slugify(issue.get("slug") or issue.get("title") or issue.get("identifier") or "issue")
    slug = base
    idx = 2
    while slug in used:
        slug = f"{base}-{idx}"
        idx += 1
    used.add(slug)
    return slug


def page_img(identifier: str, page: int) -> str:
    if not identifier:
        return ""
    return f"https://archive.org/download/{identifier}/page/n{page}_w500.jpg"


def unit_text(unit: dict) -> str:
    return " ".join(clean_text(unit.get(k, "")) for k in ["title", "topic", "summary_zh", "reading_note"]).lower()


def route_score(issue: dict, units: list[dict], route: dict) -> int:
    blob = " ".join(
        [
            clean_text(issue.get("title", "")),
            clean_text(issue.get("collection_zh", "")),
            " ".join(clean_text(x) for x in issue.get("topics", [])),
            " ".join(unit_text(u) for u in units[:24]),
        ]
    ).lower()
    return sum(blob.count(k.lower()) for k in route["keywords"])


def unit_matches(unit: dict, route: dict) -> bool:
    text = unit_text(unit)
    return any(k.lower() in text for k in route["keywords"])


def pick_units(units: list[dict], limit: int = 8) -> list[dict]:
    priority = []
    seen = set()
    for unit in units:
        title = clean_text(unit.get("title", "")).strip()
        if not title or title.lower() in seen:
            continue
        seen.add(title.lower())
        score = 0
        text = unit_text(unit)
        for word in ["program", "software", "whole systems", "community", "communications", "learning", "ecology", "energy", "tools", "interview"]:
            if word in text:
                score += 2
        if 5 <= len(title) <= 80:
            score += 1
        priority.append((score, unit))
    priority.sort(key=lambda x: x[0], reverse=True)
    return [unit for _, unit in priority[:limit]]


def is_template_summary(text: object) -> bool:
    value = clean_text(text)
    return (
        "先看标题在提出什么问题" in value
        or "再回到扫描页" in value
        or value.startswith("中文摘要：")
        or "它的价值不是单篇知识点" in value
    )


def unit_teaser(unit: dict) -> str:
    title = clean_text(unit.get("title", "")).strip()
    topic = clean_text(unit.get("topic", "")).strip()
    summary = clean_text(unit.get("summary_zh", "")).strip()
    if summary and not is_template_summary(summary):
        return summary
    if topic:
        return f"{topic} / 打开原刊核对这一条旁边的图片、推荐语和地址。"
    if title:
        return "打开原刊核对这一条的页面语境。"
    return "打开原刊核对页面语境。"


def issue_teaser(issue: dict) -> str:
    units = issue.get("preview_units", [])
    names = [clean_text(u.get("title", "")).strip() for u in units[:3] if clean_text(u.get("title", "")).strip()]
    if names:
        return " / ".join(names)
    topics = [clean_text(t) for t in issue.get("topics", [])[:3]]
    return " / ".join(topics) or clean_text(issue.get("collection_zh", ""))


def css() -> str:
    return r"""
:root {
  --paper: #f3edd9;
  --paper-2: #f9f5e7;
  --ink: #151713;
  --muted: #6c6658;
  --line: rgba(21, 23, 19, .2);
  --red: #c63823;
  --green: #14573d;
  --blue: #1d4f82;
  --yellow: #f3c94a;
  --dark: #11140f;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  letter-spacing: 0;
}
a { color: inherit; }
.shell { max-width: 1320px; margin: 0 auto; padding: 24px 28px 52px; }
.topline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
  padding-bottom: 12px;
  border-bottom: 4px solid var(--ink);
}
.brand { color: var(--green); font: 900 12px/1.1 ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: .08em; }
.smallnav { display: flex; flex-wrap: wrap; gap: 10px; color: var(--muted); font-size: 13px; }
.smallnav a { text-decoration: none; border-bottom: 1px solid var(--line); }
.route-board {
  position: relative;
  min-height: 520px;
  margin-top: 34px;
  border-bottom: 1px solid var(--line);
}
.product-home {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  gap: 18px;
  padding: 20px 0 22px;
  border-bottom: 1px solid var(--line);
}
.route-list {
  display: grid;
  gap: 8px;
  align-content: start;
}
.route-button {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: center;
  border: 2px solid var(--ink);
  background: var(--paper-2);
  padding: 12px;
  text-decoration: none;
  box-shadow: 4px 4px 0 var(--ink);
}
.route-button b { font-size: 17px; line-height: 1.15; }
.route-button span { color: var(--red); font: 900 11px/1 ui-monospace, SFMono-Regular, Menlo, monospace; }
.now-table {
  display: grid;
  grid-template-columns: 1.1fr .9fr;
  gap: 12px;
}
.feature-slice {
  min-height: 292px;
  background: var(--dark);
  color: #fff8e6;
  padding: 22px;
  text-decoration: none;
  display: grid;
  align-content: end;
}
.feature-slice small { color: var(--yellow); font: 900 12px/1 ui-monospace, SFMono-Regular, Menlo, monospace; }
.feature-slice b { display: block; margin: 12px 0 10px; font-size: 42px; line-height: .95; max-width: 9em; }
.feature-slice span { color: #d9d0bc; font-size: 16px; line-height: 1.45; }
.quick-stack {
  display: grid;
  gap: 10px;
}
.quick-slice {
  display: grid;
  grid-template-columns: 76px 1fr;
  gap: 11px;
  padding: 10px;
  background: rgba(255,255,255,.36);
  border: 1px solid var(--line);
  text-decoration: none;
}
.quick-slice img { width: 76px; height: 96px; object-fit: cover; border: 1px solid var(--line); }
.quick-slice small { color: var(--green); font: 900 11px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace; }
.quick-slice b { display: block; margin-top: 6px; font-size: 18px; line-height: 1.1; }
.route-card {
  position: absolute;
  width: 220px;
  min-height: 154px;
  padding: 17px 17px 36px;
  border: 3px solid var(--ink);
  background: var(--paper-2);
  text-decoration: none;
  box-shadow: 7px 7px 0 var(--ink);
  transform: rotate(var(--r));
}
.route-card h2 { margin: 0 0 8px; font-size: 27px; line-height: 1.02; text-wrap: balance; }
.route-card p { margin: 0; color: var(--muted); font-size: 14px; line-height: 1.45; }
.route-card small { position: absolute; right: 14px; bottom: 12px; color: var(--red); font: 900 12px/1 ui-monospace, SFMono-Regular, Menlo, monospace; }
.route-card:nth-child(1) { left: 2%; top: 22px; --r: -2deg; }
.route-card:nth-child(2) { left: 23%; top: 210px; --r: 2deg; }
.route-card:nth-child(3) { left: 42%; top: 55px; --r: -1deg; }
.route-card:nth-child(4) { right: 23%; top: 250px; --r: 2.2deg; }
.route-card:nth-child(5) { right: 2%; top: 86px; --r: -2deg; background: var(--dark); color: #fff8e6; }
.route-card:nth-child(5) p { color: #d7cfba; }
.route-card:nth-child(6) { right: 9%; top: 352px; --r: 1.2deg; background: #fff0a8; }
.start-token {
  position: absolute;
  left: 52%;
  top: 45%;
  width: 112px;
  height: 112px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--red);
  color: white;
  text-align: center;
  font: 900 17px/1 ui-monospace, SFMono-Regular, Menlo, monospace;
  box-shadow: 8px 8px 0 var(--ink);
  transform: rotate(-8deg);
}
.intro-strip {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;
  gap: 28px;
  padding: 26px 0;
  border-bottom: 1px solid var(--line);
}
.intro-strip p { margin: 0; max-width: 760px; font-size: 20px; line-height: 1.55; }
.statbox { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font: 700 13px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--muted); }
.statbox b { display: block; color: var(--ink); font-size: 24px; margin-bottom: 4px; }
.section-title {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 20px;
  padding: 26px 0 12px;
}
.section-title h1, .section-title h2 { margin: 0; font-size: 28px; line-height: 1.05; }
.section-title p { margin: 0; color: var(--muted); max-width: 520px; line-height: 1.5; }
.issue-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}
.issue-tile {
  display: grid;
  grid-template-columns: 82px 1fr;
  gap: 12px;
  min-height: 134px;
  padding: 10px;
  background: rgba(255,255,255,.34);
  border: 1px solid var(--line);
  text-decoration: none;
}
.issue-tile img { width: 82px; height: 112px; object-fit: cover; border: 1px solid var(--line); background: var(--paper-2); }
.issue-tile b { display: block; font-size: 15px; line-height: 1.22; }
.issue-tile span { display: block; color: var(--muted); font: 700 11px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace; margin-bottom: 8px; }
.issue-tile p { margin: 8px 0 0; color: var(--muted); font-size: 13px; line-height: 1.42; }
.searchbar {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 10px;
  padding: 18px 0;
}
.searchbar input {
  width: 100%;
  border: 2px solid var(--ink);
  background: var(--paper-2);
  padding: 13px 14px;
  color: var(--ink);
  font: 16px/1.3 inherit;
}
.searchbar button {
  border: 2px solid var(--ink);
  background: var(--ink);
  color: white;
  padding: 0 18px;
  font-weight: 800;
}
.route-head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 26px;
  padding: 28px 0 24px;
  border-bottom: 1px solid var(--line);
}
.route-head h1 { margin: 0; font-size: clamp(28px, 3.8vw, 42px); line-height: 1; letter-spacing: -.01em; max-width: 720px; }
.route-head p { margin: 0; color: var(--muted); font-size: 18px; line-height: 1.6; }
.clue-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  padding-top: 20px;
}
.clue {
  position: relative;
  min-height: 220px;
  padding: 16px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.36);
  text-decoration: none;
}
.clue img { width: 86px; height: 118px; object-fit: cover; border: 1px solid var(--line); float: right; margin-left: 14px; }
.clue small { color: var(--green); font: 900 11px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace; }
.clue h2 { margin: 10px 0; font-size: 25px; line-height: 1.04; }
.clue p { margin: 0; color: var(--muted); line-height: 1.55; }
.issue-desk {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  gap: 24px;
  padding-top: 24px;
}
.cover-panel {
  position: sticky;
  top: 18px;
  align-self: start;
  background: var(--paper-2);
  border: 1px solid var(--line);
  padding: 16px;
}
.cover-panel img { width: 100%; display: block; border: 1px solid var(--line); }
.cover-panel h1 { margin: 16px 0 8px; font-size: 27px; line-height: 1.04; }
.meta { color: var(--muted); font: 700 12px/1.45 ui-monospace, SFMono-Regular, Menlo, monospace; }
.source-links { display: grid; gap: 8px; margin-top: 16px; }
.source-links a { text-align: center; text-decoration: none; border: 2px solid var(--ink); padding: 10px 8px; font-weight: 800; }
.source-links a:first-child { background: var(--ink); color: white; }
.desk-intro {
  border-bottom: 1px solid var(--line);
  padding-bottom: 18px;
  margin-bottom: 18px;
}
.desk-intro p { margin: 0; max-width: 840px; color: var(--muted); font-size: 18px; line-height: 1.62; }
.unit-board {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.unit {
  min-height: 172px;
  padding: 14px;
  background: rgba(255,255,255,.38);
  border: 1px solid var(--line);
}
.unit strong { display: block; font-size: 21px; line-height: 1.08; margin: 8px 0; }
.unit span { display: inline-block; background: #fff0a8; color: #4e3e09; padding: 4px 7px; font: 900 11px/1 ui-monospace, SFMono-Regular, Menlo, monospace; }
.unit p { margin: 0; color: var(--muted); font-size: 14px; line-height: 1.55; }
.unit .note { margin-top: 9px; color: var(--ink); }
.footer-note { margin-top: 30px; padding-top: 16px; border-top: 1px solid var(--line); color: var(--muted); font-size: 13px; line-height: 1.6; }
.hidden { display: none !important; }
@media (max-width: 1000px) {
  .route-board { min-height: auto; display: grid; gap: 14px; }
  .route-card { position: relative; left: auto !important; right: auto !important; top: auto !important; width: auto; transform: none; }
  .start-token { display: none; }
  .issue-grid, .clue-grid, .unit-board { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .intro-strip, .route-head, .issue-desk, .product-home, .now-table { grid-template-columns: 1fr; }
  .cover-panel { position: static; }
}
@media (max-width: 640px) {
  .shell { padding: 18px 16px 40px; }
  .issue-grid, .clue-grid, .unit-board { grid-template-columns: 1fr; }
  .topline, .section-title { align-items: start; flex-direction: column; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}
"""


def site_js() -> str:
    return r"""
const search = document.querySelector('[data-search]');
const reset = document.querySelector('[data-reset]');
const cards = Array.from(document.querySelectorAll('[data-search-text]'));
const count = document.querySelector('[data-count]');
function applySearch() {
  if (!search) return;
  const q = search.value.trim().toLowerCase();
  let visible = 0;
  cards.forEach(card => {
    const show = !q || card.dataset.searchText.includes(q);
    card.classList.toggle('hidden', !show);
    if (show) visible += 1;
  });
  if (count) count.textContent = String(visible);
}
if (search) search.addEventListener('input', applySearch);
if (reset) reset.addEventListener('click', () => { search.value = ''; applySearch(); search.focus(); });
applySearch();
"""


def load_data() -> tuple[list[dict], dict[str, list[dict]]]:
    guides = json.loads(GUIDES_JSON.read_text(encoding="utf-8"))
    maps = json.loads(MAPS_JSON.read_text(encoding="utf-8"))
    by_key: dict[str, list[dict]] = {}
    for item in maps:
        units = item.get("content_map", [])
        by_key[item.get("identifier") or item.get("title")] = units
    return guides, by_key


def enrich_issues(guides: list[dict], by_key: dict[str, list[dict]]) -> list[dict]:
    used: set[str] = set()
    enriched = []
    for issue in guides:
        item = dict(issue)
        item["site_slug"] = issue_slug(item, used)
        item["site_href"] = f"issues/{item['site_slug']}.html"
        item["content_units"] = by_key.get(item.get("identifier")) or by_key.get(item.get("title")) or item.get("content_map", [])
        item["preview_units"] = pick_units(item["content_units"], 6)
        enriched.append(item)
    return enriched


def collection_counts(issues: list[dict]) -> Counter:
    return Counter(clean_text(issue.get("collection_zh", "未知系列")) for issue in issues)


def render_index(issues: list[dict]) -> str:
    counts = collection_counts(issues)
    years = [i["year"] for i in issues if isinstance(i.get("year"), int)]
    cards = []
    for route in ROUTES:
        matched = [i for i in issues if route_score(i, i["content_units"], route) > 0]
        cards.append(
            f'<a class="route-button" href="routes/{esc(route["slug"])}.html">'
            f'<b>{esc(route["name"])}</b><span>{len(matched)}</span></a>'
        )
    featured = [
        next((i for i in issues if "Software Catalog 2.0" in i.get("title", "")), issues[0]),
        next((i for i in issues if i.get("year") == 1968 and "Catalog" in i.get("title", "")), issues[0]),
        next((i for i in issues if i.get("year") == 1974 and "Cybernetic" in i.get("title", "")), issues[0]),
        next((i for i in issues if i.get("year") == 2002), issues[-1]),
    ]
    featured_unit = featured[0]["preview_units"][0] if featured[0]["preview_units"] else {}
    quick_slices = []
    for issue in featured[1:]:
        unit = issue["preview_units"][0] if issue["preview_units"] else {}
        quick_slices.append(
            f'<a class="quick-slice" href="{esc(issue["site_href"])}">'
            f'<img loading="lazy" src="{esc(issue.get("cover_url", ""))}" alt="{esc(issue.get("title", ""))} cover">'
            f'<div><small>{esc(issue.get("year", ""))} / {esc(unit.get("topic", issue.get("collection_zh", "")))}</small>'
            f'<b>{esc(unit.get("title", issue.get("title", "")))}</b></div></a>'
        )
    issue_tiles = []
    for issue in issues:
        text = " ".join(
            [
                clean_text(issue.get("title", "")),
                clean_text(issue.get("collection_zh", "")),
                clean_text(issue.get("year", "")),
                " ".join(clean_text(t) for t in issue.get("topics", [])),
                " ".join(clean_text(u.get("title", "")) for u in issue["preview_units"]),
            ]
        ).lower()
        desc = issue_teaser(issue)
        issue_tiles.append(
            f'<a class="issue-tile" href="{esc(issue["site_href"])}" data-search-text="{esc(text)}">'
            f'<img loading="lazy" src="{esc(issue.get("cover_url", ""))}" alt="{esc(issue.get("title", ""))} cover">'
            f'<div><span>{esc(issue.get("year", ""))} / {esc(issue.get("collection_zh", ""))}</span>'
            f'<b>{esc(issue.get("title", ""))}</b><p>{esc(desc)[:130]}</p></div></a>'
        )
    return wrap_page(
        "Whole Earth 中文内容路线",
        f"""
<main class="shell">
  <header class="topline">
    <div class="brand">WHOLE EARTH<br>中文内容路线</div>
    <nav class="smallnav"><a href="#all">全部刊物</a><a href="content_slices.json">内容切片 JSON</a></nav>
  </header>
  <section class="product-home">
    <nav class="route-list" aria-label="主题路线">{''.join(cards)}</nav>
    <div class="now-table">
      <a class="feature-slice" href="{esc(featured[0]["site_href"])}">
        <small>{esc(featured[0].get("year", ""))} / {esc(featured_unit.get("topic", "内容"))}</small>
        <b>{esc(featured_unit.get("title", "Programming"))}</b>
        <span>{esc(unit_teaser(featured_unit))}</span>
      </a>
      <div class="quick-stack">{''.join(quick_slices)}</div>
    </div>
  </section>
  <section id="all">
    <div class="section-title"><h2>全部刊物</h2><p>{len(issues)} 本 / {sum(len(i["content_units"]) for i in issues)} 条线索 / {min(years)}-{max(years)}</p></div>
    <div class="searchbar"><input data-search type="search" placeholder="搜索：Programming、通信、生态、工具、1974、Whole Earth Review"><button data-reset type="button">重置</button></div>
    <div class="meta">当前显示 <span data-count>{len(issues)}</span> / {len(issues)}</div>
    <div class="issue-grid">{''.join(issue_tiles)}</div>
  </section>
  <footer class="footer-note">数据来自 wholeearth.info 与 Internet Archive。本站是中文导读和内容路线，不提供整本替代译本。</footer>
</main>
<script>{site_js()}</script>
""",
    )


def route_units(issues: list[dict], route: dict) -> list[tuple[dict, dict]]:
    rows: list[tuple[dict, dict]] = []
    for issue in issues:
        matched = [u for u in issue["content_units"] if unit_matches(u, route)]
        if not matched and route_score(issue, issue["content_units"], route) > 0:
            matched = issue["preview_units"][:2]
        for unit in matched[:4]:
            rows.append((issue, unit))
    rows.sort(key=lambda row: (row[0].get("year") or 9999, row[0].get("title", "")))
    return rows[:90]


def render_route(route: dict, issues: list[dict]) -> str:
    rows = route_units(issues, route)
    clues = []
    for issue, unit in rows:
        clues.append(
            f'<a class="clue" href="../{esc(issue["site_href"])}">'
            f'<img loading="lazy" src="{esc(issue.get("cover_url", ""))}" alt="{esc(issue.get("title", ""))} cover">'
            f'<small>{esc(issue.get("year", ""))} / {esc(issue.get("collection_zh", ""))}</small>'
            f'<h2>{esc(unit.get("title", ""))}</h2>'
            f'<p>{esc(unit_teaser(unit))}</p></a>'
        )
    return wrap_page(
        clean_text(route["name"]),
        f"""
<main class="shell">
  <header class="topline">
    <a class="brand" href="../index.html">WHOLE EARTH<br>中文内容路线</a>
    <nav class="smallnav"><a href="../index.html">回首页</a><a href="../content_slices.json">内容切片 JSON</a></nav>
  </header>
  <section class="route-head">
    <h1>{esc(route["name"])}</h1>
    <p>{len(rows)} 条线索</p>
  </section>
  <section class="clue-grid">{''.join(clues)}</section>
  <footer class="footer-note">共选出 {len(rows)} 条线索。OCR 标题可能有噪声，进入单本页面可核对原始来源链接。</footer>
</main>
""",
    )


def render_issue(issue: dict) -> str:
    units = issue["content_units"]
    unit_html = []
    for unit in units:
        unit_html.append(
            f'<article class="unit"><span>{esc(unit.get("topic", "内容"))}</span>'
            f'<strong>{esc(unit.get("title", ""))}</strong>'
            f'<p>{esc(unit_teaser(unit))}</p></article>'
        )
    topics = " / ".join(clean_text(t) for t in issue.get("topics", [])) or "待细读"
    return wrap_page(
        clean_text(issue.get("title", "")),
        f"""
<main class="shell">
  <header class="topline">
    <a class="brand" href="../index.html">WHOLE EARTH<br>中文内容路线</a>
    <nav class="smallnav"><a href="../index.html">全部路线</a><a href="../content_slices.json">内容切片 JSON</a></nav>
  </header>
  <section class="issue-desk">
    <aside class="cover-panel">
      <img loading="lazy" src="{esc(issue.get("cover_url", ""))}" alt="{esc(issue.get("title", ""))} cover">
      <h1>{esc(issue.get("title", ""))}</h1>
      <div class="meta">{esc(issue.get("year", ""))} / {esc(issue.get("collection_zh", ""))}<br>{esc(issue.get("pages", ""))} pages / {esc(topics)}</div>
      <div class="source-links"><a href="{esc(issue.get("archive_url", ""))}" target="_blank" rel="noreferrer">Internet Archive</a><a href="{esc(issue.get("url", ""))}" target="_blank" rel="noreferrer">Whole Earth 页面</a></div>
    </aside>
    <section>
      <div class="section-title"><h2>内容桌</h2><p>{len(units)} 条线索</p></div>
      <div class="unit-board">{''.join(unit_html)}</div>
    </section>
  </section>
  <footer class="footer-note">本页为中文导读和内容地图。OCR 标题可能包含识别噪声，最终请以 Internet Archive 原扫描为准。</footer>
</main>
""",
    )


def wrap_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>{css()}</style>
</head>
<body>
{body}
</body>
</html>
"""


def write_site(issues: list[dict]) -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    ISSUES_DIR.mkdir(parents=True, exist_ok=True)
    ROUTES_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    (SITE / "index.html").write_text(render_index(issues), encoding="utf-8")
    for route in ROUTES:
        (ROUTES_DIR / f"{route['slug']}.html").write_text(render_route(route, issues), encoding="utf-8")
    for issue in issues:
        (ISSUES_DIR / f"{issue['site_slug']}.html").write_text(render_issue(issue), encoding="utf-8")

    slices = []
    for issue in issues:
        for unit in issue["content_units"]:
            slices.append(
                {
                    "issue_title": clean_text(issue.get("title", "")),
                    "issue_slug": issue["site_slug"],
                    "issue_href": issue["site_href"],
                    "year": issue.get("year"),
                    "collection_zh": clean_text(issue.get("collection_zh", "")),
                    "cover_url": clean_text(issue.get("cover_url", "")),
                    "title": clean_text(unit.get("title", "")),
                    "topic": clean_text(unit.get("topic", "")),
                    "summary_zh": clean_text(unit.get("summary_zh", "")),
                    "reading_note": clean_text(unit.get("reading_note", "")),
                }
            )
    (SITE / "content_slices.json").write_text(json.dumps(slices, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "issues": len(issues),
        "issue_pages": len(list(ISSUES_DIR.glob("*.html"))),
        "routes": len(ROUTES),
        "content_slices": len(slices),
    }
    (SITE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def qa(issues: list[dict]) -> dict:
    index = (SITE / "index.html").read_text(encoding="utf-8")
    issue_pages = list(ISSUES_DIR.glob("*.html"))
    route_pages = list(ROUTES_DIR.glob("*.html"))
    html_files = [SITE / "index.html", *issue_pages, *route_pages]
    return {
        "issues_expected": len(issues),
        "issue_pages": len(issue_pages),
        "route_pages": len(route_pages),
        "index_has_all": 'id="all"' in index,
        "index_issue_links": index.count('class="issue-tile"'),
        "content_slices": len(json.loads((SITE / "content_slices.json").read_text(encoding="utf-8"))),
        "em_dash_files": [str(p.relative_to(ROOT)) for p in html_files if "—" in p.read_text(encoding="utf-8") or "–" in p.read_text(encoding="utf-8")],
    }


def main() -> None:
    guides, by_key = load_data()
    issues = enrich_issues(guides, by_key)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S %Z')}] loaded issues={len(issues)} maps={len(by_key)}")
    write_site(issues)
    result = qa(issues)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["issue_pages"] != len(issues) or result["index_issue_links"] != len(issues) or result["em_dash_files"]:
        raise SystemExit(2)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S %Z')}] wrote site={SITE}")


if __name__ == "__main__":
    main()
