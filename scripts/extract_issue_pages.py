#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
PAGE_XML = ROOT / "_local" / "page_xml"
OUT = ROOT / "_local" / "page_dossiers"


def fetch(identifier: str, suffix: str) -> Path:
    PAGE_XML.mkdir(parents=True, exist_ok=True)
    path = PAGE_XML / f"{identifier}_{suffix}"
    if not path.exists() or path.stat().st_size < 1000:
        url = f"https://archive.org/download/{identifier}/{identifier}_{suffix}"
        for attempt in range(1, 5):
            try:
                urlretrieve(url, path)
                break
            except Exception as exc:
                if path.exists() and path.stat().st_size < 1000:
                    path.unlink()
                if attempt == 4:
                    raise
                time.sleep(attempt * 2)
    return path


def clean(text: str) -> str:
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_scandata(path: Path) -> dict[int, dict]:
    root = ET.parse(path).getroot()
    out = {}
    for page in root.findall(".//page"):
        leaf = int(page.attrib["leafNum"])
        data = {"leaf": leaf}
        for tag in ["pageType", "handSide", "origFileName"]:
            node = page.find(tag)
            data[tag] = node.text if node is not None else ""
        page_number = page.find("pageNumber")
        data["pageNumber"] = page_number.text if page_number is not None else ""
        out[leaf] = data
    return out


def object_leaf(obj: ET.Element, fallback: int) -> int:
    page_param = obj.find("PARAM[@name='PAGE']")
    if page_param is not None:
        value = page_param.attrib.get("value", "")
        m = re.search(r"_(\d+)\.djvu", value)
        if m:
            return int(m.group(1)) - 1
    return fallback


def parse_djvu(path: Path, scandata: dict[int, dict], identifier: str) -> list[dict]:
    root = ET.parse(path).getroot()
    pages = []
    for idx, obj in enumerate(root.findall(".//OBJECT")):
        leaf = object_leaf(obj, idx)
        words = []
        lines = []
        for line in obj.findall(".//LINE"):
            line_words = []
            for word in line.findall("WORD"):
                if word.text:
                    line_words.append(word.text)
            text = clean(" ".join(line_words))
            if text:
                lines.append(text)
                words.extend(line_words)
        page_text = clean(" ".join(lines))
        meta = scandata.get(leaf, {"leaf": leaf})
        access_index = leaf
        page_no = meta.get("pageNumber") or infer_printed_page(page_text)
        pages.append(
            {
                "leaf": leaf,
                "access_index": access_index,
                "page_number": page_no,
                "page_type": meta.get("pageType", ""),
                "image_url": f"https://archive.org/download/{identifier}/page/n{access_index}_w500.jpg",
                "line_count": len(lines),
                "word_count": len(words),
                "headings": candidate_headings(lines),
                "text": page_text[:6000],
                "lines": lines[:80],
            }
        )
    return pages


def infer_printed_page(text: str) -> str:
    m = re.match(r"^(\d{1,3})\s+[A-Z]", text)
    return m.group(1) if m else ""


def candidate_headings(lines: list[str]) -> list[str]:
    out = []
    seen = set()
    for line in lines[:80]:
        if len(line) < 3 or len(line) > 90:
            continue
        letters = re.sub(r"[^A-Za-z]", "", line)
        uppercase = bool(letters) and sum(c.isupper() for c in letters) / max(1, len(letters)) > 0.65
        looks_title = uppercase or re.search(r"\b(?:PROGRAMMING|PLAYING|WRITING|LEARNING|TELECOMMUNICATING|SOFTWARE|CATALOG|INTRODUCTION)\b", line, re.I)
        if looks_title:
            key = line.lower()
            if key not in seen:
                out.append(line)
                seen.add(key)
        if len(out) >= 8:
            break
    return out


def write_contact_sheet(identifier: str, pages: list[dict], out_dir: Path, start: int, end: int) -> None:
    html = [
        "<!doctype html><meta charset='utf-8'><style>body{font-family:sans-serif;background:#eee;margin:0;padding:16px}.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}.p{background:white;padding:8px}.p img{width:100%;display:block}.p b{font-size:13px}.p p{font-size:12px;color:#555}</style><div class='grid'>"
    ]
    for page in pages[start:end]:
        html.append(
            f"<div class='p'><img src='{page['image_url']}'><b>leaf {page['leaf']} / p.{page['page_number']}</b><p>{' / '.join(page['headings'][:3])}</p></div>"
        )
    html.append("</div>")
    tmp = out_dir / f"contact_{start:03d}_{end:03d}.html"
    png = out_dir / f"contact_{start:03d}_{end:03d}.png"
    tmp.write_text("\n".join(html), encoding="utf-8")
    subprocess.run(
        [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=1400,1200",
            f"--screenshot={png}",
            f"file://{tmp.resolve()}",
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("identifier")
    parser.add_argument("--title", default="")
    parser.add_argument("--contact", action="store_true")
    args = parser.parse_args()

    djvu = fetch(args.identifier, "djvu.xml")
    scandata = fetch(args.identifier, "scandata.xml")
    scan = parse_scandata(scandata)
    pages = parse_djvu(djvu, scan, args.identifier)

    out_dir = OUT / args.identifier
    out_dir.mkdir(parents=True, exist_ok=True)
    dossier = {
        "identifier": args.identifier,
        "title": args.title,
        "page_count": len(pages),
        "pages": pages,
    }
    (out_dir / "pages.json").write_text(json.dumps(dossier, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [f"# {args.title or args.identifier}", "", f"pages: {len(pages)}", ""]
    for page in pages:
        md.append(f"## leaf {page['leaf']} / p.{page['page_number']} / {page['page_type']}")
        md.append(f"image: {page['image_url']}")
        if page["headings"]:
            md.append("headings: " + " / ".join(page["headings"]))
        md.append("")
        md.append(page["text"][:1200])
        md.append("")
    (out_dir / "pages.md").write_text("\n".join(md), encoding="utf-8")
    if args.contact:
        for start in range(0, len(pages), 36):
            write_contact_sheet(args.identifier, pages, out_dir, start, min(len(pages), start + 36))
    print(json.dumps({"identifier": args.identifier, "pages": len(pages), "out": str(out_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
