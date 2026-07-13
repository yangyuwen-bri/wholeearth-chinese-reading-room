# 1974 Epilog 中文阅读室

对外展示入口：左侧原书扫描页，右侧中文译文，滚动时两边保持对照。

当前入口：`reader-prototype/index.html`。部署为静态站点时，可直接指向 `/reader-prototype/index.html`。

## 内容原则

中文阅读室的正文来源是 leaf 级忠实译稿，不再使用早期概括性精读稿。

生产正文应当：

- 基于原书 OCR 与扫描页核对后的 `Final Translation`；
- 保留原书中的评论、摘录、标题、署名、图注和论证节奏；
- 压缩或省略价格、订购地址、库存编号等低价值交易信息；
- 把章节导读、现代目录、原书目录页折叠区作为阅读辅助层，而不是把工作流说明展示给读者。

早期 `content/readings/1974_whole_earth_epilog_chapter_translation_zh.md` 属于 legacy 概括稿，不再作为阅读室生产内容来源。

## 数据来源

主构建脚本读取：

- `../content/translations/wholeearthepilog00unse/status.jsonl`
- `../content/translations/wholeearthepilog00unse/leaves/leaf_###.md`

每个 leaf 只抽取 `## Final Translation`。`Source Pack`、`Context Notes`、`OCR / Uncertainty Notes`、`Self Critique`、review 文件等只用于翻译和审核，不进入读者正文。

扫描图直接从 Internet Archive 加载：

`https://archive.org/download/wholeearthepilog00unse/page/n{leaf}_w500.jpg`

本地不缓存图片。

## 构建与运行

```bash
cd reader-prototype
python3 build_translation_reader_data.py
cd ..
python3 -m http.server 8911
# 打开 http://127.0.0.1:8911/reader-prototype/index.html
```

`index.html` 通过 fetch 读取 JSON，必须走 HTTP，不能直接双击打开文件。

`build_data.py` 是旧概括稿构建器，默认已禁用。只有做历史对照时才使用：

```bash
python3 build_data.py --legacy
```

## 功能

- 导读 + 11 个原书内容章节，按 leaf 级完整译稿连续阅读
- 每章有读者导读
- 每章有默认折叠的现代目录，展开后占据正文空间，可点击跳转条目
- 原书目录页默认隐藏在“查看原书目录页”折叠区
- 左侧扫描页随正文滚动自动切换；可用滑杆/按钮手动翻 322 个 leaf；每页有 Archive 原页链接
- 每个条目标注原书印刷页，点“看原页”跳到对应扫描
- “暗线视图”：七条暗线（找入口、看尺度、会维护、用身体学、组织社会、穿越风险、出版成工具），可跳转成员章节
- 底部进度条按 leaf 计
- 窄屏时扫描页收成顶部固定小卡片

## leaf / 印刷页映射

- leaf 0 是封面，不标正文印刷页。
- leaf 1 是《约伯记》引文内封页，不标正文印刷页。
- leaf 2 = p.450。
- leaf 3-319 按 `leaf + 449` 映射，例如 leaf 4 = p.453，leaf 142 = p.591。
- leaf 320-321 是封底相关页，不标正文印刷页。
- Archive 内容范围只收 leaf 0-321，leaf 322 是扫描校准页，不属于书。

## 当前 QA 状态

`content/translations/wholeearthepilog00unse/status.jsonl` 是翻译状态来源。

当前生成数据保留 QA 元数据，但普通读者界面不直接展示内部状态。状态含义：

- `accepted`：译文已通过当前复核。
- `needs_highres_scan`：正文已翻译，但图表、小字、手写标注或技术标签仍需高分辨率扫描复核。
- `no_translation_needed`：封面、索引、订单或非连续正文材料。

## 文件

- `build_translation_reader_data.py` — 从 leaf 级完整译稿生成阅读器数据
- `data/epilog_reader.json` — 生产阅读器数据
- `index.html` — 阅读器本体（无依赖、无构建工具）
- `build_data.py` — legacy 概括稿构建器，默认禁用

## 后续杂志复用规则

后续 Whole Earth 杂志也按同一逻辑建立中文内容：

1. 先建立 leaf 级翻译目录：`content/translations/{issue_id}/`。
2. 每页译稿分离工作流信息和 `Final Translation`。
3. 阅读室只读取 `Final Translation`。
4. 章节导读、现代目录、原书目录折叠区由构建脚本生成。
5. 旧式概括性精读稿不能作为生产正文来源。
