#!/usr/bin/env python3
"""Stop hook: hold the stop until changed design work has an originality verdict.

Claude Code runs this hook when the agent finishes its turn and passes the event as JSON on stdin.
The hook acts only when the project has a `design/` folder. The project root is the first folder
that holds `design/`, searched from `cwd` up to the git root.

It blocks the stop with `decision: "block"` when a design file changed after the newest file in
`design/reviews/` that holds a line starting with `Originality:`. With no such review, it blocks when
a design file changed in the last 24 hours. The reason tells the agent to run the critique and the
originality gate and write the verdict, or to record an override.

The stop passes when:
  - `stop_hook_active` is true, so the hook never loops;
  - `design/decisions.md` holds a line `Override: originality-gate <YYYY-MM-DD> <reason>` dated today;
  - any error or timeout occurs (the hook fails open).

Default: the hook looks at 2,000 files at most and spends 8 seconds at most.
It writes nothing and calls no network.

Environment, for tests and local runs only:
  GDH_HOOK_TIMEOUT   the total time budget in seconds; default 8.
"""
import datetime
import json
import os
import re
import sys
import time

DESIGN_EXT = {".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".svg", ".vue", ".svelte"}
EXCLUDED_DIRS = {"node_modules", ".git", "dist", "build"}
DEFAULT_BUDGET = 8.0
MAX_FILES = 2000
MAX_STDIN = 4 * 1024 * 1024
MAX_READ = 1024 * 1024
MAX_DEPTH = 64
RECENT_SECONDS = 24 * 60 * 60
SHOW = 5
OVERRIDE = re.compile(r"^\s*Override:\s*originality-gate\s+(\d{4}-\d{2}-\d{2})\s+\S")


class OutOfTime(Exception):
    pass


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


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read(MAX_READ)


def has_override(root, today):
    path = os.path.join(root, "design", "decisions.md")
    if not os.path.isfile(path):
        return False
    for line in read_text(path).splitlines():
        match = OVERRIDE.match(line)
        if match and match.group(1) == today:
            return True
    return False


def walk(top, deadline, counter):
    """Yield (path, mtime) for regular files under top. Skips excluded folders and symbolic links."""
    stack = [top]
    while stack:
        folder = stack.pop()
        try:
            entries = list(os.scandir(folder))
        except OSError:
            continue
        for entry in entries:
            if time.monotonic() > deadline:
                raise OutOfTime()
            try:
                if entry.is_symlink():
                    continue
                if entry.is_dir():
                    if entry.name not in EXCLUDED_DIRS:
                        stack.append(entry.path)
                    continue
                if not entry.is_file():
                    continue
                counter[0] += 1
                if counter[0] > MAX_FILES:
                    return
                yield entry.path, entry.stat().st_mtime
            except OSError:
                continue


def last_verdict(root, deadline, counter):
    """Return the mtime of the newest review file with an `Originality:` line, or None."""
    reviews = os.path.join(root, "design", "reviews")
    if not os.path.isdir(reviews):
        return None
    newest = None
    for path, mtime in walk(reviews, deadline, counter):
        if newest is not None and mtime <= newest:
            continue
        try:
            text = read_text(path)
        except (OSError, ValueError):
            continue
        if any(line.lstrip().startswith("Originality:") for line in text.splitlines()):
            newest = mtime
    return newest


def changed_files(root, since, deadline, counter):
    """Return the design files changed after since, newest first. Review files do not count."""
    reviews = os.path.join(root, "design", "reviews") + os.sep
    out = []
    for path, mtime in walk(root, deadline, counter):
        if path.startswith(reviews):
            continue
        if os.path.splitext(path)[1].lower() in DESIGN_EXT and mtime > since:
            out.append((mtime, os.path.relpath(path, root).replace(os.sep, "/")))
    out.sort(reverse=True)
    return [rel for _, rel in out]


def reason(changed, verdict, today):
    shown = ", ".join(changed[:SHOW])
    if len(changed) > SHOW:
        shown += " and %d more" % (len(changed) - SHOW)
    if verdict is None:
        lead = "GDH originality gate: %d design file(s) changed in the last 24 hours and no review in " \
               "design/reviews/ holds an originality verdict (%s)." % (len(changed), shown)
    else:
        lead = "GDH originality gate: %d design file(s) changed after the last originality verdict " \
               "(%s)." % (len(changed), shown)
    return " ".join([
        lead,
        "Before you stop, run the design-critique skill on the changed work.",
        "Then follow the originality-gate skill: read its SKILL.md in the GDH plugin, or ask the user to run "
        "/gdh:originality-gate.",
        "Write the result to design/reviews/%s-<scope>.md with a line that starts with 'Originality:'." % today,
        "If the user accepts the work without the gate, add this line to design/decisions.md: "
        "Override: originality-gate %s <reason>." % today,
    ])


def main():
    raw = sys.stdin.read(MAX_STDIN + 1)
    if not raw or len(raw) > MAX_STDIN:
        return 0
    try:
        data = json.loads(raw)
    except ValueError:
        return 0
    if not isinstance(data, dict) or data.get("stop_hook_active"):
        return 0
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        cwd = os.getcwd()
    root = project_root(cwd)
    if root is None:
        return 0
    root = os.path.realpath(root)
    today = datetime.date.today().isoformat()
    if has_override(root, today):
        return 0
    deadline = time.monotonic() + budget()
    counter = [0]
    try:
        verdict = last_verdict(root, deadline, counter)
        since = verdict if verdict is not None else time.time() - RECENT_SECONDS
        changed = changed_files(root, since, deadline, counter)
    except OutOfTime:
        return 0
    if not changed:
        return 0
    sys.stdout.write(json.dumps({"decision": "block", "reason": reason(changed, verdict, today)}) + "\n")
    return 0


if __name__ == "__main__":
    try:
        main()
    except BaseException:  # the hook must never fail a session
        pass
    sys.exit(0)
