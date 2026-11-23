# Impeccable

Catalog entry: [impeccable.json](../../catalogs/tools/impeccable.json). Source: https://github.com/pbakaus/impeccable

Impeccable is an agent skill by Paul Bakaus, not an MCP connector. License: Apache-2.0. Version read: 4.10.0. GDH offers it and does not copy it, because it installs a launcher binary and hooks.

Terms in this card. A command is one verb after `/impeccable`. The detector is the standalone rule scanner. The craft floor is the skill's list of checks and refusals. A tell is a visual habit that marks work as generic AI output.

## What it makes

- Reviews and edits of interface code: web pages, app screens, dashboards, and native iOS and Android screens.
- A scored design critique, and a technical audit ranked P0 to P3.
- Single-axis passes: type, color, layout, motion, copy, responsive behavior, edge cases.
- `PRODUCT.md` and `DESIGN.md` written from the project and its code.
- A deterministic scan for tells, with no model in the loop.
- It makes no logo, illustration, 3D model, video or audio.

## Connection and auth

- No account and no key. Check the skill list for `impeccable` before you route to it.
- ASK before any install. Name the hooks and the binary in the question.
- Claude Code: `/plugin marketplace add pbakaus/impeccable`, then install from `/plugin`.
- Any host: `npx impeccable install`. It detects hosts, asks project or global, and offers the hook. Update with `npx impeccable update`.
- Codex uses the prefix `$impeccable`. Codex needs the hook approved in `/hooks` after every update that changes it.
- A manual copy or the VS Code extension installs the skill without the hook.
- The repository also holds an optional `impeccable mcp` server that signs in to an account service. Research did not confirm what it unlocks. Do not register it without the owner's decision.
- Default: pin the install by npm version (for example `impeccable@4.10.0`). The marketplace line installs current upstream.

## Cost model

- Free and open source. No call spends credits. No quote tool exists and none is needed.
- The detector uses no model and no API key. The only cost is the agent's own tokens.
- The Stop hook and the edit hook add turns and time to a session.

## Call order

1. Run `/impeccable init` once for each project. It writes `PRODUCT.md`: users, purpose, constraints, brand commitments.
2. For existing code, run `/impeccable document`. It writes `DESIGN.md` from the code.
3. The skill runs `scripts/impeccable context` once in each session. It loads `PRODUCT.md`, `DESIGN.md`, the surface brief and native guidance.
4. Run one command with a target: a file path, a component name or a route.
5. The skill loads one playbook for the command. It reads the craft floor just before any interface edit.
6. The skill checks the render with `scripts/impeccable shot <page>`.

If the launcher fails, the skill says so once, reads `PRODUCT.md` and `DESIGN.md` directly, and continues. A launcher failure does not block the work.

## Key tools

| Command | Use it when |
|---|---|
| `init`, `document` | A project has no `PRODUCT.md`, or has code but no `DESIGN.md`. |
| `shape [feature]` | You plan the UX and UI of a new feature before code. |
| `critique [target]` | You need a scored review. Two isolated sub-agents run a design review and a detector pass, then merge. |
| `audit [target]` | You need a technical report: accessibility, performance, theming, responsive. |
| `polish [target]` | You run the last pass before ship. |
| `typeset`, `colorize`, `layout` | One axis is weak: type hierarchy, color or spacing rhythm. |
| `bolder`, `quieter`, `distill` | The page is too safe, too loud or too busy. |
| `animate`, `delight`, `overdrive` | You add purposeful motion, personality or ambitious effects. |
| `harden`, `adapt`, `clarify`, `onboard`, `optimize` | Edge cases and i18n; screen sizes; UX copy; first-run and empty states; render performance. |
| `live`, `generate [n] [action] [element]` | You iterate variants of one element in the browser. Accepted variants write back to source. |
| `extract [target]` | You pull repeated tokens and components into the design system. |
| `npx impeccable detect <path or url>` | You need the rule scan alone, for example in CI. Flags: `--json`, `--github`, `--sarif`, `--list-rules`. |

Other verbs: `hooks` (on, off, status, ignore rules), `doctor` (artifact drift), `foundations`, `pin` and `unpin`. `teach` is an alias of `init`. `craft` is a deprecated alias. `normalize` and `teach-impeccable` do not exist in this version.

## Inputs

- Product context for `init`: who uses the product, what it must do, constraints, brand commitments.
- A target for each command.
- A runnable local dev server for `live`, `shot`, a URL scan and `critique`.
- Brand fonts and real imagery when the brief needs them.

## Outputs and how to bring them into a project

- Impeccable edits the project's own source files. Nothing needs an import step.
- `PRODUCT.md` and `DESIGN.md` at the repository root. Commit both. GDH reads the same `DESIGN.md`.
- `.impeccable/` committed files: `config.json`, `design.json` (a token sidecar), `surfaces/*.md`, `critique/ignore.md`.
- `.impeccable/` local-only files: critique reports, screenshots, `review/` and hook caches. Keep them out of git.
- Detector output as text, JSON, GitHub annotations or SARIF 2.1.0.
- Copy critique and audit findings into `design/reviews/<date>-<scope>.md` with an evidence label.

## Handoffs

- `DESIGN.md` and `.impeccable/design.json` are the brand contract for other tools: a canvas, a component generator, a design file.
- From a Claude Design canvas: use "Send to local coding agent", or export standalone HTML, into the repository first. Then run `audit` and `polish` on that code.
- From a component catalog: bring the component into the repository first, then audit it.
- To CI: `npx impeccable detect --sarif` feeds GitHub code scanning.
- From a source-rule review (see [vercel-web-design-guidelines.md](vercel-web-design-guidelines.md)): its findings feed `harden` or `polish`.
- To motion depth: see [emil-kowalski-skills.md](emil-kowalski-skills.md) for curve and duration decisions.

## Limits and failure modes

What the craft floor checks on the render, in summary:
- Body contrast of at least 4.5:1 and large text of at least 3:1. Body measure of 65 to 75ch. GDH default measure: 45 to 75 characters.
- Display size of 6rem at most. Letter-spacing never below -0.04em. Shadows have offset and blur.
- One authored motion moment, not the same entrance on every section.
- Hover, disabled, loading, error and empty states exist. Selection, caret, scrollbars, focus rings and numerals carry the theme.

What it refuses unless the brief earns it back: grids of identical icon cards, nested cards, the big-number hero block, numbered section markers on content that is not a sequence, a modal for a non-blocking task, gradient text, decorative glass and blur, a colored side bar on a rounded box, hard zero-blur shadows, filler sparklines and progress rings, monospace as a "technical" costume, a system font as display face, emoji as icons, a theme chosen by product category.

Gotchas:
1. One hard ban: an eyebrow or kicker label above a heading. The skill says no brief earns it back.
2. GDH precedence differs. The user and the project design system outrank a tell list. Report a brand-required tell as "brand-required", not as a failure.
3. Record a brand exception as a waiver, or the hook reports it on every edit.
4. Waiver by command: `npx impeccable ignores add-value overused-font Inter --reason "Brand font"`. Waiver in a file: an inline HTML comment that starts with `impeccable-disable`, then the rule id and a reason.
5. The `overused-font` rule flags Inter and similar fonts. A brand that owns such a font needs a waiver.
6. It runs code on the machine. The plugin registers three hooks: SessionStart, PostToolUse on `Edit|Write`, and Stop (30 s timeout).
7. The launcher is a native binary. It ships beside the skill or downloads once to `~/.impeccable/bin/`.
8. Claude Code runs installed command hooks even when the model's commands are denied.
9. Turn hooks off for one run with `--settings '{"disableAllHooks": true}'`. Turn them off for a project with `/impeccable hooks off`.
10. `live` works only on a local checkout with Vite, Next, SvelteKit, Astro, Nuxt or plain HTML.
11. The `live` Apply step can fall back to the `codex` or `claude` CLI with approvals and sandboxing off. Set `IMPECCABLE_LIVE_COPY_AGENT=chat` or `off` first.
12. A new design fetches visual directions from the `impeccable.style` catalog. A sandbox that blocks the host gives a degraded start.
13. `npx impeccable telemetry off` or `DO_NOT_TRACK=1` stops the usage record. It does not stop the catalog fetch.
14. A `critique` run without sub-agents must print a "DEGRADED: single-context" banner. A skipped detector counts as a failed critique.
15. Detector exit codes: 2 means findings, 1 means the target could not be scanned. GDH scripts use 1 for findings. Map the codes.
16. Source files (JSX, TSX) get pattern rules only. Contrast rules and tiny-text rules need a rendered URL. Scan the dev server too.
17. It is strongest on interfaces that already exist. A new page from nothing is the harder mode.
18. Name collision: `/impeccable harden` is an interface edge-case pass. The `harden` skill in GCH is a security pass.
19. Name collision: `animate` is also a skill name in the Emil Kowalski set. Say which kit you mean.
20. The repository carries no release notes. The author posts them on a social account. Read the diff before you move a pin.
21. A Chrome extension overlays the same findings on a live page. Research did not exercise it.

Detector rule ids. Unverified: research took these from a source search, so the shipped list can differ. Run `--list-rules` for the live list. Examples: `overused-font`, `gradient-text`, `ai-color-palette`, `cream-palette`, `dark-glow`, `nested-cards`, `icon-tile-stack`, `border-accent-on-rounded`, `hard-offset-shadow`, `kicker-above-heading`, `hero-eyebrow-chip`, `numbered-section-labels`, `gray-on-color`, `low-contrast`, `flat-type-hierarchy`, `oversized-h1`, `extreme-negative-tracking`, `all-caps-body`, `justified-text`, `line-length`, `cramped-padding`, `monotonous-spacing`, `bounce-easing`, `pulsing-dot`, `marquee`, `em-dash-overuse`, `marketing-buzzword`, `broken-image`, and a group of `design-system-*` drift rules.

## Best for

1. A scored critique and a ranked audit of an existing dashboard or settings screen before release.
2. One-axis refinement with a named verb: `typeset` a pricing page, `quieter` an overdesigned hero, `adapt` a table for phones.
3. A deterministic gate for tells in CI, with no model in the loop.

## Wrong for

A brand identity, a logo, an illustration, a 3D asset or a video. It is also the wrong first tool for a marketing site in an empty folder with no content. Get a first build from another route (see [design-taste-frontend.md](design-taste-frontend.md)), then refine with Impeccable.

## Evidence

DOCUMENTED on 2026-11-23. Research read a shallow clone of the public repository (commit `b49177d`) and the npm record.

- DOCUMENTED: the command set, the setup order, the hooks file, the craft floor, the detector flags and the file layout.
- UNTESTED: every command, the detector, the hooks, `live`, the Chrome extension and the optional MCP server. The skill was not installed.
- Not read: the site catalog of anti-patterns, the full shipped rule list and the rubric severity bands.
- Sources read: README; the skill source file; `reference/craft-floor.md`; part of `reference/critique.md`; `plugin/hooks/hooks.json`; the npm registry record.
