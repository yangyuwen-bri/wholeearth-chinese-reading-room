# Workflow Lessons

Use this file to record issue-specific findings that may improve the global
workflow later.

Do not edit global prompts or workflow rules silently during a batch. First
record the problem here, then decide whether it is issue-local or reusable.

## Issue-Specific Risks

- Dense counterculture layouts: many leaves mix columns, hand lettering,
  photographs, clipped letters, cartoons, and sideways text. Reconstruct the
  reading order from the scan; never trust OCR line order by itself.
- Heavy back-matter lists: late leaves contain dense addresses, prices, names,
  and transactional data. Every legible item must be translated or preserved;
  do not collapse them into a list description.
- OCR typography damage: display text and rotated material frequently produce
  nonsense OCR. Such elements require high-resolution visual verification
  before acceptance.
- Two excluded physical leaves: scandata contains 134 physical leaves but only
  132 public-access/OCR leaves. The package follows the verified access mapping
  and records both access and physical leaf numbers.

## Batch Lessons

| Date | Leaves | Problem | Local Fix | Promote to Template? |
| --- | --- | --- | --- | --- |
| 2026-09-02 | 000-131 | Initial source audit found complex mixed layouts and dense transactional back matter. | Require visual inventory and scan verification on every accepted leaf. | no |

## Prompt Change Log

| Prompt | Version | Reason | First Used On |
| --- | --- | --- | --- |
| `translator_v1_2.md` | `v1.2` | full-visible-content and anti-summary baseline | 2026-09-02 |

## Reader-Facing Leak Checks

Record any wording pattern that must stay out of public reader text.

- `Final Translation`
- `Self Critique`
- `OCR Notes`
- `leaf 001` as body heading
- page-description prose such as "right column" or "this page introduces"
- evidence-quality prose such as "legible source text", "readable cover text",
  or "OCR recovered"
