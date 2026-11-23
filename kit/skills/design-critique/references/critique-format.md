# The critique format

Read this file at step 11 of `design-critique`. It fixes the order of a review, the shape of a finding, the severity scale, the evidence rules, the wording rules and the review file.

## 1. The order of a review

A review always runs in this order. Do not skip a part. Do not reorder.

1. Frame. Restate the goal and the constraints. Name the stage and the decision needed.
2. Questions. List the one to four questions this review answers.
3. Silent look. Write what is seen first, second and third. No judgement.
4. Coverage. Mark each brief requirement met, partly met or missing.
5. Required choices. List what the user or the design system prescribes.
6. Findings, worst first.
7. Working well.
8. Scores and verdict.
9. What was not checked.

Why this order: a reviewer who knows the goal gives useful feedback. A reviewer who looks before reading the rationale keeps a fresh eye. Observation before opinion keeps the review on the work.

## 2. The frame

Three lines, taken from the brief. Do not pitch the design and do not explain its intent.

```
User goal: <what the audience needs to do>
Business goal: <what the owner needs from it>
Constraints: <brand, legal, technical, time>
Stage: <explore | refine | finalize>. Decision needed: <the decision>.
```

Match the review to the stage:

| Stage | Judge | Do not judge |
| --- | --- | --- |
| explore | The idea, its fit to the brief, the difference between options | Pixel detail, final copy, missing states |
| refine | The parts in scope for this round | Parts the user already approved, unless a gate fails |
| finalize | Defects: gates, broken states, drift from tokens | Direction. It is settled. Log a doubt under "Open" |

A gate failure is reported at every stage.

## 3. The silent look

Look at the render before you read the code or the maker's notes. Write three lines.

```
First: <the element the eye lands on>
Second: <the next>
Third: <the next>
Five-second read: <what a new viewer would say this is and what to do next>
```

Compare these lines with the priority order in the brief. A mismatch is a finding under "Hierarchy and clarity".

For work you made yourself, the silent look has less value. Say so, and use the `design-critic` agent or a fresh context when the host allows it.

## 4. A finding

Every finding has the same fields.

```
### <n>. <short title> [<severity>]
Where: <evidence>
Observation: <what is there, as a fact a second viewer can confirm>
Impact: <who is affected, at which task, and which goal or brand word it harms>
Criterion: <the brief line, token rule, discipline check, gate or tell code>
Suggestion: <one direction to explore, in one sentence>
```

Rules for each field:

- Observation. A fact, not a verdict. "The primary button and the two links share one weight" is an observation. "The hierarchy is weak" is not.
- Impact. Name a person and a task. Tie it to a goal, a constraint or a brand word from the brief. An item with no impact is a preference. Label it "preference" or delete it.
- Criterion. One of: a line of the brief, a rule in `DESIGN.md`, a check from the owning skill, a gate, a tell code. Taste alone is not a criterion.
- Suggestion. A direction, not a design. One sentence. It may offer two directions to compare. It never holds code, a mockup or a full replacement.

One problem is one finding. Do not join two problems with "and". Do not list one problem five times; note the count and the first place.

## 5. Evidence

A finding without evidence is not reported. Use one of these forms.

| Kind of work | Evidence form | Example |
| --- | --- | --- |
| Rendered page or screen | Screenshot file, viewport, and a region | `shots/home-390.png`, 390 px wide, region x 0, y 520, w 390, h 240 |
| Code | A selector, or file and line | `.pricing .card:nth-child(2) .cta`; `src/Hero.tsx:42` |
| Canvas or slide | The artboard or slide name, and the element name | Artboard "B Tide Line", layer "status cell" |
| Token file | The token name | `color.text-muted` on `color.surface-raised` |
| Scan result | The code and the place | `TELL_GLOW_SHADOW` at `src/card.css:8` |
| Measurement | The number and how it was measured | Contrast 3.9:1, computed from the two token values |

Rules:

- State how a number was obtained: computed from tokens, measured on the render, or read from source.
- A region uses pixels of the screenshot named. Give the viewport width.
- When you did not render the work, say "from source only" on each finding that needs a render.
- Follow the check rule of an artifact type. When the type says not to render to check, review from the files and say so.

## 6. Severity

| Severity | Meaning | Examples | What happens |
| --- | --- | --- | --- |
| blocker | A gate fails, or the primary job cannot be done | Body text at 3.2:1. An invented customer count. No keyboard path to the main action | Delivery stops until it is fixed or the user records an exception |
| major | The primary job is harder, or a brand word is contradicted, for much of the audience | The next sailing sits below the fold. A confirmed default-look tell on the hero | Fix in the next round |
| minor | A real defect with a workaround, or a problem on a secondary path | Eleven font sizes. A missing empty state on a rare view | Fix when the part is touched |
| note | A polish item or a labelled preference | A heading that would balance better on two lines | The maker decides |

Mapping the tell scan: a `high` tell on content (placeholder text, an unsourced figure) is a blocker. Other `high` tells start as major. `medium` starts as minor, or major when it sits on the first view. `low` starts as a note. Confirm each on the render before you set the severity.

Do not inflate. A review where everything is major tells the maker nothing. Default: at most seven findings in the chat report.

## 7. Wording

- The subject of each sentence is the work. Write "the heading wraps to four lines". Never write "you made the heading too long".
- No verdict words without a fact: avoid "bad", "ugly", "amateur", "boring".
- No praise words without a fact: "working well" items also name an element and the goal it serves.
- No redesign. The review does not replace the layout, rewrite the copy or attach a new mockup.
- A question is allowed when you cannot tell the intent: "Is the second button meant to be equal to the first?"
- Report a `brand-required` choice once, in its own list, with its source. Add no opinion to it.
- When you disagree with a required choice on grounds of a gate, raise the gate. Do not relabel the choice as a tell.
- Quote feedback from other reviewers with its source. Mark relayed feedback as "relayed".

## 8. The review file

Write `design/reviews/<YYYY-MM-DD>-<scope>.md` in this shape.

```
# Review: <scope>

Date: <YYYY-MM-DD>. Stage: <stage>. Reviewer: <design-critic agent | single-context | name>.
Reviewed: <files, screens, artboards>, as <rendered at widths and themes | from source only>.
Tell list: <version>.

## Frame
User goal:
Business goal:
Constraints:
Decision needed:
Questions: 1. ... 2. ...

## First look
First: / Second: / Third: / Five-second read:

## Brief coverage
| Requirement | Status | Where |

## Required by the user or the design system
| Choice | Source |

## Findings
### 1. <title> [blocker]
Where: / Observation: / Impact: / Criterion: / Suggestion:

## Working well
- <element>: <the goal it serves>

## Scores
| Dimension | Score | Last review |
Verdict: <band>

## Not checked
- <what>: <why>

## Answers to the questions
1. ...
```

## 9. A worked finding set

Review of a ferry timetable home screen, refine stage. Questions: "Is the next sailing clear?" and "Does the page still look like a template?"

```
### 1. Cancelled sailing is marked by color alone [blocker]
Where: shots/home-390.png, 390 px wide, region x 16, y 412, w 358, h 44; selector .row.is-cancelled
Observation: The cancelled row differs from the other rows only by red text. It has no icon and no word.
Impact: A commuter who cannot tell red from black reads the 8:10 as running, and misses the 7:40.
Criterion: Gate: color is never the only carrier of meaning.
Suggestion: Explore a status word in the row end cell, with or without a strike on the time.

### 2. The page opens with a centered title and three equal cards [major]
Where: src/Home.tsx:12 and :31; TELL_HERO_THREE_CARDS
Observation: A centered h1 is followed by a three-column grid of identical cards: "Timetable", "Tickets", "Alerts".
Impact: The first view does not show the next sailing, which is the primary job. The chosen direction is a table of rows.
Criterion: Brief, primary job; direction file A, layout skeleton "table-led".
Suggestion: Explore moving the next-sailing row to the first view, and test whether the three cards are needed at all.

### 3. Eleven literal font sizes [minor]
Where: TELL_FONT_SIZE_SPRAWL, first at src/styles.css:14
Observation: The stylesheet sets eleven distinct font sizes. The type scale in DESIGN.md has six steps.
Impact: Rows that should match differ by one pixel, which breaks the board rhythm the direction relies on.
Criterion: Gate: tokens only. DESIGN.md, Type.
Suggestion: Map each size to a scale step and list any size that has no step.
```

Working well:

- The status cell at the row end: it reads third, as the brief's priority order asks.
- Signage type with tabular numerals: times line up, which serves "dependable".

Required by the design system: the amber fill on the primary action (`DESIGN.md`, Color). Reported once. Not a finding.

What this set does not do: it does not redraw the row, rewrite the labels or pick the icon. Those are the maker's decisions in the next round.

## 10. After the review

- Give the user the top findings and the verdict. Ask which findings to change.
- For each finding, the user decides: accept, decline with a reason, or defer. `refine-round` records that in `design/decisions.md`.
- A declined blocker needs a recorded exception from the user. Say what the exception costs.
- Keep the review file. The next review compares against it.

## Sources

- Principles of Product Design (DesignBetter), ch. 4: frame, questions, silent look, specific feedback tied to goals, feedback not solutions.
- Design Collaboration Handbook (DesignBetter), ch. 2: ask what was meant before you judge.
- Design Leadership Handbook (DesignBetter), ch. 4 and 5: status labels on artifacts, a disposition for each item.
- Liz Lerman, Critical Response Process: statements of what was seen come before opinions.
