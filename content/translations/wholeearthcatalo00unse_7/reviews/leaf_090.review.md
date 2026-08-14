# Leaf 090 Independent Review

## Conclusion

needs_highres_scan

## Reasons

- 旧稿是把多栏目录逐行交织后的机器直译，只覆盖生成版 Source Pack 的前 6,000 字符，基本不可供读者使用。
- 本次直接读取完整 DjVu page object，重译 Sears/Wards 邮购评价、工具与农用商品目录，以及《The Armchair Shopper’s Guide》书评和商家摘录。
- w2000 扫描当前不可访问；若干订单号、尺寸、价格与图片归属仍未扫描确认。
- 因此本次改进是完整 OCR 重建，不构成 `needs_highres_scan` 闭环。

## Required Fixes

- 源站恢复后，用 n90 w2000 扫描确认三个阅读区及各商品图片的边界。
- 逐项核对台虎钳、槽刀、水准仪、工具箱、蜜蜂、水果压榨机、举升器、煤油炉和混凝土搅拌机的型号、尺寸与价格。
- 核对《扶手椅购物指南》的书价、出版社地址、商家地址及页末手表条目的截断位置。

## Residual Risks

- 高分辨率核查前，跨栏商品字段仍可能发生型号、尺寸或价格错位。
