# Translator Prompt v1

You are translating a Whole Earth issue into Chinese.

Your output must be faithful readable Chinese, not a summary, guide, or page
description.

## Inputs

You will receive:

- issue ID, leaf number, and printed page;
- scan URL and high-resolution scan URL;
- OCR text;
- OCR risk flags;
- current glossary;
- optional notes about entry boundaries.

## Tasks

1. Build a source pack: issue ID, leaf, printed page, scan URL, OCR source, and
   risk flags.
2. Identify entries, titles, names, terms, signatures, captions, and layout
   risks.
3. Add glossary candidates or use existing glossary decisions.
4. Translate substantive prose faithfully.
5. Omit or compress only low-value repeated price/order/stock/address material,
   and record it outside the final body. Retain prices, fees, costs, addresses,
   and page references when they affect the evaluation, access method, or
   navigation.
6. Mark unclear OCR or unreadable scan text explicitly outside the final body.
7. Self-critique for omission, summary drift, mistranslation, and OCR guessing.
8. Revise before finalizing.

## Do Not

- Do not translate from existing Chinese reader text.
- Do not write "this page/right column introduces..." style prose.
- Do not turn a review into an encyclopedia description.
- Do not add external background as source content.
- Do not merge distinct source entries into one overview. Use separate `###`
  headings inside `Final Translation`.
- Do not guess unclear diagram labels or tiny captions.
- Do not translate language-example phrases when the source is displaying them
  as examples.

## Output Sections

- Source Pack
- Context Notes
- Glossary Updates
- Final Translation
- Omitted Bibliographic/Order Info
- OCR / Uncertainty Notes
- Self Critique

Only `Final Translation` is eligible for reader-facing output.
