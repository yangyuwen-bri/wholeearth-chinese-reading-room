# Issue Agent Knowledge Bundles

This directory contains structured knowledge bundles for per-issue Whole Earth
reading agents.

Each issue gets one folder named by its Internet Archive identifier:

```text
data/issue_agents/{internet_archive_identifier}/
```

Bundle layers:

- `manifest.json`: bundle entry point, source paths, counts, QA status.
- `issue_profile.json`: issue metadata, section map, source locations.
- `pages.jsonl`: page-level OCR, Chinese page reading, scan evidence.
- `chapters.jsonl`: chapter/topic-level Chinese interpretation chunks.
- `bibliography.jsonl`: audited books, pamphlets, periodicals, and links.
- `retrieval_units.jsonl`: combined RAG retrieval surface.
- `system_prompt.md`: answer policy and source-boundary rules.
- `eval_questions.json`: regression questions for smoke testing the issue agent.
- `qa_report.md`: structural QA summary for the bundle.

Runtime artifacts do not belong here. Embeddings, vector stores, model replies,
and chat transcripts should be generated under `_local/`.
