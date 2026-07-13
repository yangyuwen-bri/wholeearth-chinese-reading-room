# Leaf 240 Review

## Conclusion

needs_highres_scan

## Reasons

- Checked `https://archive.org/download/wholeearthepilog00unse/page/n240_w2000.jpg`.
- Ran `tools/extract_leaf_xml_ocr.py 240`; DjVu XML OCR only recovers fragments from the underground-comics image area, including `THEY'RE TRYING TO GET / ME BECAUSE | BRING`.
- Ran `tools/crop_ocr_leaf.sh` on the R. Crumb panel and the smaller multi-panel sample. The large panel supports the corrected speech balloon; the smaller sample panels still OCR as noise and cannot be transcribed panel by panel from this source image.
- Main entries for underground comics, Big Yellow Drawing Book, A. I. Friedman Art Supplies, and General Cartography are translated.
- Big Yellow Drawing Book labels and `OTHER RELIEF METHODS` labels visible in w2000 were cleaned up in Final Translation.
- Corrected the recoverable R. Crumb speech balloon in Final Translation: "我就直说吧！事情的事实是，我知道他们想抓我，因为我把真相带给你们！"

## Required Fixes

- Underground-comics small sample panels remain too small for reliable full panel-by-panel transcription after w2000 review and crop OCR. This is a source image-text blocker, not a normal translation omission.

## Residual Risks

- Main prose is usable; unresolved underground-comics sample-panel speech is substantive image text, so `needs_highres_scan` remains appropriate.
