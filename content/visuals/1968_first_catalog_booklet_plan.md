# 1968 First Catalog Booklet Plan

## Source

- Issue: `Whole Earth Catalog, Fall 1968`
- Issue id: `wholeearthcatalo00unse_8`
- Translation source:
  `/Users/yuwen/work/wholeearth/worktrees/1968-first-catalog/content/translations/wholeearthcatalo00unse_8/`
- Leaf source:
  `/Users/yuwen/work/wholeearth/worktrees/1968-first-catalog/content/translations/wholeearthcatalo00unse_8/leaves/leaf_*.md`
- QA state: 68 accepted leaves, no remaining translation blockers, per upstream `qa_report.md`.

This xiaohei worktree is only the booklet and visual-reading workspace. Do not edit the upstream translation package unless explicitly asked.

## Editorial Position

The 1968 first catalog should be developed chapter by chapter, following the issue's own sections and leaf order. Do not start from Xiaohongshu-style themes or cherry-picked contemporary hooks.

The booklet should preserve the same visual language as the existing 1974 Epilog Siamese-cat booklet series:

- warm paper editorial HTML page
- 16:9 Siamese cat knowledge illustrations
- black/brown ink linework, selective hatching, warm tan and archive-blue accents
- reader-facing Chinese guide copy beside each image
- module rhythm from the 1974 `*_final_booklet.html` pages

The 1968 first catalog still has its own character: it is the first version of an access system, where readers learn how to find, buy, make, repair, test, and judge things. That identity should emerge inside the chapter sequence, not replace it.

## Chapter Development Order

### 00. Front Matter / Catalog Procedure

- Leaves: `leaf_001`, `leaf_003`
- Anchors:
  - access and evaluation
  - easy mail-order availability
  - suppliers cannot buy placement
  - reader feedback changes the catalog
- Visual job: show the catalog as a practical routing desk, not a book cover.

### 01. Understanding Whole Systems

- Leaves: `leaf_004` to `leaf_013`
- Anchors:
  - Fuller and whole-systems thinking
  - Full Earth poster and NASA Earth photographs
  - form, growth, systems, cybernetics, future studies
- Visual job: make abstract systems legible through concrete diagrams, Earth images, body/computer metaphors, and reading-table relations.

### 02. Shelter And Land Use

- Leaves: `leaf_014` to `leaf_022`
- Anchors:
  - dome and structure tools
  - Audel repair/building guides
  - VITA village technology
  - tipi living and lamp choice
  - organic gardening, five-person garden table, bees
- Visual job: convert dense entries into living scenes and workflows.

### 03. Industry And Craft

- Leaves: `leaf_023` to `leaf_032`
- Anchors:
  - how things work
  - human-scale design
  - Thomas Register as industrial yellow pages
  - tools, solar energy, bookmaking, leather, yarn, beads
- Visual job: show the jump from consumer to maker.

### 04. Communications

- Leaves: `leaf_033` to `leaf_041`
- Anchors:
  - calculators, cybernetics, radio catalogs, Heathkit
  - film and television production
  - auto repair manuals
  - book-finding and art-print access
- Visual job: show media production as a skill stack, not only machines.

### 05. Community

- Leaves: `leaf_042` to `leaf_045`
- Anchors:
  - intentional community routines
  - SEALAB cramped-space behavior
  - Merck Manual as household/communal medical reference
  - Consumer Reports, land catalogs, government publications, shopping guides
- Visual job: make institutions legible through concrete domestic and purchasing scenes.

### 06. Nomadics

- Leaves: `leaf_046` to `leaf_052`
- Anchors:
  - survival and camping books
  - lightweight camping equipment patterns
  - REI, L.L. Bean, Gerry, boots, hot springs, Sierra Club
- Visual job: keep safety boundaries clear; emphasize gear, maps, packing, and reading practices.

### 07. Learning

- Leaves: `leaf_053` to `leaf_062`
- Anchors:
  - inquiry boxes
  - Cuisenaire rods and initial teaching alphabet
  - science experiments with ordinary materials
  - WFF games, Dr. Nim, children building computers
  - self-study, meditation, yoga, I Ching
- Visual job: show learning as hands-on props and repeated practice.

### 08. Back Matter

- Leaves: `leaf_063` to `leaf_067`
- Anchors:
  - ads, subscription, index, Portola Institute, back cover
- Visual job: make the publication system, subscription loop, index, and Portola context visible without over-expanding minor back matter.

## Build Sequence

Create a chapter index first:

`content/visuals/1968_first_catalog_siamese_booklet_index.html`

Then build chapter booklets in order:

1. `1968_first_catalog_front_matter_final_booklet.html`
2. `1968_first_catalog_whole_systems_final_booklet.html`
3. `1968_first_catalog_shelter_land_use_final_booklet.html`
4. `1968_first_catalog_industry_craft_final_booklet.html`
5. `1968_first_catalog_communications_final_booklet.html`
6. `1968_first_catalog_community_final_booklet.html`
7. `1968_first_catalog_nomadics_final_booklet.html`
8. `1968_first_catalog_learning_final_booklet.html`
9. `1968_first_catalog_back_matter_final_booklet.html`

Each chapter can contain multiple modules. A chapter is not limited to one image, and a dense leaf can yield more than one visual module when the source supports it.

## Visual Rules

- Use the recurring Siamese cat editor only as a guide, not as the topic.
- Do not put the cat in the same right-side pose on every spread.
- Let each chapter and module have its own visual object: routing desk, Earth-photo table, dome section, repair bench, media console, community table, packing map, play table.
- Short Chinese labels in images only; longer explanations belong in HTML copy.
- Avoid template layouts. Alternate image/copy proportions and page rhythm.
- Source evidence remains outside the reader-facing copy unless useful as leaf/page markers.

## QA Checklist

- Every spread cites the leaf cluster in internal comments or planning notes.
- Public copy contains no planning words such as "候选", "强候选", "不是全文替代", or "从完整中文章稿改写".
- No unsupported contemporary advice, especially medical, electrical, chemical, weapons, or survival procedures.
- Chinese should read naturally, with no stiff translated phrasing.
- Render desktop and mobile screenshots before reporting a finished HTML booklet.
