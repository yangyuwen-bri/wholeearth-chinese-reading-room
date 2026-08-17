# QA Report

## Release State

Release suspended on 2026-08-15 after a reader-reported summary-substitution
failure on `leaf_007`.

- Translation files: 132/132.
- Review files: 132/132.
- The previous `accepted=132` claim is withdrawn.
- Current orchestrator states: `accepted=45` (`leaf_000`–`leaf_044` rebuilt or
  scan-audited and independently re-reviewed), `self_checked=87` pending
  scan-level coverage review.
- The Fall 1969 release builder is intentionally blocked until every accepted
  review contains concrete source-to-translation coverage evidence.

## Confirmed Failure

The old `leaf_007` reader text reduced three catalog entries to descriptions.
For `Star Maker`, it omitted the editorial recommendation and most visible
literary excerpts, then presented a synthesized Chinese paraphrase as a
blockquote. Its generic review incorrectly said that no introduction-style
compression was present.

The page was rebuilt from the n7 w2000 scan and complete official DjVu page
object. All substantive reviews and excerpts are now translated, permitted
address omissions are recorded, and the visible printed page is corrected to
p.6.

## Systemic Audit

The new release gate checks:

- concrete `Coverage Evidence` in every review;
- source inventory, translation mapping and permitted omissions;
- suspicious OCR-word-to-Chinese-character compression;
- page-description, meta-review and summary language in reader text;
- contradiction between an `accepted` conclusion and non-empty required fixes;
- duplicate generic review reasons;
- final orchestrator status.

The first run correctly blocked the release with 322 findings; after closing
`leaf_000`–`leaf_013`, the original gate still blocked with 286 findings. After
strengthening the language and review-consistency checks and closing through
`leaf_044`, the current gate blocks with 236 findings. These counts mix
status/evidence failures with content-risk signals; neither is a count of bad
pages. A conservative compression screen identified 39 high-risk leaves;
all 132 leaves nevertheless remain in the coverage-review scope.

## Required Closure

1. Inventory every substantive block against the scan and complete OCR.
2. Retranslate every omitted review, argument, excerpt, caption or meaningful
   label; do not substitute themes or encyclopedia descriptions.
3. Replace generic reviews with page-specific coverage evidence.
4. Resolve printed-page mapping against scandata and visible page numbers.
5. Restore `accepted` only leaf by leaf, then regenerate and browser-test the
   reader payload.

## Reader Status

The previously generated JSON is stale and must not be treated as a final
release artifact. Production rebuilding now fails closed until the coverage
gate passes.
