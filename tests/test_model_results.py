"""Tests for kit/skills/print-design/scripts/model_results.py."""
import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "kit", "skills", "print-design", "scripts", "model_results.py")
spec = importlib.util.spec_from_file_location("model_results", SCRIPT)
mr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mr)

THINGIVERSE_SEARCH = {"total": 2, "hits": [
    {"id": 101, "name": "Self-watering planter", "public_url": "https://www.thingiverse.com/thing:101",
     "preview_image": "https://cdn.thingiverse.com/a.jpg", "creator": {"name": "maker1"}},
    {"id": 102, "name": "Pot <script>alert(1)</script>", "public_url": "https://www.thingiverse.com/thing:102",
     "thumbnail": "http://insecure.example/b.jpg", "creator": {"name": "maker2"}}]}
THINGIVERSE_THING = {"id": 101, "name": "Self-watering planter", "license": "Creative Commons - Attribution - Share Alike",
                     "public_url": "https://www.thingiverse.com/thing:101", "creator": {"name": "maker1"},
                     "files": [{"name": "planter.stl", "size": 12345, "download_url": "https://api.thingiverse.com/files/9/download"}]}
SKETCHFAB_SEARCH = {"results": [
    {"uid": "abc", "name": "Fern pot", "viewerUrl": "https://sketchfab.com/3d-models/fern-pot-abc",
     "isDownloadable": True, "user": {"displayName": "Artist"},
     "license": {"label": "CC Attribution"},
     "thumbnails": {"images": [{"url": "https://media.sketchfab.com/t/200.jpg", "width": 200},
                               {"url": "https://media.sketchfab.com/t/640.jpg", "width": 640},
                               {"url": "https://media.sketchfab.com/t/1920.jpg", "width": 1920}]}},
    {"uid": "def", "name": "NC vase", "viewerUrl": "https://sketchfab.com/3d-models/nc-vase-def",
     "isDownloadable": True, "user": {"username": "u2"}, "license": {"label": "CC Attribution-NonCommercial-NoDerivs"}}]}
SMITHSONIAN = {"response": {"rows": [
    {"id": "edanmdm-1", "title": "Fossil fern", "content": {
        "descriptiveNonRepeating": {"record_link": "https://3d.si.edu/object/1", "online_media": {"media": [
            {"type": "3d_package", "content": "https://3d-api.si.edu/content/1.zip", "thumbnail": "https://ids.si.edu/t1.jpg",
             "usage": {"access": "CC0"}, "idsId": "pkg1"}]}}}},
    {"id": "edanmdm-2", "title": "A photo only", "content": {"descriptiveNonRepeating": {"online_media": {"media": [
        {"type": "Images", "thumbnail": "https://ids.si.edu/t2.jpg"}]}}}}]}}


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = mr.main(list(argv))
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


class LicenseTests(unittest.TestCase):
    def test_table(self):
        cases = {
            "CC0": ("yes", "yes"), "Public Domain": ("yes", "yes"),
            "CC Attribution": ("yes", "yes"), "Creative Commons - Attribution": ("yes", "yes"),
            "Creative Commons - Attribution - Share Alike": ("yes", "yes-share-alike"),
            "CC BY-ND 4.0": ("yes", "no"),
            "Creative Commons - Attribution - Non-Commercial": ("no", "yes"),
            "CC BY-NC-SA": ("no", "yes-share-alike"), "CC BY-NC-ND": ("no", "no"),
            "Standard Digital File License": ("no", "no"),
            "CULTS - Commercial Use": ("yes", "yes"), "Cults CU-ND": ("yes", "no"), "Cults - Private Use": ("no", "no"),
            "GNU - GPL": ("yes", "yes-share-alike"), "MIT": ("yes", "yes"),
        }
        for text, (sell, remix) in cases.items():
            lic = mr.read_license(text)
            self.assertEqual((lic["sellPrints"], lic["remix"]), (sell, remix), text)

    def test_unknown_is_never_yes(self):
        for text in ("", "All rights reserved", "Some custom license"):
            lic = mr.read_license(text)
            self.assertEqual(lic["sellPrints"], "unknown", text)
            self.assertEqual(mr.verdict(lic, "sell"), "check")

    def test_verdicts(self):
        self.assertEqual(mr.verdict(mr.read_license("CC BY-NC"), "sell"), "no")
        self.assertEqual(mr.verdict(mr.read_license("CC BY-NC"), "personal"), "ok")
        self.assertEqual(mr.verdict(mr.read_license("CC BY-ND"), "remix"), "no")


class NormalizeTests(unittest.TestCase):
    def test_thingiverse_search_and_thing_merge(self):
        hits = mr.norm_thingiverse_search(THINGIVERSE_SEARCH)
        self.assertEqual([h["id"] for h in hits], ["thingiverse:101", "thingiverse:102"])
        self.assertIsNone(hits[1]["thumbnail"])  # http is dropped
        self.assertEqual(hits[0]["license"]["label"], "Unknown")
        merged = mr.merge([hits, mr.norm_thingiverse_thing(THINGIVERSE_THING)])
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["license"]["label"], "CC BY-SA")
        self.assertEqual(merged[0]["files"][0]["name"], "planter.stl")

    def test_sketchfab(self):
        rows = mr.norm_sketchfab_search(SKETCHFAB_SEARCH)
        self.assertEqual(rows[0]["thumbnail"], "https://media.sketchfab.com/t/640.jpg")
        self.assertEqual(rows[0]["license"]["sellPrints"], "yes")
        self.assertEqual(rows[1]["author"], "u2")
        self.assertEqual(rows[1]["license"]["sellPrints"], "no")

    def test_smithsonian_keeps_only_3d(self):
        rows = mr.norm_smithsonian(SMITHSONIAN)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["license"]["label"], "Public domain (CC0)")
        self.assertTrue(rows[0]["downloadable"])

    def test_bad_shapes_give_nothing(self):
        for fn in mr.NORMALIZERS.values():
            self.assertEqual(fn({}), [])
            self.assertEqual(fn([]), [])

    def test_hand_built_records(self):
        doc = {"records": [{"site": "yeggi", "title": "Hook", "pageUrl": "https://www.printables.com/model/1",
                            "thumbnail": "https://img.example/1.jpg", "license": "CC BY"}, {"title": "no site"}]}
        rows = mr.norm_records(doc)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["license"]["label"], "CC BY")


class GalleryTests(unittest.TestCase):
    def test_gallery_escapes_and_shows(self):
        records = mr.merge([mr.norm_thingiverse_search(THINGIVERSE_SEARCH), mr.norm_sketchfab_search(SKETCHFAB_SEARCH)])
        page = mr.gallery(records, "planter <b>", "sell",
                          [{"name": "Printables", "link": "https://www.printables.com/search/models?q=planter"},
                           {"name": "Bad", "link": "javascript:alert(1)"}])
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn("planter <b>", page)
        self.assertIn('src="https://cdn.thingiverse.com/a.jpg"', page)
        self.assertIn("Search Printables", page)
        self.assertNotIn("javascript:", page)
        self.assertIn('referrerpolicy="no-referrer"', page)
        self.assertEqual(page.count('class="card"'), 4)

    def test_cli_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = os.path.join(tmp, "raw.json")
            with open(raw, "w", encoding="utf-8") as h:
                json.dump(SKETCHFAB_SEARCH, h)
            recs = os.path.join(tmp, "recs.json")
            self.assertEqual(run("normalize", "--source", "sketchfab-search", raw, "--out", recs)[0], 0)
            merged = os.path.join(tmp, "merged.json")
            self.assertEqual(run("merge", recs, recs, "--out", merged)[0], 0)
            with open(merged, encoding="utf-8") as h:
                self.assertEqual(len(json.load(h)["records"]), 2)
            out = os.path.join(tmp, "finds.html")
            self.assertEqual(run("gallery", merged, "--out", out, "--use", "sell")[0], 0)
            with open(out, encoding="utf-8") as h:
                self.assertIn("Fern pot", h.read())

    def test_usage(self):
        self.assertEqual(run()[0], 2)
        self.assertEqual(run("normalize", "--source", "records", "/nonexistent.json")[0], 2)
        code, out, _ = run("license", "CC", "BY-SA")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["remix"], "yes-share-alike")


if __name__ == "__main__":
    unittest.main()
