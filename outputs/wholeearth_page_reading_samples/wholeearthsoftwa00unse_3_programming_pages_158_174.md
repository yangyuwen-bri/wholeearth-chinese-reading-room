# Whole Earth Software Catalog 2.0, Fall 1985 - Programming 逐页样板

状态：页级样板。依据 `outputs/wholeearth_page_dossiers/wholeearthsoftwa00unse_3/pages.json` 与 Archive 扫描图逐页整理。这里覆盖 Programming 章从开章到 Utilities 前半段，约印刷页 158-174；不是全书完成稿。

## 这一章的真实结构

Programming 不是把编程当成“学一门语言”的章节。它的展开顺序更像一条使用者的成长路径：先说明为什么普通软件用户也需要懂编程；再从程序风格、C、Pascal、BASIC、COBOL、第二语言、Prolog、机器语言、UNIX、结构化设计、软件工程一路走到 utilities。也就是说，这章的中心不是“程序员职业”，而是“怎样成为能判断、改造、绕开和理解软件的人”。

这也是为什么那句“编程可以是审美活动”不能单独抽出来看。它在这章里对应的审美，不是浪漫化地说代码很美，而是：程序有结构、风格、可读性、设计图、工具环境和使用者心理。Whole Earth 把编程放进工具文化，是因为编程让人从软件消费者变成软件机制的理解者。

## p.158 / leaf 159

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n159_w500.jpg

开章由 Gerald M. Weinberg 负责。他先用汽车类比个人电脑：早期汽车需要带机械师，早期电脑需要带程序员；大规模普及的前提是普通人不必随身带专家。但 Weinberg 没有说专家知识不重要。他强调，懂一点机械原理的司机会更会买车、修车、判断服务；同理，懂一点编程的人会更会挑软件、读懂糟糕文档、绕开程序缺陷。

这一页最重要的不是“人人都要写程序”，而是“人人都在被软件工具支配，所以至少要理解工具背后的机制”。他还批评当时个人电脑编程工具落后于大型机世界，市场不成熟导致用户看不出什么是好工具。这一页把 Programming 章的读者定位说清楚了：不是只给职业程序员，而是给所有软件使用者。

中文读者可以从这里进入：1985 年的 Whole Earth 已经在谈“软件素养”，而不是单纯教 BASIC。它关心的是用户怎样摆脱黑箱。

## p.159 / leaf 160

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n160_w500.jpg

标题是 “Why Bother Learning to Program?” Peter A. McWilliams 先提出反方意见：教 BASIC 是早年个人电脑缺少现成软件时留下的习惯，现在未必必要。Weinberg 的回答很关键：用户只要把 word processor 或 spreadsheet 的使用步骤排成流程，其实已经在编程；问题不是要不要学，而是要不要学得好。

这一页把“编程”从语言层拉到程序化思维：如何把事情拆成合乎逻辑、有效率的步骤。Girish Parikh 又补上一层：写代码之前要先有设计，就像盖房子之前要有蓝图。Weinberg 因此说，对多数个人电脑用户来说，学习程序设计可能比学习某一种语言更有价值。

这一页应作为产品里的关键卡片：它把“编程是审美活动”的实际含义落到设计感、结构感和流程感，而不是把审美理解成装饰。

## p.160 / leaf 161

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n161_w500.jpg

这一页评 Brian Kernighan 与 P. J. Plauger 的 *The Elements of Programming Style*。推荐理由非常 Whole Earth：它不讲抽象原则，而是拿真实坏程序当例子，逐步改写，让读者看见“正确且可读”的程序如何形成。

这页真正谈的是“风格”而非语法。书里的格言如先求正确再求速度、不要耍聪明、选择能让程序变简单的数据表示，都把编程放在一种手艺伦理里：好程序不是炫技，而是清楚、可维护、可被别人理解。Dennis Geller 还指出，程序错误常常不是高深公式错了，而是最基础的疏忽，比如未初始化变量。

中文产品里不要把这页做成“推荐一本书”。更好的入口是“坏例子怎样训练审美”：Whole Earth 认为编程风格可以被训练，就像写作风格可以被 Strunk and White 训练。

## p.161 / leaf 162

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n162_w500.jpg

这一页进入 C 语言生态，密集列出 Aztec C、DeSmet C、Lattice C、Mac C、Megamax C、Objective-C、PLINK-86 等工具。John Seward 的判断是：C 与 Ada、COBOL、PL/I、Pascal、BASIC 不同，它没有明显的政府、IBM、大学或默认平台背书，却正在快速成为微机上的主流语言。

这页有两个可读点。第一，1985 年的 C 还不是“理所当然的标准”，而是在多个编译器、平台、价格和拷贝保护机制中竞争出来的。第二，Whole Earth 的评测方式非常市场化也非常反市场：它列价格、内存、平台、供应商和 copy-protected 状态，让读者自己判断工具是否值得信任。

中文读者看到这里，会明白“标准”并非自然出现，而是在工具链、社区、价格和可移植性之间形成。

## p.162 / leaf 163

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n163_w500.jpg

上半页评 Macintosh Pascal。David Taylor 喜欢它的即时性：打开磁盘后有 Program、Text、Drawing 三个窗口，可以改程序、马上运行、看输出和图形。错误提示用带 bug 图像的窗口，点击后回到出错行。这已经很接近后来 IDE 和可视化调试环境的体验。

但 Whole Earth 的评测不会只夸。它指出 Mac Pascal 不能处理超过 32K 的剪贴板文件、不能链接多个模块，而且有拷贝保护。那句“自尊的程序员不会使用 copy-protected program”其实是这一页的价值判断：工具不仅要好用，还要尊重使用者的控制权。

下半页转到 *Software Tools* 与 *Software Tools in Pascal*，强调工具会教好技术。这里把编程从语言变成环境：好工具不仅帮你完成任务，还塑造你怎样思考任务。

## p.163 / leaf 164

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n164_w500.jpg

这一页主要是 Apple Pascal 与 *Pascal From BASIC*。Thomas Mayer 的个人叙述很有现场感：他买 Apple 是为了学编程，长期失望和挫败，后来靠 Apple Pascal、几本好书和艰苦练习真正进入 Pascal，甚至靠编程挣钱。

这不是“Pascal 比 BASIC 高级”的简单叙事。页面解释 Pascal 为什么适合大型程序：块结构让程序可以分块分析和调试，可读性更好，移植性也比 BASIC 强。Linda Phillips 评 *Pascal From BASIC* 时说它不是教你逐句翻译，而是教 BASIC 使用者“用 Pascal 思考”。

这一页适合做成“从熟悉语言迁移到新思维”的案例。Whole Earth 关心的不是换语法，而是换一种组织复杂性的方式。

## p.164 / leaf 165

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n165_w500.jpg

这一页为 BASIC 辩护。MBASIC、TRS-80 BASIC、BASIC Compiler、CBASIC 被放在一起评。Darrell Fichtl 直接说 BASIC 是计算机行业里的 Chevy：普通、常见、能干活。所谓 BASIC 松散、不能写严肃程序，在他看来取决于写程序的人，不取决于语言本身。

Richard Muller 从实践角度解释解释型 BASIC 的价值：可以暂停程序、查看变量、甚至改变量再继续，这让开发过程很灵活；缺点是执行慢，所以再配合编译器生成最终产品。这里的判断非常实际，不为语言鄙视链服务。

这页之后还开始出现 Commodore/Atari 的加速和开发工具。中文产品里可把这页命名为“不要被语言鄙视链骗了”：Whole Earth 的标准是能否帮助人做出好东西。

## p.165 / leaf 166

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n166_w500.jpg

这一页先评 BetterBASIC：它像披着 BASIC 外衣的 C，支持递归、数组的数组、覆盖、块结构、窗口、本地和全局变量、结构和指针。推荐逻辑很清楚：如果你熟悉 BASIC，又想比较无痛地靠近 C 的能力，这个工具给你一座桥。

下半页讨论 Nevada COBOL。Sharon Rufener 的语气很值得保留：微机爱好者嘲笑 COBOL 老旧、不性感，但 COBOL 是世界上大量职业程序员的母语，也是招聘市场和既有应用的现实。她替 COBOL 辩护，不是因为它时髦，而是因为它可靠、可移植、可结构化。

这一页的产品入口可以是“语言不是身份，是场景”。C、BASIC、COBOL 在这里不是高低贵贱，而是不同用户、组织和工作条件下的工具。

## p.166 / leaf 167

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n167_w500.jpg

这一页主题是第二门语言。Weinberg 建议，如果已经学一门主流语言，第二门应该选 FORTH、APL、Smalltalk、Modula、LISP 或汇编这类“有点偏门”的语言，因为它们会用不同方式拉伸你的头脑。

页面下方是 FORTH 工具列表和屏幕图。FORTH 被呈现为紧凑、快速、可扩展的环境；中间穿插几句关于变化和软件的短句，让这页读起来不像教材，更像程序员文化的剪贴板。重点是：学第二语言不是为了多一项技能，而是为了改变看问题的方式。

中文读者可以把这页理解为 Whole Earth 式的“反单一范式”教育：真正的计算机素养来自跨范式的比较。

## p.167 / leaf 168

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n168_w500.jpg

这一页非常接近今天的 AI 线索。Micro-Prolog 被称为微机上的真实人工智能工具，背景是日本第五代计算机计划让 Prolog 成为热门词。Ernie Tello 解释 Prolog 是用于 AI 的专门工具，适合专家系统、智能数据库和自然语言处理。

但它没有被神化。页面说 Micro-Prolog 是给已经知道逻辑和逻辑编程是什么、也知道自己要做什么的人；它数学函数少、输入输出极简，是否能在 16 位微机和更大内存上做出惊喜仍是开放问题。

这一页最适合连到“1985 年的 AI 想象”：不是聊天机器人，而是逻辑、关系、递归、专家系统和语言处理。Whole Earth 的态度是兴奋但不盲目。

## p.168 / leaf 169

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n169_w500.jpg

这一页从语言转到操作环境。Tom Love 概括 UNIX 对程序员的三大优势：可移植、模块化，以及支持多用户沟通协作。Weinberg 说，过去硬件几乎决定操作系统，UNIX 改变了 portability 的含义；如果认真编程，UNIX 领先于其他环境，哪怕最终软件运行在别处。

页面还评 *UNIX Primer Plus* 和 *The UNIX Programming Environment*。前者适合入门，后者密度高、权威但需要 C 基础。随后出现 GEM，把 PC 变成类似 Macintosh 的图形桌面。这说明这一页同时在看两个未来：命令行的可组合环境，以及图形界面对普通用户的吸引力。

中文入口可以是“环境也是语言”：UNIX 的管道、过滤器、多用户协作不是外围设施，而会改变程序员如何想象软件。

## p.169 / leaf 170

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n170_w500.jpg

这一页进入结构化设计。*Designing Structured Programs* 用 Warnier-Orr 图表示程序结构，不只是靠缩进，而是用展开括号让层级“跳出来”。页面上的例子是买面包这种日常小事，借它说明简单任务也有多层步骤。

Dennis Geller 的 “A Design Library” 开始把编程明确说成复杂智力活动：20 行程序容易，100 行不是难五倍，而可能难二十五倍。设计的意义是在坐下来写代码前，先弄清楚程序想做什么。这里还把程序设计和建筑设计联系起来，并提到 Christopher Alexander 的 *Notes on the Synthesis of Form*。

这是“编程作为审美活动”的核心证据页之一：审美不是视觉装饰，而是结构是否站得住、是否和工作环境及使用者协调。

## p.170 / leaf 171

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n171_w500.jpg

这一页延续设计书单，推荐 Sally Campbell 的 *Microcomputer Software Design* 作为不想先学计算机科学的人的入口，并用洗澡/周六洗车的流程图展示基础控制结构。关键句不是图本身，而是“任何设计都比没有设计好”。

后半页回到 Weinberg 的“软件中的人”。Geller 推荐 *Rethinking Systems Analysis and Design*、*Understanding the Professional Programmer*，说这些书好读、有趣，但下面有更深的警告：如果我们不把事情做得更好，就会被自己的技术拖垮。Railroad Paradox 的例子说明系统常常用现有行为反证用户需求，结果错过真正的需求。

这一页适合提醒中文读者：Whole Earth 的软件观并不技术至上。它很早就把软件失败看成组织、观察和人类行为的问题。

## p.171 / leaf 172

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n172_w500.jpg

这一页标题是 Software Engineering。Weinberg 用几个系统法则引入：一切都会变化；增长会带来庞大；结构良好的小程序随时间会变成混乱的大系统。大型机用户已经用昂贵方式学过这课，微机用户有机会提前学习软件工程。

评 David Marca 的 *Applying Software Engineering Principles with FORTRAN* 时，Geller 看重的是它能把原则小规模地用于下一个项目，而不是假设读者读完就能全套照搬。技术和人的限制被混在一起讨论，编码例子虽是 FORTRAN，但思想可迁移。

这一页给中文产品的意义是：软件工程在这里不是企业流程，而是普通微机用户面对增长和变化的生存知识。

## p.172 / leaf 173

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n173_w500.jpg

Utilities 章从 James Stockford 的定义开始：utilities 是帮助电脑更好运行的小工具，像整理磁盘文件、修复磁盘失败、加速程序、找回删除文件、弥补操作系统笨拙。它们像厨房用具一样有用、多样，却常被忽视。

页面随后讲 COPY II PLUS / COPY II PC / COPY II MAC / COPY II 64。Kathy Parks 的例子很具体：她作为 Whole Earth Software Catalog 的资料管理员，误毁了 Apple Writer IIe 的主盘，靠 COPY II PLUS 救回。这不是抽象评测，而是灾难恢复现场。George Beekman 又补充 Mac 版本对拷贝保护问题的意义。

这页应做成“工具箱里的急救包”，因为它体现了 Whole Earth 的核心气质：工具的价值在事故发生时才真正显形。

## p.173 / leaf 174

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n174_w500.jpg

这一页继续 utilities：The Norton Utilities 用来修改操作系统信息、从磁盘崩溃中恢复；POWER! 则是隐藏操作系统复杂命令的 shell，让新手能格式化、复制、查看磁盘、恢复误删、隔离坏扇区、组织文件。页面还补充 Dr. Dobb's Journal 与 Whole Earth 的谱系关系：它来自同一 Portola Institute 生态。

这一页的好读角度是“把操作系统从咒语变成器具”。像 `PIP PUB:=b:[EFG2UV]` 这样的命令对普通人不可读，POWER! 的意义就是把这种不可读性包起来，让人重新获得操作感。

## p.174 / leaf 175

扫描图：https://archive.org/download/wholeearthsoftwa00unse_3/page/n175_w500.jpg

这一页讲 key-changers：PROKEY 与 SMARTKEY II。Art Kleiner 把它们定义为 customizing tools，可以把不同程序混乱的命令统一成一种语法，把复杂命令串压成一个按键，也可以插入常用文本。

Tony Fanning 的例子很像今天的软件可用性问题：他每天用两个程序，一个里 CONTROL-Y 恢复删除文本，另一个里 CONTROL-Y 删除当前行，于是反复误删。PROKEY 让他重定义 CONTROL-Y，让它在不同软件里表现一致。

这页非常适合中文用户，因为它讲的不是怀旧软件，而是“用户改造界面”。Whole Earth 在 1985 年已经关心默认软件行为怎样伤害肌肉记忆，以及用户如何用工具把环境调回自己能掌控的样子。

## 样板验收

这份样板必须满足四点，后续每本正式整理也按此验收：

1. 每一页都能回到扫描图和 leaf/page 编号，不再只靠刊名或目录猜测。
2. 每页至少说明“页面实际有什么”和“为什么对中文读者有意义”，避免重复模板话术。
3. 能识别页面之间的章节逻辑，而不是把每页拆成孤立书摘。
4. 对未读完范围明确标注，不把局部样板包装成全书完成。
