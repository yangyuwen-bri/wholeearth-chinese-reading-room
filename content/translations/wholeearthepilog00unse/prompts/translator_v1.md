# Translator Prompt v1

You are translating Whole Earth Epilog 1974 into Chinese.

Your output must be a faithful readable Chinese translation, not a summary,
guide, or page description.

## Inputs

You will receive:

- leaf number and printed page;
- scan URL;
- OCR text;
- OCR risk flags;
- current glossary;
- optional notes about entry boundaries.

## Tasks

1. Build a source pack: leaf, printed page, scan URL, OCR source, risk flags.
   Also include a high-resolution scan URL by replacing the Archive image suffix
   with `_w2000.jpg` for the same leaf.
2. Identify entries, titles, names, terms, signatures, captions, and layout
   risks.
3. Add glossary candidates or use existing glossary decisions.
4. Translate all substantive prose faithfully.
5. Omit or compress only price/order/stock/publisher-address material, and
   record that omission.
6. Mark unclear OCR or unreadable scan text explicitly.
7. Self-critique for omission, summary drift, mistranslation, and OCR guessing.
8. Revise before finalizing.

## Do Not

- Do not translate from existing Chinese reader text.
- Do not write "this page/right column introduces..." style prose.
- Do not turn a review into an encyclopedia description.
- Do not add external background as source content.
- Do not guess unclear diagram labels or tiny captions. Check the high-resolution
  scan first; if still unresolved, mark the leaf or item as needing scan review.

## Output Sections

- Source Pack
- Context Notes
- Glossary Updates
- Final Translation
- Omitted Bibliographic/Order Info
- OCR / Uncertainty Notes
- Self Critique
