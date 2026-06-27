# Siamese Cat Knowledge Illustrations

Use this skill to turn one page-level knowledge anchor from the Whole Earth reading project into a consistent editorial illustration led by the project's own Siamese cat character.

## When To Use

- The task asks for a knowledge-point illustration, visual reading anchor, or illustrated explanation for a Whole Earth page, module, or concept.
- The source material has a concrete page, scan, OCR passage, or reading note.
- The output should explain one idea, not summarize an entire issue.

Do not use this skill when the task needs a dashboard, generic archive cover image, decorative mascot art, or a full-magazine summary illustration.

## Evidence Boundary

Before generating an illustration, identify:

1. Issue or module title.
2. Page or leaf number.
3. Scan URL or local scan path.
4. One-sentence knowledge anchor.
5. Three to five source-grounded concepts that may appear as short labels.

The illustration may simplify the idea, but it must not invent a claim that cannot be traced back to the selected page or module.

## Character Model

The recurring character is a semi-simplified Siamese cat reading-room editor.

Required visual traits:

- Cream body.
- Seal-point face mask, ears, paws, and tail.
- Two clear muted-blue almond eyes.
- Slim upright body.
- Simple white work apron with two tiny pencil pockets.
- Long dark tail with one calm curve.

Consistency rules:

- Preserve visual charm: use elegant editorial linework and selective hatching, not flat mascot shapes.
- Use a repeatable silhouette: slender upright body, triangular ears, almond eyes, tapered torso, dark paws, one long curved tail.
- Keep fur texture controlled: enough linework to feel crafted, but no wildlife realism or painterly fur.
- The face mask should be one clear dark shape, not many patches.
- Eyes should be the only saturated color accent on the character.
- The cat should act like an editor: pointing, sorting cards, pinning notes, drawing relation lines, or operating a small reading machine.
- Keep the head, eye shape, apron, tail curve, and mitten paws stable across images; vary only the cat's hand action and the surrounding knowledge metaphor.
- Prefer one half-body or three-quarter-body pose at a reading table. Avoid full-body action poses unless the page concept requires motion.

Avoid:

- Children's-book cuteness.
- Flat childish mascot rendering.
- Photorealistic animal anatomy.
- Overly furry or painterly rendering.
- Random costumes, hats, glasses, bowties, or props that change the identity.
- Copying Ian Xiaohei's black character silhouette or body language.

## What Is Fixed

Only the character identity and illustration temperament are fixed:

- Siamese cat editor identity.
- Seal-point face mask, blue almond eyes, apron, dark paws, and long curved tail.
- Adult editorial ink style with warm paper, controlled hatching, and archive-blue accents.
- Evidence-minded actions such as sorting, pointing, drawing lines, marking pages, and operating small explanatory devices.

The knowledge content is never fixed. Do not reuse Micro-Prolog machinery, labels, outputs, or page text unless the selected source page is actually about Micro-Prolog.

## What Changes Per Topic

For each new page or module, replace:

- The issue/module/page citation.
- The one-sentence knowledge anchor.
- The visual metaphor.
- All Chinese labels.
- Any diagrams, machines, tables, cards, tools, or outputs.

The cat may stay recognizable while the surrounding knowledge object changes completely.

## Illustration Style

- Format: 16:9.
- Background: warm white paper.
- Linework: black or very dark brown ink, with selective hatching.
- Accent colors: warm tan, muted archive blue, small seal-brown fills.
- Composition: one central metaphor plus a few marginal notes.
- Text: 4 to 6 short Chinese labels. No long paragraphs inside the image.
- Mood: precise, archival, lightly witty, never promotional.

## Prompt Template

Use this structure for image generation:

```text
Create a 16:9 editorial knowledge illustration on a warm-white paper background.

Recurring character: a semi-simplified Siamese cat reading-room editor, cream body,
single dark seal-point face mask, dark triangular ears, dark mitten paws, long
dark curved tail, two muted-blue almond eyes, slim upright body, simple white
work apron with two tiny pencil pockets. Elegant editorial linework, controlled
selective hatching, repeatable silhouette, restrained warm tan and muted
archive-blue accents. Preserve charm without becoming cute or photorealistic.

Topic: [issue/module/page].
Knowledge anchor: [one sentence].

Visual metaphor: [one central machine/table/map/workbench metaphor].
Show the cat [one editor-like action].

Include only these short Chinese labels: [label list].

Style constraints: archival editorial diagram, hand-drawn but simplified,
consistent mascot design, not cute, not photorealistic, not painterly, no
flat childish mascot style, no gradients, no 3D, no dashboard UI, no extra long
text, no unrelated props.
```

## Prompt Notes

- Put the evidence citation outside the generated image when possible. Inside the image, use a short page marker such as `p.167`, not a full source note.
- Do not ask the image model to render precise body text. Use labels as visual anchors only.
- If the first result is too realistic, repeat: `semi-simplified editorial character, controlled hatching, repeatable silhouette`.
- If the first result is too cute, repeat: `archival editor, precise reading-note tone, no children's-book style`.
- If the first result is too flat or plain, repeat: `restore elegant ink detail, adult editorial charm, not a flat mascot`.

## Consistency Checklist

Before accepting the image:

- The cat is recognizable as the same simplified Siamese character.
- The face mask, ears, paws, tail, apron, and blue eyes are present.
- The character is an explanatory editor, not a decorative pet.
- The page idea can be understood without long in-image text.
- The image still needs the scan/page note around it; it does not replace evidence.

## Reference Assets

- Page: `Whole Earth Software Catalog 2.0, Fall 1985`, Programming / Micro-Prolog, p.167.
- Best knowledge-illustration direction: `/assets/wholeearth_1985_visuals/siamese-cat-micro-prolog-editorial-v3.png`
- Character consistency reference: `/assets/wholeearth_1985_visuals/siamese-cat-character-sheet-v1.png`
- Rejected over-simplified direction: `/assets/wholeearth_1985_visuals/siamese-cat-micro-prolog-skill-v2.png`
- Use `siamese-cat-character-sheet-v1.png` as the character reference.
- Use `siamese-cat-micro-prolog-editorial-v3.png` only as a style-quality reference, not as a content template.
- Result: use the semi-simplified editorial linework direction. The v2 attempt improved control but lost charm; future prompts should not over-flatten the character or carry Micro-Prolog content into unrelated pages.
