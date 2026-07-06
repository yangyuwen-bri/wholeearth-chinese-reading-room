# AGENTS.md

## Scope

This file applies to `/Users/yuwen/work/wholeearth/ai-https-wholeearth-info-xiaohei` on branch `codex/xiaohei-visual-prototype`.

This worktree is for illustrated booklet and visual-reading experiments for the Whole Earth / 全球概览 project. It is the output workspace for reader-facing visual interpretation, booklet assembly, illustration-system experiments, and social-post visual adaptations.

The source Chinese reading content is not maintained in this worktree. Treat `/Users/yuwen/work/wholeearth/ai-https-wholeearth-info/content/readings/` as the upstream source directory for complete Chinese issue texts. Read from it as needed, but do not edit it unless the user explicitly asks.

Do not hard-code one issue, year, book, visual character, or topic as the identity of the whole project. Each booklet may focus on a different issue, year, publication type, theme, or chapter group.

This worktree is not the main reading-room, archive-map, OCR-memory, or data-pipeline project.

## Worktree Safety

Work only inside this worktree unless the user explicitly asks otherwise.

Before broad edits, check the current path and branch.

Keep prototype assets, generated images, HTML booklets, and social-post experiments isolated here. Do not damage or rewrite `main`.

When syncing or deriving from another Whole Earth worktree, copy or reference only the folders and files needed for the current booklet or visual system. Typical scoped folders may include:

- `content/visuals/`
- `assets/<booklet-or-issue-visuals>/`
- `skills/<visual-system-name>/`

Do not run broad directory copies over iCloud-backed, dataless, or partially hydrated folders without inspecting file state first.

## Required Orientation

Before booklet or illustration work, read:

- `README.md`
- `content/visuals/siamese_cat_visual_identity.md`
- the relevant source file under `/Users/yuwen/work/wholeearth/ai-https-wholeearth-info/content/readings/`
- the relevant local visual skill, such as `skills/siamese-cat-knowledge-illustrations/SKILL.md`, when using a recurring character or illustration system

For every new booklet, record the upstream source file in the planning or booklet Markdown.

## Reader-Facing vs Internal Notes

Strictly separate reader-facing copy from internal evaluation.

Reader-facing pages must not contain planning or selection language such as:

- "强候选"
- "候选模块"
- "适合做这种图"
- "这个比上一版好"
- "面向我展示"
- "不是全文替代"
- "不是装饰画集"

Those belong in planning notes, not in the public booklet or post.

If a sentence explains why a chapter was selected, rewrite it as a reader benefit or remove it.

The reader should feel they are entering the material, not reading production notes.

## Content Method

Do not batch-generate final pages from titles alone.

For each section:

1. Read the upstream Chinese text, OCR/source notes, page dossier, or issue notes.
2. Identify the actual idea worth visualizing.
3. Decide whether illustration helps the reader understand the idea.
4. Write a section-specific visual concept.
5. Generate or compose the page.
6. Verify the rendered result.

The booklet is not decoration. Each image should clarify a concept, tension, workflow, historical judgment, or reading clue from the source material.

If a section does not benefit from illustration, do not force it into the booklet.

## Series Positioning

Public copy should frame the work as part of the Whole Earth / 全球概览 series localization and interpretation.

The correct frame is:

- The creator is reading, translating, developing, and interpreting the Whole Earth / 全球概览 series.
- Each booklet or post shares something valuable found in that process.
- The current issue or theme is one source case, not the identity of the whole project.

Do not promise future output as generic tool rankings, productivity tips, AI trend commentary, or listicles unless the user explicitly asks for that direction.

A contemporary hook is allowed only when it grows naturally from the source material.

## Visual Identity

A recurring character or visual guide can help the series feel coherent, but the character is not the topic.

Do not over-emphasize the character in titles or descriptions unless the task is specifically about the character system.

Keep character consistency:

- stable body shape and face design
- stable personality
- repeatable silhouette
- recognizable color and marking system
- props and scenes change per section
- labels and metaphors are regenerated per source material

Do not reuse a finished image concept as a template for unrelated content.

Reuse the visual identity. Regenerate the content metaphor.

## Booklet Writing

Public-facing booklet copy should sound like an editorial guide for readers.

Avoid:

- AI summary voice
- generic "knowledge visualization" language
- internal selection notes
- production-process explanation
- "not X, but Y" positioning
- overexplaining what the booklet is not
- titles that make the visual character more important than the content

Prefer:

- direct reader invitations
- concrete situations from the source
- clear chapter or section framing
- short captions that help the image do work
- present-day relevance only when it is genuinely supported by the material

## Social Post Writing

For Xiaohongshu or public posts, the series voice should be:

- personal reading discovery
- grounded in Whole Earth / 全球概览 source material
- specific rather than trend-chasing
- connected to today only when the connection is real
- not a generic content account

Use `stop-slop` or `humanizer` when available and when the task is copywriting. Prefer `stop-slop` for short social posts and `humanizer` for longer explanatory drafts.

Before finalizing social copy, check for:

- template contrast phrases
- fake quotable lines
- vague "本质上 / 关键是 / 不是 X 而是 Y" language
- claims that promise the wrong series direction
- over-neat lists that sound generated

## Visual QA

After editing HTML or visual pages, render screenshots or exported PNGs when the page relies on layout, images, or relative assets.

Pure Markdown planning notes do not require rendered QA, but they should still be checked for source paths, internal-note labels, and reader-facing/internal separation.

For HTML or visual pages, check:

- text does not overflow
- no UI or content overlap
- images load
- page numbers and captions are readable
- reader-facing copy contains no internal notes
- issue/theme identity is correct
- final page does not make the wrong series promise

For local preview, use a temporary local HTTP server when relative assets require it. Stop preview servers before finishing.

## Source Grounding

Do not answer or create from titles alone.

Ground each booklet section in actual source material:

- upstream Chinese issue texts
- translated drafts
- OCR text
- page dossiers
- issue notes
- scan references
- prior reading guides

If the source is incomplete or OCR quality is poor, preserve that uncertainty in internal notes. Do not expose raw uncertainty in reader-facing copy unless it is relevant to the reader's understanding.

## File Organization

Keep artifacts organized by booklet, issue, theme, or visual system.

Typical locations:

- `content/visuals/` for booklet HTML, Markdown, and planning notes
- `assets/<booklet-or-visual-system>/` for generated or curated images
- `outputs/` for rendered exports and QA screenshots
- `skills/<visual-system-name>/` for reusable character or illustration rules

Do not mix one booklet's assets into another booklet's visual folder unless deliberately building a shared visual system.

## Git Hygiene

Do not stage or commit unless the user asks.

Generated experiments can remain untracked during exploration.

Keep booklet, atlas/map, OCR-memory, reading-room, and social-post work mentally separate. Do not merge prototype assets into production surfaces without explicit direction.

Before reporting completion, say what was changed, what was verified, and what was not touched.
