# The round protocol

Read this file at step 1 of `refine-round`. It covers stages, the scoped question, variants, the restate block, before and after, the decision entry, the stop conditions and a worked round.

Terms. A round is one cycle: ask, capture, restate, change, show, log. A scope is the screen, part or attribute that one round covers. A part is a named piece of the work: header, palette, type, hero image, a row, a state.

## 1. Stages

Name the stage before anything else. The stage decides what options look like and what feedback is useful.

| Stage | The question | Options differ in | Fidelity to show | Owning skill |
| --- | --- | --- | --- | --- |
| explore | Which idea? | Idea. Each option is a direction. | Rough. One hero or one card. | `mood-board` |
| refine | Is this part right? | One named attribute. Everything else is equal. | The real screen, in its medium. | this skill |
| finalize | Is anything broken? | Nothing. No options are shown. | The finished work, every state. | this skill, after `design-critique` |

Rules:

- A request that changes the idea is an explore request. Say so and hand off to `mood-board`. Do not smuggle a new direction into a refine round.
- A request to "polish" is a refine or finalize request. Work inside the chosen direction. Larger ideas go on the "not in this round" list.
- Put a status label on what you show: "direction", "refinement, round 2", "final candidate". Polished work reads as closed. Say what is still open.
- When the work drifts from one stage to another, stop and confirm the stage with the user.

## 2. The scoped question

Ask for the feedback you need. A scoped question names a part and a quality.

| Weak | Scoped |
| --- | --- |
| "What do you think?" | "Is the next sailing the first thing you see? If not, what is?" |
| "Do you like the colors?" | "Does the amber read as a signal or as a warning?" |
| "Any feedback?" | "For the header, the row and the status cell: keep, change or remove?" |
| "Is this better?" | "Variant A has tighter rows. Variant B has looser rows. Which fits a phone held in one hand?" |

Rules:

- One to four questions in one round.
- Ask about the artifact in front of the user. Do not ask the user to predict or to recall.
- Prefer a task to an opinion: "Find the cancelled sailing" tells more than "Is the status clear?"
- Put your recommended answer first when you offer choices, and say why in one clause.
- Give feedback with values and ask for values back: "24 px between rows now. More or less?"

## 3. Capture: keep, change, remove

Record one line for each part, in the user's words.

```
Keep / Change / Remove:
- header: keep ("the pier number up top is right")
- row height: change ("too cramped for a thumb")
- weather strip: remove ("nobody asked for it")
- status cell: no mark
```

- Keep: the part is right. It must come out of this round unchanged.
- Change: the part stays, and this version is wrong. Record what is wrong.
- Remove: the part goes.
- No mark: undecided. It is not approved. Leave it alone and log it under `Open:`.

Tag each item "observed" when the user did something with the artifact, and "stated" when they gave an opinion. When the two disagree, follow what was observed and say so.

## 4. Variants at the refine stage

Show variants only for an open question. A clear instruction needs no variants.

Rules:

- Two variants. Three only when the attribute has three natural values.
- The variants differ in exactly one named attribute. Name it in the label: "row height: 44 px against 56 px".
- Everything else is identical: content, width, theme, state, zoom. Capture both the same way.
- Keep names stable. "A" stays "A" in the next round. Never renumber.
- Each variant uses tokens. A value with no token is proposed as a new token first.
- State one gain and one cost for each variant. Then give your recommendation in a separate, labelled line.
- A variant that fails a gate is not shown. Say that it was dropped and why.

When more than one attribute is open, run them in order, or say plainly: "These differ in two things. This is a direction choice, not a test." Then you cannot tell which change caused the preference.

Attributes that work as one variable: one spacing step, one type size or weight, one color role, one radius token, one image crop, one line of copy, the position of one element, one duration.

## 5. The restate block

Restate before you edit. This is the contract of the round.

```
Round <n> on <scope>, stage <stage>.

What I heard:
1. "<the user's words>" -> <my reading>
2. "<the user's words>" -> <my reading>

I will change:
- <part>: <from> to <to> (token <name>)
- <part>: <what>

I will not touch:
- <kept parts, and everything outside the scope>

I will show:
- before and after of <screen> at <widths and themes>
- variants <A> and <B>, which differ in <attribute>

Not in this round:
- <idea or request>: <why it waits>

Is this what you want changed?
```

Rules:

- Use the user's words in quotes, then your reading. A wrong reading is cheap to fix here.
- "From" and "to" are values or token names, not adjectives.
- Wait for a yes. A "yes, but" is a new item. Restate again.
- When the reply changes the scope, restate the scope too.
- When you think a requested change harms the brief's goals, say so once, with the reason and the tradeoff. Then follow the user's decision and log it.

## 6. Change only what was asked

- Edit the listed items. Nothing else.
- Do not "fix" a neighboring part you dislike. Put it on the "not in this round" list.
- Do not replace factual copy or add a claim unless the user named it.
- Keep the identity: logo, brand colors, typefaces. A change to these is a `design-system` change.
- Carry the change through. When one edit makes another part stale, list the stale part and ask. Do not edit it in silence.
- Build on the user's idea. The after state visibly holds at least one thing the user proposed, and the report names it.
- When the user edited the work by hand, read the current state first. Never overwrite a hand edit.

Check after the edit:

1. Compare kept parts with the before state. They are identical.
2. Run the gates for what changed. A changed color needs its contrast pairs. A changed control needs keyboard and focus. Changed motion needs its reduced-motion variant.
3. Search the diff for raw values. Each value is a token.
4. Confirm that no file outside the scope changed.

## 7. Before and after

- Capture the before state first. After the edit it is gone.
- Show both at the same width, theme, state and content.
- Under the pair, list each change in one line: part, from, to.
- For motion or interaction, show a running version or a recording. A still image does not show timing.
- For an artifact type, follow the type's check rule. Describe the change in the chat and let the user look at the artifact.
- With no capture tool, list the changed values, ask the user to look, and label the visual check UNTESTED.

Default: batch the check. Render once after all listed changes.

## 8. The decision entry

Write the entry after the user answers. The format is fixed.

```
## 2026-11-23 round 2: home screen, row density
Stage: refine
Shown: before, after; variants A, B (differ in: row height, 44 px against 56 px)
Feedback asked: Which row height fits a phone held in one hand?
Keep / Change / Remove: header: keep; row height: change ("too cramped for a thumb"); weather strip: remove
Decision: B, 56 px rows (by <who>)
Rejected: A, 44 px rows: thumb misses the row on a moving deck
Open: status cell not reviewed; idea "show tide times" waits for a later round
Evidence: VERIFIED contrast pairs unchanged, rendered at 390 px in both themes; UNTESTED real device
```

Rules:

- One `Rejected:` line for each rejected option. Write `Rejected: none` when nothing was rejected.
- `Decision:` names the person. With no answer, write `Decision: pending`. Do not build on a pending decision.
- Never edit an old entry. Add a new entry that replaces it, and say which.
- Also log a feedback item you declined to apply, with the reason and who decided.
- For each feedback item the outcome is one of: adopted, adapted, declined with reason, deferred.

## 9. Stop conditions

| Signal | Action |
| --- | --- |
| The user answers "keep" for every changed part, and the gates pass | Stop. Report. Name the next skill. |
| The change list is done and new, unrelated feedback arrives | Close this round. Start a new round. |
| Default: three rounds on one scope with no convergence | Stop refining. Return to `align` with the trigger 'rounds stall'. It reopens feel, primary job and taste. |
| Feedback reverses an earlier decision, round after round | Show the logged decisions side by side. Ask the decider to choose once. |
| Each round reopens parts marked "keep" | Ask whether the direction is still right. If not, go to `mood-board`. |
| The requested change needs a new idea | It is an explore request. Hand off to `mood-board`. |
| The brief's requirements are met, the gates pass and the user approves | Stop. Do not polish further. Go to `accessibility-gate` or `handoff-to-code`. |
| A gate fails and the user insists | Do not apply it in silence. See `feedback-handling.md`, section 5. |

"No convergence" means: the same part was changed in three rounds and the user has not answered "keep". It is a sign that the goal is unclear. More variants will not fix an unclear goal.

## 10. A worked round

Scope: the home screen of the ferry app. Stage: refine. Round 2.

Feedback in chat: "The list feels cramped. And can it pop more?"

Sort: "cramped" is clear enough to scope. "Pop" is vague.

Ask: "By pop, do you mean (a) the next sailing should stand out more from the other rows, or (b) the whole screen needs more color? I recommend (a), because the brief puts the next sailing first."

Answer: "(a)."

Restate:

```
Round 2 on the home screen, stage refine.

What I heard:
1. "The list feels cramped" -> the rows are too low for a thumb.
2. "Can it pop more" -> the next sailing should stand out more from the other rows.

I will change:
- row height: 44 px to 56 px (token space-row, new value proposed)
- next-sailing row: shown as two variants that differ in type size only: A 32 px, B 40 px

I will not touch:
- header, status cell, colors, copy

I will show:
- before and after at 390 px, both themes

Not in this round:
- "show tide times": a new feature, waits for the brief owner

Is this what you want changed?
```

The user says yes. The change is made. Before and after are shown. The user picks B and answers "keep" for both parts. The entry is logged with A as rejected: "32 px did not separate from the rows at arm's length". The round stops.

What did not happen: no new accent color, no gradient on the row, no rewrite of the status labels. "Pop" was resolved into one attribute before any pixel moved.
