# Leaf 043 Review

## Conclusion

accepted

## Reasons

- 本次审核逐项对照了 `leaf_043.json`、access `n43` 对应的 PDF 第 44 页
  600 dpi 渲染与译稿。页面映射正确；上半页 `New Scientist` 与下半页
  `Scientific American` 的记录边界清楚，评论、摘录、图片和订阅块没有
  被 OCR 的跨栏顺序混入另一条记录。
- 《新科学家》的目录评论、Steve Baer 署名、漫画图注，以及吸烟、睡鼠、
  脉冲星、DNA 和全息存储等可辨标题均已保留。全息段的贝尔实验室、铌酸锂、
  同时存储 `1,000` 幅全息图、效率和容量比较也与原刊一致。
- 《科学美国人》的大脑、氮肥污染、肥皂泡和混凝土四段主体归属正确。
  `25 years / 70% / 300% / 1,400% / 10 million tons` 均无行列漂移；肥皂泡
  的两种配方、溴在与酸反应前的危险、家庭缺乏所需控制条件、不得自行配制
  的警告，以及 `P.O. Box 191 / 11510 / $4 a pint / thousands of bubbles`
  均准确保留。
- 回归审核确认 `New Scientist` 地址已经按原刊修正为
  `128 Long Avenue`；`Scientific American` 的 `$8.00 / monthly /
  415 Madison Avenue / 10017` 仍准确。全息段已将 `holographic plate`
  纠正为“全息感光板”，肥皂泡标题也已恢复 `How to blow` 的含义。
- 蛋白质摘录已补全 `hypothesis to explain how living mechanisms have
  increased in complexity`；混凝土段也已补全 `including the monomer in
  the original mix`。`Context Notes`、风险标签、遗漏声明和不确定性说明中
  关于两处截断的错误陈述均已删除。
- `Murder at Thank God Bay`、`P / h` 和六组演化标签均已写入；
  `PROBOSCIDEA` 与完整的 `PTEROSAURIA (DIMORPHODON)` 不再遗漏。
  最后一次回归确认 `Murder at Thank God Bay` 现在只作为独立标题保留；
  `P / h` 已移至单独的“小示意图”段落，并明确不判定所属文章或字母含义，
  不再制造原刊不能支持的内容归属。
- 文件采用要求的七段结构，顺序为 `Source Pack`、`Context Notes`、
  `Glossary Updates`、`Final Translation`、
  `Omitted Bibliographic/Order Info`、`OCR / Uncertainty Notes`、
  `Self Critique`；页码锚点、左右页和 `765` OCR 词、`120` 行与 JSON 一致。
  七项原 Required Fixes 及随后发现的小示意图归属问题均已关闭；回归未
  发现新的内容、数字、价格、地址或标签错误。

## Required Fixes

None.

## Residual Risks

- 右上角椭圆中的《新科学家》封面还包含数行低反差、网点化的小标题；即使
  在 600 dpi 下也无法稳定逐字辨认。地址、价格和刊名位于椭圆外，清晰度
  足够，不能用封面内部字迹的不确定性为 `Long Avenue` 的误录开脱。
- 原刊把肥皂配方印作 `Kuehner's dibromostereate soap`；当前“二溴硬脂酸盐
  肥皂”可表达化学含义，但若补英文，宜保留本页拼写并标注，不要无说明地
  现代化拼字。
- 《科学美国人》封面复制图内部还有极小的卷期/封面字样，网点与尺寸不足以
  可靠转录；本次只要求页面排版层上稳定可辨的标题、地址和图签。
- 吸烟与妊娠、氮污染、化学泡液、辐射处理和学习能力均是 1960 年代期刊
  摘录。本审核确认的是翻译忠实度，不构成现代医疗、环境或工程建议。
