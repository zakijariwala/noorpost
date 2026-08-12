# Spec check — all fourteen letters

Measured, not estimated. Counts taken from the text between the `LETTER START` / `LETTER END` markers in each file.

Re-run after any edit:

```bash
for f in 01-pilot/envelope-03/letter.md 03-content/envelope-*.md; do
  body=$(awk '/LETTER START/,/LETTER END/' "$f" | grep -v 'LETTER ')
  w=$(echo "$body" | sed 's/^[●○]*//' | wc -w)
  c=$(echo "$body" | grep -c '^○'); t=$(echo "$body" | grep -c '^●○')
  max=$(echo "$body" | grep '^○' | sed 's/^○ //' | awk '{print NF}' | sort -rn | head -1)
  echo "$(basename $f) words=$w child=$((c+t)) max=$max"
done
```

---

| # | Masoom | Letter | Words | Child lines | Longest child line | Demand line | ●○ close |
|---|---|---|---|---|---|---|---|
| 01 | Imam Husayn | *The Man Who Was Sent to Stop Them* | 366 | 7 | 12 | ✓ | ✓ |
| 02 | Imam Hasan | *The Word He Did Not Answer* | 349 | 6 | 13 | ✓ | ✓ |
| 03 | Prophet Muhammad | *The Cloak* | 367 | 8 | 14 | ✓ | ✓ |
| 04 | Imam al-Askari | *The Man Who Could Not Leave His Street* | 357 | 7 | 12 | ✓ | ✓ |
| 05 | Imam al-Baqir | *The Small Boy on That Ground* | 361 | 6 | 12 | ✓ | ✓ |
| 06 | Sayyida Fatima | *Thirty-Four, Thirty-Three, Thirty-Three* | 338 | 7 | 13 | ✓ | ✓ |
| 07 | Imam Ali | *The Man Who Lost in Court* | 364 | 8 | 13 | ✓ | ✓ |
| 08 | Imam al-Kadhim | *Four Years and No Charge* | 357 | 6 | 12 | ✓ | ✓ |
| 09 | Imam al-Sajjad | *The List* | 367 | 7 | 12 | ✓ | ✓ |
| 10 | Imam al-Mahdi | *Letters In, Answers Out* | 348 | 7 | 12 | ✓ | ✓ |
| 11 | Imam al-Hadi | *What They Found in the House* | 338 | 7 | 14 | ✓ | ✓ |
| 12 | Imam al-Sadiq | *The Years Nobody Was Watching* | 338 | 6 | 13 | ✓ | ✓ |
| 13 | Imam al-Rida | *The Job He Would Not Do* | 349 | 8 | 13 | ✓ | ✓ |
| 14 | Imam al-Jawad | *The Room Full of Grown-Ups* | 356 | 6 | 14 | ✓ | ✓ |

**All fourteen inside 330–370. All inside 6–9 child lines. No child line reaches 15 words. Every letter carries a line that demands a response and closes on ●○.**

Child-line count includes the closing ●○ line, which the child reads.

---

## Session types — assignment check

| Type | Required | Assigned | Envelopes |
|---|---|---|---|
| Conversation | 7 | 7 | 03, 05, 06, 07, 09, 12, 13 |
| Case File | 4 | 4 | 04, 08, 11, 14 |
| Mourning | 2 | 2 | 01, 02 |
| Open | 1 | 1 | 10 |

Every Conversation card carries five questions, one marked ● **grown-up answers first**, one marked ⚑ **hard for a grown-up**.

Every Case File carries a question, five evidence cards and a sealed answer, with the instruction that the parent opens the seal only when the child commits.

Both Mourning cards carry one passage, one question and two minutes of silence. No game, no points, no stickers — a pennant instead.

---

## Silsila — historical order against calendar order

The card number is the segment number. **The envelope number never prints on a card.**

| Segment | Masoom | Arrives in envelope |
|---|---|---|
| 1 | Imam Ali | 07 |
| 2 | Imam Hasan | 02 |
| 3 | Imam Husayn | 01 |
| 4 | Sayyida Fatima | 06 |
| 5 | Imam al-Sajjad | 09 |
| 6 | Imam al-Baqir | 05 |
| 7 | Imam al-Sadiq | 12 |
| 8 | Imam al-Kadhim | 08 |
| 9 | Imam al-Rida | 13 |
| 10 | Imam al-Hadi | 11 |
| 11 | Imam al-Askari | 04 |
| 12 | Imam al-Jawad | 14 |
| 13 | Prophet Muhammad | 03 |
| 14 | Imam al-Mahdi | 10 |

**Two decisions are embedded here and both need confirming.**

1. **Segments 13 and 14.** The Prophet is numbered 13 and al-Mahdi 14 in this draft, which puts the Prophet late in a sequence that otherwise runs chronologically. Two defensible schemes exist — the Prophet first and everyone else after him, or strict order of imamate with him outside the numbering entirely. **Pick one and apply it to all fourteen cards.** As drafted the file is internally consistent but the choice has not been made deliberately.
2. **Sayyida Fatima's position** in a sequence of imamate is not a matter of ordering but of what the chain is a chain *of*. **Scholar decides.**

The last card in the silsila arrives in envelope 10, and four envelopes come after it. That is deliberate — see `envelope-10.md`.

---

## The calendar ring — fourteen event prints

| Ring position | Event | Envelope |
|---|---|---|
| 1 | Karbala | 01 |
| 2 | Arbaeen | 02 |
| 3 | The Hijra — the arrival at Quba | 03 |
| 4 | Samarra | 04 |
| 5 | Sayyida Zaynab at Damascus | 05 |
| 6 | Bayt al-Ahzan | 06 |
| 7 | The Kaaba | 07 |
| 8 | Hira and the Mab'ath | 08 |
| 9 | Munajat Sha'baniyya | 09 |
| 10 | Jamkaran | 10 |
| 11 | Laylat al-Qadr | 11 |
| 12 | Eid al-Fitr | 12 |
| 13 | Qom | 13 |
| 14 | Ghadir Khumm | 14 |

---

## The women — one per envelope

Umm al-Banin · Zaynab · Khadija · Nargis · **Zaynab** · Fizza · Fatima bint Asad · Hamida · Shahrbanu · Hakima Khatun · Samana · Umm Farwa · Sayyida Masuma · Umm al-Fadl

**Thirteen distinct women in fourteen slots.** Zaynab holds 02 and 05. Decide before Gate 3.

Marked traditional: Fizza (06), Shahrbanu (09), Hakima Khatun (10), Nargis (04), and parts of Umm al-Banin (01).

**Umm al-Fadl (14) conflicts with her envelope's death line.** See `envelope-14.md` and `00-foundations/death-lines.md`.

---

## What is still open across all fourteen

| Blocker | Scope |
|---|---|
| Fixed translation editions | Every hadith card. **Fourteen cards, none selectable.** |
| The sira gap | Every letter's citations. See `citation-sheet.md` open question 1 |
| A general reference for "elsewhere in the world" | Fourteen bullets |
| Named scholar | All fourteen. **Envelope 06 blocks the print run.** |
| 05 / 11 swap | Two envelopes, entirely |
| Zaynab repeat | 02 and 05 |
| Umm al-Fadl | 14 |
| Silsila numbering scheme | All fourteen cards |
| Ring punch position | All fourteen event prints |
| Artwork | Everything. **Pending by instruction.** |
| Timing with real families | All fourteen. Nothing here has been read aloud to a child yet. |
