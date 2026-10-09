"""Richer art for the two mourning envelopes, 01 (Muharram) and 02 (Safar).

The mourning rule holds: charcoal #1B1B1B and ivory #F3EDE1 only. What these
add is everything else a picture can have inside two inks — tone (charcoal at
many strengths), texture (wash, grain, hatching) and detail — so the two most
important envelopes in the box are not the plainest.

  01 · ink wash: the camp at Karbala at nightfall; the shrine lit against the
       night; the standard; the river.
  02 · charcoal engraving: al-Baqi at dawn, hatched; the road; the treaty.

No figure anywhere, as in the rest of the box's kit.

    render(nn, item, w, h) -> svg body (no outer <svg>), or None
"""

import math

INK, IV = "#1B1B1B", "#F3EDE1"


def outline(wd, a=1.0):
    """Stroke attributes alone, for a shape that carries its own fill."""
    return f'stroke="{INK}" stroke-width="{wd}" stroke-opacity="{a}" stroke-linejoin="round"'


def ink(a):
    return f'fill="{INK}" fill-opacity="{a}"'


def stroke(wd, a=1.0):
    return f'fill="none" stroke="{INK}" stroke-width="{wd}" stroke-opacity="{a}" stroke-linecap="round" stroke-linejoin="round"'


# ---------------------------------------------------------------- shared defs

def defs(uid):
    """Wash, grain and hatch fills. Filters carry no colour of their own."""
    return (f'<defs>'
            f'<filter id="mw{uid}" x="-10%" y="-10%" width="120%" height="120%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="3" seed="11" result="n"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="2.4"/><feGaussianBlur stdDeviation="0.3"/></filter>'
            f'<filter id="mg{uid}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="5" stitchTiles="stitch"/>'
            f'<feColorMatrix type="matrix" values="0 0 0 0 0.106  0 0 0 0 0.106  0 0 0 0 0.106  0 0 0 1.2 -0.5"/></filter>'
            f'<pattern id="h1{uid}" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<path d="M0 0.8 H1.6" stroke="{INK}" stroke-width="0.32"/></pattern>'
            f'<pattern id="h2{uid}" width="1.4" height="1.4" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">'
            f'<path d="M0 0.7 H1.4" stroke="{INK}" stroke-width="0.3"/></pattern>'
            f'<pattern id="h0{uid}" width="2" height="1.3" patternUnits="userSpaceOnUse">'
            f'<path d="M0 0.65 H2" stroke="{INK}" stroke-width="0.26"/></pattern>'
            f'</defs>')


def grain(uid, w, h, op=0.35):
    return f'<rect width="{w}" height="{h}" filter="url(#mg{uid})" opacity="{op}"/>'


def wash(uid, inner):
    return f'<g filter="url(#mw{uid})">{inner}</g>'


def gradient(uid, name, stops, vertical=True):
    s = "".join(f'<stop offset="{o}" stop-color="{INK}" stop-opacity="{a}"/>' for o, a in stops)
    return (f'<defs><linearGradient id="{name}{uid}" x1="0" y1="0" x2="{0 if vertical else 1}" y2="{1 if vertical else 0}">'
            f'{s}</linearGradient></defs>')


def g(x, y, s, inner):
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({s:.3f})">{inner}</g>'


# ---------------------------------------------------------------- wash pieces (01)

def w_palm(x, y, s, a=0.7, lean=3):
    leaves = [(30, -60), (24, -76), (-26, -60), (-20, -76), (4, -84), (36, -70), (-34, -70)]
    lv = "".join(f'<path d="M{lean} -64 Q{(lean + ex) / 2:.1f} {-80 + (ey + 64) * 0.2 - 4:.1f} {ex} {ey} '
                 f'Q{(lean + ex) / 2:.1f} {-70 + (ey + 64) * 0.1:.1f} {lean} -64Z" {ink(a)}/>' for ex, ey in leaves)
    return g(x, y, s, f'<path d="M-1.6 0 Q-2 -34 {lean - 1} -64 L{lean + 1} -64 Q2 -34 1.6 0Z" {ink(a)}/>{lv}')


def w_tent(x, y, s, a=0.72, door=True):
    body = f'<path d="M-16 0 L-11 -12 Q0 -18 11 -12 L16 0Z" {ink(a)}/><path d="M0 -17 V-21" {stroke(0.6, a)}/>'
    if door:
        body += f'<path d="M-2.4 0 L0 -9 L2.4 0Z" fill="{IV}" fill-opacity="0.55"/>'
    return g(x, y, s, body)


def w_alam(x, y, s, a=0.92, wave=1.0):
    """The standard: a tall pole, a finial, a banner moving in wind, bordered and tasselled."""
    b = (f'M3 -150 Q{24 * wave} -146 {44 * wave} -150 Q{52 * wave} -126 {46 * wave} -98 '
         f'Q{26 * wave} -92 3 -100Z')
    border = (f'M6 -147 Q{24 * wave} -143 {41 * wave} -147 Q{48 * wave} -126 {43 * wave} -101 Q{26 * wave} -96 6 -103Z')
    tassels = ""
    diamonds = "".join(f'<circle cx="{dx * wave:.1f}" cy="{dy:.1f}" r="0.7" fill="{IV}" fill-opacity="0.7"/>'
                       for dx, dy in [(6 + i * 4.6, -145.5 + (i % 2) * 0.6) for i in range(9)]
                       + [(6 + i * 4.6, -103 + (i % 2) * 0.6) for i in range(9)])
    diamonds += "".join(f'<path d="M{fx * wave:.1f} -99 v4" {stroke(0.5, a)}/>' for fx in range(6, 46, 2))
    return g(x, y, s, f'<rect x="-1.4" y="-168" width="2.8" height="168" {ink(a)}/>'
                      f'<path d="M0 -186 Q7 -176 0 -166 Q-7 -176 0 -186Z" {ink(a)}/>'
                      f'<path d="M-6 -168 H6" {stroke(1.6, a)}/><circle cx="0" cy="-170" r="2" {ink(a)}/>'
                      f'<path d="{b}" {ink(a * 0.85)}/>'
                      f'<path d="{border}" fill="none" stroke="{IV}" stroke-opacity="0.55" stroke-width="0.7"/>'
                      f'{diamonds}{tassels}'
                      f'<path d="M-1 -160 Q-12 -150 -8 -134 M1 -158 Q-8 -146 -4 -128" {stroke(0.8, a * 0.8)}/>')


def w_bowl(x, y, s, a=0.8):
    return g(x, y, s, f'<path d="M-34 -18 Q-30 4 0 4 Q30 4 34 -18Z" {ink(a * 0.75)}/>'
                      f'<ellipse cx="0" cy="-18" rx="34" ry="5" {ink(a)}/>'
                      f'<ellipse cx="0" cy="-17.4" rx="29" ry="3.6" fill="{IV}" fill-opacity="0.75"/>'
                      f'<path d="M-14 -17.4 Q0 -19 14 -17.4 M-8 -16.2 Q0 -17 8 -16.2" {stroke(0.4, 0.5)}/>'
                      f'<rect x="-10" y="3" width="20" height="4" rx="1.5" {ink(a * 0.75)}/>'
                      f'<path d="M-30 -10 Q-26 -2 -14 0" fill="none" stroke="{IV}" stroke-opacity="0.35" stroke-width="1"/>')


def w_waterskin(x, y, s, a=0.8):
    return g(x, y, s, f'<path d="M-6 -40 H6 L7 -34 Q22 -30 22 -14 Q22 0 0 0 Q-22 0 -22 -14 Q-22 -30 -7 -34Z" {ink(a)}/>'
                      f'<path d="M-6 -40 H6 V-44 H-6Z" {ink(1)}/><path d="M-16 -22 Q0 -14 16 -22" '
                      f'fill="none" stroke="{IV}" stroke-opacity="0.5" stroke-width="0.8"/>'
                      f'<path d="M-6 -42 Q-24 -46 -26 -20" {stroke(1.2, a)}/>')


def w_birds(pts, s=1.0, a=0.6):
    return "".join(g(x, y, s * k, f'<path d="M-6 0 Q-3 -3 0 0 Q3 -3 6 0" {stroke(0.9, a)}/>') for x, y, k in pts)


def w_shrine(x, y, s):
    """Karbala's shrine lit against the night: ivory on charcoal."""
    arches = "".join(f'<path d="M{ax} 0 V-14 Q{ax + 4.5} -21 {ax + 9} -14 V0Z" {ink(0.75)}/>'
                     f'<circle cx="{ax + 4.5}" cy="-9" r="1.1" fill="{IV}"/>' for ax in range(-46, 46, 13))
    tile = "".join(f'<path d="M{tx} -30 l2 -2.4 l2 2.4 l-2 2.4Z" {ink(0.45)}/>' for tx in range(-48, 48, 6))
    dome_lines = "".join(f'<path d="M{dx * 0.9:.1f} -42 Q{dx * 0.95:.1f} -64 0 -86" {stroke(0.35, 0.3)}/>' for dx in (-16, -8, 8, 16))

    def minaret(mx):
        return (f'<rect x="{mx - 3}" y="-96" width="6" height="96" fill="{IV}"/>'
                f'<rect x="{mx - 5}" y="-74" width="10" height="3" fill="{IV}"/><rect x="{mx - 4.6}" y="-71" width="9.2" height="1.2" {ink(0.6)}/>'
                f'<rect x="{mx - 4.4}" y="-100" width="8.8" height="4" fill="{IV}"/>'
                f'<path d="M{mx - 3.4} -100 Q{mx} -114 {mx + 3.4} -100Z" fill="{IV}"/><path d="M{mx} -114 V-121" {stroke(0.6, 0.9)}/>'
                f'<path d="M{mx} -121 l9 2.6 l-9 2.6Z" fill="{IV}" fill-opacity="0.4" stroke="{IV}" stroke-width="0.4"/>'
                + "".join(f'<rect x="{mx - 1}" y="{wy}" width="2" height="4" rx="1" {ink(0.55)}/>' for wy in (-62, -46, -30)))
    return g(x, y, s, f'<ellipse cx="0" cy="-60" rx="54" ry="48" fill="{IV}" fill-opacity="0.08"/>'
                      f'<ellipse cx="0" cy="-58" rx="34" ry="30" fill="{IV}" fill-opacity="0.08"/>'
                      + minaret(-58) + minaret(58)
                      + f'<rect x="-50" y="-34" width="100" height="34" fill="{IV}"/>{tile}{arches}'
                      f'<rect x="-50" y="-36" width="100" height="2" {ink(0.5)}/>'
                      f'<rect x="-22" y="-42" width="44" height="7" fill="{IV}"/>'
                      f'<path d="M-20 -42 C-24 -68 -6 -84 0 -88 C6 -84 24 -68 20 -42Z" fill="{IV}"/>{dome_lines}'
                      f'<path d="M0 -88 V-98" {stroke(0.7, 0.9)}/><circle cx="0" cy="-99" r="1.6" fill="{IV}"/>')


# ---------------------------------------------------------------- 01 compositions

def karbala_front(uid, w, h):
    hz = h * 0.66
    out = (gradient(uid, "sk", [(0, 0.62), (0.45, 0.32), (0.66, 0.06)])
           + f'<rect width="{w}" height="{h}" fill="{IV}"/><rect width="{w}" height="{hz:.1f}" fill="url(#sk{uid})"/>')
    out += wash(uid, "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" {ink(a)}/>'
                             for cx, cy, rx, ry, a in ((60, 52, 70, 6, 0.1), (170, 70, 80, 5, 0.08), (110, 88, 90, 4, 0.07))))
    # a thin new moon — Muharram's — in ivory
    out += f'<path d="M126 24 A7 7 0 1 0 126 38 A8.8 8.8 0 0 1 126 24Z" fill="{IV}" fill-opacity="0.9"/>'
    out += w_birds([(96, 44, 0.9), (106, 40, 0.7), (88, 50, 0.6)])
    out += wash(uid, f'<path d="M0 {hz - 8} Q60 {hz - 14} 120 {hz - 9} T{w} {hz - 10} V{hz + 4} H0Z" {ink(0.2)}/>')
    # the river, pale, with its reflections
    out += (f'<path d="M0 {hz + 2} Q80 {hz - 1} 160 {hz + 3} T{w} {hz + 2} V{hz + 9} Q120 {hz + 7} 0 {hz + 10}Z" fill="{IV}"/>'
            + "".join(f'<path d="M{rx} {hz + 5 + (i % 3)} h{8 + i % 4 * 3}" {stroke(0.4, 0.35)}/>' for i, rx in enumerate(range(6, 220, 17))))
    for i, (px, ps) in enumerate(((10, 0.62), (22, 0.5), (34, 0.7), (46, 0.45), (58, 0.56), (70, 0.4))):
        out += w_palm(px, hz + 2, ps, 0.55 + (i % 3) * 0.1, lean=3 if i % 2 else -3)
    for i, tx in enumerate(range(84, 214, 13)):
        out += w_tent(tx, hz + 6 + (i % 2) * 1.5, 0.55 + (i % 3) * 0.08, 0.62 + (i % 2) * 0.12)
    out += wash(uid, f'<path d="M0 {hz + 10} Q70 {hz + 6} 140 {hz + 12} T{w} {hz + 9} V{h + 2} H0Z" {ink(0.3)}/>'
                     f'<path d="M0 {hz + 26} Q90 {hz + 20} 180 {hz + 28} T{w} {hz + 24} V{h + 2} H0Z" {ink(0.22)}/>')
    out += f'<rect y="{hz + 12}" width="{w}" height="{h - hz}" fill="url(#h0{uid})" opacity="0.18"/>'
    out += w_alam(176, h - 8, 0.5, 0.92)
    out += w_bowl(206, h - 10, 0.3, 0.85)
    return out + grain(uid, w, h)


def karbala_shrine(uid, w, h):
    hz = h * 0.8
    out = (gradient(uid, "ns", [(0, 0.95), (0.6, 0.8), (0.8, 0.55)])
           + f'<rect width="{w}" height="{h}" fill="{IV}"/><rect width="{w}" height="{h}" fill="url(#ns{uid})"/>')
    out += "".join(f'<circle cx="{(i * 37 + 11) % w:.1f}" cy="{(i * 53 + 7) % (h * 0.45) + 6:.1f}" r="{0.35 + (i % 3) * 0.25:.2f}" '
                   f'fill="{IV}" fill-opacity="{0.5 + (i % 2) * 0.4}"/>' for i in range(34))
    out += w_shrine(w / 2, hz, w / 150)
    out += (f'<path d="M0 {hz} H{w} V{h} H0Z" {ink(0.85)}/>'
            + "".join(f'<circle cx="{lx}" cy="{hz + 8}" r="1.1" fill="{IV}" fill-opacity="0.8"/>'
                      f'<ellipse cx="{lx}" cy="{hz + 9.5}" rx="5" ry="1" fill="{IV}" fill-opacity="0.12"/>' for lx in range(12, int(w), 22))
            + f'<rect y="{hz}" width="{w}" height="{h - hz}" fill="url(#h0{uid})" opacity="0.25"/>')
    return out + grain(uid, w, h, 0.3)


def standard_print(uid, w, h, small=False):
    hz = h * 0.72
    out = (gradient(uid, "sd", [(0, 0.45), (0.5, 0.2), (0.72, 0.04)])
           + f'<rect width="{w}" height="{h}" fill="{IV}"/><rect width="{w}" height="{hz:.1f}" fill="url(#sd{uid})"/>')
    out += wash(uid, f'<ellipse cx="{w * 0.3}" cy="{h * 0.3}" rx="{w * 0.35}" ry="4" {ink(0.08)}/>')
    out += w_birds([(w * 0.2, h * 0.24, 0.8), (w * 0.27, h * 0.2, 0.6)])
    out += wash(uid, f'<path d="M0 {hz - 5} Q{w * 0.3} {hz - 9} {w * 0.6} {hz - 5} T{w} {hz - 6} V{hz + 3} H0Z" {ink(0.16)}/>')
    for i, px in enumerate(range(4, int(w * 0.32), 11)):
        out += w_palm(px, hz + 1, 0.32 + (i % 3) * 0.05, 0.35 + (i % 2) * 0.1)
    for i, tx in enumerate(range(int(w * 0.62), int(w), 10)):
        out += w_tent(tx, hz + 3, 0.36, 0.4 + (i % 2) * 0.1)
    out += (f'<path d="M0 {hz + 3} Q{w * 0.5} {hz} {w} {hz + 3} V{hz + 7} H0Z" fill="{IV}"/>'
            + wash(uid, f'<path d="M0 {hz + 7} Q{w * 0.4} {hz + 4} {w} {hz + 8} V{h + 2} H0Z" {ink(0.26)}/>')
            + f'<rect y="{hz + 7}" width="{w}" height="{h - hz}" fill="url(#h0{uid})" opacity="0.16"/>')
    out += w_alam(w * 0.46, h - 4, (h - 10) / 190, 0.94, wave=1.1)
    if small:
        out += w_waterskin(w * 0.8, h - 6, 0.42)
    return out + grain(uid, w, h)


def euphrates(uid, w, h):
    hz = h * 0.5
    out = (gradient(uid, "eu", [(0, 0.35), (0.5, 0.05)]) + f'<rect width="{w}" height="{h}" fill="{IV}"/>'
           f'<rect width="{w}" height="{hz}" fill="url(#eu{uid})"/>')
    out += w_birds([(w * 0.6, h * 0.18, 0.8), (w * 0.67, h * 0.14, 0.6), (w * 0.72, h * 0.2, 0.5)])
    for i, px in enumerate(range(4, int(w), 12)):
        out += w_palm(px, hz + 2, 0.28 + (i % 4) * 0.05, 0.4 + (i % 3) * 0.12, lean=2 if i % 2 else -2)
    out += (f'<path d="M0 {hz + 2} H{w} V{hz + 26} Q{w * 0.5} {hz + 22} 0 {hz + 27}Z" {ink(0.1)}/>'
            + "".join(f'<path d="M{x} {hz + 6 + (i % 5) * 4} h{6 + i % 3 * 4}" {stroke(0.4, 0.4)}/>'
                      for i, x in enumerate(range(3, int(w), 9))))
    out += wash(uid, f'<path d="M0 {hz + 26} Q{w * 0.5} {hz + 21} {w} {hz + 27} V{h + 2} H0Z" {ink(0.32)}/>')
    out += "".join(f'<path d="M{rx} {h - 2} q{1 + i % 2} -10 {3 + i % 3 * 1.5} -{16 + i % 3 * 5}" {stroke(0.5, 0.75)}/>'
                   f'<ellipse cx="{rx + 3 + i % 3 * 1.5}" cy="{h - 19 - i % 3 * 5}" rx="0.9" ry="2.4" {ink(0.75)}/>'
                   for i, rx in enumerate(range(6, 46, 6)))
    out += w_waterskin(w * 0.72, h - 6, 0.5)
    return out + grain(uid, w, h)


def tents_strip(uid, w, h):
    out = gradient(uid, "ts", [(0, 0.4), (0.8, 0.05)]) + f'<rect width="{w}" height="{h}" fill="{IV}"/><rect width="{w}" height="{h}" fill="url(#ts{uid})"/>'
    for i, px in enumerate(range(int(w * 0.5), int(w * 0.68), 7)):
        out += w_palm(px, h * 0.86, 0.22 + (i % 2) * 0.05, 0.5)
    for i, tx in enumerate(range(int(w * 0.68), int(w) + 6, 8)):
        out += w_tent(tx, h * 0.88, 0.32, 0.6 + (i % 2) * 0.12)
    out += wash(uid, f'<path d="M0 {h * 0.86} Q{w * 0.5} {h * 0.82} {w} {h * 0.87} V{h + 2} H0Z" {ink(0.28)}/>')
    return out + grain(uid, w, h, 0.3)


# ---------------------------------------------------------------- engraving pieces (02)

def e_palm(x, y, s, lean=3):
    fronds = ""
    for ex, ey in ((30, -60), (24, -76), (-26, -60), (-20, -76), (4, -84), (36, -70), (-34, -70)):
        mx, my = (lean + ex) / 2, -80 + (ey + 64) * 0.2 - 4
        fronds += f'<path d="M{lean} -64 Q{mx:.1f} {my:.1f} {ex} {ey}" {stroke(0.8)}/>'
        for t in (0.3, 0.5, 0.7, 0.88):
            px = (1 - t) ** 2 * lean + 2 * (1 - t) * t * mx + t * t * ex
            py = (1 - t) ** 2 * -64 + 2 * (1 - t) * t * my + t * t * ey
            fronds += f'<path d="M{px:.1f} {py:.1f} l{2.6 if ex > 0 else -2.6} 4.2" {stroke(0.45)}/>'
    trunk = "".join(f'<path d="M-1.8 {-yy} l3.6 -1.6" {stroke(0.4)}/>' for yy in range(4, 62, 5))
    return g(x, y, s, f'<path d="M-1.8 0 Q-2.2 -34 {lean - 1} -64 M1.8 0 Q2.2 -34 {lean + 1} -64" {stroke(0.7)}/>{trunk}{fronds}')


def e_sky(uid, w, top, hz):
    """Engraver's sky: fine ruled lines overhead that thin out and stop well above
    the horizon, so the dawn reads as open paper."""
    out, y, gap = "", top, 1.4
    stop = top + (hz - top) * 0.62
    while y < stop:
        a = 0.55 * (1 - (y - top) / (stop - top)) + 0.1
        out += f'<path d="M0 {y:.2f} H{w}" {stroke(0.2, round(a, 2))}/>'
        y += gap
        gap *= 1.09
    return out


def e_rays(cx, hz, w):
    return "".join(f'<path d="M{cx + math.cos(a) * w * 0.12:.1f} {hz - math.sin(a) * w * 0.12:.1f} '
                   f'L{cx + math.cos(a) * w * 0.45:.1f} {hz - math.sin(a) * w * 0.45:.1f}" {stroke(0.2, 0.3)}/>'
                   for a in [math.pi * (0.12 + i * 0.095) for i in range(9)])


def e_medina(x, y, s):
    houses = ""
    for i, (hx, hw, hh) in enumerate(((-60, 16, 12), (-42, 12, 16), (-28, 18, 10), (16, 14, 14), (32, 20, 11), (54, 12, 15))):
        houses += (f'<rect x="{hx}" y="{-hh}" width="{hw}" height="{hh}" fill="{IV}" {outline(0.5)}/>'
                   f'<rect x="{hx + hw * 0.4:.1f}" y="{-hh * 0.6:.1f}" width="2.4" height="3.4" {ink(1)}/>')
    dome = (f'<path d="M-10 -16 C-10 -30 10 -30 10 -16Z" fill="url(#h1U)" {stroke(0.6)}/>'
            f'<rect x="-12" y="-16" width="24" height="16" fill="{IV}" stroke="{INK}" stroke-width="0.5"/>'
            f'<rect x="-1" y="-48" width="2.4" height="32" fill="{IV}" stroke="{INK}" stroke-width="0.5"/>'
            f'<path d="M-2 -48 Q0.2 -56 2.4 -48" {stroke(0.5)}/>')
    return g(x, y, s, houses + f'<g transform="translate(-6 0)">{dome}</g>')


def e_wall(x0, x1, y, hgt, gate_x=None):
    out = f'<rect x="{x0}" y="{y - hgt}" width="{x1 - x0}" height="{hgt}" fill="{IV}" stroke="{INK}" stroke-width="0.6"/>'
    for row in range(1, int(hgt / 2.2)):
        yy = y - hgt + row * 2.2
        out += f'<path d="M{x0} {yy:.1f} H{x1}" {stroke(0.2, 0.6)}/>'
        off = 3 if row % 2 else 0
        out += "".join(f'<path d="M{bx:.1f} {yy:.1f} v-2.2" {stroke(0.2, 0.6)}/>' for bx in range(int(x0) + off, int(x1), 6))
    out += f'<rect x="{x0}" y="{y - hgt - 1.6}" width="{x1 - x0}" height="1.6" fill="{IV}" stroke="{INK}" stroke-width="0.5"/>'
    if gate_x is not None:
        out += (f'<path d="M{gate_x - 6} {y} V{y - hgt + 2} Q{gate_x} {y - hgt - 6} {gate_x + 6} {y - hgt + 2} V{y}Z" '
                f'fill="url(#h1U)" stroke="{INK}" stroke-width="0.6"/>')
    return out


def e_graves(x0, x1, y0, y1, seed=1, n=14):
    """The unmarked graves: low mounds, each with a small upright stone, set
    irregularly and smaller with distance."""
    out, k, pts = "", seed, []
    for i in range(n):
        k = (k * 61 + 17) % 101
        t = (k % 37) / 36
        pts.append((x0 + (x1 - x0) * ((i * 0.618 + k / 101) % 1), y0 + (y1 - y0) * t, 0.55 + t * 0.6))
    for gx, yy, sc in sorted(pts, key=lambda q: q[1]):
        out += (f'<path d="M{gx - 7 * sc:.1f} {yy:.1f} Q{gx:.1f} {yy - 4.4 * sc:.1f} {gx + 7 * sc:.1f} {yy:.1f}Z" fill="{IV}" {outline(0.5)}/>'
                f'<path d="M{gx + 0.5 * sc:.1f} {yy - 3.6 * sc:.1f} Q{gx + 4.5 * sc:.1f} {yy - 2.6 * sc:.1f} {gx + 7 * sc:.1f} {yy:.1f} '
                f'L{gx + 0.5 * sc:.1f} {yy:.1f}Z" fill="url(#h1U)"/>'
                f'<path d="M{gx - 1 * sc:.1f} {yy - 3.4 * sc:.1f} V{yy - 8.4 * sc:.1f} Q{gx:.1f} {yy - 9.6 * sc:.1f} {gx + 1 * sc:.1f} {yy - 8.4 * sc:.1f} '
                f'V{yy - 3.4 * sc:.1f}" fill="{IV}" {outline(0.45)}/>')
    return out


def e_ground(uid, w, y, h):
    """Ground as an engraver leaves it: short strokes, denser toward the viewer."""
    out = ""
    for i in range(int(w / 3.2)):
        k = (i * 37 + 11) % 100 / 100
        yy = y + 2 + (h - y - 4) * (k ** 0.7)
        out += f'<path d="M{(i * 53) % w:.1f} {yy:.1f} h{2 + k * 4:.1f}" {stroke(0.3, round(0.45 + k * 0.4, 2))}/>'
    return out


def baqi_front(uid, w, h):
    hz = h * 0.62
    out = f'<rect width="{w}" height="{h}" fill="{IV}"/>' + e_sky(uid, w, 6, hz - 4) + e_rays(w * 0.62, hz, w * 0.5)
    out += f'<rect x="0" y="{hz - 10}" width="{w}" height="12" fill="{IV}"/>'
    out += e_medina(w * 0.66, hz, 0.7)
    for px, ps, ln in ((w * 0.1, 0.5, -3), (w * 0.2, 0.42, 3), (w * 0.46, 0.46, 2), (w * 0.9, 0.52, -2)):
        out += e_palm(px, hz + 8, ps, ln)
    out += e_wall(0, w, hz + 14, 9, gate_x=w * 0.56)
    out += e_ground(uid, w, hz + 14, h)
    out += e_graves(w * 0.52, w - 8, hz + 22, h - 12, 3, 12)
    return out.replace("url(#h1U)", f"url(#h1{uid})") + grain(uid, w, h, 0.25)


def baqi_print(uid, w, h):
    hz = h * 0.5
    out = f'<rect width="{w}" height="{h}" fill="{IV}"/>' + e_sky(uid, w, 6, hz - 4) + e_rays(w * 0.5, hz, w * 0.7)
    out += e_medina(w * 0.5, hz, 0.8)
    for px, ps, ln in ((w * 0.12, 0.72, -3), (w * 0.26, 0.58, 3), (w * 0.8, 0.66, -2), (w * 0.92, 0.5, 2)):
        out += e_palm(px, hz + 18, ps, ln)
    out += e_wall(0, w, hz + 22, 14, gate_x=w * 0.5)
    out += e_ground(uid, w, hz + 22, h)
    out += e_graves(8, w - 8, hz + 26, h - 12, 5, 30)
    return out.replace("url(#h1U)", f"url(#h1{uid})") + grain(uid, w, h, 0.25)


def road_print(uid, w, h):
    hz = h * 0.56
    out = f'<rect width="{w}" height="{h}" fill="{IV}"/>' + e_sky(uid, w, 6, hz - 2) + e_rays(w * 0.64, hz, w * 0.5)
    out += f'<path d="M0 {hz} Q{w * 0.3} {hz - 6} {w * 0.55} {hz - 2} T{w} {hz - 4}" {stroke(0.6)}/>'
    xl, xr, xf = -w * 0.06, w * 1.06, w * 0.64
    out += e_ground(uid, w, hz + 1, h)
    out += (f'<path d="M{xl} {h + 2} Q{xf - w * 0.2} {hz + (h - hz) * 0.4} {xf - 0.6} {hz} L{xf + 0.6} {hz} '
            f'Q{xf - w * 0.05} {hz + (h - hz) * 0.4} {xr} {h + 2}Z" fill="{IV}" {outline(0.7)}/>')
    out += (f'<path d="M{(xl + xr) / 2:.1f} {h + 2} Q{xf - w * 0.12:.1f} {hz + (h - hz) * 0.4:.1f} {xf} {hz + 1}" '
            f'{stroke(0.9)} stroke-dasharray="{w * 0.04:.1f} {w * 0.035:.1f}"/>')
    for mx, ms in ((w * 0.18, 0.5), (w * 0.4, 0.3)):
        out += g(mx, hz + (h - hz) * (0.7 if ms > 0.4 else 0.35), ms,
                 f'<path d="M-10 0 V-24 Q-10 -34 0 -34 Q10 -34 10 -24 V0Z" fill="{IV}" stroke="{INK}" stroke-width="1"/>'
                 f'<path d="M-10 -24 Q-10 -34 0 -34 Q4 -34 6 -32 Q-2 -26 -2 0 H-10Z" fill="url(#h1{uid})"/>')
    for px, ps in ((w * 0.86, 0.5), (w * 0.94, 0.4)):
        out += e_palm(px, hz + 2, ps)
    return out + grain(uid, w, h, 0.25)


def treaty_still(uid, w, h):
    """The treaty on a low table, a qalam and inkwell beside it — engraved."""
    out = f'<rect width="{w}" height="{h}" fill="{IV}"/>' + e_sky(uid, w, 4, h * 0.6)
    out += f'<rect x="0" y="{h * 0.6}" width="{w}" height="{h * 0.4}" fill="url(#h1{uid})" opacity="0.5"/>'
    out += f'<path d="M{w * 0.08} {h * 0.66} H{w * 0.92} L{w * 0.98} {h * 0.94} H{w * 0.02}Z" fill="{IV}" stroke="{INK}" stroke-width="0.7"/>'
    cx = w * 0.46
    lines = "".join(f'<path d="M{cx - 24} {h * 0.56 + i * 3.6:.1f} H{cx + 24}" {stroke(0.35, 0.8)}/>' for i in range(6))
    out += (f'<path d="M{cx - 30} {h * 0.5} H{cx + 30} V{h * 0.86} H{cx - 30}Z" fill="{IV}" stroke="{INK}" stroke-width="0.7" '
            f'transform="rotate(-4 {cx} {h * 0.7})"/>'
            f'<g transform="rotate(-4 {cx} {h * 0.7})">{lines}'
            f'<circle cx="{cx - 13}" cy="{h * 0.8:.1f}" r="4.2" {ink(1)}/><circle cx="{cx + 13}" cy="{h * 0.8:.1f}" r="4.2" {ink(1)}/>'
            f'<circle cx="{cx - 13}" cy="{h * 0.8:.1f}" r="2.4" fill="none" stroke="{IV}" stroke-width="0.5"/>'
            f'<circle cx="{cx + 13}" cy="{h * 0.8:.1f}" r="2.4" fill="none" stroke="{IV}" stroke-width="0.5"/></g>')
    out += (f'<path d="M{w * 0.74} {h * 0.84} V{h * 0.74} Q{w * 0.74} {h * 0.7} {w * 0.78} {h * 0.7} H{w * 0.82} '
            f'Q{w * 0.86} {h * 0.7} {w * 0.86} {h * 0.74} V{h * 0.84}Z" fill="url(#h1{uid})" stroke="{INK}" stroke-width="0.7"/>'
            f'<path d="M{w * 0.8} {h * 0.71} L{w * 0.9} {h * 0.42}" {stroke(1.1)}/>')
    return out + grain(uid, w, h, 0.25)


def baqi_strip(uid, w, h):
    out = f'<rect width="{w}" height="{h}" fill="{IV}"/>' + e_sky(uid, w, 2, h * 0.7)
    for px, ps in ((w * 0.72, 0.26), (w * 0.84, 0.3), (w * 0.95, 0.24)):
        out += e_palm(px, h * 0.84, ps)
    out += e_wall(w * 0.5, w, h * 0.92, 5)
    return out + grain(uid, w, h, 0.2)


# ---------------------------------------------------------------- dispatch

def render(nn, item, w, h):
    uid = f"{nn}{item.replace('-', '')}"
    table = {
        "01": {"front": karbala_front, "person": karbala_shrine, "event": standard_print,
               "postcard": euphrates, "head": tents_strip},
        "02": {"front": baqi_front, "person": baqi_print, "event": road_print,
               "postcard": treaty_still, "head": baqi_strip},
    }
    fn = table.get(nn, {}).get(item)
    if not fn:
        return None
    return defs(uid) + fn(uid, w, h)


def close_object(nn, x, y):
    """The object set small on face 3."""
    uid = f"{nn}close"
    if nn == "01":
        return defs(uid) + w_bowl(x, y, 1.1, 0.85)
    if nn == "02":
        return (defs(uid) + f'<g transform="rotate(-4 {x} {y - 30})">'
                f'<path d="M{x - 26} {y - 60} H{x + 26} V{y - 4} H{x - 26}Z" fill="{IV}" stroke="{INK}" stroke-width="0.7"/>'
                + "".join(f'<path d="M{x - 20} {y - 52 + i * 5} H{x + 20}" {stroke(0.4, 0.8)}/>' for i in range(7))
                + f'<circle cx="{x - 11}" cy="{y - 12}" r="4" {ink(1)}/><circle cx="{x + 11}" cy="{y - 12}" r="4" {ink(1)}/></g>')
    return None
