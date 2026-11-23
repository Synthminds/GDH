# Present, converge and prove the directions differ

Read this file at step 15 of `mood-board`. It covers the uniqueness test, how to present, how to capture feedback by part, how to merge, and when to stop.

## 1. The uniqueness test

Run it before the user sees the board. It has three parts. All must pass.

### The written half

For each direction write two lines:

- How it differs from the other directions.
- How it differs from the category norm.

Rules for the lines:

- One line each. State a difference in idea, structure or behavior.
- No color word. A difference that needs a color word is a difference in skin.
- No praise word. "Bolder" and "cleaner" say nothing a builder can use.
- A reader who sees only the lines can match each line to its direction.

Good: "It shows the whole day at once on a single line. A lists rows, and C stacks single trips."
Bad: "It is the green, calmer option."

### The computed half

`moodboard.py diff` compares each pair on three fields.

| Field | How it is read | "Same" means |
| --- | --- | --- |
| Palette family | The OKLCH hue of the `accent` color, plus the ground, light or dark | Same ground, and accent hues closer than the threshold. Default: 30 degrees. Two palettes with no chromatic accent on the same ground are one family. |
| Type class | `type.class`, lowercased, spaces to hyphens | Equal strings |
| Layout skeleton | `layout.skeleton`, lowercased, spaces to hyphens. Names come from the closed list in `directions.md` section 5 | Equal strings |

| Shared fields | Verdict | Result |
| --- | --- | --- |
| 3 of 3 | near-identical | Error. The board fails. |
| 2 of 3 | weak | Warning. Read the two concept sentences again. |
| 0 or 1 | distinct | Pass |

The same comparison runs against the category norm when the board file gives its accent, type class and skeleton. A direction that matches all three fails, unless `allowCategoryDefault` holds the reason from the brief. At stage explore, give all three. A board without them skips this comparison.

Limits of the computed half. State them when you report the result:

- It is a floor. Two directions can differ on all three fields and still be one idea in two skins.
- It trusts the names you type. Two skeletons with different names can be the same layout.
- It compares directions with each other and with the category norm only. It does not know the known default looks.
- The 30 degree threshold is a rule of thumb with no published source.
- It does not look at the rendered board.

### The reading half

Run these checks yourself. They cover what the computed half cannot see.

1. Skeleton names. Each `layout.skeleton` is a name from the closed list in `directions.md` section 5. A renamed clone counts as the same skeleton.
2. Ideas. Apply the label-free check in `directions.md` section 5 to each pair: concept words, adjectives, sample copy, swatches.
3. Known default looks. Apply the match rule in `directions.md` section 6 to each direction. Name the table date in the report.
4. Fonts. Each specimen shows its named face, or carries "fallback face shown". See `build-routes.md`.

Report each check by name: pass, fail, or accepted with the reason from the brief.

When a pair fails, do not move one field until the check passes. Go back to the idea. Pick another object from the subject's world and draft a new direction.

## 2. Present

1. Open with the frame: the user, the primary job, the brand words and the category norm. Three lines.
2. Say what stage this is: "These are directions. Nothing is final. Rough is intended."
3. Show every direction with equal detail and equal effort.
4. For each, state the idea in one sentence and the main tradeoff in one sentence. Do not sell.
5. Keep your recommendation apart. Give it after all directions, in a line that starts "Recommendation:". Say what would change it.
6. Ask the scoped question. Do not ask "Which do you like?"

The question, in full: "For each direction and each part: keep, change or remove? Which direction is the base? What is missing?"

Rules of conduct:

- Do not rebut feedback in the turn you receive it. Record it first.
- When a reply is unclear, ask "What do you mean by that?" Offer two concrete readings.
- When a reply is short or neutral, ask one question about a named part before you treat it as a choice.
- Quote the user's words in the record. Do not paraphrase from memory.
- Feedback that a third person gave is "relayed". Ask for the original wording before a large change.

## 3. Capture feedback by part

Use one line for each direction and part. The local board writes these lines for the user.

```
Keep / Change / Remove:
- A Departure Board / Type pairing: keep (the signage face feels right)
- A Departure Board / Palette: change (amber is too much like a warning)
- B Tide Line / Signature element: keep
- C Punched Ticket / Layout and shape: remove (a stack hides the timetable)
Base direction: A Departure Board
Missing or other: nothing shows a delay
```

Meaning of the three words:

- Keep: this part is right. Protect it in every later round.
- Change: the part is needed, and this version is wrong. Ask what is wrong.
- Remove: the part should not exist in this direction.

A part with no mark is undecided. It is not approved. Ask about it once, then log it under `Open:`.

When several people answer, record each person's lines with a name. Do not average them. List conflicts side by side and ask the decider. The decider is named in the brief.

## 4. Converge

Outcomes, and what to do for each:

| The user says | Action |
| --- | --- |
| One direction, keep all | Mark it chosen. Mark the others rejected, each with the user's reason. Go to section 6. |
| One base, plus named parts from others | Build a merge. See section 5. |
| "Somewhere between A and B" | Ask which parts of each. Offer two concrete merges if the user cannot say. Then section 5. |
| None of these | Ask what all of them miss. Check the brief. Draft new directions from a different object in the subject's world. Do not recolor. |
| "I like all of them" | Ask the user to vote in categories: easiest to live with, most memorable, most like us. Then ask for one base. |
| No answer on direction | Add one direction labelled "provocation" that breaks one assumption of the brief. Show the board again. |

Keep at least one bold option alive until the user rejects it with a reason. Record the reason.

## 5. A merge is a new direction

A merge takes one base direction and moves in named parts from others.

1. Write the merge as a list: base, plus each moved part and its source.
2. Check each moved part against the base idea. A part that breaks the idea stays out. Say so, and say why.
3. Rewrite the concept sentence. If the sentence now needs the word "and" to join two ideas, the merge has no idea. Stop and tell the user.
4. Give the merge its own name and the next letter. Do not reuse a name. Do not renumber the others.
5. Fill every part again. Rebuild the sample.
6. Run `diff` with the merge and the rejected directions in one board file. The merge must not fall back into the category norm or a known default look.
7. Show the merge beside its base. Ask the same scoped question.
8. Log a new decision entry. `Shown:` names the base and the merge.

Never apply a merge straight to the build. The user has not seen it until it is shown.

The compromise trap: a merge that takes the safest part of each direction has no signature. Check that the merge still holds exactly one signature element.

## 6. Close the round

1. Mark each direction file: chosen, rejected with reason, or merged into a named direction.
2. Write the decision entry in the fixed format. One `Rejected:` line for each rejected direction.
3. Test the chosen direction on one real screen: the screen that carries the primary job. Use real content. Check the contrast pairs on that screen.
4. Report what was checked and what was not. Fonts that did not load are UNTESTED.
5. Name the next skill. `design-system` writes tokens and `DESIGN.md` from the chosen direction file.

## 7. Stop conditions

| Signal | Action |
| --- | --- |
| A base is chosen and the real-screen test holds | Stop. Hand off. |
| Default: two convergence rounds pass and the user still moves between directions | Show the two candidates on the real screen. A real screen settles what a board cannot. |
| Default: three rounds with no base direction | Stop. The brief is unclear or wrong. Return to `align` with the trigger "rounds stall". It reopens feel, primary job and taste. |
| The user asks for a rejected direction again | Show the logged reason. Ask what changed. With new evidence, reopen it and log that. |
| The user asks for a small change to the chosen direction | That is refinement. Hand it to `refine-round` by the `ask-gdh` step 9 route: read `SKILL.md` in the sibling `refine-round` skill folder and follow it, or print `/gdh:refine-round`. |
| Every round adds a direction and none leaves | Ask the user to remove one before you add one. Four is the ceiling. |

## 8. Failure patterns

| Pattern | Counter-move |
| --- | --- |
| "Which do you like?" | Ask for keep, change, remove by part, and for a base. |
| The hidden favorite | Equal detail for each direction. Recommendation in its own labelled line. |
| The silent merge | A merge is named, tested and shown before anything is built on it. |
| The compromise | Check for one signature element. Rewrite the concept sentence. |
| The drift back | Read `design/decisions.md` before each proposal. A rejected option needs new evidence. |
| Passing the diff by renaming | Change the idea, not the field. State the limits of the test in the report. |
| Straight to the full build | One real screen first. |
