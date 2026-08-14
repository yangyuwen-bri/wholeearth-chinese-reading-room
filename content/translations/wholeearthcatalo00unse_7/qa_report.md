# QA Report

## Release State

Reader release accepted on 2026-08-15.

- Translation files: 132/132.
- Independent review files: 132/132.
- Review conclusions: `accepted` 132; `needs_highres_scan` 0; `revise` 0.
- Canonical `status.jsonl`: 132 contiguous leaves, all synchronized to `accepted`.
- Reader payload: 9 chapters and 132 translated sections.

## High-Resolution Scan Closure

The 29 inherited `needs_highres_scan` leaves were checked individually against
the Internet Archive w2000 scans:

`054, 056, 058, 060, 061, 063, 066, 070, 078, 088, 089, 090, 091, 092, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 118, 119, 120`.

- Twelve visibly broken or incomplete translations were reconstructed:
  `092, 103-111, 119, 120`.
- The other seventeen leaves were regressed against the scan and their reviews
  updated with page-specific evidence.
- Numeric fields, column ownership, captions, diagrams, poetry lineation,
  product groupings and cross-page boundaries were checked where applicable.

## Inherited-Accepted Regression

A whole-book reader audit found seven leaves whose old review label said
`accepted`, while the reader-facing body still contained fragmented machine
translation. Leaves `093-099` were therefore retranslated from the w2000 scans
and independently re-reviewed. Their principal entries now have coherent
reading order, source-bounded names and historical specifications.

Reader-facing text was also swept for workflow language and obvious OCR
artifacts. Editorial notes remain in the source packages, but do not leak into
the `Final Translation` sections shown in the reading room.

## Reader Integration

- Builder: `reader-prototype/build_fall_1969_reader_data.py`.
- Output: `reader-prototype/data/fall_1969_reader.json`.
- Route: `reader-prototype/index.html?issue=fall-1969`.
- Data validation confirms 9 chapters, 132 unique sections, non-empty HTML and
  `accepted` status on every section.
- `git diff --check` and Python compilation pass.

## Residual Boundaries

- The catalog preserves 1969-era prices, products, medical discussion and
  outdoor advice as historical material; they are not current recommendations.
- Some microscopic order, size and address fields remain intentionally omitted
  where the scan cannot support character-level certainty.
- The left scan panel is served directly from Internet Archive and therefore
  depends on archive.org availability; the Chinese reading text itself is
  generated locally.
