"""The illustration kit for all fourteen envelopes.

One kit of shapes — dunes, palms, shrines, a road, a door, a barred window,
the Kaaba, a cave, a pool — drawn by a Pen whose *mode* is the envelope's
style: cut paper, flat graphic, charcoal line, ink wash, stitched, riso,
gilded. Fourteen styles, one set of drawings to check.

The rule in design-system.md §3 is held by construction: there is no figure
anywhere in this kit, so nothing drawn from it can depict one of the
Fourteen. Mourning styles (line, mono wash) carry no colour but charcoal and
ivory, including in their filter definitions.

All coordinates are millimetres of the box the drawing fills.
"""

import math

MODES = ("cut", "flat", "line", "wash", "stitch", "riso", "gilt")


class Pen:
    def __init__(self, mode, pal, lw=0.35):
        assert mode in MODES, mode
        self.mode, self.pal, self.lw = mode, pal, lw

    def c(self, key):
        return self.pal.get(key, key)

    def f(self, key, layer=True):
        """Fill attributes for a shape. `layer` marks a main paper layer (gets
        the style's treatment); small details stay plain."""
        col, m = self.c(key), self.mode
        if m == "line":
            return (f'fill="{self.pal["ground"]}" stroke="{self.pal["ink"]}" '
                    f'stroke-width="{self.lw}" stroke-linejoin="round"')
        if m == "cut":
            return f'fill="{col}"' + (' filter="url(#cut)"' if layer else "")
        if m == "wash":
            return (f'fill="{col}" fill-opacity="0.78" filter="url(#wash)"' if layer
                    else f'fill="{col}" fill-opacity="0.85"')
        if m == "stitch":
            return (f'fill="{col}" stroke="{self.pal["stitch"]}" stroke-width="0.45" '
                    f'stroke-dasharray="1.1 0.8"' if layer else f'fill="{col}"')
        if m == "riso":
            return (f'fill="{col}" style="mix-blend-mode:multiply"'
                    + (' filter="url(#riso)"' if layer else ""))
        if m == "gilt":
            return (f'fill="{col}" stroke="{self.pal["gold"]}" stroke-width="0.35"' if layer
                    else f'fill="{col}"')
        return f'fill="{col}"'

    def s(self, key, w):
        col = self.pal["ink"] if self.mode == "line" else self.c(key)
        return f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"'

    def defs(self):
        p, m = self.pal, self.mode
        if m == "cut":
            return (f'<defs><filter id="cut" x="-10%" y="-20%" width="120%" height="140%">'
                    f'<feDropShadow dx="0" dy="-0.5" stdDeviation="0.7" flood-color="{p["shadow"]}" '
                    f'flood-opacity="0.3"/></filter></defs>')
        if m == "wash":
            return ('<defs><filter id="wash" x="-15%" y="-15%" width="130%" height="130%">'
                    '<feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="3" seed="7" result="n"/>'
                    '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.6"/>'
                    '<feGaussianBlur stdDeviation="0.35"/></filter></defs>')
        if m == "riso":
            return (f'<defs><filter id="riso" x="-10%" y="-10%" width="125%" height="125%">'
                    f'<feFlood flood-color="{p["riso2"]}" result="c"/>'
                    f'<feComposite in="c" in2="SourceAlpha" operator="in" result="g"/>'
                    f'<feOffset in="g" dx="0.9" dy="0.6" result="o"/>'
                    f'<feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge>'
                    f'</filter></defs>')
        return ""


def svg(pen, w, h, body, cls="art", aspect="xMidYMid slice"):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="{aspect}" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{pen.defs()}{body}</svg>')


def g(x, y, s, inner, flip=False):
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({-s if flip else s:.3f} {s:.3f})">{inner}</g>'


# ---------------------------------------------------------------- ground

def rect(p, x, y, w, h, key, layer=False):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {p.f(key, layer)}/>'


def dune(p, w, h, y, amp, key, phase=0.0, layer=True):
    a, b = w * (0.22 + phase), w * (0.5 + phase / 2)
    attrs = p.f(key, layer)
    if p.mode == "riso":
        # Riso ground layers butt up to each other rather than overprint, or
        # three inks stacked go to mud.
        attrs = attrs.replace(' style="mix-blend-mode:multiply"', "")
    return (f'<path {attrs} d="M0 {y:.1f} Q{a:.1f} {y - amp:.1f} {b:.1f} {y - amp * 0.2:.1f} '
            f'T{w} {y - amp * 0.35:.1f} V{h} H0Z"/>')


def band(p, w, h, y, key):
    return rect(p, 0, y, w, h - y, key, True)


def sun(p, cx, cy, r, key="sun"):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" {p.f(key, False)}/>'


def crescent(p, cx, cy, r, key="moon"):
    """Outer arc bulging left, inner arc of a wider circle cutting it back."""
    return (f'<path {p.f(key, False)} d="M{cx:.2f} {cy - r:.2f} A{r:.2f} {r:.2f} 0 1 0 {cx:.2f} {cy + r:.2f} '
            f'A{r * 1.25:.2f} {r * 1.25:.2f} 0 0 1 {cx:.2f} {cy - r:.2f}Z"/>')


def road_v(p, x, y, horizon, half=26, key="road"):
    """A straight road from the foot of a small picture to a point on its horizon."""
    return f'<path {p.f(key)} d="M{x - half} {y} L{x - 1} {horizon} L{x + 1} {horizon} L{x + half} {y}Z"/>'


def star(p, cx, cy, r, key="star"):
    k = r * 0.28
    d = (f"M{cx} {cy - r} L{cx + k} {cy - k} L{cx + r} {cy} L{cx + k} {cy + k} L{cx} {cy + r} "
         f"L{cx - k} {cy + k} L{cx - r} {cy} L{cx - k} {cy - k}Z")
    return f'<path d="{d}" {p.f(key, False)}/>'


def stars(p, w, h, n=9, seed=3, key="star"):
    out, x = "", seed * 7.0
    for i in range(n):
        x = (x * 37 + 11) % w
        y = ((i * 53 + seed * 17) % (h * 0.45)) + h * 0.05
        out += star(p, round(x, 1), round(y, 1), 0.9 + (i % 3) * 0.5, key)
    return out


# ---------------------------------------------------------------- plants

def palm(p, x, y, s=1.0, lean=4, trunk="trunk", frond="frond"):
    leaves = [(48, -84), (40, -112), (-40, -86), (-30, -112), (6, -124), (58, -100), (-54, -100)]
    lv = "".join(
        f'<path d="M{lean} -94 Q{(lean + ex) / 2:.1f} {-118 + (ey + 94) * 0.2 - 6:.1f} {ex} {ey} '
        f'Q{(lean + ex) / 2:.1f} {-104 + (ey + 94) * 0.1:.1f} {lean} -94Z" {p.f(frond)}/>'
        for ex, ey in leaves)
    return g(x, y, s, f'<path d="M-2.5 0 Q-3 -50 {lean - 1.6} -94 L{lean + 1.6} -94 Q3 -50 2.5 0Z" {p.f(trunk)}/>{lv}')


def tree(p, x, y, s=1.0, key="frond", trunk="trunk"):
    return g(x, y, s, f'<path d="M-2 0 L-1.5 -30 L1.5 -30 L2 0Z" {p.f(trunk)}/>'
                      f'<path d="M-30 -30 Q-28 -48 -6 -50 Q0 -58 10 -50 Q30 -48 32 -32 Q0 -24 -30 -30Z" {p.f(key)}/>')


# ---------------------------------------------------------------- buildings

def shrine(p, x, y, s=1.0, domes=1, minarets=2, dome="dome", body="body", tile="tile", tall=1.0):
    """A shrine in silhouette: a hall with arches, a drum, dome(s), minarets."""
    out = ""
    mx = {0: [], 1: [62], 2: [-66, 66], 4: [-72, -52, 52, 72]}[minarets]
    for m in mx:
        hgt = 128 * tall
        out += (f'<g transform="translate({m} 0)">'
                f'<rect x="-3.4" y="{-hgt}" width="6.8" height="{hgt}" {p.f(dome)}/>'
                f'<rect x="-5.2" y="{-hgt * 0.68:.1f}" width="10.4" height="3.4" {p.f(tile, False)}/>'
                f'<rect x="-5.2" y="{-hgt * 0.88:.1f}" width="10.4" height="3.4" {p.f(tile, False)}/>'
                f'<path d="M-3.4 {-hgt} L0 {-hgt - 12} L3.4 {-hgt}Z" {p.f(dome, False)}/></g>')
    arches = "".join(f'<path d="M{ax - 4} 0 V-12 Q{ax} -18 {ax + 4} -12 V0Z" {p.f(tile, False)}/>'
                     for ax in range(-48, 49, 12))
    out += f'<rect x="-56" y="-30" width="112" height="30" {p.f(body)}/>{arches}'
    out += f'<rect x="-56" y="-33" width="112" height="3" {p.f(tile, False)}/>'
    offs = [0] if domes == 1 else [-20, 20]
    for o in offs:
        r = 21 if domes == 1 else 15
        out += (f'<rect x="{o - r + 4}" y="-46" width="{2 * r - 8}" height="14" {p.f(tile)}/>'
                f'<path d="M{o - r} -46 Q{o - r - 2} -{46 + r * 1.6:.0f} {o} -{46 + r * 2.2:.0f} '
                f'Q{o + r + 2} -{46 + r * 1.6:.0f} {o + r} -46Z" {p.f(dome)}/>'
                f'<rect x="{o - 0.7}" y="-{56 + r * 2.2:.0f}" width="1.4" height="10" {p.f(dome, False)}/>')
    return g(x, y, s, out)


def malwiya(p, x, y, s=1.0, key="body", line="tile"):
    """Samarra's spiral minaret: a stepped cone with a ramp wound round it."""
    out = f'<path d="M-30 0 L-8 -110 L8 -110 L30 0Z" {p.f(key)}/>'
    for i in range(5):
        y0 = -i * 22
        out += f'<path d="M{-30 + i * 4.4:.1f} {y0} L{26 - i * 4.4:.1f} {y0 - 14}" {p.s(line, 1.6)}/>'
    out += f'<rect x="-8" y="-122" width="16" height="12" {p.f(key, False)}/>'
    return g(x, y, s, out)


def city(p, x, y, s=1.0, wall="body", water="water", tile="tile"):
    """A garrison city: a long crenellated wall, a gate, a river in front."""
    cren = "".join(f'<rect x="{cx}" y="-36" width="6" height="6" {p.f(wall, False)}/>' for cx in range(-90, 90, 12))
    return g(x, y, s, f'<rect x="-92" y="-30" width="184" height="30" {p.f(wall)}/>{cren}'
                      f'<path d="M-10 0 V-18 Q0 -28 10 -18 V0Z" {p.f(tile, False)}/>'
                      f'<path d="M-120 6 Q-60 2 0 6 T120 6 V16 H-120Z" {p.f(water)}/>')


def baqi(p, x, y, s=1.0, wall="body", ground="mid"):
    """Jannat al-Baqi as it stands: a low wall, unmarked ground, no dome."""
    mounds = "".join(f'<ellipse cx="{mx}" cy="-1" rx="7" ry="2.4" {p.f(ground, False)}/>' for mx in range(-60, 70, 18))
    return g(x, y, s, f'<rect x="-90" y="-14" width="180" height="14" {p.f(wall)}/>'
                      f'<rect x="-90" y="-16" width="180" height="2" {p.f("tile", False)}/>{mounds}')


def doorway(p, x, y, s=1.0, wall="body", dark="shade", door="accent"):
    """A threshold: a wall, an arched doorway, a door standing a little open."""
    return g(x, y, s, f'<rect x="-60" y="-90" width="120" height="90" {p.f(wall)}/>'
                      f'<path d="M-20 0 V-56 Q0 -76 20 -56 V0Z" {p.f(dark)}/>'
                      f'<path d="M-20 0 V-56 Q-12 -66 -2 -70 L-8 -2Z" {p.f(door)}/>'
                      f'<rect x="-30" y="0" width="60" height="5" {p.f("tile")}/>')


def window_barred(p, x, y, s=1.0, wall="body", glow="sun", bars="ink"):
    bar = "".join(f'<path d="M{bx} -20 V-70" {p.s(bars, 1.8)}/>' for bx in (-12, -4, 4, 12))
    return g(x, y, s, f'<rect x="-50" y="-100" width="100" height="100" {p.f(wall)}/>'
                      f'<path d="M-20 -20 V-62 Q0 -84 20 -62 V-20Z" {p.f("shade")}/>'
                      f'<circle cx="0" cy="-42" r="9" {p.f(glow, False)}/>{bar}'
                      f'<rect x="-24" y="-20" width="48" height="4" {p.f("tile", False)}/>')


def kaaba(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-36 0 V-58 L0 -64 V-6Z" {p.f("cube")}/>'
                      f'<path d="M0 -6 V-64 L30 -60 V-2Z" {p.f("cube2")}/>'
                      f'<path d="M-36 -48 L0 -54 L30 -50 V-46 L0 -50 L-36 -44Z" {p.f("gold", False)}/>'
                      f'<rect x="-22" y="-30" width="9" height="16" {p.f("gold", False)}/>'
                      f'<ellipse cx="0" cy="2" rx="60" ry="5" {p.f("mid", False)}/>')


def mountain_cave(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-90 0 L-40 -70 L-20 -58 L6 -96 L40 -50 L60 -62 L96 0Z" {p.f("far")}/>'
                      f'<path d="M-6 -44 Q2 -56 12 -44 Q10 -36 0 -36 Q-6 -38 -6 -44Z" {p.f("shade", False)}/>')


def house(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-28" y="-30" width="56" height="30" {p.f("body")}/>'
                      f'<rect x="-30" y="-33" width="60" height="4" {p.f("tile", False)}/>'
                      f'<rect x="-6" y="-18" width="12" height="18" {p.f("shade", False)}/>'
                      f'<rect x="12" y="-22" width="7" height="7" {p.f("shade", False)}/>')


def arcade(p, x, y, s=1.0, n=5):
    w = n * 24
    arches = "".join(f'<path d="M{-w / 2 + i * 24 + 4} 0 V-30 Q{-w / 2 + i * 24 + 12} -44 {-w / 2 + i * 24 + 20} -30 V0Z" '
                     f'{p.f("shade", False)}/>' for i in range(n))
    return g(x, y, s, f'<rect x="{-w / 2}" y="-52" width="{w}" height="52" {p.f("body")}/>{arches}')


def lantern(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M0 -40 V-34" {p.s("ink", 0.8)}/>'
                      f'<path d="M-6 -34 H6 L9 -26 L7 -8 H-7 L-9 -26Z" {p.f("accent")}/>'
                      f'<path d="M-4 -26 H4 L5 -12 H-5Z" {p.f("sun", False)}/>'
                      f'<path d="M-8 -8 H8 L5 -3 H-5Z" {p.f("accent", False)}/>')


def pool(p, x, y, s=1.0):
    return g(x, y, s, f'<ellipse cx="0" cy="0" rx="60" ry="9" {p.f("water")}/>'
                      f'<path d="M-30 0 Q0 -3 30 0" {p.s("sky", 0.6)}/>')


def standard(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-1.2" y="-120" width="2.4" height="120" {p.f("ink")}/>'
                      f'<path d="M0 -136 Q5 -128 0 -120 Q-5 -128 0 -136Z" {p.f("ink")}/>'
                      f'<rect x="-16" y="-118" width="32" height="2.4" {p.f("ink")}/>'
                      f'<path d="M-14 -116 H14 V-74 L7 -66 L0 -74 L-7 -66 L-14 -74Z" {p.f("cloak")}/>'
                      + "".join(f'<path d="M{tx} -116 V-58" {p.s("ink", 0.5)}/>'
                                f'<circle cx="{tx}" cy="-56" r="1.6" {p.f("ink", False)}/>' for tx in (-16, 16)))


def camel_kneeling(p, x, y, s=1.0, key="beast"):
    d = ("M0 0 C0 -10 4 -16 10 -18 C14 -30 30 -32 34 -20 C38 -16 42 -16 44 -20 "
         "C46 -28 48 -36 52 -38 C56 -40 62 -38 63 -34 C62 -32 58 -32 56 -32 "
         "C54 -30 52 -24 50 -14 C49 -6 48 0 44 0Z")
    return g(x, y, s, f'<path d="{d}" {p.f(key)}/>')


def camel_standing(p, x, y, s=1.0, key="beast"):
    d = ("M0 0 L1.6 -9 Q2 -18 10 -19 Q15 -27 20 -20 Q24 -18 26 -21 L30 -28 L33.5 -27.5 L29.5 -18 "
         "Q28 -12 26 -10 L27 0 L25 0 L23.5 -9 L9 -9 L6.5 0 L4.6 0 L5 -8 L2.6 -6 L2.4 0Z")
    return g(x, y, s, f'<path d="{d}" {p.f(key)}/>')


def road(p, w, h, horizon, x_far, key="road"):
    return (f'<path {p.f(key)} d="M{w * 0.30:.1f} {h} C{w * 0.42:.1f} {h * 0.82:.1f} {x_far - 10:.1f} {horizon + 22:.1f} '
            f'{x_far - 1.2:.1f} {horizon} L{x_far + 1.2:.1f} {horizon} C{x_far + 14:.1f} {horizon + 22:.1f} '
            f'{w * 0.78:.1f} {h * 0.8:.1f} {w * 0.72:.1f} {h}Z"/>')


def cloak(p, x, y, s=1.0):
    corners = [(-44, -6), (44, -6), (32, -30), (-32, -30)]
    body = (f'<path d="M-44 -6 Q-46 -2 -40 0 Q0 4 40 0 Q46 -2 44 -6 L32 -30 Q0 -34 -32 -30Z" {p.f("cloak")}/>'
            f'<path d="M-9 -15 Q-10 -22 -2 -23 Q8 -24 9 -17 Q10 -11 0 -11 Q-8 -11 -9 -15Z" {p.f("ink")}/>')
    return g(x, y, s, body + "".join(f'<circle cx="{cx}" cy="{cy}" r="2" {p.f("accent", False)}/>' for cx, cy in corners))


# ---------------------------------------------------------------- objects (stickers, postcards)

def sealed_letter(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-30" y="-40" width="60" height="40" {p.f("body")}/>'
                      f'<path d="M-30 -40 L0 -16 L30 -40" {p.s("ink", 1)}/>'
                      f'<circle cx="0" cy="-16" r="7" {p.f("accent")}/>')


def qalam(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-40 6 L30 -40 L36 -34 L-34 12Z" {p.f("accent")}/>'
                      f'<path d="M30 -40 L42 -48 L36 -34Z" {p.f("ink")}/>')


def scales(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M0 0 V-56 M-30 -50 H30" {p.s("ink", 2.2)}/>'
                      f'<path d="M-42 -30 Q-30 -18 -18 -30Z" {p.f("accent")}/>'
                      f'<path d="M18 -30 Q30 -18 42 -30Z" {p.f("accent")}/>'
                      f'<path d="M-30 -50 L-42 -30 M-30 -50 L-18 -30 M30 -50 L18 -30 M30 -50 L42 -30" {p.s("ink", 0.8)}/>'
                      f'<rect x="-14" y="-3" width="28" height="4" {p.f("ink")}/>')


def shield(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M0 -60 L30 -50 Q30 -14 0 0 Q-30 -14 -30 -50Z" {p.f("accent")}/>'
                      f'<path d="M0 -50 L20 -44 Q20 -18 0 -8 Q-20 -18 -20 -44Z" {p.f("tile", False)}/>')


def books(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-30" y="-12" width="60" height="12" {p.f("accent")}/>'
                      f'<rect x="-26" y="-24" width="54" height="12" {p.f("tile")}/>'
                      f'<rect x="-28" y="-36" width="50" height="12" {p.f("dome")}/>')


def coin(p, x, y, s=1.0):
    return g(x, y, s, f'<circle cx="0" cy="-20" r="20" {p.f("gold")}/>'
                      f'<circle cx="0" cy="-20" r="14" {p.s("ink", 0.8)}/>')


def handmill(p, x, y, s=1.0):
    return g(x, y, s, f'<ellipse cx="0" cy="-6" rx="32" ry="8" {p.f("body")}/>'
                      f'<ellipse cx="0" cy="-16" rx="28" ry="7" {p.f("tile")}/>'
                      f'<rect x="14" y="-34" width="4" height="18" {p.f("ink", False)}/>')


def bowl(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-30 -20 Q0 20 30 -20Z" {p.f("accent")}/>'
                      f'<rect x="-32" y="-22" width="64" height="3" {p.f("tile", False)}/>')


def seats(p, x, y, s=1.0, n=4):
    out = ""
    for i in range(n):
        cx = -36 + i * 24
        out += (f'<rect x="{cx - 8}" y="-30" width="16" height="16" {p.f("accent")}/>'
                f'<rect x="{cx - 9}" y="-14" width="18" height="4" {p.f("tile")}/>'
                f'<path d="M{cx - 7} -10 V0 M{cx + 7} -10 V0" {p.s("ink", 1)}/>')
    return g(x, y, s, out)


def branching(p, x, y, s=1.0):
    pts = [(0, -10), (-24, -36), (24, -36), (-36, -60), (-12, -60), (12, -60), (36, -60)]
    lines = "M0 -10 L-24 -36 M0 -10 L24 -36 M-24 -36 L-36 -60 M-24 -36 L-12 -60 M24 -36 L12 -60 M24 -36 L36 -60"
    return g(x, y, s, f'<path d="{lines}" {p.s("ink", 1.4)}/>'
                      + "".join(f'<circle cx="{a}" cy="{b}" r="5" {p.f("accent")}/>' for a, b in pts))


def mat(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-36" y="-14" width="72" height="14" {p.f("accent")}/>'
                      f'<rect x="-30" y="-11" width="60" height="8" {p.f("tile", False)}/>')


def flask(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-6 -50 H6 V-34 Q22 -24 18 -6 Q14 0 0 0 Q-14 0 -18 -6 Q-22 -24 -6 -34Z" {p.f("water")}/>')


def ring14(p, x, y, s=1.0):
    """The calendar ring, complete: fourteen marks round a circle."""
    out = f'<circle cx="0" cy="-34" r="30" {p.s("ink", 1.4)}/>'
    for i in range(14):
        a = 2 * math.pi * i / 14 - math.pi / 2
        out += f'<circle cx="{30 * math.cos(a):.2f}" cy="{-34 + 30 * math.sin(a):.2f}" r="3.6" {p.f("accent")}/>'
    return g(x, y, s, out)


# ---------------------------------------------------------------- scenes

def sky(p, w, h, time):
    out = rect(p, 0, 0, w, h, "sky")
    if time == "night":
        out += stars(p, w, h, 11) + crescent(p, w * 0.78, h * 0.18, min(w, h) * 0.07)
    elif time == "dusk":
        out += sun(p, w * 0.66, h * 0.58, min(w, h) * 0.16)
    elif time == "dawn":
        out += sun(p, w * 0.32, h * 0.62, min(w, h) * 0.12)
    else:
        out += sun(p, w * 0.68, h * 0.46, min(w, h) * 0.13)
    return out


def scene(p, w, h, motif, time="day", ground=0.72, scale=None, road_to=None, cx=0.5):
    """Sky, a far layer, the subject standing on it, then nearer layers."""
    base = h * ground
    s = scale if scale is not None else min(w / 190, h / 170) * 0.74
    out = sky(p, w, h, time)
    out += dune(p, w, h, base - h * 0.02, h * 0.06, "far", 0.1)
    out += motif(p, w * cx, base, s)
    out += dune(p, w, h, base + h * 0.06, h * 0.05, "mid", -0.1)
    out += dune(p, w, h, base + h * 0.17, h * 0.04, "near", 0.2)
    if road_to:
        # The road is the subject when there is one: drawn last, over the ground.
        out += road(p, w, h, base - h * 0.02, w * road_to)
    return out


# Each envelope's subjects, from 04-art/prompts.md. motif(p, cx, base_y, s).
def _palms_either(m):
    def f(p, x, y, s):
        return palm(p, x - 70 * s, y + 2, 0.7 * s) + m(p, x, y, s) + palm(p, x + 74 * s, y + 4, 0.6 * s, lean=-3)
    return f


SUBJECTS = {
    "karbala":   lambda p, x, y, s: shrine(p, x, y, s, 1, 2),
    "baqi":      lambda p, x, y, s: baqi(p, x, y, s) + palm(p, x - 50 * s, y - 13 * s, 0.6 * s) + palm(p, x + 46 * s, y - 13 * s, 0.7 * s, lean=-4),
    "nabawi":    lambda p, x, y, s: shrine(p, x, y, s, 1, 2) + palm(p, x - 86 * s, y + 4, 0.8 * s) + palm(p, x + 90 * s, y + 4, 0.7 * s, lean=-4),
    "samarra":   lambda p, x, y, s: shrine(p, x, y, s, 1, 2, tall=1.1),
    "samarra_city": lambda p, x, y, s: city(p, x, y, s) + malwiya(p, x + 52 * s, y - 30 * s, 0.55 * s),
    "door":      lambda p, x, y, s: doorway(p, x, y, s * 1.1) + palm(p, x + 70 * s, y + 2, 0.7 * s, lean=-3),
    "najaf":     lambda p, x, y, s: shrine(p, x, y, s, 1, 2, tall=1.05),
    "kaaba":     lambda p, x, y, s: kaaba(p, x, y, s * 1.2),
    "window":    lambda p, x, y, s: window_barred(p, x, y, s * 1.1),
    "hira":      lambda p, x, y, s: mountain_cave(p, x, y, s * 1.1),
    "courtyard": lambda p, x, y, s: arcade(p, x, y, s) + lantern(p, x, y - 30 * s, s * 0.9),
    "road_dawn": lambda p, x, y, s: "",
    "jamkaran":  lambda p, x, y, s: shrine(p, x, y, s, 1, 2),
    "qadr":      lambda p, x, y, s: arcade(p, x, y, s, 4) + star(p, x, y - 90 * s, 6 * s, "sun"),
    "teaching":  lambda p, x, y, s: arcade(p, x, y, s) + books(p, x - 20 * s, y, 0.5 * s) + lantern(p, x + 24 * s, y - 10 * s, 0.6 * s),
    "eid":       lambda p, x, y, s: shrine(p, x, y, s * 0.9, 1, 1) + lantern(p, x - 60 * s, y - 80 * s, 0.9 * s) + lantern(p, x + 50 * s, y - 92 * s, 0.8 * s),
    "mashhad":   lambda p, x, y, s: shrine(p, x, y, s, 1, 2, tall=1.1),
    "qom":       lambda p, x, y, s: shrine(p, x, y, s, 1, 2),
    "kadhimiya": lambda p, x, y, s: shrine(p, x, y, s, 2, 4),
    "ghadir":    lambda p, x, y, s: pool(p, x, y + 8 * s, s) + tree(p, x - 54 * s, y, s * 0.9) + tree(p, x + 50 * s, y + 2, s * 0.8) + palm(p, x + 80 * s, y + 4, 0.6 * s),
    "standard":  lambda p, x, y, s: standard(p, x, y, s * 0.8),
    "zaynab":    lambda p, x, y, s: shrine(p, x, y, s, 1, 2),
    "house":     lambda p, x, y, s: house(p, x, y, s * 1.2) + palm(p, x - 50 * s, y + 2, 0.75 * s) + palm(p, x + 46 * s, y + 2, 0.6 * s, lean=-3),
    "quba":      lambda p, x, y, s: camel_kneeling(p, x - 80 * s, y + 24 * s, 0.9 * s) + "".join(palm(p, x + dx * s, y - 2 * s, 0.32 * s) for dx in (40, 50, 60, 70)),
    "cloak":     lambda p, x, y, s: cloak(p, x, y + 10 * s, s * 0.9),
}

OBJECTS = {
    "sealed_letter": sealed_letter, "qalam": qalam, "scales": scales, "shield": shield, "books": books,
    "coin": coin, "handmill": handmill, "bowl": bowl, "seats": seats, "branching": branching, "mat": mat,
    "flask": flask, "lantern": lambda p, x, y, s: lantern(p, x, y, s * 1.4), "ring14": ring14,
    "cloak": lambda p, x, y, s: cloak(p, x, y, s * 0.7),
    "palm": lambda p, x, y, s: palm(p, x, y, s * 0.42),
    "door": lambda p, x, y, s: doorway(p, x, y, s * 0.45),
    "window": lambda p, x, y, s: window_barred(p, x, y, s * 0.45),
    "camel": lambda p, x, y, s: camel_standing(p, x - 16 * s, y, s * 1.0),
    "star": lambda p, x, y, s: star(p, x, y - 14 * s, 12 * s, "accent"),
    "crescent": lambda p, x, y, s: crescent(p, x, y - 16 * s, 14 * s, "accent"),
    "shrine": lambda p, x, y, s: shrine(p, x, y, s * 0.36, 1, 2),
}
