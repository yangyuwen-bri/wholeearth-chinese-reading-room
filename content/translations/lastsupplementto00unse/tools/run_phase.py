#!/usr/bin/env python3
"""Run one resilient whole-issue translation phase, one leaf at a time."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent.parent
TOOLS = PACKAGE / "tools"
STATUS = PACKAGE / "status.jsonl"


def rows() -> list[dict[str, object]]:
    return [json.loads(line) for line in STATUS.read_text().splitlines() if line.strip()]


def run(script: str, leaf: int, force: bool = False) -> bool:
    command = [sys.executable, str(TOOLS / script)]
    if force:
        command.append("--force")
    command.append(str(leaf))
    return subprocess.run(command, check=False).returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["translate", "review", "repair", "rereview"])
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=131)
    args = parser.parse_args()
    failures: list[int] = []
    for row in rows():
        leaf = int(row["leaf"])
        if not args.start <= leaf <= args.end:
            continue
        status = str(row["status"])
        if args.phase == "translate":
            if bool(row["translation_exists"]) or status == "accepted":
                continue
            ok = run("translate_with_ollama.py", leaf)
        elif args.phase == "review":
            if not bool(row["translation_exists"]) or status == "accepted":
                continue
            ok = run("review_with_ollama.py", leaf, force=True)
        elif args.phase == "repair":
            if status != "revise":
                continue
            ok = run("repair_with_ollama.py", leaf)
        else:
            if status != "needs_highres_scan" or not bool(row["review_exists"]):
                continue
            ok = run("review_with_ollama.py", leaf, force=True)
        if not ok:
            failures.append(leaf)
            print(f"leaf {leaf:03d}: phase failed; continuing", flush=True)
    print(f"phase {args.phase}: failures={failures}", flush=True)


if __name__ == "__main__":
    main()
