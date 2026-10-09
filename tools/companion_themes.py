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
    "olive": ("#C99872", "#A87652"),
    "brown": ("#B88A66", "#9A6E4C"),
    "deep": ("#6B4430", "#553424"),
}


def _fig(skin, **kw):
    s, sh = SKIN[skin]
    return dict(skin=s, skin_sh=sh, **kw)


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

# Batches, in card order (00-foundations/hadith-assignments.json "n"). The
# builder writes only the companions in a finished batch.
BATCHES = [["salman", "bilal", "abu-dharr"]]
BUILT = [s for b in BATCHES for s in b]
