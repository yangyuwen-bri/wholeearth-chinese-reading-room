# QA Report

## Phase

Recovery audit. The inherited package has complete file coverage, but its review
labels are not yet treated as orchestrator acceptance.

## Artifact Inventory

- Translation files: 132/132.
- Review files: 132/132.
- Inherited review conclusions at handoff: `accepted` 103,
  `needs_highres_scan` 29.
- Current working conclusions after three scan recoveries: `accepted` 103,
  `needs_highres_scan` 26, `revise` 3. The three `revise` leaves await
  independent regression rather than self-acceptance.
- Canonical `status.jsonl` retains conservative production states until each
  inherited conclusion is supported by page-specific scan evidence.

## Current Recovery Gate

- `n54`: w2000 scan checked and translation revised; status `self_checked`.
  The old review missed a full right-hand column, so the page requires an
  independent regression review before acceptance.
- `n118`: w2000 scan checked and summary-style text replaced with a
  source-aligned reconstruction, including the 13-day grid, quotations,
  equipment list, order fields, and the visible printed-page conflict. Status
  `self_checked`; independent table regression remains required.
- `n88`: w2000 scan checked and interleaved OCR output replaced with a
  source-aligned reconstruction. Two omitted entries, historical medical text,
  product fields, and image labels were restored. Status `self_checked`;
  independent medical-terminology and column regression remains required.

## OCR Reconstruction Pending Scan

- `n91`: broken machine-translated OCR replaced with a complete structured
  draft from the local official DjVu extraction. Archive.org closed both CLI
  and browser connections during the 2026-08-13 pass, so the conclusion stays
  `needs_highres_scan`; this page is preparation, not closure.
- `n60`: generated dossier truncation had hidden the latter half of the
  `Diagrams` entry. The complete DjVu page object restored its review, figure
  captions, and order block. Conclusion remains `needs_highres_scan` until the
  dense diagram labels can be checked on w2000.
- `n56`: complete DjVu object restored three additional loom sources and two
  yarn entries hidden beyond the generated dossier boundary. Conclusion stays
  `needs_highres_scan` pending diagram, address, and printed-page checks.
- `n66`: complete DjVu object restored three bibliographic blocks, the plane
  Fedorov-group excerpt, an Escher plate caption, and Venn/set explanations.
  Damaged headings and mathematical graphics still require w2000 inspection.
- `n61`: complete DjVu object restored the Kardashev classification and the
  majority of the `Cybernetic Serendipity` entry hidden beyond the generated
  dossier boundary. Scientific exponents, binary graphics, and interleaved
  order fields remain scan-gated.

## Remaining Blockers

- The remaining 26 inherited `needs_highres_scan` leaves require page-specific
  w2000 inspection; a generic review template is not sufficient evidence.
- Inherited `accepted` leaves with duplicated review text or unresolved scan
  notes require re-audit before final orchestrator acceptance.
- Printed-page mapping, glossary promotion, workflow lessons, issue-agent data,
  and reader integration remain incomplete.
