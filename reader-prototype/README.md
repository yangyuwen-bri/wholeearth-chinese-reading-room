# Whole Earth 中文对照阅读室

阅读器采用左侧原书扫描页、右侧中文译文的对照结构，滚动时两边保持同步。

共用公开入口是 `reader-prototype/index.html`，当前承载 1969 年秋季号、
1970 年春季号、1970 年秋季号和 1974 年 *Whole Earth Epilog*。1968 年秋季号与 1969 年春季号
的完整译稿和独立阅读器已并入 `main`，分别位于 `reader-prototype/1968/`、
`1969/`；两者仍需经过 Pages 集成检查后才算公开发布。

## 集成状态

| 出版物 | 翻译状态 | 阅读器状态 |
| --- | --- | --- |
| 1968 年秋季《全球概览》 | 68/68 页 accepted | 已并入 `main`，待发布 |
| 1969 年春季《全球概览》 | 134/134 页 accepted | 已并入 `main`，待发布 |
| 1969 年秋季《全球概览》 | 132/132 页 accepted | 已公开 |
| 1970 年春季《全球概览》 | 148/148 页 accepted | 已公开 |
| 1970 年秋季《全球概览》 | 148/148 页 accepted | 已公开 |
| 1974 *Whole Earth Epilog* | 283 页 accepted、25 页待高清复核、14 页无需翻译 | 已公开，QA 状态继续保留 |

## 内容原则

中文阅读室的正文来源是 leaf 级忠实译稿，不再使用早期概括性精读稿。

生产正文应当：

- 基于原书 OCR 与扫描页核对后的 `Final Translation`；
- 保留原书中的评论、摘录、标题、署名、图注和论证节奏；
- 完整保留可辨识的价格、订购地址、库存编号、索引和其他交易信息；
- 把章节导读、现代目录、原书目录页折叠区作为阅读辅助层，而不是把工作流说明展示给读者。

早期概括性精读稿不再作为阅读室生产内容来源。

## 数据来源

共用 Epilog 构建脚本读取：

- `../content/translations/wholeearthepilog00unse/status.jsonl`
- `../content/translations/wholeearthepilog00unse/leaves/leaf_###.md`

每个 leaf 只抽取 `## Final Translation`。`Source Pack`、`Context Notes`、`OCR / Uncertainty Notes`、`Self Critique`、review 文件等只用于翻译和审核，不进入读者正文。

1968、1969 春季、1969 秋季、1970 春季和 1970 秋季号分别从对应的
`content/translations/<issue_id>/` 包读取相同的 `Final Translation` 区段。

扫描图直接从 Internet Archive 加载：

`https://archive.org/download/wholeearthepilog00unse/page/n{leaf}_w500.jpg`

本地不缓存图片。

## 构建与运行

```bash
python3 reader-prototype/1968/build_reader_data.py
python3 reader-prototype/1969/build_reader_data.py
python3 reader-prototype/build_fall_1969_reader_data.py
python3 reader-prototype/build_spring_1970_reader_data.py
python3 reader-prototype/build_fall_1970_reader_data.py
cd reader-prototype
python3 build_translation_reader_data.py
cd ..
python3 -m http.server 8911
# 打开 http://127.0.0.1:8911/reader-prototype/index.html?issue=fall-1970
```

`index.html` 通过 fetch 读取 JSON，必须走 HTTP，不能直接双击打开文件。

`build_data.py` 仅作为兼容入口保留，会调用同一个 leaf 级构建流程：

```bash
python3 build_data.py
```

## 功能

- 按期刊章节组织 leaf 级完整译稿，支持连续阅读
- 每章有读者导读
- 每章有默认折叠的现代目录，展开后占据正文空间，可点击跳转条目
- 原书目录页默认隐藏在“查看原书目录页”折叠区
- 左侧扫描页随正文滚动自动切换；可用滑杆/按钮手动翻页；每页有 Archive 原页链接
- 每个条目标注原书印刷页，点“看原页”跳到对应扫描
- Epilog 提供七条“暗线视图”；其他期刊使用标准章节视图
- 底部进度条按 leaf 计
- 窄屏时扫描页收成顶部固定小卡片

## 1974 Epilog leaf / 印刷页映射

- leaf 0 是封面，不标正文印刷页。
- leaf 1 是《约伯记》引文内封页，不标正文印刷页。
- leaf 2 = p.450。
- leaf 3-319 按 `leaf + 449` 映射，例如 leaf 4 = p.453，leaf 142 = p.591。
- leaf 320-321 是封底相关页，不标正文印刷页。
- Archive 内容范围只收 leaf 0-321，leaf 322 是扫描校准页，不属于书。

## 当前 QA 状态

各期 `content/translations/<issue_id>/status.jsonl` 是对应翻译状态的唯一来源。

当前生成数据保留 QA 元数据，但普通读者界面不直接展示内部状态。状态含义：

- `accepted`：译文已通过当前复核。
- `needs_highres_scan`：正文已翻译，但图表、小字、手写标注或技术标签仍需高分辨率扫描复核。
- `no_translation_needed`：封面、索引、订单或非连续正文材料。

## 文件

- `build_translation_reader_data.py` — 从 leaf 级完整译稿生成阅读器数据
- `build_spring_1970_reader_data.py` — 生成 1970 年春季号阅读器数据
- `build_fall_1970_reader_data.py` — 生成 1970 年秋季号阅读器数据
- `data/epilog_reader.json` — 生产阅读器数据
- `data/spring_1970_reader.json` — 1970 年春季号生产阅读器数据
- `data/fall_1970_reader.json` — 1970 年秋季号生产阅读器数据
- `index.html` — 阅读器本体（无依赖、无构建工具）
- `build_data.py` — 兼容入口，调用当前 leaf 级构建器

## 后续杂志复用规则

后续 Whole Earth 杂志也按同一逻辑建立中文内容：

1. 先建立 leaf 级翻译目录：`content/translations/{issue_id}/`。
2. 每页译稿分离工作流信息和 `Final Translation`。
3. 阅读室只读取 `Final Translation`。
4. 章节导读、现代目录、原书目录折叠区由构建脚本生成。
5. 旧式概括性精读稿不能作为生产正文来源。
