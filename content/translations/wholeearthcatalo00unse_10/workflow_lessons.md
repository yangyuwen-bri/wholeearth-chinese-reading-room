# Workflow Lessons

Use this file to record issue-specific findings that may improve the global
workflow later.

Do not edit global prompts or workflow rules silently during a batch. First
record the problem here, then decide whether it is issue-local or reusable.

## Issue-Specific Risks

- `physical/access offset`: scandata contains excluded color cards at physical
  leaves 0 and 135. Map public access leaves by filtering excluded pages first;
  do not pair access index directly with physical `leafNum`.
- `legacy dossier offset`: the existing generated dossier pairs access `nN`
  with physical metadata `N`, so its page type and printed page are shifted.
  Use the verified package source packs.
- `layout diversity`: contents, catalog procedure, price/order tables, diagrams,
  rotated matter, and weak/blank OCR must all appear in calibration.
- `section continuity`: keep the original Spring 1969 contents structure. Do
  not inherit reader groupings or guide labels from another issue.
- `back-matter pagination`: the contents page points Portola Institute to
  p.129, but a two-sided foldout/order insert appears at n130-n131 before the
  Portola page at n132; scandata numbers this sequence through p.132. Preserve
  both anchors instead of rewriting one to match the other.

## Batch Lessons

| Date | Leaves | Problem | Local Fix | Promote to Template? |
| --- | --- | --- | --- | --- |
| 2026-07-27 | corpus audit | access/physical metadata were offset in legacy dossier | build source packs by filtered scandata order and assert equal object counts | later |

## Prompt Change Log

| Prompt | Version | Reason | First Used On |
| --- | --- | --- | --- |
| `source_provenance_v1.md` | `v1` | reusable template baseline | 2026-07-27 |
| `translator_v1_1.md` | `v1.1` | reusable template baseline | 2026-07-27 |
| `reviewer_v1_1.md` | `v1.1` | reusable template baseline | 2026-07-27 |
| `orchestrator_review_v1.md` | `v1` | reusable template baseline | 2026-07-27 |
| `anchor_auditor_v1.md` | `v1` | reusable template baseline | 2026-07-27 |

## Reader-Facing Leak Checks

Record any wording pattern that must stay out of public reader text.

- `Final Translation`
- `Self Critique`
- `OCR Notes`
- `leaf 001` as body heading
- page-description prose such as "right column" or "this page introduces"
- evidence-quality prose such as "legible source text", "readable cover text",
  or "OCR recovered"
