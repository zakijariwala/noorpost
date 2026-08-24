"""Reading and validating the source, claim and citation metadata.

Four files, all hand-editable, all under 00-sources/metadata/:

    sources.yaml     works and the fixed editions of them
    rejected.yaml    works that may never re-enter the project
    claims.yaml      one record per claim that reaches print (TV -> V)
    citations.yaml   one record per claim-to-page link

The database is built from these. They are the thing a human edits; the
database is the thing an agent queries.
"""

import json
import os

from . import config

try:
    import yaml
except ImportError:                                          # pragma: no cover
    yaml = None


class MetadataError(Exception):
    pass


def _require_yaml():
    if yaml is None:
        raise MetadataError(
            "PyYAML is needed to read 00-sources/metadata/*.yaml — pip install -r requirements.txt")


def load_yaml(path, default=None):
    if not os.path.exists(path):
        if default is not None:
            return default
        raise MetadataError("missing metadata file: %s" % path)
    _require_yaml()
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or (default if default is not None else {})


def dump_yaml(path, data, header=None):
    _require_yaml()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        if header:
            f.write(header.rstrip("\n") + "\n\n")
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=100,
                       default_flow_style=False)


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------

def load_sources():
    """(works, editions, by_id). Editions carry their work fields merged in."""
    doc = load_yaml(config.SOURCES_YAML)
    works = {w["work_id"]: w for w in doc.get("works", [])}
    editions = []
    for e in doc.get("editions", []):
        w = works.get(e.get("work_id"))
        if w is None:
            raise MetadataError("edition %s names unknown work_id %r"
                                % (e.get("source_id"), e.get("work_id")))
        merged = dict(e)
        merged["work"] = w.get("work")
        merged["author"] = w.get("author")
        merged["tradition"] = w.get("tradition")
        merged["priority_rank"] = w.get("priority_rank")
        editions.append(merged)
    return works, editions, {e["source_id"]: e for e in editions}


def load_rejected():
    doc = load_yaml(config.REJECTED_YAML, default={"rejected": []})
    return doc.get("rejected", [])


def rejected_index(rejected=None):
    """(sha256 set, lowercase name/alias set) for the ingest guard."""
    rejected = load_rejected() if rejected is None else rejected
    hashes, names = set(), set()
    for r in rejected:
        for h in r.get("sha256", []) or []:
            hashes.add(h.lower())
        names.add((r.get("work") or "").strip().lower())
        for a in r.get("aliases", []) or []:
            names.add(a.strip().lower())
        for f in r.get("files", []) or []:
            names.add(os.path.splitext(os.path.basename(f))[0].strip().lower())
    names.discard("")
    return hashes, names


def is_rejected(*, sha256=None, name=None, filename=None, index=None):
    hashes, names = index or rejected_index()
    if sha256 and sha256.lower() in hashes:
        return True
    for candidate in (name, filename and os.path.splitext(os.path.basename(filename))[0]):
        if not candidate:
            continue
        c = candidate.strip().lower()
        if c in names:
            return True
        for n in names:
            if n and (n in c or c in n):
                return True
    return False


def active_editions(editions):
    """Editions that may be retrieved from. Rejected and missing never are."""
    return [e for e in editions if e.get("status") in ("fixed", "candidate",
                                                       "verification-required",
                                                       "manuscript")]


def alias_map(editions):
    """Lowercase work/alias string -> source_id, for resolving the work names
    written on the citation sheet by hand."""
    out = {}
    for e in editions:
        for key in [e.get("work"), e.get("volume_title"), e.get("source_id")]:
            if key:
                out.setdefault(key.strip().lower(), e["source_id"])
        for a in e.get("aliases", []) or []:
            out.setdefault(a.strip().lower(), e["source_id"])
    return out


# --------------------------------------------------------------------------
# claims and citations
# --------------------------------------------------------------------------

def load_claims():
    return load_yaml(config.CLAIMS_YAML, default={"claims": []}).get("claims", [])


def load_citations():
    return load_yaml(config.CITATIONS_YAML, default={"citations": []}).get("citations", [])


def load_fetch_manifest():
    if not os.path.exists(config.FETCH_MANIFEST):
        return {}
    with open(config.FETCH_MANIFEST, encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------

def validate(works, editions, claims, citations, rejected):
    """Returns a list of problem strings. Empty means the metadata is coherent.

    This is the machine-readable form of the rules in
    00-foundations/sourcing-rules.md and 00-foundations/source-truth-rules.md.
    """
    problems = []
    idx = rejected_index(rejected)
    seen = set()

    for e in editions:
        sid = e.get("source_id")
        if not sid:
            problems.append("an edition has no source_id")
            continue
        if sid in seen:
            problems.append("duplicate source_id %s" % sid)
        seen.add(sid)
        if e.get("status") not in config.EDITION_STATUS:
            problems.append("%s: status %r is not one of %s"
                            % (sid, e.get("status"), ", ".join(config.EDITION_STATUS)))
        if e.get("pagination") not in config.PAGINATION:
            problems.append("%s: pagination %r is not one of %s"
                            % (sid, e.get("pagination"), ", ".join(config.PAGINATION)))
        if e.get("citation_unit") not in config.CITATION_TYPES:
            problems.append("%s: citation_unit %r is not one of %s"
                            % (sid, e.get("citation_unit"), ", ".join(config.CITATION_TYPES)))
        # Rule: nothing incomplete is ever "fixed".
        if e.get("status") == "fixed":
            if e.get("complete") is False:
                problems.append("%s is marked fixed but complete: false" % sid)
            if not e.get("translator"):
                problems.append("%s is marked fixed but has no translator" % sid)
        # Rule: a manuscript must say why it is one, and may never be fixed.
        # The classification is the whole protection — an unpublished draft that
        # loses its label reads exactly like a published edition.
        if e.get("status") == "manuscript" and not e.get("manuscript_note"):
            problems.append("%s is status manuscript but carries no manuscript_note "
                            "explaining why it is admitted" % sid)
        # Rule: a rejected work may not appear in the active manifest.
        if e.get("status") != "rejected" and is_rejected(
                name=e.get("work"), filename=e.get("file"), sha256=e.get("sha256"), index=idx):
            problems.append("%s (%s) is on the rejected list but is active in sources.yaml"
                            % (sid, e.get("work")))

    by_id = {e["source_id"]: e for e in editions}
    claim_ids = set()
    for c in claims:
        cid = c.get("claim_id")
        if not cid:
            problems.append("a claim has no claim_id")
            continue
        if cid in claim_ids:
            problems.append("duplicate claim_id %s" % cid)
        claim_ids.add(cid)
        if c.get("status") not in config.CLAIM_STATUS:
            problems.append("%s: status %r is not one of %s"
                            % (cid, c.get("status"), ", ".join(config.CLAIM_STATUS)))

    cite_by_claim = {}
    for ct in citations:
        cid = ct.get("citation_id")
        claim_id = ct.get("claim_id")
        sid = ct.get("source_id")
        if claim_id and claim_id not in claim_ids:
            problems.append("%s points at unknown claim %s" % (cid, claim_id))
        if sid and sid not in by_id:
            problems.append("%s points at unknown source %s" % (cid, sid))
        elif sid and by_id[sid].get("status") == "rejected":
            problems.append("%s cites rejected source %s" % (cid, sid))
        if ct.get("citation_type") not in config.CITATION_TYPES:
            problems.append("%s: citation_type %r is not one of %s"
                            % (cid, ct.get("citation_type"), ", ".join(config.CITATION_TYPES)))
        if not ct.get("ref") and ct.get("page_start") is None:
            problems.append("%s has neither a ref nor a page — a citation without a "
                            "number is decoration" % cid)
        cite_by_claim.setdefault(claim_id, []).append(ct)

    # Rule: TV is not V. A claim is only V with a citation that names a
    # permitted edition and a number.
    for c in claims:
        if c.get("status") != "V":
            continue
        cites = cite_by_claim.get(c["claim_id"], [])
        usable = [ct for ct in cites
                  if ct.get("source_id") in by_id
                  and by_id[ct["source_id"]].get("status") != "rejected"
                  and (ct.get("ref") or ct.get("page_start") is not None)]
        if not usable:
            problems.append("%s is marked V with no usable citation" % c["claim_id"])

    return problems
