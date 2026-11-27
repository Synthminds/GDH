#!/usr/bin/env python3
"""Stop hook: hold the stop once when this session changed design work without an originality verdict.

Claude Code runs this hook when the agent finishes its turn and passes the event as JSON on stdin.
The hook acts only when the project has a `design/` folder. The project root is the first folder
that holds `design/`, searched from `cwd` up to the git root. Without a git root, only `cwd` counts.

Which files count:
  - The hook reads the session transcript (`transcript_path`, JSONL), and the transcripts of its
    subagents beside it, and collects the files that Write, Edit and MultiEdit calls touched. A file counts when it has a design
    extension, lies inside the project, and is not in a skipped folder or in `design/reviews/`.
  - When the transcript cannot be read, the hook walks the project instead, but only when
    `design/brief.md` exists. Default: the walk looks at 2,000 files at most.
  - A file time more than 60 seconds in the future is ignored.

The hook blocks the stop with `decision: "block"` when a counted file changed after the newest file in
`design/reviews/` with a passing verdict line: `Originality: original` or `Originality: watch`.
A derivative verdict does not pass. With no passing review, it blocks when a counted file changed in
the last 24 hours. The block fires once per turn: on the retry `stop_hook_active` is true and the
stop goes through. The reason lets a draft handed over for feedback stop after one line.

The stop passes when:
  - `stop_hook_active` is true;
  - `design/decisions.md` holds a line `Override: originality-gate <YYYY-MM-DD> <reason>` dated today;
  - any error or timeout occurs (the hook fails open).

Default: 8 seconds of work at most. It writes nothing and calls no network.

Environment, for tests and local runs:
  GDH_HOOK_TIMEOUT   the total time budget in seconds; default 8.
"""
import datetime
import json
import os
import re
import sys
import time

DESIGN_EXT = {".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".svg", ".vue", ".svelte"}
EDIT_TOOLS = {"Write", "Edit", "MultiEdit"}
# Every folder whose name starts with a dot is skipped as well.
SKIPPED_DIRS = {"node_modules", "dist", "build", "coverage", "htmlcov", "out", "storybook-static", "vendor",
                "target"}
DEFAULT_BUDGET = 8.0
MAX_FILES = 2000
MAX_STDIN = 4 * 1024 * 1024
MAX_READ = 1024 * 1024
MAX_DEPTH = 64
RECENT_SECONDS = 24 * 60 * 60
FUTURE_SLACK = 60
SHOW = 5
MAX_SUBAGENT_LOGS = 200
NAME_LIMIT = 120
OVERRIDE = re.compile(r"^\s*Override:\s*originality-gate\s+(\d{4}-\d{2}-\d{2})\s+\S")
VERDICT = re.compile(r"^\s*Originality:\s*(original|watch)\b", re.I)
GATE_SKILL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills",
                          "originality-gate", "SKILL.md")


class OutOfTime(Exception):
    pass


def budget():
    try:
        value = float(os.environ.get("GDH_HOOK_TIMEOUT", DEFAULT_BUDGET))
    except ValueError:
        return DEFAULT_BUDGET
    return value if 0 < value <= 60 else DEFAULT_BUDGET


def skipped(name):
    return name.startswith(".") or name in SKIPPED_DIRS


def project_root(cwd):
    """Return the first folder from cwd up to the git root that holds design/, or None."""
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


def usable_mtime(mtime, now):
    """A file time more than FUTURE_SLACK seconds ahead of now is not trusted."""
    return mtime <= now + FUTURE_SLACK


def counted(path, root):
    """Return the project-relative path of a design file that counts, or None."""
    if os.path.splitext(path)[1].lower() not in DESIGN_EXT:
        return None
    try:
        rel = os.path.relpath(path, root)
    except ValueError:
        return None
    parts = rel.split(os.sep)
    if rel == ".." or rel.startswith(".." + os.sep) or any(skipped(part) for part in parts[:-1]):
        return None
    if parts[:2] == ["design", "reviews"]:
        return None
    return rel.replace(os.sep, "/")


def walk(top, deadline, counter):
    """Yield (path, mtime) for regular files under top. Skips skipped folders and symbolic links."""
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
                    if not skipped(entry.name):
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


def last_verdict(root, now, deadline, counter):
    """Return the mtime of the newest review file with a passing verdict line, or None."""
    reviews = os.path.join(root, "design", "reviews")
    if not os.path.isdir(reviews):
        return None
    newest = None
    for path, mtime in walk(reviews, deadline, counter):
        if not usable_mtime(mtime, now) or (newest is not None and mtime <= newest):
            continue
        try:
            text = read_text(path)
        except (OSError, ValueError):
            continue
        if any(VERDICT.match(line) for line in text.splitlines()):
            newest = mtime
    return newest


def tool_uses(value):
    """Yield every dict with type tool_use inside a parsed transcript line."""
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            if item.get("type") == "tool_use":
                yield item
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)


def read_edits(path, cwd, deadline, paths):
    """Add the file paths of the edit calls in one JSONL transcript to paths."""
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        for number, line in enumerate(handle):
            if number % 256 == 0 and time.monotonic() > deadline:
                raise OutOfTime()
            if '"tool_use"' not in line:
                continue
            try:
                data = json.loads(line)
            except ValueError:
                continue
            for use in tool_uses(data):
                if use.get("name") not in EDIT_TOOLS or not isinstance(use.get("input"), dict):
                    continue
                target = use["input"].get("file_path")
                if isinstance(target, str) and target:
                    paths.add(os.path.join(cwd, os.path.expanduser(target)))


def session_edits(transcript, cwd, deadline):
    """Return the absolute paths that edit calls of this session touched, or None when unreadable.

    Subagents of the session keep their own transcripts in `<transcript stem>/subagents/`; those count too.
    """
    if not isinstance(transcript, str) or not transcript:
        return None
    main_path = os.path.expanduser(transcript)
    paths = set()
    try:
        read_edits(main_path, cwd, deadline, paths)
    except (OSError, ValueError):
        return None
    subagents = os.path.join(os.path.splitext(main_path)[0], "subagents")
    try:
        names = sorted(name for name in os.listdir(subagents) if name.endswith(".jsonl"))
    except OSError:
        names = []
    for name in names[:MAX_SUBAGENT_LOGS]:
        try:
            read_edits(os.path.join(subagents, name), cwd, deadline, paths)
        except (OSError, ValueError):
            continue
    return paths


def changed_from_session(paths, root, since, now):
    out = []
    for path in paths:
        real = os.path.realpath(path)
        rel = counted(real, root)
        if rel is None:
            continue
        try:
            mtime = os.stat(real).st_mtime
        except OSError:
            continue
        if since < mtime and usable_mtime(mtime, now):
            out.append((mtime, rel))
    out.sort(reverse=True)
    return [rel for _, rel in out]


def changed_from_walk(root, since, now, deadline, counter):
    out = []
    for path, mtime in walk(root, deadline, counter):
        rel = counted(path, root)
        if rel is not None and since < mtime and usable_mtime(mtime, now):
            out.append((mtime, rel))
    out.sort(reverse=True)
    return [rel for _, rel in out]


def clean_name(name):
    text = "".join(char for char in name if char.isprintable())
    return text if len(text) <= NAME_LIMIT else text[:NAME_LIMIT - 3] + "..."


def reason(changed, verdict, today):
    shown = ", ".join(clean_name(name) for name in changed[:SHOW])
    if len(changed) > SHOW:
        shown += " and %d more" % (len(changed) - SHOW)
    if verdict is None:
        lead = "GDH originality gate: %d design file(s) changed in this session and no review in " \
               "design/reviews/ holds a passing originality verdict (%s)." % (len(changed), shown)
    else:
        lead = "GDH originality gate: %d design file(s) changed after the last passing originality verdict " \
               "(%s)." % (len(changed), shown)
    return " ".join([
        lead,
        "If this turn hands over a draft for feedback rather than finished work, say so in one line and stop.",
        "Before you call the design done, run the gate.",
        "Run the design-critique skill on the changed work.",
        "Start the originality-gate skill. If it is not listed, read %s and follow it." % GATE_SKILL,
        "Write the verdict to design/reviews/%s-originality.md with a line 'Originality: original' or "
        "'Originality: watch'. A derivative verdict does not pass; change the work first." % today,
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
    now = time.time()
    counter = [0]
    try:
        edits = session_edits(data.get("transcript_path"), cwd, deadline)
        if edits is not None and not edits:
            return 0
        if edits is None and not os.path.isfile(os.path.join(root, "design", "brief.md")):
            return 0
        verdict = last_verdict(root, now, deadline, counter)
        since = verdict if verdict is not None else now - RECENT_SECONDS
        if edits is not None:
            changed = changed_from_session(edits, root, since, now)
        else:
            changed = changed_from_walk(root, since, now, deadline, counter)
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
