# Epilog anchor audit report

Updated: 2026-07-08T18:02:02+08:00

## Summary

- Anchors audited: 111 / 111 reader sections
- `confirmed`: 19
- `range`: 71
- `chapter`: 10
- `no_direct_leaf`: 11
- `approx`: 0
- `unresolved`: 0

This pass covers the full current `epilog_reader.json` section list. It is an anchor audit only: no Chinese body text, reader HTML, build script, or generated reader JSON was edited.

## Method

- Downloaded Archive `page/n{leaf}_w500.jpg` scans for leaves 0-321 and generated chapter contact sheets.
- Manually inspected the chapter contact sheets and, where needed, individual page images.
- Used only visible scan evidence: section headings, book titles, names, page labels, column labels, images, or core page content.
- Kept synthetic reader sections as `chapter` or `no_direct_leaf` rather than upgrading them to `confirmed`.

## Important Corrections

- The prompt example placing Ladies’ Home Journal / Hoky / New Dog / New Woman at leaf 142 is not correct for Archive `n{leaf}`. Archive leaf 142 is a FOOD page with Natural Foods Cookbook / Vegetarian Epicure. Homemaking / pets / women are Archive leaves 131-133, and the reader section spans 131-134 because it includes fitness context.
- Front matter ends at leaf 2. Archive leaf 3 is already the Understanding Whole Systems chapter page, printed p.452.
- Local OCR/page dossier records remain useful but are offset by +1 against Archive scan leaves for body pages. The audit JSON uses Archive scan leaf numbering.
- Archive leaf 321 is the back cover (`Stay hungry. Stay foolish.`). Archive leaf 322 is a scan calibration page and is excluded.

## Non-contiguous Or Broad Reader Sections

- `ch08-s07`: survival/camping/climbing is visible at leaf 206 and 209-214; fishing pages 207-208 sit between those source pages.
- `ch08-s09`: fishing is visible at leaf 207-208, while late-arrivals vehicle/wilderness material is visible at leaf 219-220. The JSON includes `leaf_ranges` for the actual visible spans.
- `ch10-s03` and `ch10-s04` intentionally overlap at leaves 275-276 because the Chinese reader separates education materials from games/media/nature, while the original spread transitions continuously.

## Uncertain Or Easy To Misread

- No rows are left as `approx` or `unresolved` in this pass, but several broad `range` rows have `confidence: medium` where one Chinese reader section synthesizes several adjacent original headings.
- `chapter` rows are chapter contents/guide pages, not catalog entries.
- `no_direct_leaf` rows are translator notes or Chinese synthetic closing sections.
