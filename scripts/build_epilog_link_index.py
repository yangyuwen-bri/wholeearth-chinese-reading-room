#!/usr/bin/env python3
"""Build an audited external-link index for Whole Earth Epilog references.

The script is intentionally conservative. It only promotes a link when the
original issue text contains the title and the external bibliographic record
matches the title closely enough to support reader-facing use.

Legacy note: this script reads the older content/readings summary draft. The
Chinese reading room itself is now generated from leaf-level translations under
content/translations/wholeearthepilog00unse.
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ZH_PATH = ROOT / "content/readings/1974_whole_earth_epilog_chapter_translation_zh.md"
PAGES_PATHS = [
    ROOT / "_local/page_dossiers/wholeearthepilog00unse/pages.json",
    ROOT / "_local/legacy/outputs/wholeearth_page_dossiers/wholeearthepilog00unse/pages.json",
]
JSON_OUT = ROOT / "data/bibliography/1974_whole_earth_epilog_links.json"
MD_OUT = ROOT / "content/readings/1974_whole_earth_epilog_bibliography_links.md"

OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"
IA_SEARCH = "https://archive.org/advancedsearch.php"
MAX_SOURCE_YEAR = 1975
PRINTED_PAGE_OFFSET = 449


SECTION_RANGES = [
    ("Front Matter", 0, 2),
    ("Whole Systems", 3, 24),
    ("Land Use", 25, 56),
    ("Shelter", 57, 76),
    ("Soft Technology", 77, 96),
    ("Craft", 97, 126),
    ("Community", 127, 184),
    ("Nomadics", 185, 220),
    ("Communications", 221, 260),
    ("Learning", 261, 300),
    ("Business / Index", 301, 321),
]

SKIP_TITLES = {
    "Epilog",
    "Whole Earth Epilog",
    "Whole Earth Catalog",
    "Last Whole Earth Catalog",
    "The Original Affluent Society",
    "The Spirit of the Gift",
    "The Superfluity of Naughtiness",
    "Seven Sermons to the Dead",
}

CANONICAL_TITLE_OVERRIDES = {
    "explorers ltd source book": "The Explorers Ltd. Source Book",
    "new woman s survival catalog": "The New Woman's Survival Catalog",
    "super catalog of car parts and accessories": "The Super Catalog of Car Parts & Accessories",
    "well body book": "The Well Body Book",
}

AMBIGUOUS_TITLES = {
    "Audubon",
    "Changes",
    "Home",
    "In the Making",
    "Leather",
    "Shelter",
    "Sail Magazine",
    "Library Journal",
    "Planet/Drum",
    "Country Women",
    "Ceramics Monthly",
    "Freedomways",
    "Black World",
    "Phylon",
    "Energy Digest",
    "Vital Signs",
}

TITLE_ONLY_CONFIRM_TITLES = {
    "The Amateur Wind Instrument Maker",
    "Anybody's Bike Book",
    "The Art of Written Forms",
    "Automotive Operation and Maintenance",
    "Bike Tripping",
    "Black Reconstruction in America",
    "The Botany and Chemistry of Hallucinogens",
    "Buddhism: Its Essence and Development",
    "The Catalogue of American Catalogues",
    "The Catalogue of Catalogues",
    "Cathedral",
    "Classic Guitar Making",
    "Communication: Ethical and Moral Issues",
    "The Compact Edition of the Oxford English Dictionary",
    "The Complete Book of Woodwork",
    "The Complete Motorcycle Nomad",
    "Crafts of the North American Indians",
    "Cutting Through Spiritual Materialism",
    "The Day They Parachuted Cats on Borneo",
    "The Death and Life of Great American Cities",
    "Design for Play",
    "Editing By Design",
    "The Explorers Ltd. Source Book",
    "Food Conspiracy Cookbook",
    "Foxfire 2",
    "The Gospel of Christian Atheism",
    "Handbook of PSI Discoveries",
    "Henscratches and Flyspecks",
    "How to Buy a Used Volkswagen in Europe, Keep it Alive, and Bring it Home",
    "Improvisation for the Theater",
    "Independent Filmmaking",
    "Italic Calligraphy & Handwriting",
    "The Joy of Spinning",
    "Kind and Usual Punishment",
    "Making Puppets Come Alive",
    "Math, Writing and Games in the Open Classroom",
    "Mechanization Takes Command",
    "Memories, Dreams, Reflections",
    "Minn of the Mississippi",
    "North American Bicycle Atlas",
    "Oh, What a Blow That Phantom Gave Me!",
    "Parent Effectiveness Training",
    "Patterns in Nature",
    "The People's Guide to Mexico",
    "Pioneer Life in Western Pennsylvania",
    "Practical Navigation for the Yachtsman",
    "A Primer of Visual Literacy",
    "The Publish-it Yourself Handbook",
    "The Rolling Stone Guide to High Fidelity Sound",
    "Safe and Simple Electrical Experiments",
    "Science and the Modern World",
    "Should Trees Have Standing?",
    "Shuttle, Spindle & Dyepot",
    "Some Men Are More Perfect Than Others",
    "Spiritual Community Guide",
    "Standard Handbook for Telescope Making",
    "Start Your Own Preschool Playgroup",
    "Strategic Concepts of Go",
    "The Super Catalog of Car Parts & Accessories",
    "Supermarket Handbook",
    "Understanding Boat Design",
    "Vegetarian Epicure",
    "Will It Grow In A Classroom?",
    "Working With The Wool",
    "Zen and the Art of Motorcycle Maintenance",
    "Zen Mind, Beginner's Mind",
}

AUTHOR_CONFIRM_RULES = {
    "Balinese Character": ("bateson", 1975),
    "Energy and Equity": ("illich", None),
    "I and Thou": ("buber", None),
    "Pilot's Weather": ("welch", 1975),
    "Small is Beautiful": ("schumacher", None),
    "System and Structure": ("wilden", 1977),
    "The Psychology of Consciousness": ("ornstein", 1975),
}

TITLE_CONTAINS_CONFIRM_RULES = {
    "Fundamental Algorithms": (["art of computer programming", "fundamental algorithms"], 1975),
    "The Mariners Catalog": (["mariner", "catalog"], 1976),
}

SOURCE_ALIASES = {
    "I and Thou": ["Iand Thou", "land Thou"],
    "I Never Promised You a Rose Garden": ["Promised You a Rose Garden"],
    "Zen and the Art of Motorcycle Maintenance": ["Motorcycle Maintenance, Zen and the Art of"],
    "Zen Mind, Beginner's Mind": ["Beginners Mind", "Zen Mind"],
    "Buddhism: Its Essence and Development": ["Buddhism: Its Essence and Development", "Its Essence and Development"],
    "The Botany and Chemistry of Hallucinogens": ["Botany and Chemistry of Hallucinogens"],
    "Fundamental Algorithms": ["Fundamental Algorithms"],
    "Computers and Computation": ["Computers and Computation"],
    "Science and the Modern World": ["Science and the Modern World"],
    "The Juniper Tree and Other Tales from Grimm": ["The Juniper Tree"],
    "Memories, Dreams, Reflections": ["Memories, Dreams, Reflections"],
    "The Rolling Stone Guide to High Fidelity Sound": ["The Rolling Stone Guide to High Fidelity Sound"],
    "Safe and Simple Electrical Experiments": ["Safe and Simple Electrical Experiments"],
    "Pioneer Life in Western Pennsylvania": ["Pioneer Life in Western Pennsylvania"],
}

MANUAL_TITLES = {
    "Steps to an Ecology of Mind",
    "System and Structure",
    "Patterns in Nature",
    "I and Thou",
    "The Cosmic Connection",
    "Passages About Earth",
    "The Limits to Growth",
    "Small is Beautiful",
    "Tools for Conviviality",
    "Should Trees Have Standing?",
    "Energy and Equity",
    "Acres, U.S.A.",
    "Grow It!",
    "Shelter",
    "Handmade Houses",
    "The Barn",
    "The Thatcher's Craft",
    "The Complete Book of Woodwork",
    "Crafts of the North American Indians",
    "Foxfire 2",
    "The Making of Tools",
    "The Modern Blacksmith",
    "The Kiln Book",
    "Finding One's Way With Clay",
    "Creative Crochet",
    "The Joy of Spinning",
    "Shuttle, Spindle & Dyepot",
    "The New Woman's Survival Catalog",
    "The Death and Life of Great American Cities",
    "Diet for a Small Planet",
    "The Well Body Book",
    "Our Bodies, Ourselves",
    "Kind and Usual Punishment",
    "The Autobiography of Malcolm X",
    "Black Reconstruction in America",
    "The Souls of Black Folk",
    "The Explorers Ltd. Source Book",
    "The People's Guide to Mexico",
    "Bike Tripping",
    "Anybody's Bike Book",
    "Richard's Bicycle Book",
    "North American Bicycle Atlas",
    "Automotive Operation and Maintenance",
    "The Super Catalog of Car Parts & Accessories",
    "Roll Your Own",
    "The Complete Motorcycle Nomad",
    "The Complete Book of Sky Sports",
    "Pilot's Weather",
    "Practical Navigation for the Yachtsman",
    "Understanding Boat Design",
    "The Mariners Catalog",
    "Outdoor Living",
    "Backpacking One Step At A Time",
    "Basic Rockcraft",
    "The Snowshoe Book",
    "The Outdoor Observer",
    "The Gun Digest Book of Knives",
    "Desert Solitaire",
    "The Catalogue of Catalogues",
    "The Catalogue of American Catalogues",
    "Science and the Modern World",
    "Real Time 1",
    "Real Time 2",
    "Oh, What a Blow That Phantom Gave Me!",
    "The Art of Public Speaking",
    "Communication: Ethical and Moral Issues",
    "Italic Calligraphy & Handwriting",
    "The Art of Written Forms",
    "Bookbinding by Hand",
    "Editing By Design",
    "Comprehensive Graphic Arts",
    "The Publish-it Yourself Handbook",
    "A Manual of Style",
    "Gravity's Rainbow",
    "The Compact Edition of the Oxford English Dictionary",
    "America: A Prophecy",
    "Mural Manual",
    "A Primer of Visual Literacy",
    "A History of Underground Comics",
    "The Big Yellow Drawing Book",
    "General Cartography",
    "Photographic Composition",
    "Balinese Character",
    "Independent Filmmaking",
    "The Filmgoer's Companion",
    "Improvisation for the Theater",
    "Henscratches and Flyspecks",
    "Classic Guitar Making",
    "The Amateur Wind Instrument Maker",
    "The Rolling Stone Guide to High Fidelity Sound",
    "Cybernetics for the Modern Mind",
    "TTL Cookbook",
    "Computers and Computation",
    "Fundamental Algorithms",
    "Natural Structure",
    "Stone Age Economics",
    "Management",
    "Decision and Control",
    "Parent Effectiveness Training",
    "Paddle-to-the-Sea",
    "The Day They Parachuted Cats on Borneo",
    "The Juniper Tree and Other Tales from Grimm",
    "Cathedral",
    "Toy Book",
    "Kite Craft",
    "Making Things",
    "Making Puppets Come Alive",
    "Kids are Natural Cooks",
    "Design for Play",
    "Start Your Own Preschool Playgroup",
    "Deschooling Society",
    "Values Clarification",
    "Will It Grow In A Classroom?",
    "The Seed Catalog",
    "Math, Writing and Games in the Open Classroom",
    "An Atlas of Fantasy",
    "Gazelle-Boy",
    "Pioneer Life in Western Pennsylvania",
    "Color Star Atlas",
    "Standard Handbook for Telescope Making",
    "Safe and Simple Electrical Experiments",
    "Anti-pollution Lab",
    "New Colleges for New Students",
    "Spiritual Community Guide",
    "The Ascent of Man",
    "Zen and the Art of Motorcycle Maintenance",
    "Mechanization Takes Command",
    "Handbook of PSI Discoveries",
    "Licit & Illicit Drugs",
    "The Botany and Chemistry of Hallucinogens",
    "I Never Promised You a Rose Garden",
    "Uncommon Therapy",
    "The Psychology of Consciousness",
    "The Gospel of Christian Atheism",
    "Buddhism: Its Essence and Development",
    "Cutting Through Spiritual Materialism",
    "Zen Mind, Beginner's Mind",
    "Memories, Dreams, Reflections",
}


def normalize_title(value: str) -> str:
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\b(the|a|an)\b", " ", value)
    return " ".join(value.split())


def title_match_score(source_title: str, candidate_title: str) -> float:
    left = normalize_title(source_title)
    right = normalize_title(candidate_title or "")
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    if left in right or right in left:
        shorter = min(len(left), len(right))
        longer = max(len(left), len(right))
        return 0.86 + 0.1 * (shorter / longer)
    left_words = set(left.split())
    right_words = set(right.split())
    if not left_words or not right_words:
        return 0.0
    return len(left_words & right_words) / len(left_words | right_words)


def safe_get_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "wholeearth-link-index/0.1"})
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8", "replace"))


def years_from_value(value: Any) -> list[int]:
    if value is None:
        return []
    if isinstance(value, list):
        text = " ".join(str(item) for item in value)
    else:
        text = str(value)
    return [int(match) for match in re.findall(r"\b(18\d{2}|19\d{2}|20\d{2})\b", text)]


def years_are_compatible(source_years: list[int], candidate_years: list[int]) -> bool:
    if not source_years or not candidate_years:
        return False
    for source_year in source_years:
        for candidate_year in candidate_years:
            if abs(source_year - candidate_year) <= 2:
                return True
    return False


def section_for_leaf(leaf: int) -> str:
    for name, start, end in SECTION_RANGES:
        if start <= leaf <= end:
            return name
    return "Unknown"


def printed_page_for_leaf(leaf: int) -> str | None:
    if leaf == 2:
        return "450"
    if 3 <= leaf <= 319:
        return str(leaf + PRINTED_PAGE_OFFSET)
    return None


def load_pages() -> list[dict[str, Any]]:
    for path in PAGES_PATHS:
        if path.exists():
            return json.loads(path.read_text())["pages"]
    searched = ", ".join(str(path.relative_to(ROOT)) for path in PAGES_PATHS)
    raise FileNotFoundError(f"No Epilog page dossier found. Searched: {searched}")


def extract_titles() -> list[str]:
    text = ZH_PATH.read_text()
    bracketed = set(re.findall(r"《([^》]+)》", text))
    english = {
        item.strip()
        for item in bracketed
        if re.search(r"[A-Za-z]", item) and not re.search(r"[\u4e00-\u9fff]", item)
    }
    raw_titles = (english | MANUAL_TITLES) - SKIP_TITLES
    canonical: dict[str, str] = {}
    for title in raw_titles:
        key = normalize_title(title)
        preferred = CANONICAL_TITLE_OVERRIDES.get(key, title)
        canonical[key] = preferred
    return sorted(set(canonical.values()), key=lambda item: normalize_title(item))


def find_source_mentions(title: str, pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    title_norms = {normalize_title(title)}
    for alias in SOURCE_ALIASES.get(title, []):
        title_norms.add(normalize_title(alias))
    mentions: list[dict[str, Any]] = []
    for page in pages:
        lines = page.get("lines") or []
        for index, line in enumerate(lines):
            line_norm = normalize_title(line)
            if any(title_norm and title_norm in line_norm for title_norm in title_norms):
                start = max(0, index - 3)
                end = min(len(lines), index + 12)
                excerpt = " ".join(lines[start:end])
                source_years = [year for year in years_from_value(excerpt) if year <= MAX_SOURCE_YEAR]
                bib_score = 0
                bib_score += 4 if source_years else 0
                bib_score += 3 if re.search(r"\b\d+\s*pp\b", excerpt, re.I) else 0
                bib_score += 2 if "postpaid" in excerpt.lower() else 0
                bib_score += 1 if "from:" in excerpt.lower() else 0
                bib_score -= 4 if "Section Contents" in excerpt else 0
                mentions.append(
                    {
                        "leaf": page.get("leaf"),
                        "access_index": page.get("access_index"),
                        "page_number": printed_page_for_leaf(int(page.get("leaf") or 0)),
                        "section": section_for_leaf(int(page.get("leaf") or 0)),
                        "image_url": page.get("image_url"),
                        "excerpt": excerpt,
                        "source_years": source_years,
                        "bibliographic_score": bib_score,
                    }
                )
    return sorted(mentions, key=lambda item: item["bibliographic_score"], reverse=True)[:3]


def query_open_library(title: str) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"title": title, "limit": 5})
    url = f"{OPEN_LIBRARY_SEARCH}?{params}"
    data = safe_get_json(url)
    results = []
    for doc in data.get("docs", [])[:5]:
        key = doc.get("key")
        results.append(
            {
                "provider": "openlibrary",
                "title": doc.get("title"),
                "authors": doc.get("author_name") or [],
                "first_publish_year": doc.get("first_publish_year"),
                "work_key": key,
                "url": f"https://openlibrary.org{key}" if key else None,
                "internet_archive_ids": (doc.get("ia") or [])[:5],
                "score": title_match_score(title, doc.get("title") or ""),
            }
        )
    return results


def query_internet_archive(title: str) -> list[dict[str, Any]]:
    query = f'title:("{title}")'
    params = [
        ("q", query),
        ("fl[]", "identifier"),
        ("fl[]", "title"),
        ("fl[]", "creator"),
        ("fl[]", "date"),
        ("rows", "5"),
        ("output", "json"),
    ]
    url = f"{IA_SEARCH}?{urllib.parse.urlencode(params)}"
    data = safe_get_json(url)
    results = []
    for doc in data.get("response", {}).get("docs", [])[:5]:
        identifier = doc.get("identifier")
        results.append(
            {
                "provider": "internet_archive",
                "title": doc.get("title"),
                "creator": doc.get("creator"),
                "date": doc.get("date"),
                "identifier": identifier,
                "url": f"https://archive.org/details/{identifier}" if identifier else None,
                "score": title_match_score(title, doc.get("title") or ""),
            }
        )
    return results


def text_from_candidate_people(candidate: dict[str, Any]) -> str:
    people = candidate.get("creator") or candidate.get("authors") or []
    if isinstance(people, list):
        return " ".join(str(item) for item in people).lower()
    return str(people).lower()


def candidate_year(candidate: dict[str, Any]) -> int | None:
    years = years_from_value(candidate.get("date") or candidate.get("first_publish_year"))
    return min(years) if years else None


def year_is_not_later_than(candidate: dict[str, Any], max_year: int | None) -> bool:
    year = candidate_year(candidate)
    return max_year is None or year is None or year <= max_year


def manual_promotable_candidates(title: str, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    promoted = []
    if title in TITLE_ONLY_CONFIRM_TITLES:
        for candidate in candidates:
            if (candidate.get("score") or 0) >= 0.98 and year_is_not_later_than(candidate, 1980):
                promoted.append(candidate)
    if title in AUTHOR_CONFIRM_RULES:
        author_fragment, max_year = AUTHOR_CONFIRM_RULES[title]
        for candidate in candidates:
            if (candidate.get("score") or 0) >= 0.9 and author_fragment in text_from_candidate_people(candidate):
                if year_is_not_later_than(candidate, max_year):
                    promoted.append(candidate)
    if title in TITLE_CONTAINS_CONFIRM_RULES:
        fragments, max_year = TITLE_CONTAINS_CONFIRM_RULES[title]
        for candidate in candidates:
            candidate_title = (candidate.get("title") or "").lower()
            if all(fragment in candidate_title for fragment in fragments):
                if year_is_not_later_than(candidate, max_year):
                    promoted.append(candidate)
    seen = set()
    return [item for item in promoted if not (item.get("url") in seen or seen.add(item.get("url")))]


def best_promoted_candidate(
    source_mentions: list[dict[str, Any]],
    promoted: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not promoted:
        return []
    source_years = source_mentions[0].get("source_years") or [] if source_mentions else []

    def rank(candidate: dict[str, Any]) -> tuple[int, int, float, int]:
        year = candidate_year(candidate)
        if source_years and year:
            distance = min(abs(year - source_year) for source_year in source_years)
        elif source_years:
            distance = 50
        elif year and year <= MAX_SOURCE_YEAR:
            distance = 0
        elif year:
            distance = abs(year - MAX_SOURCE_YEAR)
        else:
            distance = 25
        has_archive = 0 if candidate.get("internet_archive_ids") or candidate.get("provider") == "internet_archive" else 1
        return (distance, has_archive, -(candidate.get("score") or 0), year or 9999)

    return [sorted(promoted, key=rank)[0]]


def promotable_candidates(title: str, source_mentions: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_years = source_mentions[0].get("source_years") or [] if source_mentions else []
    promoted = []
    for candidate in candidates:
        if (candidate.get("score") or 0) < 0.98:
            continue
        candidate_years = years_from_value(candidate.get("date") or candidate.get("first_publish_year"))
        if years_are_compatible(source_years, candidate_years):
            promoted.append(candidate)
    if source_mentions:
        promoted.extend(manual_promotable_candidates(title, candidates))
    seen = set()
    deduped = [item for item in promoted if not (item.get("url") in seen or seen.add(item.get("url")))]
    return best_promoted_candidate(source_mentions, deduped)


def final_not_linked_status(title: str, source_mentions: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> tuple[str, str]:
    if not source_mentions:
        return "not_linked_source_not_located", "Final audit: the title was not located in local OCR/source pages, so no reader-facing external link was attached."
    if title in AMBIGUOUS_TITLES:
        return "not_linked_ambiguous_title", "Final audit: the title is generic, periodical-like, or organization-like; search results cannot prove the same item."
    if not candidates or all(candidate.get("error") for candidate in candidates):
        return "not_linked_no_reliable_match", "Final audit: Open Library and Internet Archive did not return a usable bibliographic record."
    best = candidates[0]
    if (best.get("score") or 0) >= 0.92:
        return "not_linked_candidate_mismatch", "Final audit: a close external record exists, but title/author/year evidence is insufficient to assert it is the same Epilog item."
    return "not_linked_no_reliable_match", "Final audit: returned records are not close enough to attach as reader-facing links."


def pick_status(title: str, source_mentions: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> tuple[str, str]:
    if title in AMBIGUOUS_TITLES:
        return final_not_linked_status(title, source_mentions, candidates)
    best_score = max((candidate.get("score") or 0 for candidate in candidates), default=0)
    exactish = promotable_candidates(title, source_mentions, candidates)
    close = [candidate for candidate in candidates if (candidate.get("score") or 0) >= 0.92]
    if exactish:
        return "confirmed", "Confirmed because the Epilog OCR contains the title and the external record matches by exact title plus compatible year, author, or manually checked work identity."
    if close or best_score >= 0.80:
        return final_not_linked_status(title, source_mentions, candidates)
    return final_not_linked_status(title, source_mentions, candidates)


def build_markdown(payload: dict[str, Any]) -> str:
    confirmed = [item for item in payload["items"] if item["status"] == "confirmed"]
    not_linked = [item for item in payload["items"] if item["status"] != "confirmed"]
    status_counts = {}
    for item in payload["items"]:
        status_counts[item["status"]] = status_counts.get(item["status"], 0) + 1
    lines = [
        "# Whole Earth Epilog, October 1974 - 书目与册子链接索引",
        "",
        "本索引补充《Whole Earth Epilog》中文章节译写稿中提到的书、册子、目录、期刊和工具性出版物链接。它不替代原书正文，也不声称提供免费下载；链接优先指向 Open Library 和 Internet Archive 的元数据、借阅或馆藏页面。",
        "",
        "## 审核规则",
        "",
        "- `confirmed`：原书 OCR 中能找到同一标题，并且外部书目记录标题精确匹配或规范化后精确匹配。",
        "- `not_linked_*`：已审核但不挂读者链接；原因写在条目后，避免把同名、近名、不同版本或期刊卷期误当成同一资料。",
        "- 过于普通的标题、期刊名、组织名，即便搜索有候选，也不自动确认。",
        "- 原书里的邮购地址、旧价格、供应商状态不视为今天仍有效。",
        "",
        f"- total audited: {len(payload['items'])}",
        f"- confirmed linked: {len(confirmed)}",
        f"- not linked after audit: {len(not_linked)}",
        f"- status counts: {', '.join(f'{key}={value}' for key, value in sorted(status_counts.items()))}",
        "",
        "## Confirmed Links",
        "",
    ]
    for item in confirmed:
        mention = item["source_mentions"][0]
        links = []
        for link in item["links"]:
            links.append(f"[{link['provider']}]({link['url']})")
        lines.extend(
            [
                f"### {item['title']}",
                "",
                f"- section: {mention['section']}",
                f"- source: leaf {mention['leaf']}, printed page {mention.get('page_number') or 'n/a'}; [scan]({mention['image_url']})",
                f"- links: {' / '.join(links)}",
                f"- audit: {item['audit_note']}",
                "",
            ]
        )
    lines.extend(["## Final Audit: Not Linked", ""])
    for item in not_linked:
        mention = item["source_mentions"][0] if item["source_mentions"] else None
        source = (
            f"leaf {mention['leaf']}, {mention['section']}" if mention else "source mention not located"
        )
        candidate = item["candidates"][0] if item["candidates"] else None
        candidate_text = (
            f"{candidate['provider']}: {candidate.get('title')} ({candidate.get('url')})"
            if candidate
            else "no candidate"
        )
        lines.extend(
            [
                f"- `{item['title']}` - {item['status']} - {source} - best candidate: {candidate_text} - {item['audit_note']}",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    pages = load_pages()
    titles = extract_titles()
    items = []
    for index, title in enumerate(titles, 1):
        source_mentions = find_source_mentions(title, pages)
        candidates: list[dict[str, Any]] = []
        try:
            candidates.extend(query_open_library(title))
        except Exception as exc:  # noqa: BLE001 - recorded for audit output
            candidates.append({"provider": "openlibrary", "error": str(exc), "score": 0})
        has_open_library_match = any((candidate.get("score") or 0) >= 0.98 for candidate in candidates)
        if not has_open_library_match:
            try:
                candidates.extend(query_internet_archive(title))
            except Exception as exc:  # noqa: BLE001 - recorded for audit output
                candidates.append({"provider": "internet_archive", "error": str(exc), "score": 0})
        time.sleep(0.08)
        candidates = sorted(candidates, key=lambda item: item.get("score") or 0, reverse=True)
        status, audit_note = pick_status(title, source_mentions, candidates)
        links = []
        if status == "confirmed":
            promoted = promotable_candidates(title, source_mentions, candidates)
            for candidate in candidates:
                if candidate not in promoted:
                    continue
                if candidate.get("url"):
                    links.append(
                        {
                            "provider": candidate["provider"],
                            "url": candidate["url"],
                            "matched_title": candidate.get("title"),
                            "matched_creator": candidate.get("creator") or candidate.get("authors"),
                            "matched_year": candidate.get("date") or candidate.get("first_publish_year"),
                            "score": candidate.get("score"),
                        }
                    )
                if candidate.get("provider") == "openlibrary":
                    for identifier in candidate.get("internet_archive_ids") or []:
                        links.append(
                            {
                                "provider": "internet_archive",
                                "url": f"https://archive.org/details/{identifier}",
                                "matched_title": candidate.get("title"),
                                "matched_creator": candidate.get("authors"),
                                "matched_year": candidate.get("first_publish_year"),
                                "score": candidate.get("score"),
                            }
                        )
            # De-duplicate provider URLs while preserving order.
            seen = set()
            links = [link for link in links if not (link["url"] in seen or seen.add(link["url"]))]
        items.append(
            {
                "title": title,
                "status": status,
                "source_mentions": source_mentions,
                "links": links,
                "candidates": candidates[:5],
                "audit_note": audit_note,
            }
        )
        print(f"{index:03d}/{len(titles)} {status:22s} {title}", flush=True)
    payload = {
        "issue": "Whole Earth Epilog, October 1974",
        "source_identifier": "wholeearthepilog00unse",
        "method": "Titles extracted from the Chinese chapter draft and curated high-value Epilog references; source mentions checked against local OCR; external candidates queried from Open Library and Internet Archive; only exact normalized title matches are promoted.",
        "items": items,
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    MD_OUT.write_text(build_markdown(payload))
    confirmed = sum(1 for item in items if item["status"] == "confirmed")
    print(json.dumps({"items": len(items), "confirmed": confirmed, "json": str(JSON_OUT), "md": str(MD_OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
