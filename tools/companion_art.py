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


def _uid(*parts):
    import hashlib
    return hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:7]


def sky(p, w, h, time, at=(0.2, 0.17)):
    """The box's sky, which now carries its own air (envelope_art.sky)."""
    return A.sky(p, w, h, time, at)


def haze(w, h, y):
    """A pale band of air along the horizon: depth."""
    gid = _uid("haze", w, h, y)
    return (f'<defs><linearGradient id="h{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF8EA" stop-opacity="0"/>'
            f'<stop offset="0.6" stop-color="#FFF8EA" stop-opacity="0.45"/><stop offset="1" stop-color="#FFF8EA" stop-opacity="0"/></linearGradient></defs>'
            f'<rect y="{y - h * 0.08:.1f}" width="{w}" height="{h * 0.12:.1f}" fill="url(#h{gid})"/>')


def tufts(p, w, h, y, n=7, seed=3):
    """Small grass tufts and stones on the near ground."""
    out, x = "", seed * 13.0
    for i in range(n):
        x = (x * 31 + 17) % w
        yy = y + (i % 3) * h * 0.025
        if i % 3 == 0:
            out += f'<ellipse cx="{x:.1f}" cy="{yy:.1f}" rx="{w * 0.012:.1f}" ry="{w * 0.006:.1f}" fill="{p.c("shade")}" opacity="0.18"/>'
        else:
            k = w * 0.008
            out += (f'<path d="M{x:.1f} {yy:.1f} q{-k:.1f} {-2 * k:.1f} {-1.6 * k:.1f} {-2.6 * k:.1f} M{x:.1f} {yy:.1f} q0 {-2.4 * k:.1f} {0.4 * k:.1f} {-3.2 * k:.1f} '
                    f'M{x:.1f} {yy:.1f} q{k:.1f} {-1.8 * k:.1f} {1.8 * k:.1f} {-2.4 * k:.1f}" fill="none" stroke="{p.c("frond")}" '
                    f'stroke-width="{k * 0.5:.2f}" stroke-linecap="round" opacity="0.7"/>')
    return out


GRAIN = ('<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.6" '
         'numOctaves="2" seed="4" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 0.16  0 0 0 0 0.13  '
         '0 0 0 0 0.19  0 0 0 1.1 -0.42"/></filter>')


def grain(w, h, op=0.38):
    """Printed-paper grain over a whole picture."""
    return f'<defs>{GRAIN}</defs><rect width="{w}" height="{h}" filter="url(#grain)" opacity="{op}"/>'


# ---------------------------------------------------------------- the person

def _head_back(p, sp):
    h, c = sp["head"], sp.get("head_c", "#EDE3D0")
    if h == "keffiyeh":
        return (f'<path d="M-17 -100 C-19 -118 19 -118 17 -100 L23 -64 Q0 -58 -23 -64Z" {p.f(c)}/>')
    if h in ("hijab", "helmet"):
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
    if h == "helmet":
        # a rider's mail hood with a plain round cap over it
        return (f'<path d="M-14 -97 C-14 -113 14 -113 14 -97" {p.s(c2, 1.4)}/>'
                f'<path d="M-17 -101 C-17 -122 17 -122 17 -101 Q0 -106 -17 -101Z" {p.f(sp.get("cap_c", "#8E9496"))}/>'
                f'<path d="M0 -121 V-103" {p.s("#6E7476", 0.8)}/>')
    if h == "cap":
        return f'<path d="M-14.6 -100 Q-14 -114 0 -114 Q14 -114 14.6 -100 Q0 -104 -14.6 -100Z" {p.f(c)}/>'
    hair = sp.get("hair", "#2B211C")
    return f'<path d="M-15 -95 C-16.5 -115 16.5 -115 15 -95 Q12 -106 0 -107 Q-12 -106 -15 -95Z" {p.f(hair, False)}/>'


def _veiled(p, sp):
    """The face veiled in light — the convention of devotional art for the
    family of the Fourteen. No features: a warm light where the face would be."""
    hijab = sp["head"] in ("hijab", "helmet")
    rx, ry, cy = (12.5, 15, -93) if hijab else (14.5, 17, -94)
    return (f'<defs><radialGradient id="veil" cx="50%" cy="45%" r="55%">'
            f'<stop offset="0" stop-color="#FFFBEA"/><stop offset="0.55" stop-color="#FCEBB8"/>'
            f'<stop offset="1" stop-color="#F2C46D"/></radialGradient></defs>'
            f'<ellipse cx="0" cy="{cy}" rx="{rx + 5}" ry="{ry + 5}" fill="#F7D88A" opacity="0.35"/>'
            f'<ellipse cx="0" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#veil)"/>')


def _face(p, sp):
    if sp.get("face") == "light":
        return _veiled(p, sp)
    skin, sh = sp["skin"], sp["skin_sh"]
    hijab = sp["head"] in ("hijab", "helmet")
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
        gz = sp.get("gaze", 0)
        out += "".join(f'<ellipse cx="{sx * 5.6 + gz}" cy="-95" rx="1.5" ry="1.9" {p.f(INK, False)}/>'
                       f'<circle cx="{sx * 5.6 + gz + 0.5}" cy="-95.7" r="0.45" {p.f("#FFFFFF", False)}/>' for sx in (-1, 1))
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
    if not b or b == "none" or sp.get("face") == "light":
        return ""
    chin = {"short": -75, "full": -71, "long": -63}[b]
    side = -93 if b != "short" else -91
    return (f'<path d="M-14.2 {side} Q-15 -80 -8 {chin + 3} Q0 {chin - 2} 8 {chin + 3} Q15 -80 14.2 {side} '
            f'Q12 -84 6 -82.4 Q0 -84.6 -6 -82.4 Q-12 -84 -14.2 {side}Z" {p.f(c, False)}/>'
            f'<path d="M-6.4 -84.2 Q0 -86.8 6.4 -84.2 Q3 -82.6 0 -83.4 Q-3 -82.6 -6.4 -84.2Z" {p.f(c, False)}/>')


def _mouth(p, sp):
    if sp.get("face") == "light":
        return ""
    m = sp.get("mouth", "closed")
    if m == "open":
        return (f'<ellipse cx="0" cy="-80.4" rx="2.5" ry="2.4" {p.f("#5A2A2A", False)}/>')
    if m == "smile":
        return f'<path d="M-3.4 -81.2 Q0 -78.4 3.4 -81.2" {p.s("#7A3B34", 1.0)}/>'
    return (f'<path d="M-3 -80.9 Q0 -79.2 3 -80.9 Q0 -82.2 -3 -80.9Z" fill="#9A5A4A" opacity="0.75"/>'
            f'<path d="M-2.8 -80.8 Q0 -79.6 2.8 -80.8" {p.s("#7A3B34", 0.6)}/>')


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
    if sp.get("face") == "light" and sp["head"] not in ("hijab", "helmet"):
        return f'<path d="M-7 -79 L-7 -61 Q0 -57 7 -61 L7 -79Z" fill="#F6E2B0"/>'
    if sp["head"] in ("hijab", "helmet"):
        # the scarf wraps under the chin and covers the neck
        return f'<path d="M-12 -84 Q0 -72 12 -84 L15 -60 Q0 -54 -15 -60Z" {p.f(sp.get("head_c", "#EDE3D0"), False)}/>'
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


def _form(p, sp):
    """Light from the left: shadow down the right of the robe, folds, a rim of
    light on the left shoulder, embroidered trim at the neck."""
    robe = p.c(sp.get("mantle") or sp["robe"])
    trim = sp.get("trim", "#E8C15A")
    return (f'<path d="M8 -63 C32 -56 47 -36 50 0 L16 0 C22 -24 18 -46 8 -63Z" fill="#1A1424" opacity="0.16"/>'
            f'<path d="M-30 -44 Q-25 -22 -31 0 M-14 -40 Q-10 -20 -15 0 M26 -46 Q21 -22 27 0" fill="none" '
            f'stroke="{shade(robe, 0.7)}" stroke-width="1.1" stroke-linecap="round" opacity="0.55"/>'
            f'<path d="M-49 -4 C-49 -32 -43 -57 -17 -63.5" fill="none" stroke="#FFF6E0" stroke-width="1.3" opacity="0.45"/>'
            f'<path d="M-9.5 -64 L0 -47 L9.5 -64" fill="none" stroke="{trim}" stroke-width="1.5" stroke-dasharray="0.1 2.2" '
            f'stroke-linecap="round"/>'
            f'<path d="M-11.5 -64.5 L0 -44.5 L11.5 -64.5" fill="none" stroke="{trim}" stroke-width="0.5" opacity="0.8"/>')


def _face_light(p, sp):
    """The shadow side of a drawn face, lids and lips: the face turned to the light."""
    if sp.get("face") == "light":
        return ""
    hijab = sp["head"] in ("hijab", "helmet")
    sh = sp["skin_sh"]
    side = ('M3 -107 Q14 -104 12.5 -92 Q11.5 -81 3 -78.5 Q9.5 -92 3 -107Z' if hijab
            else 'M4 -110 Q16 -106 14.5 -92 Q13 -80 4 -77 Q11 -92 4 -110Z')
    lids = "".join(f'<path d="M{sx * 5.6 - 2.1} -96.4 Q{sx * 5.6} -98 {sx * 5.6 + 2.1} -96.4" fill="none" stroke="{INK}" '
                   f'stroke-width="0.55" opacity="0.7"/>' for sx in (-1, 1)) if sp.get("eyes") != "closed" else ""
    return (f'<path d="{side}" fill="{sh}" opacity="0.5"/>{lids}'
            f'<ellipse cx="-4" cy="-101" rx="5" ry="2.2" fill="#FFF6E8" opacity="0.18"/>'
            f'<path d="M-1.6 -86 Q0.4 -85 2.2 -86.4" fill="none" stroke="{sh}" stroke-width="0.6" opacity="0.7"/>')


def _cloth(p, sp):
    """Folds and a shadow side on a scarf or headcloth."""
    if sp["head"] not in ("hijab", "keffiyeh", "helmet"):
        return ""
    c = p.c(sp.get("head_c", "#EDE3D0"))
    return (f'<path d="M-21 -84 Q-23 -72 -25 -63 M21 -84 Q23 -72 25 -63 M-17 -100 Q-20 -88 -19 -80" fill="none" '
            f'stroke="{shade(c, 0.72)}" stroke-width="0.9" stroke-linecap="round" opacity="0.7"/>'
            f'<path d="M14 -108 Q22 -98 21 -86 L25 -63 Q20 -61 17 -61 L15 -84 Q17 -98 10 -110Z" fill="#1A1424" opacity="0.12"/>')


def figure(p, x, y, s, sp):
    pose = sp.get("pose", "bust")
    prop = sp.get("prop")
    tilt = sp.get("tilt", 0)
    rot = f'<g transform="rotate({tilt} 0 -72)">' if tilt else "<g>"
    out = (rot + _head_back(p, sp) + "</g>" + _body(p, sp) + _form(p, sp) + _neck(p, sp)
           + rot + _cloth(p, sp) + _face(p, sp) + _face_light(p, sp) + _beard(p, sp) + _mouth(p, sp) + _head_front(p, sp) + "</g>")
    if pose == "hold":
        # the prop says where the hands go on it; a grip of None leaves that arm at rest
        draw, (h1, h2) = prop
        out += draw(p, 0, 0, 1.0)
        out += (_arm(p, sp, -40, -22, *h1) if h1 else "") + (_arm(p, sp, 40, -24, *h2) if h2 else "")
        out += (_hand(p, sp, *h1) if h1 else "") + (_hand(p, sp, *h2) if h2 else "")
    elif pose == "call":
        # right hand raised to the ear, as one calling out does
        out += (_arm(p, sp, 32, -50, 44, -74) + _arm(p, sp, 44, -74, 23, -88)
                + f'<circle cx="44" cy="-74" r="5.5" fill="{shade(p.c(sp["robe"]))}"/>' + _hand(p, sp, 19.5, -90, 5))
        out += sound(p, -22, -86, 0.9, sp.get("sound", "#F2C46D"))
    elif pose == "raise":
        # one hand raised a little, open, as when reciting
        out += (_arm(p, sp, 34, -40, 46, -52) + _arm(p, sp, 46, -52, 38, -74)
                + f'<circle cx="46" cy="-52" r="5.5" fill="{shade(p.c(sp.get("mantle") or sp["robe"]))}"/>'
                + f'<ellipse cx="37" cy="-79" rx="4.6" ry="6" {p.f(sp["skin"], False)}/>')
    elif pose == "rest":
        out += _arm(p, sp, -42, -16, -14, -14) + _arm(p, sp, 42, -16, 14, -14)
        out += _hand(p, sp, -10, -14) + _hand(p, sp, 10, -14)
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
    return sky(p, w, h, time, at) + A.dune(p, w, h, y, h * 0.04, "far", 0.1)


def grove(p, w, h, time, at=(0.82, 0.2)):
    back = _ground(p, w, h, h * 0.62, time, at)
    for i, (fx, fy, fs) in enumerate([(0.08, 0.66, 0.28), (0.24, 0.64, 0.22), (0.78, 0.65, 0.26), (0.93, 0.67, 0.3),
                                       (0.62, 0.63, 0.18), (0.38, 0.63, 0.17)]):
        back += A.palm(p, w * fx, h * fy, min(w, h) / 100 * fs * 1.6, lean=3 if i % 2 else -3)
    back += A.dune(p, w, h, h * 0.74, h * 0.03, "mid", -0.1)
    return back, ""


def rooftop_dawn(p, w, h, time, at=(0.8, 0.5)):
    back = sky(p, w, h, time, (at[0], at[1], 1.3)) + A.dune(p, w, h, h * 0.6, h * 0.03, "far", 0.2)
    back += A.city(p, w * 0.5, h * 0.62, min(w, h) / 230)
    return back, parapet(p, w, h, h * 0.86)


def palace_back(p, w, h, time, at=(0.86, 0.16)):
    back = _ground(p, w, h, h * 0.6, time, at)
    back += palace(p, w * 0.5, h * 0.66, w / 150)
    back += A.dune(p, w, h, h * 0.72, h * 0.02, "mid", 0.1)
    return back, ""


BACKDROPS = {"grove": grove, "rooftop_dawn": rooftop_dawn, "palace": palace_back,
             "fitrus": lambda p, w, h, time, at=None: fitrus_place(p, w, h, time, at)}


def three_hundred(p, w, h, time):
    """Rows of young palms going back to the horizon, a spade standing in fresh earth."""
    out = sky(p, w, h, time, (0.86, 0.2)) + A.dune(p, w, h, h * 0.44, h * 0.03, "far", 0.1)
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
    out = sky(p, w, h, time, (0.78, 0.58, 1.4)) + A.dune(p, w, h, h * 0.66, h * 0.03, "far", 0.2)
    out += A.city(p, w * 0.62, h * 0.72, min(w, h) / 220)
    out += A.stars(p, w, h * 0.5, 5, seed=2)
    out += rooftop(p, w * 0.16, h * 1.0, 0.8) + f'<g transform="translate({w * 0.33:.1f} {h * 0.6:.1f}) scale(-1 1)">{sound(p, 0, 0, 1.1, p.c("accent"))}</g>'
    return out


def rabadha(p, w, h, time):
    """Al-Rabadha: a stop on a desert road with almost nobody in it."""
    out = sky(p, w, h, time, (0.22, 0.6, 1.4)) + A.dune(p, w, h, h * 0.62, h * 0.03, "far", 0.1)
    out += A.road(p, w, h, h * 0.62, w * 0.6)
    out += tent(p, w * 0.8, h * 0.7, 0.9) + A.dune(p, w, h, h * 0.86, h * 0.03, "mid", -0.2)
    return out


POSTCARDS = {"three_hundred": three_hundred, "call_over_city": call_over_city, "rabadha": rabadha}

OBJECTS.update({"seedling": lambda p, x, y, s: seedling(p, x, y - 8 * s, s * 1.3), "tent": tent})


# ---------------------------------------------------------------- more objects
# Everything the thirty-nine sticker specs ask for. Each draws with its foot at
# (x, y), about 40–50 high at s=1, so a sticker sheet can place any of them.

PAPER = "#FFF8EA"


def basket(p, x, y, s=1.0):
    weave = "".join(f'<path d="M{-18 + i * 6} -20 L{-15 + i * 6} 0" {p.s("#8A5A2E", 0.8)}/>' for i in range(7))
    return g(x, y, s, f'<path d="M-22 -22 H22 L17 0 H-17Z" {p.f("#C98E4A")}/>{weave}'
                      f'<path d="M-20 -14 H20 M-19 -7 H19" {p.s("#8A5A2E", 0.8)}/>'
                      f'<path d="M-14 -22 Q0 -42 14 -22" {p.s("#8A5A2E", 2)}/>')


def sandal(p, x, y, s=1.0, key="#9A6A44"):
    return g(x, y, s, f'<path d="M-8 0 Q-12 -20 -6 -34 Q0 -40 6 -34 Q12 -20 8 0 Q0 4 -8 0Z" {p.f(key)}/>'
                      f'<path d="M-8 -24 Q0 -18 8 -24 M-7 -12 Q0 -7 7 -12" {p.s("#5A3C2E", 2)}/>')


def folded_cloth(p, x, y, s=1.0, key=None):
    c = p.c(key or "accent")
    return g(x, y, s, f'<path d="M-24 0 H24 V-10 H-24Z" {p.f(c)}/><path d="M-22 -10 H22 V-19 H-22Z" fill="{shade(c, 0.88)}"/>'
                      f'<path d="M-20 -19 H20 V-27 H-20Z" fill="{shade(c, 0.76)}"/>'
                      f'<path d="M-24 -5 H24 M-22 -14.5 H22" {p.s("#FFF8EA", 0.6)}/>')


def oil_lamp(p, x, y, s=1.0):
    """A small clay lamp with its flame."""
    return g(x, y, s, f'<path d="M-18 -8 Q-18 0 0 0 Q18 0 22 -10 L30 -14 Q22 -16 16 -14 Q0 -18 -18 -8Z" {p.f("#B5683A")}/>'
                      f'<path d="M-24 -10 Q-28 -4 -18 -4" {p.s("#8A4A2A", 2)}/>'
                      f'<path d="M29 -15 Q24 -26 30 -34 Q36 -24 31 -15Z" {p.f("#F2B53B", False)}/>'
                      f'<path d="M30 -16 Q28 -22 30 -26 Q33 -21 31 -16Z" {p.f("#FFF1C2", False)}/>')


def open_book(p, x, y, s=1.0):
    lines = "".join(f'<path d="M{a} {yy} H{b}" {p.s("#B9A98E", 0.7)}/>' for yy in (-26, -21, -16, -11)
                    for a, b in ((-24, -5), (5, 24)))
    return g(x, y, s, f'<path d="M0 -4 Q-14 -10 -30 -6 V-34 Q-14 -38 0 -32Z" {p.f(PAPER)}/>'
                      f'<path d="M0 -4 Q14 -10 30 -6 V-34 Q14 -38 0 -32Z" {p.f(PAPER)}/>'
                      f'<path d="M0 -32 V-4" {p.s("#B9A98E", 0.9)}/>{lines}'
                      f'<path d="M-32 -4 Q-14 -8 0 -1 Q14 -8 32 -4 V0 Q14 -4 0 3 Q-14 -4 -32 0Z" {p.f("accent")}/>')


def jug(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-8 -40 H8 L6 -34 Q20 -26 18 -10 Q16 0 0 0 Q-16 0 -18 -10 Q-20 -26 -6 -34Z" {p.f("#C77A44")}/>'
                      f'<path d="M14 -30 Q26 -28 18 -14" {p.s("#9A5530", 2.4)}/>'
                      f'<path d="M-14 -18 Q0 -12 14 -18" {p.s("#9A5530", 1)}/>')


def broom(p, x, y, s=1.0):
    bristle = "".join(f'<path d="M0 -16 L{dx} 0" {p.s("#C8A35A", 1.2)}/>' for dx in range(-12, 13, 3))
    return g(x, y, s, f'<path d="M0 -60 V-16" {p.s("#8A5A3B", 2.6)}/>{bristle}'
                      f'<path d="M-6 -16 H6" {p.s("#8A4A2A", 2.4)}/>')


def scales_small(p, x, y, s=1.0):
    return A.scales(p, x, y, s * 0.8)


def awning(p, x, y, s=1.0):
    """A market stall: a striped awning on two poles over a counter of baskets."""
    stripes = "".join(f'<path d="M{-30 + i * 10} -48 H{-20 + i * 10} L{-20 + i * 10} -36 Q{-25 + i * 10} -31 {-30 + i * 10} -36Z" '
                      f'{p.f("accent" if i % 2 == 0 else PAPER, False)}/>' for i in range(6))
    return g(x, y, s, f'<path d="M-28 -36 V0 M28 -36 V0" {p.s("trunk", 2)}/>{stripes}'
                      f'<rect x="-32" y="-14" width="64" height="14" {p.f("#B07A4A")}/>'
                      + "".join(f'<ellipse cx="{bx}" cy="-15" rx="7" ry="3.4" {p.f("#7E3A22", False)}/>' for bx in (-18, 0, 18)))


def shirt(p, x, y, s=1.0, key=None):
    c = p.c(key or "accent")
    return g(x, y, s, f'<path d="M-10 -40 L-26 -32 L-20 -20 L-14 -24 V0 H14 V-24 L20 -20 L26 -32 L10 -40 Q0 -34 -10 -40Z" '
                      f'fill="{c}"/><path d="M-10 -40 Q0 -30 10 -40" {p.s(shade(c, 0.7), 1)}/>')


def two_shirts(p, x, y, s=1.0):
    return shirt(p, x - 9 * s, y, s * 0.85, "#E3A33B") + shirt(p, x + 10 * s, y + 2 * s, s * 0.85, "#C9C2B2")


def flag(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-14 0 V-48" {p.s("trunk", 2.4)}/>'
                      f'<path d="M-14 -48 Q2 -54 16 -46 Q8 -40 16 -32 Q2 -38 -14 -32Z" {p.f("accent")}/>')


def river_tile(p, x, y, s=1.0):
    reeds = "".join(f'<path d="M{rx} 0 Q{rx + 2} -12 {rx + 4} -20" {p.s("frond", 1.6)}/>' for rx in (-22, -18, 16, 20))
    return g(x, y, s, f'<path d="M-28 -14 Q-14 -18 0 -14 T28 -14 V0 H-28Z" {p.f("water")}/>'
                      f'<path d="M-22 -8 Q-12 -11 -2 -8 M4 -6 Q14 -9 22 -6" {p.s(PAPER, 1)}/>{reeds}')


def milestone(p, x, y, s=1.0):
    """A road marker stone."""
    return g(x, y, s, f'<path d="M-12 0 V-28 Q-12 -40 0 -40 Q12 -40 12 -28 V0Z" {p.f("#C9BBA2")}/>'
                      f'<path d="M-6 -24 H6 M-6 -18 H6" {p.s("#8E826E", 1.4)}/>'
                      f'<path d="M-20 0 H20" {p.s("#8E826E", 1.6)}/>')


def flower(p, x, y, s=1.0):
    petals = "".join(f'<ellipse cx="0" cy="-40" rx="4.6" ry="8" fill="{p.c("accent")}" transform="rotate({a} 0 -32)"/>'
                     for a in range(0, 360, 60))
    return g(x, y, s, f'<path d="M0 0 Q2 -14 0 -30" {p.s("frond", 2)}/>'
                      f'<path d="M1 -14 Q10 -20 12 -14 Q6 -10 1 -14Z" {p.f("frond", False)}/>{petals}'
                      f'<circle cx="0" cy="-32" r="4" {p.f("sun", False)}/>')


def feather(p, x, y, s=1.0, key="#FFF8EA"):
    """A single long feather — Fitrus, standing in for the figure."""
    vanes = "".join(f'<path d="M0 {yy} Q{-10 - (yy + 60) * 0.0} {yy - 8} -15 {yy - 18}" {p.s("#D9CDB4", 0.6)}/>'
                    f'<path d="M0 {yy} Q10 {yy - 8} 15 {yy - 18}" {p.s("#D9CDB4", 0.6)}/>' for yy in range(-14, -96, -8))
    return g(x, y, s, f'<path d="M0 0 Q-24 -40 -6 -110 Q4 -118 8 -108 Q24 -40 0 0Z" fill="{key}"/>{vanes}'
                      f'<path d="M0 6 Q1 -50 1 -112" {p.s("#C8B48F", 1.2)}/>')


def bird(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-24 -20 Q-12 -32 0 -18 Q12 -32 24 -20 Q12 -24 0 -12 Q-12 -24 -24 -20Z" {p.f("accent")}/>')


def hand_open(p, x, y, s=1.0, key=None):
    c = p.c(key or "#D9A47E")
    fingers = "".join(f'<rect x="{fx - 2.6}" y="{-46 + abs(fx) * 0.5}" width="5.2" height="20" rx="2.6" fill="{c}"/>'
                      for fx in (-9, -3, 3, 9))
    return g(x, y, s, fingers + f'<path d="M-12 -28 H12 V-8 Q12 0 0 0 Q-12 0 -12 -8Z" fill="{c}"/>'
                      f'<rect x="-22" y="-30" width="5.2" height="16" rx="2.6" fill="{c}" transform="rotate(-40 -19 -22)"/>')


def plain_scroll(p, x, y, s=1.0):
    lines = "".join(f'<path d="M-18 {yy} H18" {p.s("#B9A98E", 0.9)}/>' for yy in (-36, -30, -24, -18))
    return g(x, y, s, f'<rect x="-22" y="-44" width="44" height="34" {p.f(PAPER)}/>{lines}'
                      f'<rect x="-26" y="-48" width="52" height="6" rx="3" {p.f("tile")}/>'
                      f'<rect x="-26" y="-12" width="52" height="6" rx="3" {p.f("tile")}/>')


def inkwell(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-12 0 V-14 Q-12 -20 -6 -20 H6 Q12 -20 12 -14 V0Z" {p.f("#2E3A55")}/>'
                      f'<rect x="-5" y="-24" width="10" height="5" {p.f("#1E2638", False)}/>'
                      f'<path d="M2 -22 L20 -50" {p.s("#C98E4A", 2)}/>')


def ship_wheel(p, x, y, s=1.0):
    spokes = "".join(f'<path d="M{math.cos(a) * 6:.1f} {-22 + math.sin(a) * 6:.1f} L{math.cos(a) * 24:.1f} {-22 + math.sin(a) * 24:.1f}" '
                     f'{p.s("#8A5A3B", 3)}/>' for a in [i * math.pi / 4 for i in range(8)])
    return g(x, y, s, spokes + f'<circle cx="0" cy="-22" r="16" fill="none" stroke="{p.c("#A86E44")}" stroke-width="4"/>'
                              f'<circle cx="0" cy="-22" r="5" {p.f("#8A5A3B", False)}/>')


def crate(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-20" y="-34" width="40" height="34" {p.f("#C08A52")}/>'
                      f'<path d="M-20 -34 L20 0 M-20 0 L20 -34" {p.s("#8A5A30", 2)}/>'
                      f'<rect x="-20" y="-34" width="40" height="34" fill="none" stroke="{p.c("#8A5A30")}" stroke-width="2.4"/>')


def rope(p, x, y, s=1.0):
    return g(x, y, s, "".join(f'<ellipse cx="0" cy="{-8 - i * 4}" rx="{20 - i * 2.6}" ry="{6 - i * 0.6}" fill="none" '
                              f'stroke="{p.c("#C9A46A")}" stroke-width="3"/>' for i in range(5))
             + f'<path d="M18 -8 Q30 -4 28 6" {p.s("#C9A46A", 3)}/>')


def parcel(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-22 0 V-26 Q0 -32 22 -26 V0Z" {p.f("#D9C3A0")}/>'
                      f'<path d="M0 -30 V0 M-22 -13 Q0 -18 22 -13" {p.s("#9A5530", 2)}/>'
                      f'<path d="M0 -30 Q-8 -40 -10 -34 Q-6 -30 0 -30 Q8 -40 10 -34 Q6 -30 0 -30Z" {p.f("#9A5530", False)}/>')


def satchel(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-18 -26 Q-14 -54 0 -54 Q14 -54 18 -26" {p.s("#7A4E30", 2.4)}/>'
                      f'<rect x="-22" y="-28" width="44" height="28" rx="4" {p.f("#9A6A44")}/>'
                      f'<path d="M-22 -28 H22 V-14 Q0 -8 -22 -14Z" {p.f("#7A4E30", False)}/>'
                      f'<rect x="-3" y="-16" width="6" height="7" rx="1" {p.f("gold", False)}/>')


def oil_jar(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-7 -44 H7 L6 -38 Q20 -32 20 -16 Q20 0 0 0 Q-20 0 -20 -16 Q-20 -32 -6 -38Z" {p.f("#B5683A")}/>'
                      f'<path d="M-9 -46 H9" {p.s("#8A4A2A", 3)}/><path d="M-16 -22 Q0 -16 16 -22" {p.s("#E3B26A", 1.6)}/>')


def chest(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-24" y="-26" width="48" height="26" {p.f("#8A5A3B")}/>'
                      f'<path d="M-24 -26 Q0 -40 24 -26Z" {p.f("#A06A44")}/>'
                      f'<path d="M-24 -18 H24" {p.s("#5A3A26", 1.4)}/>'
                      f'<rect x="-5" y="-22" width="10" height="11" rx="1.4" {p.f("gold")}/>'
                      f'<circle cx="0" cy="-17" r="1.6" {p.f("#5A3A26", False)}/>')


def helmet(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-20 -8 Q-22 -42 0 -44 Q22 -42 20 -8Z" {p.f("#9AA0A2")}/>'
                      f'<path d="M-20 -8 H20 V0 H-20Z" {p.f("#7E8486")}/>'
                      f'<path d="M0 -44 V-52" {p.s("#7E8486", 2.4)}/><path d="M-3 -16 H3 V0 H-3Z" {p.f("#7E8486", False)}/>')


def reins(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-24 -10 Q-10 -40 6 -30 Q20 -20 24 -38" {p.s("#7A4E30", 2.6)}/>'
                      f'<circle cx="-24" cy="-10" r="4" fill="none" stroke="{p.c("#B0B6B8")}" stroke-width="2"/>'
                      f'<circle cx="24" cy="-38" r="4" fill="none" stroke="{p.c("#B0B6B8")}" stroke-width="2"/>')


def round_shield(p, x, y, s=1.0):
    return g(x, y, s, f'<circle cx="0" cy="-22" r="22" {p.f("#A86E44")}/>'
                      f'<circle cx="0" cy="-22" r="16" fill="none" stroke="{p.c("#8A5530")}" stroke-width="1.6"/>'
                      f'<circle cx="0" cy="-22" r="5" {p.f("#C9C2B2", False)}/>')


def scabbard(p, x, y, s=1.0):
    """A sword in its scabbard, never drawn."""
    return g(x, y, s, f'<path d="M-30 -6 L26 -34 L30 -28 L-26 0Z" {p.f("#6B4A3A")}/>'
                      f'<path d="M26 -34 L34 -38 M30 -28 L36 -32" {p.s("#C9A04A", 2)}/>'
                      f'<path d="M34 -40 L42 -44" {p.s("#5A3A26", 3.4)}/><circle cx="44" cy="-45" r="2.6" {p.f("gold", False)}/>'
                      f'<path d="M-30 -6 L-26 0" {p.s("#C9A04A", 2.4)}/>')


def harness(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-20 -8 Q-24 -40 0 -42 Q24 -40 20 -8" {p.s("#9A5530", 3.4)}/>'
                      f'<path d="M-22 -24 H22" {p.s("#9A5530", 3)}/>'
                      + "".join(f'<circle cx="{cx}" cy="-24" r="2.6" {p.f("gold", False)}/>' for cx in (-12, 0, 12))
                      + f'<path d="M0 -8 V2" {p.s("#9A5530", 2)}/><circle cx="0" cy="4" r="3" {p.f("gold", False)}/>')


def tether(p, x, y, s=1.0):
    """An empty tether line between two posts — no camels on it."""
    return g(x, y, s, f'<path d="M-28 0 V-30 M28 0 V-30" {p.s("trunk", 3)}/>'
                      f'<path d="M-28 -26 Q0 -14 28 -26" {p.s("#C9A46A", 2)}/>'
                      + "".join(f'<path d="M{rx} -21 v7" {p.s("#C9A46A", 1.4)}/>' for rx in (-14, 0, 14)))


def seat_circle(p, x, y, s=1.0):
    return g(x, y, s, "".join(f'<circle cx="{math.cos(a) * 20:.1f}" cy="{-22 + math.sin(a) * 12:.1f}" r="5.4" {p.f("accent")}/>'
                              for a in [i * math.pi / 3.5 for i in range(7)])
             + f'<ellipse cx="0" cy="-22" rx="11" ry="5" {p.f("tile", False)}/>')


def star_field(p, x, y, s=1.0):
    clip = f"sf{abs(hash((round(x, 1), round(y, 1)))) % 9999}"
    stars_ = "".join(A.star(p, sx, sy, r, "sun") for sx, sy, r in ((-16, -34, 2.4), (6, -38, 1.6), (16, -24, 2.8), (-6, -18, 1.8), (-18, -10, 1.4)))
    return g(x, y, s, f'<rect x="-26" y="-46" width="52" height="46" rx="6" {p.f("#26244A")}/>{stars_}')


def marks_four(p, x, y, s=1.0):
    return g(x, y, s, "".join(f'<rect x="{-22 + i * 12}" y="-26" width="7" height="26" rx="3.5" {p.f("accent")}/>' for i in range(4)))


def shared_meal(p, x, y, s=1.0):
    return g(x, y, s, f'<ellipse cx="0" cy="-4" rx="30" ry="7" {p.f("#C9A46A")}/>'
                      f'<ellipse cx="-10" cy="-10" rx="10" ry="4" {p.f("#E3C38A")}/>'
                      f'<ellipse cx="12" cy="-10" rx="9" ry="4" {p.f("#E3C38A")}/>'
                      f'<path d="M-4 -16 Q0 -24 6 -16" {p.f("#B5683A", False)}/>')


def raised_hand(p, x, y, s=1.0):
    return hand_open(p, x, y, s, "#C99872")


def dome_outline(p, x, y, s=1.0):
    return A.shrine(p, x, y, s * 0.36, 1, 2)


def door_ajar(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-18" y="-50" width="36" height="50" {p.f("shade")}/>'
                      f'<path d="M-18 0 V-50 L-4 -46 V-3Z" {p.f("#8A5A3B")}/>'
                      f'<path d="M-4 -46 L18 -50 V0 L-4 -3" fill="#FFE7A8" opacity="0.5"/>')


def door_closed(p, x, y, s=1.0):
    return g(x, y, s, f'<rect x="-18" y="-50" width="36" height="50" rx="2" {p.f("#6B4430")}/>'
                      f'<path d="M0 -50 V0" {p.s("#4A2E20", 1.2)}/><rect x="-4" y="-28" width="8" height="5" {p.f("#3A2418", False)}/>'
                      f'<circle cx="-3" cy="-24" r="1.6" {p.f("gold", False)}/>')


def tent_obj(p, x, y, s=1.0):
    return tent(p, x, y, s * 1.2)


def camel_obj(p, x, y, s=1.0):
    return A.camel_standing(p, x - 18 * s, y, s * 1.1)


def horizon_tile(p, x, y, s=1.0):
    clip = f"hz{abs(hash((round(x, 1), round(y, 1)))) % 9999}"
    return g(x, y, s, f'<clipPath id="{clip}"><rect x="-28" y="-40" width="56" height="40" rx="6"/></clipPath>'
                      f'<g clip-path="url(#{clip})"><rect x="-28" y="-40" width="56" height="40" {p.f("sky")}/>'
                      f'<circle cx="0" cy="-16" r="8" {p.f("sun", False)}/>'
                      f'<path d="M-28 -14 Q0 -20 28 -14 V0 H-28Z" {p.f("far")}/>'
                      f'<path d="M-28 -6 Q0 -10 28 -5 V0 H-28Z" {p.f("mid")}/></g>')


def awning_street(p, x, y, s=1.0):
    return g(x, y, s, A.house(p, -14, 0, 0.6) + A.house(p, 16, 0, 0.5)) + awning(p, x, y, s * 0.6)


def pair_walking(p, x, y, s=1.0):
    """Two clasped hands — the walk to a door, without the walkers."""
    return hand_open(p, x - 8 * s, y, s * 0.7, "#B88A66") + hand_open(p, x + 8 * s, y + 4 * s, s * 0.55, "#D9A47E")


OBJECTS.update({
    "basket": basket, "sandal": sandal, "folded_cloth": folded_cloth, "lamp": oil_lamp, "open_book": open_book,
    "jug": jug, "broom": broom, "scales": scales_small, "awning": awning, "two_shirts": two_shirts, "shirt": shirt,
    "flag": flag, "river": river_tile, "milestone": milestone, "flower": flower, "feather": feather, "bird": bird,
    "hand_open": hand_open, "raised_hand": raised_hand, "plain_scroll": plain_scroll, "inkwell": inkwell,
    "ship_wheel": ship_wheel, "crate": crate, "rope": rope, "parcel": parcel, "satchel": satchel, "oil_jar": oil_jar,
    "chest": chest, "helmet": helmet, "reins": reins, "shield": round_shield, "scabbard": scabbard, "harness": harness,
    "tether": tether, "seat_circle": seat_circle, "star_field": star_field, "marks_four": marks_four,
    "shared_meal": shared_meal, "dome": dome_outline, "door_ajar": door_ajar, "door_closed": door_closed,
    "tent": tent_obj, "camel": camel_obj, "horizon": horizon_tile, "market": awning_street, "mat": A.mat,
    "sealed_letter": A.sealed_letter, "pair": pair_walking, "treaty": A.treaty, "lantern": lambda p, x, y, s: A.lantern(p, x, y, s * 1.4),
})


# ---------------------------------------------------------------- props held in a portrait
# draw(p, x, y, s) at the figure's origin, and the two grips (left, right);
# None leaves that arm at rest inside the robe.

def _letter_held(p, x, y, s):
    return g(x, y, s, f'<rect x="-13" y="-48" width="26" height="19" {p.f(PAPER)}/>'
                      f'<path d="M-13 -48 L0 -38 L13 -48" {p.s("#B9A98E", 0.8)}/>'
                      f'<circle cx="0" cy="-38" r="3.4" {p.f("accent", False)}/>')


def _book_held(p, x, y, s):
    return open_book(p, x, y - 26, 0.62)


def _flower_held(p, x, y, s):
    return flower(p, x + 2, y - 30, 0.62)


def _waterskin_held(p, x, y, s):
    return waterskin(p, x + 32, y - 8, 0.8)


def _shield_low(p, x, y, s):
    return round_shield(p, x - 33, y + 2, 1.05)


def _cane(p, x, y, s):
    return g(x, y, s, f'<path d="M30 -58 Q31 -20 30 6" {p.s("trunk", 3.2)}/><path d="M24 -60 Q30 -66 34 -58" {p.s("trunk", 3.2)}/>')


def _satchel_strap(p, x, y, s):
    return g(x, y, s, f'<path d="M-30 -60 L30 -8" {p.s("#7A4E30", 4)}/>') + satchel(p, x + 30, y + 6, 0.75)


def _reins_horse(p, x, y, s):
    """A horse's head at the rider's right, the reins to her hands."""
    head = ("M40 -10 Q36 -46 52 -66 Q58 -76 66 -70 Q78 -54 84 -40 Q86 -34 80 -32 Q70 -34 64 -42 Q60 -24 62 -6Z")
    return g(x, y, s, f'<path d="{head}" {p.f("#7A4E30")}/>'
                      f'<path d="M54 -66 L50 -78 L58 -70Z" {p.f("#6A4028", False)}/>'
                      f'<path d="M50 -64 Q44 -40 46 -12" {p.s("#3A2418", 3.4)}/>'
                      f'<circle cx="70" cy="-56" r="1.8" {p.f("#1E1612", False)}/>'
                      f'<path d="M-6 -36 Q30 -30 78 -38 M8 -36 Q40 -32 78 -38" {p.s("#3A2418", 1.2)}/>')


PROPS = {
    "seedling": (lambda p, x, y, s: seedling(p, x + 14, y - 34, s), ((5, -32), (23, -33))),
    "letter": (_letter_held, ((-14, -38), (14, -39))),
    "book": (_book_held, ((-19, -30), (19, -30))),
    "flower": (_flower_held, ((-5, -30), (7, -31))),
    "waterskin": (_waterskin_held, (None, (28, -40))),
    "shield": (_shield_low, ((-30, -24), None)),
    "cane": (_cane, (None, (30, -44))),
    "satchel": (_satchel_strap, (None, None)),
    "reins": (_reins_horse, ((-6, -36), (8, -36))),
}


# ---------------------------------------------------------------- the scene composer
# A place is data: a ground and a list of elements, each (key, x, y, size,
# layer) in fractions of the box, layer "back" (behind the person) or "front"
# (over them: a table edge, a counter, a roof edge). Used for the portrait's
# place, the letter head and the postcard, so all three are the same place.

def hill(p, x, y, s=1.0):
    """A bare mountain — Uhud."""
    return g(x, y, s, f'<path d="M-90 0 Q-60 -40 -30 -52 Q-10 -70 10 -62 Q40 -58 60 -34 Q76 -16 90 0Z" {p.f("mid")}/>'
                      f'<path d="M-30 -52 Q-14 -40 -20 -20 M10 -62 Q20 -40 14 -24" {p.s("shade", 0.6)}/>')


def tents(p, x, y, s=1.0):
    return tent(p, x - 36 * s, y, s * 0.8) + tent(p, x, y - 4 * s, s * 0.65) + tent(p, x + 34 * s, y, s * 0.75)


def window_niche(p, x, y, s=1.0):
    """An arched window in the wall, the sky showing through."""
    return g(x, y, s, f'<path d="M-14 0 V-30 Q0 -48 14 -30 V0Z" {p.f("sky")}/>'
                      f'<path d="M-14 0 V-30 Q0 -48 14 -30 V0Z" fill="none" stroke="{p.c("shade")}" stroke-width="2"/>'
                      f'<rect x="-17" y="0" width="34" height="4" {p.f("tile", False)}/>')


def ship(p, x, y, s=1.0):
    return g(x, y, s, f'<path d="M-50 -14 H50 L40 0 H-40Z" {p.f("#7A4E30")}/>'
                      f'<path d="M0 -14 V-100" {p.s("#5A3A26", 2.6)}/><path d="M-26 -84 H26" {p.s("#5A3A26", 2)}/>'
                      f'<path d="M-24 -82 Q-30 -50 -22 -20 H24 Q32 -50 24 -82Z" {p.f(PAPER)}/>'
                      f'<path d="M0 -100 L18 -94 L0 -88Z" {p.f("accent", False)}/>')


def light_sliver(p, x, y, s=1.0):
    """A sliver of light ahead in the dark — the one who prays is not shown."""
    return g(x, y, s, f'<path d="M-4 0 V-80 H4 V0Z" fill="#FFE7A8"/>'
                      f'<path d="M-4 0 L-26 14 H26 L4 0Z" fill="#FFE7A8" opacity="0.35"/>')


def seated(p, x, y, s=1.0, key="shade"):
    """A row of people sitting, seen from behind — a room listening."""
    return g(x, y, s, "".join(f'<path d="M{cx - 14} 0 Q{cx - 14} -20 {cx} -22 Q{cx + 14} -20 {cx + 14} 0Z" {p.f(key)}/>'
                              f'<circle cx="{cx}" cy="-28" r="7.5" {p.f(key)}/>' for cx in (-44, -14, 16, 46)))


def stall(p, x, y, s=1.0):
    """A trader's stall seen behind the trader: awning, shelves of jars."""
    return g(x, y, s, f'<rect x="-60" y="-70" width="120" height="70" {p.f("body")}/>'
                      + "".join(f'<path d="M{-60 + i * 20} -78 H{-40 + i * 20} V-64 Q{-50 + i * 20} -58 {-60 + i * 20} -64Z" '
                                f'{p.f("accent" if i % 2 == 0 else PAPER, False)}/>' for i in range(6))
                      + "".join(oil_jar(p, jx, -30, 0.45) for jx in (-44, -28, -12, 12, 28, 44))
                      + f'<path d="M-60 -30 H60" {p.s("shade", 1.4)}/>')


def street(p, w, h, top):
    out = ""
    for i, (hx, hh) in enumerate([(0.08, 0.2), (0.25, 0.26), (0.42, 0.18), (0.6, 0.24), (0.78, 0.2), (0.95, 0.27)]):
        out += A.house(p, w * hx, h * top, min(w, h) / 100 * (0.5 + hh))
    return out


def _wide(key, p, w, h, yf):
    y = h * yf
    if key == "table":
        return (f'<rect x="0" y="{y:.1f}" width="{w}" height="{h - y + 2:.1f}" {p.f("#A0703F")}/>'
                f'<rect x="0" y="{y:.1f}" width="{w}" height="{h * 0.03:.1f}" {p.f("#B8834E", False)}/>')
    if key == "counter":
        return (f'<rect x="0" y="{y:.1f}" width="{w}" height="{h - y + 2:.1f}" {p.f("#9A6A44")}/>'
                f'<rect x="0" y="{y:.1f}" width="{w}" height="{h * 0.025:.1f}" {p.f("#B8834E", False)}/>')
    if key == "parapet":
        return parapet(p, w, h, y)
    if key == "dock":
        planks = "".join(f'<path d="M0 {y + i * h * 0.04:.1f} H{w}" {p.s("#7A5636", 0.6)}/>' for i in range(1, 6))
        return f'<rect x="0" y="{y:.1f}" width="{w}" height="{h - y + 2:.1f}" {p.f("#A07A52")}/>' + planks
    if key == "road":
        return A.road(p, w, h, y, w * 0.62)
    if key == "river":
        return (f'<path d="M0 {y:.1f} Q{w * 0.3:.1f} {y - h * 0.02:.1f} {w * 0.6:.1f} {y:.1f} T{w} {y:.1f} V{y + h * 0.1:.1f} H0Z" '
                f'{p.f("water")}/>')
    if key == "street":
        return street(p, w, h, yf)
    raise KeyError(key)


WIDE = {"table", "counter", "parapet", "dock", "road", "river", "street"}

SCENERY = {
    "palm": lambda p, x, y, s: A.palm(p, x, y, s * 0.9), "hill": hill, "tents": tents, "window": window_niche,
    "ship": ship, "light": light_sliver, "seated": seated, "stall": stall, "city": lambda p, x, y, s: A.city(p, x, y, s * 0.5),
    "shrine": lambda p, x, y, s: A.shrine(p, x, y, s * 0.5, 1, 2), "house": lambda p, x, y, s: A.house(p, x, y, s * 0.8),
    "doorway": lambda p, x, y, s: A.doorway(p, x, y, s * 0.7), "palace": palace, "arcade": A.arcade,
    "camel_big": lambda p, x, y, s: A.camel_standing(p, x, y, s * 0.9),
    "standard": lambda p, x, y, s: A.standard(p, x, y, s * 0.6), "treaty": A.treaty,
}


def compose(p, w, h, time, spec, at=None):
    """(back, front) for a place spec — see the note above."""
    ground = spec.get("ground", "dunes")
    gy = spec.get("gy", 0.62)
    sun = at if at is not None else spec.get("sun", (0.84, 0.18))
    if sun and 0.3 < sun[0] < 0.7 and sun[1] < 0.4 and len(sun) < 3:
        # a sun straight above a person's head reads as a halo; keep it to the side
        sun = (0.86 if sun[0] >= 0.5 else 0.14,) + tuple(sun[1:])
    k = min(w, h) / 100
    if ground == "room":
        back = (f'<rect width="{w}" height="{h}" {p.f("body")}/>'
                f'<rect y="{h * gy:.1f}" width="{w}" height="{h * (1 - gy) + 2:.1f}" {p.f("mid")}/>'
                f'<rect y="{h * gy - h * 0.012:.1f}" width="{w}" height="{h * 0.012:.1f}" {p.f("tile", False)}/>')
    elif ground == "dark":
        back = (f'<rect width="{w}" height="{h}" {p.f("#1F1C30")}/>'
                f'<rect y="{h * gy:.1f}" width="{w}" height="{h * (1 - gy) + 2:.1f}" {p.f("#2A2640")}/>')
    elif ground == "sea":
        back = (sky(p, w, h, time, sun)
                + f'<rect y="{h * gy:.1f}" width="{w}" height="{h * (1 - gy) + 2:.1f}" {p.f("water")}/>'
                + "".join(f'<path d="M{w * fx:.1f} {h * (gy + 0.05 + i * 0.04):.1f} q{3 * k:.1f} {-1.2 * k:.1f} {6 * k:.1f} 0" '
                          f'{p.s(PAPER, 0.5)}/>' for i, fx in enumerate((0.1, 0.5, 0.8, 0.3))))
    else:
        back = sky(p, w, h, time, sun) + A.dune(p, w, h, h * gy, h * 0.03, "far", 0.1)
    front = ""
    for el in spec.get("els", []):
        key, xf, yf, sf = el[:4]
        layer = el[4] if len(el) > 4 else "back"
        if key in WIDE:
            art = _wide(key, p, w, h, yf)
        else:
            fn = SCENERY.get(key) or OBJECTS.get(key) or A.OBJECTS[key]
            art = fn(p, w * xf, h * yf, sf * k)
        if layer == "front":
            front += art
        elif layer == "mid":
            back += art
        else:
            back += art
    if ground == "dunes" and spec.get("near", True):
        back += haze(w, h, h * gy) + A.dune(p, w, h, h * (gy + 0.12), h * 0.025, "mid", -0.1) + tufts(p, w, h, h * (gy + 0.16))
    return back, front


def fitrus_place(p, w, h, time, at=None):
    """Fitrus: no figure at all — a single feather standing in for him, on a night sky."""
    back = sky(p, w, h, "night", (0.8, 0.16)) + A.dune(p, w, h, h * 0.8, h * 0.02, "far", 0.1)
    back += feather(p, w * 0.5, h * 0.86, min(w, h) / 100 * 0.62)
    back += bird(p, w * 0.24, h * 0.3, min(w, h) / 100 * 0.25) + bird(p, w * 0.76, h * 0.42, min(w, h) / 100 * 0.18)
    return back, ""
