#!/usr/bin/env python3
"""
Build the storefront — three pages — into docs/shop/.

    python tools/build_shop.py          # write the three pages
    python tools/build_shop.py --check  # report what would be written, write nothing

    landing   docs/shop/index.html
    about     docs/shop/about.html
    checkout  docs/shop/checkout.html

This is a different thing from the site tools/build_site.py builds. That one is
an internal review site: every page carries noindex and a "draft for review, not
for circulation" footer, and it exists so the editorial work can be read. This
one is customer-facing. It shares the catalogue but not the shell.

Two files feed it, both hand-edited:

    06-commerce/products.yaml   the five SKUs, and the switches
    06-commerce/copy.md         the prose

and the catalogue itself is imported from build_site, never retyped, so the
storefront cannot drift from the content it is selling.

What this generator will not do, because tests/test_shop.py checks that it
does not:

  * print a price. There is no price in this repository, and inventing one on a
    shop page is the worst place to invent anything.
  * quote a saying. Permission is unchecked for all six fixed editions.
  * assert a fact about any of the Fourteen. Every one is still marked TV.
  * render a live buy link while the payment provider is `none`.
"""

import argparse
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_site import ENVELOPES, COMPANIONS, ZINES, blocks, inline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "shop")
COMMERCE = os.path.join(ROOT, "06-commerce")
PRODUCTS = os.path.join(COMMERCE, "products.yaml")
COPY = os.path.join(COMMERCE, "copy.md")

# The print proofs are the only images that exist. They are typeset renders of
# one envelope, and the page says so rather than passing them off as product
# photography.
PROOFS = [
    ("envelope-03-letter.png", "The letter, front"),
    ("envelope-03-fact-panel.png", "The fact panel, on the letter's reverse"),
    ("envelope-03-hadith-card.png", "The hadith card"),
    ("envelope-03-session-card.png", "The session card"),
    ("envelope-03-postcard.png", "The return postcard"),
    ("envelope-03-flap.png", "Inside the flap"),
]

# The seven items, from design-system.md §4. Sizes are the product spec and are
# checkable facts about the object, not claims about anybody.
ITEMS = [
    ("The letter", "A5, two voices, with the fact panel on its reverse"),
    ("The hadith card", "A6, sized for a child's Qur'an"),
    ("The person print", "A5 portrait, for a wall"),
    ("The event print", "A5 landscape, punched for the ring"),
    ("The session card", "A6 — a conversation, a case file, or a mourning session"),
    ("The sticker sheet", "A6, die-cut"),
    ("The return postcard", "A6, pre-addressed, to send back"),
]


# --------------------------------------------------------------------------
# names
# --------------------------------------------------------------------------

# standard-lines.md §3: full form on first mention, short form thereafter.
# The table there gives six and then "Imam al-Baqir, and so on | As above", so
# the pattern generalises; only the names whose full form differs from the
# catalogue spelling need an entry here.
FULL_NAME = {
    "Sayyida Fatima": "Sayyida Fatima al-Zahra",
}


def honorific(name):
    if name.startswith("Sayyida") or name.startswith("Lady"):
        return "peace be upon her"
    if "Prophet" in name:
        return "peace be upon him and his family"
    return "peace be upon him"


def full_form(name):
    return FULL_NAME.get(name, name)


# --------------------------------------------------------------------------
# inputs
# --------------------------------------------------------------------------

def load_products():
    try:
        import yaml
    except ImportError:                                       # pragma: no cover
        raise SystemExit("PyYAML is needed to read 06-commerce/products.yaml — "
                         "pip install -r requirements.txt")
    with open(PRODUCTS, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    return doc.get("storefront", {}) or {}, doc.get("products", []) or []


def load_copy():
    """`## key` headings -> the lines under them."""
    sections, key = {}, None
    with open(COPY, encoding="utf-8") as f:
        for line in f.read().split("\n"):
            m = re.match(r"^## (\S+)\s*$", line)
            if m:
                key = m.group(1)
                sections[key] = []
                continue
            if line.startswith("# "):
                key = None
                continue
            if key is not None:
                sections[key].append(line)
    return sections


class Copy:
    """Section lookup that fails loudly. A silently missing block of prose is a
    blank space on a customer-facing page."""

    def __init__(self, sections):
        self.sections = sections
        self.used = set()

    def __call__(self, key, required=True):
        if key not in self.sections:
            if required:
                raise SystemExit("06-commerce/copy.md has no section '## %s'" % key)
            return ""
        self.used.add(key)
        return "\n".join(blocks(self.sections[key]))

    def unused(self):
        return sorted(set(self.sections) - self.used)


# --------------------------------------------------------------------------
# the page shell
# --------------------------------------------------------------------------

NAV = [("index.html", "The series"), ("about.html", "About"), ("checkout.html", "Get it")]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=EB+Garamond:ital,wght@0,400;0,600;1,400&'
         'family=Fraunces:opsz,wght@9..144,400;9..144,700&display=swap">')


def page(title, body, current, store, description):
    # Until storefront.published is true this stays out of search results.
    # Gate 6: test with one real order before announcing anything.
    robots = "" if store.get("published") else '<meta name="robots" content="noindex">\n'
    nav = "\n".join(
        '    <a%s href="%s">%s</a>' % (' class="here"' if h == current else "", h, label)
        for h, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
{FONTS}
<link rel="stylesheet" href="shop.css">
</head>
<body>
<header class="top">
  <a class="wordmark" href="index.html">Noor&nbsp;Post</a>
  <nav>
{nav}
  </nav>
</header>
<main>
{body}
</main>
<footer>
  <p>Noor Post — a printed series for Shia families.</p>
  <p class="fine">Nothing on this page is for sale yet.</p>
</footer>
</body>
</html>
"""


# --------------------------------------------------------------------------
# shared blocks
# --------------------------------------------------------------------------

def price_line(product):
    """No price exists in this project. Say that, rather than showing a number
    that would have to be invented, or an empty space that reads as free."""
    if product.get("price") is None:
        return '<p class="price none">Price not set</p>'
    return '<p class="price">%s</p>' % html.escape(str(product["price"]))


def action(product, store, on_checkout=False):
    """The one place a buy button is decided. While provider is `none` nothing
    here becomes a link that takes money."""
    status = product.get("status")
    provider = (store.get("provider") or "none").lower()
    buy_url = product.get("buy_url")

    if status == "available" and provider != "none" and buy_url:
        return ('<a class="btn buy" href="%s">Buy</a>' % html.escape(buy_url))
    if status == "waitlist":
        href = "#waitlist" if on_checkout else "checkout.html#waitlist"
        return '<a class="btn" href="%s">Join the waitlist</a>' % href
    return '<span class="btn disabled" aria-disabled="true">Not yet available</span>'


def product_card(product, store, on_checkout=False):
    items = "".join("<li>%s</li>" % inline(i) for i in product.get("items", []) or [])
    region = product.get("region")
    return f"""<article class="product">
  <h3>{inline(product.get('name', ''))}{'<span class="region">' + inline(region) + '</span>' if region else ''}</h3>
  <p class="blurb">{inline((product.get('blurb') or '').strip())}</p>
  <ul class="items">{items}</ul>
  <p class="note">{inline((product.get('contents_note') or '').strip())}</p>
  {price_line(product)}
  <p class="avail">{inline((product.get('availability_note') or '').strip())}</p>
  {action(product, store, on_checkout)}
</article>"""


# --------------------------------------------------------------------------
# the three pages
# --------------------------------------------------------------------------

def landing(copy, store, products):
    env_tiles = "".join(
        f"""<div class="tile">
<span class="tilenum">{num}</span>
<span class="tilemonth">{html.escape(month)}</span>
<span class="tilename">{html.escape(full_form(masoom))}</span>
<span class="tilehon">{html.escape(honorific(masoom))}</span>
<span class="tilesession">{html.escape(session)}</span>
</div>"""
        for num, month, masoom, session in ENVELOPES)

    comp_tiles = "".join(
        '<span class="chip">%s</span>' % html.escape(name) for _, name in COMPANIONS)
    zine_tiles = "".join(
        '<span class="chip">%s</span>' % html.escape(name) for _, name in ZINES)

    items = "".join(
        f'<li><strong>{html.escape(n)}</strong><span>{html.escape(d)}</span></li>'
        for n, d in ITEMS)

    proofs = "".join(
        f"""<figure>
<img src="../print-proofs/png/{f}" alt="{html.escape(cap)}" loading="lazy">
<figcaption>{html.escape(cap)}</figcaption>
</figure>""" for f, cap in PROOFS)

    return f"""<section class="hero">
<h1>Noor Post</h1>
<div class="lede">{copy('landing.lede')}</div>
<div class="lede small">{copy('landing.sub')}</div>
<p class="heroactions"><a class="btn" href="checkout.html#waitlist">Join the waitlist</a>
<a class="btn ghost" href="about.html">What this is</a></p>
</section>

<section>
<h2>What arrives</h2>
{copy('landing.what-it-is')}
</section>

<section>
<h2>The first edition</h2>
{copy('landing.first-edition')}
</section>

<section id="the-fourteen">
<h2>The Fourteen</h2>
<p class="sectionnote">In calendar order, as they arrive.</p>
<div class="grid">{env_tiles}</div>
</section>

<section>
<h2>Inside one envelope</h2>
{copy('landing.envelope')}
<ul class="itemlist">{items}</ul>
<div class="aside">{copy('landing.envelope-note')}</div>
{copy('landing.collections')}
</section>

<section id="everyone-else">
<h2>Everyone Else</h2>
<p class="sectionnote">Thirty-nine single envelopes, one per person, dateless.
Five items, no event print, bought one at a time.</p>
<div class="chips">{comp_tiles}</div>
</section>

<section id="notebook">
<h2>Noori's Notebook</h2>
<p class="sectionnote">One sheet, folded to eight pages, about a place or an event.</p>
<div class="chips">{zine_tiles}</div>
</section>

<section>
<h2>How it is sourced</h2>
{copy('landing.sourcing')}
</section>

<section>
<h2>What it looks like</h2>
<div class="proofs">{proofs}</div>
<p class="sectionnote">{copy('landing.proofs')}</p>
</section>

<section>
<h2>When you can get it</h2>
{copy('landing.availability')}
<p class="heroactions"><a class="btn" href="checkout.html#waitlist">Join the waitlist</a></p>
</section>"""


def about(copy, store, products):
    return f"""<section class="hero">
<h1>About</h1>
<div class="lede">{copy('about.what')}</div>
</section>

<section><h2>Who it is for</h2>{copy('about.who')}</section>
<section><h2>How it works</h2>{copy('about.method')}</section>
<section><h2>Sources</h2>{copy('about.sourcing')}</section>
<section><h2>What it refuses to do</h2>{copy('about.refuses')}</section>
<section><h2>Where this actually is</h2>{copy('about.status')}</section>"""


def waitlist_block(copy, store):
    """A form when an endpoint exists; a mailto: when only an address does; a
    plain statement when neither.

    Never a form that posts nowhere, and never an invitation to leave an address
    when there is nowhere to leave it — the invitation is rendered here, beside
    the thing it invites you to use, so the two cannot contradict each other.
    """
    wl = store.get("waitlist") or {}
    endpoint, email = wl.get("endpoint"), wl.get("email")
    invite = copy("checkout.invite", required=False)

    if endpoint:
        return f"""{invite}
<form class="waitlist" method="POST" action="{html.escape(endpoint)}">
  <label for="email">Email address</label>
  <input id="email" type="email" name="email" required
         placeholder="you@example.com" autocomplete="email">
  <button type="submit">Tell me when it is ready</button>
</form>"""
    if email:
        return ('%s\n<p class="heroactions"><a class="btn" href="mailto:%s'
                '?subject=Noor%%20Post%%20waitlist">Email to join the waitlist</a></p>'
                % (invite, html.escape(email)))
    return '<div class="aside">%s</div>' % copy('checkout.no-legal')


def legal_block(store):
    legal = store.get("legal") or {}
    if legal.get("entity") and legal.get("contact"):
        bits = ["Sold by %s. Contact: %s."
                % (inline(legal["entity"]), inline(legal["contact"]))]
        for label, key in (("Privacy", "privacy_url"), ("Terms", "terms_url")):
            if legal.get(key):
                bits.append('<a href="%s">%s</a>' % (html.escape(legal[key]), label))
        return '<p class="fine">%s</p>' % " ".join(bits)
    return ('<p class="fine placeholder">Seller details, privacy notice and terms '
            'are not set up yet. They have to exist before any address is '
            'collected or anything is sold.</p>')


def checkout(copy, store, products):
    cards = "".join(product_card(p, store, on_checkout=True) for p in products)
    return f"""<section class="hero">
<h1>Get it</h1>
<div class="lede">{copy('checkout.intro')}</div>
</section>

<section id="waitlist">
<h2>The waitlist</h2>
{copy('checkout.next')}
{waitlist_block(copy, store)}
</section>

<section>
<h2>What there will be</h2>
<p class="sectionnote">Five things, none of them priced yet.</p>
<div class="products">{cards}</div>
</section>

<section>
<h2>The small print</h2>
{legal_block(store)}
</section>"""


PAGES = [
    ("index.html", "Noor Post — a printed series for Shia families", landing,
     "Fourteen sealed envelopes for the Fourteen Masoomeen, opened by a parent and "
     "child together. About twenty-five minutes."),
    ("about.html", "About — Noor Post", about,
     "How Noor Post is written and sourced, and what it refuses to do."),
    ("checkout.html", "Get it — Noor Post", checkout,
     "Nothing is for sale yet. Join the waitlist to hear when it is."),
]


def build(check=False):
    store, products = load_products()
    copy = Copy(load_copy())

    written = []
    for filename, title, fn, description in PAGES:
        body = fn(copy, store, products)
        out = page(title, body, filename, store, description)
        if not check:
            os.makedirs(OUT, exist_ok=True)
            with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
                f.write(out)
        written.append(filename)

    unused = copy.unused()
    if unused:
        print("  copy.md sections not used by any page: %s" % ", ".join(unused))

    priced = [p["sku"] for p in products if p.get("price") is not None]
    live = [p["sku"] for p in products
            if p.get("status") == "available" and p.get("buy_url")]
    print("  shop: %d pages, %d SKUs — %s, provider %s, %s"
          % (len(written), len(products),
             "no prices set" if not priced else "%d priced" % len(priced),
             store.get("provider") or "none",
             "published" if store.get("published") else "noindex"))
    if live and (store.get("provider") or "none") == "none":
        print("  note: %d SKU(s) marked available with a buy_url, but provider is "
              "none — the buttons stay inert" % len(live))
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="build in memory, write nothing")
    args = ap.parse_args()
    build(check=args.check)
    return 0


if __name__ == "__main__":
    sys.exit(main())
