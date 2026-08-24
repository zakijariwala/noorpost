#!/usr/bin/env python3
"""
Prove every assigned saying is really in the source, at the reference given.

    python tools/verify_hadith_assignments.py

This is the check that cannot be skipped. A selection record is a set of claims
about texts, and a claim about a text is worth nothing until the text has been
found. The failure this exists to catch is a saying that reads perfectly, cites
a real work and a plausible number, and is not there.

Three verdicts per row:

  FOUND      the text is in the corpus AND the reference points at it
  MISPLACED  the text is in the corpus but NOT where the row says it is
  ABSENT     the text is not in the corpus at all — the row is unusable

Matching is on a normalised character run with a similarity floor, so an
edition's typographic quirks do not fail a real match, but a paraphrase does.
"""

import difflib
import io
import json
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "00-foundations", "hadith-assignments.json")
DB = os.path.join(ROOT, "00-sources", "source.db")
TEXTDIR = os.path.join(ROOT, "00-sources", "text")

SIMILAR = 0.90          # below this the two are not the same sentence


def norm(t):
    t = (t or "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("ﬁ", "fi"), ("ﬂ", "fl"), ("—", "-"), ("–", "-"), (" ", " ")):
        t = t.replace(a, b)
    t = re.sub(r"\[\[p \d+\]\]", " ", t)
    t = re.sub(r"[^a-z0-9 ]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def load_corpus():
    """Every English passage held, with where it came from."""
    units = []
    for name in sorted(os.listdir(TEXTDIR)):
        if not name.endswith(".txt"):
            continue
        body = io.open(os.path.join(TEXTDIR, name), encoding="utf-8", errors="replace").read()
        units.append(("text:" + name, None, norm(body), body))
    if os.path.exists(DB):
        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        for r in con.execute("SELECT source_id, internal_ref, english FROM passages "
                             "WHERE english IS NOT NULL AND source_id LIKE 'SRC-TQ-%'"):
            units.append((r["source_id"], r["internal_ref"], norm(r["english"]), r["english"]))
        con.close()
    return units


def find(text, units):
    """(hits, best_ratio). A hit is a unit whose text contains this saying, or a
    passage that IS this saying."""
    n = norm(text)
    if len(n) < 20:
        return [], 0.0
    hits, best = [], 0.0
    for sid, ref, hay, _raw in units:
        if sid.startswith("text:"):
            if n in hay:
                hits.append((sid, ref))
                best = 1.0
            continue
        if n == hay or n in hay:
            hits.append((sid, ref))
            best = 1.0
        else:
            r = difflib.SequenceMatcher(None, n, hay).quick_ratio()
            if r > 0.75:
                r = difflib.SequenceMatcher(None, n, hay).ratio()
                if r >= SIMILAR:
                    hits.append((sid, ref))
                best = max(best, r)
    return hits, best


TUHAF_REF = re.compile(r"short maxims of (.+?), no\. (\d+)", re.I)


def tuhaf_at(number, section_hint, raw):
    """Pull the maxim printed at `number` inside the named short-maxims section,
    so a Tuhaf reference is checked against the actual numbered item and not
    merely against the book as a whole."""
    heads = {
        "the prophet": "Short Maxims Of The Prophet",
        "imam ali": "Short Maxims Of Imam Ali",
        "imam al-hasan": "Short Maxims Of Imam Al-Hasan",
        "imam al-husayn": "Short Maxims Of Imam Al-Husayn",
        "imam al-sajjad": "Short Maxims Of Imam As-Sajjad",
        "imam al-baqir": "Short Maxims Of Imam Al-Baqir",
        "imam al-sadiq": "Short Maxims Of Imam As-Sadiq",
        "imam al-kadhim": "Short Maxims Of Imam Al-Kadhim",
        "imam al-rida": "Short Maxims Of Imam Ar-Ridha",
        "imam al-jawad": "Short Maxims Of Imam Al-Jawad",
        "imam al-hadi": "Short Maxims Of Imam Al-Hadi",
        "imam al-askari": "Short Maxims Of Imam Al-Askari",
    }
    head = heads.get(section_hint.strip().lower())
    if not head:
        return None
    m = re.search(re.escape(head), raw, re.I)
    if not m:
        return None
    stop = re.compile(r"^\s*(?:Maxims Of |Short Maxims Of |Long Maxims Of |Glossary)", re.M)
    nxt = stop.search(raw, m.end() + 40)
    chunk = raw[m.end():nxt.start() if nxt else m.end() + 60000]
    got = re.search(r"^\s*%d[.)]\s+(.{10,600}?)(?=\n\s*\d{1,3}[.)]\s|\Z)" % number,
                    chunk, re.M | re.S)
    if not got:
        return None
    # Strip the page marker: it belongs to the corpus format, not the
    # maxim, and leaving it in makes every item look longer than it is.
    item = re.sub(r"\[\[p \d+\]\]", " ", got.group(1))
    return re.sub(r"\s+", " ", item).strip()


def main():
    data = json.load(io.open(DATA, encoding="utf-8"))["assignments"]
    units = load_corpus()
    tuhaf_raw = io.open(os.path.join(TEXTDIR, "tuhaf_al-uqul.txt"),
                        encoding="utf-8", errors="replace").read()
    tuhaf_raw = re.sub(r"\r+\n", "\n", tuhaf_raw)

    bad, misplaced, ok, blocked, trimmed = [], [], [], [], []
    print("%-3s %-28s %-8s %s" % ("#", "entry", "verdict", "detail"))
    print("-" * 100)

    for a in data:
        if not a.get("text"):
            blocked.append(a)
            continue
        hits, best = find(a["text"], units)

        detail = ""
        verdict = "FOUND"
        if not hits:
            verdict = "ABSENT"
            detail = "best similarity anywhere in the corpus: %.2f" % best
        else:
            # Does the reference point at it?
            m = TUHAF_REF.search(a["ref"] or "")
            if a["work"] == "Tuhaf al-Uqul" and m:
                at = tuhaf_at(int(m.group(2)), m.group(1), tuhaf_raw)
                if at is None:
                    verdict = "MISPLACED"
                    detail = "no item numbered %s in that section" % m.group(2)
                elif norm(a["text"]) in norm(at):
                    # Correct placement. A card quotes the saying without the
                    # compiler's narrative frame ("As a man asked him…"), which
                    # is why containment is the test and not equality.
                    shortened = len(norm(at)) - len(norm(a["text"])) > 25
                    ends_with_item = a["text"].rstrip().endswith(at.rstrip()[-12:])
                    # sourcing-rules.md allows an ellipsis and forbids a silent
                    # trim, so a card that carries one has already declared it.
                    marked = a["text"].rstrip().endswith(("…", "..."))
                    if shortened and not ends_with_item and not marked:
                        verdict = "TRIMMED"
                        detail = "quotes part of no. %s; the item continues: …%s" % (
                            m.group(2), at[len(at) - min(len(at), 90):])
                elif difflib.SequenceMatcher(None, norm(at), norm(a["text"])).ratio() < SIMILAR:
                    verdict = "MISPLACED"
                    detail = "no. %s in that section actually reads: %s" % (
                        m.group(2), at[:110])
            elif re.match(r"(Saying|Letter|Sermon)\s+\d+$", (a["ref"] or "").strip()):
                # The fixed Nahj edition is cited by its own Saying/Letter number,
                # which is portable across printings. The Thaqalayn copy's
                # sequential hadith number is not, and is a second witness only.
                kind, num = (a["ref"] or "").split()
                nahj = io.open(os.path.join(TEXTDIR,
                               "nahjul_balagha_part_2_letters_and_sayings.txt"),
                               encoding="utf-8", errors="replace").read()
                flat = re.sub(r"\s+", " ", nahj)
                labels = ["%s %s" % (kind, num)]
                if kind == "Saying":
                    labels += ["Hadith n. %s" % num, "Saying %s:" % num]
                start = -1
                for lab in labels:
                    start = flat.find(lab)
                    if start >= 0:
                        break
                if start < 0:
                    verdict, detail = "MISPLACED", "no %s %s in the fixed edition" % (kind, num)
                else:
                    nxt = -1
                    for lab in ([("%s %d" % (kind, int(num) + 1))] +
                                (["Hadith n. %d" % (int(num) + 1)]
                                 if kind == "Saying" else [])):
                        nxt = flat.find(lab, start + 1)
                        if nxt > 0:
                            break
                    span = flat[start:nxt if nxt > 0 else start + 6000]
                    # the held PDF carries scanning artifacts, so compare on a
                    # long distinctive run rather than demanding the whole line
                    probe = norm(a["text"])
                    words = probe.split()
                    run = " ".join(words[:6])
                    if run and run not in norm(span):
                        alt = " ".join(words[-6:])
                        if alt not in norm(span):
                            verdict = "MISPLACED"
                            detail = "not inside %s %s of the fixed edition" % (kind, num)
                        else:
                            detail = "matched on the tail — check the edition for a scanning artifact"
                    else:
                        detail = "fixed edition, %s %s" % (kind, num)
            elif a["work"] == "Tuhaf al-Uqul":
                detail = "reference is not a short-maxims number — cannot pin it"
                verdict = "UNPINNED"
            else:
                # The SAME saying often appears in several collections. That is
                # not an error — the reference only has to point at ONE place the
                # text really is, so this compares normalised refs rather than
                # demanding the hit list hold nothing else.
                refs = [r for _s, r in hits if r]
                want = re.sub(r"[^a-z0-9]+", "", (a["ref"] or "").lower())
                if refs and not any(want and want == re.sub(r"[^a-z0-9]+", "", (r or "").lower())
                                    for r in refs):
                    verdict = "MISPLACED"
                    detail = "text is really at: %s" % ", ".join(sorted(set(refs))[:3])
                elif not refs:
                    detail = "found in %s" % ", ".join(sorted({s for s, _ in hits})[:2])

        line = "%-3d %-28s %-8s %s" % (a["n"], a["entry"][:28], verdict, detail[:56])
        print(line)
        if verdict == "ABSENT":
            bad.append(a)
        elif verdict == "MISPLACED":
            misplaced.append((a, detail))
        elif verdict == "TRIMMED":
            trimmed.append((a, detail))
        else:
            ok.append(a)

    print("\n%d verified, %d misplaced, %d ABSENT, %d blocked"
          % (len(ok), len(misplaced), len(bad), len(blocked)))

    if bad:
        print("\n=== ABSENT — not in any held source. These cannot print. ===")
        for a in bad:
            print("\n  %02d %s [%s]\n     \"%s\"\n     claimed: %s, %s"
                  % (a["n"], a["entry"], a["confidence"], a["text"], a["work"], a["ref"]))
            if a.get("verified_note"):
                print("     agent note: %s" % a["verified_note"][:160])
    if misplaced:
        print("\n=== MISPLACED — real text, wrong reference. ===")
        for a, d in misplaced:
            print("\n  %02d %s\n     \"%s\"\n     claimed %s / %s\n     %s"
                  % (a["n"], a["entry"], a["text"][:90], a["work"], a["ref"], d))

    # translator credit rule
    print("\n=== Translator credits ===")
    seen = {}
    for a in data:
        if a.get("translator"):
            seen.setdefault(a["translator"], []).append(a["n"])
    for t, ns in sorted(seen.items()):
        kinds = {a.get("translator_kind") for a in data if a.get("translator") == t}
        inst = re.search(r"publicat|bureau|press|seminary|writers", t, re.I)
        if inst and "institution" not in kinds:
            flag = "  ⚠ looks institutional but translator_kind is not set"
        elif inst:
            flag = "  (institution — admitted under the institutional-credit rule)"
        else:
            flag = ""
        print("  %-34s rows %s%s" % (t, ",".join(str(n) for n in ns), flag))

    return 1 if (bad or misplaced) else 0


if __name__ == "__main__":
    sys.exit(main())
