# Leaf 076 Review

## Conclusion

needs_highres_scan

## Reasons

- The main prose and larger captions were translated using OCR plus the w2000 scan.
- DjVu XML OCR and fifth-review crops were checked for the air-dome, sanitation, and house-inspection diagrams.
- Several small technical diagram labels in the air-dome, building-construction, sanitation, and house-inspection figures remain unresolved.
- The translation marks the unresolved labels instead of silently guessing them.

## Required Fixes

- Create or obtain clearer crops of the lower and right-side diagrams, then translate any remaining legible labels; XML OCR is not usable for these technical labels.
- Re-review after crop-level inspection.

## Residual Risks

- `pages.jsonl` recorded no QA flags for this leaf, but OCR quality is poor; future status tracking should treat this leaf as scan-sensitive.
