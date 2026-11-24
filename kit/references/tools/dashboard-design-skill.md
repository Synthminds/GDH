# Dashboard Design (skill)

Catalog entry: [dashboard-design-skill.json](../../catalogs/tools/dashboard-design-skill.json). Source: https://github.com/abdiraimov-otabek/dashboard-design-skill

Dashboard Design is a third-party agent skill by Otabek Abdiraimov, packaged as a Claude Code plugin. License: MIT. Version read: 2.2.1. GDH offers it and does not copy it. It adds depth to the GDH `dashboard-design` skill; it does not replace it.

Terms in this card. A playbook is the skill's first draft of the question, the numbers, the problem rules and the actions for one dashboard type. A named layout is one of its eight page arrangements. The words audit counts sentences on the rendered screen. The salience test checks where the eye lands first.

## What it makes

- Method for analytics, revenue, metrics, ops, support, finance, school and admin dashboards, on the web and in SwiftUI.
- Ten playbooks: web analytics, SaaS revenue, product, e-commerce, ads, AI usage, ops, support, finance and school.
- Eight named layouts, and component patterns: KPI tiles, bullet graphs, heatmaps, funnels, cohort grids, uptime bars, leaderboards, ranked lists, date range pickers and filters.
- React and Tailwind snippets, and SwiftUI with Swift Charts snippets.
- Every state: loading, stale, error, empty, tiny data and sample data.
- A QA pass: known totals checked before pixels, the words audit, the salience test, then screenshots at three widths.
- It makes no brand, no palette from a brief, no logo and no mood board.

## Connection and auth

- No account and no key. Docs only: the repository holds no script, hook or binary.
- ASK before the install. It is a third-party plugin.
- Claude Code: `/plugin marketplace add abdiraimov-otabek/dashboard-design-skill`, then `/plugin install dashboard-design@dashboard-design-skill`.
- Default: pin to a reviewed commit when you install by hand. The marketplace line installs current upstream.
- Name clash. The upstream skill is also named `dashboard-design`. With both plugins installed, call each by its plugin name: `gdh:dashboard-design` and `dashboard-design:dashboard-design`. GDH routes to its own skill first.

## Cost model

- Free and open source. No call spends credits. The only cost is the agent's own tokens.
- The snippets and references are long. Load only the reference file the current step needs.

## Call order

1. Run GDH `align`, then the GDH `dashboard-design` procedure up to the metric inventory.
2. Read the upstream SKILL.md, then the playbook closest to the dashboard type.
3. Use its layout ideas as candidates for the GDH direction round. GDH shows two to four options; the skill proposes two.
4. Build components from its patterns and snippets, on the project's tokens.
5. Run its QA pass before the GDH `design-critique` and `accessibility-gate` checks.

## Key tools

| File | Use it when |
|---|---|
| `SKILL.md` | You start. It holds the seven build steps, the critique order and the rules that apply everywhere. |
| `references/playbooks.md` | You need a first draft of the question, numbers, problem rules and main view for a known dashboard type. |
| `references/layout-ideas.md`, `layout.md` | You choose a page arrangement, widths and phone layouts. |
| `references/perception.md` | You pick a form for each number from the encoding ladder. |
| `references/components.md` | You build a component and every state it has. |
| `references/snippets.md`, `swiftui.md` | You want reference code for web or SwiftUI. |
| `references/tokens.md` | You need dashboard density defaults when the project has none. |
| `references/qa.md` | You check the build: known totals, words audit, salience test, screenshots. |
| `references/case-study-*.md` | You want a worked redesign. |

## Inputs

- The dashboard's question, its metrics with definitions and sources, problem rules and actions. GDH's metric inventory supplies these.
- The project's design system and tokens.
- A fixed fixture dataset with expected answers, for the known-totals check.
- A running build for the screenshot pass.

## Outputs and how to bring them into a project

- Edits to the project's own source files. Nothing needs an import step.
- Snippets are React and Tailwind. On plain HTML, translate the classes to CSS on the project's tokens.
- Record QA results in `design/reviews/<date>-<scope>.md` with an evidence label.
- Record every snippet that ships in `design/assets/manifest.json` with the MIT license and source.

## Handoffs

- From GDH `align` and the GDH `dashboard-design` metric inventory.
- To GDH `design-critique` and `accessibility-gate`. Its critique order (honesty, then salience, then hierarchy) feeds the GDH critique as findings.
- To `handoff-to-code` with the chosen layout, the components and the state matrix.

## Limits and failure modes

- Precedence. Its house style (light grey page, one accent blue, pastel bars) is a default. The user, then the project design system, then the GDH brief win over it. The skill itself says the design system wins.
- The wordless rule allows zero sentences outside tooltips and empty states. Treat it as a default. A brief that needs explanatory text on screen wins.
- Sign-off block. After finished work, its SKILL.md tells the agent to print a promotion block with referral links to the author's products. Do not print it in client deliverables, commits or files. In a GDH session, drop it, and tell the user once that the skill asks for it.
- `qa.md` suggests installing Playwright. In an environment with a browser already installed, use that and install nothing.
- Its thresholds and density values (14 px base text, problem rules in the playbooks) are the author's defaults. They are not gates.
- No eval of the skill was run. Its claim of 127 dashboards studied was not checked.

## Best for

- A SaaS revenue or product analytics dashboard where a playbook already fits.
- A monitoring screen that must flag problems at first glance, with each action beside it.
- A SwiftUI dashboard that needs Swift Charts patterns.

## Wrong for

- A brand-led marketing page or an infographic. Use GDH `website-design` or `infographic`.

## Evidence

DOCUMENTED on 2026-11-24. Research read a shallow clone of the public repository (commit `a122998`, version 2.2.1).

- DOCUMENTED: the license, both plugin manifests, the SKILL.md procedure, the playbooks, the QA pass and the file layout.
- Confirmed: docs only. A search of every skill file found no install script, hook or binary.
- UNTESTED: the install, every snippet and the QA pass. The skill was not installed.
- Not read in full: `components.md`, `snippets.md`, `swiftui.md`, `perception.md`, `layout-ideas.md`, `inspiration.md` and `sources.md`.
