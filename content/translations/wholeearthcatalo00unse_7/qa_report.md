# QA Report

## Release State

Fall 1969 `wholeearthcatalo00unse_7` 的扫描级翻译修复已于 2026-08-21 闭合。

- 翻译文件：132/132（`leaf_000.md`–`leaf_131.md`）。
- 独立 review：132/132（`leaf_000.review.md`–`leaf_131.review.md`）。
- 状态：`accepted=132`；其他工作流状态为 0。
- 阻断标记：`coverage_review_required=0`、`independent_rereview_required=0`、`needs_highres_scan=0`、`revise=0`。
- 官方 OCR 基线总量：189,192 词；每页 review 均包含具体的 Source inventory、Translation coverage 和 Permitted omissions。
- 发布门禁：通过，输出为 `release gate passed: 132 leaves have concrete coverage evidence`。

## Failure Repaired

2026-08-15 报告的 `leaf_007` 摘要替译不是孤立问题。旧稿中曾出现以下系统性缺陷：

- 用主题提要、条目介绍或现代解释替代原刊的评论、论证和文学节选；
- 漏掉多栏版面中的右栏、下栏、广告、表格、价格、地址或图片文字；
- 将 OCR 为零或断裂的页面误判为空白或不可读；
- 在没有完成源到译文覆盖核对时沿用 `accepted`；
- 使用泛化 review，无法说明源页究竟有哪些内容、译文覆盖到哪里。

本轮已逐页重建 132 页的实质内容。评论、论证、节选、署名、表格、操作步骤、图注、价格和订购字段均按高清扫描恢复；不再允许用总结性描述代替原文。封底 `leaf_131` 也已由“空白页”纠正为包含 `FURTHER / closer` 的视觉文本页。

## Final High-Resolution Closure

最初 29 个 `needs_highres_scan` 页面均已闭合。全书恢复完成后，又对仍带历史性独立复核标记的三页使用原始 3514×4752 JP2 复核：

- `leaf_054`：补齐 40 家金工供应商的地址与品类、Adhesive Products 套装/批量价格，并纠正 Gem Guild 的克拉重量与包价关系。
- `leaf_088`：核准 Consumer Reports、避孕手册三栏、Snugli 图示及全部历史医疗文字；保留扫描页码与本地元数据冲突记录。
- `leaf_118`：核准 13 日课程表、Fuller 引文、Humanitas 两处信箱号，并补译《The Road to Kwashiorkr》封面副文。

三页 `independent_rereview_required` 均已清除。

## Release Gate

`tools/validate_release.py` 对每一页执行以下失败关闭检查：

1. `status.jsonl` 必须连续覆盖 `leaf_000`–`leaf_131`，且全部为 `accepted`。
2. 翻译和 review 文件必须同时存在，`Final Translation` 不得为空。
3. review 必须含具体 Source inventory、Translation coverage、Permitted omissions，结论必须为 `accepted`，Required Fixes 必须为“无”。
4. 读者正文不得出现页面介绍、主旨总结或书评转述等摘要替译语言。
5. 高 OCR 词数页面须通过中英文篇幅压缩筛查，任何例外必须在覆盖证据中具体说明。
6. 三页以上不得复用同一组泛化 review reasons。

2026-08-21 最终运行结果：0 个发布错误，门禁通过。

## Non-Blocking Source Risks

剩余 `qa_flags` 是版面或源材料属性，不是待办状态：

- `layout_risk=128`：原刊绝大多数页面为密集多栏拼贴，阅读室必须与扫描并排呈现。
- `ocr_reconstructed=14`：相应页面已用扫描恢复，不代表仍待翻译。
- `metadata_page_number_conflict=2`：`leaf_088`、`leaf_118` 的扫描可见页码与本地元数据不一致；译文以扫描为准并保留冲突记录。
- `medical_historical_text=2`、`numeric_boundary_risk=1`、`mathematical_graphics=1`、`scientific_notation=1`、`poetry_lineation=1`：用于提醒阅读室保留原页语境，不阻断发布。

## Reader Release Requirement

只有从当前门禁通过的 132 页重新生成、并完成本地浏览器逐页与导航测试的阅读室产物，才可发布。2026-08-15 前生成的旧 JSON 或阅读室构建不得继续使用。
