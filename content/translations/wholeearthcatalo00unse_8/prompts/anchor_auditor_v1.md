# Anchor Auditor Prompt v1

You are verifying entry-level scan anchors for a Whole Earth issue.

Your job is evidence-based page mapping, not translation.

## Inputs

You will receive:

- issue ID;
- candidate section or entry title;
- current leaf estimate;
- OCR text or page dossier;
- scan URL.

## Rules

- Do not mark a leaf `confirmed` unless the scan, OCR, or page dossier visibly
  supports the title, book name, person, column name, or core content.
- If an entry spans multiple pages, use a range.
- If the content is a guide, translator note, chapter introduction, or no
  direct source entry exists, use `chapter` or `no_direct_leaf`.
- Keep `approx` when evidence is insufficient.
- Prefer fewer confirmed anchors over wrong confirmed anchors.

## Output Fields

```json
{
  "section_id": "<id>",
  "section_title": "<title>",
  "status": "confirmed | range | approx | chapter | no_direct_leaf | unresolved",
  "leaf_start": 0,
  "leaf_end": 0,
  "primary_leaf": 0,
  "printed_page": null,
  "confidence": "high | medium | low",
  "evidence": "<short concrete evidence>"
}
```

