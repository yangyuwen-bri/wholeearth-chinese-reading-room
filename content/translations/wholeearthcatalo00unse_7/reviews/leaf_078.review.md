# Leaf 078 Independent Review

## Conclusion

needs_highres_scan

## Reasons

- 旧稿只翻译四个上半页条目，并把模式识别图注误判为页末截断；生成版 Source Pack 实际在 6,000 字符处停止。
- 本次直接读取完整 DjVu page object，补回完整图注及《Data Study》《Colour Guitar》《The Radio Amateur’s Handbook》《Printing as a Hobby》四个主体条目。
- w2000 扫描当前不可访问；《大脑模型》的书目、McBee 街道地址、图中符号下标和多个小号订购字段仍未扫描确认。
- 因此本次改进是完整 OCR 重建，不构成 `needs_highres_scan` 闭环。

## Required Fixes

- 源站恢复后，用 n78 w2000 扫描核对八个主体条目的边界、标题、署名、价格和地址。
- 确认《大脑模型》的书目行、8.50 美元价格与 Oxford University Press 地址，以及 McBee 的完整地址。
- 核对模式识别图中的 A、S、O 等符号下标，并确认 `Data Study` 的作者 J. L. Jolley。

## Residual Risks

- 页面为密集多栏版式，图示、书目和订购块的跨栏归属仍须扫描验证。
