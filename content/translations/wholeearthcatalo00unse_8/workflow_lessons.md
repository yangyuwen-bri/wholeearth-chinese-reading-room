# Workflow Lessons

Use this file to record issue-specific findings that may improve the global
workflow later.

Do not edit global prompts or workflow rules silently during a batch. First
record the problem here, then decide whether it is issue-local or reusable.

## Issue-Specific Risks

- Access vs. physical leaves: Archive access leaves `n0-n67` correspond to the
  68 OCR objects, while scandata also contains excluded color cards. Do not use
  physical `leafNum` directly as the public scan index.
- Multi-column reading order: large catalog pages contain several independent
  entries. Preserve entry boundaries and use scan evidence when OCR order is
  ambiguous.
- Access metadata: prices, fees, addresses, and page references are not
  automatically disposable. Retain them when they affect evaluation, access,
  comparison, or navigation.

## Batch Lessons

| Date | Leaves | Problem | Local Fix | Promote to Template? |
| --- | --- | --- | --- | --- |
| 2026-07-14 | n0-n6 | initial calibration | run full multi-agent loop before scaling | later |
| 2026-07-14 | n5-n6 | evidence-quality wording leaked into `Final Translation` | reviewer returned wording to translator; keep evidence quality in OCR notes | yes |

## Prompt Change Log

| Prompt | Version | Reason | First Used On |
| --- | --- | --- | --- |
| `source_provenance_v1.md` | `v1` | workflow v1.1 calibration | 2026-07-14 |
| `translator_v1.md` | `v1` | workflow v1.1 calibration | 2026-07-14 |
| `reviewer_v1.md` | `v1` | workflow v1.1 calibration | 2026-07-14 |
| `orchestrator_review_v1.md` | `v1` | workflow v1.1 calibration | 2026-07-14 |
| `translator_v1_1.md` | `v1.1` | remove evidence-quality wording from reader text | next batch |
| `reviewer_v1_1.md` | `v1.1` | detect evidence-quality wording as workflow leakage | next batch |

## Reader-Facing Leak Checks

Record any wording pattern that must stay out of public reader text.

- `Final Translation`
- `Self Critique`
- `OCR Notes`
- `leaf 001` as body heading
- page-description prose such as "right column" or "this page introduces"
- `来源文字可辨部分`
- `书封可辨文字`
