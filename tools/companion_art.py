"""The illustration kit for the companions line — Everyone Else.

The box's kit (tools/envelope_art.py) holds no figure, by rule. This line
reverses that rule on purpose (08-companions/README.md, "You can draw their
faces"), so the one thing added here is a person: a parametric portrait in
the same cut-paper language as the box, so the two lines read as one family.

    figure(p, x, y, s, spec)   a person from the waist up, foot of the crop at y

`spec` is a dict (see PEOPLE in tools/companion_themes.py): skin, head
(turban, keffiyeh, hijab, cap, bare), beard, age, clothes, pose (bust, hold,
call, rest) and the prop held. Faces are kept simple — eyes, brows, nose,
cheeks, mouth — friendly rather than cartoon.

Every other drawing here is an object or a backdrop the entries ask for.
Coordinates are millimetres of the box at s=1; a figure stands about 125 high.
"""

import math

import envelope_art as A
from envelope_art import g

INK = "#2A2230"


# ---------------------------------------------------------------- the person

def _head_back(p, sp):
    h, c = sp["head"], sp.get("head_c", "#EDE3D0")
    if h == "keffiyeh":
        return (f'<path d="M-17 -100 C-19 -118 19 -118 17 -100 L23 -64 Q0 -58 -23 -64Z" {p.f(c)}/>')
    if h == "hijab":
        return (f'<path d="M-19 -96 C-21 -121 21 -121 19 -96 L26 -62 Q0 -54 -26 -62Z" {p.f(c)}/>')
    return ""


def _head_front(p, sp):
    h, c, c2 = sp["head"], sp.get("head_c", "#EDE3D0"), sp.get("head_c2", "#C9B79A")
    if h == "turban":
        tail = (f'<path d="M12 -104 Q19 -96 15 -84 Q13 -92 9 -98Z" {p.f(c, False)}/>' if sp.get("tail") else "")
        return (tail + f'<path d="M-16 -97 C-18 -113 -9 -121 0 -121 C9 -121 18 -113 16 -97 Q0 -102 -16 -97Z" {p.f(c)}/>'
                f'<path d="M-15.5 -102.5 Q0 -108 15.5 -102.5 M-13 -110 Q0 -115 13 -110" {p.s(c2, 1.1)}/>'
                f'<path d="M-15.5 -102.5 Q-4 -104 2 -114" {p.s(c2, 0.8)}/>')
    if h == "keffiyeh":
        return (f'<path d="M-16.5 -96 C-18 -115 18 -115 16.5 -96 Q0 -102 -16.5 -96Z" {p.f(c)}/>'
                f'<path d="M-17 -103 Q0 -109 17 -103" {p.s(sp.get("cord", INK), 2.4)}/>'
                f'<path d="M-16.5 -96 L-18 -74 M16.5 -96 L18 -74" {p.s(c2, 0.7)}/>')
    if h == "hijab":
        return (f'<path d="M-14 -97 C-14 -113 14 -113 14 -97" {p.s(c2, 1.4)}/>')
    if h == "cap":
        return f'<path d="M-14.6 -100 Q-14 -114 0 -114 Q14 -114 14.6 -100 Q0 -104 -14.6 -100Z" {p.f(c)}/>'
    hair = sp.get("hair", "#2B211C")
    return f'<path d="M-15 -95 C-16.5 -115 16.5 -115 15 -95 Q12 -106 0 -107 Q-12 -106 -15 -95Z" {p.f(hair, False)}/>'


def _face(p, sp):
    skin, sh = sp["skin"], sp["skin_sh"]
    hijab = sp["head"] == "hijab"
    hair = sp.get("hair", "#2B211C")
    brow = sp.get("brow", hair)
    rx, ry, cy = (12.5, 15, -93) if hijab else (14.5, 17, -94)
    out = ""
    if not hijab:
        out += "".join(f'<ellipse cx="{sx * 14.4}" cy="-93" rx="2.6" ry="4" {p.f(sh, False)}/>' for sx in (-1, 1))
    out += f'<ellipse cx="0" cy="{cy}" rx="{rx}" ry="{ry}" {p.f(skin)}/>'
    # eyes
    if sp.get("eyes") == "closed":
        out += "".join(f'<path d="M{sx * 5.6 - 2.2} -95 Q{sx * 5.6} -93.4 {sx * 5.6 + 2.2} -95" {p.s(INK, 0.9)}/>'
                       for sx in (-1, 1))
    else:
        out += "".join(f'<ellipse cx="{sx * 5.6}" cy="-95" rx="1.5" ry="1.9" {p.f(INK, False)}/>'
                       f'<circle cx="{sx * 5.6 + 0.5}" cy="-95.7" r="0.45" {p.f("#FFFFFF", False)}/>' for sx in (-1, 1))
    # brows
    lift = -1.2 if sp.get("eyes") == "closed" else 0
    out += "".join(f'<path d="M{sx * 2.4} {-99.6 + lift} Q{sx * 5.6} {-101.6 + lift} {sx * 8.8} {-100 + lift}" {p.s(brow, 1.2)}/>'
                   for sx in (-1, 1))
    # nose and cheeks
    out += f'<path d="M0.4 -94 Q-2.2 -88.6 -0.6 -87.2 Q0.8 -86.6 2 -87.4" {p.s(sh, 0.9)}/>'
    out += "".join(f'<circle cx="{sx * 8.4}" cy="-87.6" r="2.7" {p.f(sp.get("cheek", "#E9867A"), False)} opacity="0.32"/>'
                   for sx in (-1, 1))
    if sp.get("age") == "old":
        out += "".join(f'<path d="M{sx * 5.6 - 2} -92.4 Q{sx * 5.6} -91.4 {sx * 5.6 + 2} -92.4" {p.s(sh, 0.5)}/>'
                       f'<path d="M{sx * 10.6} -98 l{sx * 1.6} 1" {p.s(sh, 0.5)}/>' for sx in (-1, 1))
        out += f'<path d="M-5 -104.6 Q0 -105.4 5 -104.6" {p.s(sh, 0.45)}/>'
    return out


def _beard(p, sp):
    b, c = sp.get("beard"), sp.get("beard_c", sp.get("hair", "#2B211C"))
    if not b or b == "none":
        return ""
    chin = {"short": -75, "full": -71, "long": -63}[b]
    side = -93 if b != "short" else -91
    return (f'<path d="M-14.2 {side} Q-15 -80 -8 {chin + 3} Q0 {chin - 2} 8 {chin + 3} Q15 -80 14.2 {side} '
            f'Q12 -84 6 -82.4 Q0 -84.6 -6 -82.4 Q-12 -84 -14.2 {side}Z" {p.f(c, False)}/>'
            f'<path d="M-6.4 -84.2 Q0 -86.8 6.4 -84.2 Q3 -82.6 0 -83.4 Q-3 -82.6 -6.4 -84.2Z" {p.f(c, False)}/>')


def _mouth(p, sp):
    m = sp.get("mouth", "closed")
    if m == "open":
        return (f'<ellipse cx="0" cy="-80.4" rx="2.5" ry="2.4" {p.f("#5A2A2A", False)}/>')
    if m == "smile":
        return f'<path d="M-3.4 -81.2 Q0 -78.4 3.4 -81.2" {p.s("#7A3B34", 1.0)}/>'
    return f'<path d="M-2.8 -80.8 Q0 -79.6 2.8 -80.8" {p.s("#7A3B34", 0.9)}/>'


def _body(p, sp):
    robe, robe2 = sp["robe"], sp.get("robe2", "#F3EAD7")
    out = (f'<path d="M-50 0 C-50 -30 -44 -58 -17 -64 L17 -64 C44 -58 50 -30 50 0Z" {p.f(robe)}/>'
           f'<path d="M-9.5 -64 L0 -47 L9.5 -64Z" {p.f(robe2, False)}/>')
    if sp.get("mantle"):
        m = sp["mantle"]
        out += (f'<path d="M-50 0 C-50 -30 -44 -58 -17 -64 L-6 -60 L-20 0Z" {p.f(m)}/>'
                f'<path d="M50 0 C50 -30 44 -58 17 -64 L6 -60 L20 0Z" {p.f(m)}/>')
    if sp.get("belt"):
        out += f'<path d="M-47 -12 Q0 -6 47 -12 L47 -5 Q0 1 -47 -5Z" {p.f(sp["belt"], False)}/>'
    return out


def _neck(p, sp):
    return f'<path d="M-7 -79 L-7 -61 Q0 -57 7 -61 L7 -79Z" {p.f(sp["skin_sh"], False)}/>'


def shade(hexcol, k=0.82):
    """The same colour, darker — a sleeve has to read against its own robe."""
    if not hexcol.startswith("#"):
        return hexcol
    r, g_, b = (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(c * k))) for c in (r, g_, b))


def _arm(p, sp, x1, y1, x2, y2):
    sleeve = shade(p.c(sp.get("mantle") or sp["robe"]))
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{sleeve}" stroke-width="11" stroke-linecap="round"/>'


def _hand(p, sp, x, y, r=4.6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" {p.f(sp["skin"], False)}/><circle cx="{x}" cy="{y}" r="{r}" {p.s(sp["skin_sh"], 0.6)}/>'


def figure(p, x, y, s, sp):
    pose = sp.get("pose", "bust")
    prop = sp.get("prop")
    out = _head_back(p, sp) + _body(p, sp) + _neck(p, sp) + _face(p, sp) + _beard(p, sp) + _mouth(p, sp) + _head_front(p, sp)
    if pose == "hold":
        # both hands on the thing held; the prop says where its grips are
        draw, (h1, h2) = prop
        out += draw(p, 0, 0, 1.0)
        out += _arm(p, sp, -40, -22, *h1) + _arm(p, sp, 40, -24, *h2)
        out += _hand(p, sp, *h1) + _hand(p, sp, *h2)
    elif pose == "call":
        # right hand raised to the ear, as one calling out does
        out += (_arm(p, sp, 32, -50, 44, -74) + _arm(p, sp, 44, -74, 23, -88)
                + f'<circle cx="44" cy="-74" r="5.5" fill="{shade(p.c(sp["robe"]))}"/>' + _hand(p, sp, 19.5, -90, 5))
        out += sound(p, -22, -86, 0.9, sp.get("sound", "#F2C46D"))
    elif pose == "rest":
        out += _arm(p, sp, -42, -16, -14, -14) + _arm(p, sp, 42, -16, 14, -14)
        out += _hand(p, sp, -10, -14) + _hand(p, sp, 10, -14)
        if prop:
            out += prop(p, 22, -6, 1.0)
    return g(x, y, s, out)


# ---------------------------------------------------------------- objects

def spade(p, x, y, s=1.0):
    """A digging spade standing upright: broad flat blade, a T-grip."""
    return g(x, y, s, f'<path d="M0 -70 V-16" {p.s("trunk", 3.4)}/><path d="M-6 -72 h12" {p.s("trunk", 4)}/>'
                      f'<path d="M-10 -18 H10 L9 -2 Q0 2 -9 -2Z" {p.f("#9AA3A6")}/>')


def seedling(p, x, y, s=1.0):
    """A young date palm in its ball of earth, ready to go in the ground."""
    fr = p.c("frond")
    leaves = "".join(f'<path d="M0 -8 Q{dx * 0.5} {dy * 0.6} {dx} {dy}" fill="none" stroke="{fr}" stroke-width="2.4" stroke-linecap="round"/>'
                     for dx, dy in ((-14, -30), (-6, -38), (4, -40), (13, -33), (18, -22), (-18, -18)))
    return g(x, y, s, leaves + f'<ellipse cx="0" cy="0" rx="10" ry="8.5" {p.f("#8A5A3B")}/>'
                              f'<path d="M-6 -3 Q0 -6 6 -3" {p.s("#6B4430", 0.8)}/>')


def fire(p, x, y, s=1.0):
    """A fire kept burning in a brazier — Salman's father's house."""
    return g(x, y, s, f'<path d="M-16 -10 H16 L12 0 H-12Z" {p.f("#6B4A3A")}/>'
                      f'<path d="M-9 -10 Q-12 -22 -4 -30 Q-4 -22 0 -20 Q2 -32 8 -38 Q8 -26 12 -20 Q14 -14 9 -10Z" {p.f("#E8642C")}/>'
                      f'<path d="M-4 -10 Q-6 -18 0 -24 Q1 -18 4 -16 Q6 -13 4 -10Z" {p.f("#F6C445", False)}/>')


def dates(p, x, y, s=1.0):
    """A hanging bunch of dates."""
    out = f'<path d="M0 -44 Q2 -36 0 -28" {p.s("#C98A2B", 1.6)}/>'
    for i, (dx, dy) in enumerate([(-6, -26), (0, -24), (6, -26), (-9, -18), (-3, -16), (3, -16), (9, -18),
                                   (-6, -9), (0, -8), (6, -9), (-2, -1), (3, -1)]):
        out += f'<ellipse cx="{dx}" cy="{dy}" rx="3.3" ry="4.4" {p.f("#8E3B22" if i % 3 else "#A8502A", False)}/>'
    return g(x, y, s, out)


def road_tile(p, x, y, s=1.0):
    """A road running away to a low sun, in a small rounded window — a sticker."""
    clip = f"rt{abs(hash((x, y))) % 9999}"
    return g(x, y, s, f'<clipPath id="{clip}"><rect x="-28" y="-44" width="56" height="44" rx="6"/></clipPath>'
                      f'<g clip-path="url(#{clip})"><rect x="-28" y="-44" width="56" height="44" {p.f("sky")}/>'
                      f'<circle cx="8" cy="-24" r="7" {p.f("sun", False)}/>'
                      f'<rect x="-28" y="-22" width="56" height="22" {p.f("far")}/>'
                      + A.road(p, None, 2, -22, 6, half=11) + "</g>")


def sun_rays(p, x, y, s=1.0):
    rays = "".join(f'<path d="M{math.cos(a) * 18:.1f} {-24 + math.sin(a) * 18:.1f} L{math.cos(a) * 25:.1f} {-24 + math.sin(a) * 25:.1f}" '
                   f'{p.s("sun", 2.6)}/>' for a in [i * math.pi / 6 for i in range(12)])
    return g(x, y, s, rays + f'<circle cx="0" cy="-24" r="13" {p.f("sun")}/>')


def sound(p, x, y, s=1.0, colour=None):
    """Three arcs of a voice carrying."""
    col = colour or p.c("accent")
    return g(x, y, s, "".join(f'<path d="M{-r * 0.5:.1f} {-r:.1f} Q{-r * 1.1:.1f} 0 {-r * 0.5:.1f} {r:.1f}" fill="none" '
                              f'stroke="{col}" stroke-width="2.2" stroke-linecap="round"/>' for r in (6, 11, 16)))


def sound_sticker(p, x, y, s=1.0):
    return g(x, y, s, f'<circle cx="0" cy="-22" r="22" {p.f("sky")}/>' + sound(p, 8, -22, 1.0, p.c("accent")))


def rooftop(p, x, y, s=1.0):
    """A flat-roofed house with steps up the side — where the call was made."""
    return g(x, y, s, f'<rect x="-24" y="-34" width="48" height="34" {p.f("body")}/>'
                      f'<rect x="-26" y="-38" width="52" height="5" {p.f("tile")}/>'
                      f'<rect x="-6" y="-16" width="12" height="16" rx="6" {p.f("shade", False)}/>'
                      f'<rect x="-18" y="-28" width="7" height="7" {p.f("shade", False)}/>'
                      f'<rect x="11" y="-28" width="7" height="7" {p.f("shade", False)}/>'
                      + "".join(f'<rect x="{24 + i * 4}" y="{-30 + i * 7.5}" width="6" height="{30 - i * 7.5}" {p.f("tile", False)}/>'
                                for i in range(4)))


def coins(p, x, y, s=1.0):
    out = ""
    for i in range(5):
        out += (f'<ellipse cx="{-8 + (i % 2) * 1.5}" cy="{-4 - i * 4.2}" rx="11" ry="3.6" {p.f("gold")}/>'
                f'<path d="M{-19 + (i % 2) * 1.5} {-4 - i * 4.2} v2.6 a11 3.6 0 0 0 22 0 v-2.6" {p.f("#B8862A", False)}/>')
    out += (f'<circle cx="13" cy="-12" r="10" {p.f("gold")}/>' f'<circle cx="13" cy="-12" r="7" {p.s("#B8862A", 0.8)}/>')
    return g(x, y, s, out)


def waterskin(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-6 -40 H6 L7 -34 Q22 -30 22 -14 Q22 0 0 0 Q-22 0 -22 -14 Q-22 -30 -7 -34Z" {p.f("#9A6A44")}/>'
                      f'<path d="M-6 -40 H6 V-44 H-6Z" {p.f("#6B4A3A", False)}/>'
                      f'<path d="M-16 -22 Q0 -14 16 -22" {p.s("#6B4A3A", 0.9)}/>'
                      f'<path d="M-6 -42 Q-24 -46 -26 -20" {p.s("#6B4A3A", 1.2)}/>')


def staff(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M0 -70 Q2 -20 0 40" {p.s("trunk", 3.4)}/>')


def city_gate(p, x, y, s=1.0):
    """A city gate, and a road leading out of it."""
    return g(x, y, s, f'<path d="M-18 6 L-6 -10 H6 L18 6Z" {p.f("road")}/>'
                      f'<rect x="-26" y="-44" width="52" height="34" {p.f("body")}/>'
                      + "".join(f'<rect x="{-26 + i * 9.4}" y="-49" width="5" height="6" {p.f("body", False)}/>' for i in range(6))
                      + f'<path d="M-9 -10 V-28 A9 9 0 0 1 9 -28 V-10Z" {p.f("shade", False)}/>')


def door_plain(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-18" y="-50" width="36" height="50" rx="2" {p.f("#8A5A3B")}/>'
                      f'<path d="M-14 -46 H14 V-27 H-14Z M-14 -23 H14 V-4 H-14Z" fill="none" stroke="#6B4430" stroke-width="1"/>'
                      f'<circle cx="11" cy="-25" r="1.8" {p.f("gold", False)}/>')


def palace(p, x, y, s=1.0):
    """A large new building: wide, arcaded, gilded — money arriving from three continents."""
    arches = "".join(f'<path d="M{-62 + i * 15.5} 0 V-22 Q{-56 + i * 15.5} -32 {-50 + i * 15.5} -22 V0Z" {p.f("shade", False)}/>'
                     for i in range(8))
    crenel = "".join(f'<rect x="{-66 + i * 8.25}" y="-51" width="4.5" height="5" {p.f("body", False)}/>' for i in range(17))
    return g(x, y, s, f'<rect x="-66" y="-46" width="132" height="46" {p.f("body")}/>{crenel}{arches}'
                      f'<rect x="-66" y="-38" width="132" height="3" {p.f("gold", False)}/>'
                      f'<path d="M-20 -46 C-20 -66 20 -66 20 -46Z" {p.f("gold")}/>'
                      f'<rect x="-1.5" y="-70" width="3" height="7" {p.f("gold", False)}/>')


OBJECTS = {
    "spade": lambda p, x, y, s: spade(p, x, y, s * 0.7),
    "fire": fire, "dates": dates, "road_tile": road_tile, "sun_rays": sun_rays, "sound": sound_sticker,
    "rooftop": rooftop, "coins": coins, "waterskin": waterskin, "city_gate": city_gate, "door": door_plain,
    "palm": lambda p, x, y, s: A.palm(p, x, y, s * 0.42),
    "star": lambda p, x, y, s: A.star(p, x, y - 14 * s, 12 * s, "accent"),
    "crescent": lambda p, x, y, s: A.crescent(p, x, y - 16 * s, 14 * s, "accent"),
}

# A prop held in both hands: how to draw it at the figure's origin, and where
# the two hands go on it.
PROPS = {
    "seedling": (lambda p, x, y, s: seedling(p, x + 14, y - 34, s), ((5, -32), (23, -33))),
}


def tent(p, x, y, s=1.0):
    """A low desert tent, its door flap open."""
    return g(x, y, s, f'<path d="M-30 0 L-22 -18 Q0 -24 22 -18 L30 0Z" {p.f("#6B4A3A")}/>'
                      f'<path d="M-22 -18 Q0 -24 22 -18 L18 -22 Q0 -27 -18 -22Z" {p.f("#5A3C2E", False)}/>'
                      f'<path d="M-5 0 L0 -15 L5 0Z" {p.f("#2E2026", False)}/>'
                      f'<path d="M-22 -18 L-26 -24 M22 -18 L26 -24" {p.s("#5A3C2E", 1)}/>')


def parapet(p, w, h, top):
    """The edge of a flat roof, in front of whoever stands on it."""
    merlons = "".join(f'<rect x="{x:.1f}" y="{top - 5:.1f}" width="{w / 18:.1f}" height="6" {p.f("body", False)}/>'
                      for x in [i * w / 9 for i in range(9)])
    return merlons + f'<rect x="0" y="{top:.1f}" width="{w}" height="{h - top + 2:.1f}" {p.f("body")}/>' + \
        f'<rect x="0" y="{top + 4:.1f}" width="{w}" height="1.6" {p.f("tile", False)}/>'


# ---------------------------------------------------------------- places
# A backdrop draws the place behind a person and returns (back, front): front
# is drawn over the figure (a roof edge), or "" when nothing stands in front.

def _ground(p, w, h, y, time, at):
    return A.sky(p, w, h, time, at) + A.dune(p, w, h, y, h * 0.04, "far", 0.1)


def grove(p, w, h, time, at=(0.82, 0.2)):
    back = _ground(p, w, h, h * 0.62, time, at)
    for i, (fx, fy, fs) in enumerate([(0.08, 0.66, 0.28), (0.24, 0.64, 0.22), (0.78, 0.65, 0.26), (0.93, 0.67, 0.3),
                                       (0.62, 0.63, 0.18), (0.38, 0.63, 0.17)]):
        back += A.palm(p, w * fx, h * fy, min(w, h) / 100 * fs * 1.6, lean=3 if i % 2 else -3)
    back += A.dune(p, w, h, h * 0.74, h * 0.03, "mid", -0.1)
    return back, ""


def rooftop_dawn(p, w, h, time, at=(0.8, 0.5)):
    back = A.sky(p, w, h, time, (at[0], at[1], 1.3)) + A.dune(p, w, h, h * 0.6, h * 0.03, "far", 0.2)
    back += A.city(p, w * 0.5, h * 0.62, min(w, h) / 230)
    return back, parapet(p, w, h, h * 0.86)


def palace_back(p, w, h, time, at=(0.86, 0.16)):
    back = _ground(p, w, h, h * 0.6, time, at)
    back += palace(p, w * 0.5, h * 0.66, w / 150)
    back += A.dune(p, w, h, h * 0.72, h * 0.02, "mid", 0.1)
    return back, ""


BACKDROPS = {"grove": grove, "rooftop_dawn": rooftop_dawn, "palace": palace_back}


def three_hundred(p, w, h, time):
    """Rows of young palms going back to the horizon, a spade standing in fresh earth."""
    out = A.sky(p, w, h, time, (0.86, 0.2)) + A.dune(p, w, h, h * 0.44, h * 0.03, "far", 0.1)
    for row in range(5):
        y = h * (0.46 + row * 0.11)
        s = 0.07 + row * 0.045
        n = 9 - row
        for i in range(n):
            x = w * (i + 0.5 + (row % 2) * 0.4) / n
            out += f'<ellipse cx="{x:.1f}" cy="{y + 0.6:.1f}" rx="{14 * s * 1.6:.1f}" ry="{3 * s * 1.6:.1f}" {p.f("#9A6A44", False)}/>'
            out += A.palm(p, x, y, s, lean=2 if i % 2 else -2)
    return out + spade(p, w * 0.86, h * 0.98, 0.55)


def call_over_city(p, w, h, time):
    out = A.sky(p, w, h, time, (0.78, 0.58, 1.4)) + A.dune(p, w, h, h * 0.66, h * 0.03, "far", 0.2)
    out += A.city(p, w * 0.62, h * 0.72, min(w, h) / 220)
    out += A.stars(p, w, h * 0.5, 5, seed=2)
    out += rooftop(p, w * 0.16, h * 1.0, 0.8) + f'<g transform="translate({w * 0.33:.1f} {h * 0.6:.1f}) scale(-1 1)">{sound(p, 0, 0, 1.1, p.c("accent"))}</g>'
    return out


def rabadha(p, w, h, time):
    """Al-Rabadha: a stop on a desert road with almost nobody in it."""
    out = A.sky(p, w, h, time, (0.22, 0.6, 1.4)) + A.dune(p, w, h, h * 0.62, h * 0.03, "far", 0.1)
    out += A.road(p, w, h, h * 0.62, w * 0.6)
    out += tent(p, w * 0.8, h * 0.7, 0.9) + A.dune(p, w, h, h * 0.86, h * 0.03, "mid", -0.2)
    return out


POSTCARDS = {"three_hundred": three_hundred, "call_over_city": call_over_city, "rabadha": rabadha}

OBJECTS.update({"seedling": lambda p, x, y, s: seedling(p, x, y - 8 * s, s * 1.3), "tent": tent})
