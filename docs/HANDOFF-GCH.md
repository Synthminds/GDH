# The hand-off between GCH and GDH

GCH is the coding harness. GDH is the design harness. This document fixes the boundary between them and the exact text GCH uses to offer GDH.

Evidence. The GDH side is built and checked in this repository. The GCH side is a proposal: the changes below were not applied to the GCH repository from here, and its own checks were not run. Apply them there, then run that repository's build, check and tests.

## 1. The boundary

GCH keeps a small design capability: decision rules for screens and evidence captures of a build. Everything design-led goes to GDH.

### Hand off to GDH when one of these holds

- No design system exists, and the task needs a look: a new site, an app shell, a landing page or a dashboard.
- The task names brand work: a logo, a wordmark, a palette, a type choice, brand guidelines.
- The task asks for a direction or a choice between looks: a mood board, "make it look great", "make it unique", a redesign of several screens.
- The task needs a chart style, an infographic or a data-visualization system, not one chart inside an existing system.
- The task needs a 3D model, an animation, a motion graphic, a video, an illustration or a generated image.
- The task needs a design tool or an outside asset.

### Stay in GCH when all of these hold

- A design system or an established look exists in the repository.
- The change stays inside it: a new field, a new state, a fix, an accessibility repair, a layout bug.
- No new asset, font, color or brand element is needed.
- The request is not feedback on the look of work that GDH made: bolder, calmer, bigger, another color. Such feedback goes to GDH. `gdh:ask-gdh` routes it to `refine-round`, which logs the round in `design/decisions.md`. An entry in `design/decisions.md` for the same element shows that GDH made it.

### The middle case

"Show me a few options for this page", inside an existing component library, stays in GCH: its prototype skill builds variants on one route. The same request with no library, or with a request for a new visual language, goes to GDH.

GDH applies the same test from its side. Its router first sends feedback on the look of GDH work to `refine-round`. Then its small-change exit hands a contained change straight back to the coding agent.

## 2. What GCH adds

A few small changes in the GCH registry and in one GCH skill. No GDH file is copied into GCH.

### 2.1 One wired entry

| Field | Value |
| --- | --- |
| id | `gdh` |
| name | `GDH (Global Design Harness)` |
| what | `runs design-led work: a short alignment interview first, then its own skills, tool catalog and review rounds` |
| install | `/plugin marketplace add Synthminds/GDH`, then `/plugin install gdh@synthminds-gdh` |
| source | `https://github.com/Synthminds/GDH` |

The GCH moments renderer writes the entry as "<name>, which <what>", so `what` starts with a verb in the third person.

### 2.2 The moment text

Two moments in GCH `kit/kit.json` offer `gdh`.

1. The existing screen moment. Find it by its `when`, which reads "You build, change or judge a screen or a user flow". Keep its `when` and its start, `ux-laws`. Replace its two offers, both third-party design skills, with `gdh`.
2. A new moment for design work that is not a screen. It starts nothing and offers `gdh`.

Use this text exactly as the `when` of the new moment:

```
The task needs a new look or a design asset: a brand or a logo, a new site, app or dashboard design, a chart or infographic style, a 3D model, an animation, a video or a mood board
```

Rendered in the moments text, the line reads:

```
- The task needs a new look or a design asset: a brand or a logo, a new site, app or dashboard design, a chart or infographic style, a 3D model, an animation, a video or a mood board. Offer `gdh`.
```

The moment offers; it does not start. GDH is a different plugin, and the user decides whether to bring it in.

### 2.3 The offer

One question, asked once in a session, in the host's question tool:

- Option 1, recommended: "Use GDH for this design work."
- Option 2: "Skip": continue in GCH with its screen rules only.

With no question tool, one closing line:

```
Option: GDH runs design-led work. Its first turn is a short alignment interview.
```

The user should know before choosing GDH that its first turn is a question.

After "Skip", GCH does not ask again in that session. It continues with its own screen rules and says so in its report.

### 2.4 The hand-off block in GCH `ux-laws`

Add this block as a "When to hand off" section at the end of `kit/skills/ux-laws/SKILL.md` in GCH. GCH has no separate design-basics file; `ux-laws` holds its screen rules.

```
When to hand off

This skill holds the screen rules. Hand the work to GDH when the task needs a new look or a design asset:
a brand, a logo, a new site or dashboard design, a chart style, a 3D model, an animation, a video or a mood board.
Feedback on the look of work that GDH made (bolder, calmer, bigger, another color) also goes to GDH.

- If the skill `gdh:align` is listed in this session, start it and give it the context below. It interviews the user,
  or re-aligns on a confirmed brief, then hands over to `gdh:ask-gdh`. Pass what you know as facts to confirm,
  not as decisions. Once `gdh:align` has closed in this session, start `gdh:ask-gdh` instead.
- Start no other GDH skill. The other GDH skills are user-invoked; `gdh:ask-gdh` loads them itself.
- If GDH is not listed, offer it once, with its install line. After "Skip", continue with these rules and say so in the report.

Context for GDH: the goal and the audience; the stack and the component library; the design system files
that exist (DESIGN.md, tokens, theme); the screens in scope; the limits (licenses, budget, deadline);
the checks that the result must pass.

What comes back: design decisions and tokens in files, assets with their source and license, and the
open questions, packaged in design/handoff.md. GCH then builds from those files and verifies the result
with its own screen rules and evidence captures.
```

### 2.5 What moves out of GCH

The wired entries for third-party design skills belong in GDH. GDH already lists them in its own registry. Remove them from the GCH screen moment when the `gdh` offer is added, so that a moment keeps three offers at most.

### 2.6 One interview, not two

Every GDH session opens with `gdh:align`. Without a confirmed `design/brief.md` it runs the full interview. With one it re-aligns in a few questions. `--full` forces the full interview.

- When `gdh:align` is listed in the session, GCH runs no design interview or design brief of its own. It defers to `gdh:align`, so the user is never interviewed twice about the same design work.
- `gdh:align` runs its own question loop by default. It hands the loop to `gch:grilling` only when the grilling description in the session contains the words "caller contract" (section 2.7). Then GCH runs the loop; GDH owns the topics, the questions and the brief.

### 2.7 What `gch:grilling` receives and returns

The marker. `gdh:align` delegates only when the description of `gch:grilling` contains the exact words "caller contract". Without them it says that GCH grilling does not yet honor the `align` contract, and runs its own loop. So GCH adds the words to the grilling description, and a "Caller contract" section that states the rules below. Without a caller, grilling keeps its own default behavior.

With the marker present, `gdh:align` calls the Skill tool with `gch:grilling` and gives it:

1. The goal: align on a design brief for one subject at one job size.
2. A topic tree, with the prerequisites of each topic.
3. A depth row: each topic marked required, optional or skipped for this job size.
4. A question bank: for each question, a recommended answer and a probe for a weak answer.
5. An evidence list: the facts that `align` already read from files, so that no question asks what a file answers.
6. A stop rule: every required topic answered or ASSUMED, or the question cap reached.

`gch:grilling` honors these loop rules:

- Ask one question at a time, with a recommended answer and its reason.
- Ask a question only when its prerequisites are settled.
- Restate each answer in one line before the next question.
- Never accept "everyone" as an audience. Never accept an adjective without its "but not" limit.
- On "skip" or "you decide", record the agent's proposal as ASSUMED.
- The user may end the interview at any time. Then every open required field is ASSUMED, and the loop stops without asking for the frontier to be empty.
- Questions use plain text, with no emoji headers.

It returns an answer record, one line for each field:

```
<brief section> | <field> | <value> | <stated | file:<path> | ASSUMED> | <observed | reported | assumed>
```

`gdh:align` reads the record as data, asks any required question that is still open, and hands the record to `gdh:design-brief`. During the interview `gch:grilling` writes nothing under `design/`, makes no spend call and uploads nothing. A fact look-up through a subagent is read-only.

## 3. What GDH gives GCH

GDH writes these files in the project. GCH needs no new convention to find them.

| File | Holds | Used by GCH for |
| --- | --- | --- |
| `DESIGN.md` | The design system in prose, with YAML front matter for colors and typography | Its "find the design system first" rule |
| `design/tokens.json`, `design/tokens.css` | Token values and generated custom properties | Tokens only; no raw values |
| `design/brief.md` | Subject, audience, primary job, use context, brand words, constraints, success measures | Scope and intent |
| `design/decisions.md` | Dated rounds: options shown, the choice, rejected options and reasons | What not to reopen |
| `design/assets/manifest.json` | Source, license, attribution, date, path and hash for each outside asset | License safety |
| `design/handoff.md` | Scope, decisions to keep, screens and states, motion table, acceptance checks, simplifications, open questions, evidence | The build contract |
| `design/reviews/` | Critique and accessibility reports | Known findings |

The `handoff-to-code` skill fills `design/handoff.md` and gives the user this start line for GCH:

```
The design is packaged in design/handoff.md.
Start the coding work with the GCH router and give it this brief:
- Goal and scope: section 1 of design/handoff.md
- Design system: DESIGN.md and design/tokens.json (tokens only; no raw values)
- Must keep: section 3. Acceptance checks: section 7. Open questions: section 9.
- Assets: design/assets/manifest.json. Do not add an asset without a record.
```

## 4. Who governs what when both are loaded

| Topic | Governs |
| --- | --- |
| How code is planned, written, tested and reviewed | GCH |
| Numbers for screens: target size, feedback timing, items at a decision point | GCH `ux-laws`. A GDH default gives way. |
| The brief, the direction, tokens, assets, motion intent, copy on screens | GDH |
| Spend and exposure gates for design tools | GDH |
| The decision record for design | GDH: `design/decisions.md` |
| Review of the rendered build against the design | GDH `design-critique` and `accessibility-gate`, on GCH's evidence captures |

The GDH kernel states this in one line: when the GCH kernel is loaded, GCH governs code work and its `ux-laws` numbers hold for screens. GDH copies no GCH kernel text.

Two context budgets load together. GDH keeps six model-invoked skills (`align`, `ask-gdh`, `design-brief`, `mood-board`, `find-assets`, `design-critique`), whose descriptions use about 3,300 of 5,000 characters, a kernel of 60 lines at most and a moments text of 3,500 characters at most, so that both fit.

## 5. Names

- In the Claude Code plugin, a GDH skill is `gdh:<name>`. The entry skill is `gdh:align`. The router is `gdh:ask-gdh`, and it runs after `gdh:align` closes.
- A GCH skill is named from GDH as `gch:<name>`, and only as an option when GCH is installed.
- Neither harness reaches the other's skill by file path.
- Six GDH skills are model-invoked: `align`, `ask-gdh`, `design-brief`, `mood-board`, `find-assets`, `design-critique`. The others are user-invoked: the Skill tool cannot start them, and `gdh:ask-gdh` loads each one by reading its `SKILL.md`. GCH hands off only to `gdh:align`, or to `gdh:ask-gdh` once `gdh:align` has closed.

## 6. Limits of the mechanism

1. A wired entry gives an install line only. The moments text cannot tell an installed GDH from a missing one. The "if the skill is listed" line in the hand-off block covers that case.
2. The offer is one for each session and each moment. After "Skip" the agent does not ask again.
3. On a host with no question tool, the user sees one closing line. The `what` text is short enough to read there.
4. A GDH change reaches installed users only after its version rises. Users then update the marketplace and run `/reload-plugins`. A session restart alone keeps the old version. Evidence: DOCUMENTED.
5. A reported trial in the GCH notes found that skills started far more often with a moments text than without one. That trial was small and was not rerun here. Evidence: UNTESTED.

## 7. To do on the GCH side

1. Add the wired entry of section 2.1.
2. In the screen moment named in section 2.2, replace the two offers with `gdh`. Add the new moment of section 2.2.
3. Add the block of section 2.4 to `kit/skills/ux-laws/SKILL.md`.
4. Add the feedback condition to the "Stay in GCH" rule of section 1, wherever GCH encodes it.
5. Remove the third-party design entries that GDH now carries.
6. Make GCH defer its own design interview or design brief to `gdh:align` when that skill is listed (section 2.6).
7. Add the words "caller contract" to the `gch:grilling` description and a "Caller contract" section that accepts the inputs, honors the loop rules and returns the answer record of section 2.7.
8. Run the GCH build, check and tests. Confirm its description budget still holds with both plugins loaded.
9. Start one session with both plugins. Confirm this order: the GDH offer, then `gdh:align`, then `gch:grilling` runs the questions one at a time, then `gdh:ask-gdh`. Confirm that "skip" records ASSUMED and "stop" ends the interview.
10. In the same session, ask "make the hero bolder" on a page GDH designed. Expect `gdh:ask-gdh`, then `refine-round` and a new entry in `design/decisions.md`, with no direct code change by GCH.
11. Ask for a new settings toggle inside the existing system. Expect GCH to keep it, with no GDH round.
12. Start one session with GCH alone. Confirm the offer appears once and that "Skip" is respected.
