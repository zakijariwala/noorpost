#!/usr/bin/env python3
"""
Pull the Thaqalayn corpus into 00-sources/api/ as pinned snapshots.

    python tools/fetch_thaqalayn.py --list              # what the API advertises
    python tools/fetch_thaqalayn.py                     # fetch everything, pin it
    python tools/fetch_thaqalayn.py --book Al-Kafi-Volume-1-Kulayni
    python tools/fetch_thaqalayn.py --check             # has the upstream moved?
    python tools/fetch_thaqalayn.py --emit-yaml         # sources.yaml rows for what is held

Why a snapshot and not a live call
----------------------------------
thaqalayn.net is re-scraped weekly by the API's own GitHub Action. An upstream
that can change under a printed citation is not a fixed edition, and
`sourcing-rules.md` requires one edition per work, fixed, never mixed. So every
book is written to disk once and pinned by SHA-256 in `api/manifest.json`.
`--check` re-fetches and compares without writing, which is how a change
upstream becomes something a human decides about rather than something that
happens silently between two print runs.

The guard
---------
`rejected.yaml` is consulted by work name before anything is written, so a work
removed under the Shia-sources-only rule cannot re-enter the project through
this door. Every book the API serves is a Shia collection, so today the guard
refuses nothing — it exists because "today" is not a rule.
"""

import argparse
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sourcelib import config, metadata, thaqalayn as tq


def log(msg):
    print(msg, flush=True)


def now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


def source_id_for(book_id):
    """SRC-TQ-<book id>. Long, and deliberately so: it names the book the API
    serves, so a snapshot on disk and a row in sources.yaml cannot be matched
    up wrongly."""
    return "SRC-TQ-" + book_id


def work_id_for(book):
    """One work_id per work, shared across its volumes — SRC-TQ-Al-Kafi-Volume-3
    and -Volume-4 are two editions of one work, which is exactly the
    works/editions split sources.yaml already makes."""
    bid = book["bookId"]
    if "-Volume-" in bid:
        head, tail = bid.split("-Volume-", 1)
        rest = tail.split("-", 1)
        bid = head + ("-" + rest[1] if len(rest) > 1 else "")
    return "WRK-TQ-" + bid


# --------------------------------------------------------------------------

def do_list(books):
    log("%d books advertised by %s\n" % (len(books), tq.BASE))
    log("%-42s %-30s %7s  %s" % ("bookId", "translator", "records", "author"))
    for b in sorted(books, key=lambda x: x["bookId"]):
        log("%-42s %-30s %7s  %s" % (b["bookId"], (b.get("translator") or "—")[:30],
                                     b.get("idRangeMax"), (b.get("author") or "")[:40]))


def fetch_all(books, only, manifest, check_only):
    rejected_idx = metadata.rejected_index()
    changed, empty, failed, unchanged = [], [], [], []

    for b in sorted(books, key=lambda x: x["bookId"]):
        bid = b["bookId"]
        if only and bid not in only:
            continue

        if metadata.is_rejected(name=b.get("BookName"), index=rejected_idx) or \
           metadata.is_rejected(name=bid, index=rejected_idx):
            log("  REFUSED %s — on the rejected list" % bid)
            continue

        if not (b.get("translator") or "").strip():
            log("  SKIP    %s — no translator credited, so nothing here is citable" % bid)
            continue

        try:
            records = tq.fetch_book(bid)
        except tq.ApiError as exc:
            log("  FAIL    %s — %s" % (bid, exc))
            failed.append(bid)
            continue

        if not records:
            log("  EMPTY   %s — advertised %s records, served none" % (bid, b.get("idRangeMax")))
            empty.append(bid)
            continue

        digest = tq.sha256_text(tq.render_jsonl(records))
        prev = manifest.get("books", {}).get(bid, {})

        if prev.get("sha256") == digest:
            unchanged.append(bid)
            log("  same    %-42s %6d records" % (bid, len(records)))
            continue

        if check_only:
            if prev:
                log("  ⚠ DRIFT %-42s %6d records (was %d) — upstream has changed"
                    % (bid, len(records), prev.get("records", 0)))
            else:
                log("  new     %-42s %6d records (not held)" % (bid, len(records)))
            changed.append(bid)
            continue

        path, digest = tq.write_snapshot(bid, records)
        manifest.setdefault("books", {})[bid] = {
            "book": b.get("BookName"),
            "english_name": b.get("englishName"),
            "author": b.get("author"),
            "translator": b.get("translator"),
            "volume": b.get("volume"),
            "records": len(records),
            "id_range": [b.get("idRangeMin"), b.get("idRangeMax")],
            "sha256": digest,
            "fetched_at": now(),
            "file": os.path.relpath(path, config.ROOT).replace("\\", "/"),
        }
        changed.append(bid)
        log("  wrote   %-42s %6d records  %s" % (bid, len(records), digest[:12]))

    return changed, empty, failed, unchanged


def emit_yaml(books, manifest):
    """sources.yaml rows for every book actually held. Printed, not written —
    sources.yaml is hand-edited by design and this tool does not own it."""
    held = manifest.get("books", {})
    by_id = {b["bookId"]: b for b in books}
    works, seen = [], set()
    editions = []

    for bid in sorted(held):
        b = by_id.get(bid)
        if b is None:
            continue
        m = held[bid]
        wid = work_id_for(b)
        if wid not in seen:
            seen.add(wid)
            works.append((wid, b))
        editions.append((source_id_for(bid), wid, bid, b, m))

    out = ["# --- Thaqalayn API snapshots. Paste under `works:` ---"]
    for wid, b in works:
        out.append("  - work_id: %s" % wid)
        out.append("    work: %s" % b.get("BookName"))
        out.append("    author: %s" % b.get("author"))
        out.append("    tradition: shia")
        out.append("    priority_rank: null")
        out.append("    note: Held as a Thaqalayn API snapshot. No page numbers exist in this "
                   "edition; cite the work's own hadith number.")
        out.append("")

    out.append("# --- Paste under `editions:` ---")
    for sid, wid, bid, b, m in editions:
        out.append("  - source_id: %s" % sid)
        out.append("    work_id: %s" % wid)
        out.append("    volume: %s" % (b.get("volume") if "-Volume-" in bid else "null"))
        out.append("    volume_title: null")
        out.append("    translator: %s" % m["translator"])
        out.append("    publisher: null")
        out.append("    year: null")
        out.append("    edition: thaqalayn.net, retrieved via thaqalayn-api.net")
        out.append("    language: en")
        out.append("    api_file: %s" % m["file"])
        out.append("    sha256: %s" % m["sha256"])
        out.append("    record_count: %d" % m["records"])
        out.append("    text_file: null")
        out.append("    pagination: api-record")
        out.append("    citation_unit: hadith-number")
        out.append("    permission: unchecked")
        out.append("    status: fixed")
        out.append("    complete: true")
        out.append("    aliases:")
        out.append("      - %s" % b.get("BookName"))
        out.append("      - %s" % b.get("englishName"))
        out.append("    notes: Approved as a source of record. Pinned by sha256; "
                   "tools/fetch_thaqalayn.py --check reports upstream drift.")
        out.append("")
    log("\n".join(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="show what the API advertises, fetch nothing")
    ap.add_argument("--book", action="append", help="one bookId (repeatable)")
    ap.add_argument("--check", action="store_true",
                    help="re-fetch and compare against the pinned hashes, write nothing")
    ap.add_argument("--emit-yaml", action="store_true",
                    help="print sources.yaml rows for the snapshots already held")
    args = ap.parse_args()

    manifest = tq.load_manifest()

    if args.emit_yaml:
        books = tq.list_books()
        emit_yaml(books, manifest)
        return 0

    log("querying %s …" % tq.BASE)
    books = tq.list_books()

    if args.list:
        do_list(books)
        return 0

    log("%d books advertised%s\n" % (len(books), ", checking against pinned hashes"
                                     if args.check else ""))
    changed, empty, failed, unchanged = fetch_all(books, set(args.book or []), manifest,
                                                  args.check)

    if not args.check and changed:
        manifest["source"] = tq.BASE
        manifest["updated_at"] = now()
        manifest["note"] = ("Pinned snapshots of thaqalayn.net via thaqalayn-api.net. The "
                            "upstream is re-scraped weekly; these hashes are what the project "
                            "cites. Run --check to see whether it has moved.")
        tq.save_manifest(manifest)
        log("\npinned %d books in %s" % (len(changed),
                                         os.path.relpath(config.API_MANIFEST, config.ROOT)))

    log("\n%d unchanged, %d %s, %d empty upstream, %d failed"
        % (len(unchanged), len(changed), "drifted" if args.check else "written",
           len(empty), len(failed)))
    if empty:
        log("  empty:  %s" % ", ".join(empty))
        log("          advertised in allbooks and served nothing. That is an upstream scrape "
            "gap, not a local error.")
    if failed:
        log("  failed: %s" % ", ".join(failed))

    if args.check and changed:
        log("\nUpstream has moved. Nothing was written. Decide per book before re-pinning — "
            "a citation of record that changes silently is the thing this guards against.")
        return 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
