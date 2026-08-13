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
  the printed number visible in the scan and scandata for each leaf until one
  issue-wide rule has been mechanically verified.

## Batch Lessons

| Date | Leaves | Problem | Local Fix | Promote to Template? |
| --- | --- | --- | --- | --- |
| 2026-08-13 | n54 | OCR omitted a complete right column; old review checked only OCR-visible material | restored scan-visible prose and labels; returned page to independent review | yes: require scan-level coverage inventory |

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
