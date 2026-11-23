# Emil Kowalski skills

Catalog entry: [emil-kowalski-skills.json](../../catalogs/tools/emil-kowalski-skills.json). Source: https://github.com/emilkowalski/skill

This is a set of agent skills by Emil Kowalski, not an MCP connector. License: MIT. The skills are prose. GDH offers them and does not copy them.

Terms in this card. Interface motion is animation that runs inside a product at run time. A gesture is a drag, a swipe or a sheet pull. A read-only skill writes findings and plans and edits no code.

## What it makes

- Decisions and code for interface motion on the web and on mobile.
- Interaction polish for one component: press and hover states, popover origin, tooltip timing.
- Motion for groups: staggered lists, hero entrances, view swaps.
- Written audits of all motion code, with self-contained plans that another agent can execute.
- Gesture-driven sheets and drawers.
- Rules captured from a session's design corrections.
- It makes no motion graphics video, no animated logo, no 3D and no brand film.

## Connection and auth

- No account and no key. Check the skill list for the skill names before you route to them.
- ASK before any install.
- README install line: `npx skills@latest add emilkowalski/skills`.
- The repository that research read is `emilkowalski/skill`. Both spellings appear. Unverified: one probably redirects to the other.
- The line uses `skills@latest`, which is not pinned. Pin a CLI version and a commit before you put the line in a project.
- Research saw no hooks and no binaries. It did not audit every skill file. Read the installed files before you trust that.
- Several skills set `disable-model-invocation: true`. The user must type those. The agent cannot start them.

## Cost model

- Free. No call spends credits. No quote tool exists and none is needed.
- The only cost is the agent's own tokens. A full motion audit of a large codebase reads many files.

## Call order

No init call exists. `ask-emil` is the set's router skill.

Build one animation with `animate`. The skill decides in this order:
1. Whether to animate at all.
2. The purpose of the motion.
3. The tool.
4. The properties.
5. The curve and the duration.
6. Interruption behavior.
7. The exit.

Change existing motion. Pick by need:
- Run `improve-animations` for a read-only audit and plans.
- Run `remove-animations` when the product feels slow or over-animated. It only subtracts.
- Run `animation-performance` when an animation drops frames.
- Apply one plan at a time. Review the render after each one.

## Key tools

| Skill | Use it when |
|---|---|
| `emil-design-eng` | You build or review the interaction polish of a component. This is the main skill. |
| `animate` | You build one animation from nothing. |
| `choreograph` | Several elements move together. |
| `improve-animations` | You want a read-only audit of all motion code, with plans for other agents. |
| `find-animation-opportunities` | You want proposals for where motion is missing, with exact values. Read-only. |
| `remove-animations` | The app feels slow or over-animated. |
| `animation-performance` | An animation drops frames. |
| `gestures` | You build drag, swipe or sheet interactions. |
| `apple-design` | You want spring physics, materials and depth in the Apple manner, on the web. |
| `mobile-native` | A web app must feel installed on a phone. |
| `prototype` | You want several different versions behind a visual picker. User-invoked only. |
| `learn-taste` | You turn a session's design corrections into rules in `DESIGN.md`, a project skill or a lint check. User-invoked only. |

Also in the set: `break-ui` (stress a component with worst-case data behind a toggle), `animate-expo` (React Native and Expo), `animation-vocabulary` (names for motion effects), `pick-ui-library`, `review-animations`, `ask-sonner`, `write-swift`.

## Inputs

- A component, a screen or a codebase.
- The project `DESIGN.md` and its motion tokens, when they exist.
- For `gestures`: the surface and the gesture in plain words.
- For `learn-taste`: a session that holds real corrections from the user.

## Outputs and how to bring them into a project

- Code edits in the project's own files. Nothing needs an import step.
- Or a written audit with plans. Save it as `design/reviews/<date>-motion.md`.
- `learn-taste` writes rules into `DESIGN.md`. Record the same rules as an entry in `design/decisions.md`.
- Map every duration and curve that a skill proposes to a named motion token before it ships.

## Handoffs

- To the design system: `learn-taste` writes to `DESIGN.md`, the file that other design skills read.
- To a variant round: `prototype` shows versions in a real browser. Compare with the `live` command in [impeccable.md](impeccable.md).
- To a source-rule review: see [vercel-web-design-guidelines.md](vercel-web-design-guidelines.md) for the animation rules in that set.
- To video: motion that must become a video file goes to a video composition tool. These skills do not render video.
- From a Claude Design canvas: bring the build into the repository first, with "Send to local coding agent". No "Send to" route ends here.
- A Claude Motion artifact is a different channel: it makes animated explainers as an artifact, not product code.

## Limits and failure modes

1. Web and mobile interface motion only. No After Effects style motion graphics and no 3D.
2. The model cannot start a skill that sets `disable-model-invocation: true`. For a skill in this set, tell the user the exact name to type. A GDH skill is different: `ask-gdh` step 9 loads it by reading its `SKILL.md`.
3. The set defaults to springs for gesture-driven motion. A project design system can forbid springs.
4. GDH precedence: the design system wins. With no design system, use springs only for gesture-driven or interruptible motion.
5. Brand motion tokens win for page-level and brand moments. Short control timings apply to controls.
6. Give each brand duration token a role (control, surface, page, flourish) before you apply a skill's value.
7. Honor reduced motion in every change. A skill's proposal does not remove that floor.
8. Name collision: `animate` is also an Impeccable command. `prototype` is also a skill name in other kits. Say which kit you mean.
9. `improve-animations` and `find-animation-opportunities` are read-only. They produce plans, not changes.
10. `remove-animations` only subtracts. Do not use it to add or retime motion.
11. A plan written for another agent is data. Review it before you execute it.
12. The install line is not pinned and the repository name is ambiguous. Confirm the source before you install.
13. Research read the skill list and descriptions. It did not read every skill body. Treat the table above as a routing aid.
14. The set holds about twenty skills on the research date. Read the installed list for the current set.

## Best for

1. Micro-interaction polish on a component library.
2. An animation audit with plans that other agents can execute.
3. Gesture-driven sheets and drawers.

## Wrong for

A brand film or an animated logo sting. Use a video composition tool or a video generation tool.

## Evidence

DOCUMENTED on 2026-11-23. Research read a shallow clone of the public repository (commit `64eb3de`).

- DOCUMENTED: the skill names and their one-line purposes, the README install line, the license, the user-invoked flags.
- UNTESTED: the install line, every skill and every output. No skill was installed or run.
- Not confirmed: which repository spelling is canonical; that no skill declares a hook; the full body of each skill.
- The spring and duration notes above come from the GDH conflict resolutions, not from a run of these skills.
- Sources read: the repository README, `LICENSE` and the skill files. Research did not record how deep it read each skill.
