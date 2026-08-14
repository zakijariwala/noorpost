#!/usr/bin/env python3
"""
Tests for the source pipeline.

    python -m unittest discover -s tests -v
    python tests/test_source_pipeline.py

Two layers:

  * a synthetic fixture corpus, built end to end in a temporary directory.
    These always run, and they cover the paths that need a PDF or OCR by
    stubbing the subprocess boundary rather than the logic.
  * checks against the real corpus in 00-sources/, skipped when source.db has
    not been built.

The numbered tests map to the sixteen validation requirements.
"""

import os
import sqlite3
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

from sourcelib import arabic, config, db, extract, metadata, passages as seg
from sourcelib.pages import (Page, block_split, markers_monotonic, normalize_newlines,
                             pages_from_pdftotext, parse_txt, read_text_file, render_md,
                             render_txt, strip_md_decoration, total_pdf_pages)

TEXT_DIR = config.TEXT
DB_PATH = config.DB
HAS_DB = os.path.exists(DB_PATH)


# --------------------------------------------------------------------------
# a small pdftotext-shaped document, with a blank page and some Arabic
# --------------------------------------------------------------------------

FAKE_PDF_TEXT = (
    "KITAB AL-FIXTURE\n\nA title page.\n"
    "\f"
    "\n   \n"                                       # page 2: blank, gets dropped
    "\f"
    "CHAPTER I: THE FIRST\n\n"
    "1. Imam Ali (‘a) said:\nA line of counsel that runs on\n"
    "2. Imam Ali (‘a) said:\nA second line.\n\n"
    "A paragraph that stops mid-\n"
    "\f"
    "sentence and finishes here.\n\n"
    "السَّلامُ عَلَيْكُمْ\n"
)


class FixtureCorpus:
    """Builds a complete corpus in a temp dir: sources.yaml, text, db, FTS."""

    def __init__(self, tmp):
        self.tmp = tmp
        self.text_dir = os.path.join(tmp, "text")
        os.makedirs(self.text_dir, exist_ok=True)
        self.pages = pages_from_pdftotext(FAKE_PDF_TEXT)
        self.txt = os.path.join(self.text_dir, "fixture.txt")
        with open(self.txt, "w", encoding="utf-8", newline="") as f:
            f.write(render_txt(self.pages, "\n"))
        self.db = os.path.join(tmp, "source.db")
        self._build()

    def _build(self):
        con = db.connect(self.db)
        db.create_schema(con)
        db.upsert_works(con, [{"work_id": "WRK-FIX", "work": "Kitab al-Fixture",
                               "author": "nobody", "tradition": "shia",
                               "priority_rank": 1, "note": None}])
        ed = {"source_id": "SRC-FIX-001", "work_id": "WRK-FIX", "translator": "A Translator",
              "publisher": "Fixture Press", "year": "2000", "status": "fixed",
              "pagination": "printed", "citation_unit": "page", "complete": True,
              "language": "en", "page_count": 4, "sha256": "0" * 64,
              "printed_page_offset": None, "extraction_method": "native_text"}
        db.upsert_edition(con, ed)
        db.replace_pages(con, "SRC-FIX-001", [{
            "source_id": "SRC-FIX-001", "pdf_page": p.pdf_page, "printed_page": None,
            "page_label": None, "text": normalize_newlines(p.text),
            "markdown": render_md([p]), "char_count": len(p.text),
            "arabic_char_count": arabic.arabic_char_count(p.text),
            "extraction_method": p.extraction_method, "ocr_confidence": None,
            "page_image_path": None} for p in self.pages])
        ps = seg.segment("SRC-FIX-001", self.pages)
        db.insert_passages(con, [p.as_row() for p in ps])
        db.replace_claims(con, [
            {"claim_id": "CLM-FIX-001", "claim_text": "A line of counsel", "status": "V",
             "env": "01", "item": "hadith card", "project_location": "fixture"},
            {"claim_id": "CLM-FIX-002", "claim_text": "Something unproven", "status": "TV",
             "env": "01", "item": "letter", "project_location": "fixture"},
        ], [
            {"citation_id": "CIT-FIX-001", "claim_id": "CLM-FIX-001",
             "source_id": "SRC-FIX-001", "passage_id": ps[1].passage_id, "ref": "no. 1",
             "citation_type": "page", "page_start": ps[1].pdf_page_start,
             "page_end": ps[1].pdf_page_end, "verified": 1},
        ])
        db.replace_rejected(con, metadata.load_rejected())
        db.rebuild_fts(con)
        con.commit()
        con.close()
        self.passages = ps


class PipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.fix = FixtureCorpus(cls._tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    # -- 1. extraction preserves the page count ---------------------------

    def test_01_extraction_preserves_page_count(self):
        """Every sheet is accounted for: kept, or empty and therefore dropped."""
        sheets = total_pdf_pages(FAKE_PDF_TEXT)
        self.assertEqual(sheets, 4)
        kept = [p.pdf_page for p in self.fix.pages]
        self.assertEqual(kept, [1, 3, 4])
        dropped = set(range(1, sheets + 1)) - set(kept)
        for n in dropped:
            self.assertEqual(FAKE_PDF_TEXT.split("\f")[n - 1].strip(), "",
                             "sheet %d was dropped but is not empty" % n)

    # -- 2 & 3. markers monotonic, nothing silently skipped ---------------

    def test_02_markers_monotonic(self):
        ok, problems = markers_monotonic(self.fix.pages)
        self.assertTrue(ok, problems)
        bad = [Page(5, "x"), Page(3, "y")]
        ok, problems = markers_monotonic(bad)
        self.assertFalse(ok)

    def test_03_no_page_marker_silently_skipped(self):
        """A gap in the markers is only ever an empty sheet — and the .txt file
        is the record of that, so the gap is visible, not silent."""
        with open(self.fix.txt, encoding="utf-8", newline="") as fh:
            body = fh.read()
        self.assertIn("[[p 1]]", body)
        self.assertNotIn("[[p 2]]", body)          # the blank sheet
        self.assertIn("[[p 3]]", body)
        self.assertIn("[[p 4]]", body)
        reparsed = parse_txt(body)
        self.assertEqual([p.pdf_page for p in reparsed],
                         [p.pdf_page for p in self.fix.pages])

    # -- 4. TXT and Markdown come from the same pages ---------------------

    def test_04_txt_and_md_derive_from_the_same_pages(self):
        md = render_md(self.fix.pages)
        stripped = strip_md_decoration(md)
        for p in self.fix.pages:
            self.assertIn("[[p %d]]" % p.pdf_page, md)
            for line in normalize_newlines(p.text).split("\n"):
                if line.strip():
                    self.assertIn(line.strip(), stripped,
                                  "line missing from markdown: %r" % line[:60])
        # and the markdown adds nothing but the marker, the front matter and
        # the heading prefix
        md_lines = {ln.strip() for ln in stripped.split("\n") if ln.strip()}
        txt_lines = set()
        for p in self.fix.pages:
            txt_lines.add("[[p %d]]" % p.pdf_page)
            txt_lines.update(ln.strip() for ln in normalize_newlines(p.text).split("\n")
                             if ln.strip())
        self.assertEqual(md_lines - txt_lines, set())

    def test_04b_round_trip_is_byte_identical(self):
        """Deterministic: the same pages render to the same bytes every time."""
        a = render_txt(self.fix.pages, "\n")
        b = render_txt(parse_txt(a), "\n")
        self.assertEqual(a, b)
        self.assertEqual(render_md(self.fix.pages), render_md(self.fix.pages))

    # -- 5. hashes are stable ---------------------------------------------

    def test_05_sha256_is_stable(self):
        """Same bytes, same hash, across reads and chunk boundaries. One byte
        different, different hash — which is what pins an edition."""
        import hashlib
        path = os.path.join(self.fix.tmp, "hash-me.bin")
        payload = b"noorpost" * 400_000          # bigger than the 1 MiB read chunk
        with open(path, "wb") as f:
            f.write(payload)

        expected = hashlib.sha256(payload).hexdigest()
        self.assertEqual(extract.sha256_file(path), expected)
        self.assertEqual(extract.sha256_file(path), extract.sha256_file(path))

        changed = os.path.join(self.fix.tmp, "hash-me-2.bin")
        with open(changed, "wb") as f:
            f.write(payload + b"!")
        self.assertNotEqual(extract.sha256_file(changed), expected)

        # the hashes recorded in sources.yaml agree with manifest.json, which is
        # where they came from
        _, editions, _ = metadata.load_sources()
        fetched = metadata.load_fetch_manifest()
        checked = 0
        for e in editions:
            rec = fetched.get(e.get("file") or "")
            if rec and e.get("sha256"):
                self.assertEqual(e["sha256"], rec["sha256"], e["source_id"])
                checked += 1
        self.assertGreater(checked, 0, "no edition hash could be cross-checked")

    # -- 6, 7, 8. citations and passages point at things that exist -------

    def _con(self):
        con = sqlite3.connect(self.fix.db)
        con.row_factory = sqlite3.Row
        return con

    def test_06_every_citation_points_to_an_existing_source(self):
        con = self._con()
        orphans = con.execute(
            "SELECT citation_id FROM citations c WHERE NOT EXISTS "
            "(SELECT 1 FROM editions e WHERE e.source_id = c.source_id)").fetchall()
        self.assertEqual([r["citation_id"] for r in orphans], [])

    def test_07_every_citation_points_to_an_existing_page(self):
        con = self._con()
        orphans = con.execute(
            "SELECT citation_id FROM citations c WHERE c.page_start IS NOT NULL AND NOT EXISTS "
            "(SELECT 1 FROM pages p WHERE p.source_id = c.source_id "
            " AND p.pdf_page = c.page_start)").fetchall()
        self.assertEqual([r["citation_id"] for r in orphans], [])

    def test_08_every_passage_points_to_an_existing_source_and_page(self):
        con = self._con()
        orphans = con.execute(
            "SELECT passage_id FROM passages ps WHERE NOT EXISTS "
            "(SELECT 1 FROM pages p WHERE p.source_id = ps.source_id "
            " AND p.pdf_page = ps.pdf_page_start)").fetchall()
        self.assertEqual([r["passage_id"] for r in orphans], [])
        # and a passage that spans a page break names both real pages
        for r in con.execute("SELECT * FROM passages WHERE pdf_page_end != pdf_page_start"):
            self.assertIsNotNone(con.execute(
                "SELECT 1 FROM pages WHERE source_id=? AND pdf_page=?",
                (r["source_id"], r["pdf_page_end"])).fetchone())

    # -- 9 & 10. the TV -> V state machine --------------------------------

    def test_09_every_V_claim_has_a_valid_citation(self):
        works, editions, by_id = metadata.load_sources()
        claims = metadata.load_claims()
        citations = metadata.load_citations()
        problems = [p for p in metadata.validate(works, editions, claims, citations,
                                                 metadata.load_rejected())
                    if "marked V with no usable citation" in p]
        self.assertEqual(problems, [])

    def test_10_TV_cannot_become_V_by_accident(self):
        """A V claim whose only citation names no number is rejected — which is
        what stops a TV row being promoted by adding an empty citation."""
        works, editions, _ = metadata.load_sources()
        claims = [{"claim_id": "CLM-X", "claim_text": "t", "status": "V"}]
        citations = [{"citation_id": "CIT-X", "claim_id": "CLM-X",
                      "source_id": "SRC-TAU-001", "citation_type": "page",
                      "ref": None, "page_start": None}]
        problems = metadata.validate(works, editions, claims, citations,
                                     metadata.load_rejected())
        self.assertTrue(any("no usable citation" in p for p in problems), problems)
        self.assertTrue(any("decoration" in p for p in problems), problems)

        # and nothing in tools/ writes a V status
        for name in ("build_source_corpus.py", "source_search.py", "import_citation_sheet.py",
                     "source_audit.py", "page_image.py"):
            with open(os.path.join(ROOT, "tools", name), encoding="utf-8") as fh:
                src = fh.read()
            self.assertNotIn('"status": "V"', src)
            self.assertNotIn("status='V'", src)

    # -- 11. Arabic ---------------------------------------------------------

    def test_11_arabic_raw_is_never_overwritten_by_normalisation(self):
        raw = "السَّلامُ"   # with diacritics
        norm = arabic.normalize_arabic(raw)
        self.assertNotEqual(raw, norm)
        self.assertIn("َ", raw)          # fatha still there
        self.assertNotIn("َ", norm)      # and gone from the search form only

        con = self._con()
        rows = con.execute("SELECT arabic_raw, arabic_normalized, arabic_verified, "
                           "quotation_ready FROM passages "
                           "WHERE arabic_raw IS NOT NULL").fetchall()
        self.assertTrue(rows, "the fixture should carry an Arabic passage")
        for r in rows:
            self.assertNotEqual(r["arabic_raw"], r["arabic_normalized"])
            self.assertIn("ّ", r["arabic_raw"])       # shadda preserved
            self.assertEqual(r["arabic_verified"], 0)
            self.assertEqual(r["quotation_ready"], 0)

        # re-running the segmenter must not alter the raw text
        again = seg.segment("SRC-FIX-001", self.fix.pages)
        first = [p.arabic_raw for p in self.fix.passages if p.arabic_raw]
        second = [p.arabic_raw for p in again if p.arabic_raw]
        self.assertEqual(first, second)

    def test_11b_no_arabic_is_manufactured(self):
        for p in self.fix.passages:
            if p.arabic_raw is None:
                self.assertIsNone(p.arabic_normalized)
            else:
                self.assertIn(p.arabic_raw.strip(), p.text)

    def test_11c_glyph_damage_is_detected_not_assumed(self):
        """A PDF that hands over positioned glyphs leaves private-use
        codepoints and bidi controls through its Arabic. That is measurable,
        and it is what marks an edition's Arabic unusable."""
        clean = "السلام عليكم"
        damaged = "‫السلام‬ ‏عليكم"
        self.assertFalse(arabic.has_broken_glyphs(clean))
        self.assertTrue(arabic.has_broken_glyphs(damaged))
        self.assertEqual(arabic.glyph_damage_ratio([clean, clean]), 0.0)
        self.assertEqual(arabic.glyph_damage_ratio([clean, damaged]), 0.5)
        self.assertEqual(arabic.glyph_damage_ratio([]), 0.0)

        # damaged text is never quotation-ready, whatever else is true of it
        pages = [Page(1, "An English line with ‫عربي‬ inside it.")]
        ps = seg.segment("SRC-DMG-001", pages)
        self.assertEqual(ps[0].quotation_ready, 0)
        self.assertEqual(ps[0].arabic_verified, 0)
        self.assertGreater(ps[0].arabic_char_count, 0)

    @unittest.skipUnless(HAS_DB, "run tools/build_source_corpus.py first")
    def test_11d_real_corpus_arabic_is_flagged_unusable(self):
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        rows = con.execute("SELECT source_id, arabic_extraction, arabic_passages "
                           "FROM editions WHERE arabic_passages > 0").fetchall()
        self.assertTrue(rows, "the corpus should carry Arabic")
        for r in rows:
            self.assertIn(r["arabic_extraction"], ("ok", "suspect", "unusable"))
        # nothing whose register is Arabic is offered as quotable, and neither
        # is anything carrying glyph damage
        self.assertEqual(con.execute(
            "SELECT COUNT(*) c FROM passages WHERE register = 'arabic' "
            "AND quotation_ready = 1").fetchone()["c"], 0)
        for r in con.execute("SELECT text FROM passages WHERE quotation_ready = 1 "
                             "AND COALESCE(arabic_char_count,0) > 0"):
            self.assertFalse(arabic.has_broken_glyphs(r["text"]),
                             "damaged text offered as quotable")
        con.close()

    # -- 12. rejected sources ----------------------------------------------

    def test_12_rejected_sources_cannot_appear_in_the_active_manifest(self):
        rejected = metadata.load_rejected()
        self.assertTrue(rejected, "rejected.yaml must list the removed works")
        keys = {r["key"] for r in rejected}
        self.assertIn("sira-guillaume", keys)
        self.assertIn("tabari", keys)

        works, editions, _ = metadata.load_sources()
        for e in editions:
            self.assertFalse(
                metadata.is_rejected(name=e.get("work"), filename=e.get("file"),
                                     sha256=e.get("sha256")),
                "%s is a rejected work but is in sources.yaml" % e["source_id"])

        # by hash, under any filename
        guillaume = ("15da6fccf1cc034b59e28e9e5dfed0093fb03c2d55aa24efd3ad900406c24461")
        self.assertTrue(metadata.is_rejected(sha256=guillaume))
        self.assertTrue(metadata.is_rejected(sha256=guillaume.upper()))
        self.assertTrue(metadata.is_rejected(filename="innocent-name.pdf",
                                             sha256=guillaume))
        self.assertTrue(metadata.is_rejected(name="The History of al-Tabari"))

        # validate() must reject an attempt to put one back
        bad = list(editions) + [{
            "source_id": "SRC-BAD-001", "work_id": "WRK-TAU", "work": "The History of al-Tabari",
            "status": "fixed", "pagination": "printed", "citation_unit": "page",
            "translator": "Michael Fishbein", "complete": True}]
        problems = metadata.validate(works, bad, [], [], rejected)
        self.assertTrue(any("rejected list" in p for p in problems), problems)

        # and the fetcher will not go looking for one
        with open(os.path.join(ROOT, "tools", "fetch_sources.py"), encoding="utf-8") as fh:
            fetch = fh.read()
        self.assertIn("rejected=True", fetch)
        self.assertIn("REFUSED", fetch)

    def test_12b_rejected_sources_are_not_in_the_corpus(self):
        con = self._con()
        rows = con.execute("SELECT DISTINCT source_id FROM passages").fetchall()
        for r in rows:
            self.assertFalse(metadata.is_rejected(name=r["source_id"]))
        for t in ("guillaume", "tabari", "ibn ishaq"):
            hit = con.execute("SELECT COUNT(*) c FROM editions WHERE lower(file) LIKE ?",
                              ("%" + t + "%",)).fetchone()["c"]
            self.assertEqual(hit, 0, "a rejected file is recorded as an edition")

    # -- 13. retrieval exposes provenance ----------------------------------

    def test_13_retrieval_results_expose_page_provenance(self):
        import source_search
        con = self._con()
        eds = source_search.edition_map(con)
        row = con.execute("SELECT * FROM passages WHERE passage_id = ?",
                          (self.fix.passages[1].passage_id,)).fetchone()
        shaped = source_search.shape(row, eds["SRC-FIX-001"])
        for key in ("passage_id", "source_id", "work", "edition", "locator", "citation",
                    "extraction_method", "quotation_ready", "citation_ready"):
            self.assertIn(key, shaped)
        self.assertIsNotNone(shaped["locator"]["pdf_page_start"])
        self.assertIn("SRC-FIX-001", shaped["citation"])
        self.assertIn(str(shaped["locator"]["pdf_page_start"]), shaped["citation"])

    def test_13b_uncitable_pagination_is_reported(self):
        import source_search
        ed = {"source_id": "SRC-WEB-001", "work": "W", "pagination": "web-generated",
              "citation_unit": "internal-number", "status": "fixed", "translator": "T"}
        row = {"pdf_page_start": 7, "pdf_page_end": 7, "printed_page_start": None,
               "printed_page_end": None, "internal_ref": None, "section": None,
               "passage_id": "SRC-WEB-001-0007-001", "quotation_ready": 1,
               "extraction_method": "native_text"}
        loc = source_search.locator(ed, row)
        self.assertFalse(loc["page_citable"])
        self.assertIn("pagination_warning", loc)
        ok, blockers = source_search.citation_ready(ed, row)
        self.assertFalse(ok)

    # -- 14. generated prose is never evidence ------------------------------

    def test_14_generated_prose_is_not_indexed(self):
        """The corpus is built only from files named in sources.yaml, all of
        which live under 00-sources/."""
        _, editions, _ = metadata.load_sources()
        for e in editions:
            for key in ("text_file", "file"):
                path = e.get(key)
                if not path:
                    continue
                norm = path.replace("\\", "/")
                self.assertFalse(os.path.isabs(norm))
                if key == "text_file":
                    self.assertTrue(norm.startswith("00-sources/"),
                                    "%s ingests from outside 00-sources/: %s"
                                    % (e["source_id"], norm))

        with open(os.path.join(ROOT, "tools", "build_source_corpus.py"),
                  encoding="utf-8") as fh:
            builder = fh.read()
        for forbidden in ("01-pilot", "03-content", "08-companions", "09-zines", "docs/"):
            self.assertNotIn('"%s' % forbidden, builder)

    @unittest.skipUnless(HAS_DB, "run tools/build_source_corpus.py first")
    def test_14b_no_draft_prose_in_the_real_corpus(self):
        """A sentence that exists only in a draft letter must not be findable."""
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        canary = "Makkah was hot that year"
        letter = os.path.join(ROOT, "01-pilot", "envelope-03", "letter.md")
        with open(letter, encoding="utf-8") as fh:
            self.assertIn(canary, fh.read(),
                          "canary sentence changed — pick another from the draft")
        hits = con.execute("SELECT COUNT(*) c FROM passages WHERE text LIKE ?",
                           ("%" + canary + "%",)).fetchone()["c"]
        self.assertEqual(hits, 0, "draft prose is in the source index")

        for r in con.execute("SELECT DISTINCT text_file f FROM editions "
                             "WHERE text_file IS NOT NULL"):
            self.assertTrue(r["f"].startswith("00-sources/"))
        con.close()

    # -- image-only PDFs and OCR --------------------------------------------

    def test_15_image_only_pdf_is_detected(self):
        sheets = 40
        thin = pages_from_pdftotext("\f".join(["  1  "] * sheets))
        self.assertTrue(extract.looks_image_only(thin, sheets))
        fat = pages_from_pdftotext("\f".join(["x" * 2000] * sheets))
        self.assertFalse(extract.looks_image_only(fat, sheets))

    def test_15b_ocr_passages_are_not_quotation_ready(self):
        pages = [Page(1, "Some text a scanner read.", extraction_method="ocr",
                      ocr_confidence=81.4)]
        ps = seg.segment("SRC-OCR-001", pages, extraction_status="ocr-unverified")
        self.assertTrue(ps)
        for p in ps:
            self.assertEqual(p.extraction_method, "ocr")
            self.assertEqual(p.quotation_ready, 0)
            self.assertEqual(p.extraction_status, "ocr-unverified")

    def test_15c_ocr_provenance_fields_exist(self):
        for col in ("extraction_method", "ocr_engine", "ocr_engine_version",
                    "ocr_confidence", "ocr_timestamp"):
            self.assertIn(col, db.SCHEMA)

    # -- 16. metadata validity ---------------------------------------------

    def test_16_repository_metadata_validates(self):
        works, editions, _ = metadata.load_sources()
        problems = metadata.validate(works, editions, metadata.load_claims(),
                                     metadata.load_citations(), metadata.load_rejected())
        self.assertEqual(problems, [], "\n".join(problems))

    def test_16b_no_incomplete_edition_is_marked_fixed(self):
        _, editions, _ = metadata.load_sources()
        for e in editions:
            if e.get("status") == "fixed":
                self.assertNotEqual(e.get("complete"), False, e["source_id"])
                self.assertTrue(e.get("translator"), e["source_id"])

    def test_16c_passage_ids_are_stable_across_runs(self):
        a = [p.passage_id for p in seg.segment("SRC-FIX-001", self.fix.pages)]
        b = [p.passage_id for p in seg.segment("SRC-FIX-001", self.fix.pages)]
        self.assertEqual(a, b)
        self.assertEqual(len(a), len(set(a)), "passage ids must be unique")
        for pid in a:
            self.assertRegex(pid, r"^SRC-FIX-001-\d{4}-\d{3}$")

    def test_16d_no_metadata_is_fabricated(self):
        """Anything the pipeline could not read off the page is NULL, and
        anything it did read is stamped so a reviewer can tell."""
        for p in self.fix.passages:
            self.assertIsNone(p.subject)
            self.assertIn(p.passage_type, seg.PASSAGE_TYPES)
            if p.speaker or p.passage_type != "unknown":
                self.assertEqual(p.metadata_source, "detected-pattern")
                if p.speaker:
                    self.assertIn(p.speaker, p.text)
            else:
                self.assertIsNone(p.metadata_source)

    def test_16e_printed_page_is_never_guessed(self):
        for p in self.fix.passages:
            self.assertIsNone(p.printed_page_start)
        for pg in self.fix.pages:
            self.assertIsNone(pg.printed_page)


# --------------------------------------------------------------------------
# the real corpus
# --------------------------------------------------------------------------

class RealCorpusTest(unittest.TestCase):

    def test_text_corpus_round_trips_byte_for_byte(self):
        """Every file in 00-sources/text/ can enter the pipeline and come back
        unchanged. This is what makes the migration safe."""
        files = sorted(f for f in os.listdir(TEXT_DIR) if f.endswith(".txt"))
        self.assertTrue(files)
        for name in files:
            path = os.path.join(TEXT_DIR, name)
            body, newline = read_text_file(path)
            pages = parse_txt(body)
            self.assertEqual(render_txt(pages, newline), body,
                             "%s does not round-trip" % name)
            ok, problems = markers_monotonic(pages)
            self.assertTrue(ok, "%s: %s" % (name, problems))

    @unittest.skipUnless(HAS_DB, "run tools/build_source_corpus.py first")
    def test_real_corpus_invariants(self):
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row

        # every passage lands on a page that exists
        self.assertEqual(con.execute(
            "SELECT COUNT(*) c FROM passages ps WHERE NOT EXISTS "
            "(SELECT 1 FROM pages p WHERE p.source_id=ps.source_id "
            " AND p.pdf_page=ps.pdf_page_start)").fetchone()["c"], 0)

        # every page belongs to a known edition
        self.assertEqual(con.execute(
            "SELECT COUNT(*) c FROM pages p WHERE NOT EXISTS "
            "(SELECT 1 FROM editions e WHERE e.source_id=p.source_id)").fetchone()["c"], 0)

        # every citation names a real edition, and a real page when it names one
        self.assertEqual(con.execute(
            "SELECT COUNT(*) c FROM citations ct WHERE NOT EXISTS "
            "(SELECT 1 FROM editions e WHERE e.source_id=ct.source_id)").fetchone()["c"], 0)
        self.assertEqual(con.execute(
            "SELECT COUNT(*) c FROM citations ct WHERE ct.page_start IS NOT NULL "
            "AND NOT EXISTS (SELECT 1 FROM pages p WHERE p.source_id=ct.source_id "
            "AND p.pdf_page=ct.page_start)").fetchone()["c"], 0)

        # every citation that names a passage names one that exists
        self.assertEqual(con.execute(
            "SELECT COUNT(*) c FROM citations ct WHERE ct.passage_id IS NOT NULL "
            "AND NOT EXISTS (SELECT 1 FROM passages p "
            "WHERE p.passage_id=ct.passage_id)").fetchone()["c"], 0)

        # no Arabic passage is quotation-ready, and none has been normalised in place
        self.assertEqual(con.execute(
            "SELECT COUNT(*) c FROM passages WHERE arabic_raw IS NOT NULL "
            "AND quotation_ready = 1").fetchone()["c"], 0)
        self.assertEqual(con.execute(
            "SELECT COUNT(*) c FROM passages WHERE arabic_raw IS NOT NULL "
            "AND arabic_raw = arabic_normalized").fetchone()["c"], 0)

        # markers are monotonic per edition
        for r in con.execute("SELECT DISTINCT source_id FROM pages"):
            pages = [row["pdf_page"] for row in con.execute(
                "SELECT pdf_page FROM pages WHERE source_id=? ORDER BY rowid", (r[0],))]
            self.assertEqual(pages, sorted(pages), "%s markers out of order" % r[0])
            self.assertEqual(len(pages), len(set(pages)))
        con.close()

    @unittest.skipUnless(HAS_DB, "run tools/build_source_corpus.py first")
    def test_search_boundary_is_the_source_library(self):
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        rejected = con.execute("SELECT COUNT(*) c FROM passages p JOIN editions e "
                               "ON e.source_id=p.source_id "
                               "WHERE e.status='rejected'").fetchone()["c"]
        self.assertEqual(rejected, 0)
        con.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
