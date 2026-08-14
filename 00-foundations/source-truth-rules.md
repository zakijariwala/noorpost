# Source truth rules

What counts as evidence in this project, and what does not. `sourcing-rules.md`
says which works may be cited; this says what a citation has to be able to
prove. Every rule below is enforced somewhere in `tools/`, and the enforcement
point is named.

---

## The twelve rules

### 1. The raw PDF is immutable

The original is opened read-only and never written to, moved, or replaced.
Everything else — the `[[p N]]` text, the Markdown, the passages, the database
— is a derivative, and any of it can be deleted and rebuilt.

> `tools/sourcelib/extract.py` only ever reads. OCR writes a derivative; it
> never produces a new PDF.

### 2. A fixed edition is identified by `source_id` **and** SHA-256

`SRC-TAU-001` names an edition. The hash pins which copy of it. Two copies of
the same translation paginate differently, so an edition without a hash is not
pinned and its page numbers are not trustworthy.

> `00-sources/metadata/sources.yaml`; `build_source_corpus.py --hash-originals`
> fills the hash and warns if a recorded one has changed. `source_audit.py`
> lists editions with no hash.

### 3. Page numbers are never inferred from chunk positions

A passage carries the page it was cut from, taken from the `[[p N]]` marker.
No page is ever computed from an offset into a chunk, and `printed_page` is
only ever set from an offset a human recorded — never guessed.

> `tools/sourcelib/passages.py`. Tests 7 and 8.

**And a page number is not always citable.** Each edition records how it
paginates:

| `pagination` | What `[[p N]]` is | Cite by |
|---|---|---|
| `printed` | the printed page | the page |
| `web-generated` | an artifact of PDF generation | the work's own internal numbering |
| `two-column` | a sheet holding two book pages | the running header, checked by hand |
| `unknown` | not established | nothing, until it is |

**Every fixed edition in this project today is `web-generated`.** Not one of
them may be cited by page. That is why `internal_ref` exists.

### 4. Generated prose is never evidence

The retrieval index covers `00-sources/` and nothing else. Letters, fact
panels, envelopes, zines, companion files, READMEs and this document are not
searched, because a draft that can retrieve itself proves itself.

> `build_source_corpus.py` ingests only files named in `sources.yaml`. Test 14.

### 5. Citations point at source pages

A citation names an edition and a number — a page where the edition's
pagination is the printed one, otherwise the work's own internal numbering,
which is stable across editions. **A citation with neither is not a citation.**

> `metadata.validate()`. Tests 6 and 7.

### 6. TV is not V

`TV` means believed sound and not yet checked. `V` means somebody opened the
named edition at the named place and read the line. **No tool in this
repository turns one into the other.** The importer can locate a quote on a
page; that is a location, not a verification.

> `metadata.validate()` refuses a `V` claim with no usable citation. Tests 9
> and 10. Nothing in `tools/` writes `status: V`.

### 7. Arabic raw text is immutable

`arabic_raw` is the Arabic exactly as extracted. Normalisation produces a
*separate* string in `arabic_normalized`, for search only. Diacritics are never
stripped from the raw text, nothing is transliterated into it, nothing is
"corrected", and Arabic is never manufactured for a source that does not carry
it.

> `tools/sourcelib/arabic.py`. Test 11.

### 8. Arabic extraction is flagged for visual verification

Every Arabic passage in this corpus starts `arabic_verified: false`. The
extracted Arabic here is reordered by the PDFs' font encodings and is visibly
wrong as a quotation. Only a person comparing it with the page image can clear
it.

> `tools/page_image.py --source SRC-NHB-002 --page 35`

### 9. Shia claims may only cite permitted Shia sources

The hard rule in `sourcing-rules.md`, in data.

> Every edition in `sources.yaml` is Shia. `metadata.validate()` fails if a
> rejected work appears with an active status.

### 10. Rejected sources stay excluded from active retrieval

Guillaume's Ibn Ishaq and both al-Tabari volumes were removed on 2026-08-12 and
are not coming back. They are recorded in `00-sources/metadata/rejected.yaml`
as a **denylist**, with their SHA-256s, so a re-downloaded copy is refused
under any filename.

> Refused at four points: `fetch_sources.py` (target and download),
> `extract_text.py`, `build_source_corpus.py`, `page_image.py`. Retrieval
> filters on edition status. Test 12.

### 11. Similarity can suggest evidence; it cannot establish it

There is no vector database here, and when one is added the rule stands: a
retrieval hit is a candidate for a human to check. Ranking is not verification.

### 12. An LLM cannot create a citation

An agent may find a passage, quote it, and propose a citation. The record is
written by a person editing `citation-sheet.md`. `source_search.py` assembles
the pieces of a citation and reports what is blocking it; it does not mark
anything verified.

---

## What a passage may be used for

| State | Findable | Quotable verbatim | Citable |
|---|---|---|---|
| native text, edition fixed, internal number present | yes | yes | yes |
| native text, edition fixed, no internal number, web-generated pagination | yes | yes | **no** — nothing to cite |
| native text, edition only a candidate | yes | no | **no** — no translator credit |
| Arabic, `arabic_verified: false` | yes | **no** | no |
| OCR, not visually checked | yes | **no** | no |

`source_search.py` prints the blockers on every result rather than leaving the
reader to work them out.

---

## The workflow this exists to support

1. A claim needs evidence. It is on `citation-sheet.md` as `TV`.
2. `python tools/source_search.py --claim "<the claim>"` returns candidates,
   each with its edition, page and passage id.
3. The reviewer opens the exact page —
   `python tools/page_image.py --source SRC-X --page N` — and reads it.
4. For Arabic, the page image is not optional.
5. The reviewer decides. A tool cannot.
6. The row on `citation-sheet.md` becomes `V`, with the edition, the number and
   the translator.
7. `python tools/import_citation_sheet.py` puts it in the database.
8. `python tools/build_source_corpus.py --validate-only` checks it holds.
9. The generation agent is given the approved claim, the approved passage and
   the citation metadata — never the book, and never its own earlier prose.
