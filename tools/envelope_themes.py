"""Fourteen envelopes, fourteen styles (decided 2026-10-08).

Each style is data: two faces, a palette for the type, a palette for the art,
an art mode (how the Pen draws), the band at the foot of each page, and the
shape of the hadith card. What does NOT vary lives in tools/build_envelopes.py
and 04-art/envelopes/envelope.css: page sizes, the ●○ voices, the fact-panel
order, the chain mark wording, the ring punch, the name area.

The two mourning styles (01, 02) use charcoal and ivory only, art included —
tests/test_envelopes.py checks every colour on those pages.
"""

INK, IVORY = "#1B1B1B", "#F3EDE1"


def _art(**kw):
    base = dict(sky="#F9D9B4", sun="#F6B48A", moon="#F2C46D", star="#F6B48A", far="#F6B48A", mid="#E58F7B",
                near="#1F5C63", road="#FCEBD5", trunk="#5B3A63", frond="#1F5C63", dome="#5B3A63",
                body="#FCEBD5", tile="#F6B48A", shade="#5B3A63", accent="#E58F7B", ink="#3B2440",
                cloak="#1F5C63", cube="#3B2440", cube2="#2A1A2E", gold="#D9A63A", water="#7FB8C4",
                paper="#FFF6EA", beast="#5B3A63", ground="#FFF6EA", stitch="#FFF6EA", shadow="#3B2440",
                riso2="#FF48B0")
    base.update(kw)
    return base


def _dunes(a, b):
    return (f"<path fill='{a}' d='M0 26 Q100 6 200 22 T400 16 V60 H0Z'/>"
            f"<path fill='{b}' d='M0 42 Q120 26 250 40 T400 34 V60 H0Z'/>")


def _line_dunes(c):
    return (f"<path fill='none' stroke='{c}' stroke-width='1' d='M0 26 Q100 6 200 22 T400 16'/>"
            f"<path fill='none' stroke='{c}' stroke-width='1' d='M0 44 Q130 28 270 42 T400 36'/>")


def _stripes(*cols):
    h = 60 / len(cols)
    return "".join(f"<rect y='{i * h:.1f}' width='400' height='{h + 0.5:.1f}' fill='{c}'/>" for i, c in enumerate(cols))


def _tiles(bg, a, b, dot):
    out = f"<rect y='20' width='400' height='40' fill='{bg}'/>"
    for x in range(0, 400, 40):
        out += (f"<path fill='{a}' d='M{x + 20} 22 L{x + 28} 40 L{x + 20} 58 L{x + 12} 40Z'/>"
                f"<path fill='{b}' d='M{x + 2} 40 L{x + 20} 32 L{x + 38} 40 L{x + 20} 48Z' opacity='.7'/>"
                f"<circle cx='{x + 20}' cy='40' r='3' fill='{dot}'/>")
    return out


def _halftone(c1, c2):
    out = ""
    for y in range(14, 60, 6):
        for x in range(0, 400, 6):
            r = min(2.6, (y - 10) / 18)
            out += f"<circle cx='{x + (3 if (y // 6) % 2 else 0)}' cy='{y}' r='{r:.2f}' fill='{c1 if x % 60 < 30 else c2}'/>"
    return out


def _stitch(c, d):
    return (f"<path fill='none' stroke='{c}' stroke-width='3' stroke-dasharray='8 6' d='M0 40 Q100 24 200 40 T400 40'/>"
            + "".join(f"<circle cx='{x}' cy='40' r='5' fill='{d}'/>" for x in range(20, 400, 60)))


def _interlace(bg, gold):
    out = f"<rect y='34' width='400' height='26' fill='{bg}'/>"
    for x in range(0, 400, 26):
        out += (f"<path fill='none' stroke='{gold}' stroke-width='2' d='M{x} 47 Q{x + 6.5} 36 {x + 13} 47 T{x + 26} 47'/>"
                f"<path fill='none' stroke='{gold}' stroke-width='2' d='M{x} 47 Q{x + 6.5} 58 {x + 13} 47 T{x + 26} 47'/>")
    return out + f"<rect y='32' width='400' height='2' fill='{gold}'/>"


def _shapes(a, b):
    return (f"<path fill='{a}' d='M0 60 V20 A40 40 0 0 1 80 20 V60Z'/><path fill='{b}' d='M80 60 A40 40 0 0 1 160 60Z'/>"
            f"<path fill='{a}' d='M200 60 V30 A30 30 0 0 1 260 30 V60Z'/><path fill='{b}' d='M300 60 A50 50 0 0 1 400 60Z'/>")


def _wash(c, o=0.18):
    return (f"<ellipse cx='120' cy='56' rx='170' ry='22' fill='{c}' fill-opacity='{o}'/>"
            f"<ellipse cx='320' cy='60' rx='140' ry='18' fill='{c}' fill-opacity='{o * 0.8:.2f}'/>")


def _night(bg, dot):
    return (f"<path fill='{bg}' d='M0 30 Q100 14 200 28 T400 22 V60 H0Z'/>"
            + "".join(f"<circle cx='{x}' cy='{12 + (x * 7) % 14}' r='1.4' fill='{dot}'/>" for x in range(14, 400, 37)))


THEMES = {
    "01": dict(
        key="M2", name="Ink Wash", fonts=("Cormorant Garamond", "Nunito Sans"), dweight=700, mode="wash",
        vars=dict(ground=IVORY, ground2=IVORY, ink=INK, soft="rgba(27,27,27,0.72)", accent=INK, child=INK,
                  bar=INK, pill="rgba(27,27,27,0.08)", pill_ink=INK, card_bg="rgba(27,27,27,0.12)",
                  card_ink=INK, card_accent=INK, seal=INK, name_bg=IVORY, stamp=INK),
        art=_art(sky=IVORY, sun="rgba(27,27,27,0.10)", moon="rgba(27,27,27,0.3)", star="rgba(27,27,27,0.4)",
                 far="rgba(27,27,27,0.12)", mid="rgba(27,27,27,0.18)", near="rgba(27,27,27,0.3)",
                 road="rgba(27,27,27,0.06)", trunk="rgba(27,27,27,0.6)", frond="rgba(27,27,27,0.45)",
                 dome="rgba(27,27,27,0.55)", body="rgba(27,27,27,0.35)", tile="rgba(27,27,27,0.5)",
                 shade="rgba(27,27,27,0.6)", accent="rgba(27,27,27,0.5)", ink=INK, cloak="rgba(27,27,27,0.45)",
                 cube=INK, cube2="rgba(27,27,27,0.8)", gold="rgba(27,27,27,0.4)", water="rgba(27,27,27,0.14)",
                 paper=IVORY, beast="rgba(27,27,27,0.6)", ground=IVORY, stitch=IVORY, shadow=INK, riso2=INK),
        band=_wash(INK), card="wash", mourning=True),
    "02": dict(
        key="M1", name="Charcoal Line", fonts=("Young Serif", "Nunito Sans"), dweight=400, mode="line",
        vars=dict(ground=IVORY, ground2=IVORY, ink=INK, soft="rgba(27,27,27,0.72)", accent=INK, child=INK,
                  bar=INK, pill="transparent", pill_ink=INK, card_bg=IVORY, card_ink=INK, card_accent=INK,
                  seal=INK, name_bg=IVORY, stamp=INK),
        art=_art(**{k: IVORY for k in ("sky", "sun", "moon", "star", "far", "mid", "near", "road", "trunk", "frond",
                                       "dome", "body", "tile", "shade", "accent", "cloak", "cube", "cube2", "gold",
                                       "water", "paper", "beast", "ground", "stitch")}, ink=INK, shadow=INK, riso2=INK),
        band=_line_dunes(INK), card="outline", mourning=True),
    "03": dict(
        key="C", name="Paper Dunes", fonts=("Young Serif", "Nunito Sans"), dweight=400, mode="cut",
        vars=dict(ground="#FFF6EA", ground2="#FCEBD5", ink="#3B2440", soft="#6B4E5E", accent="#B0503E",
                  child="#1F5C63", bar="#F6B48A", pill="#FCEBD5", pill_ink="#5B3A63", card_bg="#5B3A63",
                  card_ink="#FFF6EA", card_accent="#F6B48A", seal="#5B3A63", name_bg="#FFF6EA", stamp="#5B3A63"),
        art=_art(dome="#3E8E6E"), band=_dunes("#F6B48A", "#E58F7B"), card="arch"),
    "04": dict(
        key="B3", name="Big Shapes", fonts=("Bricolage Grotesque", "Newsreader"), dweight=800, mode="flat",
        vars=dict(ground="#FFFFFF", ground2="#F5F1E8", ink="#14205C", soft="#4A5585", accent="#E2601F",
                  child="#E2601F", bar="#F5A623", pill="#FDE9C6", pill_ink="#14205C", card_bg="#1D3FBF",
                  card_ink="#F5F1E8", card_accent="#F5A623", seal="#1D3FBF", name_bg="#F5F1E8", stamp="#1D3FBF"),
        art=_art(sky="#F5F1E8", sun="#F5A623", far="#F5A623", mid="#E2601F", near="#1D3FBF", road="#F5F1E8",
                 trunk="#14205C", frond="#1D3FBF", dome="#F5A623", body="#1D3FBF", tile="#F5F1E8", shade="#14205C",
                 accent="#E2601F", ink="#14205C", cloak="#1D3FBF", water="#1D3FBF", paper="#FFFFFF", beast="#14205C"),
        band=_shapes("#1D3FBF", "#F5A623"), card="quarter"),
    "05": dict(
        key="D", name="Illuminated", fonts=("Cormorant Garamond", "Alegreya"), dweight=700, mode="gilt",
        vars=dict(ground="#F7EFDC", ground2="#EFE3C8", ink="#1E1A33", soft="#4B4366", accent="#A8352A",
                  child="#A8352A", bar="#C9A04A", pill="#EFE3C8", pill_ink="#1F3A7A", card_bg="#1F3A7A",
                  card_ink="#F7EFDC", card_accent="#C9A04A", seal="#A8352A", name_bg="#F7EFDC", stamp="#1F3A7A"),
        art=_art(sky="#EFE3C8", sun="#C9A04A", far="#2F7D5B", mid="#1F3A7A", near="#A8352A", road="#F7EFDC",
                 trunk="#1E1A33", frond="#2F7D5B", dome="#1F3A7A", body="#F7EFDC", tile="#A8352A", shade="#1F3A7A",
                 accent="#A8352A", ink="#1E1A33", cloak="#2F7D5B", gold="#C9A04A", water="#1F3A7A",
                 paper="#F7EFDC", beast="#1E1A33"),
        band=_interlace("#1F3A7A", "#C9A04A"), card="frame"),
    "06": dict(
        key="F", name="Suzani", fonts=("Gloock", "Karla"), dweight=400, mode="stitch",
        vars=dict(ground="#F8F1E3", ground2="#EDE3CF", ink="#2B2420", soft="#5A4E44", accent="#B23A2E",
                  child="#B23A2E", bar="#E0A33A", pill="#EDE3CF", pill_ink="#263B6B", card_bg="#263B6B",
                  card_ink="#F4EBDA", card_accent="#E0A33A", seal="#B23A2E", name_bg="#263B6B", stamp="#B23A2E"),
        art=_art(sky="#EDE3CF", sun="#E0A33A", far="#E0A33A", mid="#5E7F3E", near="#B23A2E", road="#F4EBDA",
                 trunk="#2B2420", frond="#5E7F3E", dome="#263B6B", body="#F4EBDA", tile="#B23A2E", shade="#263B6B",
                 accent="#B23A2E", ink="#2B2420", cloak="#263B6B", water="#263B6B", paper="#F4EBDA",
                 beast="#263B6B", stitch="#F4EBDA"),
        band=_stitch("#B23A2E", "#263B6B"), card="medallion"),
    "07": dict(
        key="A3", name="Mosaic Stars", fonts=("Fraunces", "Literata"), dweight=700, mode="flat",
        vars=dict(ground="#FBF4E6", ground2="#0F3B3A", ink="#0F3B3A", soft="#3E615F", accent="#B0503E",
                  child="#0F3B3A", bar="#E3B657", pill="#0F3B3A", pill_ink="#FBF4E6", card_bg="#0F3B3A",
                  card_ink="#FBF4E6", card_accent="#E3B657", seal="#E3B657", name_bg="#FBF4E6", stamp="#0F3B3A"),
        art=_art(sky="#0F3B3A", sun="#E3B657", moon="#E3B657", star="#E3B657", far="#1E5A57", mid="#46B3A8",
                 near="#0A2D2C", road="#E3B657", trunk="#0A2D2C", frond="#46B3A8", dome="#E3B657", body="#46B3A8",
                 tile="#E3B657", shade="#0A2D2C", accent="#E3B657", ink="#0A2D2C", cloak="#46B3A8",
                 cube="#111111", cube2="#262626", gold="#E3B657", water="#46B3A8", paper="#FBF4E6", beast="#E3B657"),
        band=_tiles("#0F3B3A", "#46B3A8", "#E3B657", "#FBF4E6"), card="lantern"),
    "08": dict(
        key="A", name="Lantern Night", fonts=("Fraunces", "Literata"), dweight=700, mode="flat",
        vars=dict(ground="#FBF4E6", ground2="#1F2552", ink="#1F2552", soft="#4A5280", accent="#C8553A",
                  child="#C8553A", bar="#E9B44C", pill="#F6E6C8", pill_ink="#1F2552", card_bg="#1F2552",
                  card_ink="#FBF4E6", card_accent="#E9B44C", seal="#E9B44C", name_bg="#1F2552", stamp="#E9B44C"),
        art=_art(sky="#1F2552", sun="#E9B44C", moon="#E9B44C", star="#E9B44C", far="#2E3670", mid="#3A4380",
                 near="#141A3D", road="#E9B44C", trunk="#141A3D", frond="#2E8C6A", dome="#2E8C6A", body="#3A4380",
                 tile="#E9B44C", shade="#141A3D", accent="#EE7B5C", ink="#141A3D", cloak="#EE7B5C", water="#3A4380",
                 paper="#FBF4E6", beast="#E9B44C"),
        band=_night("#1F2552", "#E9B44C"), card="stars"),
    "09": dict(
        key="C2", name="Dune Night", fonts=("Young Serif", "Nunito Sans"), dweight=400, mode="cut",
        vars=dict(ground="#FFF3E2", ground2="#2B2150", ink="#2B2150", soft="#5A4E78", accent="#B0503E",
                  child="#6B4E8F", bar="#F2C46D", pill="#EFE6F7", pill_ink="#2B2150", card_bg="#2B2150",
                  card_ink="#FFF3E2", card_accent="#F2C46D", seal="#6B4E8F", name_bg="#FFF3E2", stamp="#F2C46D"),
        art=_art(sky="#2B2150", sun="#F2C46D", moon="#F2C46D", star="#F2C46D", far="#4C3870", mid="#6B4E8F",
                 near="#E58F7B", road="#4C3870", trunk="#1A1430", frond="#1A1430", dome="#1A1430", body="#1A1430",
                 tile="#F2C46D", shade="#0E0A1A", accent="#F2C46D", ink="#1A1430", cloak="#6B4E8F",
                 water="#4C3870", paper="#FFF3E2", beast="#1A1430", shadow="#0E0A1A"),
        band=_dunes("#6B4E8F", "#E58F7B"), card="arch"),
    "10": dict(
        key="A2", name="Lantern Dawn", fonts=("Fraunces", "Literata"), dweight=700, mode="flat",
        vars=dict(ground="#FBF4E6", ground2="#DCE8F2", ink="#1F2552", soft="#4A5280", accent="#C26A4A",
                  child="#C26A4A", bar="#E1A73A", pill="#DCE8F2", pill_ink="#1F2552", card_bg="#DCE8F2",
                  card_ink="#1F2552", card_accent="#C26A4A", seal="#E1A73A", name_bg="#FBF4E6", stamp="#1F2552"),
        art=_art(sky="#DCE8F2", sun="#E1A73A", far="#F7D9C4", mid="#F2B8A2", near="#1F2552", road="#FBF4E6",
                 trunk="#1F2552", frond="#1F2552", dome="#1F2552", body="#FBF4E6", tile="#E1A73A", shade="#1F2552",
                 accent="#C26A4A", ink="#1F2552", cloak="#1F2552", water="#9DBBD6", paper="#FBF4E6", beast="#1F2552"),
        band=_stripes("#F7D9C4", "#F2B8A2", "#E1A73A", "#1F2552"), card="bands"),
    "11": dict(
        key="B", name="Tile Explorer", fonts=("Bricolage Grotesque", "Newsreader"), dweight=800, mode="flat",
        vars=dict(ground="#FFFFFF", ground2="#FFF8EC", ink="#16224F", soft="#4A5580", accent="#D2483F",
                  child="#1F8F89", bar="#1FA7A0", pill="#E3F4F3", pill_ink="#16224F", card_bg="#1FA7A0",
                  card_ink="#FFFFFF", card_accent="#FFF8EC", seal="#D2483F", name_bg="#FFFFFF", stamp="#D2483F"),
        art=_art(sky="#16224F", sun="#F2A93B", moon="#F2A93B", star="#F2A93B", far="#2343A8", mid="#1FA7A0",
                 near="#0F1838", road="#F2A93B", trunk="#0F1838", frond="#1FA7A0", dome="#1FA7A0", body="#2343A8",
                 tile="#F2A93B", shade="#0F1838", accent="#D2483F", ink="#0F1838", cloak="#D2483F",
                 water="#1FA7A0", paper="#FFF8EC", beast="#F2A93B"),
        band=_tiles("#2343A8", "#1FA7A0", "#FFF8EC", "#F2A93B"), card="tile"),
    "12": dict(
        key="E", name="Riso Press", fonts=("Space Grotesk", "Atkinson Hyperlegible"), dweight=700, mode="riso",
        vars=dict(ground="#FFFDF8", ground2="#F7F3EA", ink="#1B2A4A", soft="#3E4C6B", accent="#FF48B0",
                  child="#0078BF", bar="#FFE800", pill="#FFD0EA", pill_ink="#1B2A4A", card_bg="#0078BF",
                  card_ink="#F7F3EA", card_accent="#FFE800", seal="#FF48B0", name_bg="#F7F3EA", stamp="#0078BF"),
        art=_art(sky="#F7F3EA", sun="#FFE800", moon="#FFE800", star="#FF48B0", far="#FFE800", mid="#FF8CCB",
                 near="#7FBCE0", road="#F7F3EA", trunk="#0078BF", frond="#0078BF", dome="#0078BF", body="#BFE0F2",
                 tile="#FF48B0", shade="#0078BF", accent="#FF48B0", ink="#1B2A4A", cloak="#FF48B0",
                 water="#0078BF", paper="#F7F3EA", beast="#0078BF", riso2="#FF48B0"),
        band=_halftone("#FF48B0", "#0078BF"), card="blobs"),
    "13": dict(
        key="G", name="Watercolour", fonts=("Marcellus", "Lora"), dweight=400, mode="wash",
        vars=dict(ground="#FBF6EC", ground2="#F4ECDD", ink="#3A2E26", soft="#6E5F50", accent="#B07A2A",
                  child="#235F86", bar="#86C3D1", pill="#E8F2F4", pill_ink="#235F86", card_bg="#F4ECDD",
                  card_ink="#3A2E26", card_accent="#B07A2A", seal="#235F86", name_bg="#FBF6EC", stamp="#B07A2A"),
        art=_art(sky="#F4ECDD", sun="#F2C27A", far="#D9C9A8", mid="#C9B48A", near="#86C3D1", road="#F4ECDD",
                 trunk="#6E5F50", frond="#7FA06A", dome="#E0A33A", body="#86C3D1", tile="#235F86", shade="#6E5F50",
                 accent="#B07A2A", ink="#3A2E26", cloak="#235F86", water="#86C3D1", paper="#FBF6EC",
                 beast="#8A6A4A", shadow="#3A2E26"),
        band=_wash("#86C3D1", 0.35), card="vignette"),
    "14": dict(
        key="C4", name="Garden Pop-up", fonts=("Young Serif", "Nunito Sans"), dweight=400, mode="cut",
        vars=dict(ground="#FFFDF7", ground2="#F7F1E3", ink="#26392F", soft="#4E6157", accent="#C2513F",
                  child="#2F6B4F", bar="#A9C98F", pill="#2F6B4F", pill_ink="#FFFDF7", card_bg="#FFFDF7",
                  card_ink="#26392F", card_accent="#C2513F", seal="#D9A63A", name_bg="#FFFFFF", stamp="#2F6B4F"),
        art=_art(sky="#CFE6EC", sun="#F6C27A", far="#A9C98F", mid="#7FB06A", near="#2F6B4F", road="#F7F1E3",
                 trunk="#7A4E3A", frond="#2F6B4F", dome="#D9A63A", body="#F7F1E3", tile="#C2513F", shade="#26392F",
                 accent="#C2513F", ink="#26392F", cloak="#2F6B4F", water="#7FB8C4", paper="#FFFDF7",
                 beast="#7A4E3A", shadow="#1D2C24"),
        band=_dunes("#A9C98F", "#2F6B4F"), card="garden"),
}

# Each envelope's subjects, from 04-art/prompts.md (person and event print
# tables, postcard and sticker tables). Times of day set the sky.
SCENES = {
    "01": dict(person="karbala", event="standard", postcard="standard", stickers=None, time="dusk", head="karbala"),
    "02": dict(person="baqi", event="road_dawn", postcard="road_dawn", stickers=None, time="dusk", head="baqi"),
    "03": dict(person="nabawi", event="quba", postcard="cloak", time="day", head="nabawi",
               stickers=["cloak", "palm", "camel", "star", "lantern", "crescent"]),
    "04": dict(person="samarra", event="samarra_city", postcard="sealed_letter", time="day", head="samarra_city",
               stickers=["sealed_letter", "qalam", "coin", "door", "star", "shrine"]),
    "05": dict(person="baqi", event="zaynab", postcard="qalam", time="day", head="baqi",
               stickers=["qalam", "books", "palm", "bowl", "star", "door"]),
    "06": dict(person="door", event="house", postcard="door", time="day", head="door",
               stickers=["handmill", "bowl", "door", "palm", "star", "lantern"]),
    "07": dict(person="najaf", event="kaaba", postcard="scales", time="night", head="najaf",
               stickers=["shield", "scales", "door", "star", "crescent", "lantern"]),
    "08": dict(person="window", event="hira", postcard="window", time="night", head="window",
               stickers=["window", "lantern", "sealed_letter", "star", "crescent", "door"]),
    "09": dict(person="baqi", event="courtyard", postcard="lantern", time="night", head="courtyard",
               stickers=["books", "door", "lantern", "star", "crescent", "mat"]),
    "10": dict(person="road_dawn", event="jamkaran", postcard="road_dawn", time="dawn", head="road_dawn",
               stickers=["sealed_letter", "lantern", "star", "door", "crescent", "palm"]),
    "11": dict(person="samarra", event="qadr", postcard="lantern", time="night", head="qadr",
               stickers=["mat", "door", "lantern", "crescent", "star", "shrine"]),
    "12": dict(person="teaching", event="eid", postcard="books", time="day", head="teaching",
               stickers=["books", "lantern", "flask", "door", "star", "crescent"]),
    "13": dict(person="mashhad", event="qom", postcard="sealed_letter", time="day", head="mashhad",
               stickers=["sealed_letter", "coin", "door", "star", "shrine", "palm"]),
    "14": dict(person="kadhimiya", event="ghadir", postcard="ring14", time="day", head="ghadir",
               stickers=["seats", "branching", "door", "star", "crescent", "palm"]),
}
