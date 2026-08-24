#!/usr/bin/env python3
"""
Write the hadith-card assignments into the companion entry files.

    python tools/apply_hadith_assignments.py --check   # report drift, write nothing
    python tools/apply_hadith_assignments.py

`00-foundations/hadith-assignments.json` is the record. This script is the only
thing that writes the card row into `08-companions/*.md`, so the entry files and
the assignment record cannot drift apart by hand.

An assignment with `text: null` writes a BLOCKED row naming its blocker. It
never writes a plausible-looking blank that reads as a selection — the whole
apparatus exists to stop exactly that.
"""

import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "00-foundations", "hadith-assignments.json")
ENTRIES = os.path.join(ROOT, "08-companions")

ROW = re.compile(r"^\| 2 \| Hadith card \|.*$", re.M)


def card_row(a):
    if not a.get("text"):
        return ("| 2 | Hadith card | Saying of **%s**, matched to %s. "
                "Chain mark **FIRST EDITION %02d/39**. | **BLOCKED** — %s |"
                % (a["masoom"] or "nobody", a["theme"] or "—", a["n"], a["blocker"]))
    return ("| 2 | Hadith card | **“%s”** — %s, %s, trans. %s. "
            "Saying of **%s**, matched to %s. Chain mark **FIRST EDITION %02d/39**. "
            "| **Selected** — confidence `%s`%s |"
            % (a["text"], a["work"], a["ref"], a["translator"],
               a["masoom"], a["theme"], a["n"], a["confidence"],
               ", to verify" if a["confidence"] != "high" else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    data = json.load(io.open(DATA, encoding="utf-8"))["assignments"]
    changed, missing, same = [], [], 0

    for a in data:
        path = os.path.join(ENTRIES, "%s.md" % a["slug"])
        if not os.path.exists(path):
            missing.append(a["slug"])
            continue
        body = io.open(path, encoding="utf-8").read()
        if not ROW.search(body):
            missing.append("%s (no card row)" % a["slug"])
            continue
        new = ROW.sub(lambda m: card_row(a), body, count=1)
        if new == body:
            same += 1
            continue
        changed.append(a["slug"])
        if not args.check:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new)

    print("%d %s, %d already current, %d missing"
          % (len(changed), "would change" if args.check else "written", same, len(missing)))
    if missing:
        print("  missing: %s" % ", ".join(missing))
    sel = [a for a in data if a.get("text")]
    print("\n%d of %d selected — %d high, %d medium, %d low, %d blocked"
          % (len(sel), len(data),
             sum(1 for a in data if a["confidence"] == "high"),
             sum(1 for a in data if a["confidence"] == "medium"),
             sum(1 for a in data if a["confidence"] == "low"),
             sum(1 for a in data if a["confidence"] == "blocked")))
    # No two cards may carry the same saying.
    refs = [a["ref"] for a in sel]
    dupes = {r for r in refs if refs.count(r) > 1}
    if dupes:
        print("  ✗ DUPLICATE SAYINGS: %s" % ", ".join(sorted(dupes)))
        return 1
    print("  no saying is used twice")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
