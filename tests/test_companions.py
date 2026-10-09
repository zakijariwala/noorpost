#!/usr/bin/env python3
"""
Tests for the companions line — Everyone Else.

    python -m unittest discover -s tests -v

Each built companion is rebuilt in memory. One style for the line; what must
hold for every envelope in it is checked here. Layout (nothing clipped) is
checked in the browser by tools/render_companions.js, which refuses to write
a PDF that overflows.
"""

import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import build_companions as B
import companion_sources as S
from companion_themes import BUILT, PEOPLE

TEXT = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


class Companions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.built = {s: B.build(s) for s in BUILT}
        cls.data = {s: S.load(s) for s in BUILT}

    def test_built_in_card_order(self):
        """Batches go in card order, so the set grows from 01/39 without gaps."""
        self.assertEqual(BUILT, S.ALL[:len(BUILT)])

    def test_on_disk_is_current(self):
        for s, html in self.built.items():
            with open(os.path.join(B.OUT, f"companion-{s}.html"), encoding="utf-8") as f:
                self.assertEqual(f.read(), html, f"companion-{s}.html is stale — run tools/build_companions.py")

    def test_five_items_and_never_an_event_print(self):
        for s, html in self.built.items():
            pages = re.findall(r'class="page (p-[a-z0-9]+)', html)
            for size, n in (("p-env", 2), ("p-flap", 1), ("p-spread", 2), ("p-a6p", 3), ("p-a5p", 1), ("p-a6l", 2)):
                self.assertEqual(pages.count(size), n, f"{s}: {size}")
            self.assertNotIn("p-a5l", pages, f"{s}: an event print — never in this line")
            self.assertNotIn('data-item="event"', html, s)
            self.assertNotIn('data-item="session"', html, s)

    def test_letter_is_the_source_text_in_full(self):
        for s, html in self.built.items():
            page = TEXT(html)
            for v in self.data[s]["voices"]:
                line = TEXT(re.sub(r'<span class="mark">.*?</span>', "", v)).strip()
                self.assertIn(line, page, f"{s}: letter line missing")

    def test_card_is_on_its_own_chain(self):
        for s, html in self.built.items():
            n = self.data[s]["n"]
            self.assertIn(f"First edition · {n:02d}/39", html, s)
            self.assertNotRegex(TEXT(html), r"(?i)segment\s+(\d|––)", f"{s}: a silsila segment number")

    def test_saying_is_quoted_exactly_or_the_slot_is_empty(self):
        for s, html in self.built.items():
            say = self.data[s]["saying"]
            card = re.search(r'<div class="page p-a6p card-front.*?(?=<p class="cap)', html, re.S).group(0)
            if say.get("text"):
                self.assertIn("&ldquo;" + B.E(say["text"]) + "&rdquo;", card, s)
            else:
                self.assertNotIn("&ldquo;", card, s)
                self.assertIn("No saying selected", card, s)

    def test_every_card_with_a_saying_has_a_gloss(self):
        for s in BUILT:
            if self.data[s]["saying"].get("text"):
                self.assertIn(s, B.GLOSSES, f"{s}: no 'In our words' line in hadith-glosses.json")

    def test_points_home_on_the_front(self):
        for s, html in self.built.items():
            front = re.search(r'data-item="front".*?(?=<p class="cap)', html, re.S).group(0)
            self.assertIn(B.E(self.data[s]["points"]), front, s)

    def test_last_line_is_said_together_on_face_three(self):
        for s, html in self.built.items():
            self.assertIn('class="together-big"', html, s)

    def test_fact_panel_carries_to_verify(self):
        for s, html in self.built.items():
            self.assertIn("UNVERIFIED — TO VERIFY", html, s)

    def test_every_built_companion_has_a_style(self):
        for s in BUILT:
            for k in ("colour", "colour2", "tint", "art", "figure", "backdrop", "postcard", "hero", "stickers"):
                self.assertIn(k, PEOPLE[s], f"{s}: {k}")


if __name__ == "__main__":
    unittest.main()
