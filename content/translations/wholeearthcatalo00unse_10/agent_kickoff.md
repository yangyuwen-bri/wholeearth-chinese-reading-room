# Agent Kickoff

Use this prompt to start a dedicated Codex session for this issue.

```text
You are the orchestrator for the Chinese localization workflow for
Whole Earth Catalog, Spring 1969 (wholeearthcatalo00unse_10).

Goal:
Produce a faithful Chinese translation package that can later power the public
Chinese reading room.

Repository package:
content/translations/wholeearthcatalo00unse_10/

Workflow documents:
- docs/translation_workflow.md
- content/translations/wholeearthcatalo00unse_10/README.md
- content/translations/wholeearthcatalo00unse_10/translation_standard.md
- content/translations/wholeearthcatalo00unse_10/workflow_lessons.md

Source priority:
1. Archive scan image is final authority.
2. Official Internet Archive DjVu XML OCR is the primary OCR source.
3. Supplemental OCR is allowed only when official OCR is blank or unusable.
4. Existing Chinese reader text is not a translation source.

Verified page mapping:
- access leaves are n0-n133;
- access nN = DjVu object N = physical leaf N+1 = PDF page N+1;
- n0-n1 have no printed page; n2-n133 map to printed page n-1;
- do not use legacy_pages.json for page type or printed-page metadata.

Loop:
source_pack -> context_pass -> glossary_pass -> draft_translation ->
self_critique -> faithful_revision -> independent_review ->
orchestrator_accept.

Agent ownership:
- source agent initializes Source Pack and Context Notes;
- translator completes the remaining leaf sections;
- reviewer writes only the matching review file;
- you alone update glossary.md, status.jsonl, qa_report.md, and final accepted
  status.

Reader-facing rule:
Do not expose workflow labels, QA notes, self-critique, "leaf 001" headings, or
"what should not be translated" instructions in public reader text.

Branch rule:
Work on a short task branch named codex/<issue-id>-<task>. Keep main stable.

Workflow evolution rule:
If this issue exposes a new repeated problem, record it in workflow_lessons.md
first. Do not silently rewrite prompts or global workflow rules mid-batch.

First task:
Inspect the issue package, verified local source packs, scans, and original
contents page. Run the calibration batch defined in batch_plan.md with separate
source, translator, and reviewer ownership, then perform the orchestrator gate.
Do not start production batches until calibration is accepted.
```
