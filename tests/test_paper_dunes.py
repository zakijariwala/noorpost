#!/usr/bin/env python3
"""
Tests for the Paper Dunes envelope set.

    python -m unittest discover -s tests -v

The sheets are built in memory. Each test is a rule from 00-foundations/ that
the set could break without anyone noticing on a screenshot.
"""

import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import build_paper_dunes as P

TEXT = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


class PaperDunes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.e03 = P.build_03()
        cls.e01 = P.build_01()

    def test_on_disk_is_current(self):
        for name, built in (("envelope-03.html", self.e03), ("envelope-01.html", self.e01)):
            with open(os.path.join(P.OUT, name), encoding="utf-8") as f:
                self.assertEqual(f.read(), built, f"{name} is stale — run tools/build_paper_dunes.py")

    def test_every_item_is_present(self):
        sizes = re.findall(r'class="page (p-[a-z0-9]+)', self.e03)
        self.assertEqual(sizes, ["p-env", "p-env", "p-flap", "p-spread", "p-spread",
                                 "p-a6p", "p-a6p", "p-a6p", "p-a6p",
                                 "p-a5p", "p-a5l", "p-a6p", "p-a6l", "p-a6l"])

    def test_letter_text_is_the_source_text_in_full(self):
        src = open(os.path.join(P.PILOT, "letter.md"), encoding="utf-8").read()
        body = src.split("LETTER START")[1].split("LETTER END")[0]
        page = TEXT(self.e03)
        for line in body.split("\n"):
            s = line.strip().lstrip("●○").strip()
            if s and s != "---" and "-->" not in s and "<!--" not in s:
                self.assertIn(TEXT(P.inline(s)).strip(), page)

    def test_no_envelope_number_on_any_hadith_card(self):
        for sheet in (self.e03, self.e01):
            for card in re.findall(r'<div class="page p-a6p card-front.*?</blockquote>.*?</div>', sheet, re.S):
                self.assertNotRegex(TEXT(card), r"(?i)\benvelope\b|\b0\d\b")

    def test_undecided_segment_is_not_printed(self):
        self.assertIn("Silsila segment <span class=\"undecided\">––</span> of 14", self.e03)
        self.assertIn("Silsila segment 3 of 14", self.e01)

    def test_fact_panel_carries_to_verify(self):
        self.assertIn("UNVERIFIED — TO VERIFY", self.e03)

    def test_mourning_issue_has_no_colour(self):
        pages = re.findall(r'<div class="page [^"]*">', self.e01)
        self.assertTrue(pages)
        for p in pages:
            self.assertIn("mourning", p)
        palette = ("#FFF6EA", "#FCEBD5", "#F9D9B4", "#F6B48A", "#E58F7B",
                   "#1F5C63", "#5B3A63", "#3B2440", "#3E8E6E", "#2C7179")
        for hexv in palette:
            self.assertNotIn(hexv.lower(), self.e01.lower(), f"{hexv} on a mourning page")

    def test_mourning_issue_carries_pennant_not_stickers(self):
        self.assertIn("pennant", self.e01)
        self.assertNotIn("stickers no-band", self.e01)
        self.assertIn("This one has no game in it.", self.e01)


if __name__ == "__main__":
    unittest.main()
