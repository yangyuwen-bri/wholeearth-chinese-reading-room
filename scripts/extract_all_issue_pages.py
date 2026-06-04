#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "evidence_dossiers" / "index.json"
PAGE_OUT = ROOT / "_local" / "page_dossiers"


def load_issues() -> list[dict]:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    return data["index"]


def page_count(identifier: str) -> int | None:
    path = PAGE_OUT / identifier / "pages.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return int(data.get("page_count") or len(data.get("pages", [])))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    issues = load_issues()
    if args.limit:
        issues = issues[: args.limit]

    start = time.time()
    done = 0
    skipped = 0
    failed = 0
    total_pages = 0
    for idx, issue in enumerate(issues, start=1):
        identifier = issue["identifier"]
        title = issue["title"]
        existing = page_count(identifier)
        if existing is not None and not args.force:
            skipped += 1
            total_pages += existing
            print(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S %Z')}] page_extract_skip {idx}/{len(issues)} "
                f"id={identifier} pages={existing}",
                flush=True,
            )
        else:
            cmd = [
                sys.executable,
                str(ROOT / "scripts" / "extract_issue_pages.py"),
                identifier,
                "--title",
                title,
            ]
            try:
                result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)
                print(result.stdout.strip(), flush=True)
                count = page_count(identifier) or 0
                total_pages += count
                done += 1
            except subprocess.CalledProcessError as exc:
                failed += 1
                print(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S %Z')}] page_extract_error {idx}/{len(issues)} "
                    f"id={identifier} title={title!r} rc={exc.returncode}",
                    flush=True,
                )
                if exc.stderr:
                    print(exc.stderr[-2000:], flush=True)

        elapsed = max(1e-6, time.time() - start)
        processed = done + skipped + failed
        speed = processed / elapsed
        eta = (len(issues) - processed) / speed if speed else 0
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S %Z')}] page_extract_progress "
            f"processed={processed}/{len(issues)} new={done} skipped={skipped} failed={failed} "
            f"pages={total_pages} speed={speed:.3f}_issues_per_sec eta_sec={eta:.0f}",
            flush=True,
        )

    print(
        json.dumps(
            {
                "issues": len(issues),
                "new": done,
                "skipped": skipped,
                "failed": failed,
                "pages": total_pages,
                "elapsed_sec": round(time.time() - start, 1),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
