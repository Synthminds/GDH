---
name: ask-gdh
description: Routes a design-led request in the Global Design Harness once align has run. Classifies the request by discipline, from brand, type and color to charts, 3D, video and assets. Checks the design system and the brief, and lists the design tools this session holds. States a short plan and starts the first skill. Use after align closes, or when the user asks what GDH can do. Also use when it is unclear which design skill applies. Not for a code-only change inside an existing design system.
---

# ask-gdh

This skill is the router: it classifies a design request, runs the pre-flight, plans and starts the first skill. It designs nothing.

## Before you start

- Input: the user's request, in their words, and the closing report of `align`.
- Read, when present: `DESIGN.md`, `design/brief.md`, `design/decisions.md`. A `status: template` file counts as absent. A brief is confirmed only when its status line says so.
- Precedence: follow the user first, then the project design system, then the brief, then GDH defaults.
- Model-invoked: `align`, `ask-gdh`, `design-brief`, `concept-forge`, `mood-board`, `find-assets`, `design-critique`, `originality-gate`. The rest are user-invoked; the Skill tool cannot start them.

## Procedure

0. STOP: the closing report of `align` must be in this session. When it is absent, start `align` and stop. Answer "what can GDH do" without routing.
1. Restate the request in one sentence. Name the deliverable and who it is for.
2. Run the pre-flight in [references/preflight.md](references/preflight.md). It finds the design system, the brief, the last decision and the tools present. It makes no spend call and no write.
3. Classify the request. Name one primary discipline, the mode (explore or refine) and the path (light or full). Rules are in [references/routing.md](references/routing.md).
4. Feedback on the look of work that GDH made is a refine round, not a small change. Examples: bolder, calmer, bigger, another color. Route it to `refine-round`.
5. Apply the small-change exit to the rest: a design system exists, and the change stays inside it, touches no visual decision and needs no new asset. Examples: a new field, a state, a bug. Hand back to the coding agent with the token rules. Stop.
6. Pick a standard flow, or build the order from the routing table. Skip a skill whose output already exists and is confirmed.
7. ASK: only when two disciplines fit equally, or the deliverable is unclear. Ask one question. Put the recommended answer first.
   A brief that does not cover this request goes back to `align` as an escalation. Do not interview here.
8. State the plan in three to six lines, in the format under Output.
9. Start the first skill. Tell the user in one line which skill runs now. Give it the restated request and the pre-flight result.
   - A model-invoked skill: start it by name.
   - A user-invoked skill: read `../<name>/SKILL.md` from this skill's folder and follow it as if the skill had started.
   - When the file cannot be read, print the command for the user to type, such as `/gdh:refine-round`, and wait.
10. When a skill ends, read its closing report. Start the next skill the same way. Stop when a gate failed or the user redirects.
11. GATE: this skill never spends and never publishes. Name each foreseeable spend and exposure point in the plan.

### Routing table

| Request pattern | Skill | Comes before it | Comes after it |
| --- | --- | --- | --- |
| First design-led request of a session | `align` | nothing | `ask-gdh` |
| Audience, job or brand changed later in the session | `align`, escalation only | the request that changed it | `ask-gdh` |
| Any design-led request after `align`; "what can GDH do" | `ask-gdh` | `align` | first skill of the plan |
| Write, check or amend the brief; read a brief field | `design-brief` | `align` | `mood-board` |
| Ideas before looks; directions feel generic | `concept-forge` | `design-brief` | `mood-board` |
| Look undecided; "show me options" | `mood-board` | `concept-forge` | `design-system` |
| Create, import or extend tokens and `DESIGN.md` | `design-system` | chosen direction, or an existing brand | any build skill |
| Choose, pair, scale or license type | `typography` | `design-brief`, direction | `design-system` |
| Palette, themes, semantic color, contrast | `color` | `design-brief`, direction | `design-system` |
| Logo, wordmark, icon mark, identity set | `logo-identity` | `design-brief`, `mood-board` | `design-system` |
| Marketing site, content site, landing page | `website-design` | `design-system` | `design-critique` |
| Mobile or desktop app flows, screens, states | `app-design` | `design-system` | `design-critique` |
| Monitoring, analysis or report screen | `dashboard-design` | `design-system`, `data-viz` | `design-critique` |
| A chart or a chart style that states a finding | `data-viz` | `design-brief` | `design-critique` |
| Nodes and links: a network or graph view | `network-graph` | `data-viz` | `design-critique` |
| One-message explainer, poster, one-pager | `infographic` | `design-brief`, `data-viz` | `accessibility-gate` |
| Transitions, micro-interactions, motion tokens | `ui-motion` | `design-system`, a built screen | `handoff-to-code` |
| Video, motion graphic, animated explainer | `motion-video` | `mood-board` (styleframes) | `design-critique` |
| 3D model, hero scene, product viewer | `three-d` | `mood-board` | `website-design` |
| Generate an image, a clip, a voice or music | `generate-media` | chosen direction | `find-assets` record |
| Outside font, icon, photo, component, model | `find-assets` | brief or design system | the skill that asked |
| "Make it like this site": study a reference | `reverse-engineer-reference` | `design-brief` | `mood-board` |
| Claude artifact types: canvas, slides, data, whiteboard | `claude-design` | `design-system` | `design-critique` |
| Judge work; before you say "done" | `design-critique` | any build skill | `originality-gate` |
| Is it original or derivative? | `originality-gate` | `design-critique` | `refine-round` |
| Which design rules apply here? | `design-principles` | `design-brief` | the asking skill |
| Feedback on the look of GDH work: "make the hero bolder" | `refine-round` | `design-critique` or feedback | next round, or the gates |
| Accessibility check for the medium | `accessibility-gate` | any build skill | `handoff-to-code` |
| Approved design goes to code | `handoff-to-code` | critique and gate pass | the coding harness |
| New tool, connector or asset source | `add-design-tool` | nothing | `ask-gdh` pre-flight again |

### Standard flows

Seven flows: new brand, new website or app, dashboard, infographic, motion piece, 3D hero, refresh. Each starts after `align` has closed. Their order, needed brief, skip rules and gates live only in [references/flows.md](references/flows.md).

### When GCH is installed

GCH governs code work; its `ux-laws` numbers hold for screens. Pre-flight section 5 maps GCH skills to steps.

## Tools

It reports which capabilities this session can serve.

- Vocabulary and discipline map: [capabilities.json](../../catalogs/capabilities.json).
- Tool entries: `kit/catalogs/tools/<id>.json`. Tool cards: `kit/references/tools/<id>.md`.
- A hosted design system counts as a design system. Example card: [claude-design-system](../../references/tools/claude-design-system.md).
- A brand library can hold a brand pack. Example card: [dam](../../references/tools/dam.md).
- Local programs: [scripts/local_clis.py](scripts/local_clis.py) `probe` lists CLI-Anything harnesses on PATH. Card: [cli-anything](../../references/tools/cli-anything.md).
- When a tool is absent, name its catalog `fallback` in the plan.

## Checks

Gates:

- No route before the closing report of `align` is in this session.
- The plan names the design system that was found, or says "none".
- No build skill starts before a confirmed brief exists.
- No full build starts before a direction is chosen, unless a design system already fixes the look.
- The plan names every spend and exposure point it can foresee.

Defaults. The user, the design system or the brief can replace each one.

- Default: a plan holds six skills at most. Split a longer job into phases and plan the first.
- Default: the light path applies when a design system exists, the mode is refine and one deliverable is asked for.

## Output

This skill writes no file. It prints the plan, then starts the first skill as step 9 says.

```
GDH plan: <request in one line>
Aligned: tier <one | two>, <date>; brief <status line>
Found: design system <path or none>; last decision <date and scope, or none>
Tools: <capabilities served>; missing <capability: fallback>
1. <skill> (<model | user>): <what it produces>
2. <skill> (<model | user>): <what it produces>
Gates ahead: spend <where or none>; exposure <where or none>
```

## References

- [references/preflight.md](references/preflight.md): read at step 2. The search order, the tool presence check and the report format.
- [references/routing.md](references/routing.md): read at steps 3 to 5 when the request is mixed or unclear.
- [references/flows.md](references/flows.md): read at step 6. The seven flows, with skip rules and gates.

## Sources

- GDH kernel and principles: `kit/canon/KERNEL.md`, `kit/canon/PRINCIPLES.md`.
- Design Leadership Handbook (DesignBetter), ch. 3: name the mode, exploration or refinement.
- DesignOps Handbook (DesignBetter), ch. 5: visible intake before work starts.
- Principles of Product Design (DesignBetter), ch. 3: low fidelity first.
