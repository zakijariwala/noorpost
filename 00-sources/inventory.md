# Source inventory

> ⛔ **Shia sources only** — hard rule, `00-foundations/sourcing-rules.md`. Guillaume's Ibn Ishaq (both copies) and both al-Tabari volumes were **deleted from this repo on 2026-08-12** under that rule. They are not listed below and must not be re-added. — what is on disk, and what is missing

A factual ledger of the source texts, checked against the files actually in
`00-sources/text/`. This is the *present/missing* view. For the *why it matters*
view, ordered by what it unblocks, see `00-foundations/sources-needed.md`.

Checked: 2026-08-11, against 19 text files in `00-sources/text/` and 14 PDF
records in `manifest.json`.

---

## Present and usable

Every Tier 1 priority work is here. These carry a `[[p N]]` page marker per page
and are grep-ready.

| Work | File(s) | Notes |
|---|---|---|
| Tuhaf al-Uqul | `tuhaf_al-uqul.txt` | Tier 1 rank 1 — first choice for most hadith cards |
| Nahj al-Balagha | `nahjul_balagha_part_1_-_the_sermons.txt`, `..._part_2_letters_and_sayings.txt` | Both parts |
| Sahifa Sajjadiyya | `as-sahifa_al-kamilah_al-sajjadiyya_.txt` | |
| Risalat al-Huquq | `treatise_on_rights_risalat_al-huquq.txt` | 928 lines — verify the entry count here |
| Uyun Akhbar al-Rida | `uyun_akhbar_ar-ridha_volume_1.txt`, `..._volume_2.txt` | Both volumes |
| Kitab al-Irshad (al-Mufid) | `irshad--kitab-al-irshad-1.txt`, `irshad--kitab-al-irshad-part-1.txt` | Two copies of the same work |
| Sira — Subhani, *The Message* | `sira-subhani--the-message-201506.txt` | |
| Fourteen Infallibles | `fourteen--the-fourteen-infallibles.txt`, `fourteen--nuqoosh-e-ismat-...txt` | Two works |
| Qarashi — *Life of Imam al-Kadhim* | `qarashi--the-life-of-imam-musa-bin-jafar-al-kazim.txt` | 1 of 6 in the series |
| Qarashi — *Life of Imam al-Mahdi* | `qarashi--the-life-of-imam-mahdi-a-s.txt` | 2 of 6 in the series |

---

## Present but degraded — do not rely on as-is

| File | Problem | Impact |
|---|---|---|
| `kafi--alkafi-201601.txt` | Only **Part 1 (Usul, to p 532)**. al-Kafi runs to eight volumes. | al-Kafi is the rank-4 *fallback*, so low risk — but any saying expected in a later volume (furu', rawda) is not here. |

---

## Missing — no usable text on disk

Ordered by what it blocks. These are the real holes.

### 1. Occultation / four deputies — **fully missing**
- **Works:** al-Saduq, *Kamal al-Din*; and/or Jassim Hussain, *The Occultation of the Twelfth Imam*.
- **Blocks:** Envelope 10 — the four deputies, named and in sequence, and the seventy-year span.
- **Status:** no file, no PDF in the manifest. `fetch_sources.py` target `occultation` (tier 2) has never landed a file.
- **Where to look:** `python tools/fetch_sources.py --only occultation` prints archive.org queries plus al-islam.org links (al-islam.org blocks scripts — open in a browser).

### 2. World-history reference — **missing and unfixed**
- **Work:** one fixed world-history timeline for the whole project.
- **Blocks:** all fourteen "elsewhere in the world" bullets (Tier 3) — the easiest claims in the product for a hostile reader to check.
- **Status:** two *Timetables of History* PDFs are recorded in `manifest.json` but both are **DRM-encrypted and will not extract** — no text file exists for either. **A different reference is required.** This gap is the one flagged unfixed in `HANDOVER.md`.

### 3. Later Qarashi lives — **4 of 6 missing**
- **Works:** Baqir Sharif al-Qarashi, *Life of Imam* al-Jawad, al-Rida, al-Hadi, al-Askari.
- **Blocks:** Envelopes 05, 07, 11, 13 (per `sources-needed.md`); the examination of al-Jawad; the crown-prince conditions; the night house search.
- **Status:** only al-Kadhim and al-Mahdi are on disk. `fetch_sources.py --only qarashi` lists the per-imam al-islam.org pages.

### 4. A Shia history for the imams' period — **missing, and now without a candidate**
- **Needed for:** the ruler bullet in all fourteen fact panels, and the political background of envelopes 04, 08, 11, 13, 14.
- **Was going to be:** al-Tabari (SUNY), vols covering 40–260 AH. **Excluded — Sunni work, hard rule.**
- **Now needs:** a Shia history or biographical work covering the same span. `al-Irshad` carries part of it; the Qarashi lives may carry more. Neither is fixed as an edition.


## Not a text, but tracked here because it gates the same work

These are in `sources-needed.md`; noted so the ledger is complete.

| Item | Tier | Blocks |
|---|---|---|
| Fixed editions table (translator/publisher/year/permission) in `sourcing-rules.md` | 1 | **Empty.** Blocks every hadith card — a card set against one edition and printed against another cites the wrong page. |
| A Hijri–Gregorian converter, and the jamaat calendar | 4 | Every fact-panel headline, every month stamp, the running order |
| A named scholar, engaged | 5 | Envelope 06 (blocks the whole print run), all fourteen death lines, and eleven other sign-offs |

---

## One-line summary

Tier 1 is complete. The blocking holes are all in Tier 2–3 narrative/history:
**occultation (Envelope 10), a world-history reference (all 14 bullets), four
Qarashi lives (Envelopes 05/07/11/13), and a **Shia** history covering 40–260 AH (the
ruler bullets).** Guillaume and both Tabari files were deleted on 2026-08-12 under the
Shia-sources-only rule.
