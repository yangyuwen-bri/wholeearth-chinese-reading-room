# Whole Earth Catalog, Fall 1969 Translation Package

Copy this folder to:

```text
content/translations/wholeearthcatalo00unse_7/
```

Then replace placeholders such as `wholeearthcatalo00unse_7`, `Whole Earth Catalog, Fall 1969`, and
`access leaves n0-n131`.

## Goal

Produce a faithful, readable Chinese translation of `Whole Earth Catalog, Fall 1969` that can
power the public Chinese reading room.

The translation base is the English source: Archive scans plus official OCR.
Existing Chinese summaries, older guide text, or generated reader prose must
not be used as the translation source.

## Issue Metadata

- Issue ID: `wholeearthcatalo00unse_7`
- Issue title: `Whole Earth Catalog, Fall 1969`
- Archive URL: `https://archive.org/details/wholeearthcatalo00unse_7`
- Leaf range: `access leaves n0-n131`
- Printed page rule: `provisional: n0-n2 front matter; n3-n131 map to printed page n-2`
- Source OCR path: `_local/page_xml/wholeearthcatalo00unse_7_djvu.xml`
- Issue-agent data path: `data/issue_agents/wholeearthcatalo00unse_7/`

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

Translate all substantive visible content. Repeated price, stock, postage, and
supplier/address lines may be omitted or compressed only when they do not
carry editorial, historical, navigational, or practical meaning. Record every
such omission in `Omitted Bibliographic/Order Info`.

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
