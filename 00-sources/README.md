# The source library

Everything an evidence claim in this project may rest on. Nothing else in the
repository is evidence — not the letters, not the fact panels, not the zines,
not this file.

⛔ **Shia sources only.** The hard rule is in `00-foundations/sourcing-rules.md`.
What counts as evidence, and what a citation has to be able to prove, is in
`00-foundations/source-truth-rules.md`.

---

## What is here

| Path | What it is | Tracked |
|---|---|---|
| `originals/`, `*.pdf` | The original PDFs. **Immutable.** The ultimate source of truth. | no — release zip, see `HANDOVER.md` |
| `text/` | The `[[p N]]` page-marked plain text. 15 files, 6,328 pages. | **yes** |
| `metadata/sources.yaml` | Works and editions. `source_id`, translator, SHA-256, pagination character, status. | **yes** |
| `metadata/rejected.yaml` | The denylist. Works that may never re-enter the project, by hash. | **yes** |
| `metadata/claims.yaml` | One record per claim that reaches print. TV → V. | **yes** |
| `metadata/citations.yaml` | One record per claim-to-source link. | **yes** |
| `manifest.json` | The fetcher's download record. Unchanged, still written by `fetch_sources.py`. | **yes** |
| `inventory.md` | The human ledger of what is present and missing. | **yes** |
| `reports/` | Generated: the source audit, and the generated citation-sheet view. | **yes** |
| `pages/` | The intermediate page representation, one JSONL per edition. | **yes** — derived, but tracked |
| `md/` | Canonical Markdown, one file per edition. | **yes** — derived, but tracked |
| `source.db` | SQLite + FTS5. The operational source of truth. | no — 182 MB, over GitHub's file limit |
| `page-images/` | Rendered pages, on request. | no — unbounded cache |

`md/` and `pages/` are tracked so a reader can open a source, and a change to
the extraction shows up as a reviewable diff. Both are byte-identical across
rebuilds, so a diff always means something changed in the pipeline or the
input. They come to 58 MB, and they hold the same page text as `text/` in two
other shapes — that redundancy is the price of being able to see them.

**One thing to know:** a `--from-pdf` build stamps `extracted_at` (and the OCR
engine version, when OCR ran) into each `pages/*.jsonl` header, so those files
will show a one-line diff even when the text is identical. The default
`--from-text` build carries no timestamp and is stable.

`source.db` cannot be tracked — GitHub refuses any single file over 100 MiB.
Rebuild it in about twenty seconds. Git LFS would carry it if you ever want it
pinned to a commit.

---

## Build it

```bash
pip install -r requirements.txt        # PyYAML, and nothing else
python tools/build_source_corpus.py    # ~20 seconds
```

That reads `00-sources/text/*.txt` — the corpus already in the repository — and
produces the pages, the Markdown, the passage database and the search index.
**No PDFs and no poppler needed.**

On a machine that has the PDFs:

```bash
python tools/build_source_corpus.py --hash-originals   # pin each edition by SHA-256
python tools/build_source_corpus.py --from-pdf         # re-extract from the originals
python tools/build_source_corpus.py --from-pdf --ocr   # ...OCRing any image-only PDF
```

## Search it

```bash
python tools/source_search.py "Yahya ibn Aktham"
python tools/source_search.py --claim "Makkah called him al-Amin before revelation"
python tools/source_search.py "Shurayh" --source SRC-NHB-002 --json
python tools/source_search.py --page SRC-TAU-001:142
```

## Look at the original page

```bash
python tools/page_image.py --source SRC-NHB-002 --page 35
```

Needed for every Arabic passage before it is quoted. The extracted Arabic in
this corpus is reordered by the PDFs' font encodings and is not fit to quote.

## Check its state

```bash
python tools/source_audit.py --write        # reports/source-audit.md
python tools/render_citation_sheet.py       # compare the sheet with the database
python -m unittest discover -s tests
```

---

## The pipeline

```
original PDF                     immutable, never written to
   ↓  pdftotext -layout          (or: render at 300 dpi → tesseract, if there is no native text)
intermediate pages               pages/SRC-X.pages.jsonl
   ↓
   ├──→ text/*.txt               the [[p N]] corpus — byte-identical to what extract_text.py writes
   ├──→ md/SRC-X.md              canonical Markdown, page boundaries preserved
   └──→ source.db                pages → passages → FTS5
                                    ↑
                       metadata/*.yaml — editions, claims, citations
```

**TXT and Markdown are never extracted separately.** Both are functions of the
same list of pages, which is what makes them provably consistent.

---

## Migrating from `00-sources/text/`

Nothing to migrate. The existing corpus **is** the input, and it is not
modified.

* `parse_txt()` reads the `[[p N]]` markers back into pages, and
  `render_txt()` reproduces every one of the 15 files byte for byte — including
  their `\r\r\n` line endings, which are an artifact of the machine they were
  extracted on. There is a test for this.
* Page markers are monotonic but **not contiguous**: `extract_text.py` drops a
  page holding no text, and always has. A gap is an empty sheet, not a lost
  page.
* `grep` over `00-sources/text/` still works exactly as `HANDOVER.md` describes.
  The database is an addition, not a replacement.
* Every edition record names its `text_file`, so the link between an old
  filename and a new `source_id` is in `metadata/sources.yaml`.

| Old identity | New identity |
|---|---|
| `tuhaf_al-uqul.txt` | `SRC-TAU-001` |
| `nahjul_balagha_part_1_-_the_sermons.txt` | `SRC-NHB-001` |
| `nahjul_balagha_part_2_letters_and_sayings.txt` | `SRC-NHB-002` |
| `as-sahifa_al-kamilah_al-sajjadiyya_.txt` | `SRC-SAJ-001` |
| `treatise_on_rights_risalat_al-huquq.txt` | `SRC-RHU-001` |
| `uyun_akhbar_ar-ridha_volume_1.txt` / `_2.txt` | `SRC-UYR-001` / `SRC-UYR-002` |
| `kafi--alkafi-201601.txt` | `SRC-KAF-001` |
| `irshad--kitab-al-irshad-1.txt` / `-part-1.txt` | `SRC-IRS-001` / `SRC-IRS-002` |
| `sira-subhani--the-message-201506.txt` | `SRC-MSG-001` |
| `qarashi--...-al-kazim.txt` / `...-mahdi-a-s.txt` | `SRC-QAR-001` / `SRC-QAR-002` |
| `fourteen--the-fourteen-infallibles.txt` | `SRC-FTI-001` |
| `fourteen--nuqoosh-e-ismat-...txt` | `SRC-NQI-001` |

---

## Two things to know before citing anything

### The Arabic in this corpus cannot be quoted

Every Arabic-carrying edition here — Nahj al-Balagha, both Uyun volumes, the
Sahifa, Risalat al-Huquq, al-Kafi — extracts its Arabic as **positioned glyphs,
not text**: private-use codepoints and bidirectional controls run through the
middle of every Arabic run, in visual order, split across fragments. It is
preserved verbatim in `arabic_raw` and is never overwritten, but it is not fit
to quote and searching it will mostly fail.

The pipeline measures this rather than assuming it (`arabic_extraction:
unusable` on the edition, `arabic_verified: false` and `quotation_ready: false`
on every such passage), and `source_search.py` says so on every result.

Fixing it needs the original PDFs and tesseract:

```bash
python tools/build_source_corpus.py --from-pdf --ocr --force-ocr \
    --ocr-lang ara+eng --only SRC-NHB-002
```

OCR output is derived evidence and starts `quotation_ready: false` too — it has
to be checked against the page image before anything is quoted from it.

**None of this affects the English**, which is what every current claim rests
on.

### No edition has citable page numbers

**Not one edition in this project has citable page numbers today.** Every fixed
edition is a web-generated al-islam.org PDF whose pagination is an artifact of
generation, and `kafi--alkafi-201601` is a two-column scan whose `[[p N]]` is a
sheet number covering two book pages.

The pipeline records this per edition as `pagination` and `citation_unit`, and
`source_search.py` prints the warning on every result. Cite the work's own
internal numbering — `no. 43`, `Letter 53`, `entry 3` — which is what
`internal_ref` on a passage carries, and which is stable across editions.
