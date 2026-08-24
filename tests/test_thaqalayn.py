"""The Thaqalayn API path: snapshots, pinning, and one record -> one passage.

Nothing here touches the network. The API is mutable by design — re-scraped
weekly upstream — so a test that called it would be testing today's scrape, not
this code. What is worth pinning down is everything between the snapshot on
disk and the passage in the database.
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "tools"))

from sourcelib import config, metadata, thaqalayn as tq


def record(**kw):
    base = {
        "id": 7,
        "bookId": "Al-Kafi-Volume-2-Kulayni",
        "book": "Al-Kāfi",
        "author": "al-Kulayni",
        "translator": "Muhammad Sarwar",
        "category": "The Book of Faith and Disbelief",
        "categoryId": "2",
        "chapter": "The Chapter on Good Manners",
        "volume": 2,
        "englishText": "1. He said: whoever keeps a promise has kept a trust.",
        "arabicText": "من وفى بعهده",
    }
    base.update(kw)
    return base


class SnapshotTest(unittest.TestCase):

    def test_render_is_deterministic(self):
        """Two renderings of the same records are byte-identical. Without this
        the sha256 pin is noise and --check would report drift every run."""
        recs = [record(id=2), record(id=1)]
        a = tq.render_jsonl(sorted(recs, key=lambda r: r["id"]))
        b = tq.render_jsonl(sorted(list(reversed(recs)), key=lambda r: r["id"]))
        self.assertEqual(a, b)
        self.assertEqual(tq.sha256_text(a), tq.sha256_text(b))

    def test_line_separator_does_not_split_a_record(self):
        """U+2028 is not escaped by json.dumps and IS a line break to
        str.splitlines(). Reading with splitlines() cuts a record in half; this
        is the bug that broke the first real build."""
        body = tq.render_jsonl([record(englishText="before after")])
        self.assertEqual(len(body.split("\n")) - 1, 1)      # one record, one line
        self.assertGreater(len(body.splitlines()), 1)       # ...but splitlines disagrees
        parsed = [json.loads(ln) for ln in body.split("\n") if ln.strip()]
        self.assertEqual(len(parsed), 1)
        self.assertIn(" ", parsed[0]["englishText"])

    def test_mongo_id_is_dropped(self):
        """`_id` changes on every upstream re-scrape. Keeping it would make
        every snapshot differ from the last for no reason at all."""
        self.assertIn("_id", tq.DROP_FIELDS)


class InternalRefTest(unittest.TestCase):

    def test_multivolume_ref_names_the_volume(self):
        """al-Kafi restarts its numbering in every volume, so "hadith 1371"
        alone points at eight different reports."""
        self.assertEqual(tq.internal_ref(record(id=1371, volume=5,
                                                bookId="Al-Kafi-Volume-5-Kulayni")),
                         "vol. 5, hadith 1371")

    def test_single_volume_ref_is_just_the_number(self):
        self.assertEqual(
            tq.internal_ref(record(id=3, volume=1, bookId="Risalat-al-Huquq-Abidin")),
            "hadith 3")


class PassageTest(unittest.TestCase):

    def test_one_record_makes_exactly_one_passage(self):
        """Not run through passages.segment(): the API already carries the
        work's own divisions, and re-splitting on blank lines would cut a
        report in half."""
        recs = [record(id=1, englishText="A line.\n\nA second paragraph of the same report."),
                record(id=2)]
        ps = tq.passages_from_records("SRC-TQ-X", recs)
        self.assertEqual(len(ps), 2)
        self.assertIn("second paragraph", ps[0].text)

    def test_english_is_the_text_and_arabic_sits_beside_it(self):
        """The claim rests on the credited English. The Arabic is a parallel
        field, never mixed into the quotable text."""
        p = tq.passages_from_records("SRC-TQ-X", [record()])[0]
        self.assertEqual(p.register, "english")
        self.assertEqual(p.text, p.english)
        self.assertNotIn("من", p.text)
        self.assertIsNotNone(p.arabic_raw)

    def test_arabic_is_never_born_verified(self):
        """Real Unicode is not the same as checked against the source. Every
        Arabic passage in this project starts unverified, this corpus
        included."""
        p = tq.passages_from_records("SRC-TQ-X", [record()])[0]
        self.assertEqual(p.arabic_verified, 0)

    def test_no_speaker_is_invented(self):
        """The record either states the speaker or it does not. Detecting one
        off the English would put a name in a field a reviewer trusts."""
        p = tq.passages_from_records("SRC-TQ-X", [record()])[0]
        self.assertIsNone(p.speaker)
        self.assertEqual(p.metadata_source, "thaqalayn-api")

    def test_empty_english_is_dropped_not_emitted(self):
        ps = tq.passages_from_records("SRC-TQ-X", [record(englishText="  ")])
        self.assertEqual(ps, [])


class MetadataTest(unittest.TestCase):
    """The registered editions, as they actually sit in sources.yaml."""

    @classmethod
    def setUpClass(cls):
        _, cls.editions, cls.by_id = metadata.load_sources()
        cls.api = [e for e in cls.editions if e.get("api_file")]

    def test_there_are_api_editions(self):
        self.assertTrue(self.api, "no Thaqalayn editions registered in sources.yaml")

    def test_every_api_edition_forbids_a_page_number(self):
        """There is no page in this corpus at all. An edition that let one
        through would let a citation name a number that exists in no printing."""
        for e in self.api:
            self.assertEqual(e["pagination"], "api-record", e["source_id"])
            self.assertEqual(e["citation_unit"], "hadith-number", e["source_id"])

    def test_every_api_edition_is_pinned_and_credited(self):
        for e in self.api:
            self.assertTrue(e.get("sha256"), "%s is not pinned" % e["source_id"])
            self.assertTrue(e.get("translator"), "%s has no translator" % e["source_id"])

    def test_snapshots_on_disk_match_the_pinned_hashes(self):
        """The pin is the whole reason a mutable upstream can be a source of
        record. A snapshot that no longer hashes to its recorded value is not
        the edition this project fixed."""
        for e in self.api:
            path = os.path.join(config.ROOT, e["api_file"])
            if not os.path.exists(path):
                self.skipTest("snapshots not present: %s" % e["api_file"])
            book_id = os.path.splitext(os.path.basename(path))[0]
            _, digest = tq.read_snapshot(book_id)
            self.assertEqual(digest, e["sha256"], "%s has drifted from its pin" % e["source_id"])

    def test_no_api_edition_is_on_the_rejected_list(self):
        idx = metadata.rejected_index()
        for e in self.api:
            self.assertFalse(metadata.is_rejected(name=e.get("work"), index=idx), e["source_id"])


if __name__ == "__main__":
    unittest.main()
