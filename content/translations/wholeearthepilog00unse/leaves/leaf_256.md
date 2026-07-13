# Leaf 256 Translation

## Source Pack

- Leaf: 256
- Printed page: 705
- Section: Communications / Computer Science
- Scan URL: https://archive.org/download/wholeearthepilog00unse/page/n256_w500.jpg
- Highres scan URL: https://archive.org/download/wholeearthepilog00unse/page/n256_w2000.jpg
- OCR source: `data/issue_agents/wholeearthepilog00unse/pages.jsonl` `ocr.clean_en`
- QA flags: `layout_risk`, `scan_required`
- Source risk: w2000 scan checked. Dense three-column computer-science page; all main text legible.

## Context Notes

- Continues Knuth from prior page, then reviews Scientific American computer anthology, Forrester systems, computer graphics, human-computer dialogue, and computer periodicals.

## Glossary Updates

- algorithm: 算法, accepted common term.
- computer graphics: 计算机图形学, accepted common term.
- man-computer dialogues: 人机对话, provisional.
- Computerworld: `Computerworld`, retain title.

## Final Translation

### Computers and Computation

这 26 篇来自《Scientific American》的文章，加起来成为关于计算机、它们如何出现以及如何使用它们的理想入门。

--SB  
[Bob Albrecht 推荐]

图注：犹他大学的头戴显示器使用一种显示处理器，类似于航空母舰序列所用的处理器。两只微型阴极射线管装在护目镜中。机械联动装置告诉计算机观看者每一刻在看哪里。显示处理器即时提供对应头部位置的正确图像。观看者可以自由看向 360 度圆周中的任何方向，并可上下看约 45 度。右侧展示了他所见的两个样本。随着观察者移动，物体会变大或变小，并相互改变位置关系。

### Fundamental Algorithms 续

每一章单独拿出来都足以为任何作者增光。合在一起，它们可以构成一部“巨著”。但对 Knuth 来说，这只是计划中七卷系列的第一卷！第二卷《Seminumerical Methods》和第三卷《Sorting and Searching》已经出版。与第一卷一样，它们很快成为各自更专门主题上的权威参考。

--Larry Birenbaum

摘录：让我们试着把算法这个概念同烹饪书食谱相比。食谱大概具有有限性（虽然据说盯着看的锅永远不会开）、输入（鸡蛋、面粉等）和输出（电视晚餐等）的性质，但它臭名昭著地缺乏明确性。常有明确性缺失的情况，例如“加一撮盐”。“一撮”定义为“少于 1/8 茶匙”；盐也许定义得够好；但盐应加在哪里（上面、侧面等）？“轻轻翻拌直到混合物呈碎屑状”“在小平底锅中温热干邑”等指令，对受过训练的厨师来说也许是充分解释；但算法必须规定到连计算机都能照做的程度。尽管如此，计算机程序员仍可从研究一本好食谱中学到很多。（事实上，作者差点忍不住把本卷命名为《程序员的烹饪书》。也许有一天他会写一本叫《厨房算法》的书。）

### Principles of Systems

我个人偏爱严格概念性的控制论，在那里你会听到松散语言，比如“老处女数量增加，会带来更多家猫；猫减少老鼠数量，从而在某种程度上降低鼠疫发生率。”Forrester 能教你在那些动词周围使用数字，并让计算机发挥一些用途，正如他在令人钦佩的《Limits to Growth》（第 464 页）中所做的。教材附学生练习册。

--SB

《Principles of Systems》，Jay W. Forrester，1968 年。

### Principles of Interactive Computer Graphics

就是它了……第一本告诉你开始做计算机图形学需要知道的大多数事情的书。不过，在钻进这本书之前，你需要懂一些三角学、坐标几何和矩阵代数，还要对高级语言和汇编语言编程都有适度理解。

全书由五部分组成，另有巨大的书目（319 条参考）和一堆附录：

- 显示计算机图形的硬件；如何在 CRT 上显示点和向量；用于编程简单图像的指令集。
- 生成代码来制作图像的方法；对图像作二维变换的数学；平移、旋转、缩小、放大、扭曲图像。
- 在 CRT 上指向、定位、添加、删除图像的设备：光笔、操纵杆、鼠标；用于输入图形材料的板。
- 在二维屏幕上显示三维图像：透视、数学变换、隐藏线和隐藏面问题、明暗处理。
- 做计算机图形的语言：语言特性、语言设计、对高级图形语言的需要；高级计算机图形语言概览，包括 ALGOL 60、PL1、FORTRAN、DIAL、SAIL、ELAP、EULER 等；完整图形系统的组成部分。
- 另有关于向量和矩阵、齐次坐标技术、小型计算机指令、SAIL 语言、隐藏线算法和选择显示系统等附录。

--Bob Albrecht

《Principles of Interactive Computer Graphics》，William Newman、Robert Sproull，Richard F. Dojny 编，1973 年。

### Design of Man-Computer Dialogues

这本书对可用的人机交互系统和语言类型作了非常彻底的概览。目录显示，这本书主要是这类系统/语言的例子，另加适量哲学和心理学，被划分和细分得很好，所以你应该能毫无困难地找到自己的专门领域并直接钻进去。参考资料似乎服务于作为例子的那些系统。

Martin 写给工业界读者，尤其是那些正在决定建造或购买何种计算机存储与检索系统的人。

关于这些系统如何建造，细节并不多。给出的主要是轮廓和一般考虑。

我碰到几节觉得有趣，例如：对 APL 的优秀介绍；至少两段与 ELIZA 的对话，ELIZA 是一个扮演罗杰斯派精神分析师的计算机程序；几章关于设计自己的系统时应记住什么的精彩内容；还有一个虚构的有线电视连接，把你接到旅行社计算机上，你可以免费预览可能的、或纯粹异想天开的度假地点。

--Dave Kaufman  
[Bob Albrecht 推荐]

摘录：患者接受计算机提问的轻松程度让调查组吃惊。几乎没有任何焦虑或不确定迹象。事后问及体验，没有患者说觉得不愉快或恼人。许多人把计算机同真人顾问相比，说它“有礼貌”“友好”“可理解”。在一个类似应用中，程序用于建立患者人格档案，甚至很难劝老女士离开终端；好多年没有人对她们这么感兴趣了！

### Computerworld 与 Computers and People

怎样跟上计算机科学？每周读《Computerworld》。新产品、新应用、新公司、合并、失败。计算机行业的《Wall Street Journal》。标准报纸马赛克格式和报道方式，有专栏作者、社论版、深度连载特写和一般兴趣文章。

《Computers and People》这份期刊最接近计算机取向报刊中的《Scientific American》。文章显然研究充分，主题面广：技术（硬件和软件）、社会、教育、政治。它是一份有良心的杂志。《Computers & People》（原题《Computers and Automation》）重视社会评论和计算机的人文用途。每年 8 月号聚焦计算机艺术，每年 3 月号聚焦教育中的计算机。

--Jerry Brown  
[Bob Albrecht 推荐]

## Omitted Bibliographic/Order Info

- Compressed addresses, prices, and subscription variants.
- Retained core reviews, bullet content, image captions, quote, signatures, and examples.

## OCR / Uncertainty Notes

- w2000 scan checked.
- Head-mounted-display caption and lower-left Knuth excerpt were verified against scan.
- No unresolved small captions remain for reader-level translation.

## Self Critique

- The translation keeps the page's resource-review structure and technical specificity.
- Dense lists are translated as lists rather than prose summaries.
