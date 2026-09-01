# Workflow Lessons

## Issue-Specific Risks

- Access/physical-leaf offset: public `n0` is physical leaf `1`; physical
  leaves `0` and `49` are excluded color cards. The historical page dossier
  copied scandata page types without applying that offset, so its text is
  usable but its page-type labels are shifted by one leaf.
- Cover as questionnaire: `n0` contains dozens of individually attributed
  statements with true/false boxes. They must remain separate and in visual
  reading order; a thematic summary is prohibited.
- Heterogeneous forms and letters: this supplement mixes long letters,
  financial forms, hand annotations, notices, corrections, captions, and
  transactional data. OCR line order is not a safe proxy for page order.
- Scan availability: drafting may use official OCR while Archive image access
  is unavailable, but no leaf may become `accepted` without adequate visual
  source evidence.

## Batch Lessons

| Date | Leaves | Problem | Local Fix | Promote to Template? |
| --- | --- | --- | --- | --- |
| 2026-09-01 | n0–n47 | Historical dossier page types were shifted by one physical leaf. | Rebuilt access mapping from `addToAccessFormats` in scandata; use DjVu object order for public leaves. | later |
| 2026-09-01 | n0 | Cover statements cross columns and carry attribution plus true/false boxes. | Treat each statement as an independent source unit and require scan-backed order review. | no |

## Prompt Change Log

| Prompt | Version | Reason | First Used On |
| --- | --- | --- | --- |
| `translator_v1_2.md` | `v1.2` | full visible-text coverage and anti-summary gate | 2026-09-01 |
| `reviewer_v1_2.md` | `v1.2` | scan-backed inventory and concrete omission audit | 2026-09-01 |

## Reader-Facing Leak Checks

- `Final Translation`
- `Self Critique`
- `OCR Notes`
- `leaf 001` as body heading
- page-description prose such as “本页介绍” or “右栏说明”
- evidence-quality prose such as “可辨识原文” or “OCR 已恢复”
