"""Tests for kit/hooks/stop_gate.py, the Stop hook that asks for an originality verdict.

Each test runs the hook as a subprocess with crafted stdin JSON and a crafted session transcript
in a temporary project. File times are set with os.utime, so no test waits.
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
GATE_SKILL = os.path.join(REPO, "kit", "skills", "originality-gate", "SKILL.md")
HOUR = 60 * 60


def write(path, text, age=0):
    """Write a file and set its time to `age` seconds before now. A negative age is in the future."""
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
        self.transcript = os.path.join(self.tmp, "session.jsonl")
        self.uses = []
        self.today = datetime.date.today().isoformat()

    def edit(self, rel, age=0, tool="Write", text="<p>x</p>\n"):
        """Write a project file and log a matching tool_use in the session transcript."""
        path = os.path.join(self.project, rel)
        write(path, text, age)
        self.uses.append((tool, path))
        return path

    def save_transcript(self):
        lines = [json.dumps({"type": "user", "message": {"role": "user", "content": "make the page"}})]
        for number, (tool, path) in enumerate(self.uses):
            lines.append(json.dumps({"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "text", "text": "editing"},
                {"type": "tool_use", "id": "toolu_%d" % number, "name": tool, "input": {"file_path": path}}]}}))
        lines.append("{broken json line with \"tool_use\"")
        with open(self.transcript, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")

    def run_hook(self, payload=None, raw=None, cwd=None, transcript=True):
        if payload is None:
            payload = {"hook_event_name": "Stop", "stop_hook_active": False, "cwd": cwd or self.project}
            if transcript:
                self.save_transcript()
                payload["transcript_path"] = self.transcript
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

    def review(self, text="Originality: original\n", age=0, name="review.md"):
        write(os.path.join(self.project, "design", "reviews", name), text, age)

    def test_blocks_when_session_edit_is_newer_than_last_review(self):
        self.review(age=2 * HOUR)
        self.edit("src/index.html", age=HOUR)
        reason = self.assert_blocks(self.run_hook())
        self.assertIn("src/index.html", reason)
        self.assertIn("design-critique", reason)
        self.assertIn("Start the originality-gate skill", reason)
        self.assertIn(GATE_SKILL, reason)
        self.assertIn("design/reviews/%s-originality.md" % self.today, reason)
        self.assertIn("If this turn hands over a draft for feedback rather than finished work, say so in one line "
                      "and stop.", reason)
        self.assertIn("Before you call the design done, run the gate.", reason)
        self.assertIn("Override: originality-gate %s" % self.today, reason)

    def test_edit_and_multiedit_count(self):
        self.edit("src/a.css", tool="Edit", text="a{}\n")
        self.edit("src/b.svg", tool="MultiEdit", text="<svg/>\n")
        reason = self.assert_blocks(self.run_hook())
        self.assertIn("src/a.css", reason)
        self.assertIn("src/b.svg", reason)

    def test_passes_after_original_or_watch_verdict(self):
        for verdict in ("Originality: original\n", "## Result\n  originality: Watch (hero is close)\n"):
            self.uses = []
            self.edit("src/index.html", age=2 * HOUR)
            self.review(text=verdict, age=HOUR)
            self.assert_passes(self.run_hook())

    def test_derivative_verdict_does_not_pass(self):
        self.edit("src/index.html", age=2 * HOUR)
        self.review(text="Originality: derivative\n", age=HOUR)
        self.assertIn("no review", self.assert_blocks(self.run_hook()))

    def test_review_without_verdict_line_does_not_count(self):
        self.edit("src/a.css", age=2 * HOUR, text="a{}\n")
        self.review(text="# Critique\nNo verdict here.\n", age=HOUR)
        self.assertIn("no review", self.assert_blocks(self.run_hook()))

    def test_newest_passing_review_is_used(self):
        self.review(age=5 * HOUR, name="old.md")
        self.edit("src/a.css", age=3 * HOUR, text="a{}\n")
        self.review(text="Originality: watch\n", age=HOUR, name="new.md")
        self.assert_passes(self.run_hook())

    def test_subagent_edits_count(self):
        path = os.path.join(self.project, "src", "index.html")
        write(path, "<p>x</p>\n")
        self.save_transcript()
        log = os.path.join(self.tmp, "session", "subagents", "agent-1.jsonl")
        write(log, json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Edit", "input": {"file_path": path}}]}}) + "\n")
        payload = {"stop_hook_active": False, "cwd": self.project, "transcript_path": self.transcript}
        self.assertIn("src/index.html", self.assert_blocks(self.run_hook(payload)))

    def test_session_without_design_edits_passes(self):
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n")
        self.uses.append(("Read", os.path.join(self.project, "src", "index.html")))
        self.edit("notes.md", text="# notes\n")
        self.assert_passes(self.run_hook())

    def test_session_edits_outside_project_or_in_skipped_folders_pass(self):
        outside = os.path.join(self.tmp, "elsewhere.html")
        write(outside, "<p>x</p>\n")
        self.uses.append(("Write", outside))
        for folder in (".next", ".storybook", "node_modules/pkg", "dist", "build", "coverage", "htmlcov", "out",
                       "storybook-static", "vendor", "target", "design/reviews"):
            self.edit(folder + "/a.html")
        self.assert_passes(self.run_hook())

    def test_old_session_edit_without_review_passes(self):
        self.edit("src/index.html", age=30 * HOUR)
        self.assert_passes(self.run_hook())

    def test_future_file_time_is_ignored(self):
        self.edit("src/index.html", age=-HOUR)
        self.assert_passes(self.run_hook())

    def test_future_review_time_is_ignored(self):
        self.edit("src/index.html", age=HOUR)
        self.review(age=-HOUR)
        self.assertIn("no review", self.assert_blocks(self.run_hook()))

    def test_unreadable_transcript_without_brief_passes(self):
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n")
        self.assert_passes(self.run_hook(transcript=False))
        payload = {"stop_hook_active": False, "cwd": self.project,
                   "transcript_path": os.path.join(self.tmp, "missing.jsonl")}
        self.assert_passes(self.run_hook(payload))

    def test_unreadable_transcript_with_brief_walks_the_project(self):
        write(os.path.join(self.project, "design", "brief.md"), "# Brief\n")
        for folder in (".next", "coverage", "vendor", "node_modules"):
            write(os.path.join(self.project, folder, "a.css"), "a{}\n")
        self.assert_passes(self.run_hook(transcript=False))
        write(os.path.join(self.project, "src", "index.html"), "<p>x</p>\n", age=HOUR)
        self.assertIn("src/index.html", self.assert_blocks(self.run_hook(transcript=False)))
        self.review()
        self.assert_passes(self.run_hook(transcript=False))

    def test_passes_with_todays_override(self):
        self.edit("src/index.html")
        write(os.path.join(self.project, "design", "decisions.md"),
              "## log\nOverride: originality-gate %s owner accepts the launch page as is\n" % self.today)
        self.assert_passes(self.run_hook())

    def test_old_or_empty_override_does_not_pass(self):
        self.edit("src/index.html")
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        write(os.path.join(self.project, "design", "decisions.md"),
              "Override: originality-gate %s old reason\nOverride: originality-gate %s\n" % (yesterday, self.today))
        self.assert_blocks(self.run_hook())

    def test_passes_when_stop_hook_active(self):
        self.edit("src/index.html")
        self.save_transcript()
        self.assert_passes(self.run_hook({"hook_event_name": "Stop", "stop_hook_active": True,
                                          "cwd": self.project, "transcript_path": self.transcript}))

    def test_design_folder_found_from_subfolder(self):
        self.edit("src/index.html")
        self.assert_blocks(self.run_hook(cwd=os.path.join(self.project, "src")))

    def test_no_design_folder_passes(self):
        os.rmdir(os.path.join(self.project, "design"))
        self.edit("src/index.html")
        self.assert_passes(self.run_hook())

    def test_echoed_names_are_capped_cleaned_and_truncated(self):
        self.edit("src/bad\x1b[31mname.html")
        self.edit("src/" + "n" * 200 + ".html")
        for number in range(5):
            self.edit("src/page%d.html" % number, age=60)
        reason = self.assert_blocks(self.run_hook())
        self.assertIn("and 2 more", reason)
        self.assertNotIn("\x1b", reason)
        self.assertIn("src/bad[31mname.html", reason)
        self.assertTrue(all(char.isprintable() for char in reason))
        self.assertIn("src/" + "n" * 113 + "...", reason)
        self.assertNotIn("n" * 114, reason)

    def test_malformed_stdin_exits_zero(self):
        for raw in ("", "not json", "[]", "42", '{"cwd": 7}', '{"cwd": "%s", "transcript_path": 5}' % self.project):
            self.assert_passes(self.run_hook(raw=raw))


if __name__ == "__main__":
    unittest.main()
