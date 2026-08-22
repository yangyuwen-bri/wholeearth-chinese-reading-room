# Issue Translation Package Template

Copy this folder to:

```text
content/translations/<issue_id>/
```

Then replace placeholders such as `<issue_id>`, `<issue_title>`, and
`<leaf_range>`.

## Goal

Produce a faithful, readable Chinese translation of `<issue_title>` that can
power the public Chinese reading room.

The translation base is the English source: Archive scans plus official OCR.
Existing Chinese summaries, older guide text, or generated reader prose must
not be used as the translation source.

## Issue Metadata

- Issue ID: `<issue_id>`
- Issue title: `<issue_title>`
- Archive URL: `<archive_url>`
- Leaf range: `<leaf_range>`
- Printed page rule: `<printed_page_rule>`
- Source OCR path: `<source_ocr_path>`
- Issue-agent data path: `data/issue_agents/<issue_id>/`

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
