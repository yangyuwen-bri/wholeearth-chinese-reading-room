# Whole Earth Chinese Translation Workflow

Version: v1

This document defines the repeatable workflow for turning one Whole Earth issue
into a faithful Chinese reading-room package.

The workflow is issue-based. Each magazine issue gets its own translation
package under `content/translations/<issue_id>/`. Branches are temporary task
lanes; the translation package is the long-term source of truth.

## Success Criteria

An issue is ready for reader integration only when:

- every in-scope leaf has a translation file, review file, and status record;
- substantive source text is translated from OCR plus scan checks, not from an
  existing Chinese summary;
- unresolved OCR, layout, or scan problems are visible in status files;
- glossary decisions for recurring titles, people, terms, and institutions are
  recorded;
- reader-facing text contains only final translation and guide material, not
  translator notes, self-critique, QA labels, or workflow metadata;
- the generated reader data can be rebuilt from the translation package.

## Repository Roles

- `main`: public, stable baseline.
- `gh-pages`: published static output.
- `content/translations/<issue_id>/`: long-term translation package for one
  issue.
- `data/issue_agents/<issue_id>/`: page, OCR, retrieval, and link data used by
  agents and build scripts.
- `reader-prototype/`: reading-room build and UI surface.
- `codex/<issue-id>-<task>`: temporary branch for a specific batch, fix, or
  integration task.

Do not keep one permanent branch per magazine. Use one long-lived translation
package per magazine and short branches for individual work batches.

## Issue Package Layout

Each issue should follow this layout:

```text
content/translations/<issue_id>/
  README.md
  translation_standard.md
  glossary.md
  status.jsonl
  qa_report.md
  agent_kickoff.md
  prompts/
    translator_v1.md
    reviewer_v1.md
    anchor_auditor_v1.md
  leaves/
    leaf_000.md
  reviews/
    leaf_000.review.md
  tools/
```

Use `content/translations/_template/` as the starting point for new issues.

## Versioning and Lessons

This workflow is expected to improve as new issues expose new source problems.
Treat it as a versioned operating procedure, not a fixed rulebook.

Use these rules when the loop changes:

- issue-local discoveries go first into
  `content/translations/<issue_id>/workflow_lessons.md`;
- issue-specific exceptions stay in that issue's `README.md` or
  `translation_standard.md`;
- reusable lessons can be promoted back into `docs/translation_workflow.md` and
  `content/translations/_template/`;
- prompt changes must be versioned, for example `translator_v1.md`,
  `translator_v1_1.md`, or `translator_v2.md`;
- do not silently rewrite old prompts after a batch has used them;
- record why a workflow change was made and which leaves exposed the problem.

Examples of issues that should create a lesson:

- OCR is broadly good, but a few scan-heavy leaves are blank or misleading;
- source-language examples should remain in the source language;
- recurring page-description prose leaks into the final Chinese;
- a layout type, such as foldout, table, catalog grid, or image caption, needs a
  new review rule;
- link matching or anchor auditing produces repeated false positives.

## Agent Roles

Use separate agents or separate passes for these roles:

- `source-provenance`: verifies leaf range, printed page, OCR source, scan URLs,
  and known OCR problems.
- `translator`: produces faithful Chinese translation from the source pack.
- `reviewer`: checks coverage, mistranslation, summary drift, OCR guessing, and
  terminology consistency.
- `anchor-auditor`: verifies entry-level leaf anchors against scan/OCR evidence.
- `link-auditor`: matches books, tools, organizations, and named references to
  stable external or internal links.
- `reader-integrator`: converts accepted translation output into reader JSON and
  UI data.

For small issues, one Codex session can run the roles sequentially. For large
issues, use separate agents for translation and review, but keep all outputs in
the same issue package.

## Translation Loop

Each leaf or entry goes through this loop:

1. `source_pack`: record issue ID, leaf, printed page, scan URL, OCR source, and
   risk flags.
2. `context_pass`: identify page structure, entries, people, books, captions,
   diagrams, and layout risks.
3. `glossary_pass`: record names, titles, recurring terms, and provisional
   decisions.
4. `draft_translation`: translate substantive content faithfully.
5. `self_critique`: identify omissions, summary drift, OCR uncertainty, tone
   drift, and guessed terms.
6. `faithful_revision`: revise before review; self-critique must not appear in
   reader-facing text.
7. `independent_review`: compare against OCR and scan, then assign a status.
8. `human_accept`: only accepted or explicitly allowed output enters reader
   integration.

## Statuses

- `pending`: not started.
- `source_ready`: OCR and scan references are available.
- `drafted`: initial translation exists.
- `self_checked`: translator completed self-critique and revision.
- `reviewed_needs_glossary`: otherwise viable, but major terminology or title
  decisions remain unstable.
- `needs_highres_scan`: image text, diagram labels, small captions, or
  low-contrast text need high-resolution human scan review.
- `revise`: substantive translation issue found.
- `blocked_ocr`: source text cannot be recovered reliably from current OCR and
  scan material.
- `accepted`: reviewed and ready for reader integration.
- `no_translation_needed`: blank, cover, index, order, or non-substantive
  material only.

Do not mark a leaf `accepted` to hide uncertainty. A small number of unresolved
items is better than false confidence.

## Reader-Facing Rules

Reader-facing output may include:

- final Chinese translation;
- issue or chapter guide summaries;
- hidden source table-of-contents foldouts;
- links to original scan pages and confirmed book/tool references.

Reader-facing output must not include:

- "Final Translation", "Self Critique", "OCR Notes", or similar workflow
  section labels;
- page-description prose such as "the right column introduces...";
- instructions about what should or should not be translated;
- leaf headings like `leaf 001` as body content;
- unreviewed OCR fragments unless explicitly marked as unresolved.

## Source Priority

Use this priority order:

1. Archive scan image as final authority for visible content.
2. Official Internet Archive DjVu XML OCR as primary machine text source.
3. Supplemental OCR only for official blank, broken, or unusable OCR.
4. Existing Chinese reader text only as navigation context or a warning example.

High-risk leaves must be checked against high-resolution scan images, normally:

```text
https://archive.org/download/<issue_id>/page/n<leaf>_w2000.jpg
```

## Branch and Session Pattern

For a new issue:

1. Start from current `main` unless intentionally testing workflow changes.
2. Create or refresh source data on a short branch:
   `codex/<issue-id>-source-bootstrap`.
3. Create the issue package from `_template`.
4. Start a dedicated Codex session for that issue and paste the issue's
   `agent_kickoff.md`.
5. Run translation in batches, usually 10-30 leaves per batch depending on OCR
   complexity.
6. Commit each reviewed batch on a task branch.
7. Rebuild issue-agent data and reader data only after accepted translations are
   present.
8. Merge to `main` only after build checks and spot-reading pass.

## Batch Gate

Before merging any batch:

- status counts are updated;
- `workflow_lessons.md` is updated if the batch exposed a reusable problem;
- no reader-facing file contains workflow labels or self-critique;
- representative leaves have been checked against scans;
- `needs_highres_scan`, `revise`, and `blocked_ocr` are explicit;
- generated JSON validates;
- changed files belong to the issue task.

## First-Hour Checklist for a New Issue Session

The dedicated issue session should do this before translating:

1. Confirm current branch and create a short issue branch.
2. Locate the issue record in `data/issue_index.json`.
3. Confirm Archive identifier, leaf range, PDF, cover, and available OCR files.
4. Copy `content/translations/_template/` to
   `content/translations/<issue_id>/`.
5. Fill in metadata in the issue `README.md`.
6. Generate or sketch `status.jsonl` for the full leaf range.
7. Inspect 3-5 representative scans, including cover, dense catalog page,
   image-heavy page, and back matter.
8. Record issue-specific risks in `workflow_lessons.md`.
9. Propose the first batch and verification checks.
10. Wait for explicit approval before a large batch run if source quality is
    uncertain.
