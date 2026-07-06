# 全球概览中文精读文库 / Whole Earth Chinese Close-Reading Library

把 Whole Earth 系列出版物（Whole Earth Catalog / Epilog / Software Catalog / CoEvolution Quarterly 等）做成中文读者可以真正读进去的精读本。工作基于 `wholeearth.info` 与 Internet Archive 扫描，以 OCR、页级证据和扫描图链接为编辑底线：不靠标题和目录猜内容。

## 产品定义

一期的产品是**一部中文精读本**，由两层组成：

1. **导读作序**：这期是什么、为什么值得读、怎么读。面向读者的完整叙述，不带内部工作语言。
2. **章节译写正文**：按原书顺序，保留"条目—判断—摘录"的肌理，把原书转成可连续阅读的中文。这是精读本的主体。对失效地址、旧价格和重复出版信息做压缩处理。

**证据层是内部基础设施，不是读者产品**：页级证据稿、编辑结构稿、书目审计、147 期 dossier 都属于工作台。它们支撑精读本的可信度（每一处判断可回溯到 leaf / 印刷页 / 扫描图），但不和成品混同展示。

明确不做的：

- 不承诺 147 期全集覆盖。一年做几期，看兴趣和精力。
- 不做逐字对照的全文翻译档案。译写以可读性和忠实肌理为准，不是 diplomatic edition。
- 质量线以 1974 Epilog 章节译写版为基准；自用即发布，不为发布降低标准。

## 每期完成标准

一期精读本视为完成，需要全部满足：

1. 导读作序完成，无模板化章节节奏，无内部选题/生产语言。
2. 章节译写正文覆盖原书全部章节结构（含前置页、出版机制、索引、封底）。
3. 通过三项 QA：章节覆盖检查、重复模板语言检查、过度声称检查。
4. **成稿校对一遍**：半翻译残留（如"夜shade"）、专名拼写、页码/leaf 引用抽查。
5. 页级证据稿在工作台中可回溯，OCR/版面高风险页有标注。

## 发布分层

- **自用与私下分享**：精读本全部内容。
- **公开发布**：导读作序可全文公开；章节译写正文接近整书译写，原书版权仍然有效（Point Foundation 等），公开时需收缩为"精编+评述"形态或节选。公开任何一期之前先按此分层裁剪，不直接把译写正文全文公开。

## 文库现状

### 精读本（导读 + 章节译写齐备）

- **Whole Earth Epilog, October 1974**
  - 导读作序：`content/readings/1974_whole_earth_epilog_reader_chinese.md`
  - 章节译写正文：`content/readings/1974_whole_earth_epilog_chapter_translation_zh.md`
  - 阅读入口：`reader-prototype/index.html`（当前最适合对外展示的对照阅读器）
  - 覆盖：前置页、Whole Systems、Land Use、Shelter、Soft Technology、Craft、Community、Nomadics、Communications、Learning、出版机制、索引、封底
  - QA：内容页按 Archive leaf 0-321 读取；正文印刷页号按 `leaf + 449` 映射；封底 `Stay hungry. Stay foolish.` 于 leaf 321 扫描确认，leaf 322 为扫描校准页；书目审计 216 条（140 条确认可用链接，76 条明确不链）
  - 待办：成稿校对一遍（已知残留：导读稿"夜shade"、"Epiog"）

### 导读本（仅导读层，无译写正文）

- **Whole Earth Software Catalog 2.0, Fall 1985**
  - 全书导读：`content/readings/1985_software_catalog_full_chinese_reading.md`
  - 页级导读：`content/readings/1985_software_catalog_page_level_chinese_reading.md`
  - QA：17/17 章节覆盖；leaf 0-227 页级覆盖
  - 按新产品定义，本期为导读本。是否升格为精读本（补章节译写正文）另行决定。

### 证据基础设施（工作台，非成品）

- 147 期 issue 全部有页级 dossier，合计 22,162 页；覆盖 QA 147/147 通过。
- dossier 是选题和证据基础，不作为"已完成阅读"呈现。

### 内部工作稿（当前仍在 `content/readings/` 内，待归位）

以下文件是编辑工作台产物，不是读者成品，计划迁出读者目录（迁移方案见下节）：

- `content/readings/1974_whole_earth_epilog_chinese_reading.md`（编辑结构稿）
- `content/readings/1974_whole_earth_epilog_page_level_chinese_reading.md`（页级证据工作台）
- `content/readings/1974_whole_earth_epilog_bibliography_links.md`（书目/链接审计）

### 实验归档（非产品方向）

知识地图、科幻控制台 demo、issue-agent 问答（`content/maps/`、`content/demos/`、`data/issue_agents/`、`scripts/serve_issue_agent.py`）为读期过程中的衍生实验，保留但不承担产品承诺。

## 目录规划（拟议，文件尚未搬移）

目标：读者成品与工作台分离。

```text
content/
  books/                      # 读者成品：每期一个目录
    1974_whole_earth_epilog/
      00_reader_preface.md    # 导读作序
      01_chapter_translation.md  # 章节译写正文
  workbench/                  # 内部工作台：结构稿、页级证据稿、书目审计
```

搬移前保持现状；本节仅为方向声明。

## 现有目录结构

- `scripts/`：issue 级与页级证据抽取脚本。
- `data/issue_index.json`：147 期索引元数据。
- `data/evidence_dossiers/`：issue 级 OCR 证据 dossier。
- `data/issue_agents/`：单期知识 bundle（实验）。
- `data/bibliography/`：书目审计数据。
- `content/readings/`：当前的成品与工作稿混合目录（见上节归位计划）。
- `content/samples/`：页级阅读样本（1985 Programming 章，历史基准）。
- `content/notes/`：明确标注的 legacy 过渡笔记，不作公开文案。
- `reader-prototype/`：1974 Epilog 对照阅读器，当前的读者展示入口。
- `assets/`：读稿引用的小型扫描/图片资产。
- `_local/`：不入库的本地缓存、PDF 源、日志与历史实验。

## Git 范围

跟踪：抽取/生成脚本、issue 级证据 dossier、精读本与导读本成品、小型扫描资产。

忽略：页级 OCR/XML 缓存、页级 dossier 全量输出、运行日志、QA 截图、`_local/` 全部内容。大文件均可从 Internet Archive 重建。

## 关键脚本

- `scripts/extract_wholeearth_evidence.py`：构建 issue 级 OCR 证据 dossier。
- `scripts/extract_issue_pages.py`：为单个 Internet Archive identifier 构建页级 dossier（输出 `_local/page_dossiers/`）。
- `scripts/extract_all_issue_pages.py`：为全部 147 期构建页级 dossier。
- `scripts/build_epilog_agent_bundle.py` / `build_epilog_web_agent_data.py` / `query_issue_agent_bundle.py` / `serve_issue_agent.py`：issue-agent 实验线（非产品承诺）。

## 每期工作流

1. 选期：从 147 期 dossier 里挑当下最想读的一期。
2. 建工作台：页级 dossier + 扫描链接 + 结构稿。
3. 写章节译写正文：逐章回到扫描页，保留条目—判断—摘录肌理。
4. 写导读作序。
5. 过完成标准五项（含成稿校对）。
6. 录入文库现状，标注精读本/导读本身份。
