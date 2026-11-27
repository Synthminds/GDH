"""Tests for kit/skills/design-principles/scripts/principles.py.

Run: python3 -m unittest discover -s tests
"""

import contextlib
import copy
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "kit", "skills", "design-principles", "scripts", "principles.py")
CANON = os.path.join(ROOT, "kit", "canon", "principles.json")
CAPS = os.path.join(ROOT, "kit", "catalogs", "capabilities.json")

_spec = importlib.util.spec_from_file_location("gdh_principles", SCRIPT)
pr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pr)


def run(argv):
    """Run the CLI. Return (exit code, stdout text)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = pr.main(argv)
    return code, out.getvalue()


def principle(pid, book, **over):
    item = {
        "id": pid,
        "title": "Write the brief first",
        "rule": "Write a short brief before any visual.",
        "why": "Words keep the work on track.",
        "apply": "Confirm the brief with the user.",
        "test": "A confirmed brief predates the first visual.",
        "check": "default",
        "disciplines": ["all"],
        "stages": ["brief"],
        "tags": ["process"],
        "source": {"book": book, "part": "Chapter 1"},
    }
    item.update(over)
    return item


def fixture_canon():
    """One principle per book, plus a few with distinct scopes for the filters."""
    items = []
    for book, prefix in pr.BOOKS.items():
        items.append(principle("P-%s-01" % prefix, book))
    items.append(principle("P-EMO-02", "designing-for-emotion", check="gate",
                           disciplines=["website", "app"], stages=["refine", "finalize"],
                           tags=["emotion", "originality"]))
    items.append(principle("P-GEPHI-02", "mastering-gephi", disciplines=["network-graph"],
                           stages=["explore"], tags=["data"]))
    items.append(principle("P-ANI-02", "animation-handbook", check="gate", disciplines=["ui-motion"],
                           stages=["finalize"], tags=["motion", "accessibility"]))
    return {"version": 1, "principles": items}


class TmpCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gdh-principles-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def write(self, name, data):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as fh:
            if isinstance(data, str):
                fh.write(data)
            else:
                json.dump(data, fh)
        return path

    def canon_path(self, canon=None):
        return self.write("principles.json", canon if canon is not None else fixture_canon())

    def ids(self, argv):
        code, text = run(argv + ["--canon", self.canon_path(), "--capabilities", CAPS, "--json"])
        self.assertEqual(code, 0, text)
        return [p["id"] for p in json.loads(text)["principles"]]


class FilterTests(TmpCase):
    def test_no_filter_returns_all(self):
        self.assertEqual(len(self.ids([])), len(pr.BOOKS) + 3)

    def test_discipline_includes_all_scoped(self):
        got = self.ids(["--discipline", "website"])
        self.assertIn("P-EMO-02", got)
        self.assertIn("P-DSH-01", got)
        self.assertNotIn("P-GEPHI-02", got)
        self.assertNotIn("P-ANI-02", got)

    def test_specific_drops_all_scoped(self):
        self.assertEqual(self.ids(["--discipline", "website", "--specific"]), ["P-EMO-02"])

    def test_comma_list_is_or(self):
        got = self.ids(["--discipline", "network-graph,ui-motion", "--specific"])
        self.assertEqual(sorted(got), ["P-ANI-02", "P-GEPHI-02"])

    def test_stage_and_tag_and_check_combine(self):
        self.assertEqual(self.ids(["--stage", "finalize", "--check", "gate", "--tag", "motion"]), ["P-ANI-02"])
        self.assertEqual(self.ids(["--tag", "originality"]), ["P-EMO-02"])
        self.assertEqual(self.ids(["--stage", "explore"]), ["P-GEPHI-02"])

    def test_id_exact_and_prefix(self):
        self.assertEqual(self.ids(["--id", "P-EMO-02"]), ["P-EMO-02"])
        self.assertEqual(sorted(self.ids(["--id", "P-EMO"])), ["P-EMO-01", "P-EMO-02"])
        self.assertEqual(self.ids(["--id", "P-EM"]), [])

    def test_book_filter(self):
        self.assertEqual(sorted(self.ids(["--book", "mastering-gephi"])), ["P-GEPHI-01", "P-GEPHI-02"])

    def test_text_output(self):
        code, text = run(["--canon", self.canon_path(), "--capabilities", CAPS, "--id", "P-ANI-02"])
        self.assertEqual(code, 0)
        self.assertIn("P-ANI-02 [gate]", text)
        self.assertIn("Test:", text)
        self.assertIn("1 principle(s): 1 gate, 0 default", text)

    def test_full_output_has_source(self):
        code, text = run(["--canon", self.canon_path(), "--capabilities", CAPS, "--id", "P-ANI-02", "--full"])
        self.assertEqual(code, 0)
        self.assertIn("Source: animation-handbook, Chapter 1", text)
        self.assertIn("Why:", text)

    def test_unknown_filter_value_is_usage_error(self):
        for flag, value in (("--discipline", "webs"), ("--stage", "ship"), ("--tag", "fun"),
                            ("--check", "hard"), ("--book", "nope")):
            code, _ = run(["--canon", self.canon_path(), "--capabilities", CAPS, flag, value])
            self.assertEqual(code, 2, flag)

    def test_missing_canon_is_usage_error(self):
        code, _ = run(["--canon", os.path.join(self.tmp, "absent.json"), "--capabilities", CAPS])
        self.assertEqual(code, 2)

    def test_bad_json_is_usage_error(self):
        path = self.write("broken.json", "{not json")
        code, text = run(["--canon", path, "--capabilities", CAPS, "--validate", "--json"])
        self.assertEqual(code, 2)
        self.assertFalse(json.loads(text)["ok"])


class ValidateTests(TmpCase):
    def codes(self, canon):
        disc = pr.load_disciplines(CAPS)
        return [f["code"] for f in pr.validate(canon, disc)]

    def test_fixture_is_clean(self):
        self.assertEqual(self.codes(fixture_canon()), [])

    def test_duplicate_id(self):
        canon = fixture_canon()
        canon["principles"].append(copy.deepcopy(canon["principles"][0]))
        self.assertIn("ID_DUPLICATE", self.codes(canon))

    def test_bad_prefix(self):
        canon = fixture_canon()
        canon["principles"].append(principle("P-DSH-09", "designing-for-emotion"))
        self.assertIn("ID_PREFIX", self.codes(canon))

    def test_bad_id_format(self):
        canon = fixture_canon()
        canon["principles"][0]["id"] = "DSH-1"
        self.assertIn("ID_FORMAT", self.codes(canon))

    def test_bad_discipline(self):
        canon = fixture_canon()
        canon["principles"][0]["disciplines"] = ["websites"]
        self.assertIn("DISCIPLINE", self.codes(canon))

    def test_all_must_stand_alone(self):
        canon = fixture_canon()
        canon["principles"][0]["disciplines"] = ["all", "website"]
        self.assertIn("DISCIPLINE", self.codes(canon))

    def test_bad_stage_tag_and_check(self):
        canon = fixture_canon()
        canon["principles"][0]["stages"] = ["ship"]
        canon["principles"][1]["tags"] = ["fun"]
        canon["principles"][2]["check"] = "hard"
        codes = self.codes(canon)
        for code in ("STAGE", "TAG", "CHECK_VALUE"):
            self.assertIn(code, codes)

    def test_missing_field_and_bad_title(self):
        canon = fixture_canon()
        del canon["principles"][0]["why"]
        canon["principles"][1]["title"] = "Two words"
        codes = self.codes(canon)
        self.assertIn("SCHEMA", codes)
        self.assertIn("TITLE_LENGTH", codes)

    def test_unknown_book(self):
        canon = fixture_canon()
        canon["principles"][0]["source"]["book"] = "some-book"
        self.assertIn("SOURCE_BOOK", self.codes(canon))

    def test_book_without_principle(self):
        canon = fixture_canon()
        canon["principles"] = [p for p in canon["principles"] if p["source"]["book"] != "mapping-to-mcps"]
        self.assertIn("BOOK_EMPTY", self.codes(canon))

    def test_cli_validate_exit_codes(self):
        code, _ = run(["--canon", self.canon_path(), "--capabilities", CAPS, "--validate"])
        self.assertEqual(code, 0)
        canon = fixture_canon()
        canon["principles"].append(copy.deepcopy(canon["principles"][0]))
        bad = self.write("bad.json", canon)
        code, text = run(["--canon", bad, "--capabilities", CAPS, "--validate", "--json"])
        self.assertEqual(code, 1)
        data = json.loads(text)
        self.assertFalse(data["ok"])
        self.assertEqual(data["findings"][0]["code"], "ID_DUPLICATE")


class RealCanonTests(unittest.TestCase):
    def test_real_canon_validates(self):
        code, text = run(["--validate", "--json"])
        self.assertEqual(code, 0, text)
        data = json.loads(text)
        self.assertTrue(data["ok"])
        self.assertGreater(data["principles"], 100)

    def test_default_paths_resolve(self):
        self.assertEqual(os.path.normpath(pr.DEFAULT_CANON), os.path.normpath(CANON))
        self.assertEqual(os.path.normpath(pr.DEFAULT_CAPS), os.path.normpath(CAPS))

    def test_every_book_has_a_readable_list(self):
        with open(CANON, encoding="utf-8") as fh:
            canon = json.load(fh)
        for book in pr.BOOKS:
            path = os.path.join(ROOT, "kit", "canon", "principles", book + ".md")
            self.assertTrue(os.path.isfile(path), path)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            for item in canon["principles"]:
                if item["source"]["book"] == book:
                    line = "**%s %s.** %s Test: %s" % (item["id"], item["title"], item["rule"], item["test"])
                    self.assertIn(line, text)


if __name__ == "__main__":
    unittest.main()
