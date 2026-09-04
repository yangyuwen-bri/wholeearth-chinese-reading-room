# 全球概览中文阅读室

**语言：** [English](README.md) | 简体中文

[![线上站点](https://img.shields.io/badge/live_site-GitHub_Pages-2f6f63?style=flat-square)](https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/)
[![静态站点](https://img.shields.io/badge/site-static_HTML%2FCSS%2FJS-6b7280?style=flat-square)](#本地运行)
[![已索引期数](https://img.shields.io/badge/issues_indexed-147-3b6ea8?style=flat-square)](#当前状态)
[![开放阅读室](https://img.shields.io/badge/open_reading_rooms-6-b17a2c?style=flat-square)](#重点入口)
[![视觉小册子](https://img.shields.io/badge/visual_booklets-1-7c4d9e?style=flat-square)](#重点入口)
[![许可证](https://img.shields.io/badge/license-not_declared-lightgrey?style=flat-square)](#许可与权利说明)

**全球概览中文阅读室** 是一个面向中文读者的 Whole Earth 系列阅读项目，覆盖 *Whole Earth Catalog*、*Whole Earth Epilog*、*CoEvolution Quarterly*、*Whole Earth Software Catalog* 与 *Whole Earth Review*。

这个项目把每一期出版物当作一个经过编辑的阅读对象处理。成熟内容会把原书扫描页、中文导读、章节结构、页码锚点和核查材料连接在一起。它不是批量 OCR 仓库。

**线上站点：** <https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/>

## 重点入口

<table>
  <tr>
    <td width="12%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/reader-prototype/index.html?issue=march-1971-last-supplement"><strong>1971 年 3 月《最后一期〈全球概览〉增刊》中文阅读室</strong></a><br>
      已提供 132 页中文译稿与原扫描对照，原文忠实性重新复核中。原书第 34 页尚不完整：已撤下无逐字证据的旧译，并标明剩余缺口；历史 accepted 标签不代表无遗漏。
    </td>
    <td width="12%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/reader-prototype/index.html?issue=january-1971"><strong>1971 年 1 月《全球概览》对照阅读室</strong></a><br>
      48 个扫描叶全部完成忠实全文翻译、原始高清扫描复核和独立审校；文章、书信、图注、表单、图示、价格、地址与完整订户名录均按原页保留。
    </td>
    <td width="12%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/reader-prototype/index.html?issue=fall-1970"><strong>1970 秋季《全球概览》对照阅读室</strong></a><br>
      148 个扫描叶全部完成忠实全文翻译、高清复核和独立审校，所有可辨识段落、图注、表格、规格、价格、型号与地址均按原页保留。
    </td>
    <td width="12%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/reader-prototype/index.html?issue=spring-1970"><strong>1970 春季《全球概览》对照阅读室</strong></a><br>
      148 个扫描叶全部完成忠实全文翻译、高清复核和独立审校，保留可辨识的图注、表格、规格、价格与地址。
    </td>
    <td width="12%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/reader-prototype/index.html?issue=fall-1969"><strong>1969 秋季《全球概览》对照阅读室</strong></a><br>
      132 个扫描叶全部完成全文翻译和逐页复核，中文正文与 Internet Archive 原书扫描同步。
    </td>
    <td width="12%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/reader-prototype/index.html"><strong>1974 Epilog 对照阅读室</strong></a><br>
      <em>Whole Earth Epilog</em> 的中文精读本，正文与 Internet Archive 原书扫描页同步滚动。
    </td>
    <td width="12%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/content/visuals/1974-epilog-booklet/"><strong>1974 Epilog 视觉小册子</strong></a><br>
      基于完整中文章稿制作的章节插画小册子，按 10 个章节进入。
    </td>
    <td width="12%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/content/demos/wholeearth_webgl_console_demo.html"><strong>WebGL 文库首页</strong></a><br>
      147 期 Whole Earth 出版物的视觉索引，展示每一期的阅读状态和入口。
    </td>
    <td width="12%">
      <a href="content/readings/1985_software_catalog_full_chinese_reading.md"><strong>1985 Software Catalog 中文导读</strong></a><br>
      <em>Whole Earth Software Catalog 2.0</em> 的完整中文导读，后续可整理成独立阅读室。
    </td>
  </tr>
</table>

## 编辑模型

仓库把公开阅读材料和研究工作台分开。

| 层级 | 用途 | 当前例子 |
| --- | --- | --- |
| 阅读室 | 面向读者的公开界面，保留原书扫描页上下文 | `reader-prototype/index.html` |
| 翻译包 | 逐叶源文证据、完整中文译文、审校记录与 QA 状态 | `content/translations/` |
| 导读与地图 | 单期导读、主题地图、可视化阅读索引 | `content/readings/`、`content/maps/` |
| 工作台 | OCR dossier、页级证据、锚点核查、检索包 | `data/evidence_dossiers/`、`data/issue_agents/` |

从工作台进入阅读室需要人工整理和编辑。近期目标是先做好少量高质量中文阅读室，而不是自动覆盖所有扫描期刊。

## 当前状态

| 项目 | 状态 |
| --- | --- |
| 公开首页 | WebGL 文库控制台，已部署到 GitHub Pages |
| 已开放阅读室 | *Whole Earth Catalog*：1969 年秋季号、1970 年春季号、1970 年秋季号、1971 年 1 月号、1971 年 3 月《最后一期增刊》；1974 年 10 月 *Whole Earth Epilog* |
| 已验收完整翻译包 | *Whole Earth Catalog*：1968 年秋季号（68/68 页）、1969 年春季号（134/134 页）、1969 年秋季号（132/132 页）、1970 年春季号（148/148 页）、1970 年秋季号（148/148 页）、1971 年 1 月号（48/48 页） |
| 当前校订 | 1971 年 3 月 *The Last Supplement to The Whole Earth Catalog*：132 页译稿导出核验；本轮累计 17 页校订完成，leaf 008/011/035 撤回验收并标明源文缺口，另 112 页待重新对照原文 |
| 已并入 `main`、待 Pages 发布的阅读器 | *Whole Earth Catalog* 1968 年秋季号、1969 年春季号 |
| 视觉小册子 | *Whole Earth Epilog*, 1974 章节小册子 |
| 已完成中文导读 | *Whole Earth Software Catalog 2.0*, 1985 年秋 |
| 已索引出版物 | 147 期 |
| 页级 OCR dossier | 22,162 页 |
| 覆盖率 QA | 147/147 期已覆盖 |
| 1974 Epilog 页码映射 | Archive leaf 0-321；正文印刷页使用 `printed page = leaf + 449` |

## 仓库结构

```text
content/
  assets/          # 封面缩略图、地球纹理和视觉素材
  data/            # 公开文库首页使用的出版物元数据
  demos/           # WebGL 和视觉导航原型
  maps/            # 单期地图和可视化阅读指南
  readings/        # 中文导读和精读草稿
  samples/         # 早期页级阅读样例
  vendor/          # 静态浏览器依赖
  visuals/         # 独立插画小册子和视觉导读
  translations/    # 逐叶译文、审校、状态和 QA 记录

data/
  evidence_dossiers/  # 单期 OCR 证据材料
  issue_agents/       # 实验性单期检索包
  issue_index.json    # 147 期索引

reader-prototype/
  index.html          # 已发布期刊共用的扫描对照阅读室
  1968/, 1969/        # 已验收、待发布的单期阅读器
  data/               # 1969 秋、1970 春秋、1971 年 1 月与 3 月、Epilog 阅读器数据

scripts/
  *.py                # 抽取、核查和实验性检索脚本
```

`_local/` 被故意排除在仓库之外。它只用于本地缓存、源 PDF、日志、QA 截图和不应公开发布的材料。

## 本地运行

阅读室和 WebGL 首页会加载 JSON 与浏览器模块，所以必须通过 HTTP 访问，不能直接双击 HTML 文件。

从仓库根目录运行：

```bash
python3 -m http.server 8911
```

然后打开：

```text
http://127.0.0.1:8911/
```

常用本地入口：

- `reader-prototype/index.html`
- `reader-prototype/index.html?issue=march-1971-last-supplement`
- `reader-prototype/index.html?issue=january-1971`
- `reader-prototype/index.html?issue=fall-1970`
- `reader-prototype/index.html?issue=spring-1970`
- `content/visuals/1974-epilog-booklet/index.html`
- `content/demos/wholeearth_webgl_console_demo.html`
- `content/maps/wholeearth_macro_atlas.html`

## 部署

当前公开站点使用 GitHub Pages，从 `gh-pages` 分支发布。

这个仓库本质上是静态站点，后续可以迁移到 Cloudflare Pages，不需要改动公开阅读器架构。只有实验性的 issue-agent 层需要保护服务端 API key 时，才需要加入 Worker 或 Pages Function。

## 路线图

- 稳定 WebGL 控制台，把它作为文库首页。
- 完成 Pages 集成检查后，发布已验收的 1968 年秋季号和 1969 年春季号阅读器。
- 将完成的阅读室迁移到稳定的 `/readers/<issue>/` URL 结构。
- 把更多中文导读推进成可对照扫描页的完整阅读室。
- 将公开页面和工作台 dossier、本地 QA 材料分开。
- 加入单期状态元数据，避免首页硬编码出版物入口。

## 许可与权利说明

仓库目前还没有声明正式开源许可证。在加入 `LICENSE` 文件之前，请把本仓库中的代码、数据和编辑文本视为尚未授权复用。

Whole Earth 原始出版物、扫描图、封面和出版物元数据仍受各自权利方约束。本项目尽量链接回原始扫描来源，并将材料用于教育性评论、阅读导航和研究核查。
