#!/usr/bin/env python3
import json
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work" / "wholeearth"
OUT = ROOT / "outputs"
WORK.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

IDENT = "wholeearthsoftwa00unse_3"
BASE = f"https://archive.org/download/{IDENT}"


def log(msg: str) -> None:
    now = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"[{now}] {msg}", flush=True)


def fetch(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        log(f"exists {dest} ({dest.stat().st_size} bytes)")
        return
    log(f"fetch {url}")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as r:
        data = r.read()
    dest.write_bytes(data)
    log(f"wrote {dest} ({len(data)} bytes)")


def get_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def clean_text(s: str) -> str:
    s = re.sub(r"\r\n?", "\n", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def extract_sections(index_html: Path):
    html = index_html.read_text(encoding="utf-8", errors="replace")
    # The Next.js payload contains section titles with page anchors.
    pairs = re.findall(r'<span class="sm:hanging-indent">([^<]+)</span><span[^>]*>(\d+)</span>', html)
    return [(re.sub(r"&amp;", "&", title), int(page)) for title, page in pairs]


def build_architecture(raw_text: str, sections):
    boundaries = []
    for i, (title, page) in enumerate(sections):
        next_page = sections[i + 1][1] if i + 1 < len(sections) else 200
        boundaries.append({"title": title, "start_page": page, "end_page": next_page - 1})
    front = [
        {"title": "How to Use This Book", "start_page": 2, "end_page": 3},
        {"title": "Shopping", "start_page": 4, "end_page": 9},
        {"title": "Computer Magazines", "start_page": 10, "end_page": 13},
        {"title": "Hardware", "start_page": 14, "end_page": 21},
        {"title": "Buying", "start_page": 22, "end_page": 27},
    ]
    return front + boundaries + [{"title": "Point Foundation / Indexes / Last-Minute Supplement", "start_page": 200, "end_page": 224}]


def main():
    round_id = sys.argv[1] if len(sys.argv) > 1 else "001"
    log(f"start round={round_id} pid={Path('/proc').exists()}")
    meta_path = WORK / f"{IDENT}_metadata.json"
    text_path = WORK / f"{IDENT}_djvu.txt"
    fetch(f"https://archive.org/metadata/{IDENT}", meta_path)
    fetch(f"{BASE}/{IDENT}_djvu.txt", text_path)

    meta = get_json(meta_path)
    files = meta.get("files", [])
    jpgs = [f for f in files if f.get("name", "").startswith("page/") and f.get("name", "").endswith(".jpg")]
    log(f"metadata title={meta.get('metadata', {}).get('title')!r} files={len(files)} page_jpgs={len(jpgs)}")

    raw = clean_text(text_path.read_text(encoding="utf-8", errors="replace"))
    log(f"ocr chars={len(raw)} words={len(raw.split())}")

    index_html = WORK / "software1985.html"
    if not index_html.exists():
        fetch("https://wholeearth.info/p/whole-earth-software-catalog-2_0-fall-1985", index_html)
    sections = extract_sections(index_html)
    log(f"sections from wholeearth.info={sections}")
    arch = build_architecture(raw, sections)

    arch_path = OUT / "whole_earth_software_catalog_1985_architecture.json"
    arch_md = OUT / "whole_earth_software_catalog_1985_architecture.md"
    arch_path.write_text(json.dumps(arch, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Whole Earth Software Catalog 2.0 架构草稿", ""]
    for item in arch:
        lines.append(f"- {item['start_page']}-{item['end_page']}: {item['title']}")
    arch_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"wrote {arch_path}")
    log(f"wrote {arch_md}")
    log("done")


if __name__ == "__main__":
    main()
