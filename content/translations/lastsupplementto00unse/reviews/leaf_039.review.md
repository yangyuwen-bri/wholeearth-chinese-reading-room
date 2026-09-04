# Leaf 039 Review — 2026-09-04 Corrective Audit

## Conclusion

accepted

## Coverage Evidence

- Source inventory: Internet Archive n39 原页（2727×4165），印刷页 38；左栏《EDGAR CAYCE (cont’d)》4 段、《THE READINGS》8 段，右栏《The Ordinary Group》11 段及署名 Peter Friedman。
- Translation coverage: 三个标题、23 段正文及署名逐项核对；补回凯西逝世年龄 67 岁、“四十三年的大部分时间”、上课前的走廊场景。核对 1901/1944/1909/1923、16,000、14,249、200,000、8,985、2,500、667、1,995 与 37½%（其中数字可按中文写法表达）。
- Permitted omissions: 无。

## Reasons

- 原发布阅读室在第二个正文二级标题前截断，只导出了本页约 29% 的译稿；文件存在、accepted 标签及部署哈希一致均未阻止此错误。
- 修复通用正文解析边界，并以独立的工作流分隔符核验全页导出，恢复《通灵解读》和《普通组》全文，不以摘要替代。
- 与前页 leaf 038 术语对照后，将 readings 的“读数”误译统一修正为“通灵解读”；原文讨论的是凯西的通灵解读记录，不是仪器读数。

## Required Fixes

- None.

## Residual Risks

- 本次纠错复核与修改由同一执行者完成，不另计为独立审校。该页的复核结论不能外推到其余 131 页。
