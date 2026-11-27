"""Tests for kit/skills/print-design/scripts/model_search.py and model-sites.json."""
import contextlib
import copy
import importlib.util
import io
import json
import os
import tempfile
import unittest
from urllib.parse import urlparse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "kit", "skills", "print-design", "scripts", "model_search.py")
SITES = os.path.join(REPO, "kit", "skills", "print-design", "references", "model-sites.json")
ASSETS = os.path.join(REPO, "kit", "catalogs", "assets.json")

spec = importlib.util.spec_from_file_location("model_search", SCRIPT)
ms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ms)


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = ms.main(list(argv))
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.sites, self.assets = load(SITES), load(ASSETS)

    def test_real_files_agree(self):
        self.assertEqual(ms.validate(self.sites, self.assets), [])

    def test_every_print_model_source_has_a_site(self):
        group = {s["id"] for s in self.assets["sources"] if s["group"] == "print-models"}
        listed = {s["id"] for s in self.sites["sites"]}
        self.assertTrue(group <= listed)

    def test_sites_that_forbid_automation_are_links_only(self):
        access = {s["id"]: s["access"] for s in self.sites["sites"]}
        for sid in ("printables", "makerworld", "cults3d", "myminifactory", "thangs"):
            self.assertEqual(access[sid], "links-only", sid)
        self.assertEqual(access["thingiverse"], "api")

    def test_reference_only_cad_is_never_offered_for_commercial_prints(self):
        rows = ms.plan(self.sites, self.assets, "m3 screw", commercial=True)
        self.assertNotIn("mcmaster-cad", [r["id"] for r in rows])

    def test_validate_catches_problems(self):
        bad = copy.deepcopy(self.sites)
        bad["sites"][0]["access"] = "scrape"
        bad["sites"][1]["searchUrl"] = "http://example.com/?q={q}"
        bad["sites"].append({"id": "nowhere", "access": "fetch", "searchUrl": "https://x.test/{q}", "linkChecked": False})
        codes = {f["code"] for f in ms.validate(bad, self.assets)}
        self.assertTrue({"ACCESS", "URL", "ID"} <= codes)
        missing = copy.deepcopy(self.sites)
        missing["sites"] = [s for s in missing["sites"] if s["id"] != "printables"]
        self.assertIn("MISSING", {f["code"] for f in ms.validate(missing, self.assets)})

    def test_search_host_must_match_the_catalog_host(self):
        bad = copy.deepcopy(self.sites)
        bad["sites"][0]["searchUrl"] = "https://evil.example/search?q={q}"
        self.assertIn("URL", {f["code"] for f in ms.validate(bad, self.assets)})


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.sites, self.assets = load(SITES), load(ASSETS)

    def test_order_and_links(self):
        rows = ms.plan(self.sites, self.assets, "self watering planter")
        order = [ms.ORDER[r["access"]] for r in rows]
        self.assertEqual(order, sorted(order))
        for r in rows:
            self.assertTrue(r["link"].startswith("https://"), r["id"])
            self.assertNotIn("{q}", r["link"])
            self.assertNotIn(" ", r["link"])

    def test_encoding(self):
        self.assertEqual(ms.build_link("https://a.test/s?q={q}", "a b&c"), "https://a.test/s?q=a+b%26c")
        self.assertEqual(ms.build_link("https://a.test/search/{q}?x=1", "a b/c"), "https://a.test/search/a%20b%2Fc?x=1")
        self.assertEqual(ms.build_link("https://www.yeggi.com/q/{q}/?s=f", "wall hook"), "https://www.yeggi.com/q/wall+hook/?s=f")

    def test_injection_stays_inside_the_query(self):
        rows = ms.plan(self.sites, self.assets, "hook?x=1#frag /../evil")
        for r in rows:
            site = next(s for s in self.sites["sites"] if s["id"] == r["id"])
            self.assertEqual(urlparse(r["link"]).netloc, urlparse(site["searchUrl"].replace("{q}", "q")).netloc)
            self.assertNotIn("#", r["link"])

    def test_access_filter(self):
        rows = ms.plan(self.sites, self.assets, "hook", access=["links-only"])
        self.assertTrue(rows)
        self.assertEqual({r["access"] for r in rows}, {"links-only"})

    def test_query_rules(self):
        with self.assertRaises(ValueError):
            ms.clean_query("   ")
        with self.assertRaises(ValueError):
            ms.clean_query("x" * 201)
        self.assertEqual(ms.clean_query("  wall \n hook "), "wall hook")


class CommandLineTests(unittest.TestCase):
    def test_plan_json(self):
        code, out, _ = run("plan", "cable", "clip", "--json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["query"], "cable clip")
        self.assertTrue(all("do" in r and "license" in r for r in data["sites"]))

    def test_validate_and_usage(self):
        self.assertEqual(run("validate")[0], 0)
        self.assertEqual(run()[0], 2)
        self.assertEqual(run("plan", " ")[0], 2)
        self.assertEqual(run("--sites", "/nonexistent.json", "plan", "x")[0], 2)

    def test_broken_sites_file_blocks_plan(self):
        doc = load(SITES)
        doc["sites"][0]["access"] = "scrape"
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sites.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(doc, handle)
            self.assertEqual(run("--sites", path, "plan", "x")[0], 2)
            self.assertEqual(run("--sites", path, "validate")[0], 1)


if __name__ == "__main__":
    unittest.main()
