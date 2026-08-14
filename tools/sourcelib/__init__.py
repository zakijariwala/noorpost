"""Noor Post source pipeline.

    original PDF  (immutable, the ultimate source of truth)
        -> canonical extraction        extract.py
        -> intermediate pages          pages.py     00-sources/pages/*.pages.jsonl
        -> page-preserving TXT + MD    pages.py     00-sources/text/, 00-sources/md/
        -> structured passages         passages.py
        -> SQLite + FTS5               db.py        00-sources/source.db
        -> retrieval                   ../source_search.py

The rules this code exists to enforce are written out in
00-foundations/source-truth-rules.md.
"""

__all__ = ["config", "arabic", "pages", "extract", "passages", "metadata", "db"]
