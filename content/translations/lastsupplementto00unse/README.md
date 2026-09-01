# 《最后一期〈全球概览〉增刊》中文翻译包

## Goal

Produce a faithful, readable Chinese translation of *The Last Supplement to
The Whole Earth Catalog* (March 1971) that can power the public Chinese reading
room.

The translation base is the English source: Archive scans plus official OCR.
Existing Chinese summaries, older guide text, or generated reader prose must
not be used as the translation source.

## Issue Metadata

- Issue ID: `lastsupplementto00unse`
- Issue title: *The Last Supplement to The Whole Earth Catalog, March 1971*
- Archive URL: https://archive.org/details/lastsupplementto00unse
- Leaf range: access leaves `000-131` (132 leaves)
- Printed page rule: access leaves `002-131` correspond to printed pages
  `1-130`; leaves `000-001` are the front cover and title page.
- Source OCR path:
  `ai-https-wholeearth-info/_local/legacy/work/wholeearth/page_xml/lastsupplementto00unse_djvu.xml`
- Scandata path:
  `ai-https-wholeearth-info/_local/legacy/work/wholeearth/page_xml/lastsupplementto00unse_scandata.xml`
- Issue-agent data path: `data/issue_agents/lastsupplementto00unse/`

## Work Products

- `leaves/leaf_###.md`: production translation per leaf.
- `reviews/leaf_###.review.md`: fidelity review per leaf.
- `status.jsonl`: one record per leaf.
- `glossary.md`: title, name, term, and institution decisions.
- `qa_report.md`: status counts and blockers.
- `workflow_lessons.md`: issue-specific workflow findings and reusable lessons.
- `prompts/`: agent prompts used for this issue.
- `examples/`: canonical leaf and review shapes.
- `agent_kickoff.md`: text to paste into a new Codex session.

## Content Boundary

Translate all legible visible content, including repeated prices, stock
numbers, postage, supplier and publisher lines, order addresses, indexes,
captions, tables, labels, and bibliographic details. Do not omit, compress,
group, or summarize them in reader-facing text.

If OCR and high-resolution scans cannot recover a visible element, record its
exact boundary in `OCR / Uncertainty Notes` and the review evidence and keep
the leaf out of `accepted`. `Omitted Bibliographic/Order Info` must say `None`
for accepted leaves unless the source material is proven physically absent or
irrecoverable after high-resolution review.

Do not merge distinct source entries into one overview. Use multiple `###`
headings inside `Final Translation` when a leaf contains multiple entries.

`no_translation_needed` still requires a leaf file and review. Translate any
visible heading, instruction, caption, quotation, or other non-index text.

## Agent Ownership

- Source agent: `Source Pack` and `Context Notes` for assigned leaves.
- Translator: remaining sections in assigned leaf files.
- Reviewer: matching files under `reviews/` only.
- Orchestrator: `glossary.md`, `status.jsonl`, `qa_report.md`, final acceptance,
  and workflow promotion decisions.

One leaf has one writer at a time. Agents propose shared-state changes in their
own output; they do not edit shared files concurrently.

## Operating Rule

The package is the durable memory for this issue. Branches and Codex sessions
are temporary execution lanes.

When a batch exposes a new recurring problem, record it in
`workflow_lessons.md` before changing prompts or promoting the lesson back to
the global template.
