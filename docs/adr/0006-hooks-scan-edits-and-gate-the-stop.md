# 0006: Hooks scan every design edit and gate the stop on an originality verdict

Date: 2026-11-26. Status: accepted. Amended 2026-11-27 after review.

## Context

Up to 0.1.0, GDH had one hook. It printed the kernel and the moments at session start. Every check after that depended on the agent choosing to run it: the tell scan of `design-critique` ran only when a skill said so, and nothing stopped an agent from ending a turn on templated work. The owner wants every design artifact to be distinctive and non-derivative. A rule that the agent may forget is not enough for that goal.

## Decision

- A PostToolUse hook, `kit/hooks/post_edit.py`, runs after each Write, Edit and MultiEdit call. When the edited file has a design extension and the project has a `design/` folder, it runs the tell scan on that one file, with the project tokens and `DESIGN.md` when they exist. On a markup file (`.html`, `.htm`, `.jsx`, `.tsx`, `.vue`, `.svelte`) it also runs the `originality-gate` check when that script is present. Findings reach the agent as context next to the tool result, 12 lines at most. The agent reviews each one and fixes it or records a brand-required reason. The hook never blocks the edit.
- A Stop hook, `kit/hooks/stop_gate.py`, acts only when this session edited a design file. It reads the session transcript, and the subagent transcripts beside it, for Write, Edit and MultiEdit calls on design files inside the project. When the transcript cannot be read, it walks the project instead, but only when `design/brief.md` exists.
- The Stop hook holds the end of the turn once when such a file changed after the newest review in `design/reviews/` with a passing verdict line: `Originality: original` or `Originality: watch`. A derivative verdict does not pass. With no passing review, it holds the stop when such a file changed in the last 24 hours. Default: 24 hours.
- The block fires once per turn. On the retry `stop_hook_active` is true and the stop goes through, so the hook cannot loop. The reason says: when this turn hands over a draft for feedback rather than finished work, say so in one line and stop. Before the design is called done, the agent runs `design-critique`, starts the `originality-gate` skill, and writes the verdict to `design/reviews/<today>-originality.md`.
- Override: a line `Override: originality-gate <YYYY-MM-DD> <reason>` in `design/decisions.md`, dated today, lets the stop through. The reason is required. The override lasts one day, so it never silences the gate for good.
- Both hooks act only in a project with a `design/` folder. The search runs from the session folder up to the git root, and no further. Every dot-folder, and the folders `node_modules`, `dist`, `build`, `coverage`, `htmlcov`, `out`, `storybook-static`, `vendor` and `target`, are skipped.
- A file time more than 60 seconds in the future is ignored, so a skewed clock cannot hold or free the gate for good. Default: 60 seconds.
- Both hooks fail open. Any error, a timeout or a missing script means exit 0 with no output. Each command in `hooks.json` ends with `|| true`, so a launch failure, such as an unset plugin root variable, also exits 0 and never reads as a block. Default: 8 seconds of work in total for each hook. Default: the project walk looks at 2,000 files at most.

## Why fail open

A hook runs inside every session of every project that installs the plugin. A hook that fails closed would turn a missing script, a slow disk or a bug in GDH into a stuck session for work that has nothing to do with design. The scans are heuristics, and a false block costs more trust than a missed tell. The gates that block delivery stay in the skills, where the agent can read why. The hooks remind and hold the stop once; they do not judge.

## Why a design folder and a session edit

GDH loads beside coding harnesses and is often installed globally. Most edits in most projects are not design work. The `design/` folder is the workspace that GDH skills write, so its presence is the plain sign that the user chose GDH for this project. Without it the hooks stay silent, and a coding session pays no cost beyond one small process start. The walk stops at the git root, so a stray `design/` folder in a parent directory cannot switch the hooks on. A session that did no design work is never held, even in a design project, because the gate reads what this session edited.

## Consequences

- A turn that finishes design work ends with a critique and an originality verdict, or with a dated override that the decision record keeps. A turn that hands over a draft says so and stops.
- The verdict file format is light: any file in `design/reviews/` with a passing `Originality:` line. The `originality-gate` skill owns the full report.
- A checkout, a pull or a copy that touches every file does not trigger the gate, because only files this session edited count. The exception is the fallback: with an unreadable transcript and a `design/brief.md`, file times decide, and such a bulk change can hold the stop once.
- The transcript format is not a published contract. The hook looks for `tool_use` entries with a `name` and an `input.file_path`, which matches the transcripts of Claude Code on 2026-11-27. When the format changes, the hook falls back as described above.
- The Codex hook support and its plugin root variable are still UNTESTED (open work item 34). The `|| true` guard keeps a missing variable harmless.
- `GDH_PLUGIN_ROOT` overrides the plugin folder of the PostToolUse hook; tests point it at stub scripts. `GDH_HOOK_TIMEOUT` shortens the time budget of both hooks for tests and local runs.

## Alternatives considered

- Block the edit on findings: rejected, because a PostToolUse hook runs after the file is written, and a block there only adds noise. The agent fixes faster with the findings as context.
- Run the full critique in the hook: rejected, because the critique needs judgment and the brief, and a hook has a few seconds.
- Gate on every project, or on file times alone: rejected, because it holds sessions that did no design work.
- Block on every retry: rejected, because it would hold a draft turn that waits for the user's feedback.
- A permanent override flag: rejected, because it would switch the gate off for every later round.
