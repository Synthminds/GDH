"""Tests for kit/hooks/post_edit.py, the PostToolUse tell scan.

Each test runs the hook as a subprocess with crafted stdin JSON in a temporary project.
A stub plugin root, set through GDH_PLUGIN_ROOT, stands in for the scan scripts where needed.
Run: python3 -m unittest discover -s tests
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(REPO, "kit", "hooks", "post_edit.py")

STUB_TELLS = r'''
import json, os, sys, time
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "argv.json"), "w") as handle:
    json.dump(sys.argv[1:], handle)
mode = os.environ.get("STUB_MODE", "findings")
if mode == "sleep":
    time.sleep(30)
if mode == "crash":
    sys.exit(2)
count = int(os.environ.get("STUB_COUNT", "2"))
findings = [{"code": "TELL_STUB_%d" % n, "severity": "low" if n else "high", "line": n + 1,
             "message": "stub finding %d" % n} for n in range(count)]
print(json.dumps({"findings": findings}))
sys.exit(1 if findings else 0)
'''

STUB_ORIGINALITY = r'''
import json, sys
assert sys.argv[1] == "check" and "--json" in sys.argv
print(json.dumps({"findings": [{"code": "ORIG_STUB", "severity": "medium", "message": "close to a template"}]}))
sys.exit(1)
'''


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


class PostEditHookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gdh-post-edit-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.project = os.path.join(self.tmp, "project")
        os.makedirs(os.path.join(self.project, ".git"))
        os.makedirs(os.path.join(self.project, "design"))
        self.page = os.path.join(self.project, "src", "index.html")
        write(self.page, "<h1>Hello</h1>\n")
        self.plugin = os.path.join(self.tmp, "plugin")
        write(os.path.join(self.plugin, "skills", "design-critique", "scripts", "tells.py"), STUB_TELLS)

    def run_hook(self, payload, env_extra=None, plugin=True, raw=None):
        env = {key: value for key, value in os.environ.items() if not key.startswith(("GDH_", "STUB_"))}
        if plugin:
            env["GDH_PLUGIN_ROOT"] = self.plugin
        env.update(env_extra or {})
        text = raw if raw is not None else json.dumps(payload)
        return subprocess.run([sys.executable, "-I", "-S", HOOK], input=text, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, universal_newlines=True, env=env, timeout=60)

    def payload(self, path=None, tool="Write", cwd=None):
        return {"hook_event_name": "PostToolUse", "tool_name": tool, "cwd": cwd or self.project,
                "tool_input": {"file_path": path or self.page, "content": "x"},
                "tool_response": {"filePath": path or self.page}}

    def context(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertNotIn("decision", data)
        return data["hookSpecificOutput"]["additionalContext"]

    def assert_silent(self, result):
        self.assertEqual((result.returncode, result.stdout), (0, ""), result.stderr)

    def stub_argv(self):
        with open(os.path.join(self.plugin, "skills", "design-critique", "scripts", "argv.json")) as handle:
            return json.load(handle)

    def test_findings_produce_additional_context(self):
        text = self.context(self.run_hook(self.payload()))
        self.assertIn("src/index.html", text)
        self.assertIn("TELL_STUB_0", text)
        self.assertLess(text.index("TELL_STUB_0"), text.index("TELL_STUB_1"))
        self.assertIn("Review each finding; fix it or record a brand-required reason", text)
        self.assertLessEqual(len(text.splitlines()), 12)

    def test_edit_and_multiedit_also_scan(self):
        for tool in ("Edit", "MultiEdit"):
            self.assertIn("TELL_STUB_0", self.context(self.run_hook(self.payload(tool=tool))))

    def test_other_tool_is_ignored(self):
        self.assert_silent(self.run_hook(self.payload(tool="Read")))

    def test_non_design_file_is_ignored(self):
        notes = os.path.join(self.project, "notes.md")
        write(notes, "# notes\n")
        self.assert_silent(self.run_hook(self.payload(path=notes)))
        self.assertFalse(os.path.exists(os.path.join(self.plugin, "skills", "design-critique", "scripts",
                                                     "argv.json")))

    def test_no_design_folder_is_ignored(self):
        os.rmdir(os.path.join(self.project, "design"))
        self.assert_silent(self.run_hook(self.payload()))

    def test_design_folder_found_from_a_subfolder_up_to_git_root(self):
        text = self.context(self.run_hook(self.payload(cwd=os.path.join(self.project, "src"))))
        self.assertIn("TELL_STUB_0", text)

    def test_search_stops_at_git_root(self):
        inner = os.path.join(self.project, "inner")
        os.makedirs(os.path.join(inner, ".git"))
        page = os.path.join(inner, "a.css")
        write(page, "a{}\n")
        self.assert_silent(self.run_hook(self.payload(path=page, cwd=inner)))

    def test_file_outside_project_or_in_excluded_folder_is_ignored(self):
        outside = os.path.join(self.tmp, "elsewhere.html")
        write(outside, "<p>x</p>\n")
        self.assert_silent(self.run_hook(self.payload(path=outside)))
        vendored = os.path.join(self.project, "node_modules", "pkg", "a.css")
        write(vendored, "a{}\n")
        self.assert_silent(self.run_hook(self.payload(path=vendored)))

    def test_dot_and_tool_folders_are_ignored(self):
        for folder in (".storybook", "coverage", "vendor/lib", "storybook-static"):
            page = os.path.join(self.project, folder, "a.html")
            write(page, "<p>x</p>\n")
            self.assert_silent(self.run_hook(self.payload(path=page)))

    def test_dot_dot_prefix_inside_project_is_scanned(self):
        page = os.path.join(self.project, "..page.html")
        write(page, "<p>x</p>\n")
        self.assertIn("TELL_STUB_0", self.context(self.run_hook(self.payload(path=page))))

    def test_relative_path_resolves_against_cwd(self):
        self.assertIn("TELL_STUB_0", self.context(self.run_hook(self.payload(path="src/index.html"))))

    def test_tokens_and_design_passed_only_when_present(self):
        self.context(self.run_hook(self.payload()))
        argv = self.stub_argv()
        self.assertNotIn("--tokens", argv)
        self.assertNotIn("--design", argv)
        self.assertIn("--json", argv)
        self.assertEqual(argv[-1], os.path.realpath(self.page))
        write(os.path.join(self.project, "design", "tokens.json"), "{}\n")
        write(os.path.join(self.project, "DESIGN.md"), "# Design\n")
        self.context(self.run_hook(self.payload()))
        argv = self.stub_argv()
        self.assertEqual(argv[argv.index("--tokens") + 1],
                         os.path.join(os.path.realpath(self.project), "design", "tokens.json"))
        self.assertEqual(argv[argv.index("--design") + 1], os.path.join(os.path.realpath(self.project), "DESIGN.md"))

    def test_clean_scan_prints_nothing(self):
        self.assert_silent(self.run_hook(self.payload(), {"STUB_COUNT": "0"}))

    def test_originality_findings_are_included(self):
        write(os.path.join(self.plugin, "skills", "originality-gate", "scripts", "originality.py"), STUB_ORIGINALITY)
        text = self.context(self.run_hook(self.payload(), {"STUB_COUNT": "0"}))
        self.assertIn("ORIG_STUB", text)
        self.assertIn("1 originality finding(s)", text)

    def test_originality_runs_on_markup_only(self):
        write(os.path.join(self.plugin, "skills", "originality-gate", "scripts", "originality.py"), STUB_ORIGINALITY)
        for name in ("a.css", "a.scss", "a.svg"):
            sheet = os.path.join(self.project, "src", name)
            write(sheet, "a{}\n")
            text = self.context(self.run_hook(self.payload(path=sheet)))
            self.assertNotIn("ORIG_STUB", text)
            self.assertNotIn("originality finding", text)
        component = os.path.join(self.project, "src", "Card.tsx")
        write(component, "export const Card = () => null;\n")
        self.assertIn("ORIG_STUB", self.context(self.run_hook(self.payload(path=component))))

    def test_absent_originality_script_is_tolerated(self):
        text = self.context(self.run_hook(self.payload()))
        self.assertNotIn("originality finding", text)

    def test_summary_is_at_most_twelve_lines(self):
        text = self.context(self.run_hook(self.payload(), {"STUB_COUNT": "40"}))
        lines = text.splitlines()
        self.assertEqual(len(lines), 12)
        self.assertIn("and 31 more", text)

    def test_timeout_fails_open(self):
        start = time.monotonic()
        result = self.run_hook(self.payload(), {"STUB_MODE": "sleep", "GDH_HOOK_TIMEOUT": "1"})
        self.assert_silent(result)
        self.assertLess(time.monotonic() - start, 15)

    def test_scan_error_fails_open(self):
        self.assert_silent(self.run_hook(self.payload(), {"STUB_MODE": "crash"}))

    def test_missing_scan_script_fails_open(self):
        shutil.rmtree(self.plugin)
        self.assert_silent(self.run_hook(self.payload()))

    def test_malformed_stdin_exits_zero(self):
        for raw in ("", "not json", "[1, 2]", '{"tool_input": "x"}', '{"tool_input": {"file_path": 3}}'):
            self.assert_silent(self.run_hook(None, raw=raw))

    def test_missing_edited_file_fails_open(self):
        self.assert_silent(self.run_hook(self.payload(path=os.path.join(self.project, "gone.html"))))

    def test_real_tell_scan(self):
        write(self.page, '<div class="bg-gradient-to-r from-purple-500 to-indigo-600"><h1>Hi</h1></div>\n')
        text = self.context(self.run_hook(self.payload(), plugin=False))
        self.assertIn("TELL_PURPLE_GRADIENT", text)


class HooksJsonTests(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(REPO, "kit", "hooks", "hooks.json"), "r", encoding="utf-8") as handle:
            self.hooks = json.load(handle)["hooks"]

    def test_registers_three_hooks(self):
        self.assertEqual(set(self.hooks), {"SessionStart", "PostToolUse", "Stop"})
        self.assertEqual(self.hooks["SessionStart"][0]["hooks"][0]["command"],
                         'python3 -I -S "${CLAUDE_PLUGIN_ROOT}/hooks/session_start.py"')
        post = self.hooks["PostToolUse"][0]
        self.assertEqual(post["matcher"], "Write|Edit|MultiEdit")
        self.assertEqual(post["hooks"][0]["command"],
                         'python3 -I -S "${CLAUDE_PLUGIN_ROOT}/hooks/post_edit.py" || true')
        stop = self.hooks["Stop"][0]["hooks"][0]
        self.assertEqual(stop["command"], 'python3 -I -S "${CLAUDE_PLUGIN_ROOT}/hooks/stop_gate.py" || true')

    def run_command(self, event, plugin_root, stdin, guard=True):
        env = {key: value for key, value in os.environ.items() if key != "CLAUDE_PLUGIN_ROOT"}
        if plugin_root is not None:
            env["CLAUDE_PLUGIN_ROOT"] = plugin_root
        command = self.hooks[event][0]["hooks"][0]["command"]
        if not guard:
            command = command[:-len(" || true")]
        return subprocess.run(["/bin/sh", "-c", command], input=stdin, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, universal_newlines=True, env=env, timeout=60)

    @unittest.skipUnless(os.path.exists("/bin/sh"), "needs a POSIX shell")
    def test_launch_failure_exits_zero(self):
        stdin = json.dumps({"hook_event_name": "Stop", "stop_hook_active": False, "cwd": REPO})
        with tempfile.TemporaryDirectory() as empty:
            for event in ("PostToolUse", "Stop"):
                for root in (None, "", empty, os.path.join(empty, "missing")):
                    result = self.run_command(event, root, stdin)
                    self.assertEqual((result.returncode, result.stdout), (0, ""), (event, root))
                    # Without the guard, python exits 2, which a Stop hook reads as a block.
                    self.assertNotEqual(self.run_command(event, root, stdin, guard=False).returncode, 0)

    @unittest.skipUnless(os.path.exists("/bin/sh"), "needs a POSIX shell")
    def test_command_runs_the_real_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, ".git"))
            os.makedirs(os.path.join(tmp, "design"))
            page = os.path.join(tmp, "a.html")
            write(page, '<div class="bg-gradient-to-r from-purple-500 to-indigo-600"></div>\n')
            stdin = json.dumps({"tool_name": "Write", "cwd": tmp, "tool_input": {"file_path": page}})
            result = self.run_command("PostToolUse", os.path.join(REPO, "kit"), stdin)
            self.assertEqual(result.returncode, 0)
            self.assertIn("TELL_PURPLE_GRADIENT", result.stdout)

    def test_timeouts_cover_the_internal_budget(self):
        for event in ("PostToolUse", "Stop"):
            entry = self.hooks[event][0]["hooks"][0]
            self.assertEqual(entry["type"], "command")
            self.assertGreater(entry["timeout"], 8)

    def test_scripts_exist(self):
        for name in ("session_start.py", "post_edit.py", "stop_gate.py"):
            self.assertTrue(os.path.isfile(os.path.join(REPO, "kit", "hooks", name)), name)


if __name__ == "__main__":
    unittest.main()
