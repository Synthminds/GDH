"""The per-book principle lists must match kit/canon/principles.json word for word."""
import glob
import json
import os
import re
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, "kit", "canon", "principles.json")
LISTS = os.path.join(REPO, "kit", "canon", "principles")
LINE = re.compile(r"^\*\*(P-[A-Z]+-\d+) (.+?)\.\*\* (.+?) Test: (.+)$")


def read_lists():
    found = {}
    for path in sorted(glob.glob(os.path.join(LISTS, "*.md"))):
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                match = LINE.match(line.rstrip("\n"))
                if match:
                    pid = match.group(1)
                    found.setdefault(pid, []).append((os.path.basename(path), match.groups()[1:]))
    return found


class CanonSyncTests(unittest.TestCase):
    def setUp(self):
        with open(CANON, encoding="utf-8") as handle:
            self.canon = {p["id"]: p for p in json.load(handle)["principles"]}
        self.lists = read_lists()

    def test_every_principle_listed_once(self):
        self.assertEqual(sorted(self.canon), sorted(self.lists))
        repeated = sorted(pid for pid, hits in self.lists.items() if len(hits) != 1)
        self.assertEqual(repeated, [])

    def test_lists_match_json(self):
        drift = []
        for pid, hits in self.lists.items():
            principle = self.canon.get(pid)
            if principle is None:
                continue
            title, rule, test = hits[0][1]
            if (title, rule, test) != (principle["title"], principle["rule"], principle["test"]):
                drift.append(pid)
        self.assertEqual(drift, [])

    def test_list_file_matches_book(self):
        wrong = []
        for pid, hits in self.lists.items():
            principle = self.canon.get(pid)
            if principle and hits[0][0] != principle["source"]["book"] + ".md":
                wrong.append(pid)
        self.assertEqual(wrong, [])


if __name__ == "__main__":
    unittest.main()
