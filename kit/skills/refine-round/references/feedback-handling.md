# Handling difficult feedback

Read this file at step 4 of `refine-round`. It covers vague feedback, conflicting feedback, relayed and silent feedback, scope creep, and feedback that breaks the design system or a gate.

First sort every item into one class. Then use the section for that class.

| Class | Sign | Section |
| --- | --- | --- |
| Clear | Names a part and what is wrong with it | Restate and proceed |
| Vague | A feeling with no part: "make it pop", "more modern", "not quite right" | 1 |
| Conflicting | Two inputs cannot both hold | 2 |
| Relayed or silent | "The CEO hates it"; "Looks fine" | 3 |
| Out of scope | A new feature, another screen, a new direction | 4 |
| Against the design system or a gate | Needs an off-token value, or fails contrast, keyboard, color-only or motion rules | 5 |
| A request to add content | A number, a logo, a quote, a client name | 6 |

## 1. Vague feedback

Do not guess, and do not answer a vague word with a full redesign. Turn the word into one named attribute.

Method:

1. Ask what the user means: "What do you mean by pop?" Often this is enough.
2. If the user cannot say, offer two concrete readings and recommend one. Tie the recommendation to the brief.
3. If words do not settle it, show a quick rough guess of each reading and ask which is closer.
4. Restate the chosen reading as one attribute, with a from value and a to value.

Never offer more than three readings. Never offer a reading that breaks a gate.

Readings for common words. Use them as a starting list, not as a translation table.

| The user says | Possible readings, each one attribute | Ask |
| --- | --- | --- |
| "Make it pop" | More contrast between the key element and the rest. A larger key element. One accent on the key element. Less noise around it | "Which element should stand out, and against what?" |
| "It's boring" | No signature element. Even weights everywhere. Generic copy. Default type | "Which part did your eye skip?" |
| "More modern" | Tighter type scale. Fewer borders. Another typeface class. Newer layout skeleton | "Show me one thing you call modern. Which part of it?" |
| "Cleaner" | Fewer elements. More space between groups. Fewer colors. Fewer borders | "What would you remove first?" |
| "More premium" | More space. Fewer colors. Finer type detail. Slower, shorter motion. Better imagery | "Premium like which product, and which part of it?" |
| "Friendlier" | Rounder shapes. Warmer copy. A human image. Softer contrast between surfaces | "Friendly in words, in shapes or in pictures?" |
| "Too busy" | Too many weights. Too many colors. Too little space between groups. Too many primary actions | "What competes with what?" |
| "It doesn't feel like us" | A brand word is missing. The category default crept in. The voice of the copy is off | "Which brand word is missing here?" |
| "Bigger logo" | The brand is not felt. The header is weak. The first view lacks identity | "Where did you look for the brand and not find it?" |
| "Can we try something different?" | One attribute is wrong. Or the direction is wrong | "Different in one part, or a different idea?" |
| "I'll know it when I see it" | The goal is not settled | Show two rough guesses. If neither lands, return to `align` with the trigger 'an answer contradicts the brief' |

Notes:

- "Make it pop" is most often a hierarchy problem, not a color problem. Check the first, second and third look before you add any color.
- A vague word that survives two rounds points at the brief. Check the brand words and their "does not mean" columns.
- When a reading needs a new idea, it is an explore request. Hand off to `mood-board`.

## 2. Conflicting feedback

Kinds of conflict:

- Person against person: two reviewers want opposite things.
- Now against then: the new request reverses a logged decision.
- Request against brief: the request contradicts a brand word, the audience or the primary job.
- Request against request: one message asks for two things that cannot both hold, such as "more content" and "more space".

Method:

1. List the two sides side by side, each with its source and its exact words.
2. For a relayed side, get the original wording first.
3. Name what each side protects. Often both serve one goal in different ways.
4. Find the decider. The brief names one. Ask that person.
5. If talk does not settle it in one exchange, build both as a quick comparison. Two variants, one attribute. Do not send a third argument in prose.
6. Record the decision, the rejected side and the reason.

Rules:

- Do not average. A compromise between two clear positions is usually worse than either.
- Do not pick the side of the last or the loudest speaker. Do not apply a change only because several people asked.
- Every reviewer's input appears in the record, adopted or not.
- A conflict with a logged decision: show the old entry and its reason. Ask what changed. With new evidence, reverse it and log the reversal. Without, keep the decision.
- A conflict with the brief: say which line it contradicts. The user may change the brief. Then update `design/brief.md` first, and log that.
- No conflict stays open at the end of the round. If the decider is not available, log `Decision: pending` and do not build on it.

## 3. Relayed and silent feedback

Relayed: "The board thinks it's too dark."

- Mark it "relayed". Ask for the original words, or for a direct confirmation, before a large change.
- Ask which screen and which part the person saw. They may have seen an old round.

Silent or neutral: "Looks fine." "OK."

- Do not treat it as approval of every part. Ask one specific question about a named part.
- A part with no mark stays undecided. Log it under `Open:`.

Praise only: "Love it."

- Ask what must not change. That is the keep list.

Feedback through a hand edit: the user moved or changed something directly.

- Read the current state. Treat the edit as a "change" item with the highest rank. Keep it.
- Ask whether the same change should apply to similar parts.

## 4. Out of scope

- A new feature, a new screen or a new direction is not part of this round.
- Say so in one line. Put it on the "not in this round" list with a reason.
- Offer the route: a new round, `mood-board` for a new direction, or `align` with the trigger 'the primary job changes' for a change of goal.
- Do not refuse the idea and do not start it. Log it, so that it is not lost.

Scope creep inside a round: when the fifth small request arrives mid-round, finish the agreed list first. Then start a new round.

## 5. Feedback that breaks the design system or a gate

Precedence: the user ranks above the design system. A gate ranks above nothing and below nothing; it is not a preference. So the two cases differ.

### Against the design system

Example: "Use this pink for the button." The pink is not a token.

1. Say what the system prescribes, with its source: token name and `DESIGN.md` section.
2. Offer the nearest on-system option, and show it beside the request.
3. If the user still wants the off-system value, the user wins. Then choose with the user:
   - a one-off exception, logged with a reason and an end date; or
   - a change to the system: add or change the token through `design-system`, and update `DESIGN.md`.
4. Never hard-code the value in silence. Every value in a deliverable comes from a named token.
5. When the design system belongs to someone else, such as a client brand owner, name that person. The user may need their approval.
6. A system synced from code is changed in the code, not on its page. Say where the change must be made.

### Against a gate

Example: "Make the body text light gray." The pair falls to 2.9:1. The floor is 4.5:1.

1. State the gate and the measured value: "Light gray on this ground is 2.9:1. The floor for body text is 4.5:1."
2. Say who is affected and how, in one sentence.
3. Offer the nearest passing option, and one other way to reach the same intent. Ask what the intent is: a softer page can come from less weight, more space or a tinted ground.
4. Show the passing option beside the request.
5. If the user insists, do not apply it in silence and do not refuse in silence. Record an exception: the gate, the value, the reason, and the person who accepted it. Mark the work as failing that gate in every later report.
6. The exception is the user's to make, and it stays visible. `accessibility-gate` reports it. `handoff-to-code` carries it.

Gates that this applies to: text contrast, control and focus contrast, meaning by color alone, keyboard access with visible focus, reduced motion. Also the spend gate, the exposure gate and the license rule: a request to "just publish it" or "just use that image" still needs the yes, the quote or the license read.

One more case: a brand rule that itself fails a gate. Example: a required brand gray that fails contrast on white. Report it as an accessibility finding, not as a tell. Offer a darker tint from the same hue for text, and keep the brand gray for fills. The brand owner decides.

## 6. Requests to add content

- A number, a statistic, a testimonial, a client logo, a quote: ask for the real one and its source.
- With none, use a labelled placeholder such as `[CUSTOMER COUNT]`. Never invent it.
- A photo of the user's place or product: ask for the file, or hand off to `find-assets` or `generate-media`. Never pass off a stand-in as the real thing.

## 7. Conduct

- Restate the user's view accurately before you answer it.
- Ask "What do you mean by that?" before you judge an idea.
- Do not defend your earlier work because you made it. When the user's version serves the brief better, adopt it and say so.
- Give your recommendation and the tradeoff once. Do not repeat the argument in the next turn.
- Do not make a change only because someone asked. Each change links to a goal, a brand word or evidence. A pure preference of the decider is a valid reason; log it as "preference".
- Ask once in each milestone how the rounds are working: "More options or fewer? More direction from me or less?" Use the answer in later rounds.
