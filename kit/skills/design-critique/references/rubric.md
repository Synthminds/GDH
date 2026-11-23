# The critique rubric

Read this file at step 13 of `design-critique`. It holds five scored dimensions, the band descriptors, the viewer passes and the verdict bands.

Evidence class: the rubric is a GDH default. The bands and cut-offs were not validated on real projects. The gates are not part of the score. A failed gate blocks delivery at any score.

## 1. Rules of scoring

- Score after you write the findings, not before. The score sums up the findings.
- Score each dimension from 0 to 4. Use whole numbers.
- A 4 means excellent. It does not mean acceptable. Most good work scores 3.
- Each score below 4 points to at least one finding. Each 4 points to one "working well" item.
- A `brand-required` choice never lowers a score.
- Score what you saw. A dimension you could not check gets "not scored", and the review says why.
- Record the scores of each round in the review file, so that progress is visible.
- Do not average several reviewers. List each reviewer's scores and discuss the gaps.

## 2. The five dimensions

### A. Brief fit

Question: does the work do the primary job for the named audience, in the stated context?

| Score | Descriptor |
| --- | --- |
| 0 | The work answers a different brief. The primary job is absent. |
| 1 | The primary job exists and is hard to find. Several brief requirements are missing. |
| 2 | The primary job is present. One or two requirements are missing or partly met. |
| 3 | Every requirement is met. The primary job is clear on the first view. |
| 4 | As 3, and each brand word is visible in type, copy and behavior. A stranger could reconstruct the brief from the work. |

Tests: the coverage list from step 6. The mission question: "Is this honestly what the brief asked for?" Answer yes or no with one sentence of evidence.

### B. Distinctiveness

Question: does the work belong to this subject, or would it fit any product in the category?

| Score | Descriptor |
| --- | --- |
| 0 | A current default look. Several confirmed tells. Framework defaults for type, color, spacing and components. |
| 1 | A default skeleton with a new skin. The swap test passes for most parts. |
| 2 | Some choices come from the subject. Two or more confirmed tells remain on open choices. |
| 3 | Palette, type and structure trace to the subject. At most one minor tell. One memorable element exists. |
| 4 | As 3, and the work breaks two or more named category conventions on purpose. It would look wrong under a competitor's name. |

Tests: the swap test. The competitor sheet: place the work beside five competitor screens and ask whether a reviewer can pick it out. The tell scan and the reviewer-only list in `tells.md`. A clean scan alone earns no score above 2.

### C. Hierarchy and clarity

Question: does the eye land where the brief needs it, and does the viewer know what to do next?

| Score | Descriptor |
| --- | --- |
| 0 | No reading order. Everything has the same weight, or everything shouts. |
| 1 | The first look lands on a secondary item. Several actions compete as primary. |
| 2 | The first look is right. The second and third are not. Groups are unclear. |
| 3 | First, second and third look match the content priority. One primary action for each view. Groups read by proximity. |
| 4 | As 3, and the order holds at every tested width, with long content, and in each state. |

Tests: compare the silent-look notes from step 5 with the priority order in the brief. The squint test: blur the screenshot and name what still stands out. Count the primary actions in each view. Default: one decision point asks the viewer to hold four items at most.

### D. System and craft

Question: is the work built from the system, and is the execution finished?

| Score | Descriptor |
| --- | --- |
| 0 | Raw values everywhere. No scale for type or space. Broken layout at a common width. |
| 1 | Tokens exist and many values bypass them. Visible alignment and spacing errors. |
| 2 | Mostly on tokens. Some off-scale values. Missing states: hover, focus, disabled, loading, empty or error. |
| 3 | Tokens only. Type, spacing and radius follow their scales. All states exist. Copy is specific. |
| 4 | As 3, and details are finished: balanced headings, tabular numerals where numbers compare, optical alignment, themed selection and focus. |

Tests: the checks of the discipline, from the owning skill. The tokens gate. The sprawl tells. Default: body measure of 45 to 75 characters. For code, review the render at each breakpoint and theme.

### E. Inclusion and trust

Question: can the whole audience use it, and does it deserve to be believed?

| Score | Descriptor |
| --- | --- |
| 0 | A gate fails: contrast, keyboard, color-only meaning, reduced motion, or an invented fact. |
| 1 | Gates pass on the default view only. Other themes, states or widths were not considered. |
| 2 | Gates pass where checked. Some checks are UNTESTED. Imagery or copy assumes one kind of user. |
| 3 | Gates pass in every theme and state checked. Facts have sources. The review names who might be excluded, and the work answers it. |
| 4 | As 3, and error, empty and failure states speak plainly and help the user recover. Limits and costs are stated where the user decides. |

Tests: the gate list in `SKILL.md`. The question "Who might we be excluding?" The worst case from the brief: is it handled? For the full accessibility checks, hand off to `accessibility-gate`. A score of 0 here always comes with a blocker finding.

## 3. Viewer passes

Walk the work as two or three of these viewers. Pick by the audience in the brief. Default: always include the first-timer, and include the keyboard and zoom user for any interactive work.

| Viewer | What they do | What to note |
| --- | --- | --- |
| First-timer | Arrives cold, with five seconds | Can they say what this is, who it is for and what to do next? |
| Daily user | Repeats the top task many times a day | Is the path short? Does anything animate or ask twice? |
| Keyboard and zoom user | Tabs through, zooms to 200 percent, uses a screen reader | Focus order, visible focus, reflow, names of controls |
| Phone in one hand | Small screen, thumb reach, bright light | Target size, reach of the primary action, contrast outdoors |
| Stress tester | Long names, empty data, slow network, an error | Does the layout hold? Does each state offer a next step? |
| Skeptic | Doubts every claim | Is each figure sourced? Is anything too good to be true? |

Write one line for each pass: what the viewer tried, where they stalled. A stall becomes a finding.

## 4. Verdict bands

Add the five scores. The total runs from 0 to 20.

| Condition | Verdict | Next step |
| --- | --- | --- |
| Any gate fails | Blocked | Fix the blockers. Review again. No other band applies. |
| 17 to 20, and no dimension below 3 | Ready | Fix the listed minor findings. Then `accessibility-gate` and `handoff-to-code`. |
| 13 to 16, or one dimension at 2 | Refine | One or two scoped rounds with `refine-round`. |
| 9 to 12, or any dimension at 1 | Rework | The direction may hold. The execution does not. Plan the rework with the user. |
| 0 to 8, or Brief fit or Distinctiveness at 0 | Return to direction | Go back to `mood-board`. When Brief fit is 0, return to `align` with the trigger 'an answer contradicts the brief'. |

When two rows apply, take the lower verdict.

By stage:

- Explore: score A and B only. Report them as two numbers out of 4. Do not state a verdict band. The question is which direction to pursue.
- Refine: score all five. Compare with the last review.
- Finalize: score all five. Only "Ready" allows hand-off.

## 5. Comparing options

When the review compares options, score each option on the same dimensions.

- Use a table with one column for each option.
- State one strength and one concern for each option.
- Do not name a winner from the totals alone. Say which option serves the primary job best, and what the user gives up.
- In an explore round, options differ in idea. In a refine round, two variants differ in one named attribute. Say which kind of comparison this is.

## 6. Worked scores

A landing page for a ferry timetable app, refine stage, second round.

| Dimension | Round 1 | Round 2 | Reason for the round 2 score |
| --- | --- | --- | --- |
| A. Brief fit | 2 | 3 | The next sailing now leads the first view. The cancelled-sailing state exists. |
| B. Distinctiveness | 1 | 3 | The card feed is gone. Rows follow the quay board. One tell remains: an uppercase label above two headings. |
| C. Hierarchy and clarity | 2 | 3 | One primary action. The status cell reads third, as intended. |
| D. System and craft | 2 | 2 | Eleven literal font sizes remain. The empty state is missing. |
| E. Inclusion and trust | 3 | 3 | Contrast pairs pass in both themes. Screen reader pass UNTESTED. |
| Total | 10 | 14 | |

Verdict in round 2: Refine. One dimension sits at 2. The next round is scoped to the type scale and the empty state.

## Sources

- Principles of Product Design (DesignBetter), ch. 4: goals frame every review.
- Aarron Walter, Designing for Emotion, ch. 2 and 5: brand contrast, "Who might we be excluding?".
- Impeccable critique rubric, read in part on 2026-11-23: the idea that the top score means excellent, the limit of four items at a decision point, and viewer personas. The dimensions and bands here are GDH's own.
- Nielsen Norman Group, usability heuristics: a further lens for app screens. Not read in this build.
