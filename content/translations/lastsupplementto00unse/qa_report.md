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
| Recorded translation status | 132 accepted records; historical labels, not a fresh all-page fidelity audit |
| Reader export coverage | All 132 rendered page bodies checked against explicitly delimited Final Translation sections |
| Fresh source-to-translation audit in this correction | Leaf 039 only; the other 131 pages have not been re-audited in this correction |
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

## Reproducible Gates

```sh
python3 content/translations/lastsupplementto00unse/tools/validate_release.py
python3 reader-prototype/build_march_1971_last_supplement_reader_data.py
python3 -m unittest discover -s reader-prototype/tests -v
```

The builder independently checks its rendered payload against the source
package's workflow-delimited translation. Tests also check the saved JSON, so a
correct parser with stale deployed data cannot pass. Neither check proves that
the translation itself covers every source sentence; source fidelity still
requires per-page comparison with the original scans.

## Remaining Work

- Re-audit source coverage for the other 131 leaves, replacing generic review
  prose with page-specific inventories and explicit unresolved boundaries.
- Prioritize dense calendars (including leaf 035), handwritten labels, poems,
  captions, and subscriber directories. Earlier scan-recovery claims must be
  checked, not inherited merely because a file is marked accepted.
- Keep source fidelity, reader coverage, and public deployment verification
  separate. A release hash proves artifact identity, not translation accuracy.
