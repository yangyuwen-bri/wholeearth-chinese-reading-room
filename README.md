# Whole Earth Chinese Reading Room

Local research workspace for exploring `wholeearth.info` / Internet Archive scans and turning Whole Earth publications into Chinese reading guides.

## Structure

- `work/`: extraction and site-generation scripts.
- `outputs/wholeearth_evidence_dossiers/`: issue-level OCR evidence dossiers.
- `outputs/wholeearth_full_readings/`: finished Chinese reading drafts.
- `outputs/wholeearth_page_reading_samples/`: page-level reading samples.
- `outputs/wholeearth_fun_archive/`: generated static site prototype.

Large regenerated page OCR/XML caches are intentionally ignored:

- `work/wholeearth/page_xml/`
- `outputs/wholeearth_page_dossiers/`

## Current State

- 147 issues have page-level dossiers locally, totaling 22,162 pages, but those large dossiers are not tracked in Git.
- `Whole Earth Software Catalog 2.0, Fall 1985` has a full Chinese reading draft in `outputs/wholeearth_full_readings/`.
- The existing all-issue website is a prototype and should not be treated as final editorial quality until each issue gets real reading notes.

