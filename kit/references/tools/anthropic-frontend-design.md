# Anthropic frontend-design

Catalog entry: [anthropic-frontend-design.json](../../catalogs/tools/anthropic-frontend-design.json). Source: https://github.com/anthropics/skills

This is an agent skill by Anthropic, not an MCP connector. License: Apache-2.0. It is one prose file: no scripts, no hooks, no binaries. The same file ships as the plugin `frontend-design` in the official Claude Code marketplace.

Terms in this card. A design plan is the skill's short token system: named colors, typefaces with roles, a layout concept and principles. A default look is a style that models produce when nobody chooses.

## What it makes

- A visual direction for a web or app interface: palette, type, layout concept, motion restraint and copy.
- A design plan in text, before any code.
- Interface code in the project, built from that plan.
- A self-critique of the result against the brief.
- It makes no artifact, no image, no logo and no asset. It has no detector and no audit of an existing codebase.

## Connection and auth

- No account and no key. Check the skill list for `frontend-design` first.
- Research reports it as a built-in skill in Claude apps. It was absent from the researched Claude Code session.
- Claude Code: `/plugin install frontend-design@claude-plugins-official`. That marketplace is present by default.
- Claude Code, second route: `/plugin marketplace add anthropics/skills`, then install the plugin that holds the skill.
- Any host: `npx skills add anthropics/skills --skill frontend-design`.
- The frontmatter uses `name`, `description` and `license` only. The file therefore loads on hosts that accept only the portable skill fields.
- A connector's instructions can tell the agent to use a skill of this name. Confirm that the skill is installed before you follow that route.

## Cost model

- Free. No call spends credits. No quote tool exists and none is needed.
- The only cost is the agent's own tokens: one prose file plus the plan it writes.

## Call order

No init call exists. The skill sets a four-pass process:
1. Identify the subject. When the brief names none, propose one subject, one audience and one primary job. ASK the user to confirm.
2. Write the design plan. It holds 4 to 6 named hex colors, typefaces with roles, a layout concept with ASCII wireframes, and principles.
3. Review the plan against the brief. Revise each part that reads as a default look. Say what changed.
4. Build. Then critique the result from screenshots when the host can take them.

In a GDH flow:
1. Read `design/brief.md` and `DESIGN.md` first. A project design system outranks the skill's free choices.
2. Use the plan format for each direction in a mood board.
3. Write the chosen plan into `design/decisions.md` and the tokens into `design/tokens.json`.

## Key tools

| Skill | Use it when |
|---|---|
| `frontend-design` | You set a distinct direction at the start of a new interface. This is the skill this card covers. |
| `canvas-design` | You need a static poster or art piece as PNG or PDF. |
| `theme-factory` | You want one of a set of preset themes for slides, documents or HTML. |
| `brand-guidelines` | You need a template for a brand skill. The shipped content is Anthropic's own brand. |
| `algorithmic-art` | You need generative art in p5.js with seeded randomness. |
| `web-artifacts-builder` | You build a React, Tailwind and shadcn artifact. |

The five sibling skills live in the same repository. Research read their frontmatter only. `/design` in Claude Code is a different bundled skill: it publishes artboards as a Claude Design artifact.

## Inputs

- A brief with a subject, an audience and a primary job.
- Real content from the brief. The skill treats placeholder copy as a cause of templated work.
- The project design system, when one exists.

## Outputs and how to bring them into a project

- The plan as text in the chat. Save it. The skill keeps no memory between runs.
- Code in the project's own files. Nothing needs an import step.
- Copy the plan's colors and type roles into `design/tokens.json` and `DESIGN.md` as named tokens.
- Record the direction and the rejected defaults in `design/decisions.md`.

## Handoffs

- To a mood board: the plan format (palette, type, layout, principles) maps onto one direction board.
- To a Claude Design canvas: put the plan in the canvas brief. State goal, layout, content and audience.
- From a Claude Design canvas: "Send to local coding agent" brings the artboards into the coding session. Apply the skill's rules during the build.
- To a generator or a component catalog: use the plan as the brand contract in the prompt.
- To a review: this skill has no detector. See [impeccable.md](impeccable.md) and [vercel-web-design-guidelines.md](vercel-web-design-guidelines.md).
- To a gated site build: see [design-taste-frontend.md](design-taste-frontend.md) when the user wants a dealt layout and a browser gate.

## Limits and failure modes

What the skill asks for, in summary:
- Ground every choice in the subject: its industry, its materials and its everyday visual language.
- Open the page with the most characteristic thing in the subject's world.
- Use one or two type families. Two families must differ clearly. Set a clear type scale.
- Keep line length under 80 characters. GDH default for body text: 45 to 75 characters.
- Spend boldness in one place and keep the rest quiet. Remove one accessory before you finish.
- Prefer one orchestrated motion moment to scattered effects. Motion that answers a user action is welcome.
- Use numbered markers only for a real sequence.
- Quality floor: responsive to mobile, visible keyboard focus, reduced motion respected, accessible contrast.
- Copy: write from the user's view, in active voice and sentence case. A button says what happens. An error says what went wrong and how to fix it.

The five default looks it names:
- A warm cream background with a serif display face and a terracotta accent.
- A near-black background with one acid accent.
- A broadsheet layout with hairline rules.
- The SaaS kit of identical rounded cards.
- Template chrome: tracked all-caps eyebrow labels, meta strings joined by middle dots, arrows on links.

Type tells it names: one accented word in a headline, all-caps labels, and labels above content that needs none.

Gotchas:
1. The default looks are allowed when the brief asks for them. The brief's own words always win in the skill.
2. GDH precedence adds one level: the user, then the project design system, then the brief, then these lists.
3. Report a tell that the brand requires as "brand-required", not as a failure.
4. The skill names fashions. The list will age. Read the installed file for the current list.
5. It lists a tinted near-black as a current default look. Older advice forbids pure black. Decide from the design system, then the brief.
6. An older Anthropic cookbook prompt gives different advice. It bans common sans-serif fonts and purple gradients on white, and asks for layered backgrounds.
7. Prefer the current skill file when the two disagree. Do not merge the two lists into one rule.
8. It has no verification step of its own. For a code deliverable, GDH still requires a review of the render.
9. It has no detector and no memory. It cannot tell whether two projects got the same look. Keep the record in `design/decisions.md`.
10. The skill warns about CSS selector specificity: section padding rules and margin rules can cancel each other. Check the render.
11. Claude applies a built-in design skill when it builds an artifact. Research did not confirm that it is this skill.
12. That artifact guidance sets the same precedence: the user's prompt, then the project design system, then Claude's own choices.
13. Plugin version read: 1.1.1. The two public copies matched on the research date. Compare them again before you rely on that.

## Best for

1. A distinct direction at the start of any new interface.
2. A zero-risk default on hosts that forbid hooks and binaries.
3. The planning half of a mood board step.

## Wrong for

An audit of an existing codebase for accessibility defects. Use a review skill with rules and a rendered check.

## Evidence

DOCUMENTED on 2026-11-23. Research read the skill file in two public repositories and found the copies identical.

- DOCUMENTED: the process, the principles, the default-look list, the frontmatter fields, the plugin entry and the install routes.
- UNTESTED: every install route and a run of the skill. The skill was not in the researched session.
- Not read: any supporting files in the skill's folder, and the bodies of the sibling skills.
- Not confirmed: that Claude apps carry it as a built-in skill today; which skill the artifact builder applies.
- Sources read: `skills/frontend-design/SKILL.md` in `anthropics/skills`; the `frontend-design` plugin in `anthropics/claude-plugins-official`; the cookbook "Frontend Aesthetics: A Prompting Guide"; the Claude Code artifacts page.
