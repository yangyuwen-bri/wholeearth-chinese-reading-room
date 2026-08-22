# Whole Earth Catalog, Spring 1969 Translation Workflow

This package is the durable production record for the complete Chinese
translation of the second Whole Earth Catalog.

## Goal

Produce a faithful, readable Chinese translation of `Whole Earth Catalog,
Spring 1969` that can power its public Chinese reading room.

The translation base is the English source: Archive scans plus official OCR.
Existing Chinese summaries, older guide text, or generated reader prose must
not be used as the translation source.

## Issue Metadata

- Issue ID: `wholeearthcatalo00unse_10`
- Issue title: `Whole Earth Catalog, Spring 1969`
- Archive URL: `https://archive.org/details/wholeearthcatalo00unse_10`
- Leaf range: `access leaves n0-n133` (134 leaves)
- Access mapping: `access nN = DjVu object N = physical leaf N+1 = PDF page N+1`
- Printed page rule: `n0-n1 have no printed page; n2-n133 map to printed page n-1`
- Source OCR path: repository-root
  `_local/page_xml/wholeearthcatalo00unse_10_djvu.xml`
- Scan metadata path: repository-root
  `_local/page_xml/wholeearthcatalo00unse_10_scandata.xml`
- Local high-resolution scan: package
  `_local/scans/wholeearthcatalo00unse_10.pdf`
- Verified leaf source packs: package `_local/source_packs/`

The legacy generated dossier under repository-root `_local/page_dossiers/` is
not authoritative for page type or printed-page metadata. It paired public
access leaf `nN` with physical leaf `N`, causing a one-leaf offset. Use the
verified package source packs instead.

The contents page names Portola Institute on p.129, while the scan sequence
includes a two-sided foldout/order insert at n130-n131 and scandata continues
its leaf-level numbering through p.132. Record both the printed/scandata anchor
and the contents-page reference when translating this back-matter sequence;
do not silently force them to agree.

## Work Products

- `leaves/leaf_###.md`: production translation per leaf.
- `reviews/leaf_###.review.md`: fidelity review per leaf.
- `status.jsonl`: one record per leaf.
- `glossary.md`: title, name, term, and institution decisions.
- `qa_report.md`: status counts and blockers.
- `batch_plan.md`: durable production queue and session handoff overview.
- `workflow_lessons.md`: issue-specific workflow findings and reusable lessons.
- `prompts/`: agent prompts used for this issue.
- `examples/`: canonical leaf and review shapes.
- `tools/build_source_materials.py`: repeatable source-pack builder and mapping
  verifier.
- `agent_kickoff.md`: text to paste into a new Codex session.

## Content Boundary

Translate all substantive visible content. Repeated price, stock, postage, and
supplier/address lines may be omitted or compressed only when they do not
carry editorial, historical, navigational, or practical meaning. Record every
such omission in `Omitted Bibliographic/Order Info`.

Do not merge distinct source entries into one overview. Use multiple `###`
headings inside `Final Translation` when a leaf contains multiple entries.

`no_translation_needed` still requires a leaf file and review. Translate any
visible heading, instruction, caption, quotation, or other non-index text.

## Agent Ownership

- Source agent: `Source Pack` and `Context Notes` for assigned leaves.
- Translator: remaining sections in assigned leaf files.
- Reviewer: matching files under `reviews/` only.
- Orchestrator: `glossary.md`, `status.jsonl`, `qa_report.md`, final acceptance,
  and workflow promotion decisions.

One leaf has one writer at a time. Agents propose shared-state changes in their
own output; they do not edit shared files concurrently.

## Acceptance Gate

A leaf is accepted only when:

1. access/physical/PDF/printed-page anchors follow the verified mapping;
2. every substantive visible entry has been translated rather than summarized;
3. a different agent has completed the fidelity review;
4. dense layouts, diagrams, tiny captions, rotated matter, and weak OCR have
   been checked against the high-resolution scan;
5. review outcome, `status.jsonl`, and `qa_report.md` agree.

## Operating Rule

The package is the durable memory for this issue. Branches and Codex sessions
are temporary execution lanes.

When a batch exposes a new recurring problem, record it in
`workflow_lessons.md` before changing prompts or promoting the lesson back to
the global template.
