#!/usr/bin/env python3
"""
Candidate finder for the hadith cards — the box's two blocked cards and the
companions line's thirty-nine.

    python tools/select_hadith_cards.py --index            # build the pool
    python tools/select_hadith_cards.py --propose          # rank per row
    python tools/select_hadith_cards.py --propose --entry Bilal --top 8

What this does and does not do
------------------------------
It RANKS. It does not select. Every candidate is a real saying quoted verbatim
from a held edition with the internal reference a citation needs — but which
one belongs on a card is a judgement about a child, a parent and a theme, and
that judgement is not in this file.

Two pools, in the project's own priority order
----------------------------------------------
1. **Tuhaf al-Uqul short maxims** (rank 1 in `sourcing-rules.md`), cited
   `short maxims, no. N`. Organised by Masoom, which is why attribution here is
   certain rather than inferred.
2. **The Thaqalayn corpus** (approved 2026-08-24), cited `[vol. N,] hadith N`.
   Organised by topic, not by speaker, so the speaker has to be READ OFF the
   report — and several kunyas name more than one Masoom. Those are flagged
   `ambiguous` and can never rank above `low`, because "Abu al-Hasan" is three
   different Imams and a card must not guess which.

Three rules enforced here rather than left to the reader
--------------------------------------------------------
* **No card repeats its Masoom's box card.** The twelve selected box sayings
  are struck out by reference before anything is ranked.
* **Conduct and ethics only** (`sourcing-rules.md` subject limits). A saying
  carrying jurisprudence, theology or ritual vocabulary is dropped, not
  down-ranked — the register line is not a matter of degree.
* **A saying, not an editor's footnote.** Tuhaf's numbered sections interleave
  the compiler's own notes ("In Al-Lahouf, Ibn Tawous affirms…"); anything that
  does not carry an attribution is not a candidate.

Confidence is reported, never hidden. `low` means the match rests on one weak
signal or an ambiguous attribution, and it is meant to be checked by someone
else before it reaches a card.
"""

import argparse
import io
import json
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TUHAF = os.path.join(ROOT, "00-sources", "text", "tuhaf_al-uqul.txt")
DB = os.path.join(ROOT, "00-sources", "source.db")
POOL = os.path.join(ROOT, "00-sources", "reports", "maxim-pool.json")

SECTIONS = [
    ("the Prophet",       r"Short Maxims Of The Prophet"),
    ("Imam Ali",          r"Short Maxims Of Imam Ali"),
    ("Imam Hasan",        r"Short Maxims Of Imam Al-Hasan"),
    ("Imam Husayn",       r"Short Maxims Of Imam Al-Husayn"),
    ("Imam al-Sajjad",    r"Short Maxims Of Imam As-Sajjad"),
    ("Imam al-Baqir",     r"Short Maxims Of Imam Al-Baqir"),
    ("Imam al-Sadiq",     r"Short Maxims Of Imam As-Sadiq"),
    ("Imam al-Kadhim",    r"Short Maxims Of Imam Al-Kadhim"),
    ("Imam al-Rida",      r"Short Maxims Of Imam Ar-Ridha"),
    ("Imam al-Jawad",     r"Short Maxims Of Imam Al-Jawad"),
    ("Imam al-Hadi",      r"Short Maxims Of Imam Al-Hadi"),
    ("Imam al-Askari",    r"Short Maxims Of Imam Al-Askari"),
]

STOP = re.compile(
    r"^\s*(?:Maxims Of |Short Maxims Of |Long Maxims Of |Admonitions And Maxims|"
    r"Maxims And Words Of Wisdom Of |The following (?:maxims|sayings)|Glossary|Notes?\b)",
    re.M)

# A candidate must carry an attribution. This is what separates a saying from
# the compiler's footnote sitting under the same number.
ATTRIB = re.compile(r"\b(?:said|says|wrote|was asked|answered)\b", re.I)
NOT_A_SAYING = re.compile(
    r"^(?:This sermon|In Al-|We choose|The following|See |It is (?:also )?related that this|"
    r"In the book of|This narrative|A part of|Ibn |Al-[A-Z]\w+ (?:affirms|records|says that))",
    re.I)

BANNED = re.compile(
    r"\b(?:zakat|khums|wudu|ablution|rak'?ah|qibla|menstrua\w*|divorce|inherit\w*|"
    r"usury|riba|halal|haram|imamate|occultation|raj'?a|resurrect\w*|hellfire|"
    r"apostate|infidel|unbeliever|polytheis\w*|verse|sura|dinar|dirham of zakat|"
    r"prostrat\w*|ritual|Hell|Paradise|Fire\b|Satan|devil|angel of death)\b", re.I)

MIN_CHARS, MAX_CHARS = 45, 230

# The twelve box cards already spent (citation-sheet.md), by Tuhaf maxim number.
SPENT = {
    ("the Prophet", 112), ("Imam Husayn", 18), ("Imam Hasan", 1),
    ("Imam al-Askari", 21), ("Imam al-Baqir", 2), ("Imam Ali", 8),
    ("Imam al-Kadhim", 13), ("Imam al-Hadi", 15), ("Imam al-Sadiq", 1),
    ("Imam al-Rida", 8), ("Imam al-Jawad", 12),
}

# Reading the speaker off a Thaqalayn report. Order matters — the most specific
# name wins. `ambiguous` kunyas name more than one Masoom and are never
# resolved by guessing.
SPEAKERS = [
    # Imam al-Husayn FIRST, and only on a pattern that names him. He is quoted in
    # these collections as "Abu 'Abd Allah al-Husayn", and al-Sadiq is quoted as
    # plain "Abu 'Abd Allah" — so ordering al-Sadiq first filed every Husayn
    # report under al-Sadiq and left his pool empty.
    # "(?<!Ibn )(?<!ibn )(?<!bin )" is load-bearing: "Ali Ibn al-Husayn" is Imam
    # al-Sajjad, not Imam al-Husayn, and a bare "al-Husayn (as)" test filed five
    # of al-Sajjad's reports under his father.
    ("Imam Husayn",     r"(?:Abu '?Abd ?Allah al-?Husayn|"
                        r"(?<!Ibn )(?<!ibn )(?<!bin )al-?Husayn (?:ibn|b\.) '?Ali(?! ibn)|"
                        r"Imam al-?Husayn(?! ibn)|Sayyid al-?Shuhada)", False),
    ("Imam al-Mahdi",   r"(?:al-?Mahdi|Sahib al-?Zaman|al-?Qa'?im \(a|the Awaited|tawqi)", True),
    ("Sayyida Fatima",  r"(?:Fatima al-?Zahra|Fatima \(sa\)|Fatima, the daughter of|"
                        r"Fatima, peace be upon her,? said)", False),
    ("Imam al-Sajjad",  r"(?:Ali (?:ibn|b\.) al-?Husayn|Zayn al-'?Abidin|al-Sajjad)", False),
    ("Imam al-Askari",  r"(?:al-?'?Askari|Abu Muhammad al-?Hasan (?:ibn|b\.) 'Ali)", False),
    ("Imam al-Hadi",    r"(?:al-?Hadi|'?Ali (?:ibn|b\.) Muhammad al-?Naqi|al-?Naqi)", False),
    ("Imam al-Rida",    r"(?:al-?Rida|ar-?Ridha|'?Ali (?:ibn|b\.) Musa)", False),
    ("Imam al-Kadhim",  r"(?:al-?Kadhim|al-?Kazim|Musa (?:ibn|b\.) Ja'?far)", False),
    ("Imam al-Jawad",   r"(?:al-?Jawad|Muhammad (?:ibn|b\.) 'Ali al-?Taqi|al-?Taqi)", False),
    ("Imam al-Sadiq",   r"(?:al-?Sadiq|as-?Sadiq|Abu '?Abd ?Allah|Abu 'Abdillah|Ja'?far (?:ibn|b\.) Muhammad)", False),
    ("Imam al-Baqir",   r"(?:al-?Baqir|Muhammad (?:ibn|b\.) 'Ali al-?Baqir)", False),
    ("Imam Hasan",      r"(?:al-?Hasan (?:ibn|b\.) '?Ali(?! al))", False),
    ("Imam Ali",        r"(?:Amir al-?Mu'?minin|'?Ali (?:ibn|b\.) Abi Talib)", False),
    ("the Prophet",     r"(?:the Messenger of Allah|the Holy Prophet|the Prophet \(s)", False),
    # Ambiguous by construction — kept, flagged, capped at low confidence.
    ("Imam al-Baqir",   r"Abu Ja'?far", True),
    ("Imam al-Kadhim",  r"Abu al-?Hasan", True),
]


def norm(t):
    t = re.sub(r"\r+\n", "\n", t)
    t = re.sub(r"\[\[p \d+\]\]", "", t)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("ﬁ", "fi"), ("ﬂ", "fl")):
        t = t.replace(a, b)
    return t


def usable(text):
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return False
    if NOT_A_SAYING.match(text) or not ATTRIB.search(text):
        return False
    if BANNED.search(text):
        return False
    return True


def tuhaf_pool():
    body = norm(io.open(TUHAF, encoding="utf-8", errors="replace").read())
    pool = {}
    for masoom, pat in SECTIONS:
        m = re.search(pat, body, re.I)
        if not m:
            continue
        nxt = STOP.search(body, m.end() + 40)
        chunk = body[m.end():nxt.start() if nxt else m.end() + 60000]

        items, cur, num = [], [], None
        for line in chunk.split("\n"):
            s = line.strip()
            if not s:
                continue
            mm = re.match(r"^(\d{1,3})[.)]\s+(.*)$", s)
            if mm:
                if num is not None and cur:
                    items.append((num, " ".join(cur)))
                num, cur = int(mm.group(1)), [mm.group(2)]
            elif num is not None:
                cur.append(s)
        if num is not None and cur:
            items.append((num, " ".join(cur)))

        keep, seen = [], set()
        for n, text in items:
            text = re.sub(r"\s+", " ", text).strip()
            text = re.sub(r"\s*\d{1,2}\s*$", "", text)
            if not usable(text) or (masoom, n) in SPENT or n in seen:
                continue
            seen.add(n)
            keep.append({"no": n, "text": text, "work": "Tuhaf al-Uqul",
                         "ref": "short maxims, no. %d" % n, "rank": 1, "ambiguous": False})
        pool[masoom] = keep
    return pool


def api_pool(limit_per_masoom=4000):
    """Thaqalayn reports whose speaker can be read off the text."""
    if not os.path.exists(DB):
        return {}
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT p.source_id, p.internal_ref, p.english, w.work, e.translator "
        "FROM passages p JOIN editions e ON e.source_id = p.source_id "
        "JOIN sources w ON w.work_id = e.work_id "
        "WHERE p.source_id LIKE 'SRC-TQ-%' AND length(p.english) BETWEEN ? AND ?",
        (MIN_CHARS, MAX_CHARS)).fetchall()
    con.close()

    compiled = [(m, re.compile(pat, re.I), amb) for m, pat, amb in SPEAKERS]
    pool = {}
    for r in rows:
        text = re.sub(r"\s+", " ", norm(r["english"] or "")).strip()
        text = re.sub(r"^\d{1,4}\s*[-.)]\s*", "", text)
        if not usable(text):
            continue
        for masoom, rx, amb in compiled:
            if rx.search(text):
                bucket = pool.setdefault(masoom, [])
                if len(bucket) < limit_per_masoom:
                    bucket.append({
                        "no": None, "text": text, "work": r["work"],
                        "ref": r["internal_ref"], "source_id": r["source_id"],
                        "rank": 4, "ambiguous": amb,
                    })
                break
    return pool


# --------------------------------------------------------------------------

def terms(*words):
    """Word-boundary stems. `kin` must not match `walking` — it did, and it put
    'Speedy walking removes the beauty of the believers' at the top of the row
    for 'who counts as family'."""
    return [re.compile(r"\b%s" % w, re.I) for w in words]


ROWS = [
    ("Salman al-Farsi", "the Prophet", "who counts as family",
     terms("brother", "kin", "kinship", "relative", "famil", "neighbou?r", "friend", "compan")),
    ("Bilal", "the Prophet", "steadfastness",
     terms("patien", "steadfast", "endur", "persever", "firm", "hardship", "advers", "constan")),
    ("Abu Dharr", "the Prophet", "speaking for the poor",
     terms("poor", "needy", "beggar", "destitute", "wealth", "rich", "sit with")),
    ("Sumayyah bint Khabbat", "the Prophet", "holding on when it is not safe to",
     terms("patien", "afflict", "misfortune", "trial", "endur", "fear", "courage")),
    ("Nusaybah bint Ka'b", "the Prophet", "courage that shields somebody else",
     terms("defend", "protect", "shield", "aid", "help", "support", "courage", "rescue")),
    ("Umm Ayman", "the Prophet", "care that lasts a whole life",
     terms("kind", "mercy", "merciful", "compassion", "loyal", "affection", "tend")),
    ("Halima al-Sa'diyya", "the Prophet", "kindness to a child in your care",
     terms("child", "children", "young", "orphan", "gentl", "kind", "mercy", "suckl")),
    ("Asma bint Umays", "the Prophet", "staying through every upheaval",
     terms("compan", "travel", "journey", "migrat", "steadfast", "loyal", "faithful", "remain")),

    ("Maytham al-Tammar", "Imam Ali", "truthfulness when it costs",
     terms("truth", "truthful", "honest", "lie", "liar", "falsehood", "tongue", "sincer")),
    ("Qambar", "Imam Ali", "service, and what a servant is owed",
     terms("servant", "slave", "serve", "master", "humil", "humble", "modest")),
    ("Malik al-Ashtar", "Imam Ali", "gentleness in authority",
     terms("clemen", "gentl", "forbear", "pardon", "forgiv", "anger", "power", "rule", "author")),
    ("Fatima bint Asad", "Imam Ali", "raising a child who is not your own",
     terms("child", "children", "orphan", "rear", "young", "mother", "kin", "kind")),

    ("Abbas ibn Ali", "Imam Husayn", "a trust kept when nobody would have known",
     terms("trust", "deposit", "faithful", "promis", "honest", "pledge", "covenant")),
    ("Umm Kulthum bint Ali", "Imam Husayn", "children, in the worst of it",
     terms("child", "children", "young", "orphan", "mercy", "kind", "wrong")),
    ("Rabab bint Imra' al-Qays", "Imam Husayn", "faithfulness that outlasts the person",
     terms("loyal", "faithful", "love", "remember", "friend", "affection", "constan")),
    ("Zaynab bint Ali", "Imam Husayn", "the truth said in front of a ruler",
     terms("truth", "tyrant", "unjust", "ruler", "wrong", "disobed", "speak", "silen")),
    ("Sakina bint al-Husayn", "Imam Husayn", "remembering",
     terms("remember", "mention", "forget", "memor", "lesson", "learn")),
    ("Fitrus", "Imam Husayn", "grief, and what it is owed",
     terms("grief", "sorrow", "weep", "consol", "afflict", "calamit", "mercy", "relie")),
    ("Umm al-Banin", "Imam Husayn", "raising another woman's children as your own",
     terms("child", "children", "kin", "kinship", "mercy", "kind", "famil", "brother")),
    ("Sayyida Ruqayya bint al-Husayn", "Imam Husayn", "the smallest person in the room",
     terms("small", "little", "weak", "humble", "modest", "child", "young", "poor", "support")),

    ("Qais ibn Sa'd", "Imam Hasan", "obeying when you think it is wrong",
     terms("obey", "obedien", "counsel", "consult", "command", "patien", "accept", "advis")),
    ("Tawus al-Yamani", "Imam al-Sajjad", "worship nobody is watching",
     terms("worship", "secret", "hidden", "sincer", "ostentat", "alone", "night", "pray")),
    ("Jabir ibn Abdullah al-Ansari", "Imam al-Baqir", "keeping a trust across a lifetime",
     terms("trust", "deposit", "keep", "faithful", "promis", "covenant", "entrust")),
    ("Hisham ibn al-Hakam", "Imam al-Sadiq", "knowledge, whatever the age of the one holding it",
     terms("knowledge", "learn", "scholar", "wisdom", "wise", "teach", "ask", "understand")),
    ("Umm Farwa", "Imam al-Sadiq", "honouring a mother by name",
     terms("mother", "parent", "kin", "kinship", "honou?r", "dutiful", "famil")),
    ("Safwan al-Jammal", "Imam al-Kadhim", "the earnings you refuse",
     terms("earn", "livelihood", "wealth", "gain", "unlawful", "refrain", "abstain", "trade", "wage")),
    ("Hamida Khatun", "Imam al-Kadhim", "teaching, and who is fit to teach",
     terms("teach", "knowledge", "learn", "wisdom", "wise", "scholar", "understand")),
    ("Dibil al-Khuza'i", "Imam al-Rida", "saying the thing out loud",
     terms("speak", "speech", "tongue", "silen", "word", "truth", "say")),
    ("Sayyida Ma'suma", "Imam al-Rida", "family, and the road toward it",
     terms("kin", "kinship", "brother", "famil", "visit", "relative", "affection")),
    ("Ali ibn Mahziyar", "Imam al-Jawad", "discharging a trust, every time",
     terms("trust", "deposit", "faithful", "keep", "promis", "duty", "discharg")),
    ("Abu Hashim al-Ja'fari", "Imam al-Hadi", "giving before being asked",
     terms("giv", "generos", "generous", "favou?r", "ask", "beg", "bount", "grant")),
    ("Ahmad ibn Ishaq al-Qummi", "Imam al-Askari", "carrying other people's questions",
     terms("ask", "question", "answer", "knowledge", "learn", "scholar", "tongue")),
    ("Uthman ibn Sa'id al-Amri", "Imam al-Askari", "trustworthiness",
     terms("trust", "honest", "faithful", "deposit", "reliab", "promis")),
]

BLOCKED = [
    ("Fizza", "Sayyida Fatima", "no credited edition of her sayings is held"),
    ("Muhammad ibn Uthman al-Amri", "Imam al-Mahdi", "tawqi' — Kitab al-Ghayba now held"),
    ("Husayn ibn Ruh al-Nawbakhti", "Imam al-Mahdi", "tawqi' — Kitab al-Ghayba now held"),
    ("Ali ibn Muhammad al-Samarri", "Imam al-Mahdi", "tawqi' — Kitab al-Ghayba now held"),
    ("Narjis Khatun", "Imam al-Mahdi", "tawqi' — Kitab al-Ghayba now held"),
    ("Khawla bint al-Azwar", "nobody", "points to no Masoom; a decision, not a source"),
]


def score(text, pats, rank):
    hits = [p.pattern.replace(r"\b", "") for p in pats if p.search(text)]
    s = len(hits) * 10
    if len(text) <= 110:
        s += 8
    elif len(text) <= 160:
        s += 4
    s += (4 - rank)                      # Tuhaf outranks the API corpus
    return s, hits


def confidence(cand, best, runner):
    if cand.get("ambiguous"):
        return "low"
    n = len(cand["_hits"])
    if n >= 3 and best - runner >= 6:
        return "high"
    if n >= 2:
        return "medium"
    return "low"


def propose(pool, only=None, top=4):
    out = []
    for name, masoom, theme, pats in ROWS:
        if only and only.lower() not in name.lower():
            continue
        ranked = []
        for c in pool.get(masoom, []):
            s, hits = score(c["text"], pats, c["rank"])
            if hits:
                d = dict(c); d["_hits"] = hits; d["_score"] = s
                ranked.append(d)
        ranked.sort(key=lambda d: (-d["_score"], d["rank"], d["no"] or 9999))
        picks = ranked[:top]
        conf = ("none" if not picks else
                confidence(picks[0], picks[0]["_score"],
                           picks[1]["_score"] if len(picks) > 1 else 0))
        out.append({"entry": name, "masoom": masoom, "theme": theme,
                    "confidence": conf, "candidates": picks})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--index", action="store_true")
    ap.add_argument("--propose", action="store_true")
    ap.add_argument("--entry")
    ap.add_argument("--top", type=int, default=4)
    ap.add_argument("--no-api", action="store_true", help="Tuhaf only")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    pool = tuhaf_pool()
    if not args.no_api:
        for m, items in api_pool().items():
            pool.setdefault(m, []).extend(items)

    os.makedirs(os.path.dirname(POOL), exist_ok=True)
    with io.open(POOL, "w", encoding="utf-8", newline="\n") as f:
        json.dump(pool, f, ensure_ascii=False, indent=1)

    if args.index or not args.propose:
        print("candidate pool — conduct register, card length, box cards struck out\n")
        print("  %-18s %7s %7s" % ("Masoom", "Tuhaf", "API"))
        for m in sorted(pool):
            t = sum(1 for c in pool[m] if c["rank"] == 1)
            a = sum(1 for c in pool[m] if c["rank"] != 1)
            print("  %-18s %7d %7d" % (m, t, a))
        print("\n  total: %d" % sum(len(v) for v in pool.values()))
        if not args.propose:
            return 0

    res = propose(pool, args.entry, args.top)
    if args.json:
        for r in res:
            for c in r["candidates"]:
                c.pop("_hits", None)
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    for r in res:
        print("\n== %s -> %s  [%s]   theme: %s"
              % (r["entry"], r["masoom"], r["confidence"], r["theme"]))
        for c in r["candidates"]:
            tag = "TUHAF %s" % c["ref"] if c["rank"] == 1 else "%s %s" % (c["work"], c["ref"])
            print("   [%s]%s %s" % (tag, " AMBIG" if c["ambiguous"] else "", c["text"][:190]))
    print("\n%d ranked, %d blocked:" % (len(res), len(BLOCKED)))
    for n, m, why in BLOCKED:
        print("   %-30s %-16s %s" % (n, m, why))
    return 0


if __name__ == "__main__":
    sys.exit(main())
