# GDH architecture and maintenance

This document is for the people and agents who maintain the Global Design Harness. A user of GDH needs only the [README](../README.md).

Terms used in one sense. Kernel: the always-loaded rules text. Card: one tool's reference page. Tell: a visual habit that marks work as generic AI output. Direction: one coherent visual proposal. Brief: the confirmed statement of subject, audience and job. Decision record: `design/decisions.md` in a project. Gate: a check that blocks delivery. Default: a starting value that the user, the design system or the brief can replace. Spend call: a tool call that uses credits or a paid quota.

## 1. Layout

```
.claude-plugin/marketplace.json     generated: Claude Code marketplace, plugin "gdh", source "./kit"
.agents/plugins/marketplace.json    generated: Codex marketplace
README.md  CHANGELOG.md  AGENTS.md
kit/                                the plugin
  kit.json                          the registry
  canon/KERNEL.md  PRINCIPLES.md  MOMENTS.md (generated)
  hooks/hooks.json  hooks/session_start.py  hooks/post_edit.py  hooks/stop_gate.py
  skills/<name>/SKILL.md            plus references/, scripts/, protocols/, templates/
  agents/<name>.md
  catalogs/capabilities.json  catalogs/tools/<id>.json  catalogs/assets.json
  references/tools/<id>.md
  templates/project/
brands/<slug>/  brands/_template/
scripts/gdh.py                      check | build | export | doctor | new-tool | new-skill
tests/
evals/cases/triggering/*.json
evals/cases/quality/                labelled pages and boards; evals/quality.py scores them
docs/GDH.md  docs/HANDOFF-GCH.md  docs/SOURCES.md  docs/adr/
```

Three layers load at different times:

| Layer | Loaded | Budget |
| --- | --- | --- |
| Kernel and moments | At session start, by the hook; or in the managed `AGENTS.md` block after an export | 60 lines for the kernel; 3,500 characters for the moments |
| Skill descriptions | Always, for the six model-invoked skills | 5,000 characters in total |
| Skill bodies, references, cards, catalogs | On demand, when a skill runs | 150 lines and 1,500 words for a `SKILL.md`; 400 lines for a reference |

The budgets are small on purpose. GDH is meant to load beside a coding harness that already uses most of its own budget.

The front door. Every design session starts with `align`. Without a confirmed `design/brief.md` it runs the full interview. With one it re-aligns in a few questions. `--full` forces the full interview. Four places carry this rule and must agree: kernel rule 0, the first moment in `kit.json`, the first line of the managed `AGENTS.md` block that `export` writes, and the README files. `ask-gdh` routes only after `align` closes.

## 2. The registry

[kit/kit.json](../kit/kit.json) is the single source of truth.

| Key | Holds |
| --- | --- |
| `name`, `displayName`, `version`, `description`, `author`, `repository`, `license` | Identity. `build` copies these into the manifests. |
| `budgets` | `modelDescriptionChars`, `kernelLines`, `momentsChars`. `check` enforces each. |
| `skills` | One entry for each skill: `invocation` (`model` or `user`), `origin`, `discipline`. |
| `agents` | The subagent names. They must equal the files in `kit/agents/`. |
| `moments` | `when`, `start`, `offer`, `note`. A moment starts only model-invoked skills and offers three skills at most. |
| `wired` | Skills that are not in the kit, each with its install line and source. A moment may offer one. |
| `requires` | Optional relations. GCH is optional. |

What `build` writes from it: both plugin manifests, both marketplace files, [kit/canon/MOMENTS.md](../kit/canon/MOMENTS.md), and the skill table between the two catalog marker lines in the root README and the [kit README](../kit/README.md). The marker lines are Markdown link-reference comments, not HTML comments, so the prose scan accepts them.

## 3. Finding codes

`python3 scripts/gdh.py check` runs every rule and exits 1 on any finding. Each rule has one code and one mutation test in `tests/test_gdh.py`.

| Code | Rule |
| --- | --- |
| `GDH_JSON_INVALID` | A JSON file does not parse. |
| `GDH_KIT_JSON` | kit.json is missing or does not match the registry schema. |
| `GDH_AGENT_REGISTRY` | The agents list in kit.json and the files in kit/agents differ. |
| `GDH_FRONTMATTER` | A SKILL.md has no readable frontmatter block. |
| `GDH_SKILL_NAME` | A skill name is not kebab-case or is longer than 64 characters. |
| `GDH_SKILL_NAME_FOLDER` | A skill name differs from its folder name. |
| `GDH_SKILL_DESCRIPTION` | A skill description is absent or is not 1 to 1024 characters. |
| `GDH_DESCRIPTION_BUDGET` | The model-invoked descriptions exceed budgets.modelDescriptionChars. |
| `GDH_REGISTRY_MISSING_FOLDER` | A registered skill has no folder with a SKILL.md. |
| `GDH_REGISTRY_UNREGISTERED` | A skill folder is not registered in kit.json. |
| `GDH_INVOCATION_FLAG` | disable-model-invocation does not agree with the registered invocation. |
| `GDH_SKILL_SIZE` | A SKILL.md exceeds 150 lines or 1,500 words. |
| `GDH_REFERENCE_SIZE` | A reference file exceeds 400 lines. |
| `GDH_LINK_BROKEN` | A relative Markdown link in kit/ or docs/ does not resolve. |
| `GDH_SKILL_FILE_UNLINKED` | A file in a skill folder is not linked from its SKILL.md. |
| `GDH_ROUTER_INCOMPLETE` | The ask-gdh skill does not name a registered skill. |
| `GDH_ROUTE_USER_SKILL` | A line starts a user-invoked skill as if the host could start it, or the kernel lacks the skill handoff route. |
| `GDH_SYMLINK` | The repository holds a symbolic link. |
| `GDH_HTML_COMMENT` | A kit Markdown file holds an HTML comment. |
| `GDH_BASE64` | A kit Markdown file holds a base64 run of 80 or more characters. |
| `GDH_EMOJI` | A kit Markdown file holds an emoji. |
| `GDH_EM_DASH` | A kit Markdown file holds an em dash. |
| `GDH_SECRET` | A file holds a key, a token, an email address or a uuid-like account id. |
| `GDH_PRIVATE_LINK` | A file holds a private Claude link, a workspace, team, organization or account id, or a link to another repository of the kit's owner. |
| `GDH_SCRIPT_NETWORK` | A script imports a network module or calls a download program. |
| `GDH_KERNEL_MISSING` | kit/canon/KERNEL.md is absent. |
| `GDH_KERNEL_BUDGET` | KERNEL.md exceeds budgets.kernelLines. |
| `GDH_MOMENTS_BUDGET` | The rendered MOMENTS.md exceeds budgets.momentsChars. |
| `GDH_MOMENT_SHAPE` | A moment has no 'when', a repeated 'when', or neither start nor offer. |
| `GDH_MOMENT_OFFER_LIMIT` | A moment offers more than 3 skills. |
| `GDH_MOMENT_SKILL_UNKNOWN` | A moment names a skill that is neither registered nor wired. |
| `GDH_MOMENT_START_USER` | A moment starts a skill that is not model-invoked. |
| `GDH_CAPABILITIES_SCHEMA` | capabilities.json is absent or malformed. |
| `GDH_CAPABILITIES_DISCIPLINE` | A discipline in capabilities.json names an unregistered skill. |
| `GDH_TOOL_FIELD` | A tool entry lacks a required field or a field has the wrong type. |
| `GDH_TOOL_ENUM` | A tool entry has a kind, auth or evidence value outside the allowed set. |
| `GDH_TOOL_ID` | A tool id differs from its file name or is not kebab-case. |
| `GDH_TOOL_CAPABILITY` | A tool names a capability outside the vocabulary. |
| `GDH_TOOL_DISCIPLINE` | A tool names a discipline that capabilities.json does not hold. |
| `GDH_TOOL_FALLBACK` | A tool fallback is neither an existing tool id nor 'none'. |
| `GDH_TOOL_CARD` | A tool card path is wrong or the card file is absent. |
| `GDH_TOOL_DATE` | A tool verifiedAt value is not an ISO date. |
| `GDH_TOOL_SOURCE` | A tool source is neither an https URL nor 'none'. |
| `GDH_ASSETS_FIELD` | assets.json is malformed or a source lacks a required field. |
| `GDH_ASSETS_DUPLICATE_ID` | Two asset sources share one id. |
| `GDH_ASSETS_DATE` | An asset source verifiedOn value is neither null nor an ISO date. |
| `GDH_ASSETS_URL` | An asset source url is not an https URL. |
| `GDH_BRAND_PACK` | A brand pack lacks README.md or tokens.json. |
| `GDH_BRAND_PUBLIC` | A private brand pack is not git-ignored, or a tracked .gitignore names one. |
| `GDH_HOOK_BUDGET` | KERNEL.md and the rendered MOMENTS.md together exceed the SessionStart hook limit. |
| `GDH_EVAL_CASE` | An eval case lacks a field, has a wrong kind, id or skill, or expects the wrong skills. |
| `GDH_GENERATED_DRIFT` | A generated file differs from the build output. |
| `GDH_ACCEPTED_INVALID` | A kit/scan.accepted.json entry is malformed or waives more than one finding. |

`doctor` codes are advice. They never fail `check`.

| Code | Advice |
| --- | --- |
| `GDH_DOCTOR_STALE` | A tool entry was verified more than 180 days ago. |
| `GDH_DOCTOR_UNTESTED` | A tool entry has the evidence label UNTESTED. |
| `GDH_DOCTOR_NO_CARD` | A tool has no card file. |
| `GDH_DOCTOR_CAPABILITY_NO_TOOL` | A capability has no tool in the catalog. |
| `GDH_DOCTOR_GATE_UNVERIFIED` | A capability that a gate depends on has no VERIFIED tool. |
| `GDH_DOCTOR_NO_EVAL` | A model-invoked skill has no triggering eval case. |
| `GDH_DOCTOR_NO_REFINEMENT_LOG` | A skill has no refinement-log.md. |

Rules of use:

- Fix a finding at its cause. Shorten a long `SKILL.md` by moving depth into a reference. Repair a link. Register a stray folder or remove it.
- [kit/scan.accepted.json](../kit/scan.accepted.json) holds accepted findings as `{code, path, reason}`, plus `match` where the code needs it. It is empty. Add to it only for a true false positive.
- A waiver of `GDH_SECRET`, `GDH_PRIVATE_LINK` or `GDH_SCRIPT_NETWORK` names one exact path and repeats the finding's `match` value, the sha256 of the matched line. A waiver of `GDH_SYMLINK` or `GDH_BRAND_PUBLIC` names one exact path. A glob is refused for these five codes. A pattern that matches the whole repository, such as `*`, is refused for every code. `GDH_ACCEPTED_INVALID` cannot be waived.
- Example waiver: `{"code": "GDH_SECRET", "path": "kit/references/tools/<id>.md", "match": "<sha256 from check --json>", "reason": "<why it is a false positive>"}`.
- The link rule covers `kit/` and `docs/`. It skips `kit/templates/`, because template links point at project paths. It skips links inside code.
- The secret rule looks for key and token shapes, email addresses and id-like strings. It cannot recognize a client name.

## 4. Catalogs

| File | Holds | Rule |
| --- | --- | --- |
| [capabilities.json](../kit/catalogs/capabilities.json) | The fixed capability words. For each discipline: the owning skill and the capabilities it may use, in preference order. | A new word needs the owner's yes. |
| `kit/catalogs/tools/<id>.json` | One tool: kind, capabilities, install, auth, `spendsCredits`, `exposes`, `readOnly`, `toolPrefix`, `firstCall`, `fallback`, card, source, `verifiedAt`, `evidence`, `evidenceNote`. | `id` equals the file name. Every capability is in the vocabulary. |
| `kit/references/tools/<id>.md` | The card: twelve headings from "What it makes" to "Evidence". | Own words. No price that goes stale. |
| [assets.json](../kit/catalogs/assets.json) | Free asset sources: group, what it holds, license, attribution, commercial use, fetch route, risk, `verifiedOn`. | `verifiedOn: null` means the license page was not read. `find-assets` reads it before any use. |

How a skill uses them: it names a capability; the agent lists the tools that hold it, confirms one is present in the session by its `toolPrefix`, reads the card, calls the `firstCall`, and falls back by the `fallback` id when the tool is absent. A skill body names a tool only as an example.

`exposes` means the tool can publish, share or upload outside the project. `spendsCredits` means some call can use credits or a paid quota. When in doubt, both are true.

## 5. Evidence labels, gates and defaults

| Label | Meaning |
| --- | --- |
| VERIFIED | Someone exercised it and saw the result. The note says what and when. |
| DOCUMENTED | A primary source states it. Nobody exercised it here. |
| UNTESTED | It comes from memory, a secondary page or a rule of thumb. |

- A gate blocks delivery. A gate carries a number only when the number is verified or is the published accessibility floor, which is labelled DOCUMENTED. Gates with no number need no source: brief exists, direction chosen, license read, quote shown, record written.
- A default starts with "Default:". The user, the design system or the brief can replace it.
- A research fact marked unverified, from memory or as a rule of thumb is always a default.
- The full rules are in [PRINCIPLES.md](../kit/canon/PRINCIPLES.md), sections 4 and 5.

## 6. How to add a tool

The `add-design-tool` skill is the procedure. In short:

1. Name the capability. Search the catalog. Stop when a present tool already covers the need.
2. Vet the tool: publisher, license, maintenance, auth, cost model, exposure.
3. `python3 scripts/gdh.py new-tool <id> --name "<Name>" --kind <kind> --capabilities <list> --source <https URL>` and the flags `--spends`, `--exposes`, `--read-only` as they apply.
4. Fill the entry and the twelve card sections. Set the label to DOCUMENTED.
5. Make one real free call. Write what ran into `evidenceNote`. Raise the label to VERIFIED only for what ran.
6. Add a card link to a skill's Tools table only when the tool is a good example for that capability.
7. `build`, `check`, the tests, `doctor`. Log the change.

An asset source is one new object in `assets.json`. Set `verifiedOn` only after you read the license page.

## 7. How to add a skill

Add a skill only when no skill composes the behavior and a reference file cannot carry it.

1. `python3 scripts/gdh.py new-skill <name> --invocation user --discipline <d> --description "<what it does and when to use it>"`.
2. Write the body in the eight fixed sections: purpose and boundary, Before you start, Procedure, Tools, Checks, Output, References, Sources.
3. Mark user decisions with "ASK:" and spend or exposure points with "GATE:".
4. Put depth in `references/`. Link each file from `SKILL.md` and say when to read it.
5. Name the skill in `ask-gdh`. `check` reports a skill the router does not name.
6. Prefer user invocation. A model-invoked skill spends the shared description budget and needs two triggering eval cases.
7. Add the discipline to `capabilities.json` when it is new.
8. `build`, `check`, the tests. Add a line to the changelog.

## 8. How to add a brand pack

```
DS="python3 kit/skills/design-system/scripts/ds.py"
$DS init      brands/<slug> --name "<Name>"
$DS validate  brands/<slug>/tokens.json
$DS contrast  brands/<slug>/tokens.json
$DS export    brands/<slug>/tokens.json --css brands/<slug>/tokens.css
$DS design-md brands/<slug>/tokens.json --readme brands/<slug>/README.md -o brands/<slug>/DESIGN.md
$DS specimen  brands/<slug>/tokens.json -o brands/<slug>/specimen.html
```

1. Replace the starter values and every TODO. `tokens.json` is the source; the CSS and `DESIGN.md` are generated.
2. Give every token a usage note. A text color names the grounds it reads on; `contrast` reads pairs from those notes.
3. Record where each value came from in `SOURCE.md`. A value with no source is INFERRED and waits for the owner.
4. Record each asset's source and license before use.
5. `check` requires `README.md` and `tokens.json` in each pack folder.
6. This public repository carries the fictional example pack and the template only. The owner's private packs may sit under `brands/` in a local working copy. `.gitignore` ignores every folder there except the template and the example, so a new pack needs no edit. No tracked file names a private pack; `check` reports `GDH_BRAND_PUBLIC` when one does. Put an extra local rule in `.git/info/exclude`. `check` validates every pack present on disk, private or public. See [brands/README.md](../brands/README.md).

## 9. How to add a capability

1. Check that no existing word covers the tool.
2. Get the owner's yes. The vocabulary is fixed on purpose.
3. Add the word to `capabilities.json` and to the capability list of the discipline that will use it.
4. Mention it in that skill's Tools section.
5. `doctor` reports a capability with no tool. Add the tool entry.

## 10. Export

`python3 scripts/gdh.py export --repo <project> --hosts claude,codex,cursor,agents` copies the kit into a project.

- Skills go to `.claude/skills` for the `claude` host and to `.agents/skills` for the others. The catalogs, cards and canon go beside each skills folder, so that relative links still resolve. Subagents go to `.claude/agents`.
- A managed block is written into `AGENTS.md` between two marker lines. Its first line is the entry rule: start every design-led session with the skill that the first moment starts, now `align`. Then it holds the kernel and the moments. Text outside the markers is kept.
- For the `claude` host, a second managed block in `CLAUDE.md` imports `AGENTS.md`, because Claude Code reads `CLAUDE.md` and skips `AGENTS.md` when both exist. When `CLAUDE.md` already imports `AGENTS.md`, no block is added. Evidence: DOCUMENTED for the import rule; VERIFIED for the file the export writes (unit tests).
- Project templates are added and never overwrite an existing file. A template has `status: template` in its front matter, and every skill treats such a file as absent.
- `.agents/gdh/manifest.json` records what GDH wrote, with hashes. A second run changes nothing. A copied file that a person edited is a conflict and is kept. `--replace-edited` copies it to `.agents/gdh/backups/<UTC time>/` and replaces it. A file GDH did not write is a conflict; `--force` backs it up the same way and replaces it, and it also replaces every edited GDH file. A managed block that a person edited is backed up the same way and then rewritten. A manifest key outside the managed folders is refused and never removed. No write goes through a symbolic link.
- `--json` gives machine output, as for every other subcommand.

## 11. Evals

`evals/cases/triggering/` holds one JSON file for each case. `evals/cases/quality/` holds the labelled corpus that `evals/quality.py` scores in the unit suite. `check` validates the form: the id equals the file name, the skill is model-invoked or `none`, and `expect.skills_fired` holds the skill. GDH ships no runner. See [evals/README.md](../evals/README.md).

## 12. Hooks

[kit/hooks/hooks.json](../kit/hooks/hooks.json) registers three hooks. Each runs as `python3 -I -S "${CLAUDE_PLUGIN_ROOT}/hooks/<file>"`, so no module loads from the project folder. The two enforcement commands end with `|| true`, so a launch failure exits 0 and never reads as a block. The reasons are in [ADR 0006](adr/0006-hooks-scan-edits-and-gate-the-stop.md).

| Hook | Event | Does | Blocks |
| --- | --- | --- | --- |
| `session_start.py` | SessionStart | Prints the kernel, then the moments, 9,000 characters at most. | Never |
| `post_edit.py` | PostToolUse, matcher `Write\|Edit\|MultiEdit` | Scans the edited file with `tells.py --json`, with `design/tokens.json` and `DESIGN.md` when they exist. On a markup file it also runs `originality.py check` when that script exists. Returns the top findings as `additionalContext`, 12 lines at most, and asks the agent to review each one: fix it or record a brand-required reason. | Never |
| `stop_gate.py` | Stop | Holds the stop with `decision: "block"` when a design file that this session edited changed after the newest passing verdict in `design/reviews/`, or, with no passing verdict, changed in the last 24 hours. | Once per turn, until a passing verdict or today's override exists |

Rules of the two enforcement hooks:

- They act only when the project has a `design/` folder. The search runs from `cwd` up to the git root. Without a git root, only `cwd` counts.
- Design files have the extensions `.html`, `.htm`, `.css`, `.scss`, `.jsx`, `.tsx`, `.svg`, `.vue` and `.svelte`. Markup files are the same list without `.css`, `.scss` and `.svg`.
- Every dot-folder is skipped, and so are `node_modules`, `dist`, `build`, `coverage`, `htmlcov`, `out`, `storybook-static`, `vendor` and `target`. Files in `design/reviews/` never count as design changes.
- The Stop hook reads `transcript_path`, and the subagent transcripts in `<transcript stem>/subagents/`, for Write, Edit and MultiEdit calls on design files inside the project. A session with no such call is never held.
- When the transcript cannot be read, the Stop hook walks the project, but only when `design/brief.md` exists. Default: the walk looks at 2,000 files at most.
- A passing verdict is a line `Originality: original` or `Originality: watch` in a file under `design/reviews/`. A derivative verdict does not pass. The block reason names the review file `design/reviews/<today>-originality.md`.
- A file time more than 60 seconds in the future is ignored. Default: 60 seconds.
- The block fires once per turn. On the retry `stop_hook_active` is true and the stop goes through. The reason says: when this turn hands over a draft for feedback rather than finished work, say so in one line and stop; before calling the design done, run the gate. It tells the agent to start the `originality-gate` skill and gives the absolute path of its `SKILL.md` as a fallback.
- The reason echoes 5 file names at most. Control characters are stripped and each name is cut to 120 characters.
- The override is one line in `design/decisions.md`: `Override: originality-gate <YYYY-MM-DD> <reason>`. Only a line dated today with a reason counts.
- Both fail open: any error, a timeout or a missing script gives exit 0 and no output. Default: 8 seconds of work for each. The registered timeout is 15 seconds.
- `GDH_PLUGIN_ROOT` overrides the plugin folder that `post_edit.py` reads the scan scripts from. The tests point it at stub scripts. `GDH_HOOK_TIMEOUT` sets the time budget of both hooks in seconds, for tests and local runs.
- Tests: `tests/test_hooks_post_edit.py` and `tests/test_hooks_stop_gate.py` run each hook as a subprocess with crafted input and transcripts, and run the registered command strings through a shell.
- Evidence: the input and output fields follow the Claude Code hooks reference, DOCUMENTED on 2026-11-27. The transcript shape (`tool_use` entries with `name` and `input.file_path`) was VERIFIED against one real Claude Code transcript on 2026-11-27. The unit tests are VERIFIED. No live session has run the two new hooks yet; that is UNTESTED.

## State on 2026-11-23

Commands run from the repository root on 2026-11-23, after the final integration pass (privacy fix of the ignore file, kernel rule 16, the capture route, the quality corpus and the rebuilt example pack).

```
$ python3 scripts/gdh.py build
build: 0 file(s) written, 7 unchanged

$ python3 scripts/gdh.py check
check: 0 finding(s), 0 accepted

$ python3 -m unittest discover -s tests
Ran 452 tests
OK

$ python3 scripts/gdh.py doctor
asset sources with verifiedOn null: 66 of 174 (read the license page before use)
doctor: 0 warning(s) on 2026-11-23

$ python3 evals/quality.py
pages: recall 0.83, precision 0.83
```

What the numbers are:

| Measure | Value | Limit |
| --- | --- | --- |
| Skills | 26 (6 model-invoked, 20 user-invoked) | none |
| Model-invoked description text | 3,328 characters | 5,000 |
| Kernel | 46 lines, 17 rules (0 to 16) | 60 |
| Moments text | 2,816 characters | 3,500 |
| Skill reference files | 171, plus 6 protocols | 400 lines each |
| Tool entries and cards | 32 and 32 | none |
| Tool evidence | 2 VERIFIED (`headless-browser`, `21st-dev`), 30 DOCUMENTED, 0 UNTESTED | none |
| Capability words | 30, each with one tool or more; `capture` has a VERIFIED tool | none |
| Asset sources | 174; license page read for 108, not read for 66 | none |
| Triggering eval cases | 17: four for `align`, three for `ask-gdh`, two for each other model-invoked skill, and two negative | none |
| Quality corpus | 10 labelled pages (3 first-wave generic, 3 second-wave generic, 1 brand-required, 3 distinctive) and 3 labelled mood boards | baseline in `labels.json` |
| Finding codes | 52 `check` codes, 7 `doctor` codes | none |
| Unit tests | 452, all passing | none |
| Brand packs on disk | The example, the template and private packs that the `brands/*` ignore rule keeps out of the public tree | none |
| Accepted findings | 0 | none |

How to read the doctor result. Zero warnings means: no catalog entry is older than 180 days, no entry is labelled UNTESTED, every tool has a card, every capability has a tool, the `capture` capability has a VERIFIED tool, every model-invoked skill has an eval case, and every skill has a refinement log. It does not mean that the tools work. Thirty of 32 entries are DOCUMENTED: read, not run.

Smoke tests run the same day, all with exit code 0 unless stated:

- `ds.py validate` on every `brands/*/tokens.json`: 0 errors and 0 warnings in each pack on disk.
- `ds.py contrast` on every pack. The template and the example: 22 checks, 0 failed. The private packs exit 1 on purpose: 9, 3, 9 and 4 checks fail. Each failing pair is a brand source value, kept exact and flagged in its usage note and the pack README.
- `ds.py export`, `design-md` and `specimen` regenerated the example pack after its rebuild. The unit tests confirm the committed files match the generator.
- `ds.py audit` on the example `sample.html` and `specimen.html`: 0 raw literals.
- `tells.py` on each pack specimen with its tokens and `DESIGN.md`, and on the example `sample.html`: 0 findings. Brand-required notes: 2 for one private pack (a gradient its tokens name), 0 for the example.
- `evals/quality.py`: page recall 0.83, page precision 0.83. Per-rule scores are in `kit/skills/design-critique/refinement-log.md`. All three labelled boards gave the labelled verdicts.
- `moodboard.py build` and `diff` on its template: 3 directions, 3 distinct pairs, 0 errors, 8 warnings (the template status, one accent that is for fills only, six example reference files that do not ship).
- Local capture: Playwright 1.63 and headless Chrome captured the example specimen and `sample.html` at 390, 1024 and 1440 px, light and dark. The captures were viewed. No network was used.
- `gdh.py export` into an empty folder for all four hosts: 620 changes. A second run: 0 changes, 620 unchanged. The managed `AGENTS.md` block opens with the `align` rule and holds rule 16; `CLAUDE.md` imports it.

Not verified in this build:

- No live plugin install on any host. `claude plugin validate` was not run. The Codex manifest shape and its hook support are UNTESTED; the hook command reads a Claude variable.
- No eval runner. The triggering cases are validated for form only. No model has run them.
- No spend call on any tool. No image, vector, video, audio, 3D or component retrieval was generated.
- Python 3.9 was not run. The scripts were tested on Python 3.13 only.
- The owner's asset library (DAM) and the reverse-engineering server (REA) are DOCUMENTED from their repository documents, not exercised.
- No screen reader, no real device and no keyboard pass on any page. Captures show layout and color only.
- The example pack's IBM Plex faces were checked as loaded in one headless Chrome render on 2026-11-23. No other browser was tried.

History of this state. The first build pass left 11 registered skills with no `SKILL.md`, four linked reference files absent, two reference files with wrong card links, and no example brand pack. The first integration pass wrote them. The second pass rewrote the eleven skills to full depth and added `align`. The final pass fixed the review findings listed in this file and in `CHANGELOG.md`.

## Open work

This list is the honest state of the harness. It comes from the research review and from the build. Items are in priority order.

**Blocker before the first push.** Earlier commits on this unpushed branch hold a `.gitignore` that named the owner's private brand folders. The working tree no longer names them: the ignore file is now a `brands/*` allowlist, and `check` reports a tracked ignore file that names a private folder. The history still does. Before the first push, squash the branch or rewrite `.gitignore` out of every commit, then confirm with a search of the full history that no private folder name remains. The build agents run no git, so this step is the owner's.

1. **Exercise the tools.** No tool was called with a spend call and no design was built. Run one small, owner-approved job for each key connector: an image and a vector, a local video render, a component retrieval, a model. Record time, output format, link lifetime and quality. Until then the video, mood-board and vector routing rules are proposals.
2. **Connect the owner's asset library and the reverse-engineering server.** Both cards were written from repository documents. Start both servers, read the live tool lists, and confirm what an agent sees in owner mode.
3. **Read the primary sources for every gate number.** WCAG 2.2, the Core Web Vitals pages, the Apple and Material guidelines. The contrast floor is labelled DOCUMENTED and other values are defaults until someone reads them.
4. **Avatar video.** The owner named a presenter-video tool. Only the HTML video product of that vendor was researched. Find out whether an avatar connector exists for the account, and write its card.
5. **A test for "unique" and "high-level".** A first regression guard exists: the quality corpus in `evals/cases/quality/` (10 pages, 4 boards, one reviewer). It is small and labelled by one person. Grow it, add a second labeller, and add rules for the second-wave templates that score 0 today (cream and terracotta, tinted near-black with one orange accent, bento grids). Fix the known misses: invented figures without a currency or plus sign, glass on four surfaces, invented testimonial names, plain stat rows, and emoji inside chat messages. The pastel radius miss was fixed on 2026-11-23. Read the full tell catalog and the severity bands of the critique rubric that the tell list draws on.
6. **Claude Design after 2026-12-14.** What the sync and login commands target after the standalone site closes; the exact handoff bundle format; how an agent gets a "Send to" link without the user's click. The date is close.
7. **Migrated design systems with no token file.** Decide with the owner whether GDH converts them. Until then they cannot feed a canvas, a deck or a data page automatically.
8. **Logo method from primary sources.** Vector construction, optical correction, grid use, and a trademark screening route.
9. **3D budgets.** Take them from a primary source or from measurement. Test the path from a generated mesh to an optimized file.
10. **Video platform specifications.** Read each platform's own help page for sizes, safe areas, length and disclosure rules.
11. **Asset license verification.** 66 of 174 catalog sources are unverified. Read the license pages of the high-use ones first. Write a search procedure for sources outside the catalog.
12. **Host portability.** Verify the Codex manifest and install commands against official documentation. Verify how Cursor treats `AGENTS.md` and a skills folder. Test whether one hooks file serves two hosts. Test a skill upload to the Claude apps with the extra frontmatter fields.
13. **Connectors that were blocked or partial.** Reconnect the ones whose sign-in lapsed, and read the ones whose core tools, plan or guide text were not available.
14. **General chart and dashboard sources.** Read the primary chart guidance directly, and read the host's own chart skill so that GDH does not contradict it.
15. **Vendor design references.** One media connector ships its own design recipe, review rubric and brand references. They are unread and may conflict with GDH rules.
16. **Decision record in use.** The entry format is fixed, but no project has used it yet. Check it after the first three projects.
17. **Project-level cost control.** No ledger covers credits across connectors. `generate-media` keeps a running total in its prompt sheet; that is all.
18. **Client data handling.** No card states how long a connector keeps an uploaded file. Uploads stay behind the exposure gate until this is known.
19. **Run the GCH side.** The GCH changes in [HANDOFF-GCH.md](HANDOFF-GCH.md) are a proposal. Apply them in that repository and run its own checks.
20. **Typography depth.** The pairing method, variable fonts and non-Latin scripts rest on thin sources.
21. **Mood board method from a primary source.** The stylescape method is known from secondary pages only.

Added by the build:

22. **Second review of eleven skills.** `dashboard-design`, `data-viz`, `network-graph`, `infographic`, `ui-motion`, `motion-video`, `three-d`, `generate-media`, `claude-design`, `handoff-to-code` and `add-design-tool` were rewritten to full depth in the second pass, each by one author. Their command syntax (3D, video and motion tools) was written from memory and is labelled UNTESTED. Review each against its research, and run each command's help before relying on it.
23. **An eval runner.** The cases are validated for form only. No run has shown that a skill starts on its prompts.
24. **Python 3.9.** The scripts were run on one newer version only.
25. **Brief check script.** A script that validates `design/brief.md` would make the brief gate machine-checkable.
26. **Publish and sync of a design system.** The two protocols are DOCUMENTED and were never run against a live account.
27. **License.** The repository is `UNLICENSED`. The owner chooses a license before others may reuse it.
28. **Run `align` with a real user.** The interview, its question caps and the `gch:grilling` hand-off have not met a person. Run one tier-one and one tier-two session and log what the interview missed.
29. **Fallback loops in the tool catalog.** Fixed on 2026-11-23. The critique chain ends at `vercel-web-design-guidelines` and the whiteboard chain ends at `tldraw`, each with `none`, and each card says so. Every fallback chain now ends in `none`. No `check` rule fails on a new loop yet; add one in `scripts/gdh.py`.
30. **Example pack font files.** Done on 2026-11-23. The example ships five Latin-1 WOFF2 files and `OFL.txt` from IBM's own Plex packages; `SOURCE.md` records the package versions and the sha256 of each file. A browser render of the specimen with the faces loaded is still UNTESTED.
31. **Skipped files in the tell scan.** `tells.py` exits 0 when some files are skipped as too large and others are scanned. The skipped files are listed, but the exit code does not show them. Decide whether a partial skip should exit 2.
32. **A route check for user-invoked skills.** Done on 2026-11-23. The kernel states the handoff route once: read the skill's `SKILL.md`, or print `/gdh:<name>`. `GDH_ROUTE_USER_SKILL` fails when the kernel lacks that line, and when a kit line says start, invoke, launch or trigger for a user-invoked skill without the route on the same line. Lines that say "run" rely on the kernel line.
33. **An export option for the SessionStart hook.** Not built. The `CLAUDE.md` import already loads the kernel in an exported project, and writing a user's `.claude/settings.json` is a larger change. Revisit if the import proves unreliable.
34. **The Codex hook.** The hook command reads `CLAUDE_PLUGIN_ROOT`. Confirm what Codex sets, and give Codex its own command if it differs.
