# Phase 6 — Commerce

The storefront, and the data behind it. `TASKS.md` Phase 6 is the checklist;
this folder is where its text deliverables live.

| File | What it is |
|---|---|
| `products.yaml` | The five SKUs, and the switches: published, payment provider, waitlist endpoint, legal details. Hand-edited. |
| `copy.md` | The prose for all three shop pages. Hand-edited. |

Built by `python tools/build_shop.py` — or by `python tools/build_site.py`,
which builds it along with everything else — into:

    docs/shop/index.html      the landing page, all products
    docs/shop/about.html      what this is, how it is made, what it refuses
    docs/shop/checkout.html   the waitlist and the five SKUs

`docs/shop/shop.css` is hand-maintained, like `docs/style.css`. The generator
writes the HTML and nothing else.

The catalogue — fourteen envelopes, thirty-nine companions, fifteen zines — is
imported from `tools/build_site.py`, never retyped here, so the shop cannot list
something the content does not have.

---

## Four rules this folder holds

**1. No price is invented.** There is no price anywhere in this repository, and
there cannot be one until Phase 2 comes back with a number a madrasa
administrator actually named (`TASKS.md` 82–87). Every SKU carries
`price: null`, the pages render "Price not set", and a test fails if a currency
figure appears.

**2. Nothing sells before Gate 5.** Fourteen printed envelopes in the cupboard
first (`TASKS.md` 186). Until then every SKU is `waitlist` or `not-yet`, and the
buy button is inert whatever else is configured.

**3. No quotation, and no claim about any of the Fourteen.** Permission is
unchecked for all six fixed editions, and every factual claim in the project is
still marked `TV`. The storefront describes the *product* and the *method* —
fourteen envelopes, seven items, twenty-five minutes, Shia sources only, named
translator — and asserts nothing biographical. Tested.

**4. The payment provider is a switch, not a rewrite.** `provider: none` and
`buy_url: null` today. Fill both in, set a SKU to `available`, rebuild — the same
button becomes a real link. No markup changes.

---

## Placeholder mode

`storefront.placeholders: true` fills every empty slot — price, seller, contact,
privacy, terms, shipping, delivery, returns, the waitlist form and the missing
artwork — with a **marked** placeholder, so the three pages can be reviewed
complete rather than full of holes.

Two things make this safe rather than a way of lying to yourself:

**The real values stay `null`.** A placeholder is never written into the data. A
made-up price sitting in a YAML file is indistinguishable from a decision six
weeks later; a placeholder rendered from a separate block is not. Set a real
price and its placeholder disappears on the next build.

**Every placeholder is visibly one.** It renders inside `<span class="ph">`,
dashed and in terracotta, with a banner at the top of every page saying so. The
placeholder price is `£00.00` on purpose — `£24.99` would read as a decision.
`tests/test_shop.py` strips the marked spans and fails if any currency symbol,
money-shaped number or bracket placeholder is left loose on the page.

Set `placeholders: false` and the pages go back to stating plainly what is
missing. Both modes are tested.

**Do not publish while this is true.**

## Turning things on

| To do this | Set |
|---|---|
| Open the waitlist with a form | `storefront.waitlist.endpoint` — a Formspree/Buttondown/Google Form action URL |
| Open the waitlist with an email link instead | `storefront.waitlist.email` |
| Show seller details instead of the placeholder | `storefront.legal.entity` **and** `.contact` |
| Stop showing placeholders | `storefront.placeholders: false` |
| Let search engines index it | `storefront.published: true` — removes `noindex` from all three pages. Not while `placeholders` is true. |
| Actually sell something | `storefront.provider`, then per-SKU `buy_url`, `price`, and `status: available` |

The waitlist has no third-party dependency until you give it one: with no
endpoint and no email it renders a plain statement that the list is not open,
which is the honest state today.

---

## What is missing before this can go live

Not code — none of it is solved by building pages.

- **A price.** Phase 2, and it comes from the channel, not from a spreadsheet.
- **A legal entity, a contact address, a privacy notice, terms, returns.** None
  exists in this repo. An address cannot be collected without at least the first
  three. The pages say so rather than inventing them.
- **The packs** for the thirty-nine companions (`TASKS.md` 251) — so Everyone
  Else is presented as singles only.
- **Gate 6:** "test with one real order before announcing anything."
- And upstream of all of it, the print run, which is still blocked on the
  scholar signature for envelope 06.
