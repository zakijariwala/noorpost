"""Paper Dunes — the illustration library.

Every piece of art in the Paper Dunes set is drawn here, as SVG, from a small
kit of cut-paper shapes: dunes, palms, a dome, a road, a camel, a cloak, a
standard. Layers sit on each other with a soft shadow, the way cut card does.

The rules from design-system.md §3 are held by construction, not by review:
there is no figure anywhere in this kit, so no drawing made from it can depict
one of the Fourteen. Mourning art (envelopes 01, 02) is drawn by the same
functions in line mode: charcoal stroke on ivory, no fill colour at all.

All coordinates are millimetres of the page the drawing sits on.
"""

# ---------- palette ----------

STD = {
    "sand": "#FFF6EA", "dune": "#FCEBD5", "sky": "#F9D9B4", "apricot": "#F6B48A",
    "clay": "#E58F7B", "oasis": "#1F5C63", "dusk": "#5B3A63", "ink": "#3B2440",
    "green": "#3E8E6E", "sun": "#F6B48A", "trunk": "#5B3A63", "frond": "#1F5C63",
    "road": "#FCEBD5", "stone": "#3B2440", "cloak": "#1F5C63", "cloak2": "#2C7179",
}

MOURN_INK = "#1B1B1B"
MOURN_GROUND = "#F3EDE1"


class Pen:
    """Draws one layer. In colour mode a shape is filled and shadowed; in
    mourning (line) mode it is ivory with a charcoal outline, nothing else."""

    def __init__(self, mourning=False):
        self.mourning = mourning

    def fill(self, colour, shadow=True):
        if self.mourning:
            return f'fill="{MOURN_GROUND}" stroke="{MOURN_INK}" stroke-width="0.35" stroke-linejoin="round"'
        f = ' filter="url(#cut)"' if shadow else ""
        return f'fill="{colour}"{f}'

    def c(self, key):
        return MOURN_INK if self.mourning else STD[key]


def defs(blur=0.7, dy=-0.5):
    return (f'<defs><filter id="cut" x="-10%" y="-20%" width="120%" height="140%">'
            f'<feDropShadow dx="0" dy="{dy}" stdDeviation="{blur}" flood-color="#3B2440" '
            f'flood-opacity="0.28"/></filter></defs>')


def svg(w, h, body, cls="art", extra=""):
    # The shadow filter only goes in when something uses it. Line-mode (mourning)
    # art never does, so a mourning page carries no colour at all, not even in defs.
    d = defs() if "url(#cut)" in body else ""
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true"{extra}>{d}{body}</svg>')


# ---------- shapes ----------

def rect(pen, x, y, w, h, colour, shadow=False):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {pen.fill(colour, shadow)}/>'


def dune(pen, w, h, y, amp, colour, phase=0.0, shadow=True):
    """A dune layer across the whole width, from y down to the foot of the page."""
    a, b = w * (0.22 + phase), w * (0.5 + phase / 2)
    return (f'<path {pen.fill(colour, shadow)} d="M0 {y} Q{a:.1f} {y - amp:.1f} {b:.1f} {y - amp * 0.2:.1f} '
            f'T{w} {y - amp * 0.35:.1f} V{h} H0Z"/>')


def sun(pen, cx, cy, r, colour="sun"):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" {pen.fill(pen.c(colour) if pen.mourning else STD[colour], False)}/>'


def star(pen, cx, cy, r, colour):
    k = r * 0.28
    d = (f"M{cx} {cy - r} L{cx + k} {cy - k} L{cx + r} {cy} L{cx + k} {cy + k} L{cx} {cy + r} "
         f"L{cx - k} {cy + k} L{cx - r} {cy} L{cx - k} {cy - k}Z")
    return f'<path d="{d}" {pen.fill(colour, False)}/>'


def palm(pen, x, y, s=1.0, trunk="trunk", frond="frond", lean=4):
    """A palm, base at (x, y), roughly 100*s tall."""
    t, f = STD[trunk], STD[frond]
    leaves = [(48, -84), (40, -112), (-40, -86), (-30, -112), (6, -124), (58, -100), (-54, -100)]
    lv = "".join(
        f'<path d="M{lean} -94 Q{(lean + ex) / 2:.1f} {-118 + (ey + 94) * 0.2 - 6:.1f} {ex} {ey} '
        f'Q{(lean + ex) / 2:.1f} {-104 + (ey + 94) * 0.1:.1f} {lean} -94Z" {pen.fill(f)}/>'
        for ex, ey in leaves)
    trunk_d = f"M-2.5 0 Q-3 -50 {lean - 1.6} -94 L{lean + 1.6} -94 Q3 -50 2.5 0Z"
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="{trunk_d}" {pen.fill(t)}/>{lv}</g>')


def mosque(pen, x, y, s=1.0, dome="green", body="dune", minarets=True):
    """Masjid an-Nabawi in silhouette: a low hall, the dome, two minarets."""
    db, dd = STD[body], STD[dome]
    m = ""
    if minarets:
        for mx in (-74, 74):
            m += (f'<g transform="translate({mx} 0)">'
                  f'<rect x="-3.4" y="-128" width="6.8" height="128" {pen.fill(db)}/>'
                  f'<rect x="-5.2" y="-86" width="10.4" height="3.4" {pen.fill(db, False)}/>'
                  f'<rect x="-5.2" y="-112" width="10.4" height="3.4" {pen.fill(db, False)}/>'
                  f'<path d="M-3.4 -128 L0 -142 L3.4 -128Z" {pen.fill(dd, False)}/></g>')
    arches = "".join(
        f'<path d="M{ax - 4} 0 V-12 Q{ax} -18 {ax + 4} -12 V0Z" '
        f'{pen.fill(STD["apricot"] if not pen.mourning else "", False)} opacity="0.85"/>'
        for ax in range(-48, 49, 12))
    return (f'<g transform="translate({x} {y}) scale({s})">{m}'
            f'<rect x="-58" y="-30" width="116" height="30" {pen.fill(db)}/>{arches}'
            f'<rect x="-17" y="-46" width="34" height="16" {pen.fill(db)}/>'
            f'<path d="M-21 -46 Q-23 -80 0 -92 Q23 -80 21 -46Z" {pen.fill(dd)}/>'
            f'<rect x="-0.7" y="-101" width="1.4" height="10" {pen.fill(dd, False)}/>'
            f'<circle cx="0" cy="-103" r="2.2" {pen.fill(dd, False)}/></g>')


def camel_kneeling(pen, x, y, s=1.0, colour="dusk", flip=False):
    d = ("M0 0 C0 -10 4 -16 10 -18 C14 -30 30 -32 34 -20 C38 -16 42 -16 44 -20 "
         "C46 -28 48 -36 52 -38 C56 -40 62 -38 63 -34 C62 -32 58 -32 56 -32 "
         "C54 -30 52 -24 50 -14 C49 -6 48 0 44 0Z")
    fx = -s if flip else s
    return (f'<g transform="translate({x} {y}) scale({fx} {s})">'
            f'<path d="{d}" {pen.fill(STD[colour])}/>'
            f'<ellipse cx="22" cy="-0.6" rx="17" ry="2.2" {pen.fill(STD["ink"], False)} opacity="0.55"/>'
            '</g>')


def camel_standing(pen, x, y, s=1.0, colour="dusk"):
    d = ("M0 0 L1.6 -9 Q2 -18 10 -19 Q15 -27 20 -20 Q24 -18 26 -21 L30 -28 L33.5 -27.5 L29.5 -18 "
         "Q28 -12 26 -10 L27 0 L25 0 L23.5 -9 L9 -9 L6.5 0 L4.6 0 L5 -8 L2.6 -6 L2.4 0Z")
    return f'<g transform="translate({x} {y}) scale({s})"><path d="{d}" {pen.fill(STD[colour])}/></g>'


def road(pen, w, h, horizon, x_far, colour="road"):
    """An empty road from the foot of the picture to a point on the horizon."""
    return (f'<path {pen.fill(STD[colour])} d="M{w * 0.30:.1f} {h} '
            f'C{w * 0.42:.1f} {h * 0.82:.1f} {x_far - 10:.1f} {horizon + 22:.1f} {x_far - 1.2:.1f} {horizon} '
            f'L{x_far + 1.2:.1f} {horizon} C{x_far + 14:.1f} {horizon + 22:.1f} {w * 0.78:.1f} {h * 0.8:.1f} '
            f'{w * 0.72:.1f} {h}Z"/>')


def cloak(pen, x, y, s=1.0, cords=None, colour="cloak"):
    """The cloak, spread flat, the stone in the middle, one cord at each corner.
    `cords` is four (x, y) points in page space the corners reach out to."""
    corners = [(-44, -6), (44, -6), (32, -30), (-32, -30)]
    pts = [(x + cx * s, y + cy * s) for cx, cy in corners]
    out = ""
    if cords:
        for (px, py), (tx, ty) in zip(pts, cords):
            col = MOURN_INK if pen.mourning else STD["clay"]
            out += (f'<path d="M{px:.1f} {py:.1f} Q{(px + tx) / 2:.1f} {max(py, ty) + 6:.1f} {tx} {ty}" '
                    f'fill="none" stroke="{col}" stroke-width="{0.9 * s:.2f}" stroke-linecap="round" '
                    f'stroke-dasharray="{2.4 * s:.1f} {1.4 * s:.1f}"/>')
            out += f'<circle cx="{tx}" cy="{ty}" r="{1.6 * s:.1f}" {pen.fill(STD["clay"], False)}/>'
    body = (f'<path d="M-44 -6 Q-46 -2 -40 0 Q0 4 40 0 Q46 -2 44 -6 L32 -30 Q0 -34 -32 -30Z" '
            f'{pen.fill(STD[colour])}/>'
            f'<path d="M-38 -9 Q0 -5 38 -9 L28 -27 Q0 -30 -28 -27Z" '
            f'{pen.fill(STD["cloak2"] if not pen.mourning else MOURN_GROUND, False)}/>'
            f'<path d="M-9 -15 Q-10 -22 -2 -23 Q8 -24 9 -17 Q10 -11 0 -11 Q-8 -11 -9 -15Z" '
            f'{pen.fill(STD["stone"])}/>')
    tassels = "".join(f'<circle cx="{cx}" cy="{cy}" r="2" {pen.fill(STD["apricot"], False)}/>'
                      for cx, cy in corners)
    return out + f'<g transform="translate({x} {y}) scale({s})">{body}{tassels}</g>'


def standard(pen, x, y, s=1.0):
    """A standard with no rider: a pole, a crossbar, the cloth hanging still."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-1.2" y="-120" width="2.4" height="120" {pen.fill(STD["dusk"])}/>'
            f'<path d="M0 -136 Q5 -128 0 -120 Q-5 -128 0 -136Z" {pen.fill(STD["dusk"])}/>'
            f'<rect x="-16" y="-118" width="32" height="2.4" {pen.fill(STD["dusk"])}/>'
            f'<path d="M-14 -116 H14 V-74 L7 -66 L0 -74 L-7 -66 L-14 -74Z" {pen.fill(STD["oasis"])}/>'
            f'<path d="M-9 -110 H9" stroke="{pen.c("apricot")}" stroke-width="0.8"/>'
            + "".join(f'<path d="M{tx} -116 V-58" stroke="{pen.c("dusk")}" stroke-width="0.5"/>'
                      f'<circle cx="{tx}" cy="-56" r="1.6" {pen.fill(STD["dusk"], False)}/>'
                      for tx in (-16, 16))
            + '</g>')


def lantern(pen, x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M0 -40 V-34" stroke="{pen.c("dusk")}" stroke-width="0.8"/>'
            f'<path d="M-6 -34 H6 L9 -26 L7 -8 H-7 L-9 -26Z" {pen.fill(STD["dusk"])}/>'
            f'<path d="M-4 -26 H4 L5 -12 H-5Z" {pen.fill(STD["apricot"], False)}/>'
            f'<path d="M-8 -8 H8 L5 -3 H-5Z" {pen.fill(STD["dusk"], False)}/></g>')


def stamp_ring(month, number, colour, ring_text="NOOR POST", ground="#FFF6EA"):
    """The cancellation mark: ring, month round the top, number in the middle,
    wavy killer bars. 46 mm box."""
    bars = "".join(f'<path d="M50 {y} q6 -3 12 0 t12 0 t12 0 t12 0 t12 0" fill="none" '
                   f'stroke="{colour}" stroke-width="1.3" opacity="0.85"/>' for y in (36, 44, 52, 60))
    return (f'<svg viewBox="0 0 120 96" class="stamp" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<defs><path id="arcTop" d="M14 48 A34 34 0 0 1 82 48"/>'
            f'<path id="arcBot" d="M18 52 A30 30 0 0 0 78 52"/></defs>{bars}'
            f'<circle cx="48" cy="48" r="40" fill="{ground}" fill-opacity="0.92" stroke="{colour}" stroke-width="2"/>'
            f'<circle cx="48" cy="48" r="27" fill="none" stroke="{colour}" stroke-width="1"/>'
            f'<text font-family="Nunito Sans, sans-serif" font-weight="800" font-size="7.4" '
            f'letter-spacing="1.6" fill="{colour}" text-anchor="middle">'
            f'<textPath href="#arcTop" startOffset="50%">{month}</textPath></text>'
            f'<text font-family="Nunito Sans, sans-serif" font-weight="800" font-size="6" '
            f'letter-spacing="2" fill="{colour}" text-anchor="middle">'
            f'<textPath href="#arcBot" startOffset="50%">{ring_text}</textPath></text>'
            f'<text x="48" y="58" font-family="Young Serif, serif" font-size="28" fill="{colour}" '
            f'text-anchor="middle">{number}</text></svg>')


def seal(colour, mourning=False):
    """The wax seal: a scalloped disc with an eight-point star pressed into it."""
    import math
    n, r1, r2 = 18, 48, 44
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        r = r1 if i % 2 == 0 else r2
        pts.append(f"{50 + r * math.cos(a):.2f} {50 + r * math.sin(a):.2f}")
    edge = "M" + " L".join(pts) + "Z"
    inner = "#FFF6EA" if not mourning else "#F3EDE1"
    return (f'<svg viewBox="0 0 100 100" class="seal" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<path d="{edge}" fill="{colour}"/>'
            f'<circle cx="50" cy="50" r="34" fill="none" stroke="{inner}" stroke-opacity="0.45" stroke-width="1.4"/>'
            f'<path d="M50 24 L56 41 L74 38 L61 50 L74 62 L56 59 L50 76 L44 59 L26 62 L39 50 L26 38 L44 41Z" '
            f'fill="{inner}" fill-opacity="0.85"/>'
            f'<circle cx="50" cy="50" r="6" fill="{colour}"/></svg>')
