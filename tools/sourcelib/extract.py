"""PDF -> pages. Native text first, OCR only when there is no native text.

The original PDF is opened read-only and is never written to, moved or
replaced. Everything this module produces is a derivative.

Requires poppler (pdftotext, pdfinfo, pdftoppm) for the PDF path, and
tesseract for the OCR path. Neither is needed to work with the text corpus
already in 00-sources/text/ — see ingest_from_text() in build_source_corpus.py.
"""

import datetime
import hashlib
import os
import re
import shutil
import subprocess
import tempfile

from . import config
from .pages import Page, pages_from_pdftotext, total_pdf_pages


class ExtractionError(Exception):
    pass


def have(tool):
    return shutil.which(tool) is not None


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def find_original(filename):
    """Locate a source PDF. 00-sources/ is searched before 00-sources/originals/
    so files placed by the existing fetch/extract scripts keep working."""
    if not filename:
        return None
    for d in config.ORIGINAL_DIRS:
        p = os.path.join(d, filename)
        if os.path.exists(p):
            return p
    return None


def pdf_page_count(pdf):
    if not have("pdfinfo"):
        return None
    r = subprocess.run(["pdfinfo", pdf], capture_output=True, timeout=300)
    if r.returncode != 0:
        return None
    m = re.search(r"^Pages:\s+(\d+)", r.stdout.decode("utf-8", "replace"), re.M)
    return int(m.group(1)) if m else None


def pdftotext_raw(pdf):
    """The whole document as pdftotext -layout sees it, form feeds intact."""
    if not have("pdftotext"):
        raise ExtractionError("pdftotext not on PATH (install poppler-utils)")
    r = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", pdf, "-"],
                       capture_output=True, timeout=1800)
    if r.returncode != 0:
        raise ExtractionError(r.stderr.decode("utf-8", "replace")[:300])
    return r.stdout.decode("utf-8", "replace")


def looks_image_only(pages, sheet_count, threshold=config.OCR_CHAR_THRESHOLD):
    """True when the PDF carries no usable embedded text.

    Measured against the sheet count, not against the pages that survived, so
    a 400-sheet scan that yields three pages of running heads is caught.
    """
    if not sheet_count:
        return True
    chars = sum(len(p.text) for p in pages)
    return (chars / sheet_count) < threshold


# --------------------------------------------------------------------------
# OCR
# --------------------------------------------------------------------------

def tesseract_version():
    if not have("tesseract"):
        return None
    r = subprocess.run(["tesseract", "--version"], capture_output=True, timeout=60)
    first = (r.stdout or r.stderr).decode("utf-8", "replace").splitlines()
    return first[0].strip() if first else "unknown"


def render_page_png(pdf, page_number, out_prefix, dpi=300):
    """One page of a PDF to PNG. Also the Phase 5 reviewer facility."""
    if not have("pdftoppm"):
        raise ExtractionError("pdftoppm not on PATH (install poppler-utils)")
    r = subprocess.run(["pdftoppm", "-f", str(page_number), "-l", str(page_number),
                        "-r", str(dpi), "-png", pdf, out_prefix],
                       capture_output=True, timeout=600)
    if r.returncode != 0:
        raise ExtractionError(r.stderr.decode("utf-8", "replace")[:300])
    directory = os.path.dirname(out_prefix) or "."
    base = os.path.basename(out_prefix)
    hits = sorted(f for f in os.listdir(directory)
                  if f.startswith(base) and f.endswith(".png"))
    if not hits:
        raise ExtractionError("pdftoppm produced no image for page %d" % page_number)
    return os.path.join(directory, hits[-1])


def ocr_page(png, lang):
    """(text, mean word confidence). Confidence comes from tesseract's own TSV,
    it is not estimated here."""
    r = subprocess.run(["tesseract", png, "stdout", "-l", lang, "tsv"],
                       capture_output=True, timeout=600)
    if r.returncode != 0:
        raise ExtractionError(r.stderr.decode("utf-8", "replace")[:300])
    rows = r.stdout.decode("utf-8", "replace").splitlines()
    words, confs, last_line = [], [], None
    for row in rows[1:]:
        f = row.split("\t")
        if len(f) < 12:
            continue
        conf, word = f[10], f[11]
        line_key = tuple(f[2:5])
        if word.strip():
            if last_line is not None and line_key != last_line:
                words.append("\n")
            words.append(word)
            try:
                c = float(conf)
                if c >= 0:
                    confs.append(c)
            except ValueError:
                pass
            last_line = line_key
    text = " ".join(words).replace(" \n ", "\n").replace(" \n", "\n").replace("\n ", "\n")
    mean = round(sum(confs) / len(confs), 2) if confs else None
    return text.strip(), mean


def ocr_pdf(pdf, sheet_count, lang="eng", dpi=300, first=None, last=None):
    """Render then OCR every page. Returns (pages, provenance dict)."""
    if not have("tesseract"):
        raise ExtractionError("tesseract not on PATH — cannot OCR an image-only PDF")
    version = tesseract_version()
    lo = first or 1
    hi = last or sheet_count
    pages, confs = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for n in range(lo, hi + 1):
            png = render_page_png(pdf, n, os.path.join(tmp, "pg"), dpi=dpi)
            text, conf = ocr_page(png, lang)
            os.remove(png)
            if not text:
                continue
            if conf is not None:
                confs.append(conf)
            pages.append(Page(n, text, extraction_method="ocr", ocr_confidence=conf))
    prov = {
        "extraction_method": "ocr",
        "ocr_engine": "tesseract",
        "ocr_engine_version": version,
        "ocr_lang": lang,
        "ocr_dpi": dpi,
        "ocr_confidence": round(sum(confs) / len(confs), 2) if confs else None,
        "ocr_timestamp": datetime.datetime.now(datetime.timezone.utc)
                                  .replace(microsecond=0).isoformat(),
    }
    return pages, prov


# --------------------------------------------------------------------------
# the one entry point
# --------------------------------------------------------------------------

def extract_pdf(pdf, allow_ocr=False, ocr_lang="eng", ocr_dpi=300,
                threshold=config.OCR_CHAR_THRESHOLD, force_ocr=False):
    """(pages, provenance). Native text when the PDF has any; OCR when it does
    not and allow_ocr is set; otherwise a provenance record saying so."""
    raw = pdftotext_raw(pdf)
    sheets = total_pdf_pages(raw)
    pages = pages_from_pdftotext(raw)
    prov = {
        "extraction_method": "native_text",
        "sheet_count": sheets,
        "pdf_page_count": pdf_page_count(pdf) or sheets,
        "sha256": sha256_file(pdf),
        "pipeline_version": config.PIPELINE_VERSION,
        "extracted_at": datetime.datetime.now(datetime.timezone.utc)
                                 .replace(microsecond=0).isoformat(),
    }

    if force_ocr:
        # Native text exists but is not good enough — the case for a PDF whose
        # Arabic comes out as positioned glyphs. The original is untouched; this
        # produces a second derivative from the page images.
        if not allow_ocr:
            raise ExtractionError("--force-ocr needs --ocr")
        ocr_pages, ocr_prov = ocr_pdf(pdf, sheets, lang=ocr_lang, dpi=ocr_dpi)
        prov.update(ocr_prov)
        prov["extraction_status"] = "ocr-unverified"
        prov["note"] = "OCR forced; native text was present and was not used"
        return ocr_pages, prov

    if not looks_image_only(pages, sheets, threshold):
        return pages, prov

    prov["native_text_chars"] = sum(len(p.text) for p in pages)
    if not allow_ocr:
        prov["extraction_method"] = "native_text"
        prov["extraction_status"] = "image-only-needs-ocr"
        prov["note"] = ("no usable embedded text (%.1f chars/sheet, threshold %d). "
                        "Re-run with --ocr." % (prov["native_text_chars"] / max(sheets, 1),
                                                threshold))
        return pages, prov

    ocr_pages, ocr_prov = ocr_pdf(pdf, sheets, lang=ocr_lang, dpi=ocr_dpi)
    prov.update(ocr_prov)
    prov["extraction_status"] = "ocr-unverified"
    return ocr_pages, prov
