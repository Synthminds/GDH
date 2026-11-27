"""Tests for scripts/gdh.py.

Every test works on a small kit fixture in a temporary folder. No test touches the real kit.
Run: python3 -m unittest discover -s tests
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import gdh  # noqa: E402

TODAY = "2026-06-01"


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def read(root, rel):
    with open(os.path.join(root, rel), "r", encoding="utf-8") as handle:
        return handle.read()


def write_json(root, rel, data):
    write(root, rel, json.dumps(data, indent=2) + "\n")


def read_json(root, rel):
    return json.loads(read(root, rel))


def edit_json(root, rel, change):
    data = read_json(root, rel)
    result = change(data)
    write_json(root, rel, data if result is None else result)


def run(*argv):
    """Run the command line in process. Return (exit code, stdout)."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = gdh.main(list(argv))
    return code, out.getvalue()


def tool_entry(tool_id, fallback="none"):
    return {
        "id": tool_id, "name": tool_id.title(), "what": "Makes test images.", "kind": "connector",
        "capabilities": ["image-gen"], "disciplines": ["color"], "install": "Settings, Connectors.",
        "auth": "oauth", "spendsCredits": True, "exposes": False, "readOnly": False,
        "toolPrefix": "mcp__%s__" % tool_id, "firstCall": "none", "fallback": fallback,
        "card": "references/tools/%s.md" % tool_id, "source": "https://example.com/%s" % tool_id,
        "verifiedAt": "2026-05-01", "evidence": "DOCUMENTED", "evidenceNote": "Read the public page.",
    }


def asset_source(asset_id):
    return {"id": asset_id, "name": asset_id, "url": "https://example.com/%s" % asset_id, "group": "icons",
            "holds": "icons", "license": "MIT", "attribution": "none", "commercialUse": True, "fetch": "download",
            "risk": "low", "verifiedOn": "2026-05-01"}


def make_fixture(root):
    """Write a small valid kit, then run build."""
    write_json(root, "kit/kit.json", {
        "name": "gdh", "displayName": "Test Harness", "version": "0.1.0", "description": "A test kit.",
        "author": {"name": "Test Org"}, "repository": "https://example.com/gdh", "license": "UNLICENSED",
        "budgets": {"modelDescriptionChars": 5000, "kernelLines": 60, "momentsChars": 3500},
        "skills": {
            "ask-gdh": {"invocation": "model", "origin": "gdh", "discipline": "router"},
            "color": {"invocation": "user", "origin": "gdh", "discipline": "color"},
        },
        "agents": ["critic"],
        "moments": [{"when": "The task is design-led", "start": ["ask-gdh"], "offer": ["color", "taste"]}],
        "wired": {"taste": {"name": "Taste", "what": "visual taste", "install": "/plugin install taste",
                            "source": "https://example.com/taste"}},
        "requires": {},
    })
    write(root, "kit/skills/ask-gdh/SKILL.md",
          "---\nname: ask-gdh\ndescription: Routes a design task to the right skill. Use it first.\n---\n\n"
          "# ask-gdh\n\nRoute a palette task to `color`.\n\n## References\n\n"
          "- [Routes](references/routes.md): read it for the full table.\n")
    write(root, "kit/skills/ask-gdh/references/routes.md", "# Routes\n\nSee the [kernel](../../../canon/KERNEL.md).\n")
    write(root, "kit/skills/ask-gdh/refinement-log.md", "# Refinement log\n")
    write(root, "kit/skills/color/SKILL.md",
          "---\nname: color\ndescription: Builds a palette.\ndisable-model-invocation: true\n---\n\n# color\n\nBody.\n")
    write(root, "kit/skills/color/refinement-log.md", "# Refinement log\n")
    write(root, "kit/agents/critic.md", "---\nname: critic\ndescription: Reviews a design.\n---\n\nReview it.\n")
    write(root, "kit/canon/KERNEL.md", "# Kernel\n\n1. Precedence: the user ranks first.\n\n"
          "Skill handoff: read the skill's `SKILL.md`, or print `/gdh:<name>`.\n")
    write(root, "kit/canon/PRINCIPLES.md", "# Principles\n\nBody.\n")
    write_json(root, "kit/catalogs/capabilities.json", {
        "version": 1, "capabilities": ["image-gen", "fonts"],
        "disciplines": {"color": {"skill": "color", "capabilities": ["image-gen"]}},
    })
    write_json(root, "kit/catalogs/tools/alpha.json", tool_entry("alpha"))
    write_json(root, "kit/catalogs/tools/beta.json", tool_entry("beta", fallback="alpha"))
    write(root, "kit/references/tools/alpha.md", "# Alpha\n\nCard.\n")
    write(root, "kit/references/tools/beta.md", "# Beta\n\nCard.\n")
    write_json(root, "kit/catalogs/assets.json", {"version": 1, "sources": [asset_source("one"), asset_source("two")]})
    write_json(root, "kit/scan.accepted.json", [])
    write(root, "kit/templates/project/DESIGN.md", "# Design\n\nSee [the brief](design/brief.md).\n")
    write(root, "kit/templates/project/design/brief.md", "# Brief\n")
    write(root, "kit/README.md", "# Kit\n\n%s\n%s\n" % (gdh.CATALOG_START, gdh.CATALOG_END))
    write(root, "README.md", "# Repo\n\n%s\nold\n%s\n\nTail.\n" % (gdh.CATALOG_START, gdh.CATALOG_END))
    write(root, "docs/GDH.md", "# GDH\n\nRead the [kernel](../kit/canon/KERNEL.md).\n")
    write(root, ".gitignore", "__pycache__/\n\n# Brand packs are private by default.\nbrands/*\n!brands/README.md\n!brands/_template/\n!brands/example-harbor-lantern/\n")
    write(root, "brands/acme/README.md", "# Acme\n")
    write_json(root, "brands/acme/tokens.json", {"color": []})
    write(root, "brands/_template/README.md", "# Template\n")
    write_json(root, "evals/cases/triggering/trigger-ask-gdh.json", {
        "id": "trigger-ask-gdh", "kind": "triggering", "skill": "ask-gdh",
        "prompt": "Make our landing page look less generic.", "expect": {"skills_fired": ["ask-gdh"]}})
    write(root, "scripts/tool.py", "import json\nprint(json.dumps({}))\n")
    code, out = run("build", "--root", root)
    assert code == 0, out


def codes(root):
    findings, _ = gdh.run_check(root)
    return set(f["code"] for f in findings)


def set_key(key, value):
    def change(data):
        data[key] = value
    return change


def replace(rel, old, new):
    def mutate(root):
        text = read(root, rel)
        assert old in text, (rel, old)
        write(root, rel, text.replace(old, new))
    return mutate


def append(rel, text):
    return lambda root: write(root, rel, read(root, rel) + text)


def kit_edit(change):
    return lambda root: edit_json(root, "kit/kit.json", change)


def alpha(key, value):
    return lambda root: edit_json(root, "kit/catalogs/tools/alpha.json", set_key(key, value))


def asset_edit(change):
    return lambda root: edit_json(root, "kit/catalogs/assets.json", lambda d: change(d["sources"]))


def moment(**fields):
    def change(data):
        data["moments"][0].update(fields)
    return kit_edit(change)


SKILL = "kit/skills/color/SKILL.md"
ADDRESS = "person" + "@" + "corp.io"
# Built from parts, so that this file itself holds no private-link shape.
ARTIFACT_LINK = "https://claude" + ".ai/" + "artifact/" + "0f3c9e2a-private-board"
DESIGN_LINK = "https://claude" + ".ai/" + "design/p/" + "abc123"
WORKSPACE_ID = "Workspace " + "wsp" + "_9KQ2abcdEF"
GH_TOKEN = 'token = "' + "gh" + 'p_abcdefghijklmnopqrstuvwxyz0123456789"'

DS_SCRIPT = os.path.join(REPO, "kit", "skills", "design-system", "scripts", "ds.py")


LOCAL_CLIS_SCRIPT = os.path.join(REPO, "kit", "skills", "ask-gdh", "scripts", "local_clis.py")


def local_cli_catalog(commit="0123456789abcdef0123456789abcdef01234567", network="none", exposes=False):
    """A one-entry local-clis.json that fits the fixture vocabulary."""
    return {"version": 1, "note": "Fixture.",
            "upstream": {"repo": "https://github.com/example/harnesses", "commit": commit,
                         "license": "Apache-2.0", "readAt": "2026-11-27"},
            "clis": [{"id": "painter", "name": "Painter", "capabilities": ["image-gen"], "disciplines": ["color"],
                      "harness": "cli-anything-painter", "installPath": "painter/agent-harness",
                      "backend": [["painter"]], "backendNote": "Painter on PATH.", "network": network,
                      "exposes": exposes, "spendsCredits": False,
                      "upstreamSkill": "skills/cli-anything-painter/SKILL.md", "evidence": "DOCUMENTED",
                      "evidenceNote": "Fixture."}]}


def install_local_clis(root, catalog):
    target = os.path.join(root, "kit", "skills", "ask-gdh", "scripts", "local_clis.py")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy(LOCAL_CLIS_SCRIPT, target)
    write_json(root, "kit/catalogs/local-clis.json", catalog)


def scaffold_pack(root):
    """Give the fixture the real design-system script and a pack that still holds the init colors."""
    target = os.path.join(root, "kit", "skills", "design-system", "scripts", "ds.py")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy(DS_SCRIPT, target)
    spec = importlib.util.spec_from_file_location("gdh_ds_fixture", DS_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    write_json(root, "brands/acme/tokens.json", module.starter_tokens("Acme"))


MUTATIONS = {
    "GDH_JSON_INVALID": lambda r: write(r, "kit/catalogs/tools/alpha.json", "{"),
    "GDH_KIT_JSON": kit_edit(lambda d: d.pop("budgets")),
    "GDH_AGENT_REGISTRY": lambda r: os.remove(os.path.join(r, "kit/agents/critic.md")),
    "GDH_FRONTMATTER": lambda r: write(r, SKILL, "# color\n\nBody.\n"),
    "GDH_SKILL_NAME": replace(SKILL, "name: color", "name: Bad_Name"),
    "GDH_SKILL_NAME_FOLDER": replace(SKILL, "name: color", "name: colour"),
    "GDH_SKILL_DESCRIPTION": replace(SKILL, "description: Builds a palette.\n", ""),
    "GDH_DESCRIPTION_BUDGET": kit_edit(lambda d: d["budgets"].update(modelDescriptionChars=5)),
    "GDH_REGISTRY_MISSING_FOLDER": kit_edit(
        lambda d: d["skills"].update(ghost={"invocation": "user", "origin": "gdh", "discipline": "x"})),
    "GDH_REGISTRY_UNREGISTERED": lambda r: write(
        r, "kit/skills/extra/SKILL.md", "---\nname: extra\ndescription: Extra.\ndisable-model-invocation: true\n---\n"),
    "GDH_INVOCATION_FLAG": replace(SKILL, "disable-model-invocation: true\n", ""),
    "GDH_SKILL_SIZE": append(SKILL, "line\n" * 200),
    "GDH_REFERENCE_SIZE": append("kit/skills/ask-gdh/references/routes.md", "line\n" * 401),
    "GDH_LINK_BROKEN": append("docs/GDH.md", "\nSee [nothing](missing.md).\n"),
    "GDH_SKILL_FILE_UNLINKED": lambda r: write(r, "kit/skills/color/references/extra.md", "# Extra\n"),
    "GDH_ROUTER_INCOMPLETE": replace("kit/skills/ask-gdh/SKILL.md", "`color`", "`hue`"),
    "GDH_ROUTE_USER_SKILL": append("kit/skills/ask-gdh/references/routes.md", "\nThen start `color`.\n"),
    "GDH_SYMLINK": lambda r: os.symlink(os.path.join(r, "README.md"), os.path.join(r, "docs", "link.md")),
    "GDH_HTML_COMMENT": append("kit/canon/KERNEL.md", "\n<!" + "-- hidden --" + ">\n"),
    "GDH_BASE64": append("kit/canon/KERNEL.md", "\n" + "QUJD" * 25 + "\n"),
    "GDH_EMOJI": append("kit/canon/KERNEL.md", "\nDone " + chr(0x1F600) + "\n"),
    "GDH_EM_DASH": append("kit/canon/KERNEL.md", "\nA rule " + chr(0x2014) + " with a dash.\n"),
    "GDH_PRINT_FLOOR": append("kit/canon/KERNEL.md", "\nPrint: nothing under 12 pt.\n"),
    "GDH_SECRET": append("docs/GDH.md", "\nWrite to " + ADDRESS + ".\n"),
    "GDH_PRIVATE_LINK": append("docs/GDH.md", "\nBoard: " + ARTIFACT_LINK + "\n"),
    "GDH_SCRIPT_NETWORK": append("scripts/tool.py", "import " + "socket\n"),
    "GDH_KERNEL_MISSING": lambda r: os.remove(os.path.join(r, "kit/canon/KERNEL.md")),
    "GDH_KERNEL_BUDGET": kit_edit(lambda d: d["budgets"].update(kernelLines=1)),
    "GDH_MOMENTS_BUDGET": kit_edit(lambda d: d["budgets"].update(momentsChars=10)),
    "GDH_HOOK_BUDGET": append("kit/canon/KERNEL.md", "\n" + "long rule " * 1000 + "\n"),
    "GDH_MOMENT_SHAPE": moment(when=""),
    "GDH_MOMENT_OFFER_LIMIT": moment(offer=["color", "taste", "color", "taste"]),
    "GDH_MOMENT_SKILL_UNKNOWN": moment(offer=["nope"]),
    "GDH_MOMENT_START_USER": moment(start=["color"], offer=[]),
    "GDH_CAPABILITIES_SCHEMA": lambda r: write_json(r, "kit/catalogs/capabilities.json", {}),
    "GDH_CAPABILITIES_DISCIPLINE": lambda r: edit_json(
        r, "kit/catalogs/capabilities.json", lambda d: d["disciplines"]["color"].update(skill="ghost")),
    "GDH_TOOL_FIELD": alpha("spendsCredits", "yes"),
    "GDH_TOOL_ENUM": alpha("kind", "saas"),
    "GDH_LOCAL_CLI": lambda r: install_local_clis(r, local_cli_catalog(commit="main")),
    "GDH_TOOL_ID": alpha("id", "other"),
    "GDH_TOOL_CAPABILITY": alpha("capabilities", ["teleport"]),
    "GDH_TOOL_DISCIPLINE": alpha("disciplines", ["alchemy"]),
    "GDH_TOOL_FALLBACK": alpha("fallback", "ghost"),
    "GDH_TOOL_CARD": lambda r: os.remove(os.path.join(r, "kit/references/tools/alpha.md")),
    "GDH_TOOL_DATE": alpha("verifiedAt", "2026-13-45"),
    "GDH_TOOL_SOURCE": alpha("source", "http://example.com/alpha"),
    "GDH_ASSETS_FIELD": asset_edit(lambda s: s[0].pop("license")),
    "GDH_ASSETS_DUPLICATE_ID": asset_edit(lambda s: s[1].update(id="one")),
    "GDH_ASSETS_DATE": asset_edit(lambda s: s[0].update(verifiedOn="yesterday")),
    "GDH_ASSETS_URL": asset_edit(lambda s: s[0].update(url="http://example.com/one")),
    "GDH_BRAND_PACK": lambda r: os.remove(os.path.join(r, "brands/acme/tokens.json")),
    "GDH_BRAND_PUBLIC": lambda r: write(r, ".gitignore", "__pycache__/\n"),
    "GDH_BRAND_SCAFFOLD": lambda r: scaffold_pack(r),
    "GDH_EVAL_CASE": lambda r: edit_json(r, "evals/cases/triggering/trigger-ask-gdh.json", set_key("kind", "outcome")),
    "GDH_GENERATED_DRIFT": append("kit/canon/MOMENTS.md", "\nA hand edit.\n"),
    "GDH_ACCEPTED_INVALID": lambda r: write_json(r, "kit/scan.accepted.json", {"code": "GDH_SECRET"}),
}


class FixtureCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._base = tempfile.mkdtemp(prefix="gdh-test-")
        cls.template = os.path.join(cls._base, "template")
        os.makedirs(cls.template)
        make_fixture(cls.template)
        cls._count = 0

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._base, ignore_errors=True)

    def fresh(self):
        type(self)._count += 1
        target = os.path.join(self._base, "kit-%d" % self._count)
        shutil.copytree(self.template, target)
        return target

    def folder(self):
        type(self)._count += 1
        target = os.path.join(self._base, "dir-%d" % self._count)
        os.makedirs(target)
        return target


class CheckTests(FixtureCase):
    def test_valid_fixture_passes(self):
        root = self.fresh()
        findings, accepted = gdh.run_check(root)
        self.assertEqual(findings, [])
        self.assertEqual(accepted, [])
        code, out = run("check", "--root", root)
        self.assertEqual(code, 0)
        self.assertIn("0 finding(s)", out)

    def test_local_cli_catalog_is_checked(self):
        root = self.fresh()
        install_local_clis(root, local_cli_catalog())
        self.assertNotIn("GDH_LOCAL_CLI", codes(root))
        install_local_clis(root, local_cli_catalog(network="internet", exposes=False))
        self.assertIn("GDH_LOCAL_CLI", codes(root))
        bad = local_cli_catalog()
        bad["clis"][0]["capabilities"] = ["teleport"]
        install_local_clis(root, bad)
        self.assertIn("GDH_LOCAL_CLI", codes(root))

    def test_every_code_has_a_mutation(self):
        self.assertEqual(set(MUTATIONS), set(gdh.CODES))

    def test_each_mutation_reports_its_code(self):
        for code, mutate in sorted(MUTATIONS.items()):
            with self.subTest(code=code):
                root = self.fresh()
                mutate(root)
                self.assertIn(code, codes(root))
                self.assertEqual(run("check", "--root", root)[0], 1)

    def test_print_floor_rule_reads_clauses(self):
        flagged = ["Print: nothing under 12 pt.", "Default: print text 12 pt or more.", "Slides: minimum 12pt.",
                   "| Print | at least 12 pt |"]
        kept = ["Print body at least 12 pt.", "Print body text 12 pt (16 px); no print text under 12 px.",
                "12 pt equals 16 px.", "The band's label is 12 pt regular.", "body 16 px (12 pt), nothing under 12 px"]
        for line in flagged:
            self.assertTrue(gdh.print_floor_clauses(line), line)
        for line in kept:
            self.assertEqual(gdh.print_floor_clauses(line), [], line)

    def test_brand_scaffold_spares_the_template(self):
        root = self.fresh()
        scaffold_pack(root)
        write_json(root, "brands/_template/tokens.json", read_json(root, "brands/acme/tokens.json"))
        found = [f for f in gdh.run_check(root)[0] if f["code"] == "GDH_BRAND_SCAFFOLD"]
        self.assertEqual([f["path"] for f in found], ["brands/acme/tokens.json"])

    def test_gitignored_private_pack_is_still_checked(self):
        root = self.fresh()
        write(root, "brands/private-pack/README.md", "# Private pack\n")
        self.assertIn("GDH_BRAND_PACK", codes(root))
        write_json(root, "brands/private-pack/tokens.json", read_json(root, "brands/acme/tokens.json"))
        self.assertNotIn("GDH_BRAND_PACK", codes(root))

    def test_json_output(self):
        root = self.fresh()
        MUTATIONS["GDH_EM_DASH"](root)
        code, out = run("check", "--root", root, "--json")
        data = json.loads(out)
        self.assertEqual(code, 1)
        self.assertFalse(data["ok"])
        self.assertEqual(data["findings"][0]["code"], "GDH_EM_DASH")
        self.assertEqual(data["findings"][0]["path"], "kit/canon/KERNEL.md")

    def test_accepted_finding_is_skipped_and_reported(self):
        root = self.fresh()
        MUTATIONS["GDH_EM_DASH"](root)
        write_json(root, "kit/scan.accepted.json",
                   [{"code": "GDH_EM_DASH", "path": "kit/canon/KERNEL.md", "reason": "quoted source"}])
        findings, accepted = gdh.run_check(root)
        self.assertEqual(findings, [])
        self.assertEqual([a["code"] for a in accepted], ["GDH_EM_DASH"])
        code, out = run("check", "--root", root)
        self.assertEqual(code, 0)
        self.assertIn("accepted", out)

    def leak(self):
        """A fixture copy with one token line. Return (root, finding)."""
        root = self.fresh()
        write(root, "kit/references/leak.txt", GH_TOKEN + "\n")
        findings = [f for f in gdh.run_check(root)[0] if f["code"] == "GDH_SECRET"]
        self.assertTrue(findings)
        return root, findings[0]

    def test_glob_waiver_cannot_hide_a_secret(self):
        root, _ = self.leak()
        for path in ("*", "**", "kit/*", "kit/references/*.txt"):
            with self.subTest(path=path):
                write_json(root, "kit/scan.accepted.json",
                           [{"code": "GDH_SECRET", "path": path, "reason": "false positive"}])
                found = codes(root)
                self.assertIn("GDH_SECRET", found)
                self.assertIn("GDH_ACCEPTED_INVALID", found)
                code, out = run("check", "--root", root)
                self.assertEqual(code, 1)
                self.assertIn("0 accepted", out)

    def test_secret_waiver_needs_the_line_digest(self):
        root, finding = self.leak()
        self.assertEqual(finding["match"], gdh.line_digest(GH_TOKEN))
        rel = "kit/references/leak.txt"
        write_json(root, "kit/scan.accepted.json", [{"code": "GDH_SECRET", "path": rel, "reason": "sample"}])
        self.assertEqual(codes(root), {"GDH_SECRET", "GDH_ACCEPTED_INVALID"})
        write_json(root, "kit/scan.accepted.json",
                   [{"code": "GDH_SECRET", "path": rel, "reason": "sample", "match": "0" * 64}])
        self.assertEqual(codes(root), {"GDH_SECRET"})
        write_json(root, "kit/scan.accepted.json",
                   [{"code": "GDH_SECRET", "path": rel, "reason": "sample", "match": finding["match"]}])
        findings, accepted = gdh.run_check(root)
        self.assertEqual(findings, [])
        self.assertEqual(set(a["code"] for a in accepted), {"GDH_SECRET"})
        # The waiver covers that one line. A second secret in the same file is still a finding.
        write(root, rel, GH_TOKEN + "\nkey = " + "sk-" + "a1B2c3D4e5F6g7H8i9J0k1L2\n")
        self.assertEqual(codes(root), {"GDH_SECRET"})

    def test_waiver_shapes_that_are_refused(self):
        root = self.fresh()
        MUTATIONS["GDH_EM_DASH"](root)
        bad = [
            {"code": "GDH_EM_DASH", "path": "*", "reason": "all"},
            {"code": "GDH_EM_DASH", "path": "**/*", "reason": "all"},
            {"code": "GDH_EM_DASH", "path": "kit/canon/KERNEL.md", "reason": ""},
            {"code": "GDH_EM_DASH", "path": "kit/canon/KERNEL.md", "reason": "x", "match": "short"},
            {"code": "GDH_ACCEPTED_INVALID", "path": "kit/scan.accepted.json", "reason": "hide the rest"},
            {"code": "GDH_SYMLINK", "path": "docs/*.md", "reason": "links"},
            {"code": "GDH_NOPE", "path": "kit/canon/KERNEL.md", "reason": "x"},
        ]
        for entry in bad:
            with self.subTest(entry=entry):
                write_json(root, "kit/scan.accepted.json", [entry])
                self.assertIn("GDH_ACCEPTED_INVALID", codes(root))
        # A narrow pattern stays allowed for a style rule, and one bad entry does not drop the good ones.
        write_json(root, "kit/scan.accepted.json", [
            {"code": "GDH_EM_DASH", "path": "kit/canon/*.md", "reason": "quoted source"},
            {"code": "GDH_SECRET", "path": "*", "reason": "too broad"}])
        findings, accepted = gdh.run_check(root)
        self.assertEqual([f["code"] for f in findings], ["GDH_ACCEPTED_INVALID"])
        self.assertEqual([a["code"] for a in accepted], ["GDH_EM_DASH"])

    def test_private_links_and_ids(self):
        for sample in (ARTIFACT_LINK, DESIGN_LINK, WORKSPACE_ID, "org-" + "a1b2c3d4e5f6g7h8",
                       "https://claude" + ".ai/code/session_" + "01AbCdEf/x"):
            with self.subTest(sample=sample[:20]):
                root = self.fresh()
                write(root, "kit/references/board.md", "# Board\n\nSee %s.\n" % sample)
                self.assertIn("GDH_PRIVATE_LINK", codes(root))
        root = self.fresh()
        write(root, "kit/references/board.md",
              "# Board\n\nOpen claude.ai/design. Use `<artifact link>`. The gallery is claude.ai/code/artifacts.\n"
              "The team_members table and an org-wide rule are fine.\n")
        self.assertNotIn("GDH_PRIVATE_LINK", codes(root))
        write(root, "tests/fixtures/board.md", ARTIFACT_LINK + "\n")
        self.assertNotIn("GDH_PRIVATE_LINK", codes(root))

    def test_link_to_a_sibling_repository(self):
        root = self.fresh()
        edit_json(root, "kit/kit.json", set_key("repository", "https://github.com/acme-org/GDH"))
        owner = "acme" + "-org"
        for sample in ("https://github.com/%s/Other" % owner, "/plugin marketplace add %s/other" % owner,
                       "git@github.com:%s/other.git" % owner, "https://GitHub.com/ACME-ORG/lib/blob/main/x.md"):
            with self.subTest(sample=sample):
                write(root, "kit/references/board.md", "# Board\n\nSee %s.\n" % sample)
                self.assertIn("GDH_PRIVATE_LINK", codes(root))
        write(root, "kit/references/board.md",
              "# Board\n\nRun `/plugin marketplace add %s/GDH`. See https://github.com/%s/GDH.git and "
              "https://github.com/someone/other. The %s name alone is fine.\n" % (owner, owner, owner))
        self.assertNotIn("GDH_PRIVATE_LINK", codes(root))

    def test_user_skill_route(self):
        root = self.fresh()
        write(root, "kit/skills/ask-gdh/references/routes.md",
              "# Routes\n\nRun `color`. Start `color`: read its `SKILL.md`. Invoke `color` or print `/gdh:color`.\n"
              "Start `ask-gdh`. Start `taste`. Start `colorful` things.\n")
        self.assertNotIn("GDH_ROUTE_USER_SKILL", codes(root))
        for line in ("Start `color`.", "Invoke the `color` skill.", "It starts `color` next."):
            with self.subTest(line=line):
                write(root, "kit/skills/ask-gdh/references/routes.md", "# Routes\n\n%s\n" % line)
                self.assertIn("GDH_ROUTE_USER_SKILL", codes(root))
        root = self.fresh()
        write(root, "kit/canon/KERNEL.md", "# Kernel\n\n1. Precedence: the user ranks first.\n")
        self.assertIn("GDH_ROUTE_USER_SKILL", codes(root))

    def test_tool_source_may_be_none(self):
        root = self.fresh()
        alpha("source", "none")(root)
        self.assertNotIn("GDH_TOOL_SOURCE", codes(root))
        alpha("source", "private repository")(root)
        self.assertIn("GDH_TOOL_SOURCE", codes(root))

    def test_private_link_in_a_brand_pack(self):
        root = self.fresh()
        write(root, "brands/acme/README.md", "# Acme\n\nBoard: %s\n" % ARTIFACT_LINK)
        self.assertNotIn("GDH_PRIVATE_LINK", codes(root))
        write(root, ".gitignore", "__pycache__/\n")
        found = codes(root)
        self.assertIn("GDH_PRIVATE_LINK", found)
        self.assertIn("GDH_BRAND_PUBLIC", found)

    def test_brand_public_allows_the_template_and_the_example(self):
        root = self.fresh()
        write(root, "brands/example-harbor-lantern/README.md", "# Example\n")
        write_json(root, "brands/example-harbor-lantern/tokens.json", {"color": []})
        self.assertEqual(codes(root), set())
        write(root, "brands/acme-client/README.md", "# Client\n")
        write_json(root, "brands/acme-client/tokens.json", {"color": []})
        self.assertEqual(codes(root), set())
        write(root, ".gitignore", "__pycache__/\nbrands/acme/\n")
        self.assertEqual(codes(root), {"GDH_BRAND_PUBLIC"})

    def test_tracked_ignore_file_must_not_name_a_private_pack(self):
        root = self.fresh()
        write(root, ".gitignore", read(root, ".gitignore") + "brands/acme/\n")
        found = run("check", "--root", root, "--json")[1]
        self.assertIn("GDH_BRAND_PUBLIC", codes(root))
        self.assertIn("names the brand folder", found)
        root = self.fresh()
        write(root, "brands/.gitignore", "acme-client/\n")
        self.assertIn("GDH_BRAND_PUBLIC", codes(root))
        root = self.fresh()
        write(root, ".gitignore", read(root, ".gitignore") + "!brands/example-harbor-lantern/\nbrands/*.tmp\n")
        self.assertNotIn("GDH_BRAND_PUBLIC", codes(root))

    def test_ignore_reader(self):
        cases = [
            ("brands/acme/\n", "brands/acme", True),
            ("/brands/acme\n", "brands/acme", True),
            ("acme\n", "brands/acme", True),
            ("brands/*\n!brands/_template/\n", "brands/_template", False),
            ("brands/*\n!brands/_template/\n", "brands/acme", True),
            ("brands/\n!brands/acme/\n", "brands/acme", True),
            ("brands/**/secret\n", "brands/a/b/secret", True),
            ("brands/a?me/\n", "brands/acme", True),
            ("brands/[ab]cme/\n", "brands/acme", True),
            ("# brands/acme/\n", "brands/acme", False),
            ("brands/acme/\n", "brands/acme-two", False),
            ("brands/acme\n", "brands/acme", True),
        ]
        for text, rel, expected in cases:
            with self.subTest(text=text, rel=rel):
                root = self.folder()
                write(root, ".gitignore", text)
                self.assertEqual(gdh.is_ignored(gdh.ignore_rules(root), rel, True), expected)

    def test_network_import_forms(self):
        flagged = [
            "from urllib " + "import request\nrequest.urlopen('https://x.example')\n",
            "from urllib " + "import parse, request\n",
            "from http " + "import client\n",
            "import " + "ssl\n",
            "mod = __import__(" + "'socket')\n",
            "import importlib\nmod = importlib.import_module(" + "'urllib.request')\n",
            "const https = require(" + "'node:https');\n",
            "import got from " + "'http';\n",
        ]
        for sample in flagged:
            with self.subTest(sample=sample[:24]):
                root = self.fresh()
                write(root, "scripts/tool.py", sample)
                self.assertIn("GDH_SCRIPT_NETWORK", codes(root))
        root = self.fresh()
        write(root, "scripts/tool.py",
              "from urllib.parse import urlparse\nimport urllib.parse\nfrom html.parser import HTMLParser\n")
        self.assertNotIn("GDH_SCRIPT_NETWORK", codes(root))

    def test_hook_budget_counts_characters(self):
        root = self.fresh()
        # Few lines, so the line budget passes. Long lines, so the hook would cut the moments.
        write(root, "kit/canon/KERNEL.md", "# Kernel\n\n" + ("rule " * 900 + "\n") * 2)
        found = codes(root)
        self.assertNotIn("GDH_KERNEL_BUDGET", found)
        self.assertIn("GDH_HOOK_BUDGET", found)

    def test_text_output_prints_the_match(self):
        root, finding = self.leak()
        code, out = run("check", "--root", root)
        self.assertEqual(code, 1)
        self.assertIn("(match %s)" % finding["match"], out)

    def test_secret_shapes(self):
        samples = [
            "key = " + "sk-" + "a1B2c3D4e5F6g7H8i9J0k1L2",
            "id " + "0f8fad5b-" + "d9cb-469f-a165-" + "70867728950e",
            "AKIA" + "ABCDEFGHIJKLMNOP",
        ]
        for sample in samples:
            with self.subTest(sample=sample[:8]):
                root = self.fresh()
                write(root, "docs/note.txt", sample + "\n")
                self.assertIn("GDH_SECRET", codes(root))

    def test_secret_allowances(self):
        root = self.fresh()
        write(root, "tests/fixtures/sample.txt", "Write to " + ADDRESS + ".\n")
        write(root, "docs/note.md", "Run `/plugin install tool@vendor-market`. Clone git@github.com:o/r. Use logo@2x.png.\n")
        self.assertNotIn("GDH_SECRET", codes(root))

    def test_link_rules(self):
        root = self.fresh()
        write(root, "docs/links.md",
              "[web](https://example.com) [anchor](#top) `[code](nope.md)`\n\n```\n[fenced](nope.md)\n```\n")
        self.assertNotIn("GDH_LINK_BROKEN", codes(root))
        write(root, "docs/links.md", "[out](../../outside.md)\n")
        self.assertIn("GDH_LINK_BROKEN", codes(root))

    def test_eval_case_rules(self):
        rel = "evals/cases/triggering/trigger-ask-gdh.json"
        bad = [set_key("id", "other-name"), set_key("skill", "color"), set_key("skill", "no-such-skill"),
               set_key("expect", {}), set_key("expect", {"skills_fired": "ask-gdh"}),
               set_key("expect", {"skills_fired": ["color"]})]
        for change in bad:
            root = self.fresh()
            edit_json(root, rel, change)
            self.assertIn("GDH_EVAL_CASE", codes(root))
        root = self.fresh()
        write_json(root, "evals/cases/triggering/negative-backend-fix.json", {
            "id": "negative-backend-fix", "kind": "triggering", "skill": "none",
            "prompt": "Fix the failing date parser test.", "expect": {"skills_fired": []}})
        self.assertEqual(codes(root), set())
        edit_json(root, "evals/cases/triggering/negative-backend-fix.json",
                  set_key("expect", {"skills_fired": ["ask-gdh"]}))
        self.assertIn("GDH_EVAL_CASE", codes(root))

    def test_real_registry_is_valid(self):
        kit = gdh.load_kit(REPO)
        self.assertEqual(gdh.kit_problems(kit), [])
        self.assertEqual(len(kit["skills"]), 29)
        model = sorted(n for n, e in kit["skills"].items() if e["invocation"] == "model")
        self.assertEqual(model, ["align", "ask-gdh", "concept-forge", "design-brief", "design-critique", "find-assets", "mood-board", "originality-gate"])
        self.assertEqual(kit["moments"][0]["start"], ["align"])
        self.assertLessEqual(len(gdh.render_moments(kit)), kit["budgets"]["momentsChars"])
        for entry in kit["moments"]:
            self.assertLessEqual(len(entry["offer"]), 3)
            for name in entry["start"] + entry["offer"]:
                self.assertTrue(name in kit["skills"] or name in kit["wired"])
            for name in entry["start"]:
                self.assertEqual(kit["skills"][name]["invocation"], "model")


class BuildTests(FixtureCase):
    def test_build_is_deterministic(self):
        root = self.fresh()
        outputs = sorted(gdh.build_outputs(root, gdh.load_kit(root))[0])
        before = dict((rel, read(root, rel)) for rel in outputs)
        self.assertEqual(run("build", "--root", root)[0], 0)
        self.assertEqual(before, dict((rel, read(root, rel)) for rel in outputs))
        self.assertEqual(run("build", "--root", root, "--check")[0], 0)

    def test_build_outputs(self):
        root = self.fresh()
        market = read_json(root, ".claude-plugin/marketplace.json")
        self.assertEqual(market["name"], "synthminds-gdh")
        self.assertEqual(market["plugins"][0]["name"], "gdh")
        self.assertEqual(market["plugins"][0]["source"], "./kit")
        self.assertEqual(read_json(root, ".agents/plugins/marketplace.json")["plugins"][0]["source"],
                         {"source": "local", "path": "./kit"})
        self.assertEqual(read_json(root, "kit/.claude-plugin/plugin.json")["name"], "gdh")
        codex = read_json(root, "kit/.codex-plugin/plugin.json")
        self.assertEqual((codex["skills"], codex["hooks"]), ("./skills/", "./hooks/hooks.json"))
        moments = read(root, "kit/canon/MOMENTS.md")
        self.assertLess(moments.index("## Start"), moments.index("## Offer"))
        self.assertLess(moments.index("## Offer"), moments.index("## How to offer"))
        self.assertIn("Start `ask-gdh`", moments)
        self.assertIn("Offer `color`, `taste`", moments)
        self.assertIn("/plugin install taste", moments)
        for rel in ("README.md", "kit/README.md"):
            text = read(root, rel)
            self.assertIn("| `color` | user | color | Builds a palette. |", text)
            self.assertNotIn("\nold\n", text)
        self.assertTrue(read(root, "README.md").endswith("Tail.\n"))

    def test_build_check_reports_drift(self):
        root = self.fresh()
        edit_json(root, "kit/kit.json", set_key("version", "0.2.0"))
        code, out = run("build", "--root", root, "--check")
        self.assertEqual(code, 1)
        self.assertIn("kit/.claude-plugin/plugin.json", out)
        self.assertEqual(run("build", "--root", root)[0], 0)
        self.assertEqual(run("build", "--root", root, "--check")[0], 0)

    def test_readme_without_markers_is_left_alone(self):
        root = self.fresh()
        write(root, "README.md", "# Repo\n")
        self.assertEqual(run("build", "--root", root)[0], 0)
        self.assertEqual(read(root, "README.md"), "# Repo\n")


class ExportTests(FixtureCase):
    def snapshot(self, repo):
        out = {}
        for current, _, files in os.walk(repo):
            for name in files:
                path = os.path.join(current, name)
                with open(path, "rb") as handle:
                    out[os.path.relpath(path, repo)] = handle.read()
        return out

    def test_export_writes_and_is_idempotent(self):
        root, repo = self.fresh(), self.folder()
        code, out = run("export", "--root", root, "--repo", repo, "--hosts", "claude,codex")
        self.assertEqual(code, 0, out)
        for rel in (".claude/skills/color/SKILL.md", ".agents/skills/ask-gdh/references/routes.md",
                    ".claude/agents/critic.md", ".agents/catalogs/tools/alpha.json",
                    ".claude/canon/KERNEL.md", "DESIGN.md", "design/brief.md"):
            self.assertTrue(os.path.isfile(os.path.join(repo, rel)), rel)
        self.assertFalse(os.path.exists(os.path.join(repo, ".claude/skills/gdh-color")))
        agents = read(repo, "AGENTS.md")
        self.assertTrue(agents.startswith(gdh.BLOCK_START))
        self.assertIn(gdh.BLOCK_END, agents)
        self.assertIn("Precedence: the user ranks first.", agents)
        self.assertIn("GDH moments", agents)
        manifest = read_json(repo, ".agents/gdh/manifest.json")
        data = gdh.read_bytes(os.path.join(repo, ".claude/skills/color/SKILL.md"))
        self.assertEqual(manifest["files"][".claude/skills/color/SKILL.md"]["sha256"], gdh.sha256(data))
        self.assertIn("AGENTS.md", manifest["blocks"])
        before = self.snapshot(repo)
        code, out = run("export", "--root", root, "--repo", repo, "--hosts", "claude,codex")
        self.assertEqual(code, 0, out)
        self.assertIn("0 change(s)", out)
        self.assertEqual(before, self.snapshot(repo))

    def test_block_opens_with_the_entry_rule(self):
        root, repo = self.fresh(), self.folder()
        self.assertEqual(run("export", "--root", root, "--repo", repo)[0], 0)
        body = [line for line in read(repo, "AGENTS.md").split("\n")[2:] if line.strip()]
        self.assertTrue(body[0].startswith("Start every design-led session with `ask-gdh`"), body[0])
        self.assertNotIn("Start with `ask-gdh`", read(repo, "AGENTS.md"))

    def test_block_names_align_when_the_first_moment_starts_it(self):
        root, repo = self.fresh(), self.folder()
        write(root, "kit/skills/align/SKILL.md",
              "---\nname: align\ndescription: Opens a session with an interview.\n---\n\n# align\n")
        def add_align(data):
            data["skills"]["align"] = {"invocation": "model", "origin": "gdh", "discipline": "alignment"}
            data["moments"].insert(0, {"when": "A session starts", "start": ["align"], "offer": []})

        edit_json(root, "kit/kit.json", add_align)
        self.assertEqual(run("export", "--root", root, "--repo", repo)[0], 0)
        body = [line for line in read(repo, "AGENTS.md").split("\n")[2:] if line.strip()]
        self.assertTrue(body[0].startswith("Start every design-led session with `align`"), body[0])
        self.assertIn("`--full` forces the full interview.", body[0])

    def test_dry_run_writes_nothing(self):
        root, repo = self.fresh(), self.folder()
        code, out = run("export", "--root", root, "--repo", repo, "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("dry run", out)
        self.assertEqual(os.listdir(repo), [])

    def test_human_edit_is_a_conflict_until_replace_edited(self):
        root, repo = self.fresh(), self.folder()
        self.assertEqual(run("export", "--root", root, "--repo", repo)[0], 0)
        rel = ".claude/skills/color/SKILL.md"
        original = read(repo, rel)
        write(repo, rel, original + "\nA human note.\n")
        code, out = run("export", "--root", root, "--repo", repo)
        self.assertEqual(code, 1, out)
        self.assertIn("conflict", out)
        self.assertIn("--replace-edited", out)
        self.assertIn("A human note.", read(repo, rel))
        self.assertFalse(os.path.exists(os.path.join(repo, ".agents", "gdh", "backups")))
        # The file stays owned, so the flag can replace it on the next run.
        self.assertIn(rel, read_json(repo, ".agents/gdh/manifest.json")["files"])
        code, out = run("export", "--root", root, "--repo", repo, "--replace-edited")
        self.assertEqual(code, 0, out)
        self.assertEqual(read(repo, rel), original)
        backups = os.path.join(repo, ".agents", "gdh", "backups")
        stamps = os.listdir(backups)
        self.assertEqual(len(stamps), 1)
        self.assertIn("A human note.", read(backups, os.path.join(stamps[0], rel)))

    def hostile(self, key, outside_rel="other/a/b/v.txt"):
        """Export into a project whose manifest names key. Return (code, out, base, outside file)."""
        base = self.folder()
        root, repo = self.fresh(), os.path.join(base, "proj")
        outside = os.path.join(base, outside_rel)
        write(base, outside_rel, "v\n")
        digest = gdh.sha256(gdh.read_bytes(outside))
        write_json(repo, ".agents/gdh/manifest.json", {"files": {key(base): {"sha256": digest}}})
        code, out = run("export", "--root", root, "--repo", repo)
        return code, out, base, outside

    def test_manifest_key_with_parent_steps_is_refused(self):
        for key in ("../other/a/b/v.txt", ".claude/skills/../../../other/a/b/v.txt", ".claude\\..\\..\\x"):
            with self.subTest(key=key):
                code, out, _, outside = self.hostile(lambda base, key=key: key)
                self.assertEqual(code, 1, out)
                self.assertIn("refused", out)
                self.assertTrue(os.path.isfile(outside))

    def test_manifest_key_with_absolute_path_is_refused(self):
        code, out, base, outside = self.hostile(lambda base: os.path.join(base, "other", "a", "b", "v.txt"))
        self.assertEqual(code, 1, out)
        self.assertIn("refused", out)
        self.assertTrue(os.path.isfile(outside))
        self.assertTrue(os.path.isdir(os.path.join(base, "other", "a", "b")))

    def test_manifest_key_outside_managed_folders_is_refused(self):
        base = self.folder()
        root, repo = self.fresh(), os.path.join(base, "proj")
        write(repo, "src/app.py", "print(1)\n")
        digest = gdh.sha256(gdh.read_bytes(os.path.join(repo, "src/app.py")))
        write_json(repo, ".agents/gdh/manifest.json", {
            "files": {"src/app.py": {"sha256": digest}},
            "blocks": {"src/app.py": {"sha256": digest}},
            "templates": {"../escape.md": {"sha256": digest}}})
        code, out = run("export", "--root", root, "--repo", repo)
        self.assertEqual(code, 1, out)
        self.assertEqual(out.count("refused"), 3)
        self.assertTrue(os.path.isfile(os.path.join(repo, "src/app.py")))
        manifest = read_json(repo, ".agents/gdh/manifest.json")
        self.assertNotIn("src/app.py", manifest["files"])
        self.assertEqual(sorted(manifest["blocks"]), ["AGENTS.md", "CLAUDE.md"])
        self.assertNotIn("../escape.md", manifest["templates"])

    def test_removal_stays_inside_the_repo(self):
        base = self.folder()
        root, repo = self.fresh(), os.path.join(base, "proj")
        os.makedirs(repo)
        self.assertEqual(run("export", "--root", root, "--repo", repo)[0], 0)
        os.remove(os.path.join(root, "kit/skills/ask-gdh/references/routes.md"))
        write(root, "kit/skills/ask-gdh/SKILL.md", "---\nname: ask-gdh\ndescription: Routes.\n---\n\n`color`\n")
        self.assertEqual(run("export", "--root", root, "--repo", repo)[0], 0)
        self.assertFalse(os.path.exists(os.path.join(repo, ".claude/skills/ask-gdh/references")))
        self.assertTrue(os.path.isfile(os.path.join(repo, ".claude/skills/ask-gdh/SKILL.md")))
        self.assertTrue(os.path.isdir(repo))

    def test_claude_host_writes_a_claude_md_import(self):
        root, repo = self.fresh(), self.folder()
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--hosts", "claude")[0], 0)
        text = read(repo, "CLAUDE.md")
        self.assertTrue(text.startswith(gdh.BLOCK_START))
        self.assertIn("\n@AGENTS.md\n", text)
        self.assertIn("Precedence: the user ranks first.", read(repo, "AGENTS.md"))
        self.assertIn("CLAUDE.md", read_json(repo, ".agents/gdh/manifest.json")["blocks"])
        code, out = run("export", "--root", root, "--repo", repo, "--hosts", "claude")
        self.assertEqual(code, 0, out)
        self.assertIn("0 change(s)", out)

    def test_existing_claude_md_gets_the_import_and_keeps_its_text(self):
        root, repo = self.fresh(), self.folder()
        write(repo, "CLAUDE.md", "# Claude Code workflow\n\nUse Plan Mode first.\n")
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--hosts", "claude,codex")[0], 0)
        text = read(repo, "CLAUDE.md")
        self.assertTrue(text.startswith("# Claude Code workflow\n\nUse Plan Mode first.\n"))
        self.assertEqual(text.count("\n@AGENTS.md\n"), 1)
        self.assertEqual(text.count(gdh.BLOCK_START), 1)
        # A later export with Claude dropped takes the block out and leaves the human text.
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--hosts", "codex")[0], 0)
        self.assertEqual(read(repo, "CLAUDE.md"), "# Claude Code workflow\n\nUse Plan Mode first.\n")
        self.assertNotIn("CLAUDE.md", read_json(repo, ".agents/gdh/manifest.json")["blocks"])

    def test_claude_md_that_already_imports_is_kept(self):
        root, repo = self.fresh(), self.folder()
        write(repo, "CLAUDE.md", "# Rules\n\n@AGENTS.md\n")
        code, out = run("export", "--root", root, "--repo", repo, "--hosts", "claude")
        self.assertEqual(code, 0, out)
        self.assertEqual(read(repo, "CLAUDE.md"), "# Rules\n\n@AGENTS.md\n")
        self.assertNotIn("CLAUDE.md", read_json(repo, ".agents/gdh/manifest.json")["blocks"])

    def test_no_claude_md_without_the_claude_host(self):
        root, repo = self.fresh(), self.folder()
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--hosts", "codex,cursor")[0], 0)
        self.assertFalse(os.path.exists(os.path.join(repo, "CLAUDE.md")))

    def test_dropping_claude_removes_a_claude_md_that_holds_only_the_block(self):
        root, repo = self.fresh(), self.folder()
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--hosts", "claude,agents")[0], 0)
        self.assertTrue(os.path.isfile(os.path.join(repo, "CLAUDE.md")))
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--hosts", "agents")[0], 0)
        self.assertFalse(os.path.exists(os.path.join(repo, "CLAUDE.md")))

    def test_block_keeps_human_text_and_backs_up_block_edit(self):
        root, repo = self.fresh(), self.folder()
        write(repo, "AGENTS.md", "# Project rules\n\nKeep this line.\n")
        self.assertEqual(run("export", "--root", root, "--repo", repo)[0], 0)
        text = read(repo, "AGENTS.md")
        self.assertTrue(text.startswith("# Project rules\n\nKeep this line.\n"))
        write(repo, "AGENTS.md", text.replace("Precedence: the user ranks first.", "Edited by hand.") + "\nAfter.\n")
        self.assertEqual(run("export", "--root", root, "--repo", repo)[0], 0)
        text = read(repo, "AGENTS.md")
        self.assertIn("Precedence: the user ranks first.", text)
        self.assertNotIn("Edited by hand.", text)
        self.assertTrue(text.endswith("After.\n"))
        self.assertEqual(text.count(gdh.BLOCK_START), 1)
        stamps = os.listdir(os.path.join(repo, ".agents", "gdh", "backups"))
        self.assertIn("Edited by hand.", read(repo, os.path.join(".agents", "gdh", "backups", stamps[0], "AGENTS.md")))

    def test_template_never_overwrites(self):
        root, repo = self.fresh(), self.folder()
        write(repo, "DESIGN.md", "# Mine\n")
        self.assertEqual(run("export", "--root", root, "--repo", repo)[0], 0)
        self.assertEqual(read(repo, "DESIGN.md"), "# Mine\n")

    def test_paste_in_block_template_is_not_exported(self):
        root, repo = self.fresh(), self.folder()
        write(root, "kit/templates/project/AGENTS-block.md", "## Design work\n\nPaste this block.\n")
        self.assertEqual(run("export", "--root", root, "--repo", repo)[0], 0)
        self.assertFalse(os.path.exists(os.path.join(repo, "AGENTS-block.md")))
        self.assertTrue(os.path.exists(os.path.join(repo, "AGENTS.md")))

    def test_foreign_file_is_a_conflict(self):
        root, repo = self.fresh(), self.folder()
        write(repo, ".claude/skills/color/SKILL.md", "# Not ours\n")
        code, out = run("export", "--root", root, "--repo", repo)
        self.assertEqual(code, 1)
        self.assertIn("conflict", out)
        self.assertEqual(read(repo, ".claude/skills/color/SKILL.md"), "# Not ours\n")
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--force")[0], 0)
        self.assertIn("name: color", read(repo, ".claude/skills/color/SKILL.md"))

    def test_refuses_to_write_through_a_symlink(self):
        root, repo, outside = self.fresh(), self.folder(), self.folder()
        os.symlink(outside, os.path.join(repo, ".claude"))
        code, out = run("export", "--root", root, "--repo", repo)
        self.assertEqual(code, 1)
        self.assertIn("refused", out)
        self.assertEqual(os.listdir(outside), [])

    def test_dropped_host_is_reconciled(self):
        root, repo = self.fresh(), self.folder()
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--hosts", "claude,agents")[0], 0)
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--hosts", "agents")[0], 0)
        self.assertFalse(os.path.exists(os.path.join(repo, ".claude", "skills")))
        self.assertTrue(os.path.isfile(os.path.join(repo, ".agents/skills/color/SKILL.md")))

    def test_unknown_host(self):
        root, repo = self.fresh(), self.folder()
        self.assertEqual(run("export", "--root", root, "--repo", repo, "--hosts", "emacs")[0], 1)


class DoctorTests(FixtureCase):
    def doctor(self, root, today=TODAY):
        warnings, info = gdh.run_doctor(root, gdh.parse_today(today))
        return set(w["code"] for w in warnings), warnings, info

    def test_reports(self):
        root = self.fresh()
        found, warnings, info = self.doctor(root)
        self.assertEqual(found, {"GDH_DOCTOR_CAPABILITY_NO_TOOL"})
        self.assertIn("fonts", warnings[0]["message"])
        self.assertEqual(info["assetSourcesUnverified"], 0)
        self.assertIn("GDH_DOCTOR_STALE", self.doctor(root, "2027-01-01")[0])
        edit_json(root, "kit/catalogs/tools/alpha.json", set_key("evidence", "UNTESTED"))
        os.remove(os.path.join(root, "kit/references/tools/beta.md"))
        os.remove(os.path.join(root, "evals/cases/triggering/trigger-ask-gdh.json"))
        os.remove(os.path.join(root, "kit/skills/color/refinement-log.md"))
        edit_json(root, "kit/catalogs/assets.json", lambda d: d["sources"][0].update(verifiedOn=None))
        found, _, info = self.doctor(root)
        self.assertEqual(found, set(gdh.DOCTOR_CODES) - {"GDH_DOCTOR_STALE", "GDH_DOCTOR_GATE_UNVERIFIED"})
        self.assertEqual(info["assetSourcesUnverified"], 1)
        code, out = run("doctor", "--root", root, "--today", TODAY, "--json")
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["info"]["assetSourcesUnverified"], 1)

    def test_gate_capability_needs_a_verified_tool(self):
        root = self.fresh()
        alpha("capabilities", ["image-gen", "fonts"])(root)
        edit_json(root, "kit/catalogs/capabilities.json", lambda d: d["capabilities"].append("capture"))
        edit_json(root, "kit/catalogs/tools/beta.json", lambda d: d["capabilities"].append("capture"))
        self.assertEqual(self.doctor(root)[0], {"GDH_DOCTOR_GATE_UNVERIFIED"})
        edit_json(root, "kit/catalogs/tools/beta.json", set_key("evidence", "VERIFIED"))
        self.assertEqual(self.doctor(root)[0], set())

    def test_every_doctor_code_has_a_mutation(self):
        self.assertEqual(set(DOCTOR_MUTATIONS), set(gdh.DOCTOR_CODES))

    def test_each_doctor_mutation_reports_its_code(self):
        for code, (mutate, today, where) in sorted(DOCTOR_MUTATIONS.items()):
            with self.subTest(code=code):
                root = self.fresh()
                alpha("capabilities", ["image-gen", "fonts"])(root)
                self.assertEqual(self.doctor(root, today if code != "GDH_DOCTOR_STALE" else TODAY)[0], set())
                mutate(root)
                found, warnings, _ = self.doctor(root, today)
                self.assertEqual(found, {code})
                self.assertIn(where, [w["path"] for w in warnings])
                self.assertEqual(run("doctor", "--root", root, "--today", today)[0], 1)


DOCTOR_MUTATIONS = {
    "GDH_DOCTOR_STALE": (lambda r: None, "2027-01-01", "kit/catalogs/tools/alpha.json"),
    "GDH_DOCTOR_UNTESTED": (alpha("evidence", "UNTESTED"), TODAY, "kit/catalogs/tools/alpha.json"),
    "GDH_DOCTOR_NO_CARD": (lambda r: os.remove(os.path.join(r, "kit/references/tools/beta.md")), TODAY,
                           "kit/catalogs/tools/beta.json"),
    "GDH_DOCTOR_CAPABILITY_NO_TOOL": (
        lambda r: edit_json(r, "kit/catalogs/capabilities.json", lambda d: d["capabilities"].append("vector")),
        TODAY, "kit/catalogs/capabilities.json"),
    "GDH_DOCTOR_GATE_UNVERIFIED": (
        lambda r: (edit_json(r, "kit/catalogs/capabilities.json", lambda d: d["capabilities"].append("capture")),
                   edit_json(r, "kit/catalogs/tools/beta.json", lambda d: d["capabilities"].append("capture"))),
        TODAY, "kit/catalogs/capabilities.json"),
    "GDH_DOCTOR_NO_EVAL": (lambda r: os.remove(os.path.join(r, "evals/cases/triggering/trigger-ask-gdh.json")),
                           TODAY, "kit/skills/ask-gdh"),
    "GDH_DOCTOR_NO_REFINEMENT_LOG": (lambda r: os.remove(os.path.join(r, "kit/skills/color/refinement-log.md")),
                                     TODAY, "kit/skills/color"),
}


class ScaffoldTests(FixtureCase):
    def test_new_tool(self):
        root = self.fresh()
        args = ["new-tool", "gamma-maker", "--root", root, "--name", "Gamma Maker", "--kind", "connector",
                "--capabilities", "image-gen,fonts", "--source", "https://example.com/gamma", "--spends",
                "--today", TODAY]
        code, out = run(*args)
        self.assertEqual(code, 0, out)
        entry = read_json(root, "kit/catalogs/tools/gamma-maker.json")
        self.assertEqual(entry["evidence"], "DOCUMENTED")
        self.assertEqual(entry["verifiedAt"], TODAY)
        self.assertIs(entry["spendsCredits"], True)
        self.assertIs(entry["exposes"], False)
        self.assertEqual(entry["disciplines"], ["color"])
        card = read(root, "kit/references/tools/gamma-maker.md")
        positions = [card.index("## %s\n" % heading) for heading in gdh.CARD_HEADINGS]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(gdh.run_check(root)[0], [])
        self.assertEqual(run(*args)[0], 1)
        self.assertEqual(entry, read_json(root, "kit/catalogs/tools/gamma-maker.json"))

    def test_new_tool_refuses_bad_input(self):
        root = self.fresh()
        base = ["new-tool", "--root", root, "--name", "X", "--source", "https://example.com/x"]
        self.assertEqual(run(*(base + ["x-tool", "--kind", "connector", "--capabilities", "teleport"]))[0], 1)
        self.assertEqual(run(*(base + ["x-tool", "--kind", "saas", "--capabilities", "fonts"]))[0], 1)
        self.assertEqual(run(*(base + ["Bad_Id", "--kind", "cli", "--capabilities", "fonts"]))[0], 1)
        self.assertFalse(os.path.exists(os.path.join(root, "kit/catalogs/tools/x-tool.json")))

    def test_new_skill_user(self):
        root = self.fresh()
        args = ["new-skill", "poster", "--root", root, "--invocation", "user", "--discipline", "print",
                "--description", "Lays out a poster: use it for print work.", "--today", TODAY]
        code, out = run(*args)
        self.assertEqual(code, 0, out)
        self.assertEqual(read_json(root, "kit/kit.json")["skills"]["poster"],
                         {"invocation": "user", "origin": "gdh", "discipline": "print"})
        text = read(root, "kit/skills/poster/SKILL.md")
        front, body = gdh.parse_frontmatter(text)
        self.assertEqual(front["description"], "Lays out a poster: use it for print work.")
        self.assertEqual(front["disable-model-invocation"], "true")
        headings = ["## Before you start", "## Procedure", "## Tools", "## Checks", "## Output", "## References", "## Sources"]
        positions = [body.index(h) for h in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertTrue(os.path.isfile(os.path.join(root, "kit/skills/poster/refinement-log.md")))
        self.assertFalse(os.path.exists(os.path.join(root, "evals/cases/triggering/trigger-poster.json")))
        self.assertEqual(codes(root), {"GDH_ROUTER_INCOMPLETE"})
        write(root, "kit/skills/ask-gdh/SKILL.md", read(root, "kit/skills/ask-gdh/SKILL.md") + "\nRoute print to `poster`.\n")
        self.assertEqual(gdh.run_check(root)[0], [])
        self.assertEqual(run(*args)[0], 1)

    def test_new_skill_model_adds_eval_case(self):
        root = self.fresh()
        code, out = run("new-skill", "palette-check", "--root", root, "--invocation", "model", "--discipline",
                        "color", "--description", "Checks a palette.", "--today", TODAY)
        self.assertEqual(code, 0, out)
        case = read_json(root, "evals/cases/triggering/trigger-palette-check.json")
        self.assertEqual((case["kind"], case["skill"]), ("triggering", "palette-check"))
        self.assertNotIn("disable-model-invocation", read(root, "kit/skills/palette-check/SKILL.md"))
        self.assertEqual(codes(root), {"GDH_ROUTER_INCOMPLETE"})


class HookTests(FixtureCase):
    HOOK = os.path.join(REPO, "kit", "hooks", "session_start.py")

    def run_hook(self, plugin_root):
        hook = os.path.join(plugin_root, "hooks", "session_start.py")
        os.makedirs(os.path.dirname(hook), exist_ok=True)
        shutil.copy(self.HOOK, hook)
        return subprocess.run([sys.executable, "-I", "-S", hook], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True, timeout=30)

    def test_prints_kernel_then_moments(self):
        root = self.fresh()
        result = self.run_hook(os.path.join(root, "kit"))
        self.assertEqual(result.returncode, 0)
        self.assertLess(result.stdout.index("# Kernel"), result.stdout.index("# GDH moments"))

    def test_limit_and_missing_files(self):
        root = self.fresh()
        write(root, "kit/canon/KERNEL.md", "x" * 20000)
        result = self.run_hook(os.path.join(root, "kit"))
        self.assertEqual(result.returncode, 0)
        self.assertLessEqual(len(result.stdout), 9001)
        self.assertIn("this text was cut at 9000 characters", result.stdout.rstrip().split("\n")[-1])
        empty = self.folder()
        result = self.run_hook(empty)
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_full_text_has_no_cut_note(self):
        root = self.fresh()
        result = self.run_hook(os.path.join(root, "kit"))
        self.assertNotIn("this text was cut", result.stdout)
        self.assertTrue(result.stdout.rstrip().endswith(read(root, "kit/canon/MOMENTS.md").strip().split("\n")[-1]))

    def test_check_uses_the_hook_limit(self):
        spec = importlib.util.spec_from_file_location("gdh_session_start", self.HOOK)
        hook = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hook)
        self.assertEqual(hook.LIMIT, gdh.HOOK_LIMIT)

    def test_real_kit_fits_the_hook(self):
        kit = gdh.load_kit(REPO)
        kernel = read(REPO, "kit/canon/KERNEL.md").strip()
        self.assertLessEqual(len(kernel) + 2 + len(gdh.render_moments(kit).strip()), gdh.HOOK_LIMIT)

    def test_hooks_json_registers_the_hook(self):
        with open(os.path.join(REPO, "kit", "hooks", "hooks.json"), "r", encoding="utf-8") as handle:
            data = json.load(handle)
        command = data["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertEqual(command, 'python3 -I -S "${CLAUDE_PLUGIN_ROOT}/hooks/session_start.py"')


if __name__ == "__main__":
    unittest.main()
