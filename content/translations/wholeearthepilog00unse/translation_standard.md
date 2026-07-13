# Translation Standard v1

## Core Standard

The target is faithful readable Chinese: readable enough for a public Chinese
reader, but faithful enough that it can stand as a translation rather than a
summary or guide.

Do not translate the current Chinese reader text. Translate the English source.

## Required Coverage

Translate:

- titles, subtitles, author names, editor/reviewer signatures;
- editorial reviews and recommendations;
- quoted excerpts and boxed prose;
- captions and labels when legible;
- section or column titles when they carry meaning;
- arguments, examples, jokes, irony, hesitation, and evaluative tone.

You may omit or compress:

- prices;
- order addresses;
- stock numbers;
- repeated publisher/order lines;
- purely bibliographic details that do not affect the prose.

Any omission must be recorded in an `Omitted Bibliographic/Order Info` section.

## Prohibited Drift

Do not:

- summarize the source as a guide or essay;
- write page-description prose such as "the right column introduces...";
- convert reviews into encyclopedia entries;
- add background knowledge as if it were in the source;
- silently guess OCR-unclear words;
- make the Chinese more elegant by deleting argument steps;
- merge distinct entries unless the source actually presents them as one unit.

## Readability Rules

English long sentences may be split into Chinese sentences. Keep the logical
relations intact.

Preserve original stance and intensity. If the source is compressed, witty,
ironic, polemical, or uncertain, the Chinese should not flatten it into neutral
explanation.

Use Chinese punctuation. Keep spaces between Chinese and English/numbers in
mixed text.

## Names, Titles, and Terms

Consistency matters more than matching the old reader.

For the first occurrence of an important title, person, institution, or concept,
use:

`中文译名（English Original）`

Later occurrences may use the agreed Chinese form.

If there is no stable decision yet, mark the glossary entry as `provisional`.
Do not block translation only because a title decision is provisional, but do
not mark the leaf `accepted` until major recurring terms are stable.

## OCR and Scan Rules

The scan is the final authority. OCR can be corrected when the scan visibly
supports the correction.

If the scan or OCR is unclear, write:

`[OCR unclear: original fragment or description]`

For diagrams, tables, tiny captions, vertical labels, and low-contrast type,
check a high-resolution scan first, preferably the `w2000` Archive image for
that leaf. Use `needs_highres_scan` unless the text can be confidently read
from OCR plus the high-resolution scan.

## Review Standard

Reviewer decisions:

- `accepted`: faithful, complete, and glossary-consistent.
- `reviewed_needs_glossary`: translation is otherwise viable, but title/term
  choices require stabilization.
- `needs_highres_scan`: image text or diagram labels are unresolved.
- `revise`: translation has omission, mistranslation, summary drift, or tone
  drift.
- `blocked_ocr`: source cannot be recovered enough for translation.

Reviewers should not primarily polish style. They should identify fidelity
problems and force revision when necessary.
