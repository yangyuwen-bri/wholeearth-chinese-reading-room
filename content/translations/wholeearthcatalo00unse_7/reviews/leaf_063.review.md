# Leaf 063 Independent Review

## Conclusion

needs_highres_scan

## Reasons

- 旧稿把 John Brockman 的“人死了”和电影段落误归进《Technicians of the Sacred》选文，并遗漏 Brockman 书评、普世技术段、更多诗歌和 `Garbage Event`。
- 本次直接读取完整 DjVu page object，已分离两本书和独立事件，并恢复连续可辨内容、书目、价格和地址。
- w2000 扫描当前不可访问；诗行、族群标签、装置图、页码和跨栏顺序仍未扫描确认。
- 因此本次改进是完整 OCR 重建，不构成 `needs_highres_scan` 闭环。

## Required Fixes

- 源站恢复后，用 n63 w2000 扫描逐项核验诗文署名、族群名称、引号、断行和出处标记。
- 确认 Brockman 与 `Garbage Event` 的版面边界、图像归属、书目信息和页码。
- 对 XML 中交错的 Bantu、Ojibwa、Egypt、Gabon Pygmy、Easter Island、Borneo-Dayak 等标签逐条归位；只补入扫描可证实的诗句。

## Residual Risks

- 选文断行、来源标记和装置图说明会影响作品层级，不能仅靠 OCR 定稿。
