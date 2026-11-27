"""Tests for kit/hooks/stop_gate.py, the Stop hook that asks for an originality verdict.

Each test runs the hook as a subprocess with crafted stdin JSON in a temporary project.
File times are set with os.utime, so no test waits.
Run: python3 -m unittest discover -s tests
"""
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(REPO, "kit", "hooks", "stop_gate.py")
HOUR = 60 * 60


def write(path, text, age=0):
    """Write a file and set its time to `age` seconds before now."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    stamp = time.time() - age
    os.utime(path, (stamp, stamp))


class StopGateHookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gdh-stop-gate-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.project = os.path.join(self.tmp, "project")
        os.makedirs(os.path.join(self.project, ".git"))
        os.makedirs(os.path.join(self.project, "design"))
        self.today = datetime.date.today().isoformat()

    def run_hook(self, payload=None, raw=None, cwd=None):
        if payload is None:
            payload = {"hook_event_name": "Stop", "stop_hook_active": False, "cwd": cwd or self.project}
        text = raw if raw is not None else json.dumps(payload)
        env = {key: value for key, value in os.environ.items() if not key.startswith("GDH_")}
        return subprocess.run([sys.executable, "-I", "-S", HOOK], input=text, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, universal_newlines=True, env=env, cwd=self.tmp, timeout=60)

    def assert_passes(self, result):
        self.assertEqual((result.returncode, result.stdout), (0, ""), result.stderr)

    def assert_blocks(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["decision"], "block")
        return data["reason"]

    def review(self, text="Originality: pass\n", age=0, name=None):
        write(os.path.join(self.project, "design", "reviews", name or ("%s-home.md" % self.today)), text, age)

    def test_blocks_when_design_file_is_newer_than_last_review(self):
        self.review(age=2 * HOUR)
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n", age=HOUR)
        reason = self.assert_blocks(self.run_hook())
        self.assertIn("src/index.html", reason)
        self.assertIn("design-critique", reason)
        self.assertIn("originality-gate", reason)
        self.assertIn("Originality:", reason)
        self.assertIn("Override: originality-gate %s" % self.today, reason)

    def test_passes_after_review_with_verdict(self):
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n", age=2 * HOUR)
        self.review(age=HOUR)
        self.assert_passes(self.run_hook())

    def test_review_without_verdict_line_does_not_count(self):
        write(os.path.join(self.project, "src", "a.css"), "a{}\n", age=2 * HOUR)
        self.review(text="# Critique\nNo verdict here.\n", age=HOUR)
        self.assertIn("no review", self.assert_blocks(self.run_hook()))

    def test_newest_verdict_review_is_used(self):
        self.review(age=5 * HOUR, name="old.md")
        write(os.path.join(self.project, "src", "a.css"), "a{}\n", age=3 * HOUR)
        self.review(text="  Originality: pass after round 2\n", age=HOUR, name="new.md")
        self.assert_passes(self.run_hook())

    def test_no_review_blocks_on_recent_design_file(self):
        write(os.path.join(self.project, "design", "directions", "1-calm", "board.html"), "<p>x</p>\n", age=HOUR)
        self.assertIn("design/directions/1-calm/board.html", self.assert_blocks(self.run_hook()))

    def test_no_review_passes_when_design_files_are_old(self):
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n", age=30 * HOUR)
        self.assert_passes(self.run_hook())

    def test_no_design_files_passes(self):
        write(os.path.join(self.project, "README.md"), "# x\n")
        self.assert_passes(self.run_hook())

    def test_no_design_folder_passes(self):
        os.rmdir(os.path.join(self.project, "design"))
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n")
        self.assert_passes(self.run_hook())

    def test_excluded_folders_do_not_count(self):
        for folder in ("node_modules/pkg", "dist", "build", ".git/x"):
            write(os.path.join(self.project, folder, "a.css"), "a{}\n")
        self.assert_passes(self.run_hook())

    def test_review_files_do_not_count_as_design_changes(self):
        self.review(age=HOUR)
        write(os.path.join(self.project, "design", "reviews", "capture.html"), "<p>x</p>\n")
        self.assert_passes(self.run_hook())

    def test_passes_with_todays_override(self):
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n")
        write(os.path.join(self.project, "design", "decisions.md"),
              "## log\nOverride: originality-gate %s owner accepts the launch page as is\n" % self.today)
        self.assert_passes(self.run_hook())

    def test_old_or_empty_override_does_not_pass(self):
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n")
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        write(os.path.join(self.project, "design", "decisions.md"),
              "Override: originality-gate %s old reason\nOverride: originality-gate %s\n" % (yesterday, self.today))
        self.assert_blocks(self.run_hook())

    def test_passes_when_stop_hook_active(self):
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n")
        self.assert_passes(self.run_hook({"hook_event_name": "Stop", "stop_hook_active": True,
                                          "cwd": self.project}))

    def test_design_folder_found_from_subfolder(self):
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n")
        self.assert_blocks(self.run_hook(cwd=os.path.join(self.project, "src")))

    def test_malformed_stdin_exits_zero(self):
        for raw in ("", "not json", "[]", "42", '{"cwd": 7}'):
            self.assert_passes(self.run_hook(raw=raw))

    def test_many_files_exit_zero(self):
        for number in range(2100):
            path = os.path.join(self.project, "aaa", "f%04d.txt" % number)
            if number == 0:
                os.makedirs(os.path.dirname(path))
            with open(path, "w") as handle:
                handle.write("x")
        write(os.path.join(self.project, "zzz.html"), "<p>x</p>\n")
        result = self.run_hook()
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
