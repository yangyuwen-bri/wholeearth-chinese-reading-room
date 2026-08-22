# Workflow Lessons

Use this file to record issue-specific findings that may improve the global
workflow later.

Do not edit global prompts or workflow rules silently during a batch. First
record the problem here, then decide whether it is issue-local or reusable.

## Issue-Specific Risks

- 官方 OCR 会在跨栏页面打乱段落和表格对应关系；必须以高清扫描重建阅读
  顺序，不能按 OCR 输出顺序直接翻译。
- 低文字量封面可能被 OCR 大量漏字；验收前须逐项清点可见文字。
- 名单页不能概述成“以下为名单”；人名和所在地应逐项保留，专名可原样
  保留以避免无依据音译。

## Batch Lessons

| Date | Leaves | Problem | Local Fix | Promote to Template? |
| --- | --- | --- | --- | --- |
| 2026-08-21 | 000-002, 147 | OCR 漏字、跨栏错序、名单易被摘要化 | 高清扫描逐项清点；名单逐行保留；覆盖证据列出全部内容类型 | yes |
| 2026-08-22 | full issue | 旧版提示词允许压缩价格、库存号和地址，可能诱发总结替译 | 发布 v1.2 translator/reviewer prompts；所有可辨识文字默认全文翻译，不可恢复内容必须留证并阻塞验收 | yes |

## Prompt Change Log

| Prompt | Version | Reason | First Used On |
| --- | --- | --- | --- |
| `translator_v1.md` | `v1` | initial template | `<date>` |
| `translator_v1_2.md` | `v1.2` | prohibit omission, compression, grouping, and summary substitution for all legible source text | next issue |
| `reviewer_v1_2.md` | `v1.2` | require explicit full-coverage audit and revise on any unproven omission | next issue |

## Reader-Facing Leak Checks

Record any wording pattern that must stay out of public reader text.

- `Final Translation`
- `Self Critique`
- `OCR Notes`
- `leaf 001` as body heading
- page-description prose such as "right column" or "this page introduces"
- evidence-quality prose such as "legible source text", "readable cover text",
  or "OCR recovered"
