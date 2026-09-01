# Difficult But Possible Supplement, January 1971 — Chinese Translation Package

## Goal

Produce a faithful, readable Chinese translation of *Difficult But Possible
Supplement to the Whole Earth Catalog, January 1971* that can power the public
Chinese reading room.

The translation base is the English source: Archive scans plus official OCR.
Existing Chinese summaries, older guide text, or generated reader prose must
not be used as the translation source.

## Issue Metadata

- Issue ID: `wholeearthcatalo00unse_3`
- Issue title: `Difficult But Possible Supplement to the Whole Earth Catalog,
  January 1971`
- Archive URL: https://archive.org/details/wholeearthcatalo00unse_3
- Public access leaf range: `n0`–`n47` (48 pages)
- Physical scan mapping: access leaves map to physical leaves `1`–`48` after
  excluding physical leaves `0` and `49` (`Color Card`) from access formats.
- Printed page rule: `n0`–`n2` have no printed page number; for `n3`–`n47`,
  printed page = access leaf + 1.
- Official OCR source: `_local/page_xml/wholeearthcatalo00unse_3_djvu.xml`
- Scandata source: `_local/page_xml/wholeearthcatalo00unse_3_scandata.xml`
- Historical source cache: `ai-https-wholeearth-info/_local/legacy/work/wholeearth/page_xml/`
- Issue-agent data path: `data/issue_agents/wholeearthcatalo00unse_3/`

## Work Products

- `leaves/leaf_###.md`: production translation per leaf.
- `reviews/leaf_###.review.md`: fidelity review per leaf.
- `status.jsonl`: one record per leaf.
- `glossary.md`: title, name, term, and institution decisions.
- `qa_report.md`: status counts and blockers.
- `workflow_lessons.md`: issue-specific workflow findings and reusable lessons.
- `prompts/`: prompts used for this issue.
- `examples/`: canonical leaf and review shapes.
- `agent_kickoff.md`: issue handoff instructions.

## Content Boundary

Translate every legible visible element, including the cover's individual
truth/consequence statements, repeated prices, stock numbers, postage,
addresses, corrections, form labels, credits, captions, tables, and index or
distribution data. Do not omit, compress, group, or summarize them in
reader-facing text.

If OCR and high-resolution scans cannot recover a visible element, record its
exact boundary in `OCR / Uncertainty Notes` and the review evidence and keep
the leaf out of `accepted`. `Omitted Bibliographic/Order Info` must say `None`
for accepted leaves unless source material is proven physically absent or
irrecoverable after high-resolution review.

Do not merge distinct letters, notices, quotations, records, or entries into
one overview. Use multiple `###` headings inside `Final Translation` when a
leaf contains multiple source units.

## Ownership and Acceptance

Source preparation, translation, fidelity review, and orchestrator acceptance
remain separate passes. Only the orchestrator updates `glossary.md`,
`status.jsonl`, `qa_report.md`, and the final `accepted` status.

The package is durable issue memory. Branches and sessions are temporary work
lanes. Any recurring source problem is recorded in `workflow_lessons.md`
before it is promoted to the global workflow.
