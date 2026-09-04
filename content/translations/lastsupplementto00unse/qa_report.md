# QA Report — March 1971 Last Supplement

## Corrective Audit — 2026-09-04

The previous report overstated release completeness. A reader parser stopped
at internal `##` source headings, dropping the second and third articles on
leaf `039` (printed page 38). An accepted review and matching deployment hash
did not detect the omission. The earlier blanket completeness claim is withdrawn.

## Verification Boundaries

| Check | Current evidence |
| --- | --- |
| Translation and review files | 132 of each, leaves 000–131 |
| Recorded translation status | 131 accepted records (mostly historical); leaf 035 downgraded to needs_highres_scan |
| Reader export coverage | All 132 rendered page bodies checked against explicitly delimited Final Translation sections |
| Fresh source-to-translation audit in this correction | Leaves 038 and 039 corrected; leaf 035 inspected but unresolved; the other 129 pages have not been re-audited in this correction |
| Overall fidelity re-audit | In progress; do not describe it as completed independent review |

## Completed Correction

- The shared reader parser now stops only at workflow metadata headings, not
  headings inside an article. It preserves repeated passages and internal titles.
- Leaf 039 retains all three headings and 23 paragraphs: 4 for Edgar Cayce,
  8 for The Readings, and 11 for The Ordinary Group, plus Peter Friedman's byline.
- Rechecking the original 2727×4165 scan also restored age 67, “most of” the
  forty-three years, and “before a class”. See this page's review for the inventory.
- Readings now uses 通灵解读 consistently with leaf 038, replacing the misleading
  instrument-reading term 读数 on leaf 039.
- The established display name is 中文阅读室. Added chapter guides are explicitly
  labelled as editorial material, not original text.
- Leaf 038 now identifies Charles as the sender of children's books, preserves
  the source's unusual “critical physical ability” wording and Everett Ireon
  spelling, and has a page-specific coverage inventory.
- Leaf 035's previous acceptance is withdrawn. Missing nursery rhyme, birthday
  lines, and planetary records were partially restored; Lenin's birth, calendar
  times, and the 15–30 planting date range were corrected. Two unsupported old
  passages were removed from the reading body, not replaced with summaries.
  Six explicitly bounded unresolved groups remain in the review. The reader
  shows a separate editorial notice; this page is not a complete translation.

## Reproducible Gates

```sh
# Expected to fail while leaf 035 is unresolved: full-book release stays blocked.
python3 content/translations/lastsupplementto00unse/tools/validate_release.py
python3 reader-prototype/build_march_1971_last_supplement_reader_data.py
# Explicit corrective draft only; pending pages require notices and matching reviews.
python3 reader-prototype/build_march_1971_last_supplement_reader_data.py --allow-pending-review
python3 -m unittest discover -s reader-prototype/tests -v
```

The builder independently checks its rendered payload against the source
package's workflow-delimited translation. Tests also check the saved JSON, so a
correct parser with stale deployed data cannot pass. Neither check proves that
the translation itself covers every source sentence; source fidelity still
requires per-page comparison with the original scans.

## Remaining Work

- Re-audit source coverage for the other 129 leaves, replacing generic review
  prose with page-specific inventories and explicit unresolved boundaries.
- Close leaf 035's six documented gaps without guessing. Prioritize other dense calendars, handwritten labels, poems,
  captions, and subscriber directories. Earlier scan-recovery claims must be
  checked, not inherited merely because a file is marked accepted.
- Keep source fidelity, reader coverage, and public deployment verification
  separate. A release hash proves artifact identity, not translation accuracy.
