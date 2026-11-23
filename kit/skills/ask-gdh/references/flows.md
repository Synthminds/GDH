# Standard flows

Seven flows cover most requests. Each step names the skill, what it must produce, and when you may skip it.
A flow is a default order. The user can reorder it. The gates stay.

`align` is not a step of any flow. It ran once, at the start of the session, and wrote the brief through `design-brief`. Each flow names the brief it needs in a "Brief must hold" line above its table. When the brief lacks a part, return to `align` as an escalation for that topic (`align`, realign reference, sections 3 and 5). Do not plan around the gap, and do not run `align` a second time.

Start each skill as `ask-gdh` step 9 says. Most flow skills are user-invoked: read the skill's `SKILL.md` and follow it. The Skill tool cannot start them.

Gates in every flow:

- `align` has closed in this session, and `design/brief.md` reads `Status: confirmed YYYY-MM-DD by <who>`, before any look is chosen.
- A direction is chosen before a full build, unless a strict design system fixes the look.
- Spend gate before each spend call. Exposure gate before each publish, share or upload.
- `design-critique` and `accessibility-gate` pass before `handoff-to-code`.
- Each round ends with an entry in `design/decisions.md`.

## 1. New brand

Use when no identity exists, or the user wants a new one.

Brief must hold: the full design persona.

| # | Skill | Must produce | Skip when |
| --- | --- | --- | --- |
| 1 | `mood-board` | Three directions, one chosen, rejected ones logged | The request is a mark only; `logo-identity` runs its own concept round |
| 2 | `logo-identity` | Mark concepts inside the chosen direction; one mark chosen; a vector mark system, tested small and in one color | The user keeps an existing mark |
| 3 | `typography` | Families by role, a scale, license records | The direction fixed them and licenses are recorded |
| 4 | `color` | Palette with roles, themes, measured contrast pairs | The direction fixed them and pairs are measured |
| 5 | `design-system` | `design/tokens.json`, `DESIGN.md`, a brand pack | Never |
| 6 | `design-critique` | Findings against the brief, on one real application | Never |
| 7 | `accessibility-gate` | Pass table for color and type | Never |
| 8 | `handoff-to-code` | `design/handoff.md` | No code follows |

Why this order: the mark comes after the direction, so it expresses the idea and does not set it. The user chooses a direction once, in `mood-board`. Tell `logo-identity` the chosen direction: its concept round then chooses a mark, not a second direction. Type and color come after the mark, so the wordmark and the text face agree. Tokens come last, so they record decisions and do not make them.

Spend points: concept generation in `logo-identity`. Exposure points: a trademark screening upload, a shared board.

## 2. New website or app

Brief must hold: a real content list.

| # | Skill | Must produce | Skip when |
| --- | --- | --- | --- |
| 1 | `reverse-engineer-reference` | Structure notes on named references | The user named no reference |
| 2 | `mood-board` | Directions with one real first view each; one chosen | Design system is `strict` |
| 3 | `design-system` | Tokens and `DESIGN.md` from the chosen direction | A strict system exists |
| 4 | `website-design` or `app-design` | The build, all states, each breakpoint | Never |
| 5 | `find-assets`, `generate-media`, `ui-motion` | Assets with records; motion with tokens | Not needed |
| 6 | `design-critique` | Ranked findings | Never |
| 7 | `refine-round` | Scoped changes; decision entries | The critique passes and the user approves |
| 8 | `accessibility-gate` | Pass table | Never |
| 9 | `handoff-to-code` | `design/handoff.md` | The build is the final code and no other agent continues |

Rule: test the chosen direction on one real screen before the full build. A direction that fails on the densest screen is not chosen yet.

Spend points: generated imagery. Exposure points: deploy, preview links, upload of content to a builder.

## 3. Dashboard

Brief must hold: the decisions the screen supports, who makes them, and how often.

| # | Skill | Must produce | Skip when |
| --- | --- | --- | --- |
| 1 | `design-system` | Found or created tokens, with a data color set | A strict system has data colors |
| 2 | `data-viz` | Chart choice for each question, with the finding stated | Never |
| 3 | `dashboard-design` | Layout, hierarchy, states (loading, empty, error, stale) | Never |
| 4 | `design-critique` | Findings; the one-glance test result | Never |
| 5 | `accessibility-gate` | Pass table, with series told apart without color | Never |
| 6 | `handoff-to-code` | `design/handoff.md` | No code follows |

`mood-board` is optional here. Run it with two directions when no design system exists. A dashboard's direction lives in density, type and data color, not in imagery.

Rule: use real data or a labelled sample. Invent no numbers.

## 4. Infographic

Brief must hold, at light size: the reader, the one message, where it is shown, the sources.

| # | Skill | Must produce | Skip when |
| --- | --- | --- | --- |
| 1 | `data-viz` | A chart for each number that carries the message | The piece holds no data |
| 2 | `mood-board` | Two directions as small layout sketches | A strict system exists |
| 3 | `infographic` | One reading path, sourced numbers, final file | Never |
| 4 | `find-assets` | Icons and illustrations with records | None used |
| 5 | `design-critique` | Findings; the message read back by a fresh reader | Never |
| 6 | `accessibility-gate` | Pass table; text alternative for the whole piece | Never |

Rule: every number carries its source on the piece. A number with no source is removed or labelled as an estimate.

## 5. Motion piece

Brief must hold: message, audience, platform, length, where it plays, with or without sound.

| # | Skill | Must produce | Skip when |
| --- | --- | --- | --- |
| 1 | `mood-board` | Styleframes: two or three still frames for each direction; one chosen | A strict system with motion tokens exists |
| 2 | `motion-video` | Script, storyboard, animatic, final render | Never |
| 3 | `generate-media` | Footage, voice or music, each with quote and consent | All material is code-drawn or owned |
| 4 | `find-assets` | Music, sound or stock with records | None used |
| 5 | `design-critique` | Findings on a watch-through with sound off, then on | Never |
| 6 | `refine-round` | Scoped changes by timecode | Approved |

Rule: lock the script before the storyboard, and the storyboard before any paid generation. A change after generation costs a second spend.

Spend points: every generation and some renders. Exposure points: upload of a voice sample or a likeness, publishing to a platform.

## 6. 3D hero

Brief must hold: what the model shows, why 3D and not an image, the target devices.

| # | Skill | Must produce | Skip when |
| --- | --- | --- | --- |
| 1 | `mood-board` | Directions with material, light and camera notes | A strict system exists |
| 2 | `three-d` | A sourced or generated model, optimized, with a static fallback | Never |
| 3 | `find-assets` or `generate-media` | The model or its textures, with records | `three-d` already recorded them |
| 4 | `website-design` | The model placed in the page, with load and fallback states | The model ships alone |
| 5 | `accessibility-gate` | Pass table; reduced-motion and no-WebGL fallback | Never |
| 6 | `handoff-to-code` | `design/handoff.md` with budgets as measured | No code follows |

ASK in step 1: "What does 3D do here that a still image cannot?" With no answer, propose an image or a short video.

Default budgets are rules of thumb. Measure on the target device and record the result as VERIFIED.

## 7. Refresh of an existing product

Brief must hold: what must stay, what may change, and why now. `align` asks these at session start, as a re-alignment in mode refine. With no brief, it runs the full interview first.

| # | Skill | Must produce | Skip when |
| --- | --- | --- | --- |
| 1 | `design-system` | The existing look recorded as tokens (import mode) | A written system exists |
| 2 | `design-critique` | An audit of the current product: what works, what fails, ranked | Never |
| 3 | Escalation check | Compare the audit with the brief. When a finding contradicts a "must stay" line, return to `align` with the trigger "an answer contradicts the brief". It runs only that escalation, then closes | No finding contradicts the brief |
| 4 | `mood-board` | Two directions: one close to today, one further | The user wants fixes only |
| 5 | `refine-round` | Changes in scoped rounds, one area for each round | Never |
| 6 | `accessibility-gate` | Pass table, compared with the audit | Never |
| 7 | `handoff-to-code` | `design/handoff.md` with a migration order | No code follows |

Step 3 is an escalation inside the session, not a second run of `align`.

Rules:

- List what must stay before anything changes: the mark, the brand color, key layouts users know.
- Keep the copy and the identity unless the user asks for a change.
- Change the highest-traffic screen first. It proves the direction.
- A refresh that grows into a rebrand changes the mode. Stop, ask and log it.

## Flow failure patterns

| Pattern | Sign | Correction |
| --- | --- | --- |
| Tokens first | A palette and a scale exist before any direction was chosen | Run `mood-board`. Then rebuild tokens from the choice. |
| Asset first | A hero image is generated before the brief | Stop spending. Run `align`. |
| One-direction board | Three boards, one idea, three palettes | Send back to `mood-board` with the difference test. |
| Gate at the end only | Contrast fails after forty screens are built | Run `accessibility-gate` on the direction's palette in the mood board. |
| No record | A round ends in chat only | Write the entry before the next skill starts. |
