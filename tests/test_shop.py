#!/usr/bin/env python3
"""
Tests for the storefront.

    python -m unittest discover -s tests -v

A marketing page is where this project's own rules are most likely to break.
Every rule below is one the repo already states somewhere in 00-foundations/;
these turn them into something that fails a build rather than something someone
has to remember while writing copy.

The pages are built in memory, so these run without touching docs/.
"""

import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import build_shop
from build_site import ENVELOPES, COMPANIONS, ZINES


def text_of(html_str):
    """Visible text only — tags and their attributes stripped, so a test cannot
    be fooled by a word that only appears in a class name or a URL."""
    body = re.sub(r"(?is)<(script|style).*?</\1>", " ", html_str)
    body = re.sub(r"<[^>]+>", " ", body)
    import html as H
    return re.sub(r"\s+", " ", H.unescape(body))


class ShopTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.store, cls.products = build_shop.load_products()
        cls.copy = build_shop.Copy(build_shop.load_copy())
        cls.pages = {}
        for filename, title, fn, description in build_shop.PAGES:
            body = fn(cls.copy, cls.store, cls.products)
            cls.pages[filename] = build_shop.page(title, body, filename, cls.store,
                                                  description)
        cls.text = {k: text_of(v) for k, v in cls.pages.items()}
        cls.all_text = " ".join(cls.text.values())
        cls.all_html = " ".join(cls.pages.values())

    # -- 1. the banned lines -------------------------------------------

    def test_no_banned_phrase(self):
        """standard-lines.md §7, plus rule F2's superlatives. These are banned
        from the product; a shop page is not a lower standard."""
        banned = [
            "This teaches us that", "Like the Imam, we should",
            "Sadly,", "Tragically,", "Little did he know",
            "the greatest", "the most important", "the best ",
            "most famous", "most beloved", "most influential",
        ]
        for phrase in banned:
            self.assertNotIn(phrase.lower(), self.all_text.lower(),
                             "banned phrase on a shop page: %r" % phrase)

    def test_no_uncheckable_number(self):
        """sourcing-rules.md bans the *claim*, not the word: "no follower
        counts, no 'people influenced', no population figures, nothing that
        needs 'roughly' to survive". Saying on the About page that the project
        refuses such numbers is the rule being kept, not broken — so this looks
        for a quantity attached to one of them."""
        quantified = (
            r"\b[\d,]+\s*(?:million|billion|thousand)?\s*"
            r"(?:followers?|converts?|people|muslims|families)\b",
            r"\b(?:millions?|billions?|thousands?|hundreds?)\s+of\s+"
            r"(?:followers?|converts?|people|muslims|families)\b",
            r"people influenced",
            r"\broughly\s+[\d,]",
        )
        for pattern in quantified:
            self.assertIsNone(re.search(pattern, self.all_text, re.I),
                              "uncheckable claim on a shop page: %s" % pattern)

    def test_the_refusal_itself_is_allowed(self):
        """Guard against the test above being tightened into nonsense: the
        About page is supposed to say that these numbers are refused."""
        self.assertIn("No follower counts", self.text["about.html"])

    # -- 2. no quotation ------------------------------------------------

    def test_no_quotation_is_published(self):
        """Permission is unchecked for all six fixed editions, and the repo's
        own translations have unverified licences. Until that changes, no line
        is quoted and nothing is attributed in quote position."""
        for name, body in self.text.items():
            quoted = re.findall(r"[“”\"]([^“”\"]{12,})[“”\"]",
                                body)
            self.assertEqual(quoted, [], "%s carries a quotation: %r" % (name, quoted[:1]))
        self.assertNotIn(" said:", self.all_text)
        self.assertNotIn(" said,", self.all_text)

    # -- 3. no price, no live buy link ----------------------------------

    def test_no_price_is_rendered_while_price_is_null(self):
        for p in self.products:
            self.assertIsNone(p.get("price"),
                              "%s has a price — update this test deliberately, "
                              "not by accident" % p["sku"])
        # no currency symbol, and no bare money-shaped number
        for symbol in ("£", "$", "€", "₹"):
            self.assertNotIn(symbol, self.all_text, "a currency symbol reached a page")
        self.assertIsNone(re.search(r"\b\d+\.\d{2}\b", self.all_text),
                          "a money-shaped number reached a page")
        self.assertIn("Price not set", self.text["checkout.html"])

    def test_no_live_buy_link_while_provider_is_none(self):
        self.assertEqual((self.store.get("provider") or "none").lower(), "none")
        self.assertNotIn('class="btn buy"', self.all_html)
        for p in self.products:
            self.assertIsNone(p.get("buy_url"), p["sku"])
            self.assertIn(p.get("status"), ("waitlist", "not-yet"),
                          "%s is marked available before Gate 5" % p["sku"])

    def test_the_button_would_go_live_if_the_switch_flipped(self):
        """The scaffold has to actually work, or it is decoration."""
        wired = dict(self.store, provider="stripe")
        product = dict(self.products[0], status="available",
                       buy_url="https://buy.stripe.com/test")
        markup = build_shop.action(product, wired)
        self.assertIn("https://buy.stripe.com/test", markup)
        self.assertIn("Buy", markup)
        # and stays inert if only one half is set
        self.assertNotIn("href", build_shop.action(
            dict(product, buy_url=None), wired))
        self.assertNotIn("stripe", build_shop.action(product, self.store))

    # -- 4. the month claim ---------------------------------------------

    def test_the_month_claim_is_accurate(self):
        """Fourteen envelopes across twelve months — Rajab and Sha'ban each
        carry two. The review site's hero says "one for each month of the
        Islamic year", which is not true and must not be repeated here."""
        self.assertNotIn("one for each month of the islamic year",
                         self.all_text.lower())
        landing = self.text["index.html"]
        self.assertIn("twelve months", landing)
        self.assertIn("Rajab", landing)
        self.assertIn("Sha'ban", landing)

        months = [m for _, m, _, _ in ENVELOPES]
        self.assertEqual(len(ENVELOPES), 14)
        self.assertEqual(len(set(months)), 12)

    # -- 5. counts come from the catalogue, not from typing --------------

    def test_counts_match_the_live_catalogue(self):
        landing = self.pages["index.html"]
        self.assertEqual(landing.count('class="tile"'), len(ENVELOPES))
        self.assertEqual(landing.count('class="chip"'), len(COMPANIONS) + len(ZINES))
        for _, name in COMPANIONS:
            self.assertIn(name, self.text["index.html"], "%s missing" % name)
        for _, name in ZINES:
            self.assertIn(name, self.text["index.html"], "%s missing" % name)

    # -- 6. honorifics ---------------------------------------------------

    def test_every_masoom_carries_the_honorific(self):
        """standard-lines.md §3. The catalogue grid names all fourteen, so all
        fourteen carry the full form."""
        landing = self.pages["index.html"]
        for _, _, masoom, _ in ENVELOPES:
            name = build_shop.full_form(masoom)
            hon = build_shop.honorific(masoom)
            self.assertIn(name, landing, "%s missing from the grid" % name)
            self.assertIn(
                '<span class="tilename">%s</span>\n<span class="tilehon">%s</span>'
                % (name, hon), landing,
                "%s is named without its honorific" % name)

    def test_the_honorific_matches_the_standard_lines(self):
        self.assertEqual(build_shop.honorific("Imam Ali"), "peace be upon him")
        self.assertEqual(build_shop.honorific("Sayyida Fatima"), "peace be upon her")
        self.assertEqual(build_shop.honorific("The Prophet Muhammad"),
                         "peace be upon him and his family")
        self.assertEqual(build_shop.full_form("Sayyida Fatima"),
                         "Sayyida Fatima al-Zahra")

    # -- 7. noindex while unpublished ------------------------------------

    def test_noindex_while_unpublished(self):
        self.assertFalse(self.store.get("published"))
        for name, body in self.pages.items():
            self.assertIn('<meta name="robots" content="noindex">', body, name)

    def test_publishing_removes_noindex(self):
        published = dict(self.store, published=True)
        body = build_shop.page("t", "<p>x</p>", "index.html", published, "d")
        self.assertNotIn("noindex", body)

    # -- 8. no internal references leak ----------------------------------

    def test_no_internal_reference_leaks(self):
        for name, body in self.text.items():
            self.assertIsNone(re.search(r"\b[\w-]+\.md\b", body),
                              "%s leaks an internal file reference" % name)
            for token in ("TASKS.md", "citation-sheet", "TO VERIFY", "TV row",
                          "Gate 5", "Gate 6", "PRD"):
                self.assertNotIn(token, body, "%s leaks %r" % (name, token))

    # -- 9. no unverified biographical claim -----------------------------

    def test_no_biographical_claim(self):
        """Every fact about the Fourteen is still marked TV, and nothing prints
        on TV. The shop may describe the product and the method; it may not
        assert a date, an age, a length of imamate or an event."""
        for pattern in (r"\b\d+\s*AH\b", r"\bborn in\b", r"\bdied in\b",
                        r"\bwas killed\b", r"\bmartyred\b", r"\bcaliph\b",
                        r"\bimamate\b", r"\bat the age of\b"):
            self.assertIsNone(re.search(pattern, self.all_text, re.I),
                              "an unverified biographical claim shape reached a "
                              "shop page: %s" % pattern)

    # -- structure -------------------------------------------------------

    def test_three_pages_and_no_more(self):
        self.assertEqual(sorted(self.pages), ["about.html", "checkout.html", "index.html"])

    def test_every_page_is_self_contained(self):
        for name, body in self.pages.items():
            self.assertIn('<link rel="stylesheet" href="shop.css">', body, name)
            self.assertIn("<title>", body, name)
            self.assertIn('name="description"', body, name)
            self.assertNotIn("draft for review", body,
                             "%s inherited the review site's footer" % name)

    def test_the_waitlist_never_posts_nowhere(self):
        wl = self.store.get("waitlist") or {}
        if not wl.get("endpoint"):
            self.assertNotIn("<form", self.pages["checkout.html"],
                             "a form is rendered with no endpoint to post to")
        # and the invitation is not shown when there is nowhere to leave an address
        if not (wl.get("endpoint") or wl.get("email")):
            self.assertNotIn("leave an address", self.text["checkout.html"].lower())

    def test_legal_placeholder_while_details_are_missing(self):
        legal = self.store.get("legal") or {}
        if not (legal.get("entity") and legal.get("contact")):
            self.assertIn("not set up yet", self.text["checkout.html"])

    def test_copy_sections_are_all_used(self):
        """A section written in copy.md and silently not rendered is a blank
        space on a customer-facing page."""
        self.assertEqual(self.copy.unused(), [])

    def test_proof_images_exist(self):
        for filename, _ in build_shop.PROOFS:
            path = os.path.join(ROOT, "docs", "print-proofs", "png", filename)
            self.assertTrue(os.path.exists(path), "missing proof image: %s" % filename)
        self.assertIn("not finished artwork", self.text["index.html"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
