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
| 2026-07-14 | n0-n67 | DjVu object index and scandata physical `leafNum` differ by one because excluded color cards remain in scandata | map access `nN` to OCR object `N` and physical scandata leaf `N+1`; verify printed pages independently | later |
| 2026-07-14 | n1-n13 | Archive page-image endpoint timed out while official OCR/XML remained available | allow source preparation and drafting from OCR, but block final acceptance for layout-, diagram-, caption-, or small-type-dependent content | already covered |
| 2026-07-15 | n0-n67 | Archive requests failed because the shell did not inherit the local proxy and direct DNS resolution was unreliable | use `curl -x http://127.0.0.1:7890`; cache the 68-page PDF under ignored `_local/scans/`; map access `nN` to PDF page `N+1` and verify the mapping visually before review | yes |
| 2026-07-15 | n0-n32 | several reviews still described omissions that had already been repaired in the leaf | rerun independent review after every translator revision; the orchestrator must compare the current review against the current leaf before updating status | yes |
| 2026-07-15 | n0-n67 | accepted translations still contained old "scan unavailable / needs verification" state in non-reader sections | before final acceptance, run a whole-issue stale-state audit across Source Pack, Context Notes, OCR Notes, Self Critique, reviews, `status.jsonl`, and `qa_report.md` | yes |

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
