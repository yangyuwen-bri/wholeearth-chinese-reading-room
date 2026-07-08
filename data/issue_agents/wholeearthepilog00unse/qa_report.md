# Whole Earth Epilog Issue Agent Bundle - QA Report

- issue_id: `wholeearthepilog00unse`
- schema_version: `issue-agent-bundle-v1`
- pages: 322
- leaf range: 0-321
- missing leaves: [322]
- duplicate leaves: none
- chapter records: 121
- bibliography records: 216
- retrieval units: 659
- retrieval unit counts: {'bibliography': 216, 'chapter': 121, 'page': 322}
- bibliography status counts: {'confirmed': 140, 'not_linked_ambiguous_title': 13, 'not_linked_candidate_mismatch': 26, 'not_linked_no_reliable_match': 8, 'not_linked_source_not_located': 29}
- page QA flags: {'cover_or_back_matter': 6, 'layout_risk': 216, 'ocr_risk': 142, 'scan_required': 218, 'short_text_or_image_page': 4}
- scan URL format issues: none

## Source Boundary

- `pages.jsonl` combines local OCR, scan URL evidence, and the page-level Chinese evidence workbench.
- `chapters.jsonl` comes from the reader-facing chapter translation draft.
- `bibliography.jsonl` comes from the audited bibliography/link JSON.
- Runtime chat transcripts, model outputs, vector caches, and embeddings are intentionally excluded from this tracked bundle.

## Agent Use

The chat agent should retrieve from `retrieval_units.jsonl`, then cite the underlying source record and scan leaf. For exact original wording, especially on OCR-risk pages, the answer must ask the reader to verify against the scan URL.
