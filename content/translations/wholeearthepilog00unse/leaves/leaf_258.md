# Leaf 258 Translation

## Source Pack

- Leaf: 258
- Printed page: 707
- Section: Communications / Math
- Scan URL: https://archive.org/download/wholeearthepilog00unse/page/n258_w500.jpg
- Highres scan URL: https://archive.org/download/wholeearthepilog00unse/page/n258_w2000.jpg
- OCR source: `data/issue_agents/wholeearthepilog00unse/pages.jsonl` `ocr.clean_en`
- QA flags: `dense_ocr_page`, `layout_risk`, `scan_required`
- Source risk: w2000 scan checked. Dense page with table and calculator feature lists; legible.

## Context Notes

- Top entry is Morton Davis's game theory book, including the prisoner's dilemma payoff table.
- Main page body is Andrew Fluegelman's four-function pocket-calculator buying guide plus HP scientific calculator overview.

## Glossary Updates

- prisoner's dilemma: 囚徒困境, accepted common term.
- four-function calculator: 四则运算计算器, provisional.
- algebraic logic: 代数逻辑, provisional.
- Reverse Polish Notation / RPN: 逆波兰记法 / RPN, accepted common term.

## Final Translation

### Game Theory

对博弈论的要素和用途，以及限制，作了令人钦佩的介绍。书中很好地提出了“囚徒困境”的悖论，也很好地怀疑了 Anatol Rappaport 的“解法”。

--SB

《Game Theory: A Nontechnical Introduction》，Morton D. Davis，1970 年。

### 囚徒困境

两名被怀疑共同犯罪的人被警察逮捕，分别关进不同牢房。每个嫌疑人都可以选择招供或保持沉默，并且每个人都知道自己行动可能带来的后果。这些后果是：1. 如果一名嫌疑人招供而同伙没有，招供者转为污点证人并自由离开，另一人入狱二十年。2. 如果两名嫌疑人都招供，他们都入狱五年。3. 如果两人都保持沉默，他们都因携带隐蔽武器这一较轻罪名入狱一年。我们假设“盗贼之间没有荣誉”，每名嫌疑人只关心自己的利益。

表格：嫌疑人 1 与嫌疑人 2 都可选择招供或不招供。双方都招供，各判五年；1 招供而 2 不招供，1 自由、2 二十年；1 不招供而 2 招供，1 二十年、2 自由；双方都不招供，各一年。

在这些条件下，罪犯应当怎样做？图 29 展示了这个博弈。这就是著名的囚徒困境，最初由 A.W. Tucker 提出，已经成为博弈论短暂历史中的经典问题之一。

让我们从一名嫌疑人的角度看囚徒困境。由于他必须在不知道同伙会做什么的情况下作决定，他必须考虑同伙的每一种选择，并预期每种选择对自己的影响。

假设他的同伙招供；我们的人要么保持沉默而入狱二十年，要么招供而入狱五年。或者，如果同伙保持沉默，他可以也沉默而服刑一年，也可以招供而获得自由。表面看来，无论哪种情况，他招供都更好！那么问题在哪里？

悖论在这里。两个天真的囚徒太无知，无法跟随这个强有力的论证，于是都保持沉默，只入狱一年。两个老练的囚徒接受了最好的博弈论建议，于是都招供，并得到五年徒刑来沉思自己的聪明。

当“囚徒困境”被反复玩，而且不是固定次数而是无限期地玩时，合作策略才显出力量。囚徒困境常被玩的条件正是如此。两个竞争公司知道自己不会永远经营下去，但通常无法知道死亡、合并、破产或其他力量什么时候会结束它们的竞争。因此，玩家不能分析最后一次“玩”会发生什么，再从那里倒推，因为没人知道最后一次“玩”何时到来。支持不合作策略的强有力论证于是瓦解，我们松了一口气。

### 袖珍计算器（四则运算）

作者：Andrew Fluegelman

最近的电子袖珍计算器现象不只是另一种消费者诱惑。这些机器能显著节省时间、提高准确性，可能甚至节省能量；它们是好工具。（我们在为《Epilog》确定发行商、印刷商和封面价格时，必须穿过一团相互关联且不断变化的参数，戏剧性地发现了这一点。若没有朋友借给我们的 Texas Instrument Datamath TI 2500，那件事根本无法处理。）于是我们决定寻找四则运算计算器中的“最佳交易”。

我们最重要的发现是，个人计算器行业和市场当前处在巨大动荡中：公司过量生产、压价、倒闭；批发商和零售商大批买入停产型号；价格疯狂变动，通常向下。几年内大概会稳定下来，但在稳定前，最佳交易不在那些已经站稳的几款计算器中，例如 Datamath，而在爆炸性技术的受害者中。下面内容应能帮助你选择。

既然你可以相当安全地假设，任何你买的计算器都会对你按进去的问题给出正确答案，那么你应寻找的是能力的“正确”组合。我们认为一个有用工具的最低特征如下：

- 8 位显示：多数计算器的标准。可让你算到 999,999.99，足够多数问题所需的重要位数。
- 全浮动小数：让你按入 7、11.3 和 00001，得到总数 18.30001。
- 代数逻辑，而不是最便宜型号中的“算术逻辑”：让你按你会“说”出来的方式输入问题。测试方法是按 5、减号、3、等号，能得到答案。
- 链式和混合计算：让你不必取中间总数，就能连续执行不同函数的计算。
- 常数模式：让你反复乘以或除以一个常数，而不必每次重新键入。
- 清除输入键：让你清除最后输入的项目，而不清除前面的计算。

除这些基本特征外，许多计算器上还有两个功能，会极大扩展其用途：

- 记忆：本质上是内置草稿纸。你可以把答案输入一个独立电路，后续计算的答案可以加到或减去其中。这个“记忆”的总数稍后可以重新引入主电路上的进一步计算。这个能力事实证明非常方便。
- 溢出指示 / 取回：许多计算器会提示你的答案超过显示位数能力，并只显示最高有效位。有些允许你连续把这个答案除以 10，直到小数点出现，从而帮助你弄清答案的量级。最复杂的溢出取回形式，是让你拨动开关，看见“丢失”的数字。也有下溢指示和取回，只是不太常见。

### 选择计算器

这里描述的是基本“四则运算”（加、减、乘、除）型号。你也可以买到能自动处理和计算幂与根、倒数、对数和三角函数、虚数、圆周率，并以指数形式显示答案的计算器。还有些能计算单利和复利、债券和年金收益、抵押贷款利率和趋势线。除非你对专门功能有明确需要，否则不要为这些“科学”和“商业”计算器烦心。如果确实需要，请仔细考虑哪种功能组合对你最有用，并准备花几百美元。

关于电源，计算器能用交流电运行很重要。尽管便携性是这些机器的吸引力之一，你大概会发现多数“重型”计算是在桌边做的，那里有插电电源。计算器的便携电源要么是内置可充镍镉电池，要么是单独可更换电池。不要自动假设可充电就是最佳选择。它们用完后需要数小时充电，也使计算器更贵，虽然如果常作便携使用，长期看更经济。想想你的计算器主要会怎样使用，再考虑替代成本和电池寿命。

最后，考虑计算器的“手感”。按钮位置合乎逻辑吗？有些型号的按钮登记时会有可感觉到的“咔哒”声，这似乎有助于准确输入数字。另一个考虑是显示的大小和易读性。（有些人，通常是男性，对许多型号上的红色显示色盲。）

你现在可以开始为自己的“最佳交易”购物了。去最方便的商店，玩玩一些“名牌”：Texas、Bomar、Sharp、Commodore。（也看看一台 Hewlett-Packard，好让自己相信那些额外功能对你大概完全无用，只会弄乱键盘。）然后开始寻找特别销售、清仓等，它们能比名牌型号省很多，但要记住上面列出的必要特征。

我们不建议通过邮购买清仓品。许多卖清仓品的零售商会提供相对短期的更换担保，但不包括长期维修。别太担心这一点。我们想说的是，今年买的计算器不是终身投资。买一台能用的便宜货，撑到技术和市场成熟稳定即可。我们离可编程袖珍计算机只有几年。

### 科学计算器

1972 年，Hewlett-Packard Corporation 推出 HP-35，几乎开创了一个行业。现在他们有四种昂贵的高级袖珍计算器型号，为较低价竞争者树立衡量标准。

- HP-35 有四寄存器操作栈和一个独立存储寄存器；预置四则运算、三角函数及反函数、常用对数和自然对数及反对数、倒数、平方根、任意次幂和圆周率。当前售价 225 美元。
- HP-45 在 35 的基础上增加九个可寻址存储寄存器和独立的“last-in”寄存器；三角函数可用度、弧度或百分度，并可把答案转换成度 / 分 / 秒；还增加自然反对数、直角 / 极坐标转换、向量运算、统计平均数、标准差、平方和、阶乘、百分数和百分比变化，以及公制转换常数。现价 325 美元。
- HP-65 含 100 步程序存储、51 个预置函数和磁卡读写器，可插入 HP 提供的预录程序，也可记录、编辑和重复使用键盘输入程序。HP 称它是第一台个人可编程计算机。价格 795 美元。
- HP-80 是金融计算器，有 36 个函数，包括债券收益率和价格、复利、抵押贷款支付、回报率、趋势线、应计利息、贴现票据、年收益、年百分率、均值和标准差，以及 200 年日历。395 美元。

所有 HP 都有 200 个十进位范围（10^-99 到 10^99），可表达多达 10 个有效数字。HP 也采用“逆波兰记法”。基本意思是没有等号键。数字被“输入”操作栈；然后对栈中的数字执行操作。某次操作的答案会自动装入栈中。要加 3+4，你按 3、ENTER、4、加号，答案 7 出现。对于相当直接的计算，采用代数逻辑并带记忆的计算器显然更简单；不过在包含多个括号表达式的长计算中，RPN 逻辑的优越性变得明显。

可以预期，随着新型号推出、竞争加剧，这些高级计算器的价格会下降。现在有大量带科学功能的计算器，售价 100 到 150 美元。在选择科学计算器时，第一步应当坐下来，弄清楚你将用它解决什么类型的问题。然后只为你能使用的东西付钱。

## Omitted Bibliographic/Order Info

- Compressed publisher and order addresses.
- Retained table logic, feature lists, HP model details, prices where central, and advice.

## OCR / Uncertainty Notes

- w2000 scan checked.
- Payoff table and calculator photos/captions are legible; table is translated in prose.
- Some keypad examples are translated by function rather than exact punctuation.

## Self Critique

- The translation keeps the article's buyer-guide logic and does not modernize the 1974 calculator market.
- The Game Theory excerpt is kept as a separate entry and not merged into the calculator article.
