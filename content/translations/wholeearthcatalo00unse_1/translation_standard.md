# Translation Standard

## Core Standard

The target is faithful readable Chinese: clear enough for a public Chinese
reader, but faithful enough to stand as a translation rather than a summary.

Translate the English source. Do not translate existing Chinese reader text.

## Required Coverage

Translate substantive content:

- titles, subtitles, author names, editor/reviewer signatures;
- editorial reviews and recommendations;
- quoted excerpts and boxed prose;
- captions and labels when legible;
- section or column titles when they carry meaning;
- arguments, examples, jokes, irony, hesitation, and evaluative tone.

Translate all legible order and bibliographic metadata in full, including
prices, stock numbers, postage, order addresses, repeated publisher/order
lines, page references, and dense index entries. Repetition is part of the
source and is not permission to compress it.

If OCR and high-resolution scans cannot recover a visible element, document
the exact unresolved boundary outside the reader-facing body and keep the leaf
out of `accepted`. Never replace unresolved source text with a summary or page
description.

## Prohibited Drift

Do not:

- summarize the source as a guide or essay;
- write page-description prose such as "the right column introduces...";
- convert reviews into encyclopedia entries;
- add background knowledge as if it appeared in the source;
- silently guess OCR-unclear words;
- improve readability by deleting argument steps;
- merge distinct source entries into one Chinese overview;
- translate source-language example phrases when the page is displaying that
  language as an example.

## Readability

Chinese sentences may be shorter than the English. Keep logic, tone, and
sequence intact.

Preserve stance and intensity. If the source is compressed, witty, polemical,
or uncertain, the Chinese should not flatten it into neutral explanation.

Use Chinese punctuation. Keep spaces between Chinese and English/numbers in
mixed text.

## Names, Titles, and Terms

For first occurrence of an important title, person, institution, or concept,
prefer:

```text
中文译名（English Original）
```

Later occurrences may use the agreed Chinese form.

If a decision is unstable, mark the glossary entry as `provisional`. Do not
mark recurring major terminology as accepted until it is stable.

## OCR and Scan Rules

The scan is the final authority. OCR may be corrected when the scan visibly
supports the correction.

If source text remains unclear, write an uncertainty note outside the final
reader-facing translation:

```text
[OCR unclear: original fragment or description]
```

For diagrams, tables, tiny captions, vertical labels, or low-contrast type,
check high-resolution scans before acceptance.

## Review Standard

Reviewer decisions:

- `accepted`: faithful, complete, and glossary-consistent.
- `reviewed_needs_glossary`: translation is viable, but title/term choices
  require stabilization.
- `needs_highres_scan`: image text or diagram labels are unresolved.
- `revise`: translation has omission, mistranslation, summary drift, or tone
  drift.
- `blocked_ocr`: source cannot be recovered enough for translation.

Reviewers identify fidelity problems first. Style polish is secondary.

`no_translation_needed` does not remove the file/review requirement. Translate
any visible non-index heading, instruction, caption, or quotation before using
that status.
