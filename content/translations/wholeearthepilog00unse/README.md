# Whole Earth Epilog Full Translation Workflow

This folder is the working area for a full, faithful Chinese translation of
`wholeearthepilog00unse`.

The existing reader text is not the translation base. It can be used only as
navigation context or as a warning example of over-summary. Production
translation must be based on OCR plus scan verification.

## Goal

Produce a faithful but readable Chinese translation that can later replace the
current Chinese close-reading text in the reader.

The translation should preserve substantive editorial writing, excerpts,
reviews, captions, titles, authors, signatures, and conceptual argument. It may
omit or compress prices, order addresses, stock numbers, and repetitive
bibliographic details when those details are not part of the prose.

## Source Priority

1. Archive scan image: final authority for visible page content.
2. Official IA DjVu XML OCR: primary machine text source.
3. OCR supplements: fallback only for official empty or unusable OCR pages.
4. Existing page dossiers and reader text: navigation aids only.

For scan checks, do not rely on `w500` alone. Derive a higher-resolution scan
URL from the same leaf, preferably:

`https://archive.org/download/wholeearthepilog00unse/page/n{leaf}_w2000.jpg`

Use `w1000` only when `w2000` is unavailable or unnecessary. A leaf with
diagrams, tables, maps, small captions, vertical labels, or low-contrast type
cannot be `accepted` if only `w500` was checked.

## Translation Loop

Each leaf or entry goes through this loop:

1. `source_pack`: record leaf, printed page, scan URL, OCR source, and risks.
2. `context_pass`: identify topic, entries, people, books, and layout risks.
3. `glossary_pass`: extract names, titles, and terms for consistency.
4. `draft_translation`: translate substantive content faithfully.
5. `self_critique`: check omissions, summary drift, OCR uncertainty, and tone.
6. `faithful_revision`: revise before review.
7. `independent_review`: judge fidelity against OCR and scan.
8. `human_accept`: only accepted output can enter later reader integration.

## Statuses

- `pending`: not started.
- `source_ready`: OCR and scan reference are available.
- `drafted`: initial translation exists.
- `self_checked`: translator completed self critique.
- `reviewed_needs_glossary`: otherwise viable, but terminology/title choices
  must be stabilized before acceptance.
- `needs_highres_scan`: diagram, caption, small type, or low-contrast text needs
  manual/high-resolution scan inspection.
- `revise`: substantive translation issue found.
- `blocked_ocr`: source text cannot be translated reliably from current OCR.
- `accepted`: reviewed and ready for later reader integration.
- `no_translation_needed`: non-substantive order/index/blank material only.

`accepted` is stricter than `pass`: title/term choices must be consistent, and
all visible substantive content must be either translated or explicitly marked
as omitted/unclear.

## Output Layout

- `leaves/leaf_###.md`: production leaf translations.
- `reviews/leaf_###.review.md`: review reports.
- `pilot/`: early workflow experiments; not production.
- `prompts/`: versioned prompts for translator and reviewer agents.
- `translation_standard.md`: project translation standard.
- `glossary.md`: project-wide title/name/term decisions.
- `status.jsonl`: one record per leaf, tracking progress and risks.

## Current Pilot

The first pilot covered:

- leaf 4 / p.453: `reviewed_needs_glossary`
- leaf 5 / p.454: `needs_highres_scan`

The pilot showed the loop can produce much fuller translations than the current
reader text, but also showed that glossary and image-crop checks must be formal
gates before batch rollout.
