"""Read one companion envelope from source — every word, nothing written here.

    load("salman") -> dict(slug, name, title, points, voices, panel, saying, n)

The letter and fact panel come from 08-companions/<slug>.md through the same
parser that writes the plain print templates (tools/build_print_templates.py),
so the two can never disagree. The saying comes from
00-foundations/hadith-assignments.json, the single record of what is on a card.
"""

import io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_print_templates as T

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with io.open(os.path.join(ROOT, "00-foundations", "hadith-assignments.json"), encoding="utf-8") as _f:
    _ASSIGN = {a["slug"]: a for a in json.load(_f)["assignments"]}

ALL = [a["slug"] for a in sorted(_ASSIGN.values(), key=lambda a: a["n"])]


def load(slug):
    lines = T.read(slug)
    points = ""
    for ln in lines:
        m = re.match(r"^\*\*Points home:\*\* \*(.+?)\*", ln)
        if m:
            points = m.group(1)
            break
    heading, parts = T.fact_panel(lines)
    a = dict(_ASSIGN[slug])
    return dict(slug=slug, name=T.name_of(lines), title=T.letter_title(lines), points=points,
                voices=T.letter_voices(lines), panel=dict(heading=heading, parts=parts),
                saying=a, n=a["n"], items=T.items(lines))
