#!/usr/bin/env python3
"""
Tests for the fourteen envelopes, fourteen styles.

    python -m unittest discover -s tests -v

Each envelope is built in memory. The styles may differ in everything except
the rules below — these are what must hold whatever an envelope looks like.
Layout (nothing clipped) is checked in the browser by
tools/render_envelopes.js, which refuses to write a PDF that overflows.
"""

import os
import re
import sys
import unittest
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import build_envelopes as B
import envelope_sources as S
from envelope_themes import THEMES

TEXT = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


class Envelopes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.built = {nn: B.build(nn) for nn in S.ALL}
        cls.data = {nn: S.load(nn) for nn in S.ALL}

    def test_fourteen_envelopes_fourteen_styles(self):
        keys = [THEMES[nn]["key"] for nn in S.ALL]
        self.assertEqual(len(set(keys)), 14, keys)

    def test_on_disk_is_current(self):
        for nn, html in self.built.items():
            with open(os.path.join(B.OUT, f"envelope-{nn}.html"), encoding="utf-8") as f:
                self.assertEqual(f.read(), html, f"envelope-{nn}.html is stale — run tools/build_envelopes.py")

    def test_every_item_is_present(self):
        for nn, html in self.built.items():
            pages = re.findall(r'class="page (p-[a-z0-9]+)', html)
            for size, n in (("p-env", 2), ("p-flap", 1), ("p-spread", 2), ("p-a5l", 1), ("p-a6l", 2)):
                self.assertEqual(pages.count(size), n, f"{nn}: {size}")
            kind = self.data[nn]["session"]["kind"]
            self.assertEqual(pages.count("p-a7p"), 5 if kind == "case" else 0, f"{nn}: evidence cards")
            # card front + back, session pages (mourning: one side), and stickers unless mourning
            a6 = 2 + {"case": 3, "mourning": 1}.get(kind, 2) + (0 if self.data[nn]["mourning"] else 1)
            self.assertEqual(pages.count("p-a6p"), a6, f"{nn}: A6 items")
            # person print, plus the pennant in a mourning issue
            self.assertEqual(pages.count("p-a5p"), 2 if self.data[nn]["mourning"] else 1, f"{nn}: A5 portrait")

    def test_letter_is_the_source_text_in_full(self):
        for nn, html in self.built.items():
            page = TEXT(html)
            for v in self.data[nn]["voices"]:
                line = TEXT(re.sub(r'<span class="mark">.*?</span>', "", v)).strip()
                self.assertIn(line, page, f"{nn}: letter line missing")

    def test_every_session_line_in_source_reaches_the_card(self):
        """The Q1 bug: a question sharing a block with the card title was dropped."""
        for nn in S.ALL:
            src = (open(os.path.join(S.PILOT, "session-card.md"), encoding="utf-8").read() if nn == "03"
                   else open(os.path.join(S.CONTENT, f"envelope-{nn}.md"), encoding="utf-8").read())
            labels = re.findall(r"^> \*\*(\d+|Last)[.:]\*\*", src, re.M)
            kind = self.data[nn]["session"]["kind"]
            if kind == "conversation":
                self.assertEqual([q[0] for q in self.data[nn]["session"]["questions"]], labels, nn)
            if kind in ("mourning", "open"):
                page = TEXT(self.built[nn])
                body = src.split("## Session card")[1].split("\n## ")[0]
                for ln in body.split("\n"):
                    t = ln.lstrip(">").strip()
                    if t and t != "---" and not t.startswith("#") and ln.startswith(">"):
                        self.assertIn(TEXT(S.inline(t)).strip(), page, f"{nn}: {t[:40]}")

    def test_last_line_is_said_together_on_face_three(self):
        for nn, html in self.built.items():
            self.assertIn('class="together-big"', html)

    def test_no_envelope_number_on_any_hadith_card(self):
        for nn, html in self.built.items():
            cards = re.findall(r'<div class="page p-a6p card-front.*?</div>(?=<p class="cap)', html, re.S)
            back = re.search(r'<div class="card-back">.*?</div></div>', html, re.S).group(0)
            self.assertEqual(len(cards), 1, nn)
            for c in cards + [back]:
                self.assertNotRegex(TEXT(c), r"(?i)\benvelope\b|\b0\d\b", nn)

    def test_segment_prints_only_when_decided(self):
        for nn, html in self.built.items():
            s = self.data[nn]["saying"]
            if s.get("segment_conflict") or not s.get("segment"):
                self.assertIn('Silsila segment <span class="undecided">––</span> of 14', html, nn)
            else:
                self.assertIn(f"Silsila segment {s['segment']} of 14", html, nn)

    def test_blocked_saying_is_never_filled(self):
        for nn, html in self.built.items():
            if self.data[nn]["saying"].get("text"):
                continue
            card = re.search(r'<div class="page p-a6p card-front.*?(?=<p class="cap)', html, re.S).group(0)
            self.assertNotIn("&ldquo;", card, nn)
            self.assertIn("No saying selected", card, nn)

    def test_mourning_issues_are_two_inks_on_ivory(self):
        """01 black and red, 02 black and green, on ivory — nothing else, art included."""
        second = {"01": ("#9e1b1e", "158,27,30"), "02": ("#1f6b45", "31,107,69")}
        for nn, (hexc, rgb) in second.items():
            allowed = {"#1b1b1b", "#f3ede1", hexc}
            html = unquote(self.built[nn]).lower()
            for hexv in set(re.findall(r"#[0-9a-f]{6}\b", html)):
                self.assertIn(hexv, allowed, f"{nn}: {hexv} on a mourning page")
            for rgba in set(re.findall(r"rgba?\(([^)]*)\)", html)):
                v = rgba.replace(" ", "")
                self.assertTrue(v.startswith("27,27,27") or v.startswith(rgb), f"{nn}: rgba({rgba})")

    def test_mourning_issues_carry_a_pennant_and_no_stickers(self):
        for nn in ("01", "02"):
            html = self.built[nn]
            self.assertIn("Pennant", html)
            self.assertIn("This one has no game in it.", html)
            self.assertNotIn('id="kiss"', html)

    def test_fact_panel_carries_to_verify(self):
        for nn, html in self.built.items():
            self.assertIn("UNVERIFIED — TO VERIFY", html, nn)


if __name__ == "__main__":
    unittest.main()
