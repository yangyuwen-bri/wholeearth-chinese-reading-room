# Agent Kickoff

Use this prompt to continue the dedicated Spring 1970 issue workflow.

```text
You are the orchestrator for the Chinese localization workflow for
Whole Earth Catalog, Spring 1970 (`wholeearthcatalo00unse_1`).

Goal:
Produce a faithful Chinese translation package that can later power the public
Chinese reading room.

Repository package:
content/translations/wholeearthcatalo00unse_1/

Workflow documents:
- docs/translation_workflow.md
- content/translations/wholeearthcatalo00unse_1/README.md
- content/translations/wholeearthcatalo00unse_1/translation_standard.md
- content/translations/wholeearthcatalo00unse_1/workflow_lessons.md

Active production prompts:
- content/translations/wholeearthcatalo00unse_1/prompts/translator_v1_2.md
- content/translations/wholeearthcatalo00unse_1/prompts/reviewer_v1_2.md

Source priority:
1. Archive scan image is final authority.
2. Official Internet Archive DjVu XML OCR is the primary OCR source.
3. Supplemental OCR is allowed only when official OCR is blank or unusable.
4. Existing Chinese reader text is not a translation source.

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
Translate every legible visible source element in full. Repetition, prices,
stock numbers, addresses, and index data may not be omitted or summarized.

Branch rule:
Work on a short task branch named codex/<issue-id>-<task>. Keep main stable.

Workflow evolution rule:
If this issue exposes a new repeated problem, record it in workflow_lessons.md
first. Do not silently rewrite prompts or global workflow rules mid-batch.

First task:
Inspect the issue package, source OCR, scans, and
data/issue_agents/wholeearthcatalo00unse_1/.
Then complete the first-hour checklist from docs/translation_workflow.md and
propose a calibration batch with clear verification checks. Run separate source,
translator, and reviewer agents, then perform the orchestrator gate yourself.
```
