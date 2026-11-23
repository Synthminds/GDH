# AI-product patterns

Read this file at step 14 of `app-design`, when a feature calls a model. It covers four design problems that a model adds to a screen: latency, uncertainty, correction and provenance. It also covers memory and limits, and the state list for an AI entry point.

Evidence. These patterns are GDH defaults. No primary design source for them was read in the research. The vocabulary of runtime layers comes from one vendor whitepaper, which is marketing and is used for vocabulary only. Label every pattern here UNTESTED until the project tests it with real people.

Kernel rule 11 has a special weight here. A model can state false things in a confident voice. The interface must never add confidence that the system does not have.

## 1. Scope the AI feature first

Add these lines to the brief before any screen. ASK for each one the brief does not answer.

```
AI feature: <name>
Archetype: <assistant that answers | agent that acts | prediction or ranking in the background>
What it does for the person: <one sentence from a job story>
What it must never do without a yes: <list of actions>
Stakes of a wrong output: <low: easy to notice and undo | medium | high: costly or hard to notice>
Targets: speed <...>; accuracy <...>; memory <...>; scale <...>  (or "not a priority")
Runtime layers in scope: memory <y/n>; retrieval <y/n>; cache <y/n>; routing <y/n>; limits <y/n>
```

Rules:

1. Name capabilities, not products. The coding harness picks the stack unless the user chose one.
2. The stakes line decides how much confirmation, preview and provenance the design needs.
3. An agent that acts needs an approval step for every action on the "never without a yes" list.
4. Ask whether the job needs a model at all. A filter, a template or a rule is faster and never wrong in this way.

## 2. Latency

A model call is slow and its duration varies. Some answers return almost at once, from a cache or a short path. One loading pattern cannot serve both.

| Path | What the person sees | Rule |
| --- | --- | --- |
| Fast: the answer is ready almost at once | The answer, with no loader | Do not flash a loader. Delay any busy sign briefly |
| Slow: the model is working | Their own input echoed at once, then output as it arrives | Show the first sign of work immediately. Stream when the system can |
| Long: many seconds or minutes | Real steps as they happen, partial results, a stop control | Let the person leave and return. Notify on finish |
| Background: no one is waiting | Nothing while it runs. A result later, marked new | Never block the screen for it |

Rules:

1. Echo the person's request at once. The wait then starts from a confirmed send.
2. Show a stop control for the whole time the model works. Stopping keeps what arrived.
3. Streamed text must not move the layout that the person is reading. Grow downward. Do not re-flow earlier lines.
4. Progress shows real steps from the system. Never show an invented step list or a fake percentage.
5. Keep the rest of the screen usable during a call.
6. The input stays editable, and the last request can be recalled.
7. Default wait tiers are in the states reference. With GCH loaded, its feedback number governs.
8. Test both paths with a throttled mock and an instant mock. A design tested only at one speed fails at the other.

## 3. Uncertainty

The output can be wrong, partial or made up. The design sets the right level of trust and makes a wrong output cheap to catch.

| Tool | Use it when | Do not |
| --- | --- | --- |
| A plain label that content is generated | Always, where generated and human content mix | Hide the label in a footer |
| Grounding shown: what the answer is based on | The system retrieves sources | Imply grounding when the model answered from itself |
| A designed "no answer" state | The system finds nothing reliable | Fill the gap with a guess |
| Hedged wording in the answer itself | The system reports low confidence | Show a number that the system does not really compute |
| A preview or a diff before a change applies | The output will change the person's data | Apply first and explain later |
| A confirmation that names the action | Medium and high stakes | Use "Are you sure?" with no detail |
| A second route: search, a human, the manual way | High stakes, or when the model fails | Make the model the only route |

Rules:

1. Never show a confidence score, a rating or a "verified" mark that the system does not produce.
2. Say the limits at the point of use, in one plain line. A general disclaimer elsewhere does not replace it.
3. Scale the friction to the stakes. Low stakes: apply and offer undo. High stakes: preview, confirm, log.
4. Do not give the model a human face or voice that suggests judgment it does not have, unless the brief asks and says why.
5. "I could not find that" is a good answer. Design it as carefully as a successful one.
6. Numbers, names, dates and quotes in generated text are the likeliest errors. Where the stakes are high, link each to its source or mark it unchecked.

## 4. Correction

People must be able to fix the output and steer the next one. Correction is part of the main flow, not a recovery path.

| Level | The person can | Design |
| --- | --- | --- |
| The request | Edit and resend the last request | The request stays visible and editable |
| The output | Edit the result directly | Generated text is ordinary, editable content |
| Parts of the output | Accept or reject each change | A change list or a diff, with accept and reject for each item |
| Alternatives | Ask again and compare | Keep earlier results reachable. Do not overwrite |
| Direction | Steer while it works | The stop control, then a follow-up that keeps context |
| Applied actions | Undo what the agent did | An action log with undo for each reversible step |
| The future | Tell it a standing preference | A visible memory, with edit and delete |
| The product team | Rate the output | A rating with a reason. Say what the rating does |

Rules:

1. Regenerating never destroys the earlier result without a way back.
2. A rejected suggestion does not come back in the same session.
3. After a manual edit, the system does not overwrite the edit on the next generation.
4. An agent shows its plan before a multi-step run when the stakes are medium or high. The person can change the plan.
5. Every action the agent takes on the person's behalf is listed, with what it changed.
6. Feedback controls are honest. If a rating changes nothing for this person, do not suggest that it does.

## 5. Provenance

Provenance answers three questions: where did this come from, what was used, and who or what made it.

Decide each line and record it. "Not shown" is an allowed answer; an undecided line is not.

```
Sources shown: <yes, as inline citations | yes, as a list | no: reason>
Generated content marked: <how and where>
Data scope shown: <which documents, accounts or dates the answer used>
Freshness shown: <date of the data | not applicable>
Route shown: <which model or tool answered: yes | no: reason>
Action log: <where the person sees what the agent did>
Export: <what label or attribution travels with exported content>
```

Rules:

1. A citation links to the exact passage, not to the top of a long document.
2. The interface renders only the sources that the system returns. It never formats a made-up reference.
3. Design the answer with zero sources. Say that no source supports it.
4. Keep generated and human-written content distinguishable where both live in one document.
5. Show the date of the data when a stale answer could mislead.
6. When content leaves the app, its label leaves with it. Some platforms require a disclosure for generated media; confirm the current rule for each platform in the brief.

## 6. Memory

When the app remembers things about a person, every later answer changes. A person who cannot see the memory cannot explain or fix the behavior.

- Show what the app remembers: standing instructions, preferences, facts, exclusions.
- Let the person edit and delete each item.
- Say when something new was remembered, at the moment it happens.
- Say what lasts for this session only and what lasts across sessions.
- The person should never need to repeat a standing instruction.
- ASK about privacy rules for stored personal data. Do not decide retention in a design file.

## 7. Limits and fallbacks

A model has usage limits, costs and outages. Each one is a state.

| State | The person sees |
| --- | --- |
| Near a limit | Remaining use, where plan tiers differ |
| At a limit | What was reached, when it resets, and what they can do now |
| Degraded | That a simpler path answered, when the difference matters to them |
| Refused | That the request cannot be done, in plain words, with what they can do |
| Failed | That it failed, that their input is kept, and a retry |

Limit numbers come from configuration, never from fixed copy. The design leaves room for the real value.

## 8. The state list for an AI entry point

Each place where a person calls the model needs these states. Add them as rows to the state matrix.

| State | Note |
| --- | --- |
| Idle | The input, with example requests taken from real job stories. No invented capabilities |
| Composing | Attachments, scope and options visible |
| Waiting | The request echoed. A first sign of work. Stop available |
| Streaming | Output arrives. The layout above stays still |
| Answered, fast path | No loader was shown |
| Answered, slow path | The loader left without a jump |
| Stopped or partial | What arrived is kept and marked incomplete |
| No answer | Nothing reliable found. A second route offered |
| Needs approval | The plan or the change, with accept, edit and reject |
| Limited | Cause, reset time, next step |
| Failed or fell back | Input kept. Retry. The fallback named when it matters |

Count them. Fewer than these, for a feature that can reach them, is a gap in the design.

## 9. What goes to the coding harness

The design owns the states, the words and the visible behavior. The code owns storage, thresholds and enforcement. Split them in the handoff.

`handoff-to-code` carries a runtime-behavior sheet for an AI feature: one section each for memory, retrieval, cache, routing and limits. Each line says in scope or not, who owns it, and whether it is needed for the prototype or for production. Values that the code chooses later, such as a limit number, return to the design as a copy change.

Start with one thin slice: one real request, end to end, with real data. Sign off the full design after that slice works. A model feature that was designed only in mockups meets its real latency and its real errors too late.

## 10. Worked example

The invented inspection app adds one AI feature: "Summarize this lift's history" for the office web app.

- Archetype: an assistant that answers. Stakes: medium. A wrong summary could hide a repeated fault.
- Does it need a model? A filter already lists past failures. The model adds a plain-language summary over free-text notes. The filter stays as the second route.
- Latency: the summary takes seconds. The request echoes, text streams into a fixed panel, and a stop control shows. The list of inspections beside it stays usable.
- Uncertainty: the panel is marked "Generated summary". No confidence number appears, because the system computes none.
- Provenance: each sentence about a fault cites the inspection it came from, with a link to that record and its date. With no matching inspection, the panel says "No past faults found in 14 inspections" and cites the range.
- Correction: the manager can edit the summary before it goes into a report. An edited summary is marked "edited" and is not overwritten by a new generation.
- Limits: a daily cap exists. Its state says when it resets and points to the filter.
- Thin slice first: one lift with real notes. The slice showed that summaries were slow for long histories, so the design added the streaming panel before the full build.

## 11. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| One speed | The same spinner for an instant answer and a long one | Design the fast and the slow path |
| Fake progress | Invented steps or a percentage that the system does not report | Real steps, or a plain busy sign |
| False confidence | A score, a badge or a firm tone with nothing behind it | Remove it. Show the grounding |
| Decorative citation | Sources that link to a home page, or that the model made up | Render returned sources only. Link to the passage |
| Overwrite | A new generation replaces the person's edit or the last result | Keep versions. Protect edits |
| Black box agent | Actions happened and no list shows them | An action log with undo |
| Chat for everything | A chat box where a button or a form would do | Use the simplest control that does the job |
| Hidden memory | Behavior changes with no visible reason | A memory panel with edit and delete |
| Limit surprise | A wall with no reset time and no next step | A designed limit state |
| Mockup only | The feature was approved before any real call ran | A thin slice with real data first |

## 12. Checks

Gates:

- No screen shows a confidence value, a citation or a capability that the system does not produce.
- Every AI entry point has each reachable state from part 8.
- Every action on the "never without a yes" list has an approval step.
- A wrong or unwanted output can be corrected or undone.
- The provenance lines in part 5 are each decided and recorded.

Defaults:

- Default: stream slow output and echo the request at once.
- Default: scale confirmation to the stakes line of the brief.
- Default: keep earlier results reachable after a regeneration.
- Default: a non-model route exists for a medium or high stakes job.
