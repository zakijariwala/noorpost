# Original PDFs

Put them here, or leave them in `00-sources/` — both are searched, in that
order, so nothing that already works stops working.

**The PDFs are not tracked.** `HANDOVER.md` has the release zip:

```bash
curl -L -o sources.zip https://github.com/zakijariwala/noorpost/releases/download/sources-v1/noorpost-sources.zip
unzip sources.zip -d 00-sources
```

They are never written to, moved or replaced. Everything else in
`00-sources/` is derived from them and can be rebuilt.

Once they are here:

```bash
python tools/build_source_corpus.py --hash-originals
```

which records each edition's SHA-256 in `metadata/sources.yaml`. An edition
without a hash is not pinned — a different copy of the same translation
paginates differently, so its page numbers cannot be trusted.

A file on the denylist in `metadata/rejected.yaml` is refused here by hash,
whatever it is named.
