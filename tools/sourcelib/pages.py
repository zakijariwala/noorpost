"""The intermediate page representation, and the two renderings taken from it.

    PDF ──pdftotext/OCR──┐
                         ├──> [Page, Page, ...] ──┬──> .txt   (the [[p N]] corpus)
    existing .txt ───────┘                        └──> .md    (canonical markdown)

TXT and Markdown are *never* produced by separate extraction runs. Both are
functions of the same list of Page objects, which is what makes them provably
consistent (tests/test_source_pipeline.py).

The TXT rendering is byte-for-byte what tools/extract_text.py has always
written, including the habit of dropping pages that hold no text. That is why
[[p N]] markers are monotonic but not contiguous.
"""

import json
import re

from . import config

PAGE_MARKER_RE = re.compile(r"^\[\[p (\d+)\]\][ \t]*\r?$", re.M)

# A heading is only ever a line that is *already in the source*, promoted with
# a markdown prefix. Nothing is invented, reworded or re-cased.
HEADING_RE = re.compile(
    r"^(?:CHAPTER|Chapter|PART|Part|BOOK|Book|SECTION|Section|LETTER|Letter"
    r"|SERMON|Sermon|SAYING|Saying)\b[ :\.].{0,80}$"
)


class Page:
    """One page of one edition.

    pdf_page      1-based index of the sheet in the PDF. This is what [[p N]]
                  has always meant in this repository.
    printed_page  The number printed on the page of the book, when it is known
                  to differ. None means "not established" — never guessed.
    """

    __slots__ = ("pdf_page", "printed_page", "text", "extraction_method",
                 "ocr_confidence", "page_label")

    def __init__(self, pdf_page, text, printed_page=None, extraction_method="native_text",
                 ocr_confidence=None, page_label=None):
        self.pdf_page = int(pdf_page)
        self.text = text
        self.printed_page = printed_page
        self.extraction_method = extraction_method
        self.ocr_confidence = ocr_confidence
        self.page_label = page_label

    def to_dict(self):
        return {
            "pdf_page": self.pdf_page,
            "printed_page": self.printed_page,
            "page_label": self.page_label,
            "extraction_method": self.extraction_method,
            "ocr_confidence": self.ocr_confidence,
            "text": self.text,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["pdf_page"], d["text"], d.get("printed_page"),
                   d.get("extraction_method", "native_text"),
                   d.get("ocr_confidence"), d.get("page_label"))


# --------------------------------------------------------------------------
# pdftotext output -> pages
# --------------------------------------------------------------------------

def pages_from_pdftotext(raw_text, extraction_method="native_text"):
    """Split a whole-document pdftotext dump into pages.

    This is lifted unchanged from tools/extract_text.py so that the text
    corpus already in the repository stays reproducible byte for byte:
    form-feed split, trailing blanks off each line, runs of blank lines
    collapsed, page stripped, empty pages dropped.
    """
    out = []
    for i, page in enumerate(raw_text.split("\f"), 1):
        page = re.sub(r"[ \t]+\n", "\n", page)
        page = re.sub(r"\n{3,}", "\n\n", page).strip()
        if not page:
            continue
        out.append(Page(i, page, extraction_method=extraction_method))
    return out


def total_pdf_pages(raw_text):
    """Sheet count as pdftotext saw it, including the blank ones that get
    dropped. Needed by the page-count test — a dropped blank page must not
    look like a lost page."""
    return len(raw_text.split("\f"))


# --------------------------------------------------------------------------
# pages <-> .txt
# --------------------------------------------------------------------------

def read_text_file(path):
    """Read a [[p N]] text file without touching its line endings.

    The files already in 00-sources/text/ were written on a machine that
    translated newlines, over pdftotext output that already carried CRLF, so
    they hold \\r\\r\\n internally. Reading them verbatim is what lets the
    pipeline hand them back unchanged.
    """
    with open(path, encoding="utf-8", newline="") as f:
        body = f.read()
    return body, detect_newline(body)


def detect_newline(body):
    return "\r\n" if "]]\r\n" in body else "\n"


def render_txt(pages, newline="\n"):
    """The [[p N]] corpus format. With newline="\\n" this is byte for byte
    what extract_text.py writes."""
    sep = newline + newline
    return sep.join("[[p %d]]%s%s" % (p.pdf_page, newline, p.text) for p in pages)


def parse_txt(body, extraction_method="inherited"):
    """Read an existing [[p N]] text file back into pages.

    render_txt(parse_txt(x)) == x for every file in 00-sources/text/, which is
    what lets the existing corpus enter the pipeline without re-extraction.
    """
    marks = list(PAGE_MARKER_RE.finditer(body))
    pages = []
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        text = body[start:end].strip()
        if not text:
            continue
        pages.append(Page(int(m.group(1)), text, extraction_method=extraction_method))
    return pages


# --------------------------------------------------------------------------
# pages -> .md
# --------------------------------------------------------------------------

def is_heading(line):
    line = line.rstrip()
    if not line or len(line) > 90:
        return False
    if line.endswith(","):
        return False
    return bool(HEADING_RE.match(line))


def normalize_newlines(text):
    """Line endings to LF, and nothing else.

    The corpus in 00-sources/text/ carries \\r\\r\\n as its line terminator —
    pdftotext output that already had CRLF, written through a newline
    translation. A naive \\r -> \\n replacement turns every line break into a
    paragraph break, which cuts passages in half at the line.
    """
    return re.sub(r"\r+\n", "\n", text).replace("\r", "\n")


def block_split(text):
    """Page text -> paragraph blocks, in order. Blank-line separated, which is
    what pdftotext -layout gives for this corpus."""
    blocks = []
    current = []
    for line in normalize_newlines(text).split("\n"):
        if line.strip():
            current.append(line.rstrip())
        elif current:
            blocks.append("\n".join(current))
            current = []
    if current:
        blocks.append("\n".join(current))
    return blocks


def render_md(pages, front_matter=None):
    """Canonical markdown for one edition.

    The only things markdown adds are: an optional front-matter block, the
    same [[p N]] markers, and a `## ` prefix on lines that are already
    headings in the source. No text is reworded, reordered, joined or
    corrected. strip_md_decoration() undoes it exactly.
    """
    out = []
    if front_matter:
        out.append("---")
        for k, v in front_matter:
            out.append("%s: %s" % (k, "" if v is None else v))
        out.append("---")
        out.append("")

    for p in pages:
        out.append("[[p %d]]" % p.pdf_page)
        out.append("")
        rendered = []
        for block in block_split(p.text):
            lines = block.split("\n")
            if len(lines) <= 3 and is_heading(lines[0]):
                lines = ["## " + lines[0]] + lines[1:]
            rendered.append("\n".join(lines))
        out.append("\n\n".join(rendered))
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def strip_md_decoration(text):
    """Inverse of the only decoration render_md applies, used by the test that
    proves the two renderings carry the same page text."""
    return "\n".join(re.sub(r"^## ", "", ln) for ln in text.split("\n"))


# --------------------------------------------------------------------------
# pages <-> .pages.jsonl  (the intermediate on disk)
# --------------------------------------------------------------------------

def write_pages_jsonl(path, header, pages):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"record": "header", **header}, ensure_ascii=False, sort_keys=True) + "\n")
        for p in pages:
            f.write(json.dumps({"record": "page", **p.to_dict()}, ensure_ascii=False,
                               sort_keys=True) + "\n")


def read_pages_jsonl(path):
    header, pages = {}, []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("record") == "header":
                header = {k: v for k, v in d.items() if k != "record"}
            elif d.get("record") == "page":
                pages.append(Page.from_dict(d))
    return header, pages


def markers_monotonic(pages):
    """(ok, problems). Gaps are legal — a page holding no text is dropped, and
    always has been. Going backwards or repeating a number is not."""
    problems = []
    last = 0
    for p in pages:
        if p.pdf_page <= last:
            problems.append("page marker %d follows %d" % (p.pdf_page, last))
        last = p.pdf_page
    return (not problems), problems
