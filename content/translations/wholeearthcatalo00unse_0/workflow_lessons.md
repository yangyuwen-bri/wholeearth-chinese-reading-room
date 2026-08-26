# Workflow Lessons

Use this file to record issue-specific findings that may improve the global
workflow later.

Do not edit global prompts or workflow rules silently during a batch. First
record the problem here, then decide whether it is issue-local or reusable.

## Issue-Specific Risks

- Access/physical-leaf offset: the three non-access physical pages mean public
  `n0` is physical leaf `2`; build packs by zipping DjVu objects to scandata
  only after excluding `addToAccessFormats=false` pages.
- Dense contents/index: `n3`–`n4` are multi-column and cannot be translated in
  raw OCR order. Inventory each column and every page reference from the scan.
- Summary substitution: descriptions such as “本页介绍” or merged overview
  prose are release-blocking defects, even when they mention the right topic.

## Batch Lessons

| Date | Leaves | Problem | Local Fix | Promote to Template? |
| --- | --- | --- | --- | --- |
| 2026-08-26 | n0–n147 | Public access leaves do not equal physical scan leaves. | Verified DjVu/scandata positional mapping and excluded three non-access pages. | later |
| 2026-08-26 | n3–n4 | OCR destroys dense index reading order. | Use the high-resolution scan as layout authority and translate every entry. | no |

## Prompt Change Log

| Prompt | Version | Reason | First Used On |
| --- | --- | --- | --- |
| `translator_v1_2.md` | `v1.2` | full visible-text coverage and anti-summary gate | 2026-08-26 |
| `reviewer_v1_2.md` | `v1.2` | scan-backed inventory and concrete omission audit | 2026-08-26 |

## Reader-Facing Leak Checks

Record any wording pattern that must stay out of public reader text.

- `Final Translation`
- `Self Critique`
- `OCR Notes`
- `leaf 001` as body heading
- page-description prose such as "right column" or "this page introduces"
- evidence-quality prose such as "legible source text", "readable cover text",
  or "OCR recovered"
