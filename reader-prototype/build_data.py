#!/usr/bin/env python3
"""Compatibility entrypoint for rebuilding the Epilog reader data.

The production reader now uses leaf-level translations under
content/translations/wholeearthepilog00unse. This wrapper keeps the older
`python3 build_data.py` command working while routing it to the current builder.
"""

from __future__ import annotations

from build_translation_reader_data import main


if __name__ == "__main__":
    main()
