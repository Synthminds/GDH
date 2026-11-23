# Routing rules

Read this file when a request is mixed, vague or between two disciplines.

## 1. Is it design-led at all?

Route into GDH when one of these holds:

- No design system exists and the task needs a look.
- The task names brand work: a logo, a palette, a typeface, guidelines.
- The task asks for a direction or a choice between looks.
- The task needs a chart style, an infographic, a 3D model, an animation, a video, an illustration or a generated image.
- The task needs an outside asset or a design tool.

Check the feedback rule before the small-change exit. Feedback on the look of work that GDH made is a refine round, not a small change. Bolder, calmer, bigger, smaller, tighter, a different color or a different image all count. Route it to `refine-round`, which logs the round in `design/decisions.md`. The design system may already hold the values; the choice among them is still a visual decision.

Use the small-change exit when all of these hold:

- A design system or an established look exists.
- The change stays inside it and touches no visual decision: a new field, a state, a fix, an accessibility repair, a layout bug.
- No new asset, font, color or brand element is needed.
- The request is not feedback on the look of GDH work.

On the exit, tell the coding agent three things: where the tokens are, "tokens only", and the accessibility floor. Then stop.

Middle case: "show me a few options for this page" inside an existing component library. This is a refine job. Route to `refine-round` with variants that differ in one attribute. With GCH installed, `gch:prototype` builds the variants.

## 2. Pick the primary discipline

Find the noun the user will receive. That noun decides the discipline, not the tool they named.

| The user will receive | Discipline | Skill |
| --- | --- | --- |
| A name-bearing mark or identity set | logo, brand | `logo-identity` |
| A type choice, a scale, a pairing | typography | `typography` |
| A palette or themes | color | `color` |
| Tokens, `DESIGN.md`, a component rule set | design-system | `design-system` |
| Pages people read or buy from | website | `website-design` |
| Screens people work in | app | `app-design` |
| A screen people monitor or analyze with | dashboard | `dashboard-design` |
| One or more charts | dataviz | `data-viz` |
| A picture of nodes and links | network-graph | `network-graph` |
| One composed explainer image or page | infographic | `infographic` |
| Motion inside an interface | ui-motion | `ui-motion` |
| A file that plays: video or animation | motion-video | `motion-video` |
| A model or a scene in three dimensions | 3d | `three-d` |
| Boards to choose a look from | moodboard | `mood-board` |
| A judgment on existing work | critique | `design-critique` |
| A file from outside the project | assets | `find-assets` |
| An analysis of someone else's site or app | reference | `reverse-engineer-reference` |

Tie-break rules:

1. Website versus app: people read or buy, then website. People do repeated work with their own data, then app.
2. App versus dashboard: the screen's main job is to change data, then app. Its main job is to read data and decide, then dashboard.
3. Dashboard versus data-viz: more than one view with shared filters or a layout question, then dashboard. One chart or a chart style, then data-viz.
4. Data-viz versus infographic: the reader explores, then data-viz. The author tells one message in a fixed reading path, then infographic.
5. Data-viz versus network-graph: the data is entities with relations, then network-graph.
6. UI motion versus motion video: it responds to input inside a product, then ui-motion. It plays on a timeline and exports as a file, then motion-video.
7. Generate versus find: try `find-assets` first when a real photo, a licensed icon set or an existing model can serve. Use `generate-media` when the asset must be unique to the brand or does not exist.
8. Logo versus design-system: "a brand" with no mark asked for still starts with the new-brand flow. Ask whether a mark is in scope.
9. Tool named, noun unclear: when the user says "use the design canvas" or "make it in the slide tool", route to `claude-design`. It picks the artifact type and calls the discipline skill for the content rules.
10. Slides and decks have no discipline skill of their own. Route to `claude-design` after `design-system`.

When two disciplines still fit equally, ask one question. Example: "Is the result a page people read once, or a screen they return to daily? Recommended: a page."

## 3. Set the mode

| Mode | Signal | Effect |
| --- | --- | --- |
| explore | "new", "redesign", "options", "directions", no look exists | Options differ in idea. Default: three. |
| refine | "tweak", "polish", "improve", "fix", a look exists and is liked | Options differ in one named attribute. Scope is locked. |

Say the mode in the plan. A refine job that turns into a redesign is the most costly routing error. When a refine request implies a new look, stop and ask.

## 4. Set the path

| Path | When | Effect |
| --- | --- | --- |
| light | Design system `strict`, mode refine, one deliverable | `align` ran tier two or the asset or page depth. `mood-board` is skipped or holds two directions. |
| full | Anything else | Every skill in the flow runs. |

## 5. Mixed requests

1. Split the request into deliverables. Rank them with the user: 1, 2, 3. No ties at the top.
2. Plan deliverable 1. Name the others under "later" in the plan.
3. Shared groundwork runs once: one brief, one direction, one design system.
4. When a later deliverable needs a different audience or a larger job size, send it back to `align` for those topics.

## 6. Worked examples

**"Make a landing page for our new sleep tracker."** Pre-flight: design system none, brief none. Discipline website, mode explore, path full. `align` ran tier one at page size. Plan: `mood-board`, `design-system`, `website-design`, `design-critique`, `accessibility-gate`. Gates ahead: spend at `generate-media` if product images are generated; exposure at deploy.

**"The settings page needs a new toggle for email digests."** Pre-flight: design system strict. Small-change exit. No GDH flow.

**"Make the hero bolder."** Pre-flight: design system strict, brief confirmed, the hero came from an earlier GDH round. This is feedback on the look, so the small-change exit does not apply, even though the tokens can express the change. Discipline website, mode refine, path light. Plan: `refine-round` with two or three variants that differ in one named attribute (weight, scale or contrast), then the gates. The round is logged in `design/decisions.md`.

**"Our dashboard looks dated. Freshen it up."** Pre-flight: design system implicit. Discipline dashboard, mode refine until the user says otherwise. ASK: "Keep the brand and layout and fix the craft, or explore a new look? Recommended: keep and fix." Plan on "keep": `design-system` (import), `design-critique` (audit), `refine-round`, `accessibility-gate`.

**"I need a logo and a quick explainer video for launch."** Two deliverables. Rank: logo first, because the video shows it. Plan the new-brand flow up to `logo-identity`. Name `motion-video` under "later".

**"Turn this spreadsheet into something the board can read in one minute."** One message, fixed reading path: infographic, not dashboard. `align` ran at page size: who, the one message, where it is shown. Plan: `data-viz`, `infographic`, `accessibility-gate`.

**"Add the new image tool we just connected."** Not design work. Route to `add-design-tool`. Then run the pre-flight again.

## 7. Routing failure patterns

| Pattern | Sign | Correction |
| --- | --- | --- |
| Tool-first routing | The plan starts with a generator because the user named it | Route by the noun. The tool is chosen inside the skill. |
| Skill pile | The plan lists nine skills for a one-screen change | Apply the small-change exit or the light path. |
| Silent restyle | Feedback on the look goes straight to the coding agent and no round is logged | Apply the feedback rule. Route to `refine-round`. |
| Brief skip | "The request is clear enough" and a build skill starts | `align` runs first in every session. An asset job costs six questions at most. |
| Direction skip | A full site is built in one look, then the user dislikes it | Direction before build. Two directions is the minimum with no strict system. |
| Mode drift | A refine round replaces the palette | Stop. Ask whether the mode changes to explore. Log it. |
| Lost thread | A second session re-proposes a rejected direction | Read `design/decisions.md` in the pre-flight. |
