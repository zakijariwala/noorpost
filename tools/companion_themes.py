"""The companions line — Everyone Else — as data.

The box has fourteen styles. This line has one: thirty-nine envelopes that
belong together, like a set of stamps. What is shared is the LINE below —
type, medium, layout, the stamp on the front. What each person brings is
their own colour, their own portrait, their own place, their own stickers.

PEOPLE[slug]:
  colour, colour2   the stamp's frame and its second ink
  tint              the envelope's paper, a pale wash of the colour
  art               palette overrides for the scenes (see envelope_themes._art)
  time              day / dawn / dusk / night for the skies
  figure            the portrait: see tools/companion_art.figure
  backdrop          the place behind them, on the stamp and the print
  postcard          the picture on the return postcard (no person on it)
  hero              the object set small on face 3 of the letter
  stickers          six sticker keys, from companion_art.OBJECTS
"""

from envelope_themes import _art

LINE = dict(
    key="EE", name="Everyone Else", fonts=("Fraunces", "Nunito Sans"), dweight=700, mode="cut",
)

# The three skin tones and their shades used so far; named so a later batch
# reuses them rather than inventing near-duplicates.
SKIN = {
    "light": ("#E0B48E", "#C29270"),
    "tan": ("#D3A47E", "#B4825C"),
    "olive": ("#C99872", "#A87652"),
    "brown": ("#B88A66", "#9A6E4C"),
    "dark": ("#8A5A3C", "#6E4630"),
    "deep": ("#6B4430", "#553424"),
}

# The family of the Fourteen — mothers, wives, sons and daughters of a Masoom —
# are drawn with the face veiled in light, the convention of devotional art,
# rather than with features. Everyone else in the line has a face.
VEILED = {"fatima-bint-asad", "abbas", "umm-kulthum", "rabab", "zaynab", "sakina", "umm-al-banin", "ruqayya",
          "umm-farwa", "hamida", "masuma", "narjis"}


def _fig(skin, **kw):
    s, sh = SKIN[skin]
    return dict(skin=s, skin_sh=sh, **kw)


def _woman(skin, scarf, robe, **kw):
    return _fig(skin, head="hijab", head_c=scarf, head_c2=kw.pop("edge", scarf), robe=robe,
                robe2=kw.pop("robe2", scarf), **kw)


def _pal(c, c2, sky, far, mid, **kw):
    """A person's scene palette: their colour carries the tiles and trims."""
    light = sum(int(c2[i:i + 2], 16) for i in (1, 3, 5)) > 420
    base = dict(sky=sky, sun=kw.pop("sun", c2 if light else "#F2C46D"), far=far, mid=mid, near=kw.pop("near", c), road=kw.pop("road", "#F3E2C2"),
                trunk=kw.pop("trunk", "#7A5236"), frond=kw.pop("frond", "#4E7A3A"), body=kw.pop("body", "#EAD9BC"),
                tile=c, shade=kw.pop("shade", "#3B2F45"), accent=kw.pop("accent", c), ink="#2A2230",
                shadow="#2A2230", gold=kw.pop("gold", "#D9A441"), water=kw.pop("water", "#7FB8C4"))
    base.update(kw)
    return _art(**base)


def _p(colour, colour2, tint, time, art, figure, backdrop, postcard, hero, stickers, **kw):
    return dict(colour=colour, colour2=colour2, tint=tint, time=time, art=art, figure=figure, backdrop=backdrop,
                postcard=postcard, hero=hero, stickers=stickers, **kw)


PEOPLE = {
    "salman": dict(
        colour="#2F5E8C", colour2="#E3A33B", tint="#F4EEDF", time="day",
        art=_art(sky="#F7E6C4", sun="#E3A33B", far="#E9C38A", mid="#D9A066", near="#6E8B4E", road="#F3E2C2",
                 trunk="#7A5236", frond="#3E7A3A", body="#EAD9BC", tile="#2F5E8C", shade="#3B2F45",
                 accent="#C4553A", ink="#2A2230", shadow="#2A2230"),
        figure=_fig("olive", head="turban", head_c="#F1E6D2", head_c2="#C8B48F", beard="full", beard_c="#BDB5AA",
                    brow="#9C9388", age="old", robe="#2F5E8C", robe2="#EFE3CC", pose="hold", prop="seedling"),
        backdrop="grove", postcard="three_hundred", hero="seedling",
        stickers=["seedling", "spade", "dates", "fire", "road_tile", "star"],
    ),
    "bilal": dict(
        colour="#B5452F", colour2="#F2C46D", tint="#F6EBDD", time="dawn",
        art=_art(sky="#F8D9B8", sun="#F2C46D", far="#E8A98A", mid="#C97A66", near="#6E4A5E", road="#F3E2C2",
                 trunk="#6E4A5E", frond="#3E6E58", body="#EBD3B5", tile="#B5452F", shade="#5A3A4E",
                 accent="#B5452F", ink="#2A2230", shadow="#2A2230"),
        figure=_fig("deep", head="cap", head_c="#F5EFE3", hair="#1E1612", beard="short", beard_c="#1E1612",
                    robe="#E2A33C", robe2="#F6EBD5", pose="call", eyes="closed", mouth="open", cheek="#B5523A",
                    sound="#FFF4DC"),
        backdrop="rooftop_dawn", postcard="call_over_city", hero="sound",
        stickers=["rooftop", "sun_rays", "sound", "lantern", "star"],
    ),
    "abu-dharr": dict(
        colour="#4E6B3A", colour2="#D9A441", tint="#F2EEE2", time="dusk",
        art=_art(sky="#F3D3A6", sun="#E39A4A", far="#E2B57C", mid="#C98F5C", near="#8A6A4A", road="#F1DFC0",
                 trunk="#6B4A3A", frond="#4E6B3A", body="#E8D3B0", tile="#4E6B3A", shade="#4A3A44",
                 accent="#A4532E", ink="#2A2230", shadow="#2A2230", gold="#D9A441"),
        figure=_fig("brown", head="keffiyeh", head_c="#EDE4D3", head_c2="#BFAF95", beard="long", beard_c="#E8E2D8",
                    brow="#CFC8BC", age="old", robe="#7A5B44", mantle="#5E4636", pose="rest"),
        backdrop="palace", postcard="rabadha", hero="waterskin",
        stickers=["door", "coins", "city_gate", "waterskin", "star", "road_tile"],
    ),
}


DAY_DUNES = dict(sky="#F7E6C4", far="#E9C38A", mid="#D9A066")

PEOPLE.update({
    "sumayyah": _p("#6B3A5E", "#E8B04B", "#F4ECE4", "dawn",
        _pal("#6B3A5E", "#E8B04B", "#F8DCC4", "#E9B98A", "#D29A70", accent="#B5523A"),
        _woman("tan", "#4A2E44", "#6B3A5E", edge="#3A2236", age="old", brow="#8A7A70"),
        dict(els=[("city", 0.5, 0.62, 1.0), ("palm", 0.1, 0.66, 0.36), ("palm", 0.9, 0.66, 0.3)], sun=(0.82, 0.22)),
        dict(els=[("city", 0.55, 0.64, 1.1), ("palm", 0.12, 0.7, 0.42), ("hand_open", 0.82, 0.96, 0.62, "front")], sun=(0.84, 0.24)),
        "hand_open", ["hand_open", "milestone", "horizon", "bird", "star"]),
    "nusaybah": _p("#1F6E6A", "#E2A33C", "#EEF2EC", "day",
        _pal("#1F6E6A", "#E2A33C", "#F5E4C4", "#E2B57C", "#C98F5C", accent="#B5523A"),
        _woman("tan", "#2B4A48", "#1F6E6A", edge="#1A3836", pose="hold", prop="shield"),
        dict(els=[("hill", 0.24, 0.64, 0.75), ("hill", 0.8, 0.64, 0.55)], sun=(0.86, 0.16)),
        dict(els=[("hill", 0.42, 0.64, 0.7), ("waterskin", 0.82, 0.92, 0.5, "front")], sun=(0.84, 0.2)),
        "shield", ["shield", "waterskin", "scabbard", "star", "horizon"]),
    "umm-ayman": _p("#8E5A2B", "#F0C987", "#F6EEE2", "day",
        _pal("#8E5A2B", "#F0C987", "#F7E6C4", "#E9C38A", "#D9A066", body="#EBD3B0", shade="#4A3226"),
        _woman("brown", "#EDE3D0", "#8E5A2B", edge="#C8B48F", age="old", brow="#9C9388"),
        dict(els=[("house", 0.84, 0.66, 0.9), ("doorway", 0.16, 0.8, 0.95)], sun=(0.88, 0.14)),
        dict(els=[("doorway", 0.42, 0.9, 1.2), ("basket", 0.78, 0.94, 0.5, "front"), ("sandal", 0.9, 0.96, 0.3, "front")]),
        "basket", ["basket", "door_ajar", "sandal", "lamp", "star"]),
    "halima": _p("#C77A1E", "#2E5E7E", "#F7EEDD", "day",
        _pal("#C77A1E", "#2E5E7E", "#F7E6C4", "#E9C38A", "#D9A066", sun="#F2C46D", accent="#2E5E7E", beast="#9A6A44"),
        _woman("brown", "#2E5E7E", "#C77A1E", edge="#24485F", robe2="#F3E2C2"),
        dict(els=[("tents", 0.16, 0.64, 0.45), ("camel_big", 0.56, 0.74, 1.25)], sun=(0.86, 0.14)),
        dict(els=[("tent", 0.3, 0.68, 0.7), ("camel_big", 0.62, 0.86, 1.1)], sun=(0.84, 0.2)),
        "camel", ["camel", "tent", "horizon", "bird", "star"], dx=-0.12),
    "asma": _p("#5A4A8E", "#E8B04B", "#F1EEF4", "day",
        _pal("#5A4A8E", "#E8B04B", "#F6E6CC", "#E6C79A", "#D2A878", body="#EADCC4", shade="#3B2F55"),
        _woman("tan", "#5A4A8E", "#3F3466", edge="#463A72", pose="rest"),
        dict(els=[("doorway", 0.24, 0.86, 1.3)], sun=(0.86, 0.14)),
        dict(els=[("doorway", 0.36, 0.92, 1.2), ("lamp", 0.7, 0.94, 0.5, "front"), ("folded_cloth", 0.88, 0.96, 0.4, "front")]),
        "lamp", ["folded_cloth", "door_ajar", "lamp", "flower", "star"]),
    "fizza": _p("#3E7A4E", "#F2C46D", "#EEF2E8", "day",
        _pal("#3E7A4E", "#F2C46D", "#D7E8EE", "#E6D2AE", "#C9A47A", body="#EADCC0"),
        _woman("dark", "#3E7A4E", "#2E5E3C", edge="#2A5236", pose="rest"),
        dict(ground="room", gy=0.7, els=[("window", 0.8, 0.5, 0.6), ("table", 0, 0.9, 0, "front"),
                                         ("open_book", 0.78, 0.92, 0.42, "front"), ("jug", 0.16, 0.91, 0.4, "front")]),
        dict(ground="room", gy=0.72, els=[("window", 0.5, 0.48, 0.55), ("table", 0, 0.8, 0, "front"),
                                          ("open_book", 0.42, 0.82, 0.5, "front"), ("jug", 0.72, 0.81, 0.45, "front"),
                                          ("broom", 0.12, 0.98, 0.5, "front")]),
        "open_book", ["open_book", "jug", "broom", "lamp", "star"]),
    "maytham": _p("#9A3B2A", "#F2C46D", "#F6ECE0", "day",
        _pal("#9A3B2A", "#F2C46D", "#F7E6C4", "#E9C38A", "#D9A066", accent="#9A3B2A"),
        _fig("olive", head="turban", head_c="#EFE3CC", head_c2="#C8A97A", beard="full", beard_c="#3A2A20",
             hair="#3A2A20", robe="#C27A3A", robe2="#F3E2C2", pose="rest"),
        dict(els=[("awning", 0.1, 0.78, 0.9), ("awning", 0.9, 0.78, 0.9), ("counter", 0, 0.88, 0, "front"),
                  ("dates", 0.2, 0.89, 0.42, "front"), ("scales", 0.82, 0.9, 0.42, "front")], sun=(0.86, 0.12)),
        dict(els=[("awning", 0.3, 0.78, 1.0), ("awning", 0.72, 0.78, 0.9), ("basket", 0.5, 0.96, 0.5, "front")]),
        "dates", ["dates", "basket", "scales", "awning", "star"]),
    "qambar": _p("#2E7D9A", "#F2B53B", "#EDF3F4", "day",
        _pal("#2E7D9A", "#F2B53B", "#F5E7CC", "#E3C79C", "#CFA676", accent="#D9752E"),
        _fig("dark", head="cap", head_c="#F5EFE3", hair="#1E1612", beard="short", beard_c="#1E1612",
             robe="#F2B53B", robe2="#FFF4DC", mouth="smile"),
        dict(els=[("street", 0, 0.66, 0), ("awning", 0.84, 0.74, 0.8)], sun=(0.12, 0.14)),
        dict(els=[("street", 0, 0.7, 0), ("awning", 0.5, 0.86, 0.9), ("two_shirts", 0.84, 0.96, 0.5, "front")]),
        "two_shirts", ["two_shirts", "coins", "market", "door", "star"]),
    "malik": _p("#3D4F6E", "#E39A4A", "#EEF0F2", "day",
        _pal("#3D4F6E", "#E39A4A", "#F5E7CC", "#E3C79C", "#CFA676", accent="#E39A4A"),
        _fig("olive", head="turban", head_c="#E8E2D6", head_c2="#BDB3A2", beard="full", beard_c="#4A3A2E",
             hair="#4A3A2E", robe="#9A8A72", robe2="#E8E2D6"),
        dict(els=[("street", 0, 0.66, 0), ("awning", 0.1, 0.8, 0.8), ("awning", 0.9, 0.8, 0.7)], sun=(0.14, 0.12)),
        dict(els=[("street", 0, 0.7, 0), ("sealed_letter", 0.78, 0.96, 0.55, "front")]),
        "sealed_letter", ["market", "sealed_letter", "door", "road_tile", "star"], scale=1.1),
    "fatima-bint-asad": _p("#A84B5C", "#F0C987", "#F7EDEE", "day",
        _pal("#A84B5C", "#F0C987", "#F7E6C4", "#E9C38A", "#D9A066", body="#EBD3B0", shade="#4A2A32"),
        _woman("tan", "#A84B5C", "#7E3443", edge="#8E3E4C", face="light", pose="rest"),
        dict(els=[("doorway", 0.5, 0.86, 1.5), ("sandal", 0.12, 0.98, 0.42, "front"), ("sandal", 0.2, 0.99, 0.3, "front")],
             sun=(0.88, 0.14)),
        dict(els=[("doorway", 0.44, 0.9, 1.2), ("shared_meal", 0.78, 0.94, 0.5, "front"),
                  ("sandal", 0.14, 0.97, 0.36, "front"), ("sandal", 0.22, 0.98, 0.26, "front")]),
        "shared_meal", ["door_ajar", "shared_meal", "folded_cloth", "sandal", "star"]),
    "qais": _p("#7A2E2E", "#D9B25A", "#F4ECE6", "dusk",
        _pal("#7A2E2E", "#D9B25A", "#F3D3A6", "#E2B57C", "#C98F5C", accent="#7A2E2E"),
        _fig("olive", head="turban", head_c="#6A2A2A", head_c2="#4A1E1E", beard="full", beard_c="#2E221C",
             hair="#2E221C", robe="#8A7A62", mantle="#5A4A3A", belt="#3A2E26"),
        dict(els=[("tents", 0.5, 0.64, 1.0)], sun=(0.86, 0.16)),
        dict(els=[("tent", 0.32, 0.72, 0.9), ("treaty", 0.78, 0.96, 0.5, "front")], sun=(0.82, 0.24)),
        "scabbard", ["scabbard", "treaty", "tent", "flag", "star"]),
    "abbas": _p("#1F4E79", "#E8C15A", "#EBF0F5", "day",
        _pal("#1F4E79", "#E8C15A", "#F5E4C4", "#E2C08A", "#C9A06A", water="#5FA3BE", frond="#3E6E48"),
        _fig("olive", head="turban", head_c="#2E5E3C", head_c2="#1E4A2C", face="light", robe="#1F4E79",
             mantle="#163A5A", pose="hold", prop="waterskin"),
        dict(els=[("river", 0, 0.66, 0), ("tents", 0.18, 0.6, 0.35), ("palm", 0.86, 0.68, 0.34), ("palm", 0.94, 0.7, 0.28)],
             sun=(0.84, 0.14)),
        dict(els=[("river", 0, 0.7, 0), ("palm", 0.14, 0.72, 0.36), ("palm", 0.24, 0.74, 0.28),
                  ("tents", 0.74, 0.64, 0.3), ("waterskin", 0.5, 0.96, 0.5, "front")]),
        "waterskin", ["waterskin", "flag", "river", "bird", "star"]),
    "umm-kulthum": _p("#7E4E6E", "#E8C27A", "#F3EDF0", "dusk",
        _pal("#7E4E6E", "#E8C27A", "#F3D3A6", "#E2B57C", "#C98F5C"),
        _woman("tan", "#7E4E6E", "#5E3A52", edge="#6A425E", face="light"),
        dict(els=[("road", 0, 0.62, 0), ("milestone", 0.14, 0.8, 0.4)], sun=(0.86, 0.62, 1.3)),
        dict(els=[("road", 0, 0.6, 0), ("milestone", 0.82, 0.9, 0.5), ("sandal", 0.3, 0.96, 0.3, "front")], sun=(0.62, 0.58, 1.3)),
        "sandal", ["waterskin", "sandal", "milestone", "bird", "star"]),
    "rabab": _p("#4E5A7A", "#E3C58A", "#EFF0F3", "dusk",
        _pal("#4E5A7A", "#E3C58A", "#E8C6A4", "#D9B48C", "#B9A58A", body="#E4D8C6", shade="#3A3F55"),
        _woman("tan", "#4E5A7A", "#3A4460", edge="#424D6A", face="light", pose="rest"),
        dict(ground="room", gy=0.72, els=[("window", 0.78, 0.52, 0.6), ("lamp", 0.78, 0.53, 0.36)]),
        dict(ground="room", gy=0.74, els=[("window", 0.5, 0.5, 0.6), ("lamp", 0.5, 0.51, 0.4),
                                          ("folded_cloth", 0.78, 0.92, 0.5, "front")]),
        "lamp", ["folded_cloth", "lamp", "horizon", "bird", "star"]),
    "zaynab": _p("#6E2342", "#E8C15A", "#F4EBEE", "dawn",
        _pal("#6E2342", "#E8C15A", "#F8DCC4", "#E9B98A", "#D29A70"),
        _woman("tan", "#2E1E28", "#6E2342", edge="#241820", face="light"),
        dict(els=[("road", 0, 0.62, 0)], sun=(0.86, 0.62, 1.4)),
        dict(els=[("road", 0, 0.6, 0), ("milestone", 0.16, 0.9, 0.45)], sun=(0.62, 0.58, 1.4)),
        "raised_hand", ["raised_hand", "road_tile", "milestone", "bird", "star"]),
    "sakina": _p("#B5577A", "#F2D27A", "#F8EEF2", "day",
        _pal("#B5577A", "#F2D27A", "#D7E8EE", "#E6D2AE", "#D2B48E", body="#F0E2D0", accent="#B5577A"),
        _woman("light", "#B5577A", "#8E3E5E", edge="#9E4A6A", face="light", pose="hold", prop="flower"),
        dict(ground="room", gy=0.72, els=[("window", 0.8, 0.5, 0.55)]),
        dict(ground="room", gy=0.74, els=[("window", 0.5, 0.5, 0.6), ("flower", 0.5, 0.52, 0.32),
                                          ("folded_cloth", 0.2, 0.94, 0.42, "front")]),
        "flower", ["flower", "folded_cloth", "bird", "lamp", "star"], scale=0.84),
    "fitrus": _p("#1E2A4A", "#E8D6A0", "#ECEEF3", "night",
        _pal("#1E2A4A", "#E8D6A0", "#22284A", "#2E3458", "#3A4066", moon="#E8D6A0", star="#E8D6A0", accent="#E8D6A0"),
        None, "fitrus",
        dict(els=[("bird", 0.3, 0.4, 0.4), ("bird", 0.62, 0.3, 0.3), ("feather", 0.82, 0.96, 0.5, "front")], sun=(0.16, 0.2)),
        "feather", ["feather", "bird", "star_field", "horizon", "star"]),
    "umm-al-banin": _p("#7A6A2E", "#E8D29A", "#F3F0E4", "day",
        _pal("#7A6A2E", "#E8D29A", "#F7E6C4", "#E9C38A", "#D9A066", body="#EBD3B0", shade="#3E3622"),
        _woman("brown", "#4E4422", "#7A6A2E", edge="#3E3622", face="light", pose="rest"),
        dict(els=[("doorway", 0.5, 0.86, 1.5)], sun=(0.88, 0.14)),
        dict(els=[("doorway", 0.5, 0.9, 1.2), ("marks_four", 0.5, 0.97, 0.4, "front")]),
        "waterskin", ["door_ajar", "waterskin", "marks_four", "flower", "star"]),
    "ruqayya": _p("#8A6AA8", "#F2D27A", "#F3F0F6", "night",
        _pal("#8A6AA8", "#F2D27A", "#2E2A50", "#3A3460", "#C8B8D6", body="#E6DCEC", shade="#3A2E55"),
        _woman("light", "#8A6AA8", "#6A4E88", edge="#7A5E98", face="light", pose="rest"),
        dict(ground="room", gy=0.72, els=[("window", 0.8, 0.5, 0.55), ("lantern", 0.2, 0.42, 0.5)]),
        dict(ground="room", gy=0.74, els=[("window", 0.5, 0.5, 0.62), ("lantern", 0.5, 0.5, 0.36),
                                          ("flower", 0.82, 0.96, 0.4, "front")]),
        "lantern", ["lantern", "flower", "bird", "folded_cloth", "star"], scale=0.74),
    "tawus": _p("#2E3A6E", "#F2C46D", "#EDEFF5", "night",
        _pal("#2E3A6E", "#F2C46D", "#1F2340", "#2A2E50", "#363A60", accent="#F2C46D"),
        _fig("olive", head="turban", head_c="#E8E2D6", head_c2="#BDB3A2", beard="full", beard_c="#3A2E26",
             hair="#3A2E26", robe="#4A4E6E", robe2="#C8C2B2", pose="rest"),
        dict(ground="dark", gy=0.74, els=[("light", 0.84, 0.74, 0.7)]),
        dict(ground="dark", gy=0.7, els=[("window", 0.5, 0.62, 0.9), ("star", 0.5, 0.5, 0.25), ("lamp", 0.78, 0.94, 0.45, "front"),
                                          ("mat", 0.28, 0.98, 0.5, "front")]),
        "lamp", ["star_field", "mat", "lamp", "bird", "star"], dx=-0.1),
    "jabir": _p("#A86A2E", "#2E5E7E", "#F6EFE4", "day",
        _pal("#A86A2E", "#2E5E7E", "#F7E6C4", "#E9C38A", "#D9A066", body="#EBD3B0", shade="#3E2E22", accent="#2E5E7E"),
        _fig("brown", head="turban", head_c="#EDE4D3", head_c2="#BFAF95", beard="long", beard_c="#ECE6DA",
             brow="#D2CBBF", age="old", eyes="closed", robe="#A86A2E", robe2="#F3E2C2", pose="hold", prop="cane"),
        dict(els=[("doorway", 0.22, 0.86, 1.3)], sun=(0.88, 0.14)),
        dict(els=[("doorway", 0.5, 0.9, 1.3), ("pair", 0.82, 0.96, 0.42, "front")]),
        "pair", ["door_ajar", "pair", "hand_open", "bird", "star"]),
    "hisham": _p("#2E6E5E", "#F2B53B", "#EDF3F0", "day",
        _pal("#2E6E5E", "#F2B53B", "#F5E7CC", "#E3C79C", "#C9A47A", body="#EADCC4", shade="#2E3A36"),
        _fig("tan", head="turban", head_c="#F3EEE2", head_c2="#C8BFA8", beard="short", beard_c="#2B211C",
             robe="#2E6E5E", robe2="#F3E2C2", pose="raise"),
        dict(ground="room", gy=0.7, els=[("window", 0.16, 0.48, 0.5), ("window", 0.84, 0.48, 0.5),
                                         ("seated", 0.5, 1.02, 0.9, "front")]),
        dict(ground="room", gy=0.72, els=[("seat_circle", 0.5, 0.86, 1.1), ("plain_scroll", 0.82, 0.96, 0.45, "front")]),
        "plain_scroll", ["plain_scroll", "raised_hand", "seat_circle", "inkwell", "star"]),
    "umm-farwa": _p("#9A5A7A", "#F0C987", "#F6EEF2", "day",
        _pal("#9A5A7A", "#F0C987", "#D7E8EE", "#E6D2AE", "#D2B48E", body="#EFE2D6", shade="#3E2A36"),
        _woman("tan", "#9A5A7A", "#74425C", edge="#86506C", face="light", pose="hold", prop="book"),
        dict(ground="room", gy=0.72, els=[("window", 0.82, 0.5, 0.55), ("doorway", 0.16, 0.74, 0.7)]),
        dict(ground="room", gy=0.74, els=[("window", 0.62, 0.5, 0.6), ("table", 0, 0.82, 0, "front"),
                                          ("open_book", 0.4, 0.84, 0.5, "front")]),
        "open_book", ["open_book", "door_ajar", "lamp", "flower", "star"]),
    "safwan": _p("#B0703A", "#2E4E6E", "#F6EFE6", "dusk",
        _pal("#B0703A", "#2E4E6E", "#F3D3A6", "#E2B57C", "#C98F5C", accent="#2E4E6E"),
        _fig("olive", head="keffiyeh", head_c="#EDE4D3", head_c2="#BFAF95", cord="#2A2230", beard="full",
             beard_c="#3A2A20", hair="#3A2A20", robe="#B0703A", robe2="#F3E2C2"),
        dict(els=[("tether", 0.84, 0.74, 0.7)], sun=(0.16, 0.2)),
        dict(els=[("tether", 0.5, 0.86, 1.2), ("harness", 0.5, 0.8, 0.4)], sun=(0.2, 0.3)),
        "harness", ["harness", "coins", "tether", "horizon", "star"], dx=-0.1),
    "hamida": _p("#6A4A7E", "#F0C987", "#F2EEF4", "day",
        _pal("#6A4A7E", "#F0C987", "#D7E8EE", "#E6D2AE", "#CDB4A0", body="#EDE2E6", shade="#3A2A46"),
        _woman("tan", "#6A4A7E", "#4E3660", edge="#5E426E", face="light", pose="hold", prop="book"),
        dict(ground="room", gy=0.7, els=[("window", 0.84, 0.48, 0.5), ("seated", 0.5, 1.03, 0.9, "front")]),
        dict(ground="room", gy=0.74, els=[("window", 0.5, 0.5, 0.6), ("seat_circle", 0.5, 0.92, 1.0, "front")]),
        "seat_circle", ["open_book", "seat_circle", "lamp", "flower", "star"]),
    "dibil": _p("#8E2E2E", "#E8C15A", "#F5ECEA", "dusk",
        _pal("#8E2E2E", "#E8C15A", "#F3D3A6", "#E2B57C", "#C98F5C", body="#E8D3B0", shade="#3A2626"),
        _fig("olive", head="turban", head_c="#8E2E2E", head_c2="#6A1E1E", beard="full", beard_c="#2E221C",
             hair="#2E221C", robe="#E8D3B0", mantle="#6A5A4A", pose="raise", mouth="open"),
        dict(els=[("arcade", 0.5, 0.66, 1.2)], sun=(0.88, 0.14)),
        dict(ground="room", gy=0.74, els=[("window", 0.5, 0.5, 0.6), ("table", 0, 0.82, 0, "front"),
                                          ("plain_scroll", 0.38, 0.86, 0.5, "front"), ("inkwell", 0.66, 0.86, 0.45, "front")]),
        "plain_scroll", ["plain_scroll", "inkwell", "folded_cloth", "raised_hand", "star"]),
    "masuma": _p("#2E6E8E", "#F0C987", "#EDF2F5", "dusk",
        _pal("#2E6E8E", "#F0C987", "#F3D3A6", "#E2B57C", "#C98F5C", dome="#2E6E8E", body="#E8D3B0"),
        _woman("tan", "#2E6E8E", "#22546C", edge="#285E7A", face="light"),
        dict(els=[("road", 0, 0.62, 0), ("shrine", 0.84, 0.64, 0.42)], sun=(0.14, 0.2)),
        dict(els=[("road", 0, 0.62, 0), ("shrine", 0.62, 0.62, 0.36), ("milestone", 0.16, 0.92, 0.45)], sun=(0.86, 0.22)),
        "dome", ["road_tile", "dome", "milestone", "bird", "star"]),
    "ali-ibn-mahziyar": _p("#1E5E7A", "#E39A4A", "#ECF2F4", "day",
        _pal("#1E5E7A", "#E39A4A", "#E4EEF0", "#E3C79C", "#CFA676", water="#4F8FA8", accent="#E39A4A"),
        _fig("olive", head="turban", head_c="#EDE4D3", head_c2="#BFAF95", beard="full", beard_c="#3A2E26",
             hair="#3A2E26", robe="#1E5E7A", robe2="#E8E2D6"),
        dict(ground="sea", gy=0.6, els=[("ship", 0.8, 0.66, 0.8), ("dock", 0, 0.84, 0, "front"),
                                        ("crate", 0.12, 0.94, 0.5, "front"), ("crate", 0.2, 0.86, 0.36, "front")]),
        dict(ground="sea", gy=0.56, els=[("ship", 0.6, 0.66, 0.6), ("dock", 0, 0.76, 0, "front"),
                                         ("crate", 0.2, 0.9, 0.42, "front"), ("rope", 0.82, 0.92, 0.4, "front")]),
        "ship_wheel", ["ship_wheel", "crate", "rope", "sealed_letter", "star"]),
    "abu-hashim": _p("#6E5A3A", "#E8B04B", "#F3EFE8", "day",
        _pal("#6E5A3A", "#E8B04B", "#D7E8EE", "#E6D2AE", "#C2A47E", body="#E8DCC6", shade="#3A3226"),
        _fig("olive", head="turban", head_c="#E8E2D6", head_c2="#BDB3A2", beard="full", beard_c="#9C9388",
             brow="#8A8278", age="old", robe="#6E5A3A", robe2="#E8E2D6", pose="rest"),
        dict(ground="room", gy=0.7, els=[("window", 0.16, 0.48, 0.5), ("table", 0, 0.9, 0, "front"),
                                         ("parcel", 0.8, 0.92, 0.45, "front")]),
        dict(ground="room", gy=0.74, els=[("doorway", 0.22, 0.76, 0.6), ("table", 0, 0.82, 0, "front"),
                                          ("parcel", 0.6, 0.86, 0.55, "front")]),
        "parcel", ["parcel", "door_ajar", "lamp", "coins", "star"]),
    "ahmad-ibn-ishaq": _p("#5E6E2E", "#E8B04B", "#F2F2E8", "day",
        _pal("#5E6E2E", "#E8B04B", "#F7E6C4", "#E9C38A", "#D9A066", body="#E8D3B0"),
        _fig("tan", head="turban", head_c="#EDE4D3", head_c2="#BFAF95", beard="full", beard_c="#3A2E26",
             hair="#3A2E26", robe="#5E6E2E", robe2="#F3E2C2", pose="hold", prop="satchel"),
        dict(els=[("city", 0.16, 0.62, 0.7), ("road", 0, 0.62, 0)], sun=(0.86, 0.16)),
        dict(els=[("city", 0.2, 0.6, 0.8), ("road", 0, 0.6, 0), ("milestone", 0.84, 0.92, 0.45)], sun=(0.86, 0.2)),
        "satchel", ["satchel", "sealed_letter", "milestone", "road_tile", "star"]),
    "uthman": _p("#9A6A1E", "#2E5E7E", "#F6F0E2", "day",
        _pal("#9A6A1E", "#2E5E7E", "#F7E6C4", "#E9C38A", "#D9A066", body="#E8D3B0", accent="#9A6A1E"),
        _fig("olive", head="turban", head_c="#EDE4D3", head_c2="#BFAF95", beard="full", beard_c="#B8B0A4",
             brow="#9C9388", age="old", robe="#9A6A1E", robe2="#F3E2C2", pose="rest"),
        dict(els=[("stall", 0.5, 0.86, 1.3), ("counter", 0, 0.88, 0, "front"), ("scales", 0.82, 0.9, 0.4, "front")],
             sun=(0.1, 0.1)),
        dict(els=[("stall", 0.5, 0.92, 1.0), ("sealed_letter", 0.84, 0.96, 0.4, "front")]),
        "oil_jar", ["oil_jar", "scales", "sealed_letter", "market", "star"]),
    "muhammad-ibn-uthman": _p("#7A5A1E", "#2E5E7E", "#F4EFE2", "day",
        _pal("#7A5A1E", "#2E5E7E", "#F7E6C4", "#E9C38A", "#D9A066", body="#E8D3B0", accent="#9A6A1E"),
        _fig("olive", head="turban", head_c="#EDE4D3", head_c2="#BFAF95", beard="long", beard_c="#ECE6DA",
             brow="#D2CBBF", age="old", robe="#7A5A1E", robe2="#F3E2C2", pose="rest"),
        dict(els=[("stall", 0.5, 0.86, 1.3), ("counter", 0, 0.88, 0, "front"), ("scales", 0.82, 0.9, 0.4, "front")],
             sun=(0.1, 0.1)),
        dict(els=[("stall", 0.5, 0.92, 1.0), ("oil_jar", 0.16, 0.96, 0.45, "front")]),
        "oil_jar", ["oil_jar", "scales", "sealed_letter", "coins", "star"]),
    "husayn-ibn-ruh": _p("#3A4A5A", "#E3C58A", "#EEF0F2", "day",
        _pal("#3A4A5A", "#E3C58A", "#D7E8EE", "#E6D2AE", "#BBA588", body="#E4DCCE", shade="#2E3640"),
        _fig("tan", head="turban", head_c="#3A4A5A", head_c2="#2A3640", beard="full", beard_c="#2E221C",
             hair="#2E221C", robe="#E4DCCE", mantle="#3A4A5A", pose="rest"),
        dict(ground="room", gy=0.7, els=[("window", 0.84, 0.48, 0.5), ("table", 0, 0.9, 0, "front")]),
        dict(ground="room", gy=0.74, els=[("door_closed", 0.3, 0.78, 0.8), ("chest", 0.68, 0.94, 0.6, "front")]),
        "chest", ["door_closed", "chest", "sealed_letter", "lamp", "star"]),
    "al-samarri": _p("#5A3A2E", "#E8C15A", "#F3EEEA", "dusk",
        _pal("#5A3A2E", "#E8C15A", "#E8C6A4", "#D9B48C", "#B9A58A", body="#E4D8C6", shade="#3A2A22"),
        _fig("olive", head="turban", head_c="#EDE4D3", head_c2="#BFAF95", beard="long", beard_c="#ECE6DA",
             brow="#D2CBBF", age="old", robe="#5A3A2E", robe2="#E8E2D6", pose="hold", prop="letter"),
        dict(ground="room", gy=0.72, els=[("window", 0.8, 0.5, 0.55)]),
        dict(ground="room", gy=0.74, els=[("door_ajar", 0.42, 0.78, 0.9), ("sealed_letter", 0.74, 0.94, 0.45, "front")]),
        "sealed_letter", ["sealed_letter", "door_ajar", "lamp", "milestone", "star"]),
    "narjis": _p("#4A6A8A", "#F0C987", "#EEF1F5", "night",
        _pal("#4A6A8A", "#F0C987", "#2E2A50", "#3A3460", "#C0B4C8", body="#E2DCE6", shade="#2E3646"),
        _woman("light", "#4A6A8A", "#34506C", edge="#3E5E7C", face="light", pose="rest"),
        dict(ground="room", gy=0.72, els=[("doorway", 0.2, 0.74, 0.72), ("lamp", 0.84, 0.72, 0.36)]),
        dict(ground="room", gy=0.74, els=[("door_closed", 0.5, 0.78, 0.9), ("lamp", 0.78, 0.94, 0.45, "front")]),
        "lamp", ["door_closed", "lamp", "flower", "bird", "star"]),
    "khawla": _p("#8A3A1E", "#E8C15A", "#F6EDE6", "day",
        _pal("#8A3A1E", "#E8C15A", "#F5E4C4", "#E2C08A", "#C9A06A", accent="#8A3A1E"),
        _fig("tan", head="helmet", head_c="#8E9496", head_c2="#6E7476", cap_c="#9AA0A2", robe="#7A6A5A",
             mantle="#8A3A1E", belt="#3A2E26", pose="hold", prop="reins"),
        dict(els=[("tents", 0.2, 0.64, 0.4)], sun=(0.16, 0.16)),
        dict(els=[("standard", 0.7, 0.9, 0.5), ("helmet", 0.24, 0.96, 0.5, "front")], sun=(0.2, 0.24)),
        "helmet", ["helmet", "reins", "flag", "horizon", "star"], dx=-0.12),
})

for _slug in VEILED:
    assert PEOPLE[_slug]["figure"].get("face") == "light", _slug

# Batches, in card order (00-foundations/hadith-assignments.json "n"). The
# builder writes only the companions in a finished batch.
import companion_sources as _S

BATCHES = [_S.ALL[i:i + 3] for i in range(0, len(_S.ALL), 3)]
BUILT = [s for b in BATCHES for s in b]
