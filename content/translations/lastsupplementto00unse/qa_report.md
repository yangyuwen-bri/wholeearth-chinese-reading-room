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
| Recorded translation status | 129 accepted records (mostly historical); leaves 008, 011 and 035 downgraded to needs_highres_scan |
| Reader export coverage | All 132 rendered page bodies checked against explicitly delimited Final Translation sections |
| Fresh source-to-translation audit in this correction | 17 pages corrected: 000–007, 009–010, 012–013, 034, 036–039; 008, 011 and 035 inspected but unresolved; the other 112 pages have not been re-audited in this correction |
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

## Additional Source Corrections — 2026-09-04

- Leaf 034: restored the Ron Boise / Thunder Machine caption and Peter & Helen
  Ready credit; repaired broken paragraph order and the literal-shadow mistranslation;
  preserved both four-line lyric quotations and their repetitions.
- Leaf 036: restored diagram layer labels, numbered Mineral/Vegetable/Animal/Human
  entries, Anima/Animus, and the second reflection statement. Retranslated Arthur's
  final two poem lines, restored nature/the heavens, and distinguished unconscious
  from subconscious. Poem line breaks and source footnotes remain visible.
- Leaf 037: corrected off-duty G.I., smoking dope, thumbing, and last place possible;
  restored electrical energy, source bylines and the memo's example qualifier.
- Browser inspection caught another export-order bug: the title splitter pulled
  the mid-page health memo heading above the preceding astrology continuation.
  Only a heading at the start of the page may now become its display title;
  internal headings remain in place. Regression tests check this order explicitly.
- These are executor corrections with page-specific scan inventories, not a new
  independent all-book acceptance. Leaf 035 remains unresolved.

## Front-of-Book Source Audit — 2026-09-04

- Rechecked leaves 000–013 against local high-resolution scans. Leaf 001's dedication
  required no translation change, but its review now records the actual inventory.
- Restored the cover's release slogan (not a byline), second beer label, article titles
  and authors on leaves 002/009, and the Barnes illustration credit.
- Replaced substantial omissions and column mixing in leaves 004–008: the complete
  Bible essay sequence, poems, lyrics and credits; the accident narrative's negation;
  three missing opening paragraphs and all Crime Stoppers labels on leaf 008.
- Restored the full Maslow quotation on leaf 010 and separated leaf 012's cartoon
  from Deboree's speech. Recovered its opening paragraph, three signs and nameplate.
- Corrected leaf 013's cosmic/comic confusion, inserted very, untranslated Dumb Bird
  bubble, and magic-cookie bush. Explicit line breaks retain poems and handwritten text.
- Leaf 008's handwritten illustration signature and leaf 011's two-line tiny road sign
  remain unresolved. Their prior acceptance is withdrawn; each has a visible reader notice.
- All 14 reviews are source-specific executor corrections, not an independent review.
- Verification: 19 regression tests pass; the saved 132-page payload matches all
  workflow-delimited translations. Local desktop rendering showed the correct n5 scan
  beside the restored poem; mobile rendering confirmed separate pending notices.
  The strict release gate correctly fails on leaves 008, 011 and 035.

## Reproducible Gates (Updated)

```sh
# Expected to fail while leaves 008, 011 and 035 are unresolved.
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

- Re-audit source coverage for the other 112 leaves, replacing generic review
  prose with page-specific inventories and explicit unresolved boundaries.
- Close leaf 035's six documented gaps, leaf 008's signature and leaf 011's small sign without guessing. Prioritize other dense calendars, handwritten labels, poems,
  captions, and subscriber directories. Earlier scan-recovery claims must be
  checked, not inherited merely because a file is marked accepted.
- Keep source fidelity, reader coverage, and public deployment verification
  separate. A release hash proves artifact identity, not translation accuracy.
