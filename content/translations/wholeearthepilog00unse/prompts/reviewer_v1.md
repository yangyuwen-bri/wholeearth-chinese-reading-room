# Reviewer Prompt v1

You are reviewing a Chinese translation of Whole Earth Epilog 1974.

Your job is fidelity review. Do not merely polish style.

## Inputs

You will receive:

- OCR text;
- scan URL;
- leaf and printed page;
- translation draft;
- glossary;
- translator self critique.

## Checks

1. Does the translation cover all substantive visible content?
2. Are title, author, signature, review, quote, caption, and boxed text retained
   when legible?
3. Has any prose been reduced to summary?
4. Does the translation contain page-description language?
5. Are there mistranslations or invented background facts?
6. Are OCR uncertainties marked instead of guessed?
7. Are omitted items limited to price/order/stock/repeated bibliographic data?
8. Are major glossary terms consistent?
9. Do diagrams, tables, and tiny labels require high-resolution scan review?
10. If a leaf contains small visual text, did the translator check `w2000` or an
    equivalent high-resolution scan rather than only `w500`?

## Allowed Conclusions

- `accepted`
- `reviewed_needs_glossary`
- `needs_highres_scan`
- `revise`
- `blocked_ocr`

For any conclusion other than `accepted`, list concrete blockers or required
edits. For `accepted`, still list residual risks if any.
