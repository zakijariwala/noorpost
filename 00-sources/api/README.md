# The Thaqalayn snapshots

Thirty-two Shia hadith collections, 32,531 records, every one with a named
translator. Retrieved from [thaqalayn.net](https://thaqalayn.net) through
[thaqalayn-api.net](https://github.com/MohammedArab1/ThaqalaynAPI) and **pinned**.

**Approved as a source of record on 2026-08-24.** What that approval does and
does not settle is in `00-foundations/sourcing-rules.md` — read it before
marking anything `V`.

---

## Why the files are on disk instead of a live call

The upstream is re-scraped weekly. A citation of record cannot rest on
something that changes between two print runs, so every book is written once
and pinned by SHA-256 in `manifest.json`.

```bash
python tools/fetch_thaqalayn.py --list      # what the API advertises
python tools/fetch_thaqalayn.py             # fetch and pin
python tools/fetch_thaqalayn.py --check     # has upstream moved? writes nothing
python tools/fetch_thaqalayn.py --emit-yaml # sources.yaml rows for what is held
```

`--check` exits non-zero on drift. `build_source_corpus.py` refuses to build an
edition whose snapshot no longer hashes to the value in `sources.yaml`, so a
changed file is a stopped build, not a silently different citation.

## There are no page numbers here

Not web-generated pagination, not two-column sheets — **no pages at all**. Every
edition is stamped `pagination: api-record`, `citation_unit: hadith-number`, and
`source_search.py` prints `record N`, never `p. N`.

**The record number is not the hadith number** (corrected 2026-10-10). The API's
`id` is a running row count across the snapshot, and no edition prints it:
Man La Yahduruh al-Faqih vol. 2 record 624 is the book's hadith **2320**. The
citation is the number the book prints, read off the start of the Arabic (or the
English where the Arabic has none) by `thaqalayn.printed_number()`. Before this
was fixed, `internal_ref` carried the row id, and three companion hadith cards
were cited by it.

`internal_ref` is built by `thaqalayn.internal_refs()` over a whole snapshot:

- **Numbered straight through the volume** (Faqih): `vol. 2, hadith 2320`.
- **Numbered afresh in every chapter** (al-Kafi, Khisal, most single works):
  `vol. 4, The Book of Haj, The Case of One Who Cuts His Tawaf Short…, hadith 2`.
- **No printed number**: the position in the chapter, from the record's own URL.
- **Still not unique** (a repeated chapter title, or one report split over
  several records): the record's `thaqalayn.net/hadith/…` path is appended, then
  the record number.

Every ref names exactly one report; `tests/test_thaqalayn.py` holds that.

Cite as:

> [Work], [vol. N,] hadith N. Trans. [translator], thaqalayn.net.

Publisher and year are null and stay null. The API serves neither.

## One record, one passage

The snapshots do not go through `passages.segment()`. The API already carries
the work's own divisions — category, chapter, hadith number — so re-splitting
on blank lines would cut a report in half, and re-detecting a speaker would put
a name in a field the record either states or leaves blank.

`englishText` becomes the passage text and is what every claim rests on.
`arabicText` sits beside it in `arabic_raw`, never mixed into the quotable
text, and `arabic_verified` is 0 on every one of them — real Unicode is not the
same as checked against the source.

## Two things upstream gets wrong, handled here

| Problem | What happens |
|---|---|
| **Kamal al-Din is advertised and empty.** 659 records in `allbooks`, none served. | Reported on every fetch, absent from `manifest.json`. It is an upstream scrape gap, not a local error. Both `Kitab al-Ghayba` works are complete and close what it was needed for. |
| **Twelve records carry a placeholder in `arabicText`** — `"To be added"`, `"ArabicToAdd"`, `"notfound"`, `"-"`. | Kept verbatim in the snapshot, because the snapshot is the upstream. Never promoted to `arabic_raw`: an absence that looks like content is what gets typeset by mistake. |

## What this corpus is not

It is hadith. It carries **no biography, no sira, no history**, so it does not
touch the Tier 2 gap in `00-foundations/sources-needed.md`. `Kitab al-Irshad`
with a named translator is still the project's most valuable acquisition, and
**Tuhaf al-Uqul — the rank-1 work — is not in the API at all**, which is one
reason `00-sources/text/` stays exactly where it is.

## Size

53 MB across 32 files, tracked. Comparable to the 48 MB already tracked in
`text/`, `md/` and `pages/`, and for the same reason: a source you cannot open
in a diff is a source nobody checks.
