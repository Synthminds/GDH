"""Tests for kit/skills/find-assets/scripts/assets.py and kit/catalogs/assets.json.

Run: python3 -m unittest discover -s tests
"""

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "kit", "skills", "find-assets", "scripts", "assets.py")
CATALOG = os.path.join(ROOT, "kit", "catalogs", "assets.json")

_spec = importlib.util.spec_from_file_location("gdh_assets", SCRIPT)
assets = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(assets)


def run(argv):
    """Run the CLI. Return (exit code, stdout text, stderr text)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = assets.main(argv)
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


def run_json(argv):
    code, text, _ = run(argv + ["--json"])
    return code, json.loads(text)


def write(path, data):
    parent = os.path.dirname(path)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode) as fh:
        fh.write(data)


def write_json(path, doc):
    write(path, json.dumps(doc, indent=2))


def read_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source(asset_id, **changes):
    entry = {"id": asset_id, "name": asset_id.replace("-", " ").title(), "url": "https://example.com/%s" % asset_id,
             "group": "icons", "holds": "Stroke icon set.", "license": "MIT.",
             "attribution": "none: no credit in the product", "commercialUse": "yes",
             "fetch": "npm i %s" % asset_id, "risk": "None.", "verifiedOn": "2026-11-01"}
    entry.update(changes)
    return entry


def fixture_catalog():
    return {"version": 1, "sources": [
        source("line-icons"),
        source("brand-marks", holds="Brand marks as SVG.", commercialUse="yes-with-limits",
               attribution="none: no credit for the SVG file"),
        source("open-photos", group="photo-video", holds="Free photos of places.", verifiedOn=None,
               commercialUse="yes-with-limits", attribution="none: a credit is appreciated"),
        source("credit-patterns", group="illustration", holds="Repeatable background patterns.",
               attribution="required", verifiedOn=None),
        source("mixed-models", group="3d", holds="Community 3D models with icons of each license.",
               commercialUse="varies", attribution="varies: per model"),
        source("mystery-kit", group="components", holds="Component kit.", commercialUse="unknown",
               attribution="unknown", verifiedOn=None),
        source("site-gallery", group="inspiration", holds="Design references for mood boards.",
               commercialUse="reference-only", attribution="n/a", verifiedOn=None),
        source("open-font", group="fonts", holds="Variable sans typeface.",
               attribution="notice: keep the license file with the font files"),
        source("museum-art", group="photo-video", holds="Public-domain artwork images.",
               attribution="requested: a citation is requested"),
        source("old-charts", group="dataviz", holds="Simple canvas charts.", verifiedOn="2025-01-01"),
    ]}


class TempCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gdh-assets-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def path(self, *parts):
        return os.path.join(self.tmp, *parts)


# ---------------------------------------------------------------- the real catalog

class RealCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CATALOG, "r", encoding="utf-8") as fh:
            cls.text = fh.read()
        cls.doc = json.loads(cls.text)
        cls.sources = cls.doc["sources"]

    def test_loads_without_problems(self):
        sources, problems = assets.load_catalog(CATALOG)
        self.assertEqual(problems, [])
        self.assertEqual(len(sources), 186)

    def test_shape_and_field_set(self):
        self.assertEqual(self.doc["version"], 1)
        for entry in self.sources:
            self.assertEqual(tuple(entry.keys()), assets.CATALOG_FIELDS, entry.get("id"))

    def test_ids_unique_and_kebab_case(self):
        ids = [entry["id"] for entry in self.sources]
        self.assertEqual(len(ids), len(set(ids)))
        for value in ids:
            self.assertRegex(value, r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_urls_are_https(self):
        for entry in self.sources:
            self.assertTrue(entry["url"].startswith("https://"), entry["id"])

    def test_groups_match_the_declared_list(self):
        declared = set(self.doc["groups"])
        self.assertEqual({entry["group"] for entry in self.sources}, declared)
        self.assertEqual(len(declared), 12)

    def test_enums(self):
        for entry in self.sources:
            self.assertIn(entry["commercialUse"], assets.COMMERCIAL_VALUES, entry["id"])
            head = entry["attribution"].split(":", 1)[0]
            self.assertIn(head, assets.ATTRIBUTION_CLASSES, entry["id"])

    def test_verified_on_is_null_or_a_date(self):
        unverified = 0
        for entry in self.sources:
            if entry["verifiedOn"] is None:
                unverified += 1
            else:
                self.assertIsNotNone(assets.parse_date(entry["verifiedOn"]), entry["id"])
        self.assertEqual(unverified, 66)

    def test_unverified_entries_say_so_in_risk(self):
        for entry in self.sources:
            if entry["verifiedOn"] is None and entry["id"] != "svg-noise-method":
                self.assertIn("read the license page before use", entry["risk"], entry["id"])

    def test_reference_only_group(self):
        for entry in self.sources:
            if entry["group"] == "inspiration":
                self.assertEqual(entry["commercialUse"], "reference-only", entry["id"])

    def test_no_version_pins_and_ascii_only(self):
        for entry in self.sources:
            self.assertIsNone(re.search(r"\(\D*\d+\.\d+\.\d+\)", entry["fetch"]), entry["id"])
        self.assertEqual(re.findall(r"[^\x00-\x7f]", self.text), [])

    def test_main_groups_have_a_ready_entry(self):
        code, doc = run_json(["search", CATALOG, "--limit", "0", "--today", "2026-11-23"])
        self.assertEqual(code, 0)
        self.assertEqual(doc["count"], 186)
        ready = {r["group"] for r in doc["results"] if r["status"] == "catalog-verified"}
        self.assertNotIn("inspiration", ready)
        for group in ("components", "icons", "fonts", "3d", "motion", "dataviz", "color-type-tools", "logo-aids"):
            self.assertIn(group, ready)

    def test_known_lookups(self):
        code, doc = run_json(["search", CATALOG, "--query", "dense time series", "--today", "2026-11-23"])
        self.assertEqual(code, 0)
        self.assertEqual(doc["results"][0]["id"], "uplot")
        code, doc = run_json(["search", CATALOG, "--group", "icons", "--query", "brand marks",
                              "--today", "2026-11-23"])
        self.assertEqual(doc["results"][0]["id"], "simple-icons")
        self.assertEqual(doc["results"][0]["status"], "read-license")


# ---------------------------------------------------------------- search

class SearchTests(TempCase):
    def setUp(self):
        super().setUp()
        self.catalog = self.path("assets.json")
        write_json(self.catalog, fixture_catalog())

    def search(self, *argv):
        return run_json(["search", self.catalog, "--today", "2026-11-23"] + list(argv))

    def ids(self, *argv):
        return [r["id"] for r in self.search(*argv)[1]["results"]]

    def test_lists_all_without_filters(self):
        code, doc = self.search()
        self.assertEqual(code, 0)
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["count"], 10)

    def test_group_filter(self):
        self.assertEqual(self.ids("--group", "photo-video"), ["museum-art", "open-photos"])

    def test_group_accepts_commas_and_repeats(self):
        self.assertEqual(set(self.ids("--group", "fonts,icons")), {"open-font", "line-icons", "brand-marks"})
        self.assertEqual(set(self.ids("--group", "fonts", "--group", "dataviz")), {"open-font", "old-charts"})

    def test_unknown_group_is_a_usage_error(self):
        code, _out, err = run(["search", self.catalog, "--group", "nope"])
        self.assertEqual(code, 2)
        self.assertIn("groups are", err)

    def test_query_ranks_name_above_holds(self):
        # "icons" is in the id and name of line-icons, and only in the holds text of mixed-models.
        found = self.ids("--query", "icons")
        self.assertEqual(found[0], "line-icons")
        self.assertIn("mixed-models", found)
        self.assertLess(found.index("line-icons"), found.index("mixed-models"))

    def test_query_matches_singular_and_plural(self):
        self.assertIn("line-icons", self.ids("--query", "icon"))
        self.assertIn("open-photos", self.ids("--query", "photos"))

    def test_query_uses_synonyms(self):
        self.assertIn("open-photos", self.ids("--query", "image"))
        self.assertIn("open-font", self.ids("--query", "font"))

    def test_more_matched_words_rank_first(self):
        found = self.ids("--query", "background patterns icons")
        self.assertEqual(found[0], "credit-patterns")

    def test_stopwords_are_dropped(self):
        code, doc = self.search("--query", "the free icons")
        self.assertEqual(doc["filters"]["tokens"], ["icons"])

    def test_commercial_filter(self):
        found = set(self.ids("--commercial"))
        self.assertNotIn("mixed-models", found)
        self.assertNotIn("mystery-kit", found)
        self.assertNotIn("site-gallery", found)
        self.assertIn("brand-marks", found)
        self.assertIn("line-icons", found)

    def test_no_attribution_filter(self):
        found = set(self.ids("--no-attribution"))
        self.assertEqual(found, {"line-icons", "brand-marks", "open-photos", "open-font", "museum-art", "old-charts"})

    def test_status_values(self):
        by_id = {r["id"]: r for r in self.search()[1]["results"]}
        self.assertEqual(by_id["line-icons"]["status"], "catalog-verified")
        self.assertEqual(by_id["line-icons"]["reasons"], [])
        self.assertEqual(by_id["brand-marks"]["status"], "read-license")
        self.assertEqual(by_id["open-photos"]["status"], "read-license")
        self.assertEqual(by_id["mixed-models"]["status"], "read-license")
        self.assertEqual(by_id["mystery-kit"]["status"], "blocked")
        self.assertEqual(by_id["site-gallery"]["status"], "reference-only")
        self.assertEqual(by_id["old-charts"]["status"], "read-license")
        self.assertIn("older than 180 days", by_id["old-charts"]["reasons"][0])

    def test_duties_follow_the_attribution_class(self):
        by_id = {r["id"]: r for r in self.search()[1]["results"]}
        self.assertIn("license condition", by_id["credit-patterns"]["duties"][0])
        self.assertIn("keep the license", by_id["open-font"]["duties"][0])
        self.assertEqual(by_id["line-icons"]["duties"], [])

    def test_max_age_days_changes_the_stale_rule(self):
        code, doc = self.search("--max-age-days", "1000")
        by_id = {r["id"]: r for r in doc["results"]}
        self.assertEqual(by_id["old-charts"]["status"], "catalog-verified")

    def test_verified_flag_keeps_only_ready_entries(self):
        self.assertEqual(set(self.ids("--verified")), {"line-icons", "open-font", "museum-art"})

    def test_ready_entries_rank_before_unread_ones(self):
        found = self.ids("--group", "photo-video")
        self.assertEqual(found, ["museum-art", "open-photos"])

    def test_limit(self):
        code, doc = self.search("--limit", "2")
        self.assertEqual(doc["shown"], 2)
        self.assertEqual(doc["count"], 10)
        self.assertEqual(len(doc["results"]), 2)

    def test_no_result_exits_1(self):
        code, doc = self.search("--query", "zeppelin")
        self.assertEqual(code, 1)
        self.assertFalse(doc["ok"])
        self.assertEqual(doc["results"], [])

    def test_text_output_names_the_next_step(self):
        code, out, _ = run(["search", self.catalog, "--query", "gallery", "--today", "2026-11-23"])
        self.assertEqual(code, 0)
        self.assertIn("status: reference-only", out)
        self.assertIn("Take no file", out)

    def test_bad_today_is_a_usage_error(self):
        code, _out, _err = run(["search", self.catalog, "--today", "23-11-2026"])
        self.assertEqual(code, 2)

    def test_malformed_catalog_is_a_usage_error(self):
        for doc in ([], {"sources": "x"}, {"sources": [{"id": "a"}]},
                    {"sources": [source("Bad_Id")]}, {"sources": [source("a"), source("a")]},
                    {"sources": [source("a", url="http://example.com")]},
                    {"sources": [source("a", commercialUse=True)]},
                    {"sources": [source("a", verifiedOn="soon")]}):
            write_json(self.catalog, doc)
            code, _out, err = run(["search", self.catalog])
            self.assertEqual(code, 2, doc)
            self.assertIn("catalog is not usable", err)

    def test_missing_catalog_is_a_usage_error(self):
        code, _out, _err = run(["search", self.path("absent.json")])
        self.assertEqual(code, 2)


# ---------------------------------------------------------------- record

class RecordTests(TempCase):
    def setUp(self):
        super().setUp()
        self.manifest = self.path("design", "assets", "manifest.json")
        self.icon = self.path("public", "icons", "arrow.svg")
        write(self.icon, b"<svg>arrow</svg>")

    def record(self, *argv, **options):
        base = ["record", self.manifest, "--id", options.get("id", "lucide-arrow"),
                "--source-url", options.get("source", "https://lucide.dev/icons/arrow-right"),
                "--license", "ISC, https://github.com/lucide-icons/lucide/blob/main/LICENSE",
                "--attribution", options.get("attribution", "none required"),
                "--date", options.get("date", "2026-11-23")]
        return run_json(base + list(argv))

    def test_creates_the_manifest_in_the_template_shape(self):
        code, doc = self.record("--file", self.icon)
        self.assertEqual(code, 0)
        self.assertTrue(doc["ok"])
        manifest = read_json(self.manifest)
        self.assertEqual(manifest["version"], 1)
        self.assertEqual(list(manifest["fields"]), ["id", "sourceUrl", "license", "attribution", "date", "path", "sha256"])
        self.assertEqual(manifest["assets"], [{
            "id": "lucide-arrow", "sourceUrl": "https://lucide.dev/icons/arrow-right",
            "license": "ISC, https://github.com/lucide-icons/lucide/blob/main/LICENSE",
            "attribution": "none required", "date": "2026-11-23",
            "path": "public/icons/arrow.svg", "sha256": sha(b"<svg>arrow</svg>")}])

    def test_matches_the_kit_template_fields(self):
        template = read_json(os.path.join(ROOT, "kit", "templates", "project", "design", "assets", "manifest.json"))
        self.assertEqual(list(template["fields"]), list(assets.MANIFEST_FIELDS))

    def test_appends_and_keeps_other_manifest_keys(self):
        write_json(self.manifest, {"version": 1, "fields": {}, "ignore": ["public/og/*"], "assets": []})
        self.record("--file", self.icon)
        other = self.path("public", "icons", "check.svg")
        write(other, b"<svg>check</svg>")
        code, _ = self.record("--file", other, id="lucide-check")
        self.assertEqual(code, 0)
        manifest = read_json(self.manifest)
        self.assertEqual([a["id"] for a in manifest["assets"]], ["lucide-arrow", "lucide-check"])
        self.assertEqual(manifest["ignore"], ["public/og/*"])

    def test_several_files_get_numbered_ids(self):
        second = self.path("public", "icons", "arrow-dark.svg")
        write(second, b"<svg>dark</svg>")
        code, doc = self.record("--file", self.icon, "--file", second)
        self.assertEqual(code, 0)
        self.assertEqual([e["id"] for e in doc["recorded"]], ["lucide-arrow", "lucide-arrow-2"])
        self.assertEqual(doc["recorded"][1]["path"], "public/icons/arrow-dark.svg")

    def test_optional_fields(self):
        code, doc = self.record("--file", self.icon, "--license-url", "https://example.com/LICENSE",
                                "--catalog-id", "lucide", "--modified", "--note", "recolored to ink token")
        entry = doc["recorded"][0]
        self.assertEqual(entry["licenseUrl"], "https://example.com/LICENSE")
        self.assertEqual(entry["catalogId"], "lucide")
        self.assertIs(entry["modified"], True)
        self.assertEqual(entry["note"], "recolored to ink token")
        self.assertNotIn("origin", entry)

    def test_package_entry_has_no_file(self):
        code, doc = self.record("--package", "lucide-react@1.0.0")
        self.assertEqual(code, 0)
        entry = doc["recorded"][0]
        self.assertEqual(entry["package"], "lucide-react@1.0.0")
        self.assertNotIn("path", entry)
        self.assertNotIn("sha256", entry)

    def test_own_asset_may_use_a_plain_source(self):
        code, doc = self.record("--file", self.icon, "--origin", "own", source="project: drawn in round 2")
        self.assertEqual(code, 0)
        self.assertEqual(doc["recorded"][0]["origin"], "own")

    def test_duplicate_id_writes_nothing(self):
        self.record("--file", self.icon)
        before = read_text(self.manifest)
        other = self.path("public", "icons", "check.svg")
        write(other, b"<svg>check</svg>")
        code, doc = self.record("--file", other)
        self.assertEqual(code, 1)
        self.assertEqual(doc["findings"][0]["code"], "ENTRY_DUPLICATE_ID")
        self.assertEqual(read_text(self.manifest), before)

    def test_duplicate_path_writes_nothing(self):
        self.record("--file", self.icon)
        code, doc = self.record("--file", self.icon, id="another-id")
        self.assertEqual(code, 1)
        self.assertEqual(doc["findings"][0]["code"], "ENTRY_DUPLICATE_PATH")
        self.assertEqual(len(read_json(self.manifest)["assets"]), 1)

    def test_replace_updates_the_hash(self):
        self.record("--file", self.icon)
        write(self.icon, b"<svg>arrow v2</svg>")
        code, _ = self.record("--file", self.icon, "--replace", "--modified", date="2026-12-01")
        self.assertEqual(code, 0)
        entries = read_json(self.manifest)["assets"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["sha256"], sha(b"<svg>arrow v2</svg>"))
        self.assertEqual(entries[0]["date"], "2026-12-01")

    def test_root_argument_and_default_root(self):
        loose = self.path("elsewhere", "manifest.json")
        inside = self.path("elsewhere", "img", "a.png")
        write(inside, b"png")
        code, doc = run_json(["record", loose, "--id", "a", "--source-url", "https://example.com/a",
                              "--license", "CC0-1.0", "--attribution", "none required",
                              "--date", "2026-11-23", "--file", inside])
        self.assertEqual(code, 0)
        self.assertEqual(doc["recorded"][0]["path"], "img/a.png")
        code, doc = run_json(["record", loose, "--id", "b", "--source-url", "https://example.com/b",
                              "--license", "CC0-1.0", "--attribution", "none required",
                              "--date", "2026-11-23", "--file", self.icon, "--root", self.tmp])
        self.assertEqual(code, 0)
        self.assertEqual(doc["recorded"][0]["path"], "public/icons/arrow.svg")

    def test_usage_errors(self):
        outside = tempfile.NamedTemporaryFile(delete=False)
        outside.write(b"x")
        outside.close()
        self.addCleanup(os.remove, outside.name)
        cases = [
            (("--file", self.icon), {"date": "2026-02-30"}),
            (("--file", self.icon), {"id": "Not Kebab"}),
            (("--file", self.icon), {"source": "lucide.dev"}),
            (("--file", self.icon), {"attribution": "  "}),
            (("--file", self.path("missing.svg")), {}),
            (("--file", outside.name), {}),
            ((), {}),
            (("--file", self.icon, "--package", "x@1"), {}),
            (("--file", self.icon, "--license-url", "example.com"), {}),
        ]
        for argv, options in cases:
            code, doc = self.record(*argv, **options)
            self.assertEqual(code, 2, (argv, options))
            self.assertFalse(doc["ok"])
        self.assertFalse(os.path.exists(self.manifest))

    def test_missing_required_flag_exits_2(self):
        code, _out, _err = run(["record", self.manifest, "--id", "a", "--file", self.icon])
        self.assertEqual(code, 2)

    def test_broken_manifest_is_a_finding(self):
        write(self.manifest, "{not json")
        code, doc = self.record("--file", self.icon)
        self.assertEqual(code, 1)
        self.assertEqual(doc["findings"][0]["code"], "MANIFEST_INVALID")
        self.assertEqual(read_text(self.manifest), "{not json")


# ---------------------------------------------------------------- check

class CheckTests(TempCase):
    def setUp(self):
        super().setUp()
        self.manifest = self.path("design", "assets", "manifest.json")
        self.files = {
            "public/img/hero.jpg": b"hero",
            "public/fonts/inter.woff2": b"font",
            "design/assets/mark.svg": b"<svg>mark</svg>",
        }
        for rel, data in self.files.items():
            write(self.path(*rel.split("/")), data)
        write(self.path("public", "index.html"), "<html></html>")
        write(self.path("public", "fonts", "OFL.txt"), "license text")
        write(self.path("public", "img", ".gitkeep"), "")
        self.entries = [
            {"id": "hero-photo", "sourceUrl": "https://example.com/photo/1", "license": "CC0-1.0",
             "attribution": "none required", "date": "2026-11-23", "path": "public/img/hero.jpg",
             "sha256": sha(b"hero")},
            {"id": "inter-font", "sourceUrl": "https://example.com/inter", "license": "OFL-1.1",
             "attribution": "none required", "date": "2026-11-23", "path": "public/fonts/inter.woff2",
             "sha256": sha(b"font")},
            {"id": "own-mark", "sourceUrl": "project", "license": "owned by the client", "origin": "own",
             "attribution": "none required", "date": "2026-11-23", "path": "design/assets/mark.svg",
             "sha256": sha(b"<svg>mark</svg>")},
            {"id": "motion-lib", "sourceUrl": "https://example.com/motion", "license": "MIT",
             "attribution": "none required", "date": "2026-11-23", "package": "motion@1.0.0"},
        ]
        self.save()

    def save(self, **extra):
        doc = {"version": 1, "fields": {}, "assets": self.entries}
        doc.update(extra)
        write_json(self.manifest, doc)

    def check(self, *argv):
        return run_json(["check", self.manifest, "--root", self.tmp] + list(argv))

    def codes(self, *argv):
        code, doc = self.check(*argv)
        return code, [f["code"] for f in doc["findings"]]

    def test_clean_project_passes(self):
        code, doc = self.check()
        self.assertEqual(code, 0, doc["findings"])
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["info"]["files"], 3)
        self.assertEqual(doc["info"]["recorded"], 3)
        self.assertEqual(doc["info"]["packages"], 1)
        self.assertEqual(doc["info"]["assetDirs"], ["design/assets", "public"])

    def test_text_output(self):
        code, out, _ = run(["check", self.manifest, "--root", self.tmp])
        self.assertEqual(code, 0)
        self.assertIn("0 finding(s)", out)

    def test_file_unrecorded(self):
        write(self.path("public", "img", "extra.png"), b"extra")
        code, doc = self.check()
        self.assertEqual(code, 1)
        self.assertEqual([(f["code"], f["path"]) for f in doc["findings"]],
                         [("FILE_UNRECORDED", "public/img/extra.png")])

    def test_non_asset_types_need_all_files(self):
        self.assertEqual(self.codes(), (0, []))
        code, doc = self.check("--all-files")
        self.assertEqual(code, 1)
        self.assertEqual(sorted(f["path"] for f in doc["findings"]), ["public/fonts/OFL.txt", "public/index.html"])

    def test_file_hash(self):
        write(self.path("public", "img", "hero.jpg"), b"changed")
        code, doc = self.check()
        self.assertEqual(code, 1)
        self.assertEqual(doc["findings"][0]["code"], "FILE_HASH")
        self.assertEqual(doc["findings"][0]["id"], "hero-photo")

    def test_file_missing(self):
        os.remove(self.path("public", "img", "hero.jpg"))
        self.assertEqual(self.codes(), (1, ["FILE_MISSING"]))

    def test_entry_field_license_and_source(self):
        self.entries[0]["license"] = ""
        del self.entries[1]["sourceUrl"]
        self.save()
        code, doc = self.check()
        self.assertEqual(code, 1)
        messages = {f["id"]: f["message"] for f in doc["findings"] if f["code"] == "ENTRY_FIELD"}
        self.assertIn("license", messages["hero-photo"])
        self.assertIn("sourceUrl", messages["inter-font"])

    def test_entry_field_file_or_package(self):
        del self.entries[3]["package"]
        del self.entries[0]["sha256"]
        self.save()
        code, found = self.codes()
        self.assertEqual(found.count("ENTRY_FIELD"), 2)

    def test_entry_id(self):
        self.entries[0]["id"] = "Hero Photo"
        self.save()
        self.assertEqual(self.codes(), (1, ["ENTRY_ID"]))

    def test_entry_duplicate_id(self):
        self.entries[1]["id"] = "hero-photo"
        self.save()
        self.assertEqual(self.codes(), (1, ["ENTRY_DUPLICATE_ID"]))

    def test_entry_duplicate_path(self):
        clone = dict(self.entries[0], id="hero-photo-again")
        self.entries.append(clone)
        self.save()
        self.assertEqual(self.codes(), (1, ["ENTRY_DUPLICATE_PATH"]))

    def test_entry_date(self):
        self.entries[0]["date"] = "2026-13-01"
        self.save()
        self.assertEqual(self.codes(), (1, ["ENTRY_DATE"]))

    def test_entry_source(self):
        self.entries[0]["sourceUrl"] = "a stock site"
        self.save()
        self.assertEqual(self.codes(), (1, ["ENTRY_SOURCE"]))

    def test_entry_origin(self):
        self.entries[2]["origin"] = "borrowed"
        self.save()
        self.assertEqual(self.codes(), (1, ["ENTRY_ORIGIN"]))

    def test_entry_path(self):
        self.entries[0]["path"] = "../outside.jpg"
        self.entries[1]["path"] = os.path.abspath(self.path("public", "fonts", "inter.woff2"))
        self.save()
        code, found = self.codes()
        self.assertEqual(code, 1)
        self.assertEqual(found.count("ENTRY_PATH"), 2)
        self.assertEqual(found.count("FILE_UNRECORDED"), 2)

    def test_manifest_invalid(self):
        os.remove(self.manifest)
        self.assertEqual(self.codes(), (1, ["MANIFEST_INVALID"]))
        write(self.manifest, "[]")
        self.assertEqual(self.codes(), (1, ["MANIFEST_INVALID"]))
        write(self.manifest, "{oops")
        self.assertEqual(self.codes(), (1, ["MANIFEST_INVALID"]))

    def test_ignore_patterns(self):
        write(self.path("public", "og", "card.png"), b"og")
        self.save(ignore=["public/og/*"])
        code, doc = self.check()
        self.assertEqual(code, 0)
        self.assertEqual(doc["info"]["ignored"], 1)

    def test_blanket_ignore_is_refused(self):
        # Review finding: one glob such as "*" let every unrecorded file pass.
        write(self.path("public", "img", "stock.jpg"), b"stock")
        for pattern in ("*", "**", "**/*", "*.*", "public/*", "public/**", "*.jpg", "public/img/../*",
                        {"pattern": "design/assets/*", "reason": "generated"}):
            self.save(ignore=[pattern])
            code, found = self.codes()
            self.assertEqual(code, 1, pattern)
            self.assertIn("MANIFEST_IGNORE", found, pattern)
            self.assertIn("FILE_UNRECORDED", found, pattern)

    def test_ignore_objects_with_a_reason(self):
        write(self.path("public", "og", "card.png"), b"og")
        self.save(ignore=[{"pattern": "public/og/*.png", "reason": "built by the og script"}])
        code, doc = self.check()
        self.assertEqual(code, 0)
        self.assertEqual(doc["info"]["ignoredFiles"], ["public/og/card.png"])

    def test_ignored_file_is_still_compared_with_references(self):
        write(self.path("public", "og", "card.png"), b"captured")
        write(self.path("design", "directions", "refs", "competitor.png"), b"captured")
        self.save(ignore=["public/og/*"])
        code, found = self.codes()
        self.assertEqual(code, 1)
        self.assertEqual(found, ["REFERENCE_SHIPPED"])

    def catalog(self):
        path = self.path("catalog.json")
        base = {"name": "x", "url": "https://example.com", "group": "photo-video", "holds": "x", "license": "x",
                "fetch": "x", "risk": "x", "verifiedOn": "2026-11-23"}
        sources = [dict(base, id="free-photos", attribution="none: no credit", commercialUse="yes"),
                   dict(base, id="gallery", attribution="n/a", commercialUse="reference-only"),
                   dict(base, id="credit-icons", attribution="required: name the author", commercialUse="yes"),
                   dict(base, id="mystery", attribution="unknown", commercialUse="unknown", verifiedOn=None)]
        write_json(path, {"version": 1, "groups": ["photo-video"], "sources": sources})
        return path

    def test_catalog_terms_check(self):
        catalog = self.catalog()
        self.entries[0]["catalogId"] = "gallery"
        self.entries[1]["catalogId"] = "credit-icons"
        self.entries[3]["catalogId"] = "nowhere"
        self.save()
        code, found = self.codes("--catalog", catalog)
        self.assertEqual(code, 1)
        self.assertEqual(sorted(found), ["CATALOG_CREDIT", "CATALOG_REFERENCE_ONLY", "CATALOG_UNKNOWN"])
        self.entries[0]["catalogId"] = "free-photos"
        self.entries[1]["attribution"] = "Icons by A. Author, CC BY 4.0"
        self.entries[3]["catalogId"] = "mystery"
        self.save()
        self.assertEqual(self.codes("--catalog", catalog), (1, ["CATALOG_TERMS_UNKNOWN"]))
        del self.entries[3]["catalogId"]
        self.save()
        self.assertEqual(self.codes("--catalog", catalog), (0, []))

    def test_kit_catalog_is_the_default(self):
        self.entries[0]["catalogId"] = "not-a-catalog-id"
        self.save()
        code, doc = self.check()
        self.assertEqual(code, 1)
        self.assertTrue(doc["info"]["catalog"].endswith(os.path.join("catalogs", "assets.json")))
        self.assertEqual(self.codes("--no-catalog"), (0, []))

    def test_custom_asset_dir(self):
        write(self.path("media", "clip.mp4"), b"clip")
        self.assertEqual(self.codes(), (0, []))
        code, doc = self.check("--asset-dir", "media")
        self.assertEqual([(f["code"], f["path"]) for f in doc["findings"]], [("FILE_UNRECORDED", "media/clip.mp4")])
        self.assertEqual(doc["info"]["assetDirs"], ["media"])

    def test_skipped_folders(self):
        write(self.path("public", "node_modules", "pkg", "logo.png"), b"dep")
        self.assertEqual(self.codes(), (0, []))

    def test_reference_shipped(self):
        write(self.path("design", "directions", "references", "acme", "shots", "desktop.jpg"), b"hero")
        code, doc = self.check()
        self.assertEqual(code, 1)
        self.assertEqual(doc["findings"][0]["code"], "REFERENCE_SHIPPED")
        self.assertEqual(doc["findings"][0]["path"], "public/img/hero.jpg")
        self.assertIn("design/directions/references/acme/shots/desktop.jpg", doc["findings"][0]["message"])

    def test_reference_files_need_no_entry(self):
        write(self.path("design", "directions", "1-quiet", "board.png"), b"board")
        self.assertEqual(self.codes(), (0, []))

    def test_hotlink_scan(self):
        write(self.path("src", "page.html"), "\n".join([
            '<img src="https://cdn.example.com/photos/team.jpg?w=800">',
            '<link href="https://fonts.googleapis.com/css2?family=Inter" rel="stylesheet">',
            '<svg xmlns="http://www.w3.org/2000/svg"></svg>',
            '<a href="https://example.com/pricing">Pricing</a>',
            '<img src="/img/hero.jpg">',
        ]))
        self.assertEqual(self.codes(), (0, []))
        code, doc = self.check("--scan", "src")
        self.assertEqual(code, 1)
        self.assertEqual([f["code"] for f in doc["findings"]], ["HOTLINK", "HOTLINK"])
        self.assertIn("line 1", doc["findings"][0]["message"])
        self.assertIn("fonts.googleapis.com", doc["findings"][1]["message"])

    def test_hotlink_exception_needs_a_reason(self):
        write(self.path("src", "app.css"), '@import url("https://use.typekit.net/abc.css");\n')
        self.save(hotlinkExceptions=[{"prefix": "https://use.typekit.net/",
                                      "reason": "The font vendor forbids self-hosting."}])
        code, doc = self.check("--scan", "src")
        self.assertEqual(code, 0)
        self.assertEqual(doc["info"]["hotlinkExempted"], 1)
        self.save(hotlinkExceptions=[{"prefix": "https://use.typekit.net/", "reason": ""}])
        self.assertEqual(self.codes("--scan", "src"), (1, ["MANIFEST_EXCEPTION", "HOTLINK"]))

    def test_root_must_be_a_folder(self):
        code, _out, _err = run(["check", self.manifest, "--root", self.path("nope")])
        self.assertEqual(code, 2)

    def test_check_writes_nothing(self):
        before = sorted(os.path.join(d, f) for d, _dirs, files in os.walk(self.tmp) for f in files)
        text = read_text(self.manifest)
        self.check("--scan", "public")
        after = sorted(os.path.join(d, f) for d, _dirs, files in os.walk(self.tmp) for f in files)
        self.assertEqual(before, after)
        self.assertEqual(read_text(self.manifest), text)

    def test_record_then_check_round_trip(self):
        extra = self.path("public", "img", "extra.png")
        write(extra, b"extra")
        code, _ = run_json(["record", self.manifest, "--id", "extra-art", "--source-url", "https://example.com/x",
                            "--license", "CC BY 4.0, https://creativecommons.org/licenses/by/4.0/",
                            "--attribution", "Extra by A. Maker, CC BY 4.0", "--date", "2026-11-23",
                            "--file", extra])
        self.assertEqual(code, 0)
        self.assertEqual(self.codes(), (0, []))


class CodeCoverageTests(unittest.TestCase):
    def test_each_code_has_a_test(self):
        with open(os.path.abspath(__file__), "r", encoding="utf-8") as fh:
            text = fh.read()
        for code in assets.CODES:
            self.assertGreaterEqual(text.count('"%s"' % code), 1, code)


# ---------------------------------------------------------------- notices

class NoticesTests(TempCase):
    def setUp(self):
        super().setUp()
        self.manifest = self.path("design", "assets", "manifest.json")
        self.output = self.path("ATTRIBUTION.md")
        self.entries = [
            {"id": "wave-pattern", "sourceUrl": "https://example.com/patterns/wave", "license": "CC BY 4.0",
             "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
             "attribution": "Wave pattern by A. Maker, CC BY 4.0", "date": "2026-11-23",
             "path": "public/img/wave.svg", "sha256": "0" * 64, "modified": True},
            {"id": "hero-photo", "sourceUrl": "https://example.com/photo/1", "license": "CC0-1.0 | public domain",
             "attribution": "none required", "date": "2026-11-20", "path": "public/img/hero.jpg", "sha256": "1" * 64},
            {"id": "motion-lib", "sourceUrl": "https://example.com/motion", "license": "MIT",
             "attribution": "None required.", "date": "2026-11-21", "package": "motion@1.0.0"},
            {"id": "own-mark", "sourceUrl": "project", "license": "owned by the client", "origin": "own",
             "attribution": "none required", "date": "2026-11-22", "path": "design/assets/mark.svg",
             "sha256": "2" * 64},
        ]
        write_json(self.manifest, {"version": 1, "assets": self.entries})

    def notices(self, *argv):
        return run_json(["notices", self.manifest, "-o", self.output, "--label", "design/assets/manifest.json"]
                        + list(argv))

    def test_writes_the_three_sections(self):
        code, doc = self.notices()
        self.assertEqual(code, 0)
        self.assertEqual(doc["counts"], {"credited": 1, "noCredit": 2, "own": 1})
        text = read_text(self.output)
        self.assertTrue(text.startswith("# Third-party notices\n"))
        self.assertIn("Generated from `design/assets/manifest.json`", text)
        credits = text.split("## Credits")[1].split("## Other outside and generated assets")[0]
        self.assertIn("- Credit: Wave pattern by A. Maker, CC BY 4.0", credits)
        self.assertIn("- License text: https://creativecommons.org/licenses/by/4.0/", credits)
        self.assertIn("- Changed by this project: yes", credits)
        self.assertNotIn("hero-photo", credits)
        other = text.split("## Other outside and generated assets")[1].split("## Assets made by this project")[0]
        self.assertIn("| hero-photo | `public/img/hero.jpg` |", other)
        self.assertIn("| motion-lib | `motion@1.0.0` |", other)
        self.assertIn("CC0-1.0 \\| public domain", other)
        self.assertIn("| own-mark | `design/assets/mark.svg` |", text.split("## Assets made by this project")[1])

    def test_output_is_deterministic_and_sorted(self):
        self.notices()
        first = read_text(self.output)
        self.entries.reverse()
        write_json(self.manifest, {"version": 1, "assets": self.entries})
        self.notices()
        self.assertEqual(read_text(self.output), first)
        self.assertLess(first.index("hero-photo"), first.index("motion-lib"))

    def test_title_option(self):
        self.notices("--title", "Credits and licenses")
        self.assertTrue(read_text(self.output).startswith("# Credits and licenses\n"))

    def test_empty_manifest(self):
        write_json(self.manifest, {"version": 1, "assets": []})
        code, doc = self.notices()
        self.assertEqual(code, 0)
        text = read_text(self.output)
        self.assertIn("No asset in this project needs a credit line.", text)
        self.assertNotIn("## Assets made by this project", text)

    def test_incomplete_entry_writes_nothing(self):
        self.entries[0]["license"] = ""
        write_json(self.manifest, {"version": 1, "assets": self.entries})
        code, doc = self.notices()
        self.assertEqual(code, 1)
        self.assertEqual(doc["findings"][0]["code"], "ENTRY_FIELD")
        self.assertFalse(os.path.exists(self.output))

    def test_missing_manifest(self):
        os.remove(self.manifest)
        code, doc = self.notices()
        self.assertEqual(code, 1)
        self.assertEqual(doc["findings"][0]["code"], "MANIFEST_INVALID")
        self.assertFalse(os.path.exists(self.output))


# ---------------------------------------------------------------- group reference files

class GroupFileTests(unittest.TestCase):
    """The group files of find-assets name catalog ids. Keep them in step with the catalog."""

    REFERENCES = os.path.join(ROOT, "kit", "skills", "find-assets", "references")
    TOKEN_RE = re.compile(r"`([a-z0-9][a-z0-9-]*)(\*?)`")

    @classmethod
    def setUpClass(cls):
        with open(CATALOG, "r", encoding="utf-8") as fh:
            cls.doc = json.load(fh)
        cls.by_id = {entry["id"]: entry for entry in cls.doc["sources"]}

    def tokens(self, name):
        return self.TOKEN_RE.findall(read_text(os.path.join(self.REFERENCES, name)))

    def test_each_group_has_a_file_that_names_every_id(self):
        for group in self.doc["groups"]:
            name = "group-%s.md" % group
            self.assertTrue(os.path.isfile(os.path.join(self.REFERENCES, name)), name)
            named = {token for token, _star in self.tokens(name)}
            for entry in self.doc["sources"]:
                if entry["group"] == group:
                    self.assertIn(entry["id"], named, "%s does not name %s" % (name, entry["id"]))

    def test_star_marks_exactly_the_unverified_ids(self):
        for group in self.doc["groups"]:
            name = "group-%s.md" % group
            for token, star in self.tokens(name):
                if star:
                    self.assertIn(token, self.by_id, "%s stars a word that is not a catalog id: %s" % (name, token))
                if token in self.by_id:
                    unverified = self.by_id[token]["verifiedOn"] is None
                    self.assertEqual(bool(star), unverified, "%s: star and verifiedOn disagree for %s" % (name, token))

    def test_known_limits_table_names_catalog_ids(self):
        text = read_text(os.path.join(self.REFERENCES, "license-decision.md"))
        table = text.split("## Known limits in the catalog")[1].split("## Marks, people and logos")[0]
        ids = [token for token, _star in self.TOKEN_RE.findall(table)]
        self.assertGreater(len(ids), 20)
        for token in ids:
            self.assertIn(token, self.by_id, token)

    def test_search_order_lists_every_group(self):
        text = read_text(os.path.join(self.REFERENCES, "search-order.md"))
        for group in self.doc["groups"]:
            self.assertIn("`%s`" % group, text)
            self.assertIn("group-%s.md" % group, text)


# ---------------------------------------------------------------- CLI and script rules

class CliTests(unittest.TestCase):
    def test_no_subcommand_exits_2(self):
        code, out, _ = run([])
        self.assertEqual(code, 2)
        self.assertIn("search", out)

    def test_script_has_no_network_code(self):
        with open(SCRIPT, "r", encoding="utf-8") as fh:
            text = fh.read()
        for pattern in (r"urllib\.request", r"http\.client", r"^\s*(?:import|from)\s+(?:socket|requests|httpx)\b",
                        r"\bsubprocess\b", r"\bos\.system\b"):
            self.assertIsNone(re.search(pattern, text, re.M), pattern)

    def test_script_imports_only_the_standard_library(self):
        with open(SCRIPT, "r", encoding="utf-8") as fh:
            text = fh.read()
        modules = set(re.findall(r"^(?:import|from)\s+([a-zA-Z_]+)", text, re.M))
        self.assertEqual(modules, {"argparse", "datetime", "fnmatch", "hashlib", "json", "os", "re", "sys",
                                   "collections"})


if __name__ == "__main__":
    unittest.main()
