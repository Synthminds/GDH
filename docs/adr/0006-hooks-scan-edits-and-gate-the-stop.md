# 0006: Hooks scan every design edit and gate the stop on an originality verdict

Date: 2026-11-26. Status: accepted.

## Context

Up to 0.1.0, GDH had one hook. It printed the kernel and the moments at session start. Every check after that depended on the agent choosing to run it: the tell scan of `design-critique` ran only when a skill said so, and nothing stopped an agent from ending a turn on templated work. The owner wants every design artifact to be distinctive and non-derivative. A rule that the agent may forget is not enough for that goal.

## Decision

- A PostToolUse hook, `kit/hooks/post_edit.py`, runs after each Write, Edit and MultiEdit call. When the edited file has a design extension and the project has a `design/` folder, it runs the tell scan on that one file, with the project tokens and `DESIGN.md` when they exist. It also runs the `originality-gate` check when that script is present. Findings reach the agent as context next to the tool result, 12 lines at most. The hook never blocks the edit.
- A Stop hook, `kit/hooks/stop_gate.py`, holds the end of the turn when a design file changed after the newest review in `design/reviews/` that holds a line starting with `Originality:`. With no such review, it holds the stop when a design file changed in the last 24 hours. The reason tells the agent to run `design-critique` and `originality-gate` and to write the verdict.
- Override: a line `Override: originality-gate <YYYY-MM-DD> <reason>` in `design/decisions.md`, dated today, lets the stop through. The reason is required. The override lasts one day, so it never silences the gate for good.
- Both hooks act only in a project with a `design/` folder. The search for it runs from the session folder up to the git root, and no further.
- Both hooks fail open. Any error, a timeout or a missing script means exit 0 with no output. Default: 8 seconds of work in total for each hook. Default: the Stop hook looks at 2,000 files at most.
- The Stop hook passes when `stop_hook_active` is true, so it cannot hold a turn twice in a row.

## Why fail open

A hook runs inside every session of every project that installs the plugin. A hook that fails closed would turn a missing script, a slow disk or a bug in GDH into a stuck session for work that has nothing to do with design. The scans are heuristics, and a false block costs more trust than a missed tell. The gates that block delivery stay in the skills, where the agent can read why. The hooks remind and hold the stop; they do not judge.

## Why a design folder

GDH loads beside coding harnesses and is often installed globally. Most edits in most projects are not design work. The `design/` folder is the workspace that GDH skills write, so its presence is the plain sign that the user chose GDH for this project. Without it the hooks stay silent, and a coding session pays no cost beyond one small process start. The walk stops at the git root, so a stray `design/` folder in a parent directory cannot switch the hooks on.

## Consequences

- A turn that changes design work now ends with a critique and an originality verdict, or with a dated override that the decision record keeps.
- The verdict file format is light: any file in `design/reviews/` with a line that starts with `Originality:`. The `originality-gate` skill owns the full report.
- The 24-hour window means a fresh project with older design files and no review is not held. Default: 24 hours.
- File times decide what changed. A checkout or a copy that touches every file can trigger the gate once.
- The Codex hook support and its plugin root variable are still UNTESTED (open work item 34). The hooks read `CLAUDE_PLUGIN_ROOT` through the command line only.
- Tests can point the PostToolUse hook at stub scripts with `GDH_PLUGIN_ROOT`, and shorten the time budget of both hooks with `GDH_HOOK_TIMEOUT`.

## Alternatives considered

- Block the edit on findings: rejected, because a PostToolUse hook runs after the file is written, and a block there only adds noise. The agent fixes faster with the findings as context.
- Run the full critique in the hook: rejected, because the critique needs judgment and the brief, and a hook has a few seconds.
- Gate on every project: rejected, for the cost and noise in non-design work described above.
- A permanent override flag: rejected, because it would switch the gate off for every later round.
