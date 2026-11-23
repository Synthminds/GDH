# Changelog

Format: one section for each release, newest first. A catalog-only change is a patch. A new skill or a new capability word is a minor change. A change to the kernel or to the registry schema is a major change.

## Unreleased

### Added

- `align`, a model-invoked skill that opens every GDH session. Without a confirmed `design/brief.md` it runs the full interview, one question at a time with a recommended answer, scaled to the job size. With a confirmed brief it re-aligns in a few questions. `--full` forces the full interview. It hands its questions to `gch:grilling` only when that skill declares the `caller contract`. The kit now holds 26 skills, six of them model-invoked.
- Kernel rule 0: align first. The first moment starts `align`; `ask-gdh` routes only after `align` closes.
- `brands/README.md`: what a brand pack is, the example pack, the template, and how to make a pack with the `design-system` skill.
- Kernel rule 16: derive from the subject. Every visible choice traces to the brief or the subject's world, and open choices face the swap test.
- `app-design/references/character.md`: where an app's character lives, how to restyle a component library off its stock theme, the swap test for screens, and a worked example.
- Tool entry and card `headless-browser`: local full-page captures with Playwright or Chrome, the first VERIFIED provider of `capture`.
- `gdh.py doctor` reports `GDH_DOCTOR_GATE_UNVERIFIED` when a capability that a gate depends on has no VERIFIED tool.
- The quality corpus `evals/cases/quality/` and the scorer `evals/quality.py`: ten labelled pages and three labelled mood boards, scored in the unit suite against a recorded baseline.
- The triggering case `trigger-ask-gdh-feedback`: feedback on the look of earlier GDH work starts `ask-gdh`.
- `brands/example-harbor-lantern/sample.html`: one screen built only from the pack's tokens.

### Changed

- Rewrote eleven skills to full depth: `network-graph`, `data-viz`, `dashboard-design`, `infographic`, `ui-motion`, `motion-video`, `three-d`, `generate-media`, `claude-design`, `handoff-to-code`, `add-design-tool`. Each change is logged in the skill's `refinement-log.md`.
- `design-brief` gave its interview to `align`. It keeps the brief format, the status line, the persona form and the fidelity ladder.
- `gdh.py export` opens the managed `AGENTS.md` block with the entry rule: start every design-led session with the skill that the first moment starts, now `align`. The block no longer says to start with `ask-gdh`.
- `.gitignore` ignores every folder under `brands/` except `README.md`, `_template/` and the example pack. A private pack needs no edit to a tracked file, and no tracked file names one. `gdh.py check` validates each pack present on disk and reports `GDH_BRAND_PUBLIC` when a tracked ignore file names a private folder.
- The project handoff template carries the subsections that `handoff-to-code` fills: components with props, the screen state matrix, layout and breakpoints, content and the copy deck, and the AI runtime sheet.
- `PRINCIPLES.md` records the exit-easing resolution from `ui-motion`.
- The example brand pack was rebuilt from its subject: chart white, wet slate, and navigation-light green and red replace the cream and orange template; IBM Plex faces replace a system stack. `SOURCE.md` traces each choice. The pack ships six IBM Plex WOFF2 files and `OFL.txt` from IBM's own packages, declared in `type.fonts` and loaded by `@font-face` in `tokens.css`, the specimen and the sample.
- The Codex manifest names one skills folder and the hooks file, as its schema documents.
- The design-brief moment no longer fires when `align` closes, because `align` already hands its record to `design-brief`.
- The offer text, `PRINCIPLES.md` and the README name how `ask-gdh` starts a user-invoked skill: it reads that skill's `SKILL.md`.
- The Higgsfield card treats a generated SVG as a logo concept for `logo-identity`, never as the master.
- Capture examples in `design-critique`, `accessibility-gate`, `website-design` and `handoff-to-code` point at the `headless-browser` card; the `vercel` card covers deploy only.
- Motion examples in `ui-motion` and `motion-video` use invented round values instead of values from private brands.
- The public tree holds no link and no install line for the owner's private repositories. `kit.json` no longer wires `gch`; `requires.gch` keeps only an optional note. The DAM tool entry has `source: "none"`, which `GDH_TOOL_SOURCE` and `new-tool --source` now accept for a tool with no public page.
- `GDH_PRIVATE_LINK` also reports a link or a marketplace line for another repository of the kit's owner, read from `kit.json` `repository`. A public sibling takes an exact-path waiver.
- The kernel states the skill handoff route once: read a user-invoked skill's `SKILL.md`, or print `/gdh:<name>`. The new code `GDH_ROUTE_USER_SKILL` fails when the kernel lacks it, or when a kit line starts a user-invoked skill by name without it. Two mood-board lines now give the route.
- `tells.py` counts the elements that a style-block radius rule matches, so `TELL_UNIFORM_RADIUS` finds the pastel template. Its quality baseline rose from 0.0 to 1.0, and `evals/quality.py` closes the files it reads.
- The `app-design` prototype purpose template is in the kit's own words.

## 0.1.0 (2026-11-23)

First version of the Global Design Harness.

### Review fixes

- The adversarial review findings were fixed across the kit, the docs and the catalogs. Every pointer to a missing brief now names `align`, with a named trigger for a re-entry. Every `SKILL.md` uses one tool-pick lead-in (kernel rule 8, then the card) and one `Defaults` lead-in. Each description sentence holds 20 words or fewer, with no colon inside. Consent entries in `three-d` and `motion-video` use the fixed decision-record format of `generate-media`. Alignment entries are `round 0`, and `refine-round` skips them when it counts. The handoff template and `handoff-to-code` use the same subsection names. `design-system` and `design-critique` document the `--force` flags and the `tells.py` exit codes. The waiver shape with `match`, and the export conflicts, backups and `CLAUDE.md` import, are documented as the code behaves. "GATE:" now marks only spend and exposure; "STOP:" marks other blocking preconditions. Every tool fallback chain ends in `none`. The `design-critic` agent uses the skill's finding shape, cap and verdict names. `docs/HANDOFF-GCH.md` names the real GCH targets, the feedback rule and the `caller contract` marker. `color` and `typography` gained a worked example for an abstract subject. `tells.md` lists the second-wave rules. The generate-media "media brief" is now the "prompt sheet".

### Added

- The kernel: 15 always-on rules, with precedence, the spend gate, the exposure gate, the license rule, the accessibility floor and evidence labels. A SessionStart hook prints it with the moments text.
- 25 skills. Model-invoked: `ask-gdh`, `design-brief`, `mood-board`, `find-assets`, `design-critique`. User-invoked: `design-system`, `typography`, `color`, `logo-identity`, `website-design`, `app-design`, `dashboard-design`, `data-viz`, `network-graph`, `infographic`, `ui-motion`, `motion-video`, `three-d`, `generate-media`, `reverse-engineer-reference`, `claude-design`, `refine-round`, `accessibility-gate`, `handoff-to-code`, `add-design-tool`.
- Four subagents: `art-director`, `design-critic`, `asset-scout`, `a11y-auditor`.
- The capability vocabulary and the discipline routing table.
- A tool catalog with one entry and one card for each tool, each with an evidence label.
- An asset-source catalog with license notes. Sources whose license page was not read carry `verifiedOn: null`.
- Scripts, standard library only: `ds.py` (design systems in the Claude Design System token shape), `moodboard.py`, `tells.py`, `assets.py`.
- The engine `scripts/gdh.py`: `check`, `build`, `export`, `doctor`, `new-tool`, `new-skill`.
- Project templates: `DESIGN.md`, `design/brief.md`, `design/decisions.md`, `design/handoff.md`, `design/assets/manifest.json`.
- The example brand pack `brands/example-harbor-lantern/` for a fictional brand, and `brands/_template/`.
- Triggering eval cases: two for each model-invoked skill and two negative cases.
- Documents: architecture and maintenance, the GCH hand-off, sources, four decision records.

### Known limits

- No tool was exercised with a spend call. Nearly every tool card is DOCUMENTED, not VERIFIED.
- No design was built with the kit before release. Output quality is UNTESTED.
- No eval runner exists in this repository. The eval cases are validated for form only.
- Plugin installs on Claude Code and Codex were not run. The export route is the tested one.
- Eleven skills and four reference files were written in the integration pass, after the first build pass left them absent: `dashboard-design`, `data-viz`, `network-graph`, `infographic`, `ui-motion`, `motion-video`, `three-d`, `generate-media`, `claude-design`, `handoff-to-code`, `add-design-tool`. They had one author and no second review.
- The full list is in `docs/GDH.md`, section "Open work".
