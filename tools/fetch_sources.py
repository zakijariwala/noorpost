#!/usr/bin/env python3
"""
Find and download the missing source texts into 00-sources/.

    python tools/fetch_sources.py                 # search only, download nothing
    python tools/fetch_sources.py --download      # fetch what it found
    python tools/fetch_sources.py --only irshad   # one target
    python tools/fetch_sources.py --tier 2        # only the blocking tier
    python tools/fetch_sources.py --list          # show the target list

Stdlib only, no dependencies.

archive.org is fully automated — search, relevance filter, pick the PDF, download,
record a sha256 in 00-sources/manifest.json.

al-islam.org, thaqalayn.net and hubeali.com return 403 to scripted requests or
serve their texts through JavaScript. They block bots on purpose and this script
does not try to get around that. For those the script prints the exact search URL
to open in a browser; the file then goes in 00-sources/ by hand.
"""

import argparse, json, os, re, sys, time, hashlib, urllib.parse, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "00-sources")
MANIFEST = os.path.join(DEST, "manifest.json")

UA = "Mozilla/5.0 (compatible; noorpost-source-fetcher/1.0; personal research use)"
PAUSE = 1.5  # seconds between requests to the same host

def alislam(term):
    return "https://www.al-islam.org/search?search_api_fulltext=" + urllib.parse.quote(term)

# --------------------------------------------------------------------------
# targets
#   archive   : queries for archive.org
#   must_any  : a hit's title must contain at least one of these (lowercase)
#   must_not  : a hit's title must contain none of these
#   manual    : (label, url) pairs to open in a browser
# --------------------------------------------------------------------------

TARGETS = [
    dict(
        key="kafi", tier=1,
        title="al-Kafi (al-Kulayni), English",
        need="Fallback for any saying not in the four works you already have",
        archive=['title:("al-Kafi") AND mediatype:texts',
                 '"usul al-kafi" English translation'],
        must_any=["kafi"],
        must_not=["kafirun", "kafka"],
        manual=[("thaqalayn.net — searchable by hadith number, the best fit for your citation format",
                 "https://thaqalayn.net/book/1"),
                ("hubeali.com — volume PDFs", "https://www.hubeali.com/#/books"),
                ("al-islam.org", alislam("al-Kafi"))],
    ),
    dict(
        key="irshad", tier=2,
        title="Kitab al-Irshad — al-Mufid, trans. I.K.A. Howard",
        need="The spine of eleven letters. Get this one first.",
        archive=['title:("Kitab al-Irshad") AND mediatype:texts',
                 '"Book of Guidance" Twelve Imams Mufid'],
        must_any=["irshad", "guidance"],
        must_not=["juwayni", "buddha", "hayari", "nasari"],
        manual=[("al-islam.org", alislam("Kitab al-Irshad Mufid"))],
    ),
    dict(
        key="sira-subhani", tier=2,
        title="The Message — Ja'far Subhani (Shia sira)",
        need="Envelope 03 in full; Salman; Bilal; the Trench and Hudaybiyya zines",
        archive=['Subhani "The Message" prophet mediatype:texts'],
        must_any=["message", "subhani"],
        must_not=["messages of", "messenger service"],
        manual=[("al-islam.org — The Message", alislam("The Message Subhani"))],
    ),
    dict(
        key="sira-guillaume", tier=2,
        title="Sirat Rasul Allah — Ibn Ishaq, trans. A. Guillaume",
        need="Cross-check for the Kaaba rebuilding and al-Amin",
        archive=['title:("The Life of Muhammad") AND Guillaume',
                 '"Sirat Rasul Allah" Ibn Ishaq'],
        must_any=["life of muhammad", "sirat", "ishaq"],
        must_not=[],
        manual=[],
    ),
    dict(
        key="qarashi", tier=2,
        title="The Life of Imam ... — Baqir Sharif al-Qarashi (series)",
        need="Rulers, the imprisonment, the examination of al-Jawad, the crown-prince conditions",
        archive=['Qarashi "The Life of Imam" mediatype:texts'],
        must_any=["life of imam", "qarashi"],
        must_not=[],
        manual=[("al-islam.org — the series", alislam("Baqir Sharif al-Qarashi Life of Imam")),
                ("al-Kadhim", alislam("The Life of Imam Musa al-Kadhim")),
                ("al-Jawad", alislam("The Life of Imam Muhammad al-Jawad")),
                ("al-Rida", alislam("The Life of Imam Ali ibn Musa al-Rida")),
                ("al-Hadi", alislam("The Life of Imam Ali al-Hadi")),
                ("al-Askari", alislam("The Life of Imam Hasan al-Askari"))],
    ),
    dict(
        key="occultation", tier=2,
        title="The Occultation of the Twelfth Imam — Jassim Hussain; and Kamal al-Din",
        need="Envelope 10 — the four deputies, named and in sequence",
        archive=['"Occultation of the Twelfth Imam" mediatype:texts',
                 '"Kamal al-Din" Saduq English mediatype:texts'],
        must_any=["occultation", "kamal al-din", "kamaluddin"],
        must_not=[],
        manual=[("al-islam.org — Jassim Hussain", alislam("Occultation of the Twelfth Imam")),
                ("al-islam.org — Kamal al-Din", alislam("Kamal al-Din Saduq"))],
    ),
    dict(
        key="tabari", tier=2,
        title="The History of al-Tabari (SUNY) — volumes covering 40–260 AH",
        need="The ruler bullet in all fourteen fact panels. Vol 19 is Karbala.",
        archive=['title:("The History of al-Tabari") AND mediatype:texts'],
        must_any=["tabari"],
        must_not=["tafsir"],
        manual=[],
    ),
    dict(
        key="fourteen", tier=2,
        title="A Brief History of the Fourteen Infallibles (WOFIS)",
        need="Dates, imamate lengths, mothers — the fact panel skeleton",
        archive=['"Fourteen Infallibles" mediatype:texts'],
        must_any=["infallible", "fourteen"],
        must_not=[],
        manual=[("al-islam.org", alislam("Brief History of the Fourteen Infallibles"))],
    ),
    dict(
        key="worldhistory", tier=3,
        title="A single world-history reference",
        need="The fourteen 'elsewhere in the world' bullets — one fixed reference for all of them",
        archive=['title:("Timetables of History") mediatype:texts',
                 'title:("Oxford Dictionary of World History") mediatype:texts'],
        must_any=["timetable", "world history"],
        must_not=[],
        manual=[],
    ),
]

# --------------------------------------------------------------------------
# http
# --------------------------------------------------------------------------

_last = {}

def get(url, binary=False, timeout=60):
    host = urllib.parse.urlparse(url).netloc
    wait = PAUSE - (time.time() - _last.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    _last[host] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")

# --------------------------------------------------------------------------
# archive.org
# --------------------------------------------------------------------------

def archive_search(query, rows=8):
    url = ("https://archive.org/advancedsearch.php?q="
           + urllib.parse.quote(query)
           + "&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=creator&fl%5B%5D=year&fl%5B%5D=downloads"
           + f"&rows={rows}&page=1&output=json&sort%5B%5D=downloads+desc")
    try:
        return json.loads(get(url)).get("response", {}).get("docs", [])
    except Exception as e:
        print(f"      archive.org search failed: {e}")
        return []

def relevant(doc, must_any, must_not):
    hay = ((doc.get("title") or "") + " " + str(doc.get("creator") or "")).lower()
    if must_not and any(b in hay for b in must_not):
        return False
    if must_any and not any(g in hay for g in must_any):
        return False
    return True

def pick_pdf(pdfs, max_bytes):
    """Largest PDF under the size ceiling; if all are over it, the smallest one.

    archive.org often holds a scanned monster next to a usable copy of the same
    book — Guillaume's Sira is there at both 26 MB and 1.5 GB."""
    ok = [p for p in pdfs if p[1] <= max_bytes]
    return (ok[0] if ok else pdfs[-1]) if pdfs else None


def archive_pdfs(identifier):
    """[(name, size, url)] of real PDFs in an item, largest first."""
    try:
        meta = json.loads(get(f"https://archive.org/metadata/{urllib.parse.quote(identifier)}"))
    except Exception as e:
        print(f"      metadata failed: {e}")
        return []
    out = []
    for f in meta.get("files", []):
        name = f.get("name", "")
        if not name.lower().endswith(".pdf") or "_text.pdf" in name.lower():
            continue
        out.append((name, int(f.get("size", 0) or 0),
                    f"https://archive.org/download/{identifier}/{urllib.parse.quote(name)}"))
    return sorted(out, key=lambda x: -x[1])

# --------------------------------------------------------------------------
# download
# --------------------------------------------------------------------------

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:70]

def load_manifest():
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_manifest(m):
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2, sort_keys=True)

def download(url, filename, manifest, key, title, source_title):
    path = os.path.join(DEST, filename)
    if os.path.exists(path):
        print(f"      already have {filename}")
        return False
    print(f"      downloading …")
    try:
        data = get(url, binary=True, timeout=300)
    except Exception as e:
        print(f"      FAILED: {e}")
        return False
    if not data.startswith(b"%PDF"):
        print(f"      not a PDF ({len(data)} bytes) — skipped")
        return False
    os.makedirs(DEST, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    manifest[filename] = dict(target=key, target_title=title, item_title=source_title,
                              url=url, bytes=len(data),
                              sha256=hashlib.sha256(data).hexdigest(),
                              edition_checked=False, translator=None)
    save_manifest(manifest)
    print(f"      saved {filename}  ({len(data)//1024} KB)")
    return True

# --------------------------------------------------------------------------
# run
# --------------------------------------------------------------------------

def run(t, do_download, manifest, cap, max_bytes):
    print(f"\n{'='*74}\n[tier {t['tier']}]  {t['title']}\n  needed for: {t['need']}\n")
    got = 0
    seen = set()

    for q in t["archive"]:
        if got >= cap:
            break
        print(f"  archive.org ← {q}")
        hits = archive_search(q)
        kept = [d for d in hits if relevant(d, t["must_any"], t["must_not"])]
        if not kept:
            print(f"    nothing relevant ({len(hits)} hits filtered out)")
        for doc in kept:
            if got >= cap:
                break
            ident = doc.get("identifier", "")
            if ident in seen:
                continue
            seen.add(ident)
            print(f"    · {doc.get('title','?')}  [{ident}]")
            pdfs = archive_pdfs(ident)
            if not pdfs:
                print("      no PDF in this item")
                continue
            name, size, url = pick_pdf(pdfs, max_bytes)
            print(f"      pdf: {name}  ({size//1024} KB)")
            print(f"      {url}")
            if do_download:
                if download(url, f"{t['key']}--{slug(ident)}.pdf", manifest,
                            t["key"], t["title"], doc.get("title", "")):
                    got += 1

    if t["manual"]:
        print("\n  open these in a browser — these sites block scripted access:")
        for label, url in t["manual"]:
            print(f"    {label}\n      {url}")

    if not do_download:
        print("\n  (search only — add --download to fetch)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true", help="actually fetch the files")
    ap.add_argument("--only", help="one target, by key")
    ap.add_argument("--tier", type=int, help="only this tier")
    ap.add_argument("--max", type=int, default=2, help="max files per target (default 2)")
    ap.add_argument("--max-mb", type=int, default=80, dest="max_mb",
                    help="skip PDFs bigger than this many MB (default 80)")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        for t in TARGETS:
            print(f"{t['key']:16} tier {t['tier']}  {t['title']}")
        return

    os.makedirs(DEST, exist_ok=True)
    manifest = load_manifest()
    targets = [t for t in TARGETS
               if (not a.only or t["key"] == a.only) and (not a.tier or t["tier"] == a.tier)]
    if not targets:
        print("no targets matched — try --list")
        return

    for t in targets:
        try:
            run(t, a.download, manifest, a.max, a.max_mb * 1024 * 1024)
        except KeyboardInterrupt:
            print("\nstopped")
            sys.exit(1)
        except Exception as e:
            print(f"  target failed: {e}")

    pdfs = [f for f in os.listdir(DEST) if f.endswith(".pdf")]
    print(f"\n{'='*74}\nPDFs in 00-sources/: {len(pdfs)}")
    print("""
Before anything here is cited:

  1. Open it. Confirm it is the work you think it is — archive.org has several
     unrelated books under similar titles.
  2. Find the translator and the edition. Write both into the fixed-editions
     table in 00-foundations/sourcing-rules.md.
  3. Set edition_checked and translator in 00-sources/manifest.json.

A PDF of the wrong edition cites the wrong page, which is worse than no citation.""")


if __name__ == "__main__":
    main()
