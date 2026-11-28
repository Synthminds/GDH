"""Tests for kit/skills/ask-gdh/scripts/local_clis.py and the real local-clis.json catalog."""
import contextlib
import copy
import importlib.util
import io
import json
import os
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "kit", "skills", "ask-gdh", "scripts", "local_clis.py")
CATALOG = os.path.join(REPO, "kit", "catalogs", "local-clis.json")
CAPS = os.path.join(REPO, "kit", "catalogs", "capabilities.json")
TOOL = os.path.join(REPO, "kit", "catalogs", "tools", "cli-anything.json")

spec = importlib.util.spec_from_file_location("local_clis", SCRIPT)
lc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = lc.main(list(argv))
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


def fake_which(present):
    return lambda name: ("/usr/bin/" + name) if name in present else None


class RealCatalogTests(unittest.TestCase):
    def setUp(self):
        self.doc = load(CATALOG)
        self.vocab, self.disciplines = lc.vocabulary(load(CAPS))

    def test_real_catalog_is_valid(self):
        self.assertEqual(lc.validate(self.doc, self.vocab, self.disciplines), [])

    def test_pin_is_a_full_commit(self):
        self.assertRegex(self.doc["upstream"]["commit"], r"^[0-9a-f]{40}$")

    def test_every_install_is_pinned_to_the_commit(self):
        commit = self.doc["upstream"]["commit"]
        for entry in self.doc["clis"]:
            command = lc.install_command(self.doc, entry)
            self.assertIn("@%s#subdirectory=" % commit, command)
            self.assertNotIn("@main", command)

    def test_internet_harnesses_expose(self):
        for entry in self.doc["clis"]:
            if entry["network"] == "internet":
                self.assertTrue(entry["exposes"], entry["id"])

    def test_umbrella_entry_covers_every_capability(self):
        tool = load(TOOL)
        used = set(c for e in self.doc["clis"] for c in e["capabilities"])
        self.assertEqual(used, set(tool["capabilities"]))
        self.assertTrue(tool["exposes"])
        self.assertFalse(tool["spendsCredits"])


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self.doc = load(CATALOG)

    def codes(self, doc):
        return set(f["code"] for f in lc.validate(doc))

    def test_branch_pin_is_refused(self):
        doc = copy.deepcopy(self.doc)
        doc["upstream"]["commit"] = "main"
        self.assertIn("PIN", self.codes(doc))

    def test_path_traversal_is_refused(self):
        doc = copy.deepcopy(self.doc)
        doc["clis"][0]["installPath"] = "../evil/agent-harness"
        self.assertIn("PATH", self.codes(doc))
        doc = copy.deepcopy(self.doc)
        doc["clis"][0]["upstreamSkill"] = "../../etc/passwd"
        self.assertIn("PATH", self.codes(doc))

    def test_harness_must_be_a_bare_command(self):
        doc = copy.deepcopy(self.doc)
        doc["clis"][0]["harness"] = "cli; rm -rf /"
        self.assertIn("HARNESS", self.codes(doc))

    def test_backend_names_are_binaries(self):
        doc = copy.deepcopy(self.doc)
        doc["clis"][0]["backend"] = [["inkscape && curl x"]]
        self.assertIn("BACKEND", self.codes(doc))
        doc["clis"][0]["backend"] = [[]]
        self.assertIn("BACKEND", self.codes(doc))

    def test_internet_without_exposes_is_refused(self):
        doc = copy.deepcopy(self.doc)
        doc["clis"][0]["network"] = "internet"
        doc["clis"][0]["exposes"] = False
        self.assertIn("EXPOSES", self.codes(doc))

    def test_duplicate_id_is_refused(self):
        doc = copy.deepcopy(self.doc)
        doc["clis"].append(copy.deepcopy(doc["clis"][0]))
        self.assertIn("ID", self.codes(doc))

    def test_unknown_capability_with_vocabulary(self):
        doc = copy.deepcopy(self.doc)
        doc["clis"][0]["capabilities"] = ["teleport"]
        found = set(f["code"] for f in lc.validate(doc, {"vector"}, {"logo"}))
        self.assertIn("CAPABILITY", found)

    def test_non_object(self):
        self.assertEqual(self.codes([]), {"SCHEMA"})


class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.doc = load(CATALOG)

    def by_id(self, rows):
        return {r["id"]: r for r in rows}

    def test_states(self):
        rows = self.by_id(lc.probe(self.doc, which=fake_which({
            "cli-anything-inkscape", "inkscape", "cli-anything-gimp", "melt"})))
        self.assertEqual(rows["inkscape"]["state"], "ready")
        self.assertNotIn("install", rows["inkscape"])
        self.assertEqual(rows["gimp"]["state"], "needs-backend")
        self.assertEqual(rows["gimp"]["missingBackend"], ["gimp or gimp-console"])
        self.assertEqual(rows["kdenlive"]["state"], "needs-harness")
        self.assertIn("install", rows["kdenlive"])
        self.assertEqual(rows["blender"]["state"], "needs-both")

    def test_all_backend_groups_are_needed(self):
        rows = self.by_id(lc.probe(self.doc, which=fake_which({"cli-anything-shotcut", "melt"})))
        self.assertEqual(rows["shotcut"]["state"], "needs-backend")
        self.assertEqual(rows["shotcut"]["missingBackend"], ["ffmpeg"])

    def test_capability_filter(self):
        rows = lc.probe(self.doc, ["vector"], which=fake_which(set()))
        self.assertEqual([r["id"] for r in rows], ["inkscape"])

    def test_localhost_service_is_flagged(self):
        rows = self.by_id(lc.probe(self.doc, which=fake_which({"cli-anything-comfyui"})))
        self.assertEqual(rows["comfyui"]["state"], "ready")
        self.assertIn("serviceCheck", rows["comfyui"])

    def test_summary_lists_ready_ids(self):
        rows = lc.probe(self.doc, which=fake_which({"cli-anything-inkscape", "inkscape"}))
        summary = lc.capability_summary(rows)
        self.assertEqual(summary["vector"], ["inkscape"])
        self.assertEqual(summary["image-edit"], [])


class CommandLineTests(unittest.TestCase):
    def test_validate_passes(self):
        code, out, _ = run("validate", "--json")
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out)["ok"])

    def test_probe_json_shape(self):
        code, out, _ = run("probe", "--capability", "slides", "--json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual([r["id"] for r in data["clis"]], ["libreoffice"])
        self.assertIn("slides", data["ready"])

    def test_install_prints_only(self):
        code, out, _ = run("install", "gimp")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith('python3 -m pip install "git+https://github.com/HKUDS/CLI-Anything.git@'))

    def test_usage_errors(self):
        self.assertEqual(run()[0], 2)
        self.assertEqual(run("install", "nope")[0], 2)
        self.assertEqual(run("--catalog", "/nonexistent/x.json", "probe")[0], 2)

    def test_invalid_catalog_blocks_probe(self):
        doc = load(CATALOG)
        doc["upstream"]["commit"] = "main"
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "local-clis.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(doc, handle)
            self.assertEqual(run("--catalog", path, "probe")[0], 2)
            self.assertEqual(run("--catalog", path, "validate")[0], 1)


if __name__ == "__main__":
    unittest.main()
