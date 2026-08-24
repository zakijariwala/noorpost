# Hadith cards — verification worklist

Written 2026-08-24, alongside the selection pass. **This is a brief for a second pair of eyes, not a to-do list for the person who made the selections.**

The record is `hadith-assignments.json`. `tools/apply_hadith_assignments.py` writes the card row into every entry file from it, so **correct the JSON and re-run the tool — never edit an entry file's card row by hand.**

---

## What is being asked

Every row below carries a saying that is **really in the edition, at the number given** — the selector quotes verbatim from `00-sources/text/tuhaf_al-uqul.txt` and cannot invent one. That is not what needs checking.

**Three things need checking, in this order:**

1. **Does the saying actually meet the theme?** The selector matched on vocabulary. Vocabulary is not meaning, and a `low` row usually means one word carried the whole match.
2. **Is it conduct, or has something theological slipped through?** `sourcing-rules.md` subject limits. The filter is a word list and a word list is porous.
3. **Does it read to an eight-year-old, out loud, off a card?** A maxim that needs a gloss has failed even if the match is perfect.

Two further rules the selector already enforces mechanically, so they need spot-checking rather than auditing: **no card repeats its Masoom's box card**, and **no two companion cards carry the same saying**.

---

## To verify — 22 rows

| # | Entry | Points to | Theme | Saying | Ref | Conf | Why it is here |
|---|---|---|---|---|---|---|---|
| 01 | Salman al-Farsi | the Prophet | who counts as family | “Regard your relatives even by means of mere greeting.” | short maxims of the Prophet, no. 165 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 04 | Sumayyah bint Khabbat | the Prophet | holding on when it is not safe to | “Blessed are those who leave a current passion for obtaining a promised one that they have not seen yet.” | short maxims of the Prophet, no. 119 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 05 | Nusaybah bint Ka'b | the Prophet | courage that shields somebody else | “It is illicit to violate anything of the believer: his honor, wealth, and blood—all are sanctified.” | short maxims of the Prophet, no. 164 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 06 | Umm Ayman | the Prophet | care that lasts a whole life | “Hearts are molded on cherishing those who treat them charitably and abhorring those who treat them nastily.” | short maxims of the Prophet, no. 17 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 07 | Halima al-Sa'diyya | the Prophet | kindness to a child in your care | “Kindness gives embellishment to everything it joins, and clumsiness ruins everything it joins.” | short maxims of the Prophet, no. 95 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 08 | Asma bint Umays | the Prophet | staying through every upheaval | “The proper fulfillment of the pledges is a part of faith.” | short maxims of the Prophet, no. 100 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 11 | Qambar | Imam Ali | service, and what a servant is owed | “Every powerful that is under God's control is humble.” | short maxims of Imam Ali, no. 95 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 12 | Malik al-Ashtar | Imam Ali | gentleness in authority | “People's similarity to their rulers is more than their similarity to their fathers.” | short maxims of Imam Ali, no. 57 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 13 | Fatima bint Asad | Imam Ali | raising a child who is not your own | “A true friend is that who regards in misfortunes, absence, and after death.” | short maxims of Imam Ali, no. 129 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 15 | Abbas ibn Ali | Imam Husayn | a trust kept when nobody would have known | “Favors should be like the heavy rain that covers the pious and the sinful.” | short maxims of Imam al-Husayn, no. 3 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 16 | Umm Kulthum bint Ali | Imam Husayn | children, in the worst of it | “Beware of things for which you apologize.” | short maxims of Imam al-Husayn, no. 16 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 18 | Zaynab bint Ali | Imam Husayn | the truth said in front of a ruler | “He who tries to achieve something through acting disobediently to God will miss what he expects and fall in what he fears.” | short maxims of Imam al-Husayn, no. 19 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 23 | Tawus al-Yamani | Imam al-Sajjad | worship nobody is watching | “Many are those whom are deceived by commendation.” | short maxims of Imam al-Sajjad, no. 23 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 26 | Umm Farwa | Imam al-Sadiq | honouring a mother by name | “A twenty-year friendship is kinship.” | short maxims of Imam al-Sadiq, no. 16 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 27 | Safwan al-Jammal | Imam al-Kadhim | the earnings you refuse | “The expiation of working with the (unjust) rulers is to treat the friends with kindness.” | short maxims of Imam al-Kadhim, no. 20 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 28 | Hamida Khatun | Imam al-Kadhim | teaching, and who is fit to teach | “The astonishment of the ignorant at the intelligent is greater than the astonishment of the intelligent at the ignorant.” | short maxims of Imam al-Kadhim, no. 34 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 29 | Dibil al-Khuza'i | Imam al-Rida | saying the thing out loud | “When you want to mention a present person, you should use his surname, but when you refer to an absent person, you should use his name.” | short maxims of Imam al-Rida, no. 13 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 30 | Sayyida Ma'suma | Imam al-Rida | family, and the road toward it | “The elder brother is as same as the father.” | short maxims of Imam al-Rida, no. 10 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 31 | Ali ibn Mahziyar | Imam al-Jawad | discharging a trust, every time | “A believer is in need of successfulness from God, a self-preaching, and accession to the advisers.” | short maxims of Imam al-Jawad, no. 13 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 32 | Abu Hashim al-Ja'fari | Imam al-Hadi | giving before being asked | “The thankful of a grace should be happy for thankfulness more than it is for the grace.” | short maxims of Imam al-Hadi, no. 10 | `low` | One weak signal carried the match. Most likely to be replaced. |
| 33 | Ahmad ibn Ishaq al-Qummi | Imam al-Askari | carrying other people's questions | “Those who advice their friends secretly are respecting them, and those who advice them openly are humiliating them.” | short maxims of Imam al-Askari, no. 33 | `medium` | Plausible, not obviously right. Read it against the entry's letter. |
| 34 | Uthman ibn Sa'id al-Amri | Imam al-Askari | trustworthiness | “The faithful believer is a blessing for the believers and a claim against the disbelievers.” | short maxims of Imam al-Askari, no. 20 | `low` | One weak signal carried the match. Most likely to be replaced. |

### The seven that are not on this list

`high` rows, recorded so the list is the whole picture: Bilal, Abu Dharr, Maytham al-Tammar, Qais ibn Sa'd, Sayyida Ruqayya, Jabir ibn Abdullah, Hisham ibn al-Hakam. Spot-check them; do not re-derive them.

---

## Blocked — 10 rows, and none of them is a verification job

These need a source or a decision. Do not attempt to fill them from memory.

| # | Entry | Points to | Blocker |
|---|---|---|---|
| 09 | Fizza | Sayyida Fatima | No credited edition of her sayings is held. Searched all 32,531 Thaqalayn records and every fixed edition: two passages read as her speaking, both inside al-Kafi narrator chains, neither a conduct maxim. Same blocker as box card 06. |
| 17 | Rabab bint Imra' al-Qays | Imam Husayn | Tuhaf's Imam al-Husayn short-maxims section is exhausted — see the worklist. Four of his eight rows cannot be filled from anything held. |
| 19 | Sakina bint al-Husayn | Imam Husayn | Tuhaf's Imam al-Husayn short-maxims section is exhausted. |
| 20 | Fitrus | Imam Husayn | Tuhaf's Imam al-Husayn short-maxims section is exhausted. |
| 21 | Umm al-Banin | Imam Husayn | Tuhaf's Imam al-Husayn short-maxims section is exhausted. |
| 35 | Muhammad ibn Uthman al-Amri | Imam al-Mahdi | Both Kitab al-Ghayba works are now held with named translators, so this is a search job rather than a purchase — but no conduct-register tawqi' surfaced in the pool, and rule Q3 bans one about religious authority. |
| 36 | Husayn ibn Ruh al-Nawbakhti | Imam al-Mahdi | Same as 35 — Kitab al-Ghayba held, no conduct-register tawqi' found. |
| 37 | Ali ibn Muhammad al-Samarri | Imam al-Mahdi | Same as 35 — Kitab al-Ghayba held, no conduct-register tawqi' found. |
| 38 | Narjis Khatun | Imam al-Mahdi | Same as 35 — Kitab al-Ghayba held, no conduct-register tawqi' found. |
| 39 | Khawla bint al-Azwar | nobody | Points to no Masoom, so the selection rule has nothing to draw on. Needs the scholar's call on whether the entry survives at all — a decision, not a source. |

### The two that would unblock eight items

**A credited edition carrying Sayyida Fatima's short sayings** closes row 09 (Fizza) *and* box card 06. **A conduct-register tawqi'** closes rows 35–38 *and* box card 10 — and both `Kitab al-Ghayba` works are already held with named translators, so that one is reading, not buying.

**Imam al-Husayn's four blocked rows are a different shape.** Nothing is missing from the library; Tuhaf's section for him is simply nine items long and four of them are unusable. Closing rows 17, 19, 20 and 21 means fixing a second edition that carries his sayings, and recording it in `sourcing-rules.md` first.

---

## How to record a correction

```bash
# 1. edit 00-foundations/hadith-assignments.json — the saying, ref and confidence
# 2. rewrite every entry file's card row from it
python tools/apply_hadith_assignments.py
# 3. see what else is available for that Masoom
python tools/select_hadith_cards.py --propose --entry "Umm Farwa" --top 8
```

Raising a row to `high` is a real decision and should say who made it. Nothing on this list prints while it still reads `low`.
