# Whole Earth Chinese Reading Room

[![Live site](https://img.shields.io/badge/live_site-GitHub_Pages-2f6f63?style=flat-square)](https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/)
[![Static site](https://img.shields.io/badge/site-static_HTML%2FCSS%2FJS-6b7280?style=flat-square)](#run-locally)
[![Issues indexed](https://img.shields.io/badge/issues_indexed-147-3b6ea8?style=flat-square)](#current-status)
[![Reading rooms](https://img.shields.io/badge/open_reading_rooms-1-b17a2c?style=flat-square)](#featured-entries)
[![License](https://img.shields.io/badge/license-not_declared-lightgrey?style=flat-square)](#license-and-rights)

**Whole Earth Chinese Reading Room** builds Chinese reading rooms for the Whole Earth family of publications: *Whole Earth Catalog*, *Whole Earth Epilog*, *CoEvolution Quarterly*, *Whole Earth Software Catalog*, and *Whole Earth Review*.

The project treats each published issue as an edited reading object. A finished issue connects the original scan, Chinese editorial guide, section structure, page anchors, and verification notes. It is not a bulk OCR archive.

**Live site:** <https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/>

## Featured Entries

<table>
  <tr>
    <td width="33%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/reader-prototype/index.html"><strong>1974 Epilog Reading Room</strong></a><br>
      Chinese close reading of <em>Whole Earth Epilog</em>, synchronized with Internet Archive scan pages.
    </td>
    <td width="33%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/content/demos/wholeearth_webgl_console_demo.html"><strong>WebGL Library Console</strong></a><br>
      A visual index for 147 Whole Earth issues, with reading status and publication routes.
    </td>
    <td width="33%">
      <a href="content/readings/1985_software_catalog_full_chinese_reading.md"><strong>1985 Software Catalog Guide</strong></a><br>
      Full Chinese guide for <em>Whole Earth Software Catalog 2.0</em>, ready for future reading-room work.
    </td>
  </tr>
</table>

## Editorial Model

The repository separates public reading material from research workbench material.

| Layer | Purpose | Current example |
| --- | --- | --- |
| Reading room | Public reading interface with original scan context | `reader-prototype/index.html` |
| Guide and map | Issue-level Chinese guide, atlas, or thematic map | `content/readings/`, `content/maps/` |
| Workbench | OCR dossier, page evidence, anchor audit, retrieval bundle | `data/evidence_dossiers/`, `data/issue_agents/` |

Promotion from workbench to reading room is manual. The near-term goal is a small set of high-quality Chinese reading rooms, not automatic coverage of every scanned issue.

## Current Status

| Area | Status |
| --- | --- |
| Public home | WebGL console deployed on GitHub Pages |
| Open reading room | *Whole Earth Epilog*, October 1974 |
| Full Chinese guide | *Whole Earth Software Catalog 2.0*, Fall 1985 |
| Indexed issues | 147 |
| Page-level OCR dossiers | 22,162 pages |
| Coverage QA | 147/147 issues covered |
| 1974 Epilog page mapping | Archive leaves 0-321; printed body pages use `printed page = leaf + 449` |

## Repository Layout

```text
content/
  assets/          # cover thumbnails, Earth textures, and visual assets
  data/            # publication-level metadata for the public atlas
  demos/           # WebGL and visual navigation prototypes
  maps/            # issue maps and visual reading guides
  readings/        # Chinese guides and close-reading drafts
  samples/         # historical page-level reading samples
  vendor/          # static browser dependencies

data/
  evidence_dossiers/  # issue-level OCR evidence
  issue_agents/       # experimental per-issue retrieval bundles
  issue_index.json    # 147-issue index

reader-prototype/
  index.html          # 1974 Epilog synchronized reading room
  data/               # generated reader JSON and anchor audit data

scripts/
  *.py                # extraction, audit, and experimental retrieval scripts
```

`_local/` is ignored on purpose. It is for local caches, source PDFs, logs, QA screenshots, and other material that should not be published.

## Run Locally

The site must run over HTTP because the reading room and WebGL console load JSON and browser modules.

From the repository root:

```bash
python3 -m http.server 8911
```

Open:

```text
http://127.0.0.1:8911/
```

Useful local paths:

- `reader-prototype/index.html`
- `content/demos/wholeearth_webgl_console_demo.html`
- `content/maps/wholeearth_macro_atlas.html`

## Deployment

The public site currently uses GitHub Pages from the `gh-pages` branch.

The repository is already a static site, so it can move to Cloudflare Pages without changing the public reader architecture. A server-side component should only be added when the experimental issue-agent layer needs protected API keys.

## Roadmap

- Stabilize the WebGL console as the library home page.
- Move finished readers toward a stable `/readers/<issue>/` URL pattern.
- Promote more issue guides into full scan-linked reading rooms.
- Keep public pages separate from workbench dossiers and local QA material.
- Add issue-level status metadata so the home page does not hard-code publication routes.

## License and Rights

No open-source license has been declared for this repository yet. Until a `LICENSE` file is added, treat the code, data, and editorial text in this repository as not licensed for reuse.

Original Whole Earth publications, scans, covers, and publication metadata remain subject to the rights of their respective holders. This project links back to source scans where possible and uses the material for educational commentary, reading navigation, and research verification.

---

# 全球概览中文阅读室

**全球概览中文阅读室** 是一个面向中文读者的 Whole Earth 系列阅读项目，覆盖 *Whole Earth Catalog*、*Whole Earth Epilog*、*CoEvolution Quarterly*、*Whole Earth Software Catalog* 与 *Whole Earth Review*。

项目不是 OCR 堆料。每一期成熟内容都会把原书扫描页、中文导读、章节结构、页码锚点和核查材料放在同一个阅读对象里。

## 当前入口

| 入口 | 内容 |
| --- | --- |
| [1974 Epilog 对照阅读器](https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/reader-prototype/index.html) | 中文精读正文与 Internet Archive 扫描页同步滚动 |
| [WebGL 文库首页](https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/content/demos/wholeearth_webgl_console_demo.html) | 147 期 Whole Earth 出版物的视觉索引 |
| [1985 Software Catalog 中文导读](content/readings/1985_software_catalog_full_chinese_reading.md) | 已完成中文导读，尚未整理成完整阅读室 |

## 中文说明

- 当前对外展示重点是 1974 年 *Whole Earth Epilog* 阅读室。
- 147 期出版物已经建立索引，页级 OCR dossier 覆盖 22,162 页。
- 后续目标不是一次性铺满全集，而是逐步把精选期刊做成可读、可查、可验证的中文阅读室。
- 仓库暂无正式开源许可证；原始出版物和扫描资料不因本项目而改变权利归属。
