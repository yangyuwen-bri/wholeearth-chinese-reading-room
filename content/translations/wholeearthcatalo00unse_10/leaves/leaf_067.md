# Leaf 067 Translation

## Source Pack

- Issue ID: `wholeearthcatalo00unse_10`.
- Access leaf: `n67`; canonical DjVu object:
  `wholeearthcatalo00unse_10_0068.djvu` (object 68 of 134).
- Physical/PDF mapping: scandata physical leaf `68`, PDF page `68`,
  `pageType=Normal`, left-hand page.
- Printed page: `66`.
- Section: `Communications`.
- Scan URL:
  https://archive.org/download/wholeearthcatalo00unse_10/page/n67_w500.jpg
- High-resolution scan URL:
  https://archive.org/download/wholeearthcatalo00unse_10/page/n67_w2000.jpg
- OCR source: official Internet Archive DjVu XML at
  `_local/page_xml/wholeearthcatalo00unse_10_djvu.xml`; 860 OCR words in
  147 lines.
- Scan evidence: local PDF page 68 was rendered at 300 dpi and checked as a
  full page. Independent review must use 600/1,200 dpi for the code diagrams,
  activity sequence, set table, price list, addresses, and photo caption.
- Source-pack gap: `ocr_risk_flags` is absent. Direct inspection indicates
  `two_records`, `binary_code_diagrams`, `dense_process_example`,
  `set_classification_table`, `historical_product_prices`, and
  `highres_review_required`.

## Context Notes

- 本页有两条独立记录：左栏《Data Study》，右栏 McBee Keysort System。左栏的
  二进制编码图、信息定义、活动序列和集合示例均属于书摘；右栏的穿孔卡说明、
  价格清单和 Hal 分拣照片属于 McBee 产品记录。
- 《Data Study》的图表使用 `A / B / C / D`、`0 / 1` 和组合代码展示单项到四项
  组合；译文保留稳定层级和示例，不把排版连线扩写为额外算法。
- Keysort 价格、地址、油墨复制能力和产品建议均为 1969 年目录信息，不代表当前
  可购性、价格或档案管理建议。

## Glossary Updates

- `information handling` → `信息处理`
- `monograph code` → `单项代码`
- `digraph code` → `二项组合代码`
- `trigraph code` → `三项组合代码`
- `tetragraph code` → `四项组合代码`
- `punched feature card` → `特征穿孔卡`
- `mutually exclusive set` → `互斥集合`
- `overlapping set` → `重叠集合`
- `cumulative set` → `累积集合`
- `equivalent set` → `等价集合`
- `edge-notched card` → `边缘缺口卡`

## Final Translation

### 《数据研究》（Data Study）

没有组织起来的信息，在你的生活里就不是信号，而是噪声。你为了找一样东西，从头
到尾翻遍整份档案，把自己耗得筋疲力尽，感觉像一名驾车穿越纽约市区的司机一样蠢；
原因也一样：你的访问方式蛮横、线性而费力。这本书帮不了纽约，却能帮你。它讲解
怎样把东西整理清楚的理论与实践——至少是在组织层面。至于展示则是另一回事，
信息科学在这方面仍然很差。

#### 书目与订购

**Data Study**
J. L. Jolley 著
1968 年；254 页
2.45 美元，邮资付讫

书封系列名：`World University Library`（世界大学文库）。

购自 McGraw-Hill Book Company 的下列地址：

- Princeton Road / Hightstown, N.J. 08520；
- Manchester Road / Manchester, Missouri 63062；
- 8171 Redwood Highway / Novato, California 94947。

或向 WHOLE EARTH CATALOG 购买。

#### 编码图

上图以 `A / B / C / D` 四个位置逐行列出十六种状态，并用分支线展示层级关系：

```text
0000 = 0    0001 = 1    0010 = 2    0011 = 3
0100 = 4    0101 = 5    0110 = 6    0111 = 7
1000 = 8    1001 = 9    1010 = 10   1011 = 11
1100 = 12   1101 = 13   1110 = 14   1111 = 15
```

下图首先列出空图代码（`Agraph code`）：`∅ = 0000`。随后把同样的四个位置分为：

- 单项代码：`A = 1000 / B = 0100 / C = 0010 / D = 0001`；
- 二项组合代码：`AB = 1100 / AC = 1010 / AD = 1001 / BC = 0110 /
  BD = 0101 / CD = 0011`；
- 三项组合代码：`ABC = 1110 / ABD = 1101 / ACD = 1011 / BCD = 0111`；
- 四项组合代码：`ABCD = 1111`。

右侧连线图显示从空图、单项到四项组合的包含关系。

十进制数字系统若把十个字符按升序排列，就从 `0` 开始。二进制、八进制及其他
系统也从 `0` 开始，因为 `0` 是原点，是零，是情境发生某种变化、从而给我们带来
信息以前的起点。

本书的主题是信息处理。信息由变化产生；我们用什么作为变化单位，就用什么作为
信息单位。

#### 一连串活动

大量信息处理都与一组连续操作有关：识别、转译、检索、描述、搜索，再识别、
转译、检索——这样的序列可以不断重复。设想一位索引员使用一叠特征穿孔卡，在
人事记录系统中寻找若干人，他或她的思考与行动如下：

- **识别：** 我需要“男性的”（`masculine`）和“人员”（`personnel`）这两个概念……
- **转译：** 但系统把它们称作“男性”和“职员”……
- **检索：** 于是我找到带有这些标题的卡片……（假定按字母顺序排列）
- **描述：** 把它们叠起来……
- **搜索：** 寻找重合的孔……
- **识别：** 它们位于 `32` 和 `457` 号位置……
- **转译：** 对应 Jim Robinson 和 Patrick Lucas……（假定登记簿把姓名列在号码
  旁边）
- **检索：** 于是我找到他们的记录卡……（再次假定按字母顺序排列）
- **描述：** 一次一张……（单张卡就是只有一张的卡叠）
- **搜索：** 分别寻找两人的特征……
- **识别：** 结果如下……
- **转译：** 从中我推断……

#### 四种集合示例

- **互斥集合：** `hotel is in France / Spain / the United States / Germany /
  Switzerland`（旅馆位于法国／西班牙／美国／德国／瑞士）；
- **重叠集合：** `hotel possesses a ballroom / tennis courts / a swimming pool /
  a bowling green / a skittle alley / a golf course`（旅馆拥有舞厅／网球场／
  游泳池／草地保龄球场／九柱戏球道／高尔夫球场）；
- **累积集合：** `hotel is more than 50 / 100 / 200 years old`（旅馆有超过
  50／100／200 年历史）；
- **等价（相同）集合：** `hotel has first class food / excellent cuisine /
  top quality refreshments`（旅馆有一流食物／优秀菜肴／顶级茶点）。

### McBee Keysort 系统

你手头什么东西特别多？学生、订户、笔记、书、记录、客户，还是项目？一旦同类
东西超过 `50` 或 `100` 件，就很难再记清楚；该把存储与检索系统外置了。在昂贵
计算机之外，McBee 是一种顺手的方法。它粗朴，却实用：一叠边缘有许多孔的卡片、
一根长而钝的针和一个切口钳。

把针穿过一叠卡的某个孔，再往上一提；在该孔切过缺口的卡不会被提起，而会掉下来。
因此，卡片无需保持固定顺序。你可以按特征、数字、字母或其他方式分拣：只要穿针、
扇开、提起、接住。卡片还带有一种功能：用一件手持、气味强烈的小装置在每张卡上
刷两下，就能印出地址或其他内容；大约可以得到 `50` 份清楚副本，随后印迹又退回
原始的模糊状态。

Doug Engelbart 告诉我们，用给动物耳朵打缺口的钳子给卡片切口，比 McBee 出售的
钳子更好，也更便宜。

［Doug Engelbart 与 Joe Bonner 推荐。］

#### 历史价格

- `1,000` 张印刷型 Keysort 卡：`35.75` 美元；
- `1,000` 张 Hecto carbon black（用于印刷）：`3.60` 美元；
- `1` 根 Keysorter（针）：`5.05` 美元；
- `1` 把 Handpunch：`9.55` 美元；
- `1` 台 Handiprinter（前述小装置）：`41.40` 美元。

可在电话簿中查找 McBee，或写信至：

Litton Automated Business Systems
600 Washington Avenue
Carlstadt, N.J. 07072

#### 照片图注

照片中的 Hal 正在分拣目前已确定收入春季《CATALOG》的全部条目。他先把针穿过
`No. 4` 孔——如果本店备货，该孔就会切出缺口——于是所有已经备货的条目都会
掉下来。接着，他会把针穿过 `No. 2` 孔——如果我们无法供货，该孔会切出缺口——
最后仍留在针上的，就是他需要为商店订购的新品。

## Omitted Bibliographic/Order Info

- 无。《Data Study》的作者、年份、页数、价格、McGraw-Hill 三处地址及 WHOLE
  EARTH CATALOG 选项均已保留；McBee 的五项价格、查询方式和 Carlstadt 地址也已
  收录。
- 左栏编码图的 `0000 = 0` 至 `1111 = 15` 已逐行转录；下表的
  `∅ / Agraph code` 及单项、二项、三项、四项的全部四位代码也已纳入，右侧连线
  关系按层级说明保留。

## OCR / Uncertainty Notes

- 官方 OCR 把编码图的 `0 / 1`、书目地址、活动序列、集合表和 McBee 价格交错输出。
  译文依据左右栏粗边界和标题恢复两条记录。
- `Hecto carbon black`、`Handpunch`、`Handiprinter` 以及价格
  `35.75 / 3.60 / 5.05 / 9.55 / 41.40` 需在独立 1,200 dpi 审校中逐字逐项复核。
- 活动序列的 `32 / 457`、两个人名和四类集合示例依据整页图转录；不把书摘中的
  假设性档案流程改写成当前数据治理建议。
- Hal 图注中的 `No. 4 / No. 2` 与“备货／无法供货”切口含义方向相反，译文按原页
  保留，未用直觉统一。

## Self Critique

- 已完整分开《Data Study》与 McBee Keysort，覆盖两条评论、书目、三处出版社
  地址、编码层级、信息定义、活动序列、集合表、产品原理、价格、地址和照片图注。
- 对二进制图逐行保留十六种状态，并完整转录空图、单项、二项、三项和四项代码；
  没有用端点概述替代可稳定读取的矩阵证据。
- 所有价格、产品能力和索引方法均明确限定为历史资料；未把 1969 年的卡片系统包装
  成现行采购或信息管理方案。
