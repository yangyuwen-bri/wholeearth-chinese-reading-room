#!/usr/bin/env python3
import sys
from pathlib import Path
import xml.etree.ElementTree as ET


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: extract_leaf_xml_ocr.py LEAF", file=sys.stderr)
        return 2
    leaf = int(sys.argv[1])
    xml_path = Path("_local/page_xml/wholeearthepilog00unse_djvu.xml")
    root = ET.parse(xml_path).getroot()
    objects = root.findall(".//OBJECT")
    obj = objects[leaf]
    print(f"# leaf {leaf}")
    print(f"# size {obj.attrib.get('width')}x{obj.attrib.get('height')}")
    print()
    for line in obj.findall(".//LINE"):
        words = []
        coords = []
        for word in line.findall(".//WORD"):
            text = (word.text or "").strip()
            if text:
                words.append(text)
                coords.append(
                    (
                        int(word.attrib.get("coords", "0,0,0,0").split(",")[0])
                        if "coords" in word.attrib
                        else int(word.attrib.get("x", "0"))
                    )
                )
        if words:
            prefix = f"{min(coords):04d} " if coords else ""
            print(prefix + " ".join(words))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
