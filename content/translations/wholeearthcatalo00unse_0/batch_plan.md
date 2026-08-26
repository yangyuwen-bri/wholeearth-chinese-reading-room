# Fall 1970 Translation Batch Plan

All leaves use the strict `translator_v1_2` → self-check → `reviewer_v1_2` →
orchestrator gate. A leaf is accepted only after high-resolution scan review
confirms every visible source element is represented in Chinese.

## Calibration Batch

- `n0`–`n5`: cover, copyright/function statement, credits and ordering,
  two-page contents/index, and the first Whole Systems page.
- Section/layout probes: `n19`, `n43`, `n63`, `n83`, `n103`, `n121`.
- Back-matter probes: `n144`–`n147`.

Verification: reconstruct page reading order from the scan; inventory all
titles, bylines, prose blocks, quotations, captions, diagrams, prices, stock
numbers, addresses, page references, and labels; compare the Chinese body to
that inventory before review.

## Production Batches

1. `n6`–`n18`: Whole Systems
2. `n20`–`n42`: Shelter and Land Use
3. `n44`–`n62`: Community
4. `n64`–`n82`: Communications
5. `n84`–`n102`: Industry and Craft
6. `n104`–`n120`: Nomadics
7. `n122`–`n143`: Learning

## Release Gate

- Exactly 148 leaf translations and 148 independent reviews.
- `status.jsonl`: `accepted=148`; all other statuses `0`.
- `tools/validate_release.py` passes with no coverage, omission, duplicate
  review, or summary-drift findings.
- Reader build and content audit pass before merge and publication.
