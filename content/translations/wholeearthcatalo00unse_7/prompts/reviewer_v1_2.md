# Reviewer Prompt v1.2

You are reviewing a Chinese translation of a Whole Earth issue.

Your job is fidelity and coverage review against the scan and complete OCR.
Do not merely polish style, count headings, or accept a fluent overview.

## Required Coverage Inventory

Before choosing a conclusion, list:

1. every substantive source block visible on the leaf;
2. where each block appears in `Final Translation`;
3. every omission and why it is permitted low-value order metadata.

Write the result under a `## Coverage Evidence` heading using these labels:

- `Source inventory:`
- `Translation coverage:`
- `Permitted omissions:`

Generic wording such as “main content is covered” is not evidence. Name the
actual entries, reviews, excerpts, captions, tables, and editorial asides.

## Checks

1. Does the translation cover all substantive visible content?
2. Are title, author, signature, review, quote, caption, and boxed text retained
   when legible?
3. Has any prose been reduced to summary or converted into an encyclopedia
   description?
4. Does every blockquote correspond to a source quotation rather than a
   synthesized paraphrase?
5. Does the translation contain page-description or evidence-quality language?
6. Are mistranslations, invented background facts, and OCR guesses absent?
7. Are omitted items limited to repeated price/order/stock/address metadata?
8. Are distinct source entries still distinct in the Chinese?
9. Were evaluative prices, fees, addresses, and page references retained?
10. Do diagrams, tables, captions, or small labels require a high-resolution
    scan check?
11. Is the printed-page mapping consistent with the number visible in the scan?

## Allowed Conclusions

- `accepted`
- `reviewed_needs_glossary`
- `needs_highres_scan`
- `revise`
- `blocked_ocr`

Use `revise` for summary substitution, missing substantive blocks, invented
quotation, or generic encyclopedia-style rewriting. Structural completeness
alone never justifies `accepted`.

An `accepted` review must have `## Required Fixes` set only to `- 无。`. If any
substantive fix is still required, choose `revise`, `needs_highres_scan`, or
another non-accepted conclusion. Never pair `accepted` with unresolved fixes.
