# Noor Post — Phased Task List

Sequential build plan derived from the PRD. Phases run in order. Each phase ends in a gate that must pass before the next phase starts. Within a phase, tasks marked **∥** can run in parallel.

Two hard constraints drive the whole sequence:

1. **All fourteen envelopes must be printed before a single subscription is sold.** Monthly must be a posting job, never a production job. This pushes all commerce work behind production.
2. **The madrasa price test comes before the full build.** One finished envelope and one zine are enough to run it. Everything else before that test is desk work.

---

## Phase 0 — Foundations

Nothing gets written or drawn until the rules are fixed. Rewriting fourteen envelopes because a rule changed late is the single most expensive mistake available.

### 0.1 Editorial rulebook
- [x] Write the house style sheet from PRD §7 and §8 as a checkable list, one line per rule. → `00-foundations/editorial-rulebook.md`
- [x] Define the two-voice letter spec in enforceable terms: 330–370 words, 6–9 child lines, child lines under 15 words, at least one line demanding a response, last line read together. → rulebook §1
- [x] Write the reading-age test for child lines. Pick one word list an eight-year-old is assumed to know; anything outside it needs a decision. → rulebook §2, Dolch + Fry 1000 + a named madrasa list
- [x] Fix the fact panel skeleton: bullet order, the fixed woman slot, the fixed death slot as the last line, citation format and point size. → `00-foundations/fact-panel-spec.md`
- [x] Write the standard difference-of-opinion line verbatim. → `00-foundations/standard-lines.md` §1, with the seven places it is used
- [x] Write the standard traditional-account marker, the exact words used in the child's copy. → `standard-lines.md` §2, long and short forms
- [x] Write the death-line formula and draft all fourteen at once. → `00-foundations/death-lines.md`. **Surfaced three problems the PRD does not address — read that file.**
- [x] Write the envelope sign-off checklist. → `00-foundations/checklist.md`

### 0.2 Source library ∥
- [ ] Acquire published translations in priority order: Tuhaf al-Uqul, Nahj al-Balagha, Sahifa Sajjadiyya, al-Kafi, Uyun Akhbar al-Rida.
- [ ] Record translator, publisher, edition and year for each. Credit lines are needed on the cards.
- [x] Build a citation sheet: one row per hadith or passage, with text, source, hadith or page number, and the translation credited. → `00-foundations/citation-sheet.md`, with status codes, the AH→CE table, and the fourteen women's rows. **Nothing prints on `TV`.**
- [x] Rule set for sourcing, written down. → `00-foundations/sourcing-rules.md`
- [ ] **Close the sira gap. Fully open again as of 2026-08-12.** It was briefly closed for envelope 03 with Guillaume's Ibn Ishaq, plus SUNY al-Tabari Vol. VIII — **both Sunni, both removed under the hard rule in `sourcing-rules.md`.** It must now be closed with a Shia work. **Acquiring al-Mufid's `Kitab al-Irshad` with a named translator is the single highest-value purchase in the project**; it has to carry the narrative spine of most of the fourteen letters and much of the companions line.
- [ ] **Fix one general reference for the "elsewhere in the world" bullet.** Fourteen claims about world history with no source rule at all.
- [ ] Build the fact bank per Masoom: ruler of the day, length of the imamate, named students, attributed compilations, what was happening elsewhere in the world that year. This is the raw material for all fourteen fact panels and it is the slowest research task in the project. Start it now, finish it during Phase 3.

### 0.3 Scholarly review line ∥
- [ ] Identify and approach a named scholar willing to sign wording.
- [ ] Agree scope, turnaround and how sign-off is recorded.
- [ ] Flag envelope 06 (Sayyida Fatima) explicitly at the outset as line-by-line review, not a skim. It does not print without a signature.
- [ ] Agree what happens on disagreement: who has the final word on wording.

### 0.4 Design system ∥
- [x] Pick and license the two typefaces: body face and display face for child lines. → `00-foundations/design-system.md` §1 — EB Garamond / Fraunces, both SIL OFL
- [x] Build the palette. Standard palette plus the mourning palette for envelopes 01 and 02. → §2
- [x] Design the seven item templates: letter with fact panel reverse, hadith card, person print (A5 portrait), event print (landscape, punched), session card, sticker sheet, return postcard. → §4. Sizes and layout fixed; final art is Phase 4.
- [x] Design the pennant that replaces the sticker sheet in mourning issues. → §4. Material and ink fixed; exact dimension deliberately left for a physical proof, not a ruler.
- [x] Design the envelope exterior: circular postal cancellation month stamp, name area, wax-seal sticker. → §5
- [x] Design the inside-flap block that carries the running order and the runtime. → §5
- [x] Set the illustration style rules. Note the split: no faces in the Fourteen, faces allowed in the companions line. → §3
- [x] Decide the calendar ring hole position and spacing once. All fourteen event prints must clip onto the same ring. → §6 — 6mm hole, 12mm from edge (ISO 838 sizing), 25mm book ring. **Physically proof before Phase 4 art is finalised.**
- [x] Number the hadith cards by silsila segment, in historical order. Never print the envelope number on the card. → §7

**Gate 0:** Rulebook, citation format, scholar relationship and templates all exist. Sources are in hand.

**Design system is a first fixed draft, not a finished art direction.** It unblocks Phase 4 art from starting without a design brief; it does not replace physically proofing the ring punch, the pennant, or the CMYK/foil builds before they're committed to a print run (see design-system.md §"What this doesn't settle").

---

## Phase 1 — Pilot

One finished envelope and one zine. Real print, real paper, real stock. Not a PDF.

- [x] Envelope 03 written: letter (*The Cloak*, 367 words, 8 child lines), fact panel, Conversation session card, and specs for the other five items. → `01-pilot/envelope-03/`
- [ ] Produce artwork for envelope 03's five remaining items. Blocked on the ring punch position and the fixed Tuhaf al-Uqul edition — see `01-pilot/envelope-03/items.md`.
- [ ] Fact-check envelope 03 against the citation sheet. Every claim traceable.
- [ ] Scholar review on envelope 03.
- [ ] Prepress and short-run print envelope 03: all seven items, envelope, seal, stamp.
- [ ] Produce one zine, Ghadir Khumm. One A4 sheet, folded to eight pages, one cut, single ink. Prints on equipment already owned.
- [ ] Run the session with two or three real families in the 8–12 range. Time it. Target twenty-five minutes.
- [ ] Record what actually happened: where the child lost interest, where the parent stumbled, whether the adult learned the new thing, whether the activity genuinely needed two people.
- [ ] Revise the templates from what the session showed. Cheap now, ruinous in Phase 5.

**Gate 1:** One envelope exists physically, has been used by a real family, and the runtime is inside the target.

---

## Phase 2 — Channel test

The test that matters. It comes before the full build, not after.

- [ ] Cost the unit properly: paper, printing, illustration amortised across the run, envelope, seal, sticker, box, assembly labour.
- [ ] Cost domestic post per envelope and international parcel per box.
- [ ] Take the finished envelope and the zine to a madrasa administrator. Ask what forty sets would need to cost.
- [ ] Repeat with at least three institutions. One conversation is an anecdote.
- [ ] Work the KSIJ directory relationships into a target list of jamaats and madrasas.
- [ ] Compare their number against the true unit cost.
- [ ] Set the flagship price. Set the institutional bulk price. Set the Named Edition premium at flagship plus 25–30%. Set the companions envelope at an impulse price.
- [ ] Decide the print run size from institutional interest, not from hope.

**Gate 2:** At least one institution has named a workable number for forty sets, and the unit economics survive it. If nothing survives, stop and rework the format or the channel before spending on Phase 3.

---

## Phase 3 — Content build, all fourteen

Write everything before drawing anything. Art follows locked text.

### 3.1 Calendar and anchors
- [ ] Confirm the running order against your jamaat's calendar.
- [ ] Decide the two weak anchors: al-Baqir (05) and al-Hadi (11). Swap them with each other if the convention favours it. Decide once, then freeze — every downstream item depends on the month.
- [ ] Resolve the split-date anchors: Imam Hasan 7th or 28th Safar, the Prophet 12th or 17th Rabi al-Awwal. Both take the differ-by-community line.

### 3.2 Letters

**All fourteen written.** Counts measured, not estimated — see `03-content/spec-check.md`. Every letter is inside 330–370 words with 6–9 child lines, no child line at 15 words, a line that demands a response, and a ●○ close.

Written in this order, which front-loaded the strongest content and the hardest reviews.

- [x] 09 Imam al-Sajjad — Risalat al-Huquq. Strongest piece in the box. Write it second overall, after the pilot.
- [x] 14 Imam al-Jawad — the public examination at eight years old.
- [x] 01 Imam Husayn — Hurr. Ends before Ashura afternoon.
- [x] 02 Imam Hasan — the treaty, through the man who insulted him. Draft exists in the Safar pack.
- [x] 08 Imam al-Kadhim — four years in prison, no charge. Draft exists in the merged spec.
- [x] 07 Imam Ali — the shield case and the judge who ruled against him.
- [x] 12 Imam al-Sadiq — the teaching circle and the named students.
- [x] 13 Imam al-Rida — crown prince on conditions, title without the job.
- [x] 04 Imam al-Askari — the wikala network out of Samarra.
- [x] 11 Imam al-Hadi — the night house search.
- [x] 05 Imam al-Baqir — a child at Karbala, later the school in Medina.
- [x] 10 Imam al-Mahdi — the minor occultation and the four deputies.
- [x] 06 Sayyida Fatima — the tasbih. Written carefully; the letter avoids the disputed ground entirely.

For each letter: 330–370 words, voice marks assigned, child lines counted and word-length checked, read aloud and timed to four to four and a half minutes.

### 3.3 Fact panels
**All fourteen written.** Every claim marked `TO VERIFY` pending sources.
- [x] One per envelope, following the fixed skeleton.
- [x] The "one new thing for the adult" identified per envelope. Non-negotiable; the PRD names all fourteen.
- [x] The woman slot filled per the assignments: Umm al-Banin, Zaynab, Khadija, Nargis, Zaynab, Fizza, Fatima bint Asad, Hamida, Shahrbanu, Hakima Khatun, Samana, Umm Farwa, Sayyida Masuma, Umm al-Fadl.
- [x] Traditional accounts marked: Fizza's twenty years of Qur'anic answers, Bayt al-Ahzan, Shahrbanu's origin. Also Nargis (04) and Hakima Khatun (10).
- [x] Death line last, formula applied, no method, no symptoms, no final hours. **Envelope 06's is a placeholder — the scholar writes it.**
- [x] Check the through-question is answered in every issue: what did he do with the freedom he had? Stated per envelope under *How much room he had*.

### 3.4 Hadith cards
**Blocked in full.** No saying can be selected until the fixed editions are settled — a card written against one edition and printed against another cites the wrong page.
- [x] Write the fourteen silsila segments and assign segment numbers. Historical order fixed in `03-content/spec-check.md`. **Two numbering decisions still open — see that file.**
- [ ] Select fourteen sayings, sourced in priority order, ethics and conduct only.
- [ ] Envelope 10 takes a tawqi' from the minor occultation.
- [ ] Write the fourteen silsila segments, historical order, so they read as one chain when the cards are stacked.
- [ ] Number by segment. Check no envelope number leaked onto a card.

### 3.5 Session cards
**All fourteen written**, and the type counts check out against the PRD: 7 / 4 / 2 / 1.
- [x] Conversation ×7 (03, 05, 06, 07, 09, 12, 13): five questions each, one answered by the adult first, one hard for an adult.
- [x] Case File ×4 (04, 08, 11, 14): question, five evidence cards, sealed answer. The parent opens the seal only when the child commits.
- [x] Mourning ×2 (01, 02): one passage, one question, one instruction to sit quietly. No game, no points. Envelope 02 uses the Jabir passage.
- [x] Open ×1 (10): no answer card, no five questions.
- [x] Audit every activity for two roles. Anything one person can do alone gets rewritten.

### 3.6 Review
- [ ] Fact-check all fourteen against the citation sheet.
- [ ] Scholar review, all fourteen.
- [ ] **Envelope 06 signed line by line by a named scholar. Blocking.** No signature, no print.

**Gate 3:** Fourteen letters, fourteen fact panels, fourteen hadith cards and fourteen session cards are written, checked, and signed off. Text is frozen.

> ⚠ **Gate 3 blocker found 2026-08-12: no letter fits its page.** Every letter template — all fourteen here and all thirty-nine companions — renders 28–76% taller than the A5 sheet it is specified on. The rendered PDFs clip the excess silently and still look like valid proofs. **The word-count spec (330–370), the A5 single-side spec, and the type spec are mutually incompatible; one of the three has to give.** Four options with costs are laid out in `04-art/print/README.md`. This is a text-and-format decision, so it belongs before the freeze, not at prepress.

---

## Phase 4 — Art build

- [ ] 14 person prints. Note the repeats and the pairings: Jannat al-Baqi appears three times at three angles (02, 05, 09); Samarra pairs 04 and 11; Kadhimiya in 14 pairs with the barred window in 08. Draw them as a deliberate set, not one at a time.
- [ ] 14 event prints. Common landscape format, common ring punch. They must hang together as one calendar.
- [ ] 12 sticker sheets, plus 2 pennants for the mourning issues.
- [ ] 14 return postcards, pre-addressed, two signature lines.
- [ ] 14 envelope exteriors with the circular month cancellation.
- [ ] Wax-seal stickers.
- [ ] Box design.
- [ ] Lay all 42 collectible pieces out together and check the three collections read as sets: hadith cards in the Qur'an, person prints on the wall, event prints on the ring.

**Gate 4:** All art approved. Ring test passed with physical proofs on the actual ring.

---

## Phase 5 — Production

- [ ] Prepress all fourteen envelopes: bleed, trim, ink, punch positions.
- [ ] Get quotes at the run size set in Phase 2.
- [ ] Print one full physical proof envelope. Check against the pilot learnings.
- [ ] Print the full run, all fourteen, complete.
- [ ] Print the digital-variable Named Edition components: names on envelopes, plus Noori's letter to the child by name.
- [ ] Produce the Named Edition colourways: rose, sage, plum, ochre. Flat ribbon only, never bows.
- [ ] Assemble, seal and box.
- [ ] Store finished stock, sorted by envelope number, ready for monthly posting.

**Gate 5: this is the hard gate.** Fourteen finished envelopes sit in the cupboard. Only now can a subscription be sold.

---

## Phase 6 — Commerce

- [ ] Set up the SKUs: The Fourteen — Box; The Fourteen — Monthly (India only); The Named Edition; Everyone Else; Noori's Notebook.
- [ ] Build the storefront.
- [ ] **Bill the monthly annually.** Charge for the year upfront, deliver monthly. Delivery schedule, not a billing schedule.
- [ ] Build the Named Edition order flow: name capture, colourway choice by the child, ribbon and seal. Note that bulk orders ship standard.
- [ ] Build the institutional order path: bulk pricing, invoicing, single-parcel delivery.
- [ ] Set international shipping for the box. One parcel, priced honestly.
- [ ] Set the domestic monthly posting workflow and calendar. Each envelope posts to land before its date.
- [ ] Decide the mid-year subscription start rule: does a buyer joining in Rajab start at envelope 01 or at the current month?
- [ ] Build the return postcard handling process. Decide what comes back and what happens when it does.

**Gate 6:** An order can be placed, paid for, fulfilled and delivered end to end. Test with one real order before announcing anything.

---

## Phase 7 — Launch

- [ ] Institutional first. Go back to the jamaats and madrasas from Phase 2 with finished product and their own quoted number.
- [ ] Close the first bulk orders. Forty sets solves discovery, shipping and fulfilment in one transaction.
- [ ] Open direct sales.
- [ ] Open monthly subscriptions, India only.
- [ ] Hand zines out at majlis.

---

## Phase 8 — Companions line, "Everyone Else"

Runs after launch. It is a first purchase and a gift, not the flagship.

**Thirty-nine written — all fourteen Masoomeen have a companion, all four nayibs of the occultation are covered, and the line stands at twenty men to eighteen women plus Fitrus.** Letters and fact panels, in `08-companions/`. Artwork pending.

- [x] Build the four-item template: two-voice letter with fact panel on the reverse, person print, sticker sheet, return postcard.
- [x] Enforce the two protective rules in the template itself: **no hadith card, no event print, ever.** Those two carry the silsila and the calendar ring. The box must stay the only way to complete anything.
- [x] Set the faces-allowed illustration style (specified per envelope; artwork pending). A child sees the difference instantly.
- [x] Write the first six: Salman al-Farsi, Bilal, Maytham al-Tammar, Qambar, Abu Dharr, Malik al-Ashtar. All six letters inside 330–370 words, 7–8 child lines.
- [x] Write four more, chosen to reach Masoomeen the first six didn't touch: Uthman ibn Sa'id al-Amri (al-Mahdi's deputy network), Abbas ibn Ali (Husayn), Fizza (Fatima), Jabir ibn Abdullah al-Ansari (al-Baqir). Same word count and child-line rules.
- [x] Write the next eight, closing every remaining Masoom gap: Qais ibn Sa'd (Hasan), Tawus al-Yamani (al-Sajjad), Safwan al-Jammal (al-Kadhim), Dibil al-Khuza'i (al-Rida), Ahmad ibn Ishaq al-Qummi (al-Askari), Abu Hashim al-Ja'fari (al-Hadi), Hisham ibn al-Hakam (al-Sadiq), Ali ibn Mahziyar (al-Jawad). **All fourteen Masoomeen now have a companion.** These rest on narrower, more specific episodes than the first ten — real citation work needed before print, not a light pass.
- [x] Write eight women, closing a different gap: seventeen of the first eighteen companions were men. Sumayyah bint Khabbat, Nusaybah bint Ka'b, Umm Ayman, Halima al-Sa'diyya, Asma bint Umays, Khawla bint al-Azwar, Umm Kulthum bint Ali, Rabab bint Imra' al-Qays. **Khawla's entry needs a scholar decision on whether it survives at all** — the most historically uncertain account in the whole companions line.
- [x] **Decided (2026-08-12): "Everyone Else" includes family members and traditional/miraculous figures, not just servants and companions in the strict sense.** See `08-companions/README.md` "Scope, decided." Drafted Zaynab bint Ali, Sakina bint al-Husayn, and the angel Fitrus on this basis.
- [x] Write the other three nayibs of the minor occultation — Muhammad ibn Uthman al-Amri, Husayn ibn Ruh al-Nawbakhti, Ali ibn Muhammad al-Samarri — completing the set of four alongside Uthman ibn Sa'id. Same occultation restraint as `envelope-10.md`: no theology, the working life of the post only.
- [x] Write seven more women, skewed 7-to-3 against this batch's three men, moving the line further toward parity: Fatima bint Asad (Imam Ali), Umm al-Banin (raised Hasan and Husayn, mother of Abbas), Hamida Khatun (al-Kadhim), Umm Farwa (al-Sadiq), Narjis Khatun (al-Mahdi), Sayyida Ma'suma (al-Rida's sister), and Sayyida Ruqayya bint al-Husayn (new ground — a second young daughter lost in the Karbala captivity, alongside Sakina). Six of the seven promote an existing citation-sheet woman-slot claim to a full entry and must be reconciled with that row once sourced. **Ruqayya needs the same category-before-wording scholar review as Khawla.**
- [x] Print the connection to the Fourteen on every envelope. Salman served the Prophet. Qambar served Imam Ali. Maytham died refusing to insult him. No selling language.
- [x] **Print templates for the whole line — 39 of 39**, generated by `tools/build_print_templates.py` rather than hand-built, so the gap cannot reopen when an entry is added.
- [ ] **Close the rest of the backlog before writing entry forty.** Citations verified for 0 of 39; scholar sign-off for 0 of 39; artwork for 0 of 39. See the gaps table in `08-companions/README.md`. Writing entries is the cheap activity and has outrun the expensive ones that gate print.
- [ ] Print, stock singly, and list as a checkout add-on, an Eid gift and a madrasa prize.

---

## Phase 9 — Noori's Notebook, ongoing

Events and places only. Never people — people live in envelopes, and one-person zines would sell the same six people twice.

- [x] Build the eight-page zine template: one A4 sheet, one cut, single ink. → `09-zines/README.md`, with the imposition and the eight page jobs.
- [x] Write the pilot zine, Ghadir Khumm, in full. → `09-zines/ghadir-khumm.md`
- [x] Write Hira in full. → `09-zines/hira.md`
- [x] Outline the remaining thirteen, page by page. → `09-zines/outlines.md`
- [x] Draft all fifteen zines to full text. → `09-zines/`, including Fadak (drafted 2026-08-12 on verbal scholar agreement — still needs full written sign-off before print, per its own production note).
- [ ] Publish on a schedule. Fifteen subjects in the bank: Ghadir Khumm, Mubahala, Hudaybiyya, the Trench, Hira, Jannat al-Baqi, Jamkaran, the road to Karbala, Kufa, Samarra, Fadak, Laylat al-Mabit, Dahw al-Ard, the Constitution of Medina, Bayt al-Hikma.
- [ ] Time each release against its date in the calendar where one exists.
- [ ] Feed Instagram from the zine pages. Hand out physical copies at majlis.

---

## Open decisions, to close before Phase 3

| Decision | Where it bites | Status |
|---|---|---|
| Swap envelopes 05 and 11? | Every downstream item is keyed to the month | **Still open.** Not a community-observance question, so "most publicly prominent in India" doesn't resolve it — provisionally kept as-is (no swap) for lack of a positive reason to change it. Revisit with real information on which Imam has the stronger anchor date. |
| Imam Hasan: 7th or 28th Safar | Envelope 02 stamp and letter | **Decided: 28 Safar** — the mainstream Twelver anchor, most widely observed in India, and the one commonly marked alongside the Prophet's death. This sets the *production* anchor (narrative emphasis, release timing); the printed fact panel still carries both dates with the standard differ line per `standard-lines.md` §1 — the rule against adjudicating what's printed is unchanged. |
| The Prophet: 12th or 17th Rabi al-Awwal | Envelope 03 stamp and letter | **Decided: 17 Rabi al-Awwal** — the Shia-observed date, publicly prominent in India (marked alongside Imam al-Sadiq's birth as Eid-e-Zahra). Same caveat: production anchor only, both dates still print with the differ line. |
| The Prophet's death: 28 Safar or 12 Rabi al-Awwal | Envelope 03 fact panel | **Decided: 28 Safar** — consistent with the Imam Hasan decision above; both mainstream Twelver anchors are commonly marked together. Differ line still applies in print. |
| Print run size | Phase 5 cost, Phase 6 commitment |
| Mid-year subscription start | Phase 6 fulfilment logic |
| What comes back on the return postcard | Phase 6 process |

## Standing risks

- **Envelope 06 blocks the box.** No scholar signature, no print run. Start that review early, not at Gate 3.
- **The fourteen are printed as one run.** A text error found after Phase 5 costs the whole run. That is why text freezes at Gate 3.
- **No subscription sells before Gate 5.** This is the only thing keeping monthly fulfilment safe.
- **Cash from annual billing pays for the print run** only if Phase 2 came back with real institutional numbers first.
