"""Pages -> passages.

What this module will not do:

* invent a speaker, a subject or a passage type. Anything it cannot read off
  the page deterministically stays NULL, or "unknown".
* infer a page number from a position in a chunk. Every passage carries the
  page it was cut from.
* touch Arabic. arabic_raw is the block exactly as extracted.

passage_id is SOURCE-PPPP-NNN — edition, zero-padded first page, ordinal on
that page. Stable across rebuilds, which is what later embeddings will key on.
"""

import re

from . import config
from .arabic import (arabic_ratio, arabic_char_count, has_broken_glyphs,
                     normalize_arabic)
from .pages import block_split, is_heading

PASSAGE_TYPES = ("saying", "hadith", "sermon", "letter", "narrative", "biography",
                 "historical_event", "commentary", "introduction", "other", "unknown")

ARABIC_BLOCK_RATIO = 0.5     # at or above this a block is Arabic
ANY_ARABIC_RATIO = 0.05      # below this a block is treated as clean English

_SENTENCE_END = re.compile(r"[.!?:;”\"')\]]\s*$")
_LOWER_START = re.compile(r"^[a-z]")

# ---------------------------------------------------------------------------
# Reading metadata off the page. Every pattern below matches something the
# source itself prints. Nothing is guessed: where a pattern does not match,
# the field stays NULL and passage_type stays "unknown". Anything set here is
# stamped metadata_source='detected-pattern' so a reviewer can tell it apart
# from something a human recorded.
# ---------------------------------------------------------------------------

# "43. Imam Ali (‘a) said:"  — Tuhaf al-Uqul's numbered maxims. The number is
# this edition's citation of record, not a page.
NUMBERED_SAYING = re.compile(r"^(?P<num>\d{1,4})\s*[.)]\s+(?P<who>[^\n]{2,60}?)\s*said\s*[:,]")

# "Imam Ali (‘a) said:" without a number.
_TITLES = (r"(?:Imam|The Imam|Amir al-Mu'minin|Amir al-Muminin|The Holy Prophet|The Prophet"
           r"|Prophet|Sayyida|Lady|Abu|Ali|Fatima)")
SAYING = re.compile(r"^(?P<who>%s[^\n]{0,60}?)\s*said\s*[:,]" % _TITLES)

# Nahj al-Balagha's own divisions, printed as headings.
SECTION_TYPES = (
    (re.compile(r"^(?P<ref>Letter\s+\d+)\b"), "letter"),
    (re.compile(r"^(?P<ref>Sermon\s+\d+)\b"), "sermon"),
    (re.compile(r"^(?P<ref>Saying\s+\d+)\b"), "saying"),
)


def split_numbered_sayings(block):
    """Split a block that runs several numbered sayings together.

    Some pages in this corpus carry no blank line between one maxim and the
    next, so a whole page arrives as a single block and a citation to "no. 8"
    would land on a passage starting at no. 4. The split is on the source's own
    numbering, at a line boundary, and only where the block holds at least two
    of them — so it never cuts a sentence.
    """
    lines = block.split("\n")
    starts = [i for i, ln in enumerate(lines) if NUMBERED_SAYING.match(ln.strip())]
    if len(starts) < 2:
        return [block]
    if starts[0] != 0:
        starts.insert(0, 0)
    out = []
    for j, s in enumerate(starts):
        e = starts[j + 1] if j + 1 < len(starts) else len(lines)
        chunk = "\n".join(lines[s:e]).strip()
        if chunk:
            out.append(chunk)
    return out


def read_metadata(text, section):
    """(speaker, passage_type, internal_ref) or (None, 'unknown', None).

    Reads only what is printed. Called once per passage.
    """
    head = text.lstrip()

    m = NUMBERED_SAYING.match(head)
    if m:
        return m.group("who").strip(), "saying", "no. %s" % m.group("num")

    m = SAYING.match(head)
    if m:
        return m.group("who").strip(), "saying", None

    if section:
        for pat, kind in SECTION_TYPES:
            m = pat.match(section.strip())
            if m:
                return None, kind, m.group("ref")

    return None, "unknown", None


class Passage:
    __slots__ = ("passage_id", "source_id", "pdf_page_start", "pdf_page_end",
                 "printed_page_start", "printed_page_end", "ordinal", "section",
                 "chapter", "title", "speaker", "subject", "passage_type", "register",
                 "arabic_raw", "arabic_normalized", "english", "text", "arabic_verified",
                 "extraction_method", "extraction_status", "quotation_ready", "char_count",
                 "internal_ref", "metadata_source", "arabic_char_count")

    def __init__(self, **kw):
        for s in self.__slots__:
            setattr(self, s, kw.get(s))

    def as_row(self):
        return {s: getattr(self, s) for s in self.__slots__}


def make_passage_id(source_id, page, ordinal):
    return "%s-%04d-%03d" % (source_id, page, ordinal)


def classify_block(text):
    """(kind, arabic_raw, english). kind is 'arabic', 'mixed' or 'english'.

    A mixed block keeps its whole text in english/text and gets no arabic_raw:
    splitting one out would mean deciding which characters belong to a quoted
    Arabic phrase, and getting that wrong silently corrupts a quotation.
    """
    ratio = arabic_ratio(text)
    if ratio >= ARABIC_BLOCK_RATIO:
        return "arabic", text, None
    if ratio >= ANY_ARABIC_RATIO:
        return "mixed", None, text
    return "english", None, text


def segment_page(source_id, page, section=None, chapter=None, join_carry=None,
                 extraction_status=None):
    """One page -> (passages, trailing_section, trailing_chapter, carry).

    ``carry`` is a block that ran off the bottom of the page mid-sentence. It
    is handed to the next page so the passage can be closed with a real
    page_start/page_end pair rather than cut in half.
    """
    passages = []
    ordinal = 0
    blocks = []
    for b in block_split(page.text):
        blocks.extend(split_numbered_sayings(b))
    pending = join_carry

    def emit(block_text, page_start, page_end, sec, chap, head):
        nonlocal ordinal
        ordinal += 1
        kind, ar, en = classify_block(block_text)
        method = page.extraction_method
        status = extraction_status or ("ocr-unverified" if method == "ocr" else "extracted")
        # OCR text and Arabic are both unfit for verbatim quotation until a
        # human has put them next to the page image. So is any block carrying
        # glyph damage — private-use codepoints and bidi controls left behind by
        # a PDF that hands over positioned glyphs instead of text. That damage
        # runs through the English of a two-column Arabic/English scan too, not
        # only through the Arabic.
        damaged = has_broken_glyphs(block_text)
        quotation_ready = 0 if (method == "ocr" or kind == "arabic" or damaged) else 1
        ar_chars = arabic_char_count(block_text)
        # A mixed block keeps its Arabic inside `text` verbatim and gets no
        # arabic_raw — see classify_block — but it still needs flagging, or a
        # damaged Arabic phrase inside an English paragraph passes unnoticed.
        # A stray diacritic or a bismillah ligature in an English line is not
        # Arabic to verify, which is why this keys on the register and not on
        # the raw character count.
        verified = 0 if kind in ("arabic", "mixed") else None
        speaker, ptype, internal_ref = ((None, "unknown", None) if kind == "arabic"
                                        else read_metadata(block_text, sec))
        return Passage(
            passage_id=make_passage_id(source_id, page_start, ordinal),
            source_id=source_id,
            pdf_page_start=page_start, pdf_page_end=page_end,
            printed_page_start=None, printed_page_end=None,
            ordinal=ordinal, section=sec, chapter=chap, title=head,
            speaker=speaker, subject=None,
            passage_type=ptype,
            internal_ref=internal_ref,
            metadata_source=("detected-pattern" if (speaker or ptype != "unknown") else None),
            register=kind,
            arabic_raw=ar,
            arabic_normalized=normalize_arabic(ar) if ar else None,
            english=en,
            text=block_text,
            arabic_char_count=ar_chars,
            arabic_verified=verified,
            extraction_method=method,
            extraction_status=status,
            quotation_ready=quotation_ready,
            char_count=len(block_text),
        )

    for i, block in enumerate(blocks):
        lines = block.split("\n")
        head = lines[0] if (len(lines) <= 3 and is_heading(lines[0])) else None
        if head:
            # A heading line names the section the passages under it belong to.
            # It is the source's own line, promoted, never rewritten.
            section = head
            if re.match(r"^(CHAPTER|Chapter|PART|Part|BOOK|Book)\b", head):
                chapter = head

        if pending is not None:
            # close the carry from the previous page with this block
            ptext, ppage = pending
            pending = None
            if arabic_ratio(ptext) < ARABIC_BLOCK_RATIO and _LOWER_START.match(block.lstrip()):
                passages.append(emit(ptext + "\n" + block, ppage, page.pdf_page,
                                     section, chapter, head))
                continue
            passages.append(emit(ptext, ppage, ppage, section, chapter, None))

        last = (i == len(blocks) - 1)
        if (last and not head
                and not _SENTENCE_END.search(block)
                and arabic_ratio(block) < ARABIC_BLOCK_RATIO):
            pending = (block, page.pdf_page)   # runs on to the next page
            continue

        passages.append(emit(block, page.pdf_page, page.pdf_page, section, chapter, head))

    return passages, section, chapter, pending


def segment(source_id, pages, join_pages=True, extraction_status=None):
    """Whole edition -> passages, in page order."""
    out, section, chapter, carry = [], None, None, None
    for page in pages:
        got, section, chapter, carry = segment_page(
            source_id, page, section, chapter,
            join_carry=carry if join_pages else None,
            extraction_status=extraction_status)
        out.extend(got)
        if not join_pages:
            carry = None
    if carry is not None:
        text, page_no = carry
        kind, ar, en = classify_block(text)
        out.append(Passage(
            passage_id=make_passage_id(source_id, page_no, 999),
            source_id=source_id, pdf_page_start=page_no, pdf_page_end=page_no,
            ordinal=999, section=section, chapter=chapter, title=None,
            passage_type="unknown", register=kind, arabic_raw=ar,
            arabic_normalized=normalize_arabic(ar) if ar else None, english=en,
            text=text, arabic_verified=(0 if ar else None),
            extraction_method="native_text", extraction_status=extraction_status or "extracted",
            quotation_ready=0 if (kind == "arabic" or has_broken_glyphs(text)) else 1,
            char_count=len(text), arabic_char_count=arabic_char_count(text),
            internal_ref=None, metadata_source=None))
    _renumber(out)
    return out


def _renumber(passages):
    """Ordinals are per starting page and must be dense and unique, because the
    passage_id is built from them."""
    seen = {}
    for p in passages:
        n = seen.get(p.pdf_page_start, 0) + 1
        seen[p.pdf_page_start] = n
        p.ordinal = n
        p.passage_id = make_passage_id(p.source_id, p.pdf_page_start, n)
