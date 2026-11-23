# The GDH kit

This folder is the plugin. Everything an agent loads at run time is here. The repository root holds the engine, the tests, the brand packs and the documents for people.

## Layout

| Path | Holds | Edited by |
| --- | --- | --- |
| `kit.json` | The registry: skills, agents, moments, wired skills, budgets. The single source of truth. | a person or an agent |
| `canon/KERNEL.md` | The always-on rules: rule 0, align first, then 15 more. 60 lines at most. | a person |
| `canon/PRINCIPLES.md` | Precedence, the shape of a skill, evidence labels, gates and defaults. Loaded on demand. | a person |
| `canon/MOMENTS.md` | When to start or offer a skill. | generated |
| `hooks/` | The SessionStart hook. It prints the kernel, then the moments. | a person |
| `skills/<name>/` | One folder for each skill: `SKILL.md`, `references/`, and where needed `scripts/`, `protocols/`, `templates/`. | a person or an agent |
| `agents/<name>.md` | Subagents. | a person or an agent |
| `catalogs/capabilities.json` | The fixed capability words, and for each discipline the owning skill. | through `add-design-tool` |
| `catalogs/tools/<id>.json` | One entry for each design tool. | through `add-design-tool` |
| `catalogs/assets.json` | Free asset sources with license notes. | through `add-design-tool` |
| `references/tools/<id>.md` | One card for each tool: call order, limits, evidence. | through `add-design-tool` |
| `templates/project/` | Files that the export copies into a project. | a person |
| `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` | Plugin manifests. | generated |
| `scan.accepted.json` | Accepted findings as `{code, path, reason}`, plus `match` (the sha256 that `check --json` prints) for `GDH_SECRET`, `GDH_PRIVATE_LINK` and `GDH_SCRIPT_NETWORK`. One exact path for those and for `GDH_SYMLINK` and `GDH_BRAND_PUBLIC`. Empty by default. Rules in `docs/GDH.md`, section 3. | a person |
| `upstream.lock.json` | Provenance of copied third-party files. The kit copies none. | a person |

Do not edit a generated file. Change `kit.json` or a skill description, then run `python3 scripts/gdh.py build` from the repository root.

## How an agent uses the kit

1. At session start the hook prints [canon/KERNEL.md](canon/KERNEL.md) and [canon/MOMENTS.md](canon/MOMENTS.md).
2. The first design-led request of a session starts `align`. Without a confirmed `design/brief.md` it runs the full interview. With one it re-aligns in a few questions. `--full` forces the full interview.
3. `align` hands its answers to `design-brief`, which writes the brief. Then `ask-gdh` runs a pre-flight and names the skills to run. It starts a model-invoked skill by name. For a user-invoked skill it reads that skill's `SKILL.md` and follows it, because the host does not let the model start such a skill.
4. A skill names the capabilities it needs. The agent reads [catalogs/capabilities.json](catalogs/capabilities.json) and the tool entries, confirms that a tool is present in the session, and reads its card before the first call.
5. A skill writes its results into the project: `DESIGN.md`, `design/brief.md`, `design/decisions.md`, `design/tokens.json`, `design/assets/manifest.json`, `design/reviews/`, `design/handoff.md`.

The reasons behind the rules are in [canon/PRINCIPLES.md](canon/PRINCIPLES.md).

## Scripts in the kit

Each script uses the Python standard library only, makes no network call, and exits 0 on a pass and 1 on findings.

| Script | Skill | Does |
| --- | --- | --- |
| `skills/design-system/scripts/ds.py` | `design-system` | Validates tokens, measures contrast, converts from CSS and DTCG, exports CSS and a theme file, writes `DESIGN.md` and a specimen page, audits raw values. |
| `skills/mood-board/scripts/moodboard.py` | `mood-board` | Builds an offline board page from a board file and checks it. |
| `skills/design-critique/scripts/tells.py` | `design-critique` | Scans HTML and CSS for habits that mark generic output. Brand-required choices are reported apart. |
| `skills/find-assets/scripts/assets.py` | `find-assets` | Searches the asset catalog, writes provenance records, checks the manifest against files, writes notices. |

## Skills

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
[//]: # (gdh-catalog:end)
