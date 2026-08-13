# Leaf 091 Independent Review

## Conclusion

needs_highres_scan

## Reasons

- 旧译文是断行 OCR 的逐行机翻，存在乱码、错词和大量未译完的主题与书目；现已依据本地官方 DjVu XML 重建为完整中文预备稿。
- 当前无法连接 w2000 扫描，尚未确认页面分栏、印刷页码、复选框、封面文字归属和字符级书目信息。
- OCR 对免费的双周清单《Selected U. S. Government Publications》和 6 美元《Monthly Catalog》的句序发生交错；预备稿按语法恢复，但必须用扫描判定。
- 因此本次改进不构成 `needs_highres_scan` 闭环，也不应标为 `revise` 或 `accepted`。

## Required Fixes

- 源站恢复后，用 n91 w2000 扫描确认印刷页码及“书评—GPO 说明—主题清单—书目例项—封面”版面顺序。
- 核对全部主题编号、出版物代码、年份、价格、批量价格和 `Carper Buckley` 姓名行。
- 确认双周清单与月度目录句序，以及 `O.P.` 等孤立缩写属于哪个条目。
- 检查两幅复制封面的可读文字，删除任何由 OCR 串入错误条目的内容。

## Residual Risks

- 当前译文内容覆盖基于完整官方 OCR，而非扫描；图像文字和跨栏边界仍可能存在遗漏或误归属。
- 小号出版物代码中 `1/I`、`0/O`、连字符和标点最容易发生字符级错误。
