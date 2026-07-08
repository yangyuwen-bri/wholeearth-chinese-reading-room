#!/usr/bin/env python3
"""Build deep, issue-specific 1985 HTML knowledge maps.

This generator intentionally follows the single Software Catalog map architecture:
theme rail, mode filters, node network, timeline, and an inspector panel.
For WER issues, nodes are extracted from the issue-specific local reading drafts,
so each issue gets its own structure rather than a fixed template.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "content" / "maps" / "1985"
OLD_SOFTWARE = ROOT / "content" / "maps" / "1985_software_catalog_knowledge_map.html"
PANEL_COPY_PATH = ROOT / "content" / "maps" / "1985_panel_copy.json"

ISSUES = [
    {
        "id": "wholeearthreview00unse",
        "short": "Jan",
        "label": "No. 44",
        "title": "Whole Earth Review, January 1985",
        "pages": 108,
        "words": 54114,
        "flagged": "31 / 108",
        "accent": "#d35f45",
        "scanBase": "https://archive.org/download/wholeearthreview00unse/page/n{leaf}_w500.jpg",
        "source": "_local/reading_sources/wholeearthreview00unse/map_content_draft.md",
        "sections": ["建议的地图结构", "全期结构草案"],
        "center": "注意力",
        "subtitle": "电脑时代免疫手册",
        "timeline": ["沉浸", "怀疑", "信息神话", "办公室", "隐私", "软件", "读者网络"],
        "themes": [
            ("attention", "注意力陷阱", "电脑先改变沉浸、速度和审美判断。"),
            ("power", "技术神话", "信息更多不自动等于知识、民主或自由。"),
            ("labor", "劳动空间", "办公室、家庭和远程工作被电脑重新排布。"),
            ("privacy", "数据画像", "公开行为被拼成私人轮廓和治理能力。"),
            ("culture", "未来想象", "小说、寓言和书评测试技术神话。"),
            ("platform", "软件目录", "批判之后仍然认真评测软件与工具。"),
        ],
    },
    {
        "id": "wholeearthreview00unse_0",
        "short": "Mar",
        "label": "No. 45",
        "title": "Whole Earth Review, March 1985",
        "pages": 110,
        "words": 57728,
        "flagged": "26 / 110",
        "accent": "#5f8a5f",
        "scanBase": "https://archive.org/download/wholeearthreview00unse_0/page/n{leaf}_w500.jpg",
        "source": "_local/reading_sources/wholeearthreview00unse_0/map_content_draft.md",
        "sections": ["这本自己的结构", "中文入口问题"],
        "center": "反教条",
        "subtitle": "环保运动的自我校准",
        "timeline": ["城市", "自批判", "地球图像", "修复", "复杂政治", "软件更新"],
        "themes": [
            ("ecology", "城市生态", "城市和自然不是简单敌我关系。"),
            ("movement", "运动自批判", "成功后的环保主义可能僵化、专业化和恐慌化。"),
            ("image", "图像政治", "Whole Earth 图像也可能制造疏离。"),
            ("repair", "修复尺度", "有些地方要设计，有些地方要撤回人的痕迹。"),
            ("politics", "复杂政治", "原住民、革命政府和冷战不能被压成阵营选择题。"),
            ("platform", "工具转向", "工具观进入电脑、软件和地方网络。"),
        ],
    },
    {
        "id": "wholeearthreview00unse_1",
        "short": "May",
        "label": "No. 46",
        "title": "Whole Earth Review, May 1985",
        "pages": 118,
        "words": 62185,
        "flagged": "33 / 118",
        "accent": "#8368b3",
        "scanBase": "https://archive.org/download/wholeearthreview00unse_1/page/n{leaf}_w500.jpg",
        "source": "_local/reading_sources/wholeearthreview00unse_1/map_content_draft.md",
        "sections": ["这期自己的结构", "中文入口问题"],
        "center": "行动",
        "subtitle": "自治实践现场图",
        "timeline": ["死亡", "尼加拉瓜", "生态系统", "小企业", "黑客伦理", "传播", "平台"],
        "themes": [
            ("witness", "见证", "死亡、战争和照护经验把工具拉回生存现场。"),
            ("politics", "政治判断", "宏大意识形态会吞掉具体处境。"),
            ("systems", "系统观察", "生态球、土地和深生态让系统变得可看见。"),
            ("selforg", "自组织", "小企业、无政府和黑客伦理测试轻结构。"),
            ("network", "传播网络", "民间外交、BBS 和读者来信构成平台前夜。"),
            ("culture", "边缘文化", "朋克、软技术、艺术和旅行是离开默认生活的工具。"),
        ],
    },
    {
        "id": "wholeearthreview00unse_2",
        "short": "Jul",
        "label": "No. 47",
        "title": "Whole Earth Review, July 1985",
        "pages": 124,
        "words": 59823,
        "flagged": "45 / 124",
        "accent": "#3d7f91",
        "scanBase": "https://archive.org/download/wholeearthreview00unse_2/page/n{leaf}_w500.jpg",
        "source": "_local/reading_sources/wholeearthreview00unse_2/quality_for_map.md",
        "sections": ["Recommended Map Themes"],
        "center": "证据",
        "subtitle": "民主、媒介与日常善意",
        "timeline": ["民主", "生态冲突", "小说", "小企业", "数字图像", "互动媒体", "善意"],
        "themes": [
            ("politics", "民主学习", "民主是制度，也是需要练习的文化。"),
            ("ecology", "生态争议", "动物伦理、直接行动和公共叙事互相冲突。"),
            ("culture", "社会想象", "小说和故事提供替代社会模型。"),
            ("media", "媒介证据", "照片、视频和互动媒体改变真实感。"),
            ("network", "全球访问", "音乐、海外工作和工具渠道把读者带出本地。"),
            ("body", "日常伦理", "Random Kindness 把政治降到可实践的小动作。"),
        ],
    },
    {
        "id": "wholeearthreview00unse_3",
        "short": "Fall",
        "label": "No. 48",
        "title": "Whole Earth Review, Fall 1985",
        "pages": 148,
        "words": 72713,
        "flagged": "27 / 148",
        "accent": "#bb6c35",
        "scanBase": "https://archive.org/download/wholeearthreview00unse_3/page/n{leaf}_w500.jpg",
        "source": "_local/reading_sources/wholeearthreview00unse_3/map_content_draft.md",
        "sections": ["建议的地图结构", "章节/板块草案"],
        "center": "信任",
        "subtitle": "1985 文化剖面",
        "timeline": ["经济", "服务", "疾病", "园林", "电脑健康", "故事", "读者网络"],
        "themes": [
            ("politics", "新经济", "投机、债务、创业和资源限制改变行为。"),
            ("selforg", "服务伦理", "公司关系、顾客和员工信任决定组织质量。"),
            ("body", "身体公共性", "AIDS 和电脑健康风险让技术进入身体。"),
            ("ecology", "生态设计", "园林、空间和观看让自然保护变成设计问题。"),
            ("network", "故事网络", "都市传说、WELL、读者和财务公开组成共同体。"),
        ],
    },
    {
        "id": "wholeearthreview00unse_4",
        "short": "Winter",
        "label": "No. 49",
        "title": "Whole Earth Review, Winter 1985",
        "pages": 146,
        "words": 80748,
        "flagged": "25 / 146",
        "accent": "#426f7f",
        "scanBase": "https://archive.org/download/wholeearthreview00unse_4/page/n{leaf}_w500.jpg",
        "source": "_local/reading_sources/wholeearthreview00unse_4/map_content_draft.md",
        "sections": ["地图入口", "全期结构"],
        "center": "他者",
        "subtitle": "他者、系统与共同体",
        "timeline": ["Islam", "盲点", "身体", "复杂系统", "共同体", "敌人", "创作工具"],
        "themes": [
            ("religion", "Islam 镜子", "专题挑战美国媒体制造的他者想象。"),
            ("body", "身体实践", "宗教被读成姿势、时间、文本和日常节律。"),
            ("systems", "复杂系统", "Conway's Life 把生命模拟和个人电脑连接起来。"),
            ("community", "共同体失败", "The Farm 让理想社区承受劳动和权力检验。"),
            ("politics", "敌人与沟通", "Us and Them 把他者问题落回个人实践。"),
            ("design", "创作工具", "Oblique Strategies 让判断卡住时换一条路径。"),
        ],
    },
    {
        "id": "wholeearthsoftwa00unse_3",
        "short": "Software",
        "label": "Software Catalog",
        "title": "Whole Earth Software Catalog 2.0, Fall 1985",
        "pages": 228,
        "words": 126473,
        "flagged": "58 / 228 refined",
        "accent": "#d8912f",
        "scanBase": "https://archive.org/download/wholeearthsoftwa00unse_3/page/n{leaf}_w500.jpg",
    },
]

THEME_COLORS = {
    "attention": "#d35f45", "power": "#8b5a3c", "labor": "#3f6f7f", "privacy": "#80629d",
    "culture": "#4f7d62", "platform": "#396f90", "ecology": "#5f8a5f", "movement": "#bb6c35",
    "image": "#426f7f", "repair": "#6f7d45", "politics": "#a94f38", "witness": "#8368b3",
    "systems": "#4f7d62", "selforg": "#d8912f", "network": "#a94f38", "media": "#396f90",
    "body": "#a94f38", "religion": "#426f7f", "community": "#8368b3", "design": "#d8912f",
}

THEME_WORDS = {
    "attention": "注意力 沉浸 速度 审美 monkey mind personal computing",
    "power": "神话 信息 民主 doubt mythinformation technology",
    "labor": "办公室 劳动 work office home office vdt screen labor",
    "privacy": "隐私 数据 public image database state",
    "culture": "小说 故事 文化 fiction story le guin punk art travel game",
    "platform": "软件 通信 computer software telecom bbs well smart system",
    "ecology": "生态 自然 城市 园林 garden seed forest permaculture land ecology nature",
    "movement": "运动 环保主义 自批判 ethics professionalism panic poison",
    "image": "图像 照片 影像 photo image retouching video",
    "repair": "修复 repair recreate meadow bamboo",
    "politics": "政治 战争 敌人 经济 债务 投机 泡沫 创业 资源 democracy nicaragua miskito islam enemy economy hawken 1920s",
    "witness": "死亡 见证 照护 death witness care",
    "systems": "系统 复杂 生态球 conway life system ecosphere",
    "selforg": "服务 顾客 员工 公司 小企业 商业 组织 信任 business service customer company hacker anarchy",
    "network": "读者 网络 平台 共同体 well backscatter gate five bbs reader urban legends foaf",
    "media": "媒介 照片 视频 互动 photo video film interactive retouching",
    "body": "身体 疾病 健康 aids herpes computer hazards vdt radiation health salat",
    "religion": "宗教 islam qur salat muslim",
    "community": "共同体 公社 farm commune community",
    "design": "设计 工具 判断 oblique craft tool design",
}

ISSUE_THEME_OVERRIDES = {
    "wholeearthreview00unse_3": [
        (r"经济转型|开场：危险设施", ["politics", "selforg"]),
        (r"身体、疾病|疾病、亲密|个人电脑|电脑和现代办公室", ["body"]),
        (r"自然不是背景|生态作为设计|旅行、游戏", ["ecology"]),
        (r"故事、记忆|传统、流言|知识、历史", ["network"]),
        (r"艺术进入太空", ["ecology"]),
    ],
}

FALL_PANEL_COPY = {
    "经济转型不是宏观数字，而是行为方式": {
        "claim": "新经济首先改变人的行为方式，然后才表现为宏观数字。",
        "role": "这组内容不是商业管理摘要，而是 Whole Earth 式的新经济观察。Paul Hawken 把 1980 年代与 1920 年代并置，重点不是预测崩盘，而是看投机、债务、创业、技术重组和资源约束怎样让社会失去真实感；紧接着的服务文章又把宏观经济落到公司内部，提醒读者商业关系最终取决于顾客、员工和错误处理。",
        "objects": ["We're in a 1920s Economy", "You Are the Customer, You Are the Company", "Small Business", "Home Office", "SMART SYSTEM"],
        "links": "连接“服务伦理”，因为这组内容把新经济从宏观判断落到组织关系；也连接 Software 1985，因为家庭办公和集成软件已经进入商业日常。",
    },
    "身体、疾病和公共恐惧": {
        "claim": "疾病不是单纯医学问题，而是社群、亲密关系和公共知识的压力测试。",
        "role": "Living With AIDS 把 AIDS 放进 1980 年代旧金山 gay community、公共卫生、志愿护理、医学研究和死亡经验里；Saint Herpes 则把非致命但高度污名化的疾病写成亲密关系与自我认识的转折。这组内容真正关心的是：当医学还不能给出稳定答案时，人如何靠社群、信息和照护继续生活。",
        "objects": ["Living With AIDS", "Saint Herpes", "AIDS 社群照护", "疾病污名", "瘟疫史"],
        "links": "连接“电脑健康风险”，因为两者都在讨论技术时代的不确定风险；也连接“故事网络”，因为疾病知识需要通过社群传播才变成行动。",
    },
    "自然不是背景，而是一套设计方法": {
        "claim": "生态在这里不是背景，而是判断尺度、居住方式和设计方法。",
        "role": "这组内容把生态放进园林、森林经营、种子保存、农具、建筑、能源和室内空气里。Reflections on a Chinese Garden 尤其适合中文读者：它不是把中国园林当作审美样式，而是用中国思想反问西方环境伦理为什么总把人和自然分开；Four Pairs 则把 permaculture 变成可操作的设计原则。",
        "objects": ["Reflections on a Chinese Garden", "Garden Seed Inventory", "Forest Farmer's Handbook", "Four Pairs", "soft technology"],
        "links": "连接“新经济”，因为两者都把抽象系统落到日常行动；也连接“旅行、游戏、学习和手艺”，因为工具文化最终要回到身体和场地。",
    },
    "个人电脑从工具进入身体和风险": {
        "claim": "电脑不只是办公工具，也开始成为身体环境的一部分。",
        "role": "这组内容适合连接今天的屏幕劳动和 AI 使用。它不是简单说电脑有害，而是展示 1985 年的人如何在证据不足时聪明地担心：辐射、眩光、静电、怀孕风险、工会调查、厂商沉默、屏幕滤镜和工作姿势，都被放进同一个不确定性框架里。",
        "objects": ["The Health Hazards of Computers", "VDT", "screen labor", "屏幕滤镜", "measurement culture"],
        "links": "连接“身体公共性”，因为技术风险已经进入身体；也连接 Software 1985 的办公工具，因为生产力软件背后有真实的劳动环境。",
    },
    "故事、记忆和共同体": {
        "claim": "故事不是装饰，它是共同体保存经验和传播判断的方式。",
        "role": "这一组解释了 Whole Earth 为什么不是普通工具目录。Ron Jones 把世界纪录从精英成就改成可共同发明的游戏；犹太另类杂志评论讨论传统、激进、女性、政治和灵性如何通过小刊物继续生产；Urban Legends 则把流言当成现代民间故事的活体标本。最后的读者来信、WELL、财务公开和募款，让杂志自身也成为一个正在维持的共同体。",
        "objects": ["World Records", "Jewish alternative magazines", "Things Which Get Lost", "Urban Legends", "WELL"],
        "links": "连接“服务伦理”，因为信任需要被组织出来；也连接“传统、流言和读者网络”，因为这本杂志把读者当成共同生产者。",
    },
}

PANEL_COPY = json.loads(PANEL_COPY_PATH.read_text(encoding="utf-8")) if PANEL_COPY_PATH.exists() else {}

POSITIONS = [
    (35, 22, "-2deg"), (24, 39, "1deg"), (32, 57, "-1deg"), (45, 15, "2deg"),
    (17, 62, "1.5deg"), (28, 79, "-2deg"), (43, 83, "1deg"), (58, 82, "-1.5deg"),
    (72, 73, "1.8deg"), (84, 57, "-1deg"), (84, 39, "1.2deg"), (74, 22, "-2deg"),
    (60, 16, "1.5deg"), (52, 35, "-1deg"), (43, 51, "2deg"), (58, 58, "-2deg"),
    (68, 44, "1deg"), (71, 88, "-1deg"), (47, 67, "1.4deg"),
]


def strip_prefix(title: str) -> str:
    title = re.sub(r"^`([^`]+)`$", r"\1", title.strip())
    title = re.sub(r"^(入口\s*[A-Z0-9一二三四五六七八九十]+|路径\s*[A-Z0-9一二三四五六七八九十]+|[0-9]+|[A-Z])[:：.、]\s*", "", title)
    return title.strip()


def section_blocks(markdown: str, section_names: list[str]) -> list[tuple[str, str, str]]:
    lines = markdown.splitlines()
    active = None
    current = None
    blocks: list[tuple[str, str, str]] = []
    section_re = re.compile(r"^##\s+(.+)$")
    sub_re = re.compile(r"^###\s+(.+)$")
    for line in lines:
        sec = section_re.match(line)
        if sec:
            active = sec.group(1).strip() if sec.group(1).strip() in section_names else None
            current = None
            continue
        if not active:
            continue
        sub = sub_re.match(line)
        if sub:
            current = [active, strip_prefix(sub.group(1)), []]
            blocks.append(current)  # type: ignore[arg-type]
            continue
        if current is not None:
            current[2].append(line)
    return [(section, title, "\n".join(body).strip()) for section, title, body in blocks]


def first_leaf(text: str, fallback: int) -> int:
    match = re.search(r"leaf\s+([0-9]+)", text, re.I)
    return int(match.group(1)) if match else fallback


def leaf_range(text: str, fallback: int) -> str:
    match = re.search(r"leaf\s+([0-9]+)(?:\s*[-–]\s*([0-9]+))?", text, re.I)
    if not match:
        return f"leaf {fallback}"
    if match.group(2):
        return f"leaf {match.group(1)}-{match.group(2)}"
    return f"leaf {match.group(1)}"


def first_sentences(text: str, count: int = 2) -> list[str]:
    for label in ("中文导读角度：", "给中文读者的进入方式：", "内容位置：", "Why it matters:", "Interpretation:"):
        if label in text:
            text = text.split(label, 1)[1]
            break
    clean = re.sub(r"https?://\S+", "", text)
    clean = re.sub(r"`([^`]+)`", r"\1", clean)
    clean = re.sub(r"^[\s*\-]+", "", clean, flags=re.M)
    paras = []
    for p in re.split(r"\n\s*\n", clean):
        p = p.strip()
        if not p:
            continue
        low = p.lower()
        if low.startswith(("evidence", "scan", "关键 leaf", "核心页", "risk", "status", "leaf")):
            continue
        paras.append(p)
    sentence_text = " ".join(paras[:3])
    parts = re.split(r"(?<=[。！？.!?])\s*", sentence_text)
    return [p.strip() for p in parts if len(p.strip()) > 8][:count]


def trim_text(text: str, limit: int) -> str:
    text = clean_inline(text)
    if len(text) <= limit:
        return text
    return text[:limit].rstrip("，、；：,. ") + "。"


def panel_override(issue: dict, title: str) -> dict:
    return PANEL_COPY.get(issue["id"], {}).get(title, {})


def panel_claim(issue: dict, title: str, claim: str) -> str:
    override = panel_override(issue, title) or (FALL_PANEL_COPY.get(title) if issue["id"] == "wholeearthreview00unse_3" else None)
    if override:
        return override["claim"]
    return trim_text(claim, 56)


def panel_role(issue: dict, title: str, claim: str, role: str) -> str:
    override = panel_override(issue, title) or (FALL_PANEL_COPY.get(title) if issue["id"] == "wholeearthreview00unse_3" else None)
    if override:
        return override["role"]
    source = claim if claim and claim != title else role
    return trim_text(source, 180)


def panel_links(issue: dict, title: str, theme_ids: list[str]) -> str:
    override = panel_override(issue, title) or (FALL_PANEL_COPY.get(title) if issue["id"] == "wholeearthreview00unse_3" else None)
    if override:
        return override["links"]
    theme_titles = [theme_title(issue, theme_id) for theme_id in theme_ids]
    if len(theme_titles) > 1:
        return "连接“" + " / ".join(theme_titles[1:]) + "”，因为这个节点跨越了本期不止一条暗线。"
    return "连接同一暗线下的相邻节点，帮助读者把这组内容放回全期结构里。"


def clean_inline(text: str) -> str:
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -*")


def objects_from(text: str, title: str) -> list[str]:
    objects: list[str] = []
    objects += re.findall(r"`([^`]{2,45})`", text)
    objects += re.findall(r"《([^》]{2,45})》", text)
    objects += re.findall(r"\b([A-Z][A-Za-z0-9'&.\-]*(?:\s+[A-Z][A-Za-z0-9'&.\-]*){0,3})\b", title + "\n" + text)
    dedup: list[str] = []
    for item in objects:
        item = item.strip(" .,;:()[]")
        if re.fullmatch(r"leaf\s+[0-9,\-\s]+", item, re.I):
            continue
        if item and item not in dedup and len(item) <= 50 and item.lower() not in {"evidence", "status", "risk"}:
            dedup.append(item)
    return (dedup or [title])[:5]


def panel_objects(issue: dict, title: str, body: str) -> list[str]:
    override = panel_override(issue, title) or (FALL_PANEL_COPY.get(title) if issue["id"] == "wholeearthreview00unse_3" else None)
    if override:
        return override["objects"]
    return objects_from(body, title)


def theme_title(issue: dict, theme_id: str) -> str:
    for item_id, title, _ in issue.get("themes", []):
        if item_id == theme_id:
            return title
    return theme_id


def themes_for(issue: dict, title: str, body: str) -> list[str]:
    text = (title + "\n" + body).lower()
    for pattern, theme_ids in ISSUE_THEME_OVERRIDES.get(issue["id"], []):
        if re.search(pattern, title):
            return theme_ids
    valid = {theme_id for theme_id, *_ in issue.get("themes", [])}
    scores: dict[str, int] = {theme_id: 0 for theme_id in valid}
    for theme_id, words in THEME_WORDS.items():
        if theme_id not in valid:
            continue
        for word in words.split():
            if word.lower() in text:
                scores[theme_id] += 1
    for theme_id, title_cn, desc in issue.get("themes", []):
        if theme_id not in valid:
            continue
        for token in re.split(r"[、，。和与 ]+", title_cn + " " + desc):
            token = token.strip().lower()
            if len(token) >= 2 and token in text:
                scores[theme_id] += 2
    ranked = [k for k, v in sorted(scores.items(), key=lambda kv: kv[1], reverse=True) if v > 0]
    return ranked[:3] or [issue["themes"][0][0]]


def thumb_path(issue: dict, leaf: int) -> str:
    return f"scans/{issue['id']}_n{leaf}_w500.png"


def ensure_thumb(issue: dict, leaf: int) -> None:
    scan_dir = OUT_DIR / "scans"
    scan_dir.mkdir(parents=True, exist_ok=True)
    target = OUT_DIR / thumb_path(issue, leaf)
    if target.exists() and target.stat().st_size > 1024:
        return
    url = issue["scanBase"].replace("{leaf}", str(leaf))
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=6) as response:
            target.write_bytes(response.read())
    except Exception:
        if target.exists():
            target.unlink()


def build_issue_map(issue: dict) -> dict:
    markdown = (ROOT / issue["source"]).read_text(encoding="utf-8")
    blocks = section_blocks(markdown, issue["sections"])
    nodes = []
    by_section: dict[str, list[str]] = {}
    for index, (section, title, body) in enumerate(blocks):
        if len(title) < 3:
            continue
        source_title = title
        override = panel_override(issue, source_title)
        display_title = override.get("title", source_title)
        x, y, tilt = POSITIONS[index % len(POSITIONS)]
        sentences = first_sentences(body, 2)
        claim = sentences[0] if sentences else source_title
        role = sentences[1] if len(sentences) > 1 else claim
        theme_ids = themes_for(issue, source_title, body)
        theme = theme_ids[0]
        leaf = first_leaf(body, max(1, index * 7 + 1))
        pages = leaf_range(body, leaf)
        node_id = re.sub(r"[^a-z0-9]+", "-", source_title.lower()).strip("-")[:42] or f"node-{index}"
        if any(n["id"] == node_id for n in nodes):
            node_id = f"{node_id}-{index}"
        nodes.append({
            "id": node_id,
            "title": display_title,
            "source_title": source_title,
            "theme": theme,
            "themes": theme_ids,
            "pages": pages,
            "leaf": leaf,
            "thumb": thumb_path(issue, leaf),
            "claim": panel_claim(issue, source_title, claim),
            "role": panel_role(issue, source_title, claim, role),
            "objects": panel_objects(issue, source_title, body),
            "links": panel_links(issue, source_title, theme_ids),
            "x": x,
            "y": y,
            "tilt": tilt,
            "color": THEME_COLORS.get(theme, issue["accent"]),
        })
        by_section.setdefault(section, []).append(node_id)
    modes = [{"id": "all", "title": "全部", "nodes": None}]
    for idx, section in enumerate(issue["sections"], 1):
        ids = by_section.get(section, [])
        if ids:
            modes.append({"id": f"section-{idx}", "title": section[:8], "nodes": ids})
    return {
        "subtitle": issue["subtitle"],
        "center": issue["center"],
        "center_sub": issue["subtitle"],
        "source_note": f"依据 {issue['source']}；不是全文翻译，节点来自这本自己的草案结构。",
        "themes": [{"id": k, "title": t, "text": d, "color": THEME_COLORS.get(k, issue["accent"])} for k, t, d in issue["themes"]],
        "modes": modes,
        "timeline": issue["timeline"],
        "nodes": nodes,
    }


def render_issue(issue: dict, slim_issues: list[dict]) -> str:
    map_data = build_issue_map(issue)
    for node in map_data["nodes"][:4]:
        if not (OUT_DIR / node["thumb"]).exists():
            node["thumb"] = issue["scanBase"].replace("{leaf}", str(node["leaf"]))
    data = json.dumps({"issue": issue, "map": map_data, "issues": slim_issues}, ensure_ascii=False)
    template = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__ · 中文知识地图</title>
  <link rel="icon" href="data:,">
  <style>
    :root { --ink:#171713; --paper:#ece7da; --panel:rgba(244,239,225,.72); --line:rgba(23,23,19,.18); --muted:#6b6558; --accent:__ACCENT__; --shadow:0 22px 55px rgba(43,35,22,.18); }
    *{box-sizing:border-box} body{margin:0;color:var(--ink);background:radial-gradient(circle at 14% 12%, color-mix(in srgb,var(--accent) 24%,transparent), transparent 24rem),radial-gradient(circle at 84% 22%,rgba(57,111,144,.16),transparent 25rem),linear-gradient(90deg,rgba(23,23,19,.04) 1px,transparent 1px),linear-gradient(rgba(23,23,19,.04) 1px,transparent 1px),var(--paper);background-size:auto,auto,28px 28px,28px 28px,auto;font-family:"Iowan Old Style","Songti SC","STSong",Georgia,serif} button{border:0;font:inherit;color:inherit;cursor:pointer}
    .desk{min-height:100vh;padding:20px;display:grid;grid-template-rows:auto 1fr;gap:16px}.rail{min-height:54px;border-bottom:1px solid rgba(23,23,19,.2);display:grid;grid-template-columns:minmax(220px,1fr) auto;align-items:center;gap:18px}.identity{display:flex;align-items:baseline;flex-wrap:wrap;gap:10px 14px}.stamp{display:inline-flex;align-items:center;min-height:24px;padding:2px 9px;border:1px solid rgba(23,23,19,.28);background:rgba(255,251,239,.55);font-family:"Courier New",monospace;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em}.identity strong{font-size:clamp(18px,2.5vw,32px);line-height:.96;font-weight:600}.identity span:last-child{color:var(--muted);font-size:14px}
    .modes,.issue-jump{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:8px}.issue-jump{margin-top:8px;justify-content:flex-start}.mode,.issue-link{min-height:34px;padding:7px 11px;border:1px solid rgba(23,23,19,.22);background:rgba(255,251,239,.46);font-family:"Courier New",monospace;font-size:12px;transition:transform .2s ease,background .2s ease;text-decoration:none;color:inherit}.mode:hover,.mode.active,.issue-link.active{transform:translateY(-2px);background:var(--ink);color:var(--paper)}
    .workspace{display:grid;grid-template-columns:minmax(210px,260px) minmax(520px,1fr) minmax(260px,360px);gap:16px;min-height:0}.routes,.inspector{border:1px solid rgba(23,23,19,.18);background:var(--panel);box-shadow:var(--shadow);min-width:0}.routes{display:grid;grid-template-rows:auto 1fr auto;overflow:hidden}.routes h2,.inspector h2{margin:0;padding:15px 16px 11px;font-size:14px;font-family:"Courier New",monospace;text-transform:uppercase;letter-spacing:.09em;border-bottom:1px solid rgba(23,23,19,.17)}
    .theme-list{overflow-y:auto;overflow-x:visible;padding:10px}.theme{width:100%;max-width:100%;min-width:0;text-align:left;display:grid;grid-template-columns:12px minmax(0,1fr);gap:10px;padding:12px 9px;background:transparent;border-bottom:1px dashed rgba(23,23,19,.18)}.theme i{width:11px;height:11px;margin-top:4px;background:var(--theme-color);transform:rotate(45deg);box-shadow:0 0 0 4px rgba(255,251,239,.62)}.theme-copy b{display:block;font-size:17px;line-height:1.15;font-weight:600}.theme-copy span{display:block;max-width:20ch;margin-top:4px;color:var(--muted);font-size:13px;line-height:1.45;overflow-wrap:anywhere}.theme.active,.theme:hover{background:rgba(255,251,239,.7)}.source-note{margin:0;padding:12px 14px;border-top:1px solid rgba(23,23,19,.17);color:var(--muted);font-size:12px;line-height:1.5;overflow-wrap:anywhere;word-break:break-word}
    .map-stage{position:relative;overflow:hidden;border:1px solid rgba(23,23,19,.22);background:linear-gradient(115deg,rgba(255,255,255,.26),rgba(255,255,255,0) 44%),repeating-linear-gradient(0deg,rgba(23,23,19,.07) 0 1px,transparent 1px 42px),repeating-linear-gradient(90deg,rgba(23,23,19,.045) 0 1px,transparent 1px 42px),rgba(236,231,218,.78);box-shadow:var(--shadow);min-height:720px}.map-stage:before{content:"";position:absolute;inset:20px;border:1px dashed rgba(23,23,19,.25);pointer-events:none}.orbit-label{position:absolute;left:28px;top:22px;z-index:3;display:flex;gap:8px;align-items:center;font-family:"Courier New",monospace;font-size:12px;text-transform:uppercase;letter-spacing:.07em}.scan-strip{position:absolute;right:26px;top:26px;z-index:3;width:min(27vw,260px);display:grid;grid-template-columns:repeat(4,1fr);gap:6px;opacity:.9}.scan-card{position:relative;display:block;min-height:96px;border:1px solid rgba(23,23,19,.22);background:rgba(255,251,239,.62);overflow:hidden;text-decoration:none;color:inherit}.scan-card img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}.scan-card span{position:absolute;left:4px;right:4px;bottom:4px;padding:2px 4px;background:rgba(255,251,239,.82);font-family:"Courier New",monospace;font-size:9px;line-height:1.1}.scan-card.missing{display:grid;place-items:center;font-family:"Courier New",monospace;font-size:10px;color:var(--muted)}
    .connections{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1}.connections path{fill:none;stroke:rgba(23,23,19,.25);stroke-width:1.1;stroke-dasharray:8 7}.connections path.strong{stroke:var(--accent);stroke-width:2;stroke-dasharray:none}.center{position:absolute;left:50%;top:50%;width:158px;min-height:158px;transform:translate(-50%,-50%);border-radius:999px;background:var(--ink);color:var(--paper);display:grid;place-items:center;text-align:center;z-index:2;box-shadow:0 20px 50px rgba(23,23,19,.24)}.center b{display:block;font-size:25px;line-height:1.05}.center span{display:block;max-width:12ch;margin-top:5px;font-family:"Courier New",monospace;font-size:10px;text-transform:uppercase;letter-spacing:.08em}
    .nodes{position:absolute;inset:0;z-index:2}.node{position:absolute;left:var(--x);top:var(--y);width:142px;min-height:86px;transform:translate(-50%,-50%) rotate(var(--tilt));border:1px solid rgba(23,23,19,.24);background:rgba(255,251,239,.84);box-shadow:8px 10px 0 color-mix(in srgb,var(--node-color) 42%,transparent);padding:10px 12px;text-align:left;transition:opacity .2s ease,transform .2s ease,box-shadow .2s ease}.node:hover,.node.active{transform:translate(-50%,-50%) rotate(0deg) scale(1.05);background:#fffdf5;z-index:5}.node.dim{opacity:.24;filter:grayscale(.4)}.node b{display:block;font-size:17px;line-height:1.05}.node span{display:block;margin-top:6px;color:var(--muted);font-family:"Courier New",monospace;font-size:11px;line-height:1.15}.node em{display:block;margin-top:7px;color:var(--node-color);font-style:normal;font-family:"Courier New",monospace;font-size:10px;font-weight:700;text-transform:uppercase}
    .mini-timeline{position:absolute;left:34px;right:34px;bottom:18px;z-index:3;display:grid;grid-template-columns:repeat(var(--cols),minmax(0,1fr));border-top:2px solid rgba(23,23,19,.5)}.phase{position:relative;padding-top:12px;font-size:12px;line-height:1.25;color:var(--muted)}.phase:before{content:"";position:absolute;top:-5px;left:0;width:10px;height:10px;border-radius:999px;background:var(--ink)}
    .inspector{overflow:auto}.reader-card{padding:18px 16px 16px;border-bottom:1px solid rgba(23,23,19,.17);background:rgba(255,251,239,.54)}.kicker{display:flex;justify-content:space-between;gap:12px;color:var(--muted);font-family:"Courier New",monospace;font-size:11px;text-transform:uppercase}.reader-card h3{margin:12px 0 8px;font-size:clamp(25px,2.7vw,38px);line-height:1.02;font-weight:500}.reader-card p,.field p,.field li{font-size:15px;line-height:1.58}.field{padding:15px 16px;border-bottom:1px solid rgba(23,23,19,.17)}.field b{display:block;margin-bottom:8px;font-family:"Courier New",monospace;font-size:12px;text-transform:uppercase;letter-spacing:.08em}.field p{margin:0}.field ul{margin:0;padding-left:18px}.field li+li{margin-top:6px}.field:empty{display:none}.theme-count{float:right;color:var(--muted);font-family:"Courier New",monospace;font-size:11px}.evidence{padding:16px;background:var(--ink);color:var(--paper)}.evidence a{display:block;color:var(--paper);text-decoration:none;font-size:18px;margin-bottom:10px}.evidence small{display:block;color:rgba(236,231,218,.72);line-height:1.5;font-family:"Courier New",monospace}
    @media(max-width:1120px){.workspace{grid-template-columns:1fr}.modes{justify-content:flex-start}.map-stage{min-height:980px}.scan-strip{width:190px;right:18px;top:64px}.center{width:142px;min-height:142px}.node{width:126px;min-height:82px}.mini-timeline{grid-template-columns:1fr;border-top:0;left:18px;right:18px}.phase{border-left:2px solid rgba(23,23,19,.55);padding:7px 0 7px 16px}.phase:before{top:12px;left:-6px}}@media(max-width:680px){.desk{padding:12px}.rail{grid-template-columns:minmax(0,1fr);align-items:start}.identity,.modes,.issue-jump{min-width:0}.mode,.issue-link{white-space:normal;max-width:100%;overflow-wrap:anywhere}.map-stage{min-height:auto;overflow:visible;padding:14px}.map-stage:before,.connections,.center,.scan-strip,.mini-timeline{display:none}.orbit-label{position:static;margin-bottom:12px}.nodes{position:static;display:grid;gap:10px}.node{position:relative;left:auto!important;top:auto!important;width:100%;min-height:auto;transform:none!important;overflow-wrap:anywhere}.node:hover,.node.active{transform:translateX(3px)!important}.theme-copy span{max-width:none}}
  </style>
</head>
<body>
  <script id="map-data" type="application/json">__DATA__</script>
  <main class="desk">
    <header class="rail"><div><div class="identity"><span class="stamp" id="issueLabel"></span><strong id="issueTitle"></strong><span id="issueSubtitle"></span></div><nav class="issue-jump" id="issueJump"></nav></div><nav class="modes" id="modes"></nav></header>
    <section class="workspace"><aside class="routes"><h2>暗线</h2><div class="theme-list" id="themeList"></div><p class="source-note" id="sourceNote"></p></aside><section class="map-stage" aria-label="知识地图"><div class="orbit-label"><span class="stamp" id="leafCount"></span><span>点击节点看关系</span></div><div class="scan-strip" id="scanStrip"></div><svg class="connections" id="connections"></svg><div class="center"><div><b id="centerTitle"></b><span id="centerSub"></span></div></div><div class="nodes" id="nodes"></div><div class="mini-timeline" id="timeline"></div></section><aside class="inspector"><h2>当前节点</h2><section class="reader-card"><div class="kicker"><span id="panelTheme"></span><span id="panelPages"></span></div><h3 id="panelTitle"></h3><p id="panelClaim"></p></section><section class="field"><b>这一章解决什么问题</b><p id="panelRole"></p></section><section class="field"><b>关键物件</b><ul id="panelObjects"></ul></section><section class="field"><b>连接关系</b><p id="panelLinks"></p></section><section class="evidence"><a id="scanLink" href="#" target="_blank" rel="noreferrer">打开对应扫描页</a><small id="panelEvidence"></small></section></aside></section>
  </main>
  <script>
    const payload = JSON.parse(document.getElementById('map-data').textContent);
    const issue = payload.issue;
    const map = payload.map;
    const nodes = map.nodes;
    const themes = map.themes;
    const byId = Object.fromEntries(nodes.map(n => [n.id, n]));
    const edges = [];
    for (let i = 0; i < nodes.length - 1; i++) edges.push([nodes[i].id, nodes[i + 1].id]);
    map.modes.forEach(m => {
      if (!m.nodes) return;
      for (let i = 0; i < m.nodes.length - 1; i++) edges.push([m.nodes[i], m.nodes[i + 1]]);
    });
    let activeTheme = null;
    let activeMode = 'all';
    let activeNode = nodes[Math.min(1, nodes.length - 1)].id;
    function scan(leaf) { return issue.scanBase.replace('{leaf}', leaf); }
    function nodeThemes(node) {
      return node.themes && node.themes.length ? node.themes : [node.theme];
    }
    function boot() {
      document.getElementById('issueLabel').textContent = issue.label;
      document.getElementById('issueTitle').textContent = issue.title;
      document.getElementById('issueSubtitle').textContent = map.subtitle;
      document.getElementById('sourceNote').textContent = map.source_note;
      document.getElementById('leafCount').textContent = `${issue.pages} leaves`;
      document.getElementById('centerTitle').textContent = map.center;
      document.getElementById('centerSub').textContent = map.center_sub;
      document.documentElement.style.setProperty('--accent', issue.accent);
      document.getElementById('issueJump').innerHTML = payload.issues.map(item => `<a class="issue-link ${item.id === issue.id ? 'active' : ''}" href="${item.id}.html">${item.short}</a>`).join('');
      document.getElementById('modes').innerHTML = map.modes.map(m => `<button class="mode ${m.id === activeMode ? 'active' : ''}" data-mode="${m.id}">${m.title}</button>`).join('');
      document.getElementById('timeline').style.setProperty('--cols', map.timeline.length);
      document.getElementById('timeline').innerHTML = map.timeline.map(x => `<div class="phase">${x}</div>`).join('');
      document.getElementById('scanStrip').innerHTML = nodes.slice(0, 4).map(n => `<a class="scan-card" href="${scan(n.leaf)}" target="_blank" rel="noreferrer"><img src="${n.thumb}" alt="${n.pages}" loading="eager"><span>${n.pages}</span></a>`).join('');
      document.querySelectorAll('.scan-card img').forEach(img => {
        img.onerror = () => {
          img.closest('.scan-card').classList.add('missing');
          img.closest('.scan-card').textContent = 'scan';
        };
      });
    }
    function renderThemes() {
      themeList.innerHTML = '';
      themes.forEach(t => {
        const count = nodes.filter(n => nodeThemes(n).includes(t.id)).length;
        const b = document.createElement('button');
        b.className = 'theme';
        b.style.setProperty('--theme-color', t.color);
        b.dataset.theme = t.id;
        b.innerHTML = `<i></i><div class="theme-copy"><b>${t.title}<span class="theme-count">${count}</span></b><span>${t.text}</span></div>`;
        b.onclick = () => {
          activeTheme = activeTheme === t.id ? null : t.id;
          update();
        };
        themeList.appendChild(b);
      });
    }
    function renderNodes() {
      nodesEl = document.getElementById('nodes');
      nodesEl.innerHTML = '';
      nodes.forEach(n => {
        const b = document.createElement('button');
        b.className = 'node';
        b.type = 'button';
        b.dataset.id = n.id;
        b.dataset.theme = n.theme;
        b.style.left = `${n.x}%`;
        b.style.top = `${n.y}%`;
        b.style.setProperty('--tilt', n.tilt);
        b.style.setProperty('--node-color', n.color);
        const theme = themes.find(t => t.id === n.theme);
        b.innerHTML = `<b>${n.title}</b><span>${n.pages}</span><em>${theme ? theme.title : n.theme}</em>`;
        b.onclick = () => setNode(n.id);
        nodesEl.appendChild(b);
      });
    }
    function drawEdges() {
      const svg = document.getElementById('connections');
      svg.innerHTML = '';
      const st = svg.getBoundingClientRect();
      if (!st.width || matchMedia('(max-width:680px)').matches) return;
      const c = { x: st.width / 2, y: st.height / 2 };
      const seen = new Set();
      edges.forEach(([f, t]) => {
        const k = f + '>' + t;
        if (seen.has(k)) return;
        seen.add(k);
        const a = document.querySelector(`.node[data-id="${f}"]`);
        const b = document.querySelector(`.node[data-id="${t}"]`);
        if (!a || !b) return;
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        const ax = ar.left + ar.width / 2 - st.left;
        const ay = ar.top + ar.height / 2 - st.top;
        const bx = br.left + br.width / 2 - st.left;
        const by = br.top + br.height / 2 - st.top;
        const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        p.setAttribute('d', `M ${ax} ${ay} Q ${c.x} ${c.y} ${bx} ${by}`);
        if (f === activeNode || t === activeNode) p.classList.add('strong');
        svg.appendChild(p);
      });
    }
    function setNode(id) {
      activeNode = id;
      const n = byId[id] || nodes[0];
      const theme = themes.find(t => t.id === n.theme) || { title: n.theme };
      panelTheme.textContent = nodeThemes(n).map(id => (themes.find(t => t.id === id) || { title: id }).title).join(' / ');
      panelPages.textContent = n.pages;
      panelTitle.textContent = n.title;
      panelClaim.textContent = n.claim;
      panelRole.textContent = n.role;
      panelObjects.innerHTML = n.objects.map(object => `<li>${object}</li>`).join('');
      panelLinks.textContent = n.links;
      scanLink.href = scan(n.leaf);
      panelEvidence.textContent = `${n.pages} / 原始扫描图可用来复核 OCR、版式和图像。`;
      update();
      drawEdges();
    }
    function update() {
      const mode = map.modes.find(m => m.id === activeMode) || map.modes[0];
      const filter = mode.nodes ? new Set(mode.nodes) : null;
      document.querySelectorAll('.theme').forEach(b => b.classList.toggle('active', activeTheme === b.dataset.theme));
      document.querySelectorAll('.node').forEach(b => {
        const n = byId[b.dataset.id];
        const hide = (activeTheme && !nodeThemes(n).includes(activeTheme)) || (filter && !filter.has(n.id));
        b.classList.toggle('dim', hide);
        b.classList.toggle('active', n.id === activeNode);
      });
    }
    document.addEventListener('click', e => {
      const b = e.target.closest('.mode');
      if (!b) return;
      activeMode = b.dataset.mode;
      document.querySelectorAll('.mode').forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      update();
    });
    boot();
    renderThemes();
    renderNodes();
    setNode(activeNode);
    addEventListener('resize', drawEdges);
  </script>
</body>
</html>"""
    return template.replace("__TITLE__", html.escape(issue["title"])).replace("__ACCENT__", issue["accent"]).replace("__DATA__", data)


def render_index(slim: list[dict]) -> str:
    cards = []
    for issue in ISSUES:
        if issue["id"] == "wholeearthsoftwa00unse_3":
            chips = ["Shopping", "Programming", "Learning"]
            source = "恢复旧单本 18 节点结构"
        else:
            m = build_issue_map(issue)
            chips = [n["title"] for n in m["nodes"][:3]]
            source = f"{len(m['nodes'])} 个草案节点"
        cards.append(f"""<a class="issue" href="{issue['id']}.html" style="--accent:{issue['accent']}"><span>{issue['label']}</span><b>{issue['title']}</b><em>{source} · {issue['flagged']}</em><div>{''.join(f'<i>{html.escape(c)}</i>' for c in chips)}</div><p>{issue.get('subtitle','从工具判断进入编程、网络与学习')}</p></a>""")
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>1985 Whole Earth 中文知识地图</title><link rel="icon" href="data:,"><style>*{{box-sizing:border-box}}body{{margin:0;color:#171713;background:linear-gradient(90deg,rgba(23,23,19,.04) 1px,transparent 1px),linear-gradient(rgba(23,23,19,.04) 1px,transparent 1px),#ece7da;background-size:28px 28px;font-family:"Iowan Old Style","Songti SC",Georgia,serif}}main{{padding:18px}}.top{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid rgba(23,23,19,.22);padding-bottom:12px}}.top b{{font-size:clamp(20px,2.5vw,36px)}}.top span{{font-family:"Courier New",monospace;font-size:12px;color:#6b6558}}.grid{{display:grid;grid-template-columns:repeat(7,minmax(140px,1fr));border:1px solid rgba(23,23,19,.2);border-right:0;border-bottom:0;margin-top:16px;min-height:calc(100vh - 92px)}}.issue{{color:inherit;text-decoration:none;border-right:1px solid rgba(23,23,19,.2);border-bottom:1px solid rgba(23,23,19,.2);padding:14px;display:grid;grid-template-rows:auto auto auto auto 1fr;gap:12px;background:rgba(255,255,255,.28)}}.issue:hover{{background:color-mix(in srgb,var(--accent) 15%,#fffdf5)}}.issue span,.issue em{{font-family:"Courier New",monospace;font-size:12px;color:#6b6558;font-style:normal}}.issue b{{font-size:22px;line-height:1.05}}.issue i{{display:block;font-style:normal;border-left:4px solid var(--accent);background:rgba(255,255,255,.38);padding:8px 9px;margin:7px 0;font-size:13px}}.issue p{{align-self:end;margin:0;font-size:14px;line-height:1.5}}@media(max-width:1080px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}@media(max-width:620px){{.grid{{grid-template-columns:1fr}}.top{{display:block}}}}</style></head><body><main><div class="top"><b>1985 Whole Earth 中文知识地图</b><span>issue-specific maps · not one template</span></div><section class="grid">{''.join(cards)}</section></main></body></html>"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    slim = [{k: i[k] for k in ("id", "short", "label", "title", "pages", "flagged", "accent", "scanBase")} for i in ISSUES]
    for issue in ISSUES:
        target = OUT_DIR / f"{issue['id']}.html"
        if issue["id"] == "wholeearthsoftwa00unse_3":
            html_text = OLD_SOFTWARE.read_text(encoding="utf-8").replace("../../assets/", "../../../assets/")
            target.write_text(html_text, encoding="utf-8")
        else:
            target.write_text(render_issue(issue, slim), encoding="utf-8")
    (OUT_DIR / "index.html").write_text(render_index(slim), encoding="utf-8")
    payload = []
    for issue in ISSUES:
        if issue["id"] == "wholeearthsoftwa00unse_3":
            payload.append({"id": issue["id"], "title": issue["title"], "node_count": 18, "source": "legacy software map"})
        else:
            m = build_issue_map(issue)
            payload.append({"id": issue["id"], "title": issue["title"], "node_count": len(m["nodes"]), "themes": [t["title"] for t in m["themes"]]})
    (OUT_DIR / "1985_issue_maps.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "issues": len(ISSUES), "out_dir": str(OUT_DIR.relative_to(ROOT))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
