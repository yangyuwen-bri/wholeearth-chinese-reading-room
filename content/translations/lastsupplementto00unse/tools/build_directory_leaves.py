#!/usr/bin/env python3
"""Retired: raw directory OCR must not overwrite scan-checked translations."""


def main() -> None:
    raise SystemExit(
        "Directory generation is disabled: the old OCR copier dropped records "
        "and mixed columns. Edit leaves 114–125 against their scans, record "
        "page-specific reviews, then build the reader from those checked files. "
        "No translation or status file has been changed."
    )


if __name__ == "__main__":
    main()
