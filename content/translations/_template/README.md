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
- `agent_kickoff.md`: text to paste into a new Codex session.

## Operating Rule

The package is the durable memory for this issue. Branches and Codex sessions
are temporary execution lanes.

When a batch exposes a new recurring problem, record it in
`workflow_lessons.md` before changing prompts or promoting the lesson back to
the global template.
