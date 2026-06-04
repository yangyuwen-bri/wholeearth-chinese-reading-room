# Whole Earth Chinese Reading Room

Local research workspace for exploring `wholeearth.info` / Internet Archive scans and turning Whole Earth publications into readable Chinese guides.

This project is not a full-text translation archive. The product goal is to help Chinese readers understand what each Whole Earth issue is about, why it matters, and where to enter the original scans. The editorial standard is: do not rely on titles or index guesses alone; use OCR, page-level evidence, and scan links.

## Current Editorial Status

### Completed Reading Drafts

The only issue currently treated as a complete Chinese reading draft is:

- `Whole Earth Software Catalog 2.0, Fall 1985`
  - full guide: `outputs/wholeearth_full_readings/wholeearthsoftwa00unse_3_full_chinese_reading.md`
  - chapter coverage: 17/17 chapters
  - format: Chinese reading guide, not full-text translation
  - QA status: passed chapter coverage / duplicate-paragraph / overclaim checks

The same issue also has a deeper page-level sample for the Programming section:

- `outputs/wholeearth_page_reading_samples/wholeearthsoftwa00unse_3_programming_pages_158_174.md`
  - covers the Programming section around printed pages 158-174
  - includes leaf/page mapping and scan links
  - used as the quality benchmark for future issue-level reading work

### Data Layer Completed, Not Yet Editorially Complete

- 147 issues have local page-level dossiers.
- Total local page count: 22,162 pages.
- Coverage QA result: 147/147 dossiers present, 0 missing, 0 empty, 0 invalid JSON.
- These dossiers are evidence infrastructure, not finished understanding. They should not be presented as completed Chinese reading notes.

### Prototype Only

`outputs/wholeearth_fun_archive/` is a static site prototype generated from earlier evidence summaries. It is useful as a navigation and design experiment, but its issue pages should not be treated as final editorial content. Many issue summaries still need real reading work.

## Structure

- `work/`: extraction and site-generation scripts.
- `outputs/wholeearth_evidence_dossiers/`: issue-level OCR evidence dossiers.
- `outputs/wholeearth_full_readings/`: finished Chinese reading drafts.
- `outputs/wholeearth_page_reading_samples/`: page-level reading samples.
- `outputs/wholeearth_fun_archive/`: generated static site prototype.
- `outputs/whole_earth_software_catalog_1985_architecture.*`: section architecture for the 1985 Software Catalog.
- `outputs/wholeearth_all_issues_guides.json`: 147-issue index metadata used by scripts and prototypes.

Large regenerated page OCR/XML caches are intentionally ignored:

- `work/wholeearth/`
- `outputs/wholeearth_page_dossiers/`

They remain available locally on this machine, but they are not tracked in Git because they are large and reproducible from Internet Archive sources.

## Git Scope

Tracked:

- extraction and generation scripts
- issue-level evidence dossiers
- the 1985 complete Chinese reading draft
- the 1985 Programming page-level sample
- static site prototypes and supporting small assets

Ignored:

- page-level OCR/XML caches
- full page-level dossier JSON/Markdown output
- runtime logs
- QA screenshots and design trials

## Key Scripts

- `work/extract_wholeearth_evidence.py`: builds issue-level OCR evidence dossiers.
- `work/extract_issue_pages.py`: builds page-level dossier for one Internet Archive identifier.
- `work/extract_all_issue_pages.py`: builds page-level dossiers for all 147 issues.
- `work/build_wholeearth_fun_archive.py`: builds the current static archive prototype.

## Important Caveat

Earlier issue notes under `outputs/wholeearth_understanding_notes/` are explicitly marked as initial OCR-based judgments, not page-level readings. They should not be used as finished public-facing copy.

## Suggested Next Step

Continue issue by issue. For each issue:

1. Read from the page-level dossier and scan links.
2. Write a Chinese guide in `outputs/wholeearth_full_readings/`.
3. Run a small QA check for chapter coverage, repeated template language, and overclaims.
4. Only then promote the issue into the product UI as editorially complete.
