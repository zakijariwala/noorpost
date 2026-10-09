"""Read everything one envelope prints from its source files.

Envelope 03 lives in 01-pilot/envelope-03/ across four files; the other
thirteen are one file each in 03-content/. Either way this returns the same
shape, so the builder never knows where a word came from — only that it came
from source. Nothing here is retyped or summarised.
"""

import io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_print_templates import letter_voices, inline
from build_site import ENVELOPES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PILOT = os.path.join(ROOT, "01-pilot", "envelope-03")
CONTENT = os.path.join(ROOT, "03-content")


def _lines(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def _section(lines, head):
    """Lines under the first '## <head>…' heading, up to the next '## '."""
    out, on = [], False
    for ln in lines:
        if ln.startswith("## "):
            if on:
                break
            on = ln.startswith("## " + head)
            continue
        if on:
            out.append(ln)
    return out


def _quote_blocks(lines):
    """A '> ' quoted block split on its '> ---' rules into lists of lines."""
    body = [ln[1:].strip() for ln in lines if ln.startswith(">")]
    blocks, cur = [], []
    for s in body:
        if s == "---":
            blocks.append(cur); cur = []
        elif s:
            cur.append(s)
    blocks.append(cur)
    return [b for b in blocks if b]


def _saying(nn):
    with io.open(os.path.join(ROOT, "00-foundations", "hadith-assignments.json"), encoding="utf-8") as f:
        for b in json.load(f)["box"]:
            if b["envelope"] == nn:
                return b
    raise SystemExit(f"no box saying for envelope {nn}")


def _name(caps):
    """IMAM JA'FAR AL-SADIQ -> Imam Ja'far al-Sadiq."""
    words = []
    for w in caps.lower().split():
        if w in ("ibn", "bint"):
            words.append(w if words else w.capitalize())
        elif w.startswith("al-"):
            words.append("al-" + w[3:4].upper() + w[4:])
        else:
            words.append(w[:1].upper() + w[1:])
    return " ".join(words)


def fact_panel(lines):
    """The fact-panel skeleton: name, honorific, dates, bullets, then the death
    line and anything after it (standard lines), and the credit."""
    out = {"bullets": [], "after": [], "honorific": "", "dates": "", "credit": ""}
    seen_name = False
    for ln in lines:
        s = ln.strip()
        if s.startswith("## ") and seen_name:
            break
        if s.startswith("### "):
            out["name"] = _name(s[4:].strip())
            seen_name = True
            continue
        if not seen_name or not s or s == "---":
            continue
        if s.startswith("*(") and not out["honorific"]:
            out["honorific"] = s.strip("*")
        elif re.match(r"^\*\*(b\.|d\.|c\.)", s) and not out["dates"]:
            out["dates"] = s.strip("*")
        elif s.startswith("● "):
            out["bullets"].append(inline(s[2:]))
        elif s.startswith("<sub>"):
            out["credit"] = inline(re.sub(r"</?sub>", "", s))
        elif s.startswith("**Every") or s.startswith("Follows"):
            continue
        else:
            out["after"].append(inline(s))
    if "name" not in out:
        raise SystemExit("fact panel has no ### name")
    return out


def _conversation(blocks):
    """Title, the line under it, then every numbered question. A question starts
    at a line opening **N.** or **Last** — wherever it falls, including in the
    same block as the title (05–14 put question 1 there; 03 does not)."""
    title = blocks[0][0].lstrip("#").strip()
    sub = blocks[0][1].strip("*") if len(blocks[0]) > 1 else ""
    chunks, cur = [], None
    for b in blocks:
        for ln in b:
            if re.match(r"\*\*(\d+|Last)[.:]\*\*", ln):
                cur = [ln]; chunks.append(cur)
            elif cur is not None:
                cur.append(ln)
        cur = None
    qs = []
    for c in chunks:
        m = re.match(r"\*\*(\d+|Last)[.:]\*\*\s*(.*)", " ".join(c))
        label, rest = m.group(1), m.group(2)
        flag = None
        f = re.match(r"([●⚑])\s*\*\*(.+?)\*\*\s*(.*)", rest)
        if f:
            flag, rest = f"{f.group(1)} {f.group(2)}", f.group(3)
        qs.append((label, flag, inline(rest)))
    return {"kind": "conversation", "title": title, "sub": sub, "questions": qs}


def _prose(kind, blocks):
    """Mourning and Open cards: a title, a line under it, then blocks of prose,
    set as written."""
    title = blocks[0][0].lstrip("#").strip()
    sub = blocks[0][1].strip("*") if len(blocks[0]) > 1 else ""
    rest = ([blocks[0][2:]] if len(blocks[0]) > 2 else []) + blocks[1:]
    return {"kind": kind, "title": title, "sub": sub,
            "blocks": [[inline(s) for s in b] for b in rest]}


def _case_file(lines):
    q, ev, instr, answer = "", [], "", []
    part = None
    cur = None
    for ln in lines:
        s = ln.strip()
        if s.startswith("### "):
            part = s[4:].lower(); continue
        if not s or s == "---":
            continue
        if part == "the question" and s.startswith("**"):
            q = inline(s.strip("*"))
        elif part == "the five evidence cards" and s.startswith(">"):
            t = s[1:].strip()
            m = re.match(r"\*\*EVIDENCE (\d+)\*\*", t)
            if m:
                cur = {"n": m.group(1), "text": []}; ev.append(cur)
            elif t and cur:
                cur["text"].append(inline(t))
        elif part == "the sealed answer":
            if s.startswith(">"):
                t = s[1:].strip()
                if t:
                    answer.append(inline(t))
            elif s.startswith("*"):
                instr = inline(s)
    return {"kind": "case", "title": "The case file", "question": q, "evidence": ev,
            "instruction": instr, "answer": answer}


def load(nn):
    nn = "%02d" % int(nn)
    num, month, masoom, session_type = next(e for e in ENVELOPES if e[0] == nn)
    if nn == "03":
        letter = _lines(os.path.join(PILOT, "letter.md"))
        panel_lines = _lines(os.path.join(PILOT, "fact-panel.md"))
        panel_lines = panel_lines[:next((i for i, l in enumerate(panel_lines)
                                         if l.startswith("## The one new thing")), len(panel_lines))]
        sess = _conversation(_quote_blocks(_section(_lines(os.path.join(PILOT, "session-card.md")), "Card front")))
        items = _lines(os.path.join(PILOT, "items.md"))
        stamp = "RABI AL-AWWAL"
    else:
        doc = _lines(os.path.join(CONTENT, f"envelope-{nn}.md"))
        letter = doc
        panel_lines = _section(doc, "Fact panel")
        if any(l.startswith("## Case File") for l in doc):
            sess = _case_file(_section(doc, "Case File"))
        else:
            head = next(l for l in doc if l.startswith("## Session card"))
            kind = head.split("—")[-1].strip().lower()
            blocks = _quote_blocks(_section(doc, "Session card"))
            sess = _conversation(blocks) if kind == "conversation" else _prose(kind, blocks)
        items = doc
        ext = next((l for l in doc if l.startswith("**Exterior:**")), "")
        m = re.search(r"cancellation reading \*\*(.+?)\*\*", ext)
        stamp = m.group(1) if m else month.upper()

    title_line = next(l for l in letter if l.startswith("## Letter"))
    title = re.search(r"\*(.+?)\*", title_line).group(1)
    voices = letter_voices(letter)
    if not voices or 'class="voice together"' not in voices[-1]:
        raise SystemExit(f"envelope {nn}: the letter's last line is not the ●○ line")

    return {
        "nn": nn, "month": month, "masoom": masoom, "session_type": session_type,
        "stamp": stamp, "title": title, "voices": voices,
        "panel": fact_panel(panel_lines if nn != "03" else panel_lines),
        "session": sess, "saying": _saying(nn),
        "mourning": nn in ("01", "02"),
    }


ALL = ["%02d" % i for i in range(1, 15)]
