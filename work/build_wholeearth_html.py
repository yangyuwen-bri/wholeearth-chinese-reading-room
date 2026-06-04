#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "outputs" / "whole_earth_software_catalog_1985_chinese_companion.md"
OUT = ROOT / "outputs" / "whole_earth_software_catalog_1985_chinese_companion.html"


FEATURE_IMAGES = [
    ("封面", "wholeearth_assets/software1985_n0.jpg"),
    ("目录", "wholeearth_assets/software1985_n2.jpg"),
    ("编程章", "wholeearth_assets/software1985_n159.jpg"),
    ("学习章", "wholeearth_assets/software1985_n178.jpg"),
]

SECTION_TAGS = {
    "Playing": "游戏 / 交互",
    "Writing": "写作",
    "Analyzing": "数字模型",
    "Organizing": "知识管理",
    "Accounting": "业务基础",
    "Managing": "集成办公",
    "Drawing": "视觉思考",
    "Telecommunicating": "在线网络",
    "Programming": "编程美学",
    "Learning": "学习",
    "Etc.": "边界实验",
}


def slug(text: str, used: set[str]) -> str:
    base = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text).strip("-").lower()
    base = base or "section"
    candidate = base
    n = 2
    while candidate in used:
        candidate = f"{base}-{n}"
        n += 1
    used.add(candidate)
    return candidate


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def parse(md: str):
    used = set()
    title = ""
    blocks = []
    current = None
    paragraph = []
    list_items = []

    def flush_paragraph():
        nonlocal paragraph
        if paragraph and current is not None:
            current["content"].append(("p", " ".join(paragraph).strip()))
        paragraph = []

    def flush_list():
        nonlocal list_items
        if list_items and current is not None:
            current["content"].append(("ul", list_items))
        list_items = []

    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("# "):
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            name = line[3:].strip()
            current = {"level": 2, "title": name, "id": slug(name, used), "content": []}
            blocks.append(current)
            continue
        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            name = line[4:].strip()
            current = {"level": 3, "title": name, "id": slug(name, used), "content": []}
            blocks.append(current)
            continue
        if current is None:
            continue
        if not line.strip():
            flush_paragraph()
            flush_list()
            continue
        if re.match(r"^\d+\.\s+", line) or line.startswith("- "):
            flush_paragraph()
            item = re.sub(r"^\d+\.\s+|^-\s+", "", line)
            list_items.append(item)
            continue
        flush_list()
        paragraph.append(line)
    flush_paragraph()
    flush_list()
    return title, blocks


def render_content(items):
    out = []
    for kind, value in items:
        if kind == "p":
            klass = " callout" if value.startswith(("短摘译：", "读法：", "阅读重点：", "说明：")) else ""
            out.append(f'<p class="copy{klass}">{inline_md(value)}</p>')
        elif kind == "ul":
            out.append('<ul class="item-list">')
            for item in value:
                out.append(f"<li>{inline_md(item)}</li>")
            out.append("</ul>")
    return "\n".join(out)


def main():
    assets = ROOT / "outputs" / "wholeearth_assets"
    assets.mkdir(exist_ok=True)
    for name in ["software1985_n0.jpg", "software1985_n2.jpg", "software1985_n159.jpg", "software1985_n178.jpg"]:
        src = ROOT / "work" / "wholeearth" / name
        dest = assets / name
        if src.exists() and (not dest.exists() or dest.stat().st_size != src.stat().st_size):
            dest.write_bytes(src.read_bytes())

    md = SRC.read_text(encoding="utf-8")
    title, blocks = parse(md)
    h2s = [b for b in blocks if b["level"] == 2]
    article_count = sum(1 for b in blocks if b["level"] == 3)
    bullet_count = sum(len(v) for b in blocks for k, v in b["content"] if k == "ul")
    section_cards = [b for b in h2s[:18]]

    nav = "\n".join(
        f'<a href="#{b["id"]}" data-target="{b["id"]}"><span>{i:02d}</span>{html.escape(b["title"])}</a>'
        for i, b in enumerate(h2s, start=1)
    )
    hero_images = "\n".join(
        f'<figure><img src="{src}" alt="{html.escape(label)}扫描页"><figcaption>{html.escape(label)}</figcaption></figure>'
        for label, src in FEATURE_IMAGES
    )
    card_html = "\n".join(
        f'<a class="chapter-card" href="#{b["id"]}"><span>{SECTION_TAGS.get(b["title"], "导读")}</span><strong>{html.escape(b["title"])}</strong></a>'
        for b in section_cards
    )
    body = "\n".join(
        f'<section class="reader-section level-{b["level"]}" id="{b["id"]}" data-title="{html.escape(b["title"])}">'
        f'<div class="section-kicker">{"Article" if b["level"] == 3 else "Chapter"}</div>'
        f'<h{"3" if b["level"] == 3 else "2"}>{html.escape(b["title"])}</h{"3" if b["level"] == 3 else "2"}>'
        f'{render_content(b["content"])}</section>'
        for b in blocks
    )

    css = r"""
    :root {
      --paper: #f4ead7;
      --paper-2: #fff8e8;
      --ink: #201b16;
      --muted: #766b5f;
      --red: #d93220;
      --gold: #c89320;
      --green: #29483b;
      --rule: rgba(32, 27, 22, .18);
      --shadow: 0 24px 70px rgba(35, 24, 13, .18);
      --mono: "Courier New", "Courier", monospace;
      --serif: Georgia, "Times New Roman", "Songti SC", "SimSun", serif;
      --sans: "Avenir Next", "Gill Sans", "Trebuchet MS", "Microsoft YaHei", sans-serif;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at 16% 8%, rgba(217, 50, 32, .14), transparent 28rem),
        linear-gradient(90deg, rgba(32,27,22,.045) 1px, transparent 1px),
        linear-gradient(var(--paper), #e8dcc3 72%, #d8c59f);
      background-size: auto, 34px 34px, auto;
      font-family: var(--serif);
      letter-spacing: 0;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      opacity: .22;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='90' height='90'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='90' height='90' filter='url(%23n)' opacity='.45'/%3E%3C/svg%3E");
      mix-blend-mode: multiply;
    }
    .progress { position: fixed; top: 0; left: 0; height: 5px; width: 0%; background: var(--red); z-index: 30; }
    .layout { display: grid; grid-template-columns: 18rem minmax(0, 1fr); min-height: 100vh; }
    .rail {
      position: sticky; top: 0; height: 100vh; overflow: auto;
      padding: 1.1rem 1rem 1.6rem;
      border-right: 1px solid var(--rule);
      background: rgba(244, 234, 215, .82);
      backdrop-filter: blur(12px);
      z-index: 10;
    }
    .mark {
      display: grid; grid-template-columns: 3.3rem 1fr; gap: .7rem; align-items: center;
      padding-bottom: 1rem; border-bottom: 2px solid var(--ink);
    }
    .seal {
      width: 3.3rem; aspect-ratio: 1; border: 2px solid var(--ink);
      display: grid; place-items: center; font-family: var(--mono); font-weight: 700;
      color: var(--red); transform: rotate(-4deg); background: var(--paper-2);
    }
    .mark strong { font-family: var(--sans); text-transform: uppercase; font-size: .9rem; line-height: 1.05; }
    .mark small { display: block; margin-top: .25rem; font-family: var(--mono); color: var(--muted); font-size: .72rem; }
    .tools { display: grid; grid-template-columns: 1fr auto; gap: .5rem; margin: 1rem 0; }
    .tools input {
      min-width: 0; border: 1px solid var(--rule); background: var(--paper-2);
      padding: .68rem .72rem; font-family: var(--sans); border-radius: 0;
    }
    .tools button {
      border: 1px solid var(--ink); background: var(--ink); color: var(--paper-2);
      font-family: var(--mono); padding: .4rem .65rem; cursor: pointer;
    }
    .nav { display: grid; gap: .18rem; font-family: var(--sans); }
    .nav a {
      color: var(--ink); text-decoration: none; display: grid; grid-template-columns: 2rem 1fr;
      gap: .55rem; padding: .46rem .4rem; border-left: 3px solid transparent;
      font-size: .88rem;
    }
    .nav a span { font-family: var(--mono); color: var(--muted); font-size: .74rem; }
    .nav a.active, .nav a:hover { border-color: var(--red); background: rgba(255,248,232,.8); }
    main { min-width: 0; }
    .hero {
      min-height: 92vh; display: grid; grid-template-columns: minmax(0, 1fr) minmax(22rem, 36rem);
      gap: clamp(2rem, 5vw, 5rem); align-items: end;
      padding: clamp(2rem, 5vw, 5rem);
      border-bottom: 1px solid var(--rule);
    }
    .eyebrow { font-family: var(--mono); color: var(--red); text-transform: uppercase; font-weight: 700; }
    h1 {
      font-family: var(--serif);
      font-size: clamp(3.1rem, 9vw, 8.8rem);
      line-height: .86;
      margin: 1rem 0;
      letter-spacing: 0;
      max-width: 10ch;
    }
    .subtitle {
      font-size: clamp(1.05rem, 1.8vw, 1.45rem);
      line-height: 1.75; max-width: 42rem; color: #31261d;
    }
    .stats { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1.5rem; }
    .stat { border: 1px solid var(--ink); padding: .6rem .8rem; background: var(--paper-2); box-shadow: 4px 4px 0 var(--ink); }
    .stat strong { display: block; font-family: var(--mono); font-size: 1.1rem; color: var(--red); }
    .hero-gallery {
      display: grid; grid-template-columns: 1fr 1fr; gap: .8rem; align-items: end;
    }
    .hero-gallery figure {
      margin: 0; background: var(--paper-2); border: 1px solid var(--ink);
      padding: .45rem; box-shadow: var(--shadow); transform: rotate(var(--r, 1deg));
    }
    .hero-gallery figure:nth-child(2) { --r: -2deg; margin-top: 2rem; }
    .hero-gallery figure:nth-child(3) { --r: 1.7deg; }
    .hero-gallery figure:nth-child(4) { --r: -1deg; margin-bottom: 2.5rem; }
    .hero-gallery img { width: 100%; display: block; aspect-ratio: 3 / 4; object-fit: cover; filter: saturate(.9) contrast(1.04); }
    figcaption { font-family: var(--mono); font-size: .72rem; margin-top: .35rem; color: var(--muted); }
    .chapter-strip {
      padding: 1.2rem clamp(1rem, 5vw, 5rem);
      display: grid; grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
      gap: .7rem;
      border-bottom: 1px solid var(--rule);
    }
    .chapter-card {
      min-height: 7rem; display: flex; flex-direction: column; justify-content: space-between;
      padding: .85rem; color: var(--ink); text-decoration: none; background: rgba(255,248,232,.68);
      border: 1px solid var(--rule);
      transition: transform .18s ease, background .18s ease, border-color .18s ease;
    }
    .chapter-card:hover { transform: translateY(-4px); background: var(--paper-2); border-color: var(--ink); }
    .chapter-card span { font-family: var(--mono); color: var(--red); font-size: .72rem; }
    .chapter-card strong { font-family: var(--sans); font-size: 1.18rem; }
    .reader {
      width: min(100%, 64rem); margin: 0 auto; padding: clamp(1.5rem, 5vw, 4rem);
    }
    .reader-section {
      position: relative; margin: 0 0 1.15rem; padding: clamp(1.15rem, 3vw, 2rem);
      background: rgba(255,248,232,.78); border: 1px solid var(--rule);
      box-shadow: 0 1px 0 rgba(32,27,22,.08);
    }
    .reader-section.hidden { display: none; }
    .reader-section.level-3 { margin-left: clamp(0rem, 3vw, 2.3rem); border-left: 4px solid rgba(217,50,32,.58); }
    .section-kicker { font-family: var(--mono); color: var(--red); font-size: .74rem; text-transform: uppercase; margin-bottom: .35rem; }
    h2, h3 { margin: 0 0 1rem; letter-spacing: 0; }
    h2 { font-size: clamp(2rem, 5vw, 4.2rem); line-height: .95; color: var(--green); }
    h3 { font-size: clamp(1.35rem, 2.6vw, 2.25rem); line-height: 1.08; }
    .copy { font-size: 1.08rem; line-height: 1.95; margin: .75rem 0; }
    .callout {
      font-family: var(--sans); line-height: 1.72; padding: .85rem 1rem;
      border-left: 4px solid var(--red); background: rgba(217,50,32,.08);
    }
    .item-list { padding: 0; list-style: none; display: grid; gap: .42rem; }
    .item-list li {
      position: relative; padding: .48rem .55rem .48rem 1.65rem;
      border-bottom: 1px dashed rgba(32,27,22,.18);
      font-size: 1rem; line-height: 1.65;
    }
    .item-list li::before {
      content: "✦"; position: absolute; left: .25rem; color: var(--red);
    }
    .no-results {
      display: none; margin: 2rem auto; width: min(100%, 36rem); padding: 1.2rem;
      border: 1px solid var(--ink); background: var(--paper-2); font-family: var(--sans);
    }
    .no-results.show { display: block; }
    footer {
      padding: 2rem clamp(1rem, 5vw, 5rem); border-top: 2px solid var(--ink);
      font-family: var(--sans); color: var(--muted);
    }
    @media (max-width: 920px) {
      .layout { grid-template-columns: 1fr; }
      .rail { position: static; height: auto; border-right: 0; border-bottom: 1px solid var(--rule); }
      .nav { grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); }
      .hero { min-height: auto; grid-template-columns: 1fr; padding-top: 2rem; }
      .hero-gallery { max-width: 38rem; }
    }
    @media (max-width: 560px) {
      .hero-gallery { grid-template-columns: 1fr 1fr; gap: .45rem; }
      .hero-gallery figure { padding: .28rem; box-shadow: 8px 10px 24px rgba(35,24,13,.12); }
      .reader { padding: 1rem; }
      .reader-section, .reader-section.level-3 { margin-left: 0; }
      .copy { font-size: 1rem; line-height: 1.82; }
    }
    @media print {
      .rail, .progress, .chapter-strip, .hero-gallery, .tools { display: none; }
      .layout, .hero { display: block; }
      body { background: white; }
      .reader-section { break-inside: avoid; box-shadow: none; }
    }
    """

    js = r"""
    const progress = document.querySelector('.progress');
    const navLinks = Array.from(document.querySelectorAll('.nav a'));
    const sections = Array.from(document.querySelectorAll('.reader-section'));
    const search = document.querySelector('#search');
    const clear = document.querySelector('#clear');
    const noResults = document.querySelector('.no-results');

    function updateProgress() {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
      progress.style.width = pct + '%';
    }

    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter(e => e.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      navLinks.forEach(a => a.classList.toggle('active', a.dataset.target === visible.target.id));
    }, { rootMargin: '-20% 0px -65% 0px', threshold: [0.05, 0.2, 0.5] });
    sections.forEach(section => observer.observe(section));

    function filter() {
      const q = search.value.trim().toLowerCase();
      let shown = 0;
      sections.forEach(section => {
        const text = section.textContent.toLowerCase();
        const ok = !q || text.includes(q);
        section.classList.toggle('hidden', !ok);
        if (ok) shown++;
      });
      noResults.classList.toggle('show', shown === 0);
    }

    search.addEventListener('input', filter);
    clear.addEventListener('click', () => { search.value = ''; filter(); search.focus(); });
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
    """

    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} - 互动阅读版</title>
  <style>{css}</style>
</head>
<body>
  <div class="progress" aria-hidden="true"></div>
  <div class="layout">
    <aside class="rail">
      <div class="mark">
        <div class="seal">WE</div>
        <div><strong>Software Catalog<br>中文阅读室</strong><small>1985 / 2.0 / interactive</small></div>
      </div>
      <div class="tools">
        <input id="search" type="search" placeholder="搜索：LOGO、写作、通信..." aria-label="搜索导读内容">
        <button id="clear" type="button">清空</button>
      </div>
      <nav class="nav" aria-label="章节导航">{nav}</nav>
    </aside>
    <main>
      <header class="hero">
        <div>
          <div class="eyebrow">Whole Earth Software Catalog 2.0</div>
          <h1>1985 软件目录中文阅读室</h1>
          <p class="subtitle">把一本 224 页的早期个人电脑工具目录，整理成可以跳读、搜索、对照扫描页的中文导览。它讲游戏、写作、电子表格、数据库、通信、编程和学习，也讲怎样在混乱的软件市场里保持判断力。</p>
          <div class="stats">
            <div class="stat"><strong>{len(h2s)}</strong>主章节</div>
            <div class="stat"><strong>{article_count}</strong>文章/框文</div>
            <div class="stat"><strong>{bullet_count}</strong>条目线索</div>
          </div>
        </div>
        <div class="hero-gallery">{hero_images}</div>
      </header>
      <div class="chapter-strip">{card_html}</div>
      <div class="no-results">没有匹配内容。换一个关键词试试，比如“通信”“编程”“LOGO”“数据库”。</div>
      <article class="reader">{body}</article>
      <footer>生成自中文导读 Markdown。原始扫描页来自 Internet Archive / Whole Earth Index；本页为导读、摘要和短摘译，不是原书完整替代译本。</footer>
    </main>
  </div>
  <script>{js}</script>
</body>
</html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
