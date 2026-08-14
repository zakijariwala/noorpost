"""The SQLite schema, ingestion, and the FTS5 index.

00-sources/source.db is the operational source of truth. The raw PDF remains
the ultimate one — every row here carries the edition and the page that lets a
reviewer go back to it.

Nothing outside 00-sources/ is ever ingested. That boundary is what stops a
draft letter becoming evidence for itself.
"""

import os
import sqlite3

from . import config

SCHEMA = """
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);

-- the work, independent of any printing of it
CREATE TABLE IF NOT EXISTS sources (
    work_id       TEXT PRIMARY KEY,
    work          TEXT NOT NULL,
    author        TEXT,
    tradition     TEXT,
    priority_rank INTEGER,
    note          TEXT
);

-- the physical thing a page number belongs to. source_id identifies an
-- edition, because that is what a citation has to name.
CREATE TABLE IF NOT EXISTS editions (
    source_id          TEXT PRIMARY KEY,
    work_id            TEXT NOT NULL REFERENCES sources(work_id),
    volume             INTEGER,
    volume_title       TEXT,
    translator         TEXT,
    publisher          TEXT,
    year               TEXT,
    edition            TEXT,
    language           TEXT,
    file               TEXT,
    sha256             TEXT,
    page_count         INTEGER,
    text_file          TEXT,
    pagination         TEXT,
    citation_unit      TEXT,
    permission         TEXT,
    status             TEXT NOT NULL,
    complete           INTEGER,
    notes              TEXT,
    extraction_method  TEXT,
    extraction_status  TEXT,
    ocr_engine         TEXT,
    ocr_engine_version TEXT,
    ocr_confidence     REAL,
    ocr_timestamp      TEXT,
    printed_page_offset INTEGER,
    pipeline_version   TEXT,
    ingested_pages     INTEGER,
    arabic_extraction  TEXT,
    arabic_passages    INTEGER
);

CREATE TABLE IF NOT EXISTS pages (
    source_id         TEXT NOT NULL REFERENCES editions(source_id),
    pdf_page          INTEGER NOT NULL,
    printed_page      INTEGER,
    page_label        TEXT,
    text              TEXT NOT NULL,
    markdown          TEXT,
    char_count        INTEGER,
    arabic_char_count INTEGER,
    extraction_method TEXT,
    ocr_confidence    REAL,
    page_image_path   TEXT,
    PRIMARY KEY (source_id, pdf_page)
);

CREATE TABLE IF NOT EXISTS passages (
    passage_id         TEXT PRIMARY KEY,
    source_id          TEXT NOT NULL REFERENCES editions(source_id),
    pdf_page_start     INTEGER NOT NULL,
    pdf_page_end       INTEGER NOT NULL,
    printed_page_start INTEGER,
    printed_page_end   INTEGER,
    ordinal            INTEGER,
    section            TEXT,
    chapter            TEXT,
    title              TEXT,
    speaker            TEXT,
    subject            TEXT,
    passage_type       TEXT NOT NULL DEFAULT 'unknown',
    register           TEXT,
    arabic_raw         TEXT,
    arabic_normalized  TEXT,
    english            TEXT,
    text               TEXT NOT NULL,
    arabic_verified    INTEGER,
    extraction_method  TEXT,
    extraction_status  TEXT,
    quotation_ready    INTEGER,
    char_count         INTEGER,
    internal_ref       TEXT,
    metadata_source    TEXT,
    arabic_char_count  INTEGER,
    FOREIGN KEY (source_id, pdf_page_start) REFERENCES pages(source_id, pdf_page)
);

CREATE INDEX IF NOT EXISTS ix_passages_src_page ON passages(source_id, pdf_page_start);
CREATE INDEX IF NOT EXISTS ix_passages_type ON passages(passage_type);
CREATE INDEX IF NOT EXISTS ix_passages_speaker ON passages(speaker);
CREATE INDEX IF NOT EXISTS ix_passages_ref ON passages(source_id, internal_ref);

CREATE TABLE IF NOT EXISTS claims (
    claim_id         TEXT PRIMARY KEY,
    project_location TEXT,
    env              TEXT,
    item             TEXT,
    claim_text       TEXT NOT NULL,
    status           TEXT NOT NULL,
    work_hint        TEXT,
    ref_hint         TEXT,
    translator_hint  TEXT,
    notes            TEXT,
    created_from     TEXT
);

CREATE TABLE IF NOT EXISTS citations (
    citation_id   TEXT PRIMARY KEY,
    claim_id      TEXT REFERENCES claims(claim_id),
    source_id     TEXT REFERENCES editions(source_id),
    passage_id    TEXT REFERENCES passages(passage_id),
    ref           TEXT,
    citation_type TEXT,
    page_start    INTEGER,
    page_end      INTEGER,
    quote         TEXT,
    translator    TEXT,
    verified      INTEGER,
    notes         TEXT
);

CREATE INDEX IF NOT EXISTS ix_citations_claim ON citations(claim_id);
CREATE INDEX IF NOT EXISTS ix_citations_source ON citations(source_id);

-- kept so the guard can refuse them by hash, never as sources
CREATE TABLE IF NOT EXISTS rejected_sources (
    key        TEXT PRIMARY KEY,
    work       TEXT,
    reason     TEXT,
    decided_on TEXT,
    sha256     TEXT,
    files      TEXT
);

CREATE VIEW IF NOT EXISTS v_editions AS
SELECT e.*, s.work, s.author, s.tradition, s.priority_rank
FROM editions e JOIN sources s ON s.work_id = e.work_id;
"""

FTS = """
DROP TABLE IF EXISTS passages_fts;
CREATE VIRTUAL TABLE passages_fts USING fts5(
    text, english, arabic_raw, arabic_normalized,
    speaker, subject, chapter, section, title, internal_ref,
    content='passages', content_rowid='rowid',
    tokenize="unicode61 remove_diacritics 2"
);
INSERT INTO passages_fts(rowid, text, english, arabic_raw, arabic_normalized,
                         speaker, subject, chapter, section, title, internal_ref)
SELECT rowid, text, english, arabic_raw, arabic_normalized,
       speaker, subject, chapter, section, title, internal_ref
FROM passages;
"""


def connect(path=None, readonly=False):
    path = path or config.DB
    if readonly:
        if not os.path.exists(path):
            raise FileNotFoundError(
                "%s does not exist — run: python tools/build_source_corpus.py" % path)
        con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def create_schema(con):
    con.executescript(SCHEMA)


def set_meta(con, key, value):
    con.execute("INSERT INTO meta(key,value) VALUES(?,?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))


def get_meta(con, key, default=None):
    r = con.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return r["value"] if r else default


# --------------------------------------------------------------------------
# ingest
# --------------------------------------------------------------------------

def upsert_works(con, works):
    con.executemany(
        "INSERT INTO sources(work_id,work,author,tradition,priority_rank,note) "
        "VALUES(:work_id,:work,:author,:tradition,:priority_rank,:note) "
        "ON CONFLICT(work_id) DO UPDATE SET work=excluded.work, author=excluded.author, "
        "tradition=excluded.tradition, priority_rank=excluded.priority_rank, note=excluded.note",
        [{"work_id": w["work_id"], "work": w.get("work"), "author": w.get("author"),
          "tradition": w.get("tradition"), "priority_rank": w.get("priority_rank"),
          "note": w.get("note")} for w in works])


EDITION_COLS = ("source_id", "work_id", "volume", "volume_title", "translator", "publisher",
                "year", "edition", "language", "file", "sha256", "page_count", "text_file",
                "pagination", "citation_unit", "permission", "status", "complete", "notes",
                "extraction_method", "extraction_status", "ocr_engine", "ocr_engine_version",
                "ocr_confidence", "ocr_timestamp", "printed_page_offset", "pipeline_version",
                "ingested_pages", "arabic_extraction", "arabic_passages")


def upsert_edition(con, e):
    row = {c: e.get(c) for c in EDITION_COLS}
    if row.get("complete") is not None:
        row["complete"] = 1 if row["complete"] else 0
    if row.get("year") is not None:
        row["year"] = str(row["year"])
    cols = ",".join(EDITION_COLS)
    binds = ",".join(":" + c for c in EDITION_COLS)
    updates = ",".join("%s=excluded.%s" % (c, c) for c in EDITION_COLS if c != "source_id")
    con.execute("INSERT INTO editions(%s) VALUES(%s) ON CONFLICT(source_id) DO UPDATE SET %s"
                % (cols, binds, updates), row)


def replace_pages(con, source_id, rows):
    con.execute("DELETE FROM passages WHERE source_id=?", (source_id,))
    con.execute("DELETE FROM pages WHERE source_id=?", (source_id,))
    con.executemany(
        "INSERT INTO pages(source_id,pdf_page,printed_page,page_label,text,markdown,"
        "char_count,arabic_char_count,extraction_method,ocr_confidence,page_image_path) "
        "VALUES(:source_id,:pdf_page,:printed_page,:page_label,:text,:markdown,"
        ":char_count,:arabic_char_count,:extraction_method,:ocr_confidence,:page_image_path)",
        rows)


PASSAGE_COLS = ("passage_id", "source_id", "pdf_page_start", "pdf_page_end",
                "printed_page_start", "printed_page_end", "ordinal", "section", "chapter",
                "title", "speaker", "subject", "passage_type", "register", "arabic_raw",
                "arabic_normalized", "english", "text", "arabic_verified",
                "extraction_method", "extraction_status", "quotation_ready", "char_count",
                "internal_ref", "metadata_source", "arabic_char_count")


def insert_passages(con, rows):
    cols = ",".join(PASSAGE_COLS)
    binds = ",".join(":" + c for c in PASSAGE_COLS)
    con.executemany("INSERT INTO passages(%s) VALUES(%s)" % (cols, binds), rows)


def replace_claims(con, claims, citations):
    con.execute("DELETE FROM citations")
    con.execute("DELETE FROM claims")
    con.executemany(
        "INSERT INTO claims(claim_id,project_location,env,item,claim_text,status,"
        "work_hint,ref_hint,translator_hint,notes,created_from) "
        "VALUES(:claim_id,:project_location,:env,:item,:claim_text,:status,"
        ":work_hint,:ref_hint,:translator_hint,:notes,:created_from)",
        [{k: c.get(k) for k in ("claim_id", "project_location", "env", "item", "claim_text",
                                "status", "work_hint", "ref_hint", "translator_hint",
                                "notes", "created_from")} for c in claims])
    con.executemany(
        "INSERT INTO citations(citation_id,claim_id,source_id,passage_id,ref,citation_type,"
        "page_start,page_end,quote,translator,verified,notes) "
        "VALUES(:citation_id,:claim_id,:source_id,:passage_id,:ref,:citation_type,"
        ":page_start,:page_end,:quote,:translator,:verified,:notes)",
        [{k: c.get(k) for k in ("citation_id", "claim_id", "source_id", "passage_id", "ref",
                                "citation_type", "page_start", "page_end", "quote",
                                "translator", "verified", "notes")} for c in citations])


def replace_rejected(con, rejected):
    con.execute("DELETE FROM rejected_sources")
    con.executemany(
        "INSERT INTO rejected_sources(key,work,reason,decided_on,sha256,files) "
        "VALUES(?,?,?,?,?,?)",
        [(r.get("key"), r.get("work"), r.get("reason"), str(r.get("decided_on")),
          " ".join(r.get("sha256", []) or []), " ".join(r.get("files", []) or []))
         for r in rejected])


def rebuild_fts(con):
    con.executescript(FTS)
