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
| Recorded translation status | 132 accepted records: 127 closed with source evidence and 5 accepted with user-authorized, visibly disclosed source gaps (011/035/062/084/086) |
| Reader export coverage | Rebuilt after the page-exception decision: 132 sections, 34 regression tests pass, complete workflow-delimited bodies match saved JSON |
| Fresh source-to-translation audit in this correction | All 132 leaves inspected from cover to cover. The five authorized gaps were not deciphered; user permission changed their acceptance treatment, not the source evidence |
| Overall fidelity re-audit | Cover-to-cover executor audit performed; 035 remains an explicitly disclosed user-authorized page exception. This is not a new independent review |

## User-Authorized Page Exception — 2026-10-05

- The user approved treating leaf 035 (printed page 34, the Atlantis Almanac calendar insert) as a secondary page exception so it no longer blocks the reading-room release.
- The readable calendar, astronomical records, gardening list, song, and verified corrections remain in the translation. The Earth prose block, the longer May 6 white-text passage, and a small set of memorial lines, planetary glyphs, and handwriting remain omitted because the scans do not support reliable character-level transcription.
- `status.jsonl` records leaf 035 as `accepted` with both `source_exception` and `reader_notice`. This is a disclosed omission decision, not evidence that the omitted text was recovered or independently reviewed.

The table above is the current checkpoint. Earlier sections below retain the audit history; their intermediate counts and pending lists are not current totals.

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

## Interview and Inserted Pages — 2026-09-04

- Re-audited leaves 014–021, including the complete Hoover Vacuum interview through
  its final answer on leaf 021, the Guns insert, Steal This Book advertisement,
  Blue Phantom story and the opening Weather Bureau article.
- Corrected invented SNS wording, reversed negation, wrong speaker, omitted questions,
  Indian/Daily News/Money Warfare mistakes, and missing large titles and image credits.
- The interview resumes on leaf 019 after two inserted pages; notes record this exact
  sequence. Source 13:11 and the 4-F card are now retained, with no summary substitutions.
- These eight pages now have specific source inventories and updated character counts.
- Verification: the rebuilt payload passes 20 regression tests, including explicit
  interview/insert order and restored small-label checks. Strict release remains blocked
  on the three documented unresolved pages; corrective export is explicitly opt-in.

## Law and Computer Activism — 2026-09-04

- Re-audited leaves 022–025. Restored the Weather Underground credit, corrected Giap
  and legal/metaphorical terms, and recovered the missing connect-the-dots / monster
  passage in Law as a Revolutionary Tool.
- The continuation retains Jab, KK, all quotations and all 12 lines of the King Kong poem.
  Blow the judge's and jury's minds is translated as intellectual shock, not physical injury.
- Retranslated leaf 025 from its scan: restored the 1984 / 13 years early title, all five
  issues, Jerry Mayer, Interrupt 14 and 137 West 14th Street. Withdrawn wording had
  conflated Honeywell, military intelligence and IBM into unsupported CIA/South Asia claims.
- Remaining fresh source audit starts at leaf 026 (apart from already completed 034/036–039).
- Verification: 21 regression tests pass and all 132 saved page bodies match the current
  translations. Strict complete-release validation still fails on 008, 011 and 035.

## Mantras, Sufism, Yoga and Lyrics — 2026-09-04

- Re-audited leaves 026–033 against their high-resolution scans. Rebuilt Mantras'
  column order and repeated prayer; restored its final paragraph and Have Faith!
  caption. Restored Sufism's title and corrected its cross-page book review.
- Recovered the omitted dervish dialogue and action, distinguished the Bindu to
  Ojas review from its preceding story, and retained the sundae / Sunday school pun.
- Removed the invented 15-dollar price: the original reads ॐ 15, paired with
  ॐ CVII on the other illustration. Retained all four PARADOX repetitions.
- Restored numbered sutras, the Yoruba tale's actors and hot amala, and both
  labels on the Hell's Angels emblem. Recovered the large omitted opening-right
  paragraph on leaf 033, full repeated lyrics, allusions and a separate footnote.
- These are executor corrections, not new independent reviews. Remaining fresh
  audit: 040–131, plus the unresolved items on 008, 011 and 035.

## Reproducible Gates

```sh
# Strict release validation now passes with five user-authorized, visibly disclosed source exceptions.
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

- Leaf 035 remains a disclosed page-level exception: six documented source-gap
  groups include two prose passages, not only signatures or prices. The user
  explicitly authorized this exception, so it no longer blocks the release;
  the reader notice keeps the omission visible.
- The user's 2026-09-04 reply explicitly allowed unrecoverable minor details
  after checking the original. Accordingly 011's small sign, 062's signature,
  084's cartoon price and 086's damaged name no longer block page acceptance.
  Each has a source_exception, permitted-omission review and visible notice.
  This is permission to retain disclosed gaps, not new transcription evidence.
  No further scan request to the user is needed for these four details.
- Rechecking 062's original also exposed a missing Chinese predicate in the
  Hazlitt quote. Restored is struck by as 所触动; this is not covered by the
  signature exception. Regression tests protect that predicate, the exception
  notices and the prohibition against silently waiving 035's prose.
- The updated local browser renders all 132 sections, the 132-page reading-room
  preface, all five authorized-gap notices and the repaired
  Hazlitt predicate. The prior preview process returned empty HTTP responses;
  restarted this task's port-4191 server and verified JSON HTTP 200 and DOM load.
- Leaf 008's signature is Cieciorka. Leaf 082's suspected boar inscription is
  actually miniature architecture and seated figures, verified against the same
  painting in color. The older sections below record earlier checkpoints, not
  current unresolved status.
- Keep source fidelity, reader coverage, and public deployment verification
  separate. A release hash proves artifact identity, not translation accuracy.

## Source Audit Through Leaf 131 — 2026-09-04

- Rebuilt the seven remaining six-column directory pages (119–125) from scan
  inspection: 230, 239, 235, 238, 246, 246 and 214 postal records respectively.
  Preserved separate and repeated names, source spellings, fractional house
  numbers, state/country headings, addresses and military unit identifiers.
  Translated institutional descriptions without inventing standardized names.
- Restored the complete Max Picard quotation on 125; Meher Baba information
  heading on 126; all ten left-column notices and the middle/right continuations
  on 127; the full Realist subscription form and book/interview listing on 128;
  the June 11 closing-party invitation and RSVP instructions on 129; the complete
  talcum-powder aside on 130; and the title, quotation and mailing imprint on 131.
  Yippie in 128 means a Youth International Party member, not a Yuppie.
- Corrected 127's press cards, aboveground alternatives, address line and
  cross-column continuation, and 129's party date and total attendance count.
  Historical fuel/product and talc claims have separate editorial notices; the
  original-text translation does not contain added safety advice.
- Resolved 082 using the matching color painting at
  https://ferrebeekeeper.wordpress.com/wp-content/uploads/2010/12/varaha.jpg:
  the alleged inscription consists of temples and seated figures. No new source
  text was inferred or replaced with an image description.
- A 1991 reprint of Flip Decision, found at
  https://random-happenstance.blogspot.com/2026/07/its-coin-toss-whether-or-not-you-like.html,
  confirms the same two small sign rows and arrows on 011, but does not establish
  a reliable literal reading. The leaf remains pending. Likewise, Realist 89
  scans of printed pages 61, 83 and 85 do not resolve the signature, price or name.
- Latest local verification: all 132 source bodies match saved reader JSON,
  32 regression tests pass, and git diff --check passes. Strict release validation
  fails only on 011/035/062/084/086. The corrected artifact has not been published.
- Browser verification on the local corrective reader confirmed 132 DOM sections,
  the current 127/5 preface, distinct editorial notices with no duplicated prefix,
  and 15 rendered separators on leaf 127. The scan finished loading at n127 with
  printed page 126, matching the Chinese page. Screenshots also checked the
  preface and the first subscriber table. This is not a public deployment check.
- Corrected the stale preface and literal Markdown separators, and standardized
  Ken Kesey as 肯·凯西 on leaves 127/128/130. New regression checks cover the
  preface/status agreement, thematic breaks and these name occurrences.

## Source Audit Through Leaf 099 — 2026-09-04

- Corrected leaves 072–099 against original full-resolution scans, with individual
  source inventories. Restored omitted lyrics in musical scores, the downers
  paragraph and cartoon text, the voter/politician paragraph, the military article
  opening, and the final lead-poisoning committee paragraph.
- Fixed misread titles, names, ages, negations, column order and page-spanning
  sentences. Actual source repetitions and historical claims remain intact.
- Leaves 082 (boar inscription), 084 (one cartoon price), and 086 (damaged name)
  are reopened, not falsely accepted. Nancy Mann on 099 was resolved using the
  scan and the original-book authorship record at Wellcome.
- Added separate, sourced historical safety notices for ginseng/strychnine,
  dentistry, unsafe propane leak testing, and obsolete blood-lead thresholds.
  These notices are not inserted into the original-text translation.
- Restored the immutable official OCR evidence blocks after detecting accidental
  name substitutions in nine blocks; translation corrections remain separate.
- Not a new independent review, not yet a completed book, and not yet deployed.

## Source Audit Through Leaf 118 — 2026-09-04

- Rechecked leaves 100–113: restored the anti-vaccination essay's qualifications,
  missing alginate continuation, complete drug-policy citations and repeated
  quotations, the CIA article's cross-page opening and omitted Joel Fort passage,
  the full manuscript letter, alternative-community report and Dream article.
- Rechecked disputed values against scan crops: 1969-04-13, 350 personnel,
  $5,000, CN 221, March 16, and two-thirds/one-third cups. Original source
  disagreements, historical claims, slurs and repeated text are not normalized.
- Rebuilt leaves 114–118 from column-by-column scan inspection: 231 name/location
  rows on 114 and 203/242/240/243 postal records on 115/116/117/118. Restored
  the full comic and editorial, omitted names and addresses, fractional house
  numbers, state headings and descriptive institution names. Names and historical
  postal identifiers retain their original spelling, including source errors.
- Disabled the obsolete directory OCR copier: rerunning it now fails without
  modifying translations or status. Regression coverage verifies this safeguard,
  record counts, source repetitions and restored late-book text units.
- Added separate non-source notices for historical anti-vaccination claims,
  alginate research, gas kilns and borax. Sources include WHO's smallpox history
  (https://www.who.int/health-topics/smallpox), propane safety
  (https://propane.com/safety/safety-guide-for-propane-users/) and Poison Control
  (https://www.poison.org/articles/borates). Original translations are unchanged
  by these editorial notices.
- Rebuilt 132 reader sections; 29 tests and git diff --check pass. All 132 official
  OCR evidence blocks are byte-identical to HEAD. The strict release gate fails
  only on the six documented pending leaves. This is an executor audit checkpoint,
  not completed independent review and not a public deployment.
