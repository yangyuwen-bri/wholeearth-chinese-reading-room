#!/usr/bin/env python3
from __future__ import annotations

import html
from pathlib import Path

from build_wholeearth_html import FEATURE_IMAGES, SECTION_TAGS, SRC, OUT, parse, inline_md

ROOT = Path(__file__).resolve().parents[1]


def copy_assets() -> None:
    assets = ROOT / "outputs" / "wholeearth_assets"
    assets.mkdir(exist_ok=True)
    for name in ["software1985_n0.jpg", "software1985_n2.jpg", "software1985_n159.jpg", "software1985_n178.jpg"]:
        src = ROOT / "work" / "wholeearth" / name
        dest = assets / name
        if src.exists() and (not dest.exists() or dest.stat().st_size != src.stat().st_size):
            dest.write_bytes(src.read_bytes())


def render_content(items) -> str:
    out = []
    for kind, value in items:
        if kind == "p":
            tone = " note" if value.startswith(("短摘译：", "读法：", "阅读重点：", "说明：")) else ""
            out.append(f'<p class="copy{tone}">{inline_md(value)}</p>')
        elif kind == "ul":
            out.append('<ul class="line-list">')
            for item in value:
                out.append(f"<li>{inline_md(item)}</li>")
            out.append("</ul>")
    return "\n".join(out)


def main() -> None:
    copy_assets()
    title, blocks = parse(SRC.read_text(encoding="utf-8"))
    h2s = [b for b in blocks if b["level"] == 2]
    article_count = sum(1 for b in blocks if b["level"] == 3)
    bullet_count = sum(len(v) for b in blocks for k, v in b["content"] if k == "ul")

    nav = "\n".join(
        f'<a href="#{b["id"]}" data-target="{b["id"]}"><span>{i:02d}</span>{html.escape(b["title"])}</a>'
        for i, b in enumerate(h2s, start=1)
    )
    hero_images = "\n".join(
        f'<figure class="scan-card"><img src="{src}" alt="{html.escape(label)}扫描页"><figcaption>{html.escape(label)}</figcaption></figure>'
        for label, src in FEATURE_IMAGES
    )
    cards = "\n".join(
        f'<a class="chapter-card reveal" href="#{b["id"]}" style="--index:{i}">'
        f'<span class="tag">{SECTION_TAGS.get(b["title"], "导读")}</span><strong>{html.escape(b["title"])}</strong>'
        f'</a>'
        for i, b in enumerate(h2s[:18])
    )
    sections = "\n".join(
        f'<section class="reader-section level-{b["level"]} reveal" id="{b["id"]}" data-title="{html.escape(b["title"])}">'
        f'<div class="section-meta">{"Article" if b["level"] == 3 else "Chapter"}</div>'
        f'<h{"3" if b["level"] == 3 else "2"}>{html.escape(b["title"])}</h{"3" if b["level"] == 3 else "2"}>'
        f'{render_content(b["content"])}</section>'
        for b in blocks
    )

    css = r"""
    :root {
      --canvas: #F7F6F3;
      --surface: #FFFFFF;
      --soft: #F9F9F8;
      --ink: #2F3437;
      --heading: #111111;
      --muted: #787774;
      --border: #EAEAEA;
      --red-bg: #FDEBEC;
      --red-text: #9F2F2D;
      --blue-bg: #E1F3FE;
      --blue-text: #1F6C9F;
      --green-bg: #EDF3EC;
      --green-text: #346538;
      --yellow-bg: #FBF3DB;
      --yellow-text: #956400;
      --sans: "SF Pro Display", "Geist Sans", "Helvetica Neue", "Switzer", "Microsoft YaHei", sans-serif;
      --serif: "Newsreader", "Lyon Text", "Instrument Serif", "Songti SC", Georgia, serif;
      --mono: "Geist Mono", "SF Mono", "JetBrains Mono", "Courier New", monospace;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      color: var(--ink);
      background-color: var(--canvas);
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='52' height='52' viewBox='0 0 52 52'%3E%3Cpath d='M0 51.5h52M51.5 0v52' fill='none' stroke='%23EAEAEA' stroke-width='1'/%3E%3C/svg%3E");
      font-family: var(--sans);
      letter-spacing: 0;
    }
    .layout { display: grid; grid-template-columns: minmax(220px, 300px) minmax(0, 1fr); min-height: 100vh; }
    .rail {
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
      padding: 24px;
      border-right: 1px solid var(--border);
      background: rgba(247, 246, 243, .94);
      backdrop-filter: blur(10px);
    }
    .brand {
      display: grid;
      gap: 14px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border);
    }
    .brand-mark {
      width: 40px;
      height: 40px;
      display: grid;
      place-items: center;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      font-family: var(--mono);
      font-size: 12px;
      color: var(--red-text);
      font-weight: 700;
    }
    .brand strong {
      color: var(--heading);
      font-size: 15px;
      line-height: 1.25;
      letter-spacing: -.01em;
    }
    .brand small {
      color: var(--muted);
      font-family: var(--mono);
      font-size: 11px;
    }
    .tools { display: grid; grid-template-columns: 1fr auto; gap: 8px; margin: 24px 0; }
    .tools input {
      width: 100%;
      min-width: 0;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      color: var(--ink);
      padding: 11px 12px;
      font: 14px/1.4 var(--sans);
      outline: none;
    }
    .tools input:focus { border-color: rgba(17, 17, 17, .28); }
    .tools button {
      border: 0;
      border-radius: 6px;
      background: var(--heading);
      color: #FFFFFF;
      padding: 0 14px;
      font: 12px/1 var(--mono);
      cursor: pointer;
    }
    .tools button:active { transform: scale(.98); }
    .nav { display: grid; gap: 4px; }
    .nav a {
      display: grid;
      grid-template-columns: 28px 1fr;
      align-items: center;
      min-height: 34px;
      padding: 6px 8px;
      color: var(--ink);
      text-decoration: none;
      border-radius: 8px;
      font-size: 13px;
      line-height: 1.2;
    }
    .nav a span {
      font-family: var(--mono);
      font-size: 11px;
      color: var(--muted);
    }
    .nav a:hover,
    .nav a.active {
      background: var(--surface);
      box-shadow: 0 2px 8px rgba(0, 0, 0, .04);
    }
    main { min-width: 0; }
    .hero {
      max-width: 1180px;
      margin: 0 auto;
      padding: 88px 48px 72px;
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(320px, .95fr);
      gap: 48px;
      align-items: end;
    }
    .eyebrow {
      display: inline-flex;
      width: fit-content;
      border-radius: 9999px;
      background: var(--yellow-bg);
      color: var(--yellow-text);
      padding: 6px 10px;
      font: 700 11px/1 var(--mono);
      letter-spacing: .05em;
      text-transform: uppercase;
    }
    h1 {
      margin: 24px 0;
      max-width: 780px;
      color: var(--heading);
      font-family: var(--serif);
      font-size: clamp(54px, 8vw, 112px);
      line-height: .94;
      letter-spacing: -.04em;
      font-weight: 500;
    }
    .subtitle {
      max-width: 720px;
      color: var(--ink);
      font-size: clamp(17px, 1.6vw, 22px);
      line-height: 1.72;
      margin: 0;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 36px;
      max-width: 620px;
    }
    .stat {
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--surface);
      padding: 18px;
      color: var(--muted);
      font-size: 13px;
    }
    .stat strong {
      display: block;
      margin-bottom: 6px;
      color: var(--heading);
      font: 700 24px/1 var(--mono);
    }
    .hero-gallery {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    .scan-card {
      margin: 0;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--surface);
      overflow: hidden;
    }
    .scan-card img {
      display: block;
      width: 100%;
      aspect-ratio: 3 / 4;
      object-fit: cover;
      filter: grayscale(.18) saturate(.7) contrast(1.03);
    }
    .scan-card figcaption {
      padding: 10px 12px;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font: 12px/1.2 var(--mono);
    }
    .chapter-strip {
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 48px 72px;
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 12px;
    }
    .chapter-card {
      grid-column: span 3;
      min-height: 136px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--surface);
      padding: 24px;
      text-decoration: none;
      color: var(--heading);
      transition: transform 200ms ease, box-shadow 200ms ease;
    }
    .chapter-card:nth-child(5n + 1) { grid-column: span 4; }
    .chapter-card:nth-child(7n + 2) { grid-column: span 5; }
    .chapter-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 2px 8px rgba(0, 0, 0, .04);
    }
    .chapter-card strong {
      font: 600 24px/1.1 var(--serif);
      letter-spacing: -.02em;
    }
    .tag, .section-meta {
      width: fit-content;
      border-radius: 9999px;
      background: var(--green-bg);
      color: var(--green-text);
      padding: 6px 9px;
      font: 700 10px/1 var(--mono);
      letter-spacing: .05em;
      text-transform: uppercase;
    }
    .reader {
      max-width: 940px;
      margin: 0 auto;
      padding: 0 48px 96px;
    }
    .reader-section {
      border-top: 1px solid var(--border);
      padding: 56px 0;
    }
    .reader-section.hidden { display: none; }
    .reader-section.level-3 {
      padding: 32px 0 32px 28px;
      border-left: 1px solid var(--border);
    }
    .reader-section.level-3 + .reader-section.level-3 { border-top: 0; }
    .section-meta {
      margin-bottom: 18px;
      background: var(--blue-bg);
      color: var(--blue-text);
    }
    h2, h3 {
      margin: 0 0 24px;
      color: var(--heading);
      font-family: var(--serif);
      letter-spacing: -.035em;
      font-weight: 500;
    }
    h2 { font-size: clamp(42px, 6vw, 76px); line-height: 1; }
    h3 { font-size: clamp(28px, 4vw, 42px); line-height: 1.08; }
    .copy {
      margin: 16px 0;
      font-family: var(--sans);
      font-size: 17px;
      line-height: 1.76;
      color: var(--ink);
    }
    .copy.note {
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--soft);
      padding: 18px 20px;
    }
    code, kbd {
      border: 1px solid var(--border);
      border-radius: 4px;
      background: var(--canvas);
      padding: 1px 5px;
      font-family: var(--mono);
      font-size: .9em;
    }
    .line-list {
      margin: 20px 0 0;
      padding: 0;
      list-style: none;
      border-top: 1px solid var(--border);
    }
    .line-list li {
      display: grid;
      grid-template-columns: 18px 1fr;
      gap: 12px;
      padding: 14px 0;
      border-bottom: 1px solid var(--border);
      font: 15px/1.7 var(--sans);
    }
    .line-list li::before {
      content: "";
      width: 6px;
      height: 6px;
      margin-top: 10px;
      border-radius: 2px;
      background: var(--red-text);
      opacity: .38;
    }
    .no-results {
      display: none;
      max-width: 560px;
      margin: 0 auto 48px;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--surface);
      padding: 24px;
      color: var(--muted);
      font: 15px/1.6 var(--sans);
    }
    .no-results.show { display: block; }
    footer {
      max-width: 1180px;
      margin: 0 auto;
      padding: 32px 48px 64px;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font: 13px/1.6 var(--sans);
    }
    .reveal {
      opacity: 0;
      transform: translateY(12px);
      transition: opacity 600ms cubic-bezier(.16, 1, .3, 1), transform 600ms cubic-bezier(.16, 1, .3, 1);
      transition-delay: calc(var(--index, 0) * 45ms);
    }
    .reveal.visible {
      opacity: 1;
      transform: translateY(0);
    }
    @media (max-width: 1080px) {
      .layout { grid-template-columns: 1fr; }
      .rail {
        position: static;
        height: auto;
        border-right: 0;
        border-bottom: 1px solid var(--border);
      }
      .nav { grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); }
      .hero { grid-template-columns: 1fr; padding: 64px 28px; }
      .chapter-strip { padding: 0 28px 56px; grid-template-columns: repeat(6, 1fr); }
      .chapter-card, .chapter-card:nth-child(5n + 1), .chapter-card:nth-child(7n + 2) { grid-column: span 3; }
      .reader { padding: 0 28px 72px; }
      footer { padding: 28px; }
    }
    @media (max-width: 620px) {
      .rail { padding: 18px; }
      .tools { grid-template-columns: 1fr; }
      .tools button { min-height: 40px; }
      .hero { padding: 48px 18px; }
      .hero-gallery { grid-template-columns: 1fr 1fr; gap: 8px; }
      .stats { grid-template-columns: 1fr; }
      .chapter-strip { padding: 0 18px 48px; grid-template-columns: 1fr; }
      .chapter-card, .chapter-card:nth-child(5n + 1), .chapter-card:nth-child(7n + 2) { grid-column: span 1; }
      .reader { padding: 0 18px 56px; }
      .reader-section.level-3 { padding-left: 16px; }
      h1 { font-size: clamp(46px, 16vw, 72px); }
      .copy { font-size: 16px; }
    }
    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      .reveal { opacity: 1; transform: none; transition: none; }
    }
    @media print {
      .rail, .chapter-strip, .hero-gallery, .tools { display: none; }
      .layout, .hero { display: block; }
      body { background: #FFFFFF; }
      .reader-section { break-inside: avoid; }
    }
    """

    js = r"""
    const navLinks = Array.from(document.querySelectorAll('.nav a'));
    const sections = Array.from(document.querySelectorAll('.reader-section'));
    const search = document.querySelector('#search');
    const clear = document.querySelector('#clear');
    const noResults = document.querySelector('.no-results');
    const revealItems = Array.from(document.querySelectorAll('.reveal'));

    const activeObserver = new IntersectionObserver((entries) => {
      const visible = entries.filter(entry => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      navLinks.forEach(link => link.classList.toggle('active', link.dataset.target === visible.target.id));
    }, { rootMargin: '-22% 0px -62% 0px', threshold: [0.08, 0.2, 0.45] });

    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    sections.forEach(section => activeObserver.observe(section));
    revealItems.forEach(item => revealObserver.observe(item));

    function filterSections() {
      const query = search.value.trim().toLowerCase();
      let shown = 0;
      sections.forEach(section => {
        const match = !query || section.textContent.toLowerCase().includes(query);
        section.classList.toggle('hidden', !match);
        if (match) shown += 1;
      });
      noResults.classList.toggle('show', shown === 0);
    }

    search.addEventListener('input', filterSections);
    clear.addEventListener('click', () => {
      search.value = '';
      filterSections();
      search.focus();
    });
    """

    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} - 极简阅读版</title>
  <style>{css}</style>
</head>
<body>
  <div class="layout">
    <aside class="rail">
      <div class="brand">
        <div class="brand-mark">WE</div>
        <div>
          <strong>Software Catalog<br>中文阅读室</strong><br>
          <small>1985 / 2.0 / minimalist edition</small>
        </div>
      </div>
      <div class="tools">
        <input id="search" type="search" placeholder="搜索 LOGO、写作、通信" aria-label="搜索导读内容">
        <button id="clear" type="button">清空</button>
      </div>
      <nav class="nav" aria-label="章节导航">{nav}</nav>
    </aside>
    <main>
      <header class="hero">
        <div class="reveal">
          <div class="eyebrow">Whole Earth Software Catalog 2.0</div>
          <h1>1985 软件目录中文阅读室</h1>
          <p class="subtitle">把一本早期个人电脑工具目录整理成安静、可搜索、可跳读的中文导览。它谈游戏、写作、数字模型、数据库、通信、编程和学习，也谈怎样在混乱的软件市场中保持判断。</p>
          <div class="stats">
            <div class="stat"><strong>{len(h2s)}</strong>主章节</div>
            <div class="stat"><strong>{article_count}</strong>文章与框文</div>
            <div class="stat"><strong>{bullet_count}</strong>条目线索</div>
          </div>
        </div>
        <div class="hero-gallery reveal">{hero_images}</div>
      </header>
      <div class="chapter-strip">{cards}</div>
      <div class="no-results">没有匹配内容。换一个关键词试试，比如“通信”“编程”“LOGO”“数据库”。</div>
      <article class="reader">{sections}</article>
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
