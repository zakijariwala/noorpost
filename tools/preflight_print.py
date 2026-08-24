#!/usr/bin/env python3
"""
The gate before a print run. Everything prototype mode relaxes comes back here.

    python tools/preflight_print.py

This is what makes the relaxation safe. Prototype mode does not delete a single
rule — it moves them all to this one command, so a design task stops waiting on
a citation and a print run still cannot start without one.

Exit 0 means the run may proceed. Anything else lists what is still open.
"""

import io
import json
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def main():
    fail, warn = [], []

    mode = load("00-foundations/build-mode.json").get("mode")
    print("build mode: %s\n" % mode)

    # --- hadith cards -----------------------------------------------------
    cards = load("00-foundations/hadith-assignments.json")["assignments"]
    unselected = [a for a in cards if not a.get("text")]
    lowconf = [a for a in cards if a.get("confidence") in ("low", "medium")]
    unnumbered = [a for a in cards if a.get("text") and a.get("ref")
                  and not re.search(r"\d", a["ref"])]
    refs = [a["ref"] for a in cards if a.get("text")]
    dupes = sorted({r for r in refs if refs.count(r) > 1})

    if unselected:
        fail.append("%d companion cards carry no saying: %s"
                    % (len(unselected), ", ".join(a["entry"] for a in unselected[:6])))
    if lowconf:
        fail.append("%d cards are still low/medium confidence and unverified — see "
                    "hadith-verification-worklist.md" % len(lowconf))
    if unnumbered:
        fail.append("%d citations carry no number: %s"
                    % (len(unnumbered), ", ".join(a["entry"] for a in unnumbered)))
    if dupes:
        fail.append("a saying is used on more than one card: %s" % ", ".join(dupes))

    # --- claims -----------------------------------------------------------
    db = os.path.join(ROOT, "00-sources", "source.db")
    if os.path.exists(db):
        con = sqlite3.connect(db)
        tv = con.execute("SELECT COUNT(*) FROM claims WHERE status='TV'").fetchone()[0]
        cont = con.execute("SELECT COUNT(*) FROM claims WHERE status='CONT'").fetchone()[0]
        con.close()
        if tv:
            fail.append("%d claims are still TO VERIFY. Nothing prints on TV." % tv)
        if cont:
            warn.append("%d claims are contested (CONT) — decide each before the run" % cont)
    else:
        warn.append("source.db not built; claim status not checked")

    # --- editions ---------------------------------------------------------
    try:
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        from sourcelib import metadata
        _w, editions, _b = metadata.load_sources()
        nocredit = [e["source_id"] for e in editions
                    if e.get("status") in ("fixed", "candidate")
                    and not e.get("translator") and e.get("text_file")]
        noperm = [e["source_id"] for e in editions
                  if e.get("status") == "fixed" and e.get("permission") != "checked"]
        manuscripts = [e["source_id"] for e in editions if e.get("status") == "manuscript"]
        if nocredit:
            fail.append("editions in use with no translator credit: %s" % ", ".join(nocredit))
        if noperm:
            fail.append("quotation permission unchecked on %d fixed editions — this is a "
                        "Phase 0 question and it is now due: %s"
                        % (len(noperm), ", ".join(noperm[:5])))
        if manuscripts:
            warn.append("%d source(s) admitted as unpublished manuscripts: %s — confirm each is "
                        "still the only thing carrying its claim" % (len(manuscripts),
                                                                    ", ".join(manuscripts)))
    except Exception as exc:
        warn.append("edition metadata not checked: %s" % exc)

    # --- decisions that gate the run --------------------------------------
    for path, needle, why in [
        ("00-foundations/citation-sheet.md", "Two cards currently claim segment 1",
         "the silsila numbering is undecided and the segment number prints on every box card"),
        ("TASKS.md", "**Envelope 06 signed line by line",
         "envelope 06 needs a named scholar's signature and blocks the whole run"),
    ]:
        try:
            if needle in io.open(os.path.join(ROOT, path), encoding="utf-8").read():
                fail.append("%s — %s" % (os.path.basename(path), why))
        except OSError:
            pass

    # --- physical proofs owed --------------------------------------------
    warn.append("physical proofs owed regardless of this check: the ring punch on real stock, "
                "and the pennant dimension")

    for f in fail:
        print("  ✗ %s" % f)
    for w in warn:
        print("  ⚠ %s" % w)

    if fail:
        print("\n%d blocking. Not ready to print." % len(fail))
        print("Prototype freely — none of this blocks a draft. See 00-foundations/build-mode.md.")
        return 1
    print("\nNothing blocking. A print run may proceed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
