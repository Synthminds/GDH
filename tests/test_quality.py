"""The labelled quality corpus: tell-scan precision and recall, and mood-board verdicts."""

import contextlib
import io
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "evals"))

import quality  # noqa: E402


class QualityCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = quality.score()
        with open(os.path.join(quality.CORPUS, "labels.json"), encoding="utf-8") as handle:
            cls.labels = json.load(handle)

    def test_meets_the_recorded_baseline(self):
        self.assertEqual(self.result["belowBaseline"], [])
        self.assertTrue(self.result["pass"])

    def test_every_labelled_page_exists(self):
        for case in self.labels["cases"]:
            with self.subTest(case=case["id"]):
                self.assertTrue(os.path.isfile(os.path.join(quality.CORPUS, case["page"])))
                self.assertIn(case["class"], ("generic-first-wave", "generic-second-wave",
                                              "brand-required", "distinctive"))

    def test_corpus_holds_each_class(self):
        classes = [case["class"] for case in self.labels["cases"]]
        for name in ("generic-first-wave", "generic-second-wave", "brand-required", "distinctive"):
            self.assertIn(name, classes)

    def test_labels_use_known_rule_codes(self):
        codes = set(quality.load_tells().RULES)
        for case in self.labels["cases"]:
            for code in case.get("expect", []) + case.get("expectBrandRequired", []):
                self.assertIn(code, codes)

    def test_rule_scores_are_reported(self):
        rules = self.result["rules"]
        self.assertEqual(rules["TELL_PURPLE_GRADIENT"]["recall"], 1.0)
        for counts in rules.values():
            self.assertEqual(set(counts), {"tp", "fp", "fn", "precision", "recall"})

    def test_brand_required_case_reports_no_finding(self):
        case = [c for c in self.result["cases"] if c["id"] == "brand-violet"][0]
        self.assertEqual(case["extra"], [])
        self.assertEqual(case["brandRequired"], ["TELL_GLOW_SHADOW", "TELL_PURPLE_GRADIENT"])

    def test_boards_match_their_labels(self):
        self.assertEqual([b["id"] for b in self.result["boards"]],
                         ["passing-ferry", "three-skins", "three-defaults", "three-default-looks"])
        for board in self.result["boards"]:
            with self.subTest(board=board["id"]):
                self.assertTrue(board["asLabelled"])

    def test_a_lowered_baseline_fails(self):
        labels = json.loads(json.dumps(self.labels))
        # A label that the scan cannot meet drops TELL_LOREM recall below its floor of 1.0, so the run must fail.
        case = next(c for c in labels["cases"] if c["id"] == "second-wave-soft-pastel")
        case["expect"] = case["expect"] + ["TELL_LOREM"]
        self.assertEqual(labels["baseline"]["ruleRecall"]["TELL_LOREM"], 1.0)
        folder = os.path.join(quality.CORPUS)
        saved = quality.json.load
        quality.json.load = lambda handle, **kw: labels if handle.name.endswith("labels.json") else saved(handle, **kw)
        try:
            result = quality.score(folder)
        finally:
            quality.json.load = saved
        self.assertFalse(result["pass"])
        self.assertTrue(any("TELL_LOREM recall" in line for line in result["belowBaseline"]))

    def test_command_line(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = quality.main(["--json"])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out.getvalue())["pass"])


if __name__ == "__main__":
    unittest.main()
