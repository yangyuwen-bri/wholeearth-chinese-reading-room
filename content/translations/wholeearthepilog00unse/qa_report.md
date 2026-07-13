# Whole Earth Epilog Full Translation QA Report

## Status Counts

- `accepted`: 283
- `needs_highres_scan`: 25
- `no_translation_needed`: 14

## Remaining Blockers

### needs_highres_scan

- leaf 15: Poorest Developing Countries 数字表行值、脚注、n.a. 对齐；XML/crop OCR 不能保留表格行列。
- leaf 47: Practical Farm Buildings 的 Table of Dimensions 尺寸表行值不可可靠恢复。
- leaf 58: Shelter 缩印书页与施工图手写标签不可完整恢复。
- leaf 67: Applying Mortar 砌砖步骤图右缘仍裁切；砂浆配方已补，步骤图未全。
- leaf 69: 椅面编藤、水管照片、Alaskan drum-stove 技术图标签，尤其炉图安全/进气标签。
- leaf 76: air-dome、sanitation、house-inspection 等技术图标签。
- leaf 82: The Collector Absorber - Part A 平面图手写标签与左下管路小图。
- leaf 106: 蜡烛添加剂/性质手写图表，左缘裁切且 OCR 噪声重。
- leaf 111: 合成染料用量/牢度表无法完整恢复。
- leaf 184: 北京公交路线图路线号、站点和内部标签混列乱码。
- leaf 186: 马具驮运、滑雪打蜡附件、地图/制图标签。
- leaf 195: landsailer 规格表，若干帆面积/成本/供应商单元不可靠。
- leaf 197: 滑翔机控制、气球图、纸偶稳定性图标签。
- leaf 198: 天气图、滑翔机表，图表列混乱。
- leaf 201: Hasler 装置、造船图、成本百分比图表标签。
- leaf 202: 舱口、网片、Zurn 太阳能充电器、Pansy 取暖器规格逐格不可靠。
- leaf 203: Samson 游艇编织绳尺寸/载荷/重量表单元格。
- leaf 204: Grand Canyon 路线图、Canoe Trail Guides 路线微表、气垫船图。
- leaf 209: Noamtrac 地图、能量消耗表细项。
- leaf 213: Prusik 步骤、水泡/足部护理、冰屋切块图。
- leaf 214: 雪鞋图、Wedeln 滑雪阶段图。
- leaf 215: 刮皮器、陷阱/套索图标签。
- leaf 217: 刀具结构标签、鹰猎结步骤。
- leaf 220: 路边故障排查流程图决策框/动作标签/量油尺标签。
- leaf 240: 地下漫画样张多格手写对白；R. Crumb 大格已补，小格 OCR 为图像噪声。

## Notes

- All leaves 0-321 have translation and review files.
- `no_translation_needed` is used for cover/index/back matter or non-body pages.
- `needs_highres_scan` means the prose translation exists, but a substantive image/table/diagram/label blocker remains.
- The workflow uses Archive scans, local DjVu XML OCR, and crop-level OCR helpers.
