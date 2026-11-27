#!/usr/bin/env python3
"""PostToolUse hook: scan one edited design file for tells and report them to the agent.

Claude Code runs this hook after a Write, Edit or MultiEdit call and passes the call as JSON on stdin.
The hook acts only when the edited file has a design extension and the project has a `design/` folder.
The project root is the first folder that holds `design/`, searched from `cwd` up to the git root.
Then it runs the tell scan of `design-critique` on that one file. On a markup file it also runs the
`originality-gate` check when that script exists. Findings come back as `hookSpecificOutput.additionalContext`, 12 lines at most.

The hook never blocks the edit. It fails open: any error, a timeout or a missing file means exit 0
with no output. Default: 8 seconds in total for both scans.
It writes nothing and calls no network. Child scripts run as `python3 -I -S`, so no module loads
from the project folder.

Environment:
  GDH_PLUGIN_ROOT    override of the plugin folder that holds `skills/`; default: the parent of this
                     script's folder. Tests point it at stub scripts.
  GDH_HOOK_TIMEOUT   the total time budget in seconds, for tests and local runs; default 8.
"""
import json
import os
import subprocess
import sys
import time

DESIGN_EXT = {".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".svg", ".vue", ".svelte"}
MARKUP_EXT = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}
# Every folder whose name starts with a dot is skipped as well.
SKIPPED_DIRS = {"node_modules", "dist", "build", "coverage", "htmlcov", "out", "storybook-static", "vendor",
                "target"}
EDIT_TOOLS = {"Write", "Edit", "MultiEdit"}
DEFAULT_BUDGET = 8.0
MAX_STDIN = 32 * 1024 * 1024
MAX_LINES = 12
MAX_DEPTH = 64
SEVERITY_RANK = {"high": 0, "medium": 1, "low": 2}
TELLS = os.path.join("skills", "design-critique", "scripts", "tells.py")
ORIGINALITY = os.path.join("skills", "originality-gate", "scripts", "originality.py")


def plugin_root():
    override = os.environ.get("GDH_PLUGIN_ROOT", "")
    if override:
        return os.path.abspath(override)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def budget():
    try:
        value = float(os.environ.get("GDH_HOOK_TIMEOUT", DEFAULT_BUDGET))
    except ValueError:
        return DEFAULT_BUDGET
    return value if 0 < value <= 60 else DEFAULT_BUDGET


def project_root(cwd):
    """Return the first folder from cwd up to the git root that holds design/, or None.

    Without a git root, only cwd itself counts, so the search never reaches an unrelated folder.
    """
    chain = []
    here = os.path.abspath(cwd)
    for _ in range(MAX_DEPTH):
        chain.append(here)
        if os.path.exists(os.path.join(here, ".git")):
            break
        parent = os.path.dirname(here)
        if parent == here:
            chain = chain[:1]
            break
        here = parent
    else:
        chain = chain[:1]
    for folder in chain:
        if os.path.isdir(os.path.join(folder, "design")):
            return folder
    return None


def run_json(command, cwd, deadline):
    """Run a child scan. Return its JSON object, or None on any failure or timeout."""
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return None
    try:
        result = subprocess.run(command, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, timeout=remaining, universal_newlines=True)
    except (OSError, subprocess.SubprocessError, ValueError):
        return None
    if result.returncode not in (0, 1):
        return None
    try:
        data = json.loads(result.stdout)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def findings_of(data, source):
    """Normalize the findings list of a scan into (rank, text) pairs."""
    out = []
    items = data.get("findings") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return out
    for item in items:
        if isinstance(item, str):
            out.append((1, "[%s] %s" % (source, item.strip()[:160])))
            continue
        if not isinstance(item, dict):
            continue
        severity = str(item.get("severity") or "medium").lower()
        code = str(item.get("code") or item.get("id") or source)
        message = str(item.get("message") or item.get("hint") or "").strip()
        line = item.get("line")
        where = " line %d" % line if isinstance(line, int) and not isinstance(line, bool) else ""
        text = "[%s] %s%s: %s" % (severity, code, where, message)
        out.append((SEVERITY_RANK.get(severity, 1), text[:200]))
    return out


def summary(rel, tells, originality):
    """Build the context text. originality is None when the originality check did not run."""
    head = "GDH scan of %s: %d tell finding(s)" % (rel, len(tells))
    if originality is not None:
        head += ", %d originality finding(s)" % len(originality)
    ranked = sorted(tells + (originality or []), key=lambda pair: pair[0])
    total = len(ranked)
    lines = [head + "."]
    room = MAX_LINES - 3
    for _, text in ranked[:room]:
        lines.append("- " + text)
    if total > room:
        lines.append("- and %d more; run the scan with --json for the full list." % (total - room))
    lines.append("Review each finding; fix it or record a brand-required reason in design/decisions.md.")
    return "\n".join(lines[:MAX_LINES])


def main():
    raw = sys.stdin.read(MAX_STDIN + 1)
    if not raw or len(raw) > MAX_STDIN:
        return 0
    try:
        data = json.loads(raw)
    except ValueError:
        return 0
    if not isinstance(data, dict):
        return 0
    tool = data.get("tool_name")
    if isinstance(tool, str) and tool and tool not in EDIT_TOOLS:
        return 0
    tool_input = data.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    path = tool_input.get("file_path")
    if not isinstance(path, str) or not path:
        return 0
    if os.path.splitext(path)[1].lower() not in DESIGN_EXT:
        return 0
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        cwd = os.getcwd()
    root = project_root(cwd)
    if root is None:
        return 0
    path = os.path.realpath(os.path.join(cwd, path))
    real_root = os.path.realpath(root)
    try:
        rel = os.path.relpath(path, real_root)
    except ValueError:
        return 0
    parts = rel.split(os.sep)
    if rel == ".." or rel.startswith(".." + os.sep) or \
            any(part.startswith(".") or part in SKIPPED_DIRS for part in parts[:-1]):
        return 0
    if not os.path.isfile(path):
        return 0

    deadline = time.monotonic() + budget()
    plugin = plugin_root()
    python = sys.executable or "python3"
    tells_script = os.path.join(plugin, TELLS)
    tells = []
    if os.path.isfile(tells_script):
        command = [python, "-I", "-S", tells_script, "--json"]
        tokens = os.path.join(real_root, "design", "tokens.json")
        design = os.path.join(real_root, "DESIGN.md")
        if os.path.isfile(tokens):
            command += ["--tokens", tokens]
        if os.path.isfile(design):
            command += ["--design", design]
        command.append(path)
        result = run_json(command, real_root, deadline)
        if result is not None:
            tells = findings_of(result, "tells")
    originality = None
    gate_script = os.path.join(plugin, ORIGINALITY)
    if os.path.splitext(path)[1].lower() in MARKUP_EXT and os.path.isfile(gate_script):
        result = run_json([python, "-I", "-S", gate_script, "check", path, "--json"], real_root, deadline)
        if result is not None:
            originality = findings_of(result, "originality")
    if not tells and not originality:
        return 0
    text = summary(rel.replace(os.sep, "/"), tells, originality)
    sys.stdout.write(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                        "additionalContext": text}}) + "\n")
    return 0


if __name__ == "__main__":
    try:
        main()
    except BaseException:  # the hook must never fail or block an edit
        pass
    sys.exit(0)
