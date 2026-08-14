# Leaf 100 Independent Review

## Conclusion

needs_highres_scan

## Reasons

- 旧稿是把多栏商品目录逐行交织后的机器直译，只覆盖生成版 Source Pack 的前 6,000 字符，基本不可供读者使用。
- 本次直接读取完整 DjVu page object，重译 Ski Hut、REI 和 Sierra Designs 的评价、目录信息及主要商品条目。
- w2000 扫描当前不可访问；两款雨衣段落、分数尺寸、商品图片、库存号和部分价格仍未扫描确认。
- 因此本次改进是完整 OCR 重建，不构成 `needs_highres_scan` 闭环。

## Required Fixes

- 源站恢复后，用 n100 w2000 扫描确认三个供应商区域及各商品图片的边界。
- 逐项核对折刀、Logan 夹克、炉具、背架、背包袋、帐杆、动力绳、冻干食品和钓竿的规格、库存号与价格。
- 重点重建 Wind & Rain Parka 与 Mountain Rain Parka 的交错栏位，并核对 Double Mummy 的重量、尺寸和温标。

## Residual Risks

- 高分辨率核查前，跨栏商品字段仍可能发生型号、尺寸或价格错位。
