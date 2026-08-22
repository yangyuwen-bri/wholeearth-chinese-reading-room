# QA Report

Update this file after each completed role handoff.

## Status Counts

- `pending`: 0
- `source_ready`: 0
- `drafted`: 0
- `self_checked`: 0
- `reviewed_needs_glossary`: 0
- `needs_highres_scan`: 0
- `revise`: 0
- `blocked_ocr`: 0
- `accepted`: 134
- `no_translation_needed`: 0

## Remaining Blockers

- None. All 134 public access leaves, n0-n133, have passed source preparation,
  translation, independent review, required revision and regression where
  applicable, glossary synchronization, and orchestrator acceptance.

## Notes

- Verified corpus: 134 public access leaves, `n0-n133`.
- Official DjVu OCR contains 168,352 word tokens before correction.
- Physical scan leaves 0 and 135 are excluded color cards.
- The legacy page dossier has a one-leaf metadata offset and is not an
  authoritative source for page type or printed-page mapping.
- Expected issue risks include dense multi-column contents, prices/order tables,
  diagrams, small captions, rotated back matter, and at least one leaf with
  unusable official OCR. These require high-resolution scan checks.
- n3 demonstrated the return loop: its shifted three-column contributor list
  and incorrect printer name were corrected, independently re-reviewed, and
  accepted only after the second review.
- n130 demonstrated that rotation direction is source metadata: the stored
  image is counter-clockwise and must be rotated 90 degrees clockwise before
  main-text review; the oppositely oriented form fields need a second check.
- n72 demonstrated that diagram review must preserve node progression, row
  labels, numeric angles, repeated edit markers, material labels, and exact
  source-language examples. All five fix groups passed independent re-review.
- n5 demonstrated that image-based charts cannot be reduced to a free-standing
  label list. Its electromagnetic-spectrum scale, unaided/aided ranges,
  `15.00 c.p.s.` marker, and metabolic-water containment were restored from
  high-resolution scan evidence and independently re-reviewed.
- n7 demonstrated that clearly legible cover subtitles, map headings, and map
  scales must be retained even when smaller surrounding legends remain
  unreadable.
- n13 demonstrated that biological hierarchy must remain exact
  (`chordates`, therefore vertebrates, not chordates equated with vertebrates)
  and that unique legible cover text remains source content.
- n14 demonstrated that unexplained source markers and small but legible
  bibliographic dimensions must be retained rather than silently normalized
  away.
- n16-n17 demonstrated that visible source typos or unusual wording must not
  be mislabeled as OCR errors. Any intended-sense normalization remains
  explicit in the uncertainty notes.
- n18 demonstrated that capitalized conceptual terms such as `the All` and
  `the Person` require recoverable source-language anchors.
- n19 demonstrated that legible headings inside a reproduced instruction sheet
  remain source content even when its smaller body text cannot be recovered.
- n20 demonstrated that grouped figure numbers do not justify invented
  per-figure captions; only the source prose's explicit figure references may
  be interpreted.
- n21 demonstrated that stylized display lettering requires dedicated crops:
  visually plausible readings such as `ROLL`, `DOG WILL KNOW`, and `WARMTH
  DOWN THERE?` were rejected after high-resolution review.
- n23 demonstrated that adjacent technical diagrams must remain separate:
  plumbing sizes, rammed-earth dimensions, and floor-layer labels cannot be
  reassigned from construction convention.
- n22 demonstrated that conflicting price statements in editorial prose and
  order blocks must both be retained and explained rather than silently
  reconciled; uncaptioned adjacent drawings do not license invented captions.
- n24 demonstrated that technical tables require cell-by-cell preservation of
  printed constants, while small but legible material and gauge labels such as
  `No. 10 wire tie` must not be generalized away.
- n25 demonstrated that dense catalog lists require source-order and
  missing-price fidelity, while construction drawings must distinguish
  single and paired members and state a cutting table's verified subdivision
  pattern without inventing unreadable cells.
- n27 demonstrated that interleaved OCR must be separated by visible entry
  ownership, while a legible nail schedule must be restored exactly and a
  nearby corner detail must not inherit an overlap principle from another
  drawing.
- n28 demonstrated that handwritten construction figures require
  character-level regression: seating labels, pole-order suffixes, material
  widths, cord lengths, and the product text's normalization were all checked
  against dedicated high-resolution crops before acceptance.
- n26 demonstrated that a future-design wish list must not be presented as
  orderable inventory, and that engineering labels must retain their
  dimensional relationships rather than only collecting isolated numerals.
- n29 demonstrated that clearly legible map scales, edge coordinates, and
  photograph scale captions remain required even when nearby marginal text is
  too degraded to recover; the durable seven-section schema is also part of
  acceptance.
- n32 demonstrated that a likely historical source typo must be preserved and
  explicitly noted rather than silently corrected, while product test counts
  must not be expanded from a total into a per-measure claim.
- n30 demonstrated that visual regression must distinguish two injured feet
  from two injuries, and that even small but legible contour values belong in
  a map's retained numeric evidence.
- n31 demonstrated that visible subsection headings and figure signatures are
  retained content, while visual descriptions not printed as prose must stay
  out of the reader translation.
- n33 demonstrated that editorial idiom must not acquire unsupported permission
  or usability claims, and that ordering-code punctuation such as a leading
  asterisk is evidence rather than decoration.
- n35 demonstrated that an uncertain historical plant common name should be
  preserved rather than normalized to an unsupported species, and that a
  separate legible cover caption remains required.
- n36 demonstrated that a dense reproduced newspaper contents list requires
  title-by-title and page-number regression; a single dropped digit prevents
  acceptance even when the long excerpts and record boundaries are sound.
- n54 demonstrated that an original page-count contradiction must remain
  visible, while dense engineering tables may retain only the labels, row
  sequence, and footnotes that survive high-resolution inspection rather than
  guessed microtype values.
- n56 demonstrated that relative historical dates require the issue's 1968
  reading frame, and that stable figure numbers remain part of a technical
  illustration even when its smallest internal arrows cannot be recovered.
- n58 demonstrated that many scattered excerpts can belong to one catalog
  record: numbered knots, figure captions, action labels, and book-order blocks
  must be reassembled by visible ownership before a neighboring book begins.
- n60 demonstrated that a prose summary cannot replace a numbered technical
  sequence: stable step boundaries, component labels, extension lengths, and
  subsidiary figure captions remain required source content.
- n59 demonstrated that small handwritten values remain required even when the
  page does not explain their function; retaining the marks without inventing
  an interpretation is more faithful than silently dropping them.
- n62 demonstrated that stable cover subtitles and institutional names remain
  source content, and that a completed high-resolution gate must be reflected
  consistently in OCR notes and self-critique rather than left as future work.
- n63 demonstrated that a plausible extra qualifier can still change a
  theoretical definition, while stable cover endorsements and edition text
  must be transcribed separately from genuinely unreadable attribution microtype.
- n61 demonstrated that visibly contaminated binary data should not be
  presented as an exact bitstream: preserve the verified symbol count, signal
  classes, decoding conditions, and figure semantics until a cleaner source exists.
- n64 demonstrated that a stable printed figure number overrides OCR and
  prompt assumptions, while repeated poem numbering and historical currency
  must remain as printed rather than normalized for convenience.
- n66 demonstrated that title and author variants printed on the same page
  must remain visible even when they resemble errors, and that stable source
  letters inside mathematical diagrams cannot be replaced by a generic summary.
- n67 demonstrated that a compact diagram summary is insufficient when every
  binary row is legible; exact states, empty-set code, source-language examples,
  and process-step boundaries all remain part of the translated evidence.
- n65 demonstrated that a single catalog record may continue physically across
  the gutter while neighboring records begin on the next leaf; only visibly
  continuous bibliography tails may cross that boundary, with losses explicit.
- n68 demonstrated that three dense technical records can share one page while
  retaining separate logic diagrams, calculator specifications, shipping weight,
  machine weight, and a visibly truncated source caption.
- n70 demonstrated that audit language belongs in uncertainty notes, not the
  reader translation; the final text should describe visible diagrams neutrally
  while preserving illegible labels as explicit review evidence elsewhere.
- n69 demonstrated that tiny anatomy keys require character-level checking:
  a single source abbreviation can change both the named body part and its
  Chinese translation even when every surrounding diagram is correct.
- n71 demonstrated that visible figure labels take precedence over a mistaken
  source caption, while the caption conflict and a visibly truncated sentence
  remain explicit evidence rather than being silently repaired.
- n73 demonstrated that equipment reviews, contributor lists, record catalog
  numbers, and adjacent model specifications must remain distinct even when
  the page presents them as one continuous electronic-music spread.
- n74 demonstrated that a readable curriculum matrix must be transcribed
  item by item: plausible summaries can invent modes, erase chord modifiers,
  and alter musical actions even when surrounding prose and prices are sound.
- n75 demonstrated that compressed catalog notation can encode quantity and
  length in the same token, while conflicting prose and caption prices must
  remain separate; both issues require specification-level regression review.
- n76 demonstrated that a political forecast's denominator must remain exact:
  fewer than half able to vote is stronger than half unable to vote, even when
  both sound similar in a dense historical quotation.
- n77 demonstrated that an embedded bibliography remains source content even
  when it is not a set of editorial recommendations; compressed historical
  fields must be preserved rather than silently normalized from external data.
- n78 demonstrated that stable printer credits and specimen text remain part
  of the source even when they sit below a quotation or function mainly as a
  visual typography example.
- n79 demonstrated that repeated diagram labels must remain attached to their
  individual figures: grouping them by function can hide misspellings,
  singular-plural differences, and figure-specific population data.
- n80 demonstrated that a single stable initial in an otherwise unreadable
  caption still belongs in the translation, especially when the uncertainty
  notes already record that character as verified.
- n81 demonstrated that sequential diagrams must preserve the transformation
  between panels, not merely describe each image's broad shape; possessive
  words in dialogue remain source content even when the phrase is colloquial.
- n82 demonstrated that stable bylines, continuation notes, and addresses in a
  newspaper thumbnail remain required, while a poem's action verb and a meal's
  single time point cannot be replaced by plausible static paraphrase.
- n83 demonstrated that uncaptioned photographs do not authorize reader-layer
  scene descriptions; nested quotation layers, source cover spacing, and a
  single middle initial all remain character-level evidence.
- n84 demonstrated that a source sentence printed once must not be duplicated
  as both prose and caption, and that uncaptioned photographs belong in the
  evidence notes rather than invented reader-layer scene descriptions.
- n85 demonstrated that medically distinct terms such as illusion and
  hallucination cannot be collapsed, while every independent diagram label
  must remain explicit and workflow qualifiers must stay outside the reader layer.
- n86 demonstrated that an intentionally blank source-table cell is itself
  reader-visible evidence and must not disappear or be algorithmically inferred;
  stable cover edition and credential text must also survive image handling.
- n87 demonstrated that a source count contradiction must be preserved rather
  than silently repaired, while excerpt connectors, per-item quantities, and
  stable cover organization text remain required evidence.
- n88 demonstrated that dense mail-order tables require row-by-row validation,
  but surrounding advertising claims and mechanical component terms still need
  sentence-level review rather than numeric verification alone.
- n89 demonstrated that cover text must be identified as cover text rather than
  an interior heading, and that an uncaptioned demonstration photo cannot create
  reader-layer prose when the adjacent source sentence already carries the method.
- n90 demonstrated that missing source step numbers and unresolved table-header
  asterisks must remain visible rather than reconstructed, even when the adjacent
  recipe or specification sequence appears inferable.
- n91 demonstrated that high-density directories require both mechanical entry
  counts and source-column order checks; familiar personal names, truncated school
  names, and suspect historical addresses must not be externally normalized.
- n92 demonstrated that non-Latin samples require character-level scan review,
  including punctuation and omitted function words; nearby location wording and
  seemingly minor quantity intensifiers can also invent unsupported evidence.
- n94 demonstrated that government directories require full index, program-table,
  price, and office-address counts, while genuinely unstable serial numbers and
  address prefixes must remain explicitly unresolved rather than guessed.
- n95 demonstrated that adverbial emotional force and literary profanity are
  fidelity-bearing content; a fluent paraphrase cannot silently flatten either
  intensity while claiming to preserve the source voice.
- n93 demonstrated that an editorial shorthand title must remain distinct from
  a formal book title, and that every directly readable cover title belongs in
  the reader layer without surrounding evidence-acquisition language.
- n97 demonstrated that anatomically distinct pack-frame components cannot share
  one generic strap label, and that a folded length and diameter must retain their
  separate dimensional roles rather than form a false two-dimensional size.
- n96 demonstrated that unusual historical word forms require the same source-first
  treatment as scientific names, while stable diagram step letters and dimensions
  remain translatable evidence even when the surrounding lines are not inferred.
- n98 demonstrated that material compounds such as canvas duck must not be split
  into duplicate nouns, and that adjective scope can distinguish whole-shoe lining
  from localized padding even inside compact catalog prose.
- n99 demonstrated that catalog material terms, rotated book descriptions, and
  slang evaluations each require contextual translation; literal word substitution
  can turn alloy into gold, free eating into fire-making, and satire into nonsense.
- n100 demonstrated that source-blank table cells must remain blank and Markdown
  structure must be validated separately from cell content; one extra separator
  can misalign a numerically perfect table in the reader.
- n101 demonstrated that absence is evidence at character and table levels: no
  degree sign and no printed row number may be supplied, while a real cross-page
  title conflict must remain documented without overriding the current leaf.
- n102 demonstrated that figure numbers, diagram sublabels, and long numbered
  free-publication lists must be verified independently from prose; a correct
  record count does not substitute for exact labels and ordering.
- n103 demonstrated that a numerically and structurally correct 42-row table can
  coexist with small but required diagram labels; independent review must check
  both dense tables and isolated abbreviations rather than treating either as a proxy.
- n104 demonstrated that domain motion terms such as aircraft hunt cannot be
  translated as ordinary verbs, and that summary counts must reconcile all nine
  addresses and three paid amounts rather than drift across workflow sections.
- n107 demonstrated that a crude idiom can carry both grammar and a product joke:
  the translated sentence must keep the person as its object, while a source
  variant such as `qui vivre` must remain traceable even when translated by its
  intended standard idiom.
- n105 demonstrated that diagram labels require literal visual support even when
  domain knowledge makes a guessed label plausible; regression removed two
  unsupported alignments, restored two printed labels, and preserved `HEX` exactly.
- n106 demonstrated that a visually clear summary value must override a plausible
  OCR or model-memory value: regression restored the NSU Ro 80's printed
  `111.8 mph / 180 km/h` while retaining two genuinely unreadable price endings.
- n109 demonstrated that dense product pages require stock-number counts and
  fractional dimensions to be checked separately; even the physically unusual
  printed `3½ × ⅝ in.` must be preserved when high-resolution evidence is clear.
- n110 demonstrated that a dense bibliography needs independent mechanical counts
  for author works, other education entries, and psychology entries, while source
  anomalies and handwritten years remain visible rather than silently normalized.
- n111 demonstrated that a horizontal rule can determine record ownership more
  reliably than semantic proximity, and that readable child handwriting must be
  transcribed fully while only the source's genuinely unfinished ending stays open.
- n112 demonstrated that experimental student language cannot be resolved from OCR
  confidence alone: 600 dpi letterform evidence restored `finely`, while the rotated
  extract required both halves of `questing-questioning` to remain in translation.
- n114 demonstrated that large mixed reference pages need separate count contracts
  for lists, summaries, films, and every table cell; exact source spelling still
  matters after all 220 numerical table cells have passed.
- n113 demonstrated that typographic student work is itself source text: a literal
  run of punctuation cannot be replaced by an editorial placeholder, and repeated
  word counts require character-level regression beside dense price-list review.
- n115 demonstrated that conspicuous address anomalies must be preserved and
  explained rather than silently normalized, while occupational humor depends on
  distinguishing a school custodian from an administrator.
- n116 demonstrated that a large plan needs label-by-label spatial review alongside
  mechanical counts for paired prose lists, while genuinely unstable figure microtext
  must not be reconstructed from a plausible mathematical pattern.
- n117 demonstrated that a source-language teaching sample still needs a Chinese
  semantic layer for a complete translation; preserving its distinctive orthography
  and translating its meaning are complementary rather than competing requirements.
- n119 demonstrated that dense numbered vocabulary diagrams need independent
  continuity checks as well as character-level review of unusual source spellings;
  plausible normalization can erase evidence even when all numbers are present.
- n118 demonstrated that physical collage occlusion does not erase every fragment:
  numbered left edges and unnumbered right edges must both be retained in page order,
  without forcing disconnected remnants back into invented catalog rows.
- n120 demonstrated that repeated fractional dimensions require direct glyph-level
  review across both prose and uncertainty notes, while technical time labels need
  domain-appropriate Chinese rather than an everyday homograph.
- n121 demonstrated that supplemental same-program evidence may restore eroded
  wording and day sequence but cannot establish the Catalog's column placement;
  blank schedule days and record-specific bylines must remain un-inferred.
- n122 demonstrated that historical names and paradoxical prose both require
  character- and logic-level review: a plausible modern spelling or fluent-looking
  sentence can still alter the source's evidence and comparison structure.
- n123 demonstrated that rotated bibliographies need line-count and empty-field
  checks, while even a supplier's apparently misspelled name must remain as printed
  and be explained rather than silently standardized.
- n124 demonstrated that a procedural program needs step-by-step continuity checks
  alongside medical-warning and source-spelling review; a clean long translation is
  accepted only after every numbered action and bibliographic anchor survives.
- n125 demonstrated that quoted pronouns can carry intentional personification and
  that comparative syntax must preserve who experiences interest; both can be lost
  even when every numbered exercise and bibliographic field is present.
- n126 demonstrated that ordinary-looking comparative phrases still require exact
  semantic review, while uncertainty about a date belongs in notes rather than as
  audit narration inside the reader translation.
- n127 demonstrated that advertising policy, rate tables, and supplier copy remain
  source content, while dark photographic overprint must stop at verified fragments
  rather than being reconstructed from background knowledge.
- n128 demonstrated that financial charts require arithmetic reconciliation, while
  handwritten plots and route maps must not be converted into invented exact values.
- n129 demonstrated that duplicated reader forms are two source objects rather than
  one reusable template; every price, start period, blank line, and zip field remains
  part of the translation record.
- n131 demonstrated that a form's rotation and table geometry are primary evidence:
  ten blank rows and split price cells remain content, while cropped headers must be
  reconstructed only with explicit disclosure.
- n132 demonstrated that a closing institutional profile must keep photo captions,
  cover-source credits, organization prose, and the detachable request form separate;
  cross-column OCR noise is not reader content.
- n37 demonstrated that OCR-corrupted equipment specifications require
  independent value-by-value review, while attributed user testimonials must
  remain distinct from the Catalog's own product claims.
- n38 demonstrated that a table's stated weekly production and its adjacent
  daily footnotes must both be preserved without reconciliation, while
  handwritten construction geometry requires region-specific visual review.
- n40 demonstrated that a dense materials page requires value-by-value review
  of engineering test data and strict ownership of supplier, price, dimension,
  and product-label details across adjacent records.
- n42 demonstrated that technical diagrams require their stable printed labels,
  not plausible labels inferred from geometry; regression restored the solar
  still, bird-flight forces, feather structure, and trout-motion stages.
- n39 demonstrated that a full technical-report excerpt can preserve its
  classification tree and dimensioned sections while still isolating genuinely
  unreadable photograph microcopy and anomalous source notation as residual risk.
- n41 demonstrated that a process diagram cannot be reduced to a prose summary:
  stable branch labels, specialized hinge and turbine terms, figure titles, and
  formula units all require explicit high-resolution regression.
- n43 demonstrated that clipping adjacency does not establish article or figure
  ownership: complete clipped sentences must be restored, while an isolated
  `P/h` diagram remains explicitly unassigned rather than attached by proximity.
- n44 demonstrated the same boundary rule at a harder scale: a genuinely
  truncated Volita clipping must not absorb an adjacent subscription address,
  while stable schematic labels, casting dimensions, and lyric fragments remain
  translatable even when surrounding microcopy is degraded.
- n46 demonstrated that neighboring historical-machine figures must keep their
  own diagrams: the horizontal windmill's wind-cycle labels cannot migrate to
  the sailing wheelbarrow, and visible source spelling, era marks, directions,
  and unexplained letter labels must be preserved without normalization.
- n47 demonstrated that small scientific tables still require cell-by-cell
  verification: paired axis scales, numbered rows, unnumbered cross-references,
  and nested subheadings cannot be inferred from sequence or collapsed into a
  generic summary.
- n48 demonstrated that physical adjacency can invite a semantic misread even
  without OCR error: a solar-path diagram beside an auditory passage remains a
  solar-path diagram, and a numbered beam figure requires its printed component
  labels rather than a generalized structural summary.
- n45 demonstrated that a dense reprint catalog requires item-level regression:
  all 86 visible codes can be present while a single page number and singular
  noun remain wrong; rotated captions and technical abstracts require separate
  orientation-aware checks.
- n49 demonstrated that stable cover metadata remains part of a catalog record:
  a future-edition date must be restored even when the neighboring telephone
  digits remain legitimately unreadable at high resolution.
- n50 demonstrated that advertising addresses require the same evidentiary
  discipline as product data: a clear Brooklyn address must not be discarded,
  and an unsupported Chicago location must not replace a printed Pennsylvania
  address.
- n52 demonstrated that a dense tool table needs character-level review across
  stock codes, dimensions, descriptions, and page references, while a later
  handwritten price remains a preserved annotation rather than catalog price.
- n51 demonstrated that source contradictions must survive alongside corrected
  values: the printed hydraulic heading's `3-WAY and 6-WAY` remains visible even
  though the body and model table specify 3-way and 4-way equipment.
- n53 demonstrated that task examples are not source authority: canonical leaf
  mapping and the actual four bordered records overrode an adjacent-page tool
  list before any content could be silently imported.
- n55 demonstrated that handwritten prices can remain source evidence when
  clearly legible, while unlabeled tool photographs remain non-textual and must
  not acquire invented product names.
- n57 demonstrated that an exploded-view diagram requires exact printed labels,
  including source singulars and distinct generic braces, rather than a modernized
  or consolidated component vocabulary.
