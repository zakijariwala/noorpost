"""Paths and constants for the source pipeline.

Everything here is relative to the repository root, resolved from this file's
own location, so the tools work from any working directory.
"""

import os

PIPELINE_VERSION = "1.0"

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SOURCES = os.path.join(ROOT, "00-sources")

# Where the original PDFs live. 00-sources/ itself is checked first because
# that is where extract_text.py and fetch_sources.py have always put them.
ORIGINAL_DIRS = [SOURCES, os.path.join(SOURCES, "originals")]
ORIGINALS = os.path.join(SOURCES, "originals")

TEXT = os.path.join(SOURCES, "text")            # existing corpus, [[p N]] marked
PAGES = os.path.join(SOURCES, "pages")          # intermediate representation
MD = os.path.join(SOURCES, "md")                # canonical markdown
METADATA = os.path.join(SOURCES, "metadata")
REPORTS = os.path.join(SOURCES, "reports")
PAGE_IMAGES = os.path.join(SOURCES, "page-images")
DB = os.path.join(SOURCES, "source.db")

SOURCES_YAML = os.path.join(METADATA, "sources.yaml")
REJECTED_YAML = os.path.join(METADATA, "rejected.yaml")
CLAIMS_YAML = os.path.join(METADATA, "claims.yaml")
CITATIONS_YAML = os.path.join(METADATA, "citations.yaml")
FETCH_MANIFEST = os.path.join(SOURCES, "manifest.json")

# --- status vocabularies -------------------------------------------------
# Edition status. "fixed" means: this exact edition is the one the project
# cites, and it is complete. Nothing incomplete is ever "fixed".
EDITION_STATUS = ("fixed", "candidate", "verification-required", "missing", "rejected")

# Claim status. TV -> V is the project's existing state machine; the other
# three codes are the citation sheet's own and are carried through unchanged.
CLAIM_STATUS = ("TV", "V", "TRAD", "CONT", "CUT", "rejected", "needs-review")

# What a citation actually points at. The project's rule is that for a
# web-generated PDF the work's own internal numbering is the citation of
# record and a page number is decoration.
CITATION_TYPES = ("page", "internal-number", "entry", "hadith-number", "chapter-report", "none")

# How a page's text came to exist.
EXTRACTION_METHODS = ("native_text", "ocr", "inherited")

# Pagination character of an edition, which decides whether a page number
# may be cited at all. Both values other than "printed" come straight from
# the two traps documented in sourcing-rules.md / HANDOVER.md.
PAGINATION = ("printed", "web-generated", "two-column", "unknown")

PAGINATION_WARNING = {
    "web-generated": ("web-generated PDF: [[p N]] is an artifact of generation, not the printed "
                      "edition. Cite the work's own internal numbering."),
    "two-column": ("two-column scan: one [[p N]] covers two book pages. Read the running header "
                   "for the real book page before citing."),
    "unknown": "pagination character not established for this edition; do not cite a page number.",
}

# Below this many characters per page, averaged, a PDF is treated as
# image-only and needs OCR before it carries any usable text.
OCR_CHAR_THRESHOLD = 100

PAGE_MARKER = "[[p {n}]]"
