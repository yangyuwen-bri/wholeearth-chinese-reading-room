# 全球概览中文阅读室

Whole Earth Chinese Reading Room is a Chinese close-reading project for the Whole Earth family of publications, including *Whole Earth Catalog*, *Whole Earth Epilog*, *CoEvolution Quarterly*, *Whole Earth Software Catalog*, and *Whole Earth Review*.

The project turns scanned issues into reader-facing Chinese guides, structured reading rooms, and page-linked research material. It is not a bulk OCR dump. Each published issue is treated as an edited reading object: original scan, Chinese guide, section structure, and page-level evidence stay connected.

**Live site:** <https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/>

## What is published now

| Status | Issue | Entry point | Notes |
| --- | --- | --- | --- |
| Open reading room | *Whole Earth Epilog*, October 1974 | `reader-prototype/index.html` | Chinese close-reading text with synchronized Internet Archive scan pages. |
| Chinese guide | *Whole Earth Software Catalog 2.0*, Fall 1985 | `content/readings/1985_software_catalog_full_chinese_reading.md` | Full guide and page-level reading notes; not yet promoted to a complete reading room. |
| Archive atlas | 147 Whole Earth issues | `content/demos/wholeearth_webgl_console_demo.html` | WebGL console for navigating the publication series and routing issues by reading status. |

## Public interface

The public home page is a WebGL signal console:

- 147 issues orbit a central Earth model.
- The right-hand signal panel shows the selected issue and its reading status.
- Issues are routed as `开放阅读室`, `导读本`, `阅读地图`, `已建索引`, or `原始扫描`.
- The current featured issue is *Whole Earth Epilog*, October 1974, with a direct link into the Chinese reading room.

This interface is intended to become the front door for future Chinese reading rooms, not just a one-off demo.

## Editorial model

The project separates three layers:

1. **Reading room**: the reader-facing product. It combines Chinese editorial text with source scan navigation.
2. **Guide and map**: intermediate public material for issues that have been studied but not yet rewritten as full reading rooms.
3. **Workbench**: OCR dossiers, page evidence, bibliography audits, anchor checks, and scripts used to verify the reading material.

Promotion from workbench to public reading room is manual and selective. The goal is a small number of high-quality Chinese reading rooms, not automatic coverage of every issue.

## Current data foundation

- 147 issues are indexed.
- Page-level OCR dossiers cover 22,162 pages.
- Coverage QA currently passes for 147/147 issues.
- The 1974 Epilog reader uses Archive leaves 0-321; leaf 321 is the back cover and leaf 322 is a scanner calibration page.
- Body printed-page mapping for 1974 Epilog uses `printed page = leaf + 449`.

## Repository structure

```text
content/
  assets/          # cover thumbnails, Earth textures, and small visual assets
  data/            # publication-level metadata for the public atlas
  demos/           # WebGL and visual navigation prototypes
  maps/            # issue maps and visual reading guides
  readings/        # Chinese guide and close-reading drafts
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

`_local/` is intentionally ignored. It contains local caches, source PDFs, logs, and QA screenshots that can be regenerated or are not meant for the repository.

## Run locally

The site must be served over HTTP because the reading room and WebGL console load JSON and module scripts.

From the repository root:

```bash
python3 -m http.server 8911
```

Then open:

```text
http://127.0.0.1:8911/
```

Useful direct paths:

- `content/demos/wholeearth_webgl_console_demo.html`
- `reader-prototype/index.html`
- `content/maps/wholeearth_macro_atlas.html`

## Deployment

The public site is currently deployed with GitHub Pages from the `gh-pages` branch.

Development happens on normal source branches such as `codex/visual-atlas-prototype`. Static files are then copied to `gh-pages` for publication.

Future hosting can move to Cloudflare Pages without changing the core architecture: this repository already works as a static site. A Worker or Pages Function should only be added when the experimental issue-agent layer needs a server-side API key.

## Roadmap

- Stabilize the WebGL console as the permanent library home page.
- Promote future issues into `/readers/<issue>/` style reading rooms.
- Move finished reader-facing content away from workbench drafts.
- Add issue-level status metadata so the homepage does not hard-code publication routes.
- Keep the issue-agent retrieval system separate until it has a public-safe backend.

## Sources and rights

This is an independent educational and research project. Source scans and publication metadata are linked back to Internet Archive and Whole Earth source pages where available. Original Whole Earth publications remain the property of their respective rightsholders.

Public pages should prioritize commentary, guide text, structured navigation, and links to original scans. Workbench material may contain fuller OCR-derived notes for private research and editorial verification.
