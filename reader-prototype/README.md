# 1974 Epilog 对照阅读器

「中文精读本」的对外展示入口：左侧原书扫描页，右侧章节译写正文，滚动时两边保持对照。

当前入口：`reader-prototype/index.html`。部署为静态站点时，可直接指向 `/reader-prototype/index.html`。

## 数据来源（只读）

构建脚本从仓库内读取两份成品稿，不修改源稿：

- `../content/readings/1974_whole_earth_epilog_chapter_translation_zh.md`（章节译写正文）
- `../content/readings/1974_whole_earth_epilog_reader_chinese.md`（导读作序）

暗线数据（七条暗线、章节在各暗线下的解读）取自主仓库 `content/maps/1974_epilog_access_atlas.html` 中的编辑成果，以静态形式内嵌在 `build_data.py` 里。

扫描图直接从 Internet Archive 加载：`https://archive.org/download/wholeearthepilog00unse/page/n{leaf}_w500.jpg`，本地不缓存图片。

## 构建与运行

```bash
python3 build_data.py          # 重新生成 data/epilog_reader.json
python3 -m http.server 8901 -d ..   # 从仓库根目录起服务
# 打开 http://localhost:8901/reader-prototype/index.html
```

`index.html` 通过 fetch 读取 JSON，必须走 HTTP，不能直接双击打开文件。

## 功能

- 序（导读）+ 12 章 121 节译写正文，单页连续阅读
- 左侧扫描页随正文滚动自动切换；可用滑杆/按钮手动翻 322 个 leaf；每页有 Archive 原页链接
- 每节标注 `≈ leaf / 印刷页`，点「看这一页」跳到对应扫描
- 「暗线视图」：七条暗线（找入口、看尺度、会维护、用身体学、组织社会、穿越风险、出版成工具），每条列出成员章节及该暗线下的解读，可跳转；导航栏高亮成员章节
- 底部进度条按 leaf 计
- 窄屏时扫描页收成顶部固定小卡片

## leaf / 印刷页映射（2026-07-06 实证核对）

对 leaf 5、9、60、150、250 五个采样点逐张目检确认：

- **印刷页号 = leaf + 449**（如 leaf 9 = p.458，leaf 60 = p.509，leaf 150 = p.599，leaf 250 = p.699）。
- **leaf 0 是真正的封面**（阿波罗照片 + access to tools + 价格）。
- **leaf 321 是封底**（`Stay hungry. Stay foolish.` + ISBN）；**leaf 322 是扫描仪校准页（"Test Shot"），不是书的内容**，阅读器不收录。
- 早期主仓库 1974 工作稿曾按 `leaf + 447` 推算，系统性偏小 2；且"封底在 leaf 322、leaf 321 是制作痕迹"的说法与实际相反（疑为 1 起数的 PDF 页码对 0 起数的 Archive leaf 造成的错位）。当前阅读器和主仓库文档已按实证结果修正。

## 已知近似与待决

- **条目级 leaf 对齐是线性插值的近似**（章节 leaf 范围来自页级证据稿）。要做到条目级精确对齐，需要在译写稿或页级 dossier 里为每个 `###` 条目补一个 leaf 锚点。
- issue-agent 问答未接入（主仓库 `scripts/serve_issue_agent.py` 已具备，接入只需换用该服务并加一个聊天组件）。
- 小黑猫章节扉页插画未接入（xiaohei worktree 的成品图可作为每章开头的分隔页）。

## 文件

- `build_data.py` — 解析译稿生成阅读器数据
- `data/epilog_reader.json` — 生成物（约 250KB）
- `index.html` — 阅读器本体（无依赖、无构建工具）
