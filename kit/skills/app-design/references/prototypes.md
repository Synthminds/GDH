# Prototypes at the right fidelity

Read this file at steps 16 to 19 of `app-design`. It covers the purpose statement, the fidelity ladder, the choice of prototype type, data in prototypes, review on the target device, and test rounds with people.

A prototype answers a question. It is not a small version of the product. The cheapest artifact that answers the question is the right one.

## 1. The purpose statement

Write it before you build. Show it to the user and get a yes.

```
Prototype goal: <explore | validate> how <the person or role>
handles <the problem> in <the situation>.
We believe <the hypothesis>.
We will know from <what we will watch or ask>.
It covers <the flows in scope>. It does not cover <what is stubbed or left out>.
```

Rules:

1. One statement, one question. A second question is a second prototype or a later round.
2. Build only the parts that the question needs. Stub the rest, and mark each stub.
3. Work that does not serve the statement waits.
4. After the review, write one line: the hypothesis held, failed or is still open.

## 2. The fidelity ladder

Fidelity follows confidence. Low confidence and many possible answers mean low fidelity.

| Rung | What it is | It answers | It cannot answer | Cost |
| --- | --- | --- | --- | --- |
| 1. Text flow | The flow map and the screen inventory | Is the path right? Are steps missing? | How it feels | Minutes |
| 2. Gray boxes | Boxes with real labels, linked by taps | Can a person find the way? Is the structure right? | Whether the content works | Under an hour |
| 3. Static, real content | Styled screens with real copy and plausible data | Is the content right? Does the hierarchy work? | Interaction, timing, edge cases | Hours |
| 4. Clickable | Linked screens that move through the top flow | Does the flow hold together? | Real input, real data, performance | Hours |
| 5. Coded, mock data | Real components, real input, invented but realistic data | Interaction, states, responsiveness, motion | Behavior with real data | A day or more |
| 6. Coded, real data | The same, with a real or realistic dataset | Edge cases, empty and extreme values, feasibility | Scale and production load | More |

The cost column is a rough guide, not a measurement.

Rules:

1. Start at the lowest rung that can answer the question.
2. Move up one rung only when the question at the current rung is answered. Write the reason for the move.
3. Rungs 1 and 2 come before any styled screen. The user sees them and answers keep, change or remove.
4. A polished prototype for an idea with no agreed direction is a failure of process, not progress.
5. Show unfinished work as unfinished. Rough work invites comments on the idea. Polished work invites approval or rejection.
6. No more than one rung passes between user checkpoints.

## 3. Choose the type by the question

| The open question | Prototype type |
| --- | --- |
| Is the information architecture right? | Gray boxes, clickable |
| Do people understand the words and the content? | Static with real content |
| Does the top task take too many steps? | Clickable, timed by hand |
| How should this interaction or gesture feel? | Coded, on the target device |
| Do the loading, error and offline states work? | Coded, with a mock that can be slow, fail and go offline |
| Does the layout hold with real values? | Coded, with real or realistic data |
| Can it be built in this stack? | A technical spike by the coding harness, not a design prototype |
| Which of two designs is better for one attribute? | Two variants that differ in that attribute only |

For a gesture, a prototype on real hardware is the only honest test. A simulator hides friction.

## 4. Routes and tools

| Rung | Route | Notes |
| --- | --- | --- |
| 1 | A text file, or a diagram by capability `diagram` | The text form lives in `app-plan.md` |
| 2 to 4 | A design canvas through the `claude-design` skill, or local HTML | An artifact follows its type's own check rule |
| 5 to 6 | Code in the project stack | With GCH installed, `gch:prototype` builds coded variants |
| 5 to 6, when the user names a builder | A prompt-to-code builder | A spend call. The builder's flow leads |

Rules:

1. Use the stack and the component library that the project already has. Rebuilding buttons wastes the prototype's time.
2. With no library, use unstyled primitives and project tokens.
3. Label every code artifact "prototype". Prototype code does not ship without the production checks.
4. Build for change: one design value changes in one place.
5. Keep each idea on its own branch or folder. The user or the coding harness runs version control.
6. GATE: a paid generation or a builder run is a spend call. Prefer free and owned tools at this stage. Paid generation waits until a direction has passed a test.
7. GATE: a share link or a hosted preview is exposure. Ask first.
8. Keep the prototype cheap enough to throw away. A prototype that cost too much to discard stops you from acting on feedback.

## 5. Data in a prototype

1. Use mock data in anything that will be shared. No real names, addresses, account numbers or messages, unless the user approved real data for this test.
2. Make mock data realistic: real lengths, real ranges, awkward cases. Tidy data hides layout failures.
3. Include the extremes: no data, one item, far too many items, a very long name, a zero, a negative value, a missing field.
4. Label sample data as sample where a viewer could take it for real.
5. Before sign-off of a data-heavy screen, render it once with a real or realistic dataset. A screen seen only with invented "nice" data is unproven.
6. A mock can be slow, can fail and can go offline, on demand. Without that, the states cannot be reviewed.

## 6. Review at the target

1. Review at the target viewport: phone width for a phone app, a resizable window for a desktop app.
2. Review on the target device when one is available. Touch, text size and brightness differ from a desktop browser.
3. Walk the top task from the entry point to the confirmed finish.
4. Walk it again with the system set to large text, to dark mode and to reduced motion.
5. Trigger each state in the matrix.
6. Label honestly. "VERIFIED at a 390 px viewport in a desktop browser" is not "verified on a phone".
7. For a coded prototype, the rendered check is a gate. For an artifact, the type's own rule governs.

## 7. Feasibility pass on the prototype

Before a test with real users, get a build-side check.

- Hand the prototype and the feasibility table to the code owner, or to the coding harness.
- Ask three things: is each shown field available, are the required fields all present, does any interaction fight the platform?
- Record the answer as a feasibility note in `app-plan.md`, with who gave it.
- A "no" changes the prototype before any user sees it.

## 8. Test with people

Test inside the team first. Colleagues find the obvious problems for free. Then test with people who match the brief.

| Step | Do |
| --- | --- |
| Recruit | A short screener that filters for the role in the brief. State the thanks or payment |
| Size | Default: about 5 people in a round, then revise, then test again. The source reports this as a finding from usability research; this kit did not verify it |
| Script | Five parts: welcome, warm-up questions, introduction of the prototype, tasks, debrief |
| Tasks | Taken from the job stories. Stated as goals, not as instructions on where to tap |
| During | Do not help. Do not explain. Note where the person hesitates, and their words |
| Record | With consent. Notes are shared with the team soon after |
| After | One or two key findings from each session, each with a quote or an observation |

For a customer test, make the prototype realistic enough that the roughness does not become the topic. For an internal concept review, keep it rough on purpose.

The agent's part: write the screener, the script and the tasks; prepare the mock states; turn notes into findings. The agent does not invent a test result. With no test run, the report says UNTESTED.

## 9. After the round

1. Write the hypothesis verdict.
2. List what changed and what was rejected, with reasons, in `design/decisions.md`.
3. Raise fidelity only if the question was answered.
4. Stop when the brief's requirements are met, the gates pass and the user approves.

## 10. Worked example

The invented inspection app.

Purpose statement: "Prototype goal: validate that a technician can log an inspection with one hand, in a lift shaft with no signal. We believe three visible answers for each question, saved on the device at once, will let them finish in under two minutes. We will know from timing five technicians and counting mis-taps. It covers the Today list to the confirmation. It does not cover history, profile or the office web app."

- Rung 2 first: gray boxes of the six steps. The user removed the summary step.
- Then rung 5, skipping the static rungs. Reason recorded: the open question is about touch and offline behavior, which a static screen cannot answer.
- The mock can go offline and can fail a submit. Data: forty invented lifts with real-length names, one with no past inspection.
- Feasibility pass by the code owner: the signature field was missing. Added before any technician saw it.
- Review: VERIFIED in a browser at a 360 dp viewport with large text. A test with gloves on a real phone is planned and is UNTESTED today.
- Spend: none. Exposure: one hosted preview link for the five testers, approved by the user.

## 11. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| No question | A prototype with no purpose statement | Write the statement. Cut what it does not need |
| Too polished, too early | Styled screens before the flow was agreed | Go back to gray boxes |
| Whole product | Every screen built, most testing nothing | Scope to the open questions |
| Precious prototype | Feedback is resisted because the build was costly | Use a cheaper route next time. Say the cost now |
| Tidy data | Every name is short and every list has six items | Add the extremes |
| Desktop proof | A phone flow approved in a wide desktop window | Review at the target viewport |
| Helping hand | The moderator explains the screen during a task | Follow the script |
| Invented finding | "Users liked it" with no session behind it | Report UNTESTED |
| Prototype shipped | Prototype code merged as production | Label it. Run the production checks through `handoff-to-code` |

## 12. Checks

Gates:

- A purpose statement exists and the user agreed to it.
- Gray-box flows were shown before any styled screen.
- No shared prototype holds real personal data without the user's recorded yes.
- A coded prototype was reviewed as rendered at the target viewport.
- No test result is reported that was not observed.

Defaults:

- Default: the lowest rung that answers the question.
- Default: about 5 people in a test round.
- Default: free and owned tools for prototypes; paid generation only after a direction passed a test.
- Default: one rung between user checkpoints.
