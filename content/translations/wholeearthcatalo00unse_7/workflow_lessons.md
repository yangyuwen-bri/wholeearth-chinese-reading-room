# Workflow Lessons

Use this file to record issue-specific findings that may improve the global
workflow later.

Do not edit global prompts or workflow rules silently during a batch. First
record the problem here, then decide whether it is issue-local or reusable.

## Issue-Specific Risks

- `official OCR can omit a complete visible column`: confirmed on `n54`, where
  the w2000 scan exposed sand-casting prose, forge-welding instructions, anvil
  labels, and a supplier directory absent from the leaf's OCR transcript. A
  fluent translation of all OCR text is not evidence of page completeness.
- `generic review text can hide page-specific failures`: groups of inherited
  reviews repeat identical reasons across unrelated leaves. Re-audit against
  the scan and record concrete entry names, values, omissions, and fixes.
- `printed-page mapping is inconsistent across generated source packs`: trust
  the printed number visible in the scan and record any conflict with
  DjVu/scandata-derived metadata until one issue-wide rule has been
  mechanically verified.
- `a fluent summary is not a translation`: confirmed on `n118`, where the old
  public text converted a dense catalog page into themes while omitting the
  schedule grid, quotations, equipment list, prices, and addresses. Review
  must compare a scan-level content inventory with the final translation.
- `machine-translated OCR noise can look falsely complete`: confirmed on
  `n88`, where the seven-section template existed but the public text preserved
  broken English tokens, interleaved unrelated entries, and omitted most of the
  lower page. Structural presence checks must be paired with readability and
  scan-coverage checks.
- `generated page dossiers can truncate source text`: `pages.json` and
  `rawtext_*.txt` may stop at 6,000 characters even when the page word count
  shows more content. Before declaring an omitted tail unreadable, query the
  corresponding DjVu XML page object directly.
- `accepted can conceal synthesized quotations and summary substitution`:
  confirmed on `n7`, where three entries were reduced to descriptions and a
  Chinese blockquote combined several source passages instead of translating
  one quotation. Release review must inventory source blocks and map each one
  to the final translation; heading counts and fluent prose are not evidence.
- `accepted can contradict its own required fixes`: inherited reviews paired
  `accepted` with non-empty `Required Fixes` on 29 leaves. A conclusion and its
  action items must agree; release validation now rejects this combination.

## Batch Lessons

| Date | Leaves | Problem | Local Fix | Promote to Template? |
| --- | --- | --- | --- | --- |
| 2026-08-13 | n54 | OCR omitted a complete right column; old review checked only OCR-visible material | restored scan-visible prose and labels; returned page to independent review | yes: require scan-level coverage inventory |
| 2026-08-13 | n118 | old translation summarized a four-column page and omitted most verifiable fields | rebuilt column order and table from w2000; recorded page-number and address conflicts; returned page to independent review | yes: reject summary substitution |
| 2026-08-13 | n88 | machine-translated OCR interleaved entries and omitted most of two lower-page blocks | rebuilt three reading zones from w2000; preserved historical-medical framing; returned page to independent review | yes: add readability and coverage gates |
| 2026-08-13 | n89 | machine-translated OCR interleaved a long review with a product catalogue and stopped mid-page | separated the two main columns from the complete DjVu object; retained scan gates on product-field pairing | yes: add readability and coverage gates |
| 2026-08-14 | n90 | machine-translated OCR interleaved two mail-order catalogues with a shopping-guide review and stopped mid-page | rebuilt three reading zones from the complete DjVu object; retained scan gates on product fields | yes: add readability and coverage gates |
| 2026-08-14 | n100 | machine-translated OCR interleaved three outdoor suppliers and omitted most of the product page | rebuilt supplier and product groups from the complete DjVu object; retained scan gates on specifications | yes: add readability and coverage gates |
| 2026-08-14 | n101 | machine-translated OCR stopped inside one of six outdoor suppliers and preserved decorative noise | used complete page text plus coordinates to separate suppliers; retained scan gates on tables and fractional fields | yes: add coordinate-aware reconstruction |
| 2026-08-14 | n102 | machine-translated OCR interleaved three mail-order suppliers and hid the page's self-critical editorial aside | restored supplier regions and editorial voice from complete page text; retained scan gates on illustrated product tables | yes: preserve editorial asides |
| 2026-08-13 | n56, n58, n60, n61, n63, n66, n70, n78, n92 | generated dossier text stopped at 6,000 characters and hid or interleaved source tails | read complete DjVu page objects; repaired n56/n58/n60/n61/n63/n66/n70/n78, deferred dense n92 until scan access returns | yes: detect dossier truncation |
| 2026-08-15 | n7 and inherited accepted leaves | accepted review missed summary substitution and a synthesized quotation | suspended the release, added concrete coverage evidence and compression gates, reopened every leaf for scan-level review | yes: require source-to-translation coverage evidence |
| 2026-08-18 | inherited reviews | 29 accepted reviews still contained required fixes; summary wording survived ratio checks | reject accepted-plus-fixes and detect meta-summary phrases in final translations | yes: enforce conclusion/action consistency |
| 2026-08-18 | n17-n19 | summaries omitted a newsletter, a 15-row table, eight catalog entries, an entire space-grid entry, and mispaired patent numbers | rebuilt all source blocks from w2000 scans and recorded page-specific coverage evidence | yes: inventories must include tables and every independent catalog entry |

## Prompt Change Log

| Prompt | Version | Reason | First Used On |
| --- | --- | --- | --- |
| `translator_v1.md` | `v1` | initial template | `<date>` |

## Reader-Facing Leak Checks

Record any wording pattern that must stay out of public reader text.

- `Final Translation`
- `Self Critique`
- `OCR Notes`
- `leaf 001` as body heading
- page-description prose such as "right column" or "this page introduces"
- evidence-quality prose such as "legible source text", "readable cover text",
  or "OCR recovered"
