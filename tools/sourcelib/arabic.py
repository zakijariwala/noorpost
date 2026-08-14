"""Arabic detection and normalisation.

Two rules govern this module and are enforced by the tests:

1. ``arabic_raw`` is never touched. Normalisation always produces a *new*
   string that goes in a *different* column, and is only ever used for search.
2. Nothing here manufactures Arabic. If a page has no Arabic in it, no
   Arabic field is written.
"""

import re
import unicodedata

# Arabic, Arabic Supplement, Arabic Extended-A, presentation forms.
ARABIC_RANGES = (
    (0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF),
    (0xFB50, 0xFDFF), (0xFE70, 0xFEFF),
)

# Harakat, tanwin, shadda, sukun, superscript alef, and the Qur'anic marks.
DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭ࣓-ࣿ]")
TATWEEL = "ـ"

_FOLD = {
    "آ": "ا", "أ": "ا", "إ": "ا", "ٱ": "ا",  # alef forms
    "ى": "ي",                                                              # alef maqsura
    "ة": "ه",                                                              # ta marbuta
    "ؤ": "و", "ئ": "ي",                                          # hamza carriers
}


def is_arabic_char(ch):
    o = ord(ch)
    return any(lo <= o <= hi for lo, hi in ARABIC_RANGES)


def arabic_char_count(text):
    return sum(1 for ch in text if is_arabic_char(ch))


def arabic_ratio(text):
    """Share of the *letters* in ``text`` that are Arabic. Digits, spaces and
    punctuation are ignored so a line of Arabic with Latin footnote markers in
    it still reads as Arabic."""
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for ch in letters if is_arabic_char(ch)) / len(letters)


# Private Use Area, and the bidirectional embedding/override controls. Both
# are signs that a PDF's Arabic came out as positioned glyphs rather than as
# text: the letters are in visual order, split across runs, with font-specific
# codepoints among them. Such text is searchable only by accident and is never
# fit to quote.
BROKEN_GLYPH = re.compile(r"[-‪-‮‎‏]")


def has_broken_glyphs(text):
    return bool(BROKEN_GLYPH.search(text or ""))


def glyph_damage_ratio(texts):
    """Share of the given Arabic strings showing glyph-level damage."""
    texts = [t for t in texts if t]
    if not texts:
        return 0.0
    return sum(1 for t in texts if has_broken_glyphs(t)) / len(texts)


def normalize_arabic(text):
    """Search-only form: NFKC, diacritics and tatweel dropped, letter forms
    folded, whitespace collapsed.

    Never write this back over ``arabic_raw``. It is lossy on purpose — that
    is what makes it match a query typed without harakat.
    """
    if not text:
        return text
    out = unicodedata.normalize("NFKC", text)
    out = DIACRITICS.sub("", out)
    out = out.replace(TATWEEL, "")
    out = "".join(_FOLD.get(ch, ch) for ch in out)
    return re.sub(r"\s+", " ", out).strip()
