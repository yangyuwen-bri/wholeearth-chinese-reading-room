# Production Batch Plan

This file is the handoff queue for later Codex sessions. The canonical per-leaf
state remains `status.jsonl`.

## Calibration Gate

Production batches opened after all calibration leaves completed the full
source, translation, independent-review, scan-check, and orchestrator loop.

| Batch | Leaves | Risk represented | State |
| --- | --- | --- | --- |
| calibration | n0, n1, n2, n3, n11, n34, n72, n108, n130, n133 | cover; title/purpose; multi-column contents; catalog procedure; dense ordinary prose; price table; diagram/cross-column reading; blank OCR; rotated back matter; back cover | accepted |

Calibration acceptance requires:

- all ten leaf files and all ten independent review files;
- verified access, physical, PDF, and printed-page anchors;
- no unresolved entry-boundary, price association, table, diagram, or rotated
  text problems;
- review outcomes, `status.jsonl`, and `qa_report.md` in agreement;
- glossary decisions recorded before production expansion.

## Production Queue

Batches do not cross original issue sections and generally target 2,500–3,500
official OCR words. Smaller batches are retained where a single dense leaf,
section edge, or calibration leaf makes a larger grouping unsafe. Leaves
already accepted during calibration are skipped when they fall inside a range.

| Section | Batches | State |
| --- | --- | --- |
| Understanding Whole Systems | n4; n5–6; n7–10; n11–12; n13; n14–15; n16–17; n18 | complete; n4–18 accepted |
| Shelter and Land Use | n19–22; n23–24; n25–27; n28–29; n30–31; n32–33; n34–35; n36–37; n38–39; n40 | complete; n19–40 accepted |
| Industry and Craft | n41–43; n44–45; n46–48; n49–50; n51–52; n53–54; n55–57; n58–60 | complete; n41–60 accepted |
| Communications | n61–62; n63–64; n65–67; n68–70; n71–72; n73–74; n75–76; n77–78 | complete; n61–78 accepted |
| Community | n79–80; n81–82; n83–85; n86; n87; n88; n89–90; n91–92; n93–94 | complete; n79–94 accepted |
| Nomadics | n95; n96–97; n98–99; n100–102; n103–104; n105; n106–108 | complete; n95–108 accepted |
| Learning | n109–111; n112; n113; n114–115; n116–117; n118; n119; n120–121; n122–123; n124; n125–126 | complete; n109–126 accepted |
| Back Matter | n127–133 | complete; n127–133 accepted |
