# GDH: Global Design Harness

GDH is a kit of skills, rules and catalogs that makes a coding agent do design work the way a careful designer does. It covers brand and logo, typography, color, design systems, websites, apps, dashboards, charts, network graphs, infographics, 3D, interface motion, video, mood boards, critique, accessibility and the handoff to code.

GDH does four things that a plain agent does not:

1. It asks before it draws. Every session opens with `align`, a short alignment interview. A confirmed brief and a chosen direction come before any full build.
2. It routes by capability. A catalog says which connected tool can make an image, a video, a board or a model, and what each one costs and exposes.
3. It guards the user. A call that spends credits needs a quote and a yes. Anything that leaves the project needs a yes. An outside asset needs a read license and a record.
4. It keeps a record. Each round, each choice and each rejected option is written to the project, with a label that says what was proven.

The kit is plain files: Markdown, JSON and Python with no dependency. It ships no vendor code.

## GDH and GCH

GCH is the coding harness. GDH is its sibling for design. Neither needs the other.

| Question | GDH | GCH |
| --- | --- | --- |
| What does it govern? | The look, the content of screens, assets, motion, the brand | Code, tests, review, architecture |
| Where does a task start? | A new look, a brand, a mood board, a chart style, 3D, video, an outside asset | A change inside an existing design system |
| What does it hand over? | `DESIGN.md`, `design/tokens.json`, `design/handoff.md`, assets with licenses | The built and verified product |
| Whose numbers hold for screens when both are loaded? | GDH defaults give way | GCH `ux-laws` |

When both are installed, GCH offers GDH for design-led work, and GDH hands approved designs back through `handoff-to-code`. The text GCH uses is in [docs/HANDOFF-GCH.md](docs/HANDOFF-GCH.md).

## Install

Each route has an evidence label. VERIFIED: run in this repository on 2026-11-23. DOCUMENTED: stated by the host's own documentation, not run here. UNTESTED: from a secondary source, or not tried.

### Claude Code plugin

```
/plugin marketplace add Synthminds/GDH
/plugin install gdh@synthminds-gdh
```

- Evidence: DOCUMENTED. The command forms come from the Claude Code documentation. The install was not run for this release.
- To try the kit for one session without installing: `claude --plugin-dir ./kit`. Evidence: DOCUMENTED.
- To check the plugin form: `claude plugin validate ./kit`. Evidence: UNTESTED. It was not run for this release.
- A SessionStart hook prints the kernel and the moments text. Evidence: VERIFIED for the script output in the unit tests. UNTESTED for a live session.
- In the plugin, each skill name carries the prefix `gdh:`.

### Codex

The repository holds a Codex marketplace file at `.agents/plugins/marketplace.json` and a plugin manifest at `kit/.codex-plugin/plugin.json`.

- The manifest names one skills folder (`"skills": "./skills/"`) and the hooks file (`"hooks": "./hooks/hooks.json"`).
- Evidence: DOCUMENTED for the file layout, which follows sample repositories from the publisher. UNTESTED for the install commands and for hook support. The hook command reads `CLAUDE_PLUGIN_ROOT`; whether Codex sets that variable is UNTESTED. When the hook does not run, the kernel reaches Codex only through the export route. Read the current Codex documentation for the command that adds a marketplace.
- The export route below is the tested way to give Codex the skills.

### Export into any project

```
python3 scripts/gdh.py export --repo /path/to/project --hosts claude,codex,cursor,agents --dry-run
python3 scripts/gdh.py export --repo /path/to/project --hosts claude,codex,cursor,agents
```

- The export copies the skills to `.claude/skills` and `.agents/skills`, with the catalogs, tool cards and canon beside them. It copies the subagents to `.claude/agents`. It writes a managed block into `AGENTS.md` between two marker lines. For the `claude` host it also writes a managed block into `CLAUDE.md` that imports `AGENTS.md`, unless `CLAUDE.md` already imports it. It adds project templates that never overwrite an existing file.
- A second run changes nothing. A copied file that a person edited is a conflict and stays as it is. `--replace-edited` copies it to `.agents/gdh/backups/<UTC time>/` and replaces it. A file that GDH did not write is a conflict; `--force` backs it up the same way and replaces it. A managed block that a person edited is backed up the same way and then rewritten. Run `--dry-run` first to see each action.
- Evidence: VERIFIED for the copy, the dry run and the second run (unit tests and a run into an empty folder). DOCUMENTED that Claude Code reads `.claude/skills`, and that it reads the kernel through the `@AGENTS.md` import that the export writes into `CLAUDE.md`. UNTESTED that Cursor reads `.agents/skills` or acts on `AGENTS.md`.

### Claude apps: upload a skill or the plugin

- One skill: zip one folder under `kit/skills/` from its parent, so that the archive holds `<skill-name>/SKILL.md`. In the app, open Customize, then Skills, and upload it. Evidence: DOCUMENTED.
- The whole plugin: zip the `kit` folder and upload it under Customize, then Plugins. Evidence: DOCUMENTED.
- Limits. Evidence: DOCUMENTED. The chat apps load skills. They do not load hooks or subagents, so the kernel is not printed at session start. Start with the `align` skill; it opens the session and hands over to `ask-gdh`.
- Known risk. Evidence: UNTESTED. The skill upload is documented to accept only the standard frontmatter fields. GDH skills also carry `disable-model-invocation` and `argument-hint`. An upload may reject or ignore them.
- A skill uploaded alone cannot follow its links to the catalogs and tool cards. Upload the plugin when you need those.

## Your first design project

1. Install GDH by one route above. Open your project.
2. Say what you want in plain words. Example: "We are opening a bakery. Design the shop site." The agent starts `align`.
3. Answer the alignment interview. Without a confirmed `design/brief.md`, `align` runs the full interview, one question at a time, each with a recommended answer. With a confirmed brief, it re-aligns in a few questions. Say `--full` or "full interview" to force the long form. Say "skip" or "you decide" at any question; the agent records its proposal as ASSUMED. You may end the interview at any time.
4. Confirm the brief. `design-brief` writes `design/brief.md` from your answers and waits for your yes. Then `ask-gdh` reports what exists, which tools are connected, and which skills it will run.
5. Choose a direction. The agent shows two to four boards that differ in idea. You say keep, change or remove for each part. The choice goes into `design/decisions.md`.
6. Approve the system. The agent writes `design/tokens.json`, `design/tokens.css` and `DESIGN.md`, and checks contrast in every theme.
7. Let it build, one gate at a time. Before a call that spends credits, you see a quote. Before anything is published or uploaded, you are asked. Each outside asset gets a license record.
8. Review and hand off. The agent runs `design-critique` and `accessibility-gate`, runs a round for the fixes you pick, then packages `design/handoff.md` for the coding work.

To see what a finished design system looks like, open `brands/example-harbor-lantern/specimen.html` in a browser. `sample.html` beside it is one screen built only from the pack's tokens. Its `SOURCE.md` traces each color and face to the subject.

## Skill catalog

The kit holds 29 skills. Eight are model-invoked: the agent starts them from the task. `align` opens every session. The other 21 are user-invoked: the user types their command, or `ask-gdh` reads their `SKILL.md` and follows it.

[//]: # (gdh-catalog:start)
| Skill | Invocation | Discipline | What it does |
| --- | --- | --- | --- |
| `align` | model | alignment | Opens every GDH session with an alignment interview, before any other GDH skill and before any look is chosen. |
| `ask-gdh` | model | router | Routes a design-led request in the Global Design Harness once align has run. |
| `design-brief` | model | brief | Owns the GDH brief, with the format of design/brief.md, the design persona form and the fidelity ladder. |
| `mood-board` | model | moodboard | Sets the art direction from a confirmed brief. |
| `find-assets` | model | assets | Finds outside assets and clears them for use, including components, icons, fonts, illustrations, photos, video, 3D and motion files. |
| `design-critique` | model | critique | Reviews design work against the brief, the design system, the checks of its discipline and the dated tell list. |
| `design-system` | user | design-system | Creates, loads, checks and publishes design systems in the Claude Design System shape. |
| `typography` | user | typography | Chooses, pairs, licenses, loads, scales and sets type for a brand or a product. |
| `color` | user | color | Builds palettes, themes and contrast-checked semantic colors for a brand or a product. |
| `logo-identity` | user | logo | Takes a logo from a brief to a tested vector system. |
| `website-design` | user | website | Takes a chosen direction to a built website. |
| `app-design` | user | app | Designs mobile, desktop and web app flows, screens and states. |
| `dashboard-design` | user | dashboard | Designs a screen that people monitor, analyze or report with. |
| `data-viz` | user | dataviz | Chooses and builds charts that state a finding. |
| `network-graph` | user | network-graph | Designs a readable picture of entities and their relations, static or interactive. |
| `infographic` | user | infographic | Designs one composed explainer with one message and one reading path. |
| `ui-motion` | user | ui-motion | Decides, times and specifies motion inside an interface. |
| `motion-video` | user | motion-video | Takes a video or motion graphic from brief to delivered files. |
| `three-d` | user | 3d | Puts 3D on the web when it earns its place. |
| `generate-media` | user | media | Generates images, vectors, video clips, audio, voice and 3D models for a design. |
| `reverse-engineer-reference` | user | reference | Studies a reference site, app or screenshot and writes a teardown sheet of what can be learned from it. |
| `claude-design` | user | claude-design | Chooses and drives the Claude artifact types for design work. |
| `refine-round` | user | refinement | Runs one scoped feedback round on a design. |
| `accessibility-gate` | user | accessibility | Runs the accessibility checks for the medium of a design and writes a pass or fail report. |
| `handoff-to-code` | user | handoff | Packages an approved design for the coding harness or any coding agent. |
| `add-design-tool` | user | evolution | Vets, catalogs, exercises and wires a new design tool, connector or asset source. |
| `design-principles` | user | critique | Selects the design principles that apply to a task from the GDH principles canon, by discipline and stage, and lists each as a gate or a default with its source. |
| `concept-forge` | model | moodboard | Generates original design concepts from the subject's own world before any style choice. |
| `originality-gate` | model | critique | Tests whether a design is derivative before it is called done. |
[//]: # (gdh-catalog:end)

The kit also ships five subagents: `art-director` writes direction files; `design-critic`, `a11y-auditor` and `originality-auditor` are read-only reviewers; `asset-scout` searches and reads licenses. It ships a catalog of design tools with one card for each, a catalog of local creative programs (Inkscape, GIMP, Blender, FreeCAD and others) that agents drive through pinned CLI-Anything harnesses, and a catalog of free asset sources with license notes.

## How GDH evolves

GDH grows by data. A new tool is one JSON file and one card. A skill changes only when a tool needs method that no skill holds.

- Say "add this tool" and name it. The agent runs `add-design-tool`: it vets the tool, writes the catalog entry and the card, makes one real free call, and labels the evidence.
- `python3 scripts/gdh.py new-tool` and `new-skill` scaffold the files. `build` regenerates the manifests and this catalog. `check` runs every rule. `doctor` lists stale entries, untested tools and skills with no eval case.
- Each skill keeps a `refinement-log.md` with one line for each change.
- Prices, credit amounts, model names and tool counts are never written into a skill. The agent reads them live.

Architecture, finding codes and the open-work list are in [docs/GDH.md](docs/GDH.md). Rules for working on this repository are in [AGENTS.md](AGENTS.md).

## Brand packs

A brand pack is the portable copy of one brand's design system: `README.md`, `tokens.json`, and the generated `tokens.css` and `DESIGN.md`.

- This public repository carries one example pack, `brands/example-harbor-lantern/`, for a fictional brand, and the template `brands/_template/`.
- Every other folder under `brands/` is private by default. `.gitignore` ignores `brands/*` and allows only the README, the template and the example. A new private pack needs no edit to any tracked file. `gdh.py check` still validates every pack that is present on disk.
- Never name a private pack in a tracked file, `.gitignore` included. Put any extra local ignore rule in `.git/info/exclude`, which is never committed.
- More detail is in [brands/README.md](brands/README.md).
- Make a pack with `python3 kit/skills/design-system/scripts/ds.py init brands/<slug> --name "<Name>"`, then run the `design-system` skill.
- Keep private facts out of any pack that goes public: no client names, no account ids, no private links.

## What is proven and what is not

- VERIFIED on 2026-11-23: `gdh.py check` exits 0; the unit tests pass; the token, mood-board, tell-scan and asset scripts run on real input; the export is idempotent.
- DOCUMENTED: every tool card. Nearly all were written from guides and tool descriptions. No spend call was made.
- UNTESTED: output quality of any connected tool, live plugin installs, and every eval case. No design was built with this kit before release.

The honest list of gaps is in [docs/GDH.md](docs/GDH.md), under "Open work".

## License

`UNLICENSED`: all rights reserved by the owner until a license is chosen. Sources that informed the kit are listed in [docs/SOURCES.md](docs/SOURCES.md). The kit copies no text and no code from them.
