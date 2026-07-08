# 全球概览中文阅读室

**语言：** [English](README.md) | 简体中文

[![线上站点](https://img.shields.io/badge/live_site-GitHub_Pages-2f6f63?style=flat-square)](https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/)
[![静态站点](https://img.shields.io/badge/site-static_HTML%2FCSS%2FJS-6b7280?style=flat-square)](#本地运行)
[![已索引期数](https://img.shields.io/badge/issues_indexed-147-3b6ea8?style=flat-square)](#当前状态)
[![开放阅读室](https://img.shields.io/badge/open_reading_rooms-1-b17a2c?style=flat-square)](#重点入口)
[![许可证](https://img.shields.io/badge/license-not_declared-lightgrey?style=flat-square)](#许可与权利说明)

**全球概览中文阅读室** 是一个面向中文读者的 Whole Earth 系列阅读项目，覆盖 *Whole Earth Catalog*、*Whole Earth Epilog*、*CoEvolution Quarterly*、*Whole Earth Software Catalog* 与 *Whole Earth Review*。

这个项目把每一期出版物当作一个经过编辑的阅读对象处理。成熟内容会把原书扫描页、中文导读、章节结构、页码锚点和核查材料连接在一起。它不是批量 OCR 仓库。

**线上站点：** <https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/>

## 重点入口

<table>
  <tr>
    <td width="33%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/reader-prototype/index.html"><strong>1974 Epilog 对照阅读室</strong></a><br>
      <em>Whole Earth Epilog</em> 的中文精读本，正文与 Internet Archive 原书扫描页同步滚动。
    </td>
    <td width="33%">
      <a href="https://yangyuwen-bri.github.io/wholeearth-chinese-reading-room/content/demos/wholeearth_webgl_console_demo.html"><strong>WebGL 文库首页</strong></a><br>
      147 期 Whole Earth 出版物的视觉索引，展示每一期的阅读状态和入口。
    </td>
    <td width="33%">
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
| 导读与地图 | 单期导读、主题地图、可视化阅读索引 | `content/readings/`、`content/maps/` |
| 工作台 | OCR dossier、页级证据、锚点核查、检索包 | `data/evidence_dossiers/`、`data/issue_agents/` |

从工作台进入阅读室需要人工整理和编辑。近期目标是先做好少量高质量中文阅读室，而不是自动覆盖所有扫描期刊。

## 当前状态

| 项目 | 状态 |
| --- | --- |
| 公开首页 | WebGL 文库控制台，已部署到 GitHub Pages |
| 已开放阅读室 | *Whole Earth Epilog*, 1974 年 10 月 |
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

data/
  evidence_dossiers/  # 单期 OCR 证据材料
  issue_agents/       # 实验性单期检索包
  issue_index.json    # 147 期索引

reader-prototype/
  index.html          # 1974 Epilog 对照阅读室
  data/               # 生成的阅读器 JSON 和锚点核查数据

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
- `content/demos/wholeearth_webgl_console_demo.html`
- `content/maps/wholeearth_macro_atlas.html`

## 部署

当前公开站点使用 GitHub Pages，从 `gh-pages` 分支发布。

这个仓库本质上是静态站点，后续可以迁移到 Cloudflare Pages，不需要改动公开阅读器架构。只有实验性的 issue-agent 层需要保护服务端 API key 时，才需要加入 Worker 或 Pages Function。

## 路线图

- 稳定 WebGL 控制台，把它作为文库首页。
- 将完成的阅读室迁移到稳定的 `/readers/<issue>/` URL 结构。
- 把更多中文导读推进成可对照扫描页的完整阅读室。
- 将公开页面和工作台 dossier、本地 QA 材料分开。
- 加入单期状态元数据，避免首页硬编码出版物入口。

## 许可与权利说明

仓库目前还没有声明正式开源许可证。在加入 `LICENSE` 文件之前，请把本仓库中的代码、数据和编辑文本视为尚未授权复用。

Whole Earth 原始出版物、扫描图、封面和出版物元数据仍受各自权利方约束。本项目尽量链接回原始扫描来源，并将材料用于教育性评论、阅读导航和研究核查。
