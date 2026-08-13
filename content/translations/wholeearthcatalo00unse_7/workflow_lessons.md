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

## Batch Lessons

| Date | Leaves | Problem | Local Fix | Promote to Template? |
| --- | --- | --- | --- | --- |
| 2026-08-13 | n54 | OCR omitted a complete right column; old review checked only OCR-visible material | restored scan-visible prose and labels; returned page to independent review | yes: require scan-level coverage inventory |
| 2026-08-13 | n118 | old translation summarized a four-column page and omitted most verifiable fields | rebuilt column order and table from w2000; recorded page-number and address conflicts; returned page to independent review | yes: reject summary substitution |
| 2026-08-13 | n88 | machine-translated OCR interleaved entries and omitted most of two lower-page blocks | rebuilt three reading zones from w2000; preserved historical-medical framing; returned page to independent review | yes: add readability and coverage gates |
| 2026-08-13 | n56, n60, n61, n66, n92 | generated dossier text stopped at 6,000 characters and hid source tails | read complete DjVu page objects; repaired n56/n60/n61/n66, deferred dense n92 until scan access returns | yes: detect dossier truncation |

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
