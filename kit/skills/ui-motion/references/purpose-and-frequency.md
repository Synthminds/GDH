# What to animate: purpose and frequency

Read this file at steps 1 to 4 of `ui-motion`. It covers the inventory of state changes, the purpose test, the frequency ladder, the environment line and the nuance pass that removes motion.

Evidence. The purposes and the nuance pass come from the Animation Handbook, chapters 1 and 4, and from published animation review standards read on 2026-11-23. The frequency ladder comes from those standards. No rule here was tested on a product built with this kit. The counts in the ladder are defaults.

## 1. Start from the state changes, not from effects

A computer changes state faster than a person can see. Motion supplies the missing in-between frame. So the inventory starts from what changes, never from a list of effects to add.

List every state change in the flow:

| Kind of change | Examples |
| --- | --- |
| Appear | A menu opens. A toast arrives. A row is added. |
| Leave | A dialog closes. An item is deleted. A banner is dismissed. |
| Expand or collapse | An accordion. A card opens into a detail view. |
| Load | A skeleton becomes content. A spinner becomes a result. |
| Value change | A counter rises. A progress bar fills. A price updates. |
| Selection | A tab changes. A filter applies. A toggle switches. |
| Route change | A new page. A step in a wizard. |
| Limit reached | The end of a list. A drag past its threshold. |

Each change gets one of two outcomes: a motion with a purpose, or a written reason to stay instant. "Instant" is a valid design answer.

## 2. The purpose test

Each motion has exactly one main job from this list. Write it in the spec row.

| Purpose | The question it answers | Typical motion |
| --- | --- | --- |
| Orientation | Where did this come from, and where did it go? | A menu grows from its trigger. A drawer slides from its edge and returns there. |
| Feedback | Did my input register? | A button compresses. A field shakes once on error and sets its error state. |
| Continuity | How are these two states related? | A card expands into its detail view. A list closes the gap after a removal. |
| Attention | What changed that I must notice? | A new message slides into view. A value rolls in the direction of its change. |
| Character | What kind of product is this? | A rare success moment. A signature brand transition. |

Rules:

1. "It looks nice" is not a purpose. Find the job or remove the motion.
2. Character is the weakest job. It earns a place only at rare moments and only after the other four are served.
3. Attention motion competes with the task. Use it only for a change the person must act on.
4. A hint at a hidden feature is attention motion. Keep primary actions visible at rest; never make them depend on a hint.
5. Warnings, errors with consequences and legal statements always exist as text. Motion may draw the eye to the text. It never replaces it.

## 3. The frequency ladder

Decide whether to animate before you decide how. A motion that pleases at the first view is a delay at the hundredth.

| How often one person sees it | Motion | Example |
| --- | --- | --- |
| A hundred times a day or more | None | Typing, a keyboard shortcut, moving between list rows, a command palette |
| Tens of times a day | None, or the shortest control motion | A hover, a toggle, a tab switch, a checkbox |
| Occasional | Standard surface motion | A dialog, a drawer, a toast, a date picker |
| Rare | Room for a flourish | Onboarding, a first success, a completed purchase, a brand moment |

Default: these frequency bands are rules of thumb from the review standards. Count with the user when the product's usage is known.

Rules:

1. An action triggered by the keyboard shows its result at once, even when the same action animates on click.
2. A professional tool used all day gets less motion than a marketing page seen once.
3. A theme switch does not animate every color.
4. A list that updates many times a second does not animate each update.
5. Count the frequency per person, not per product. An admin may open one dialog fifty times a day.

## 4. The environment line

Write one sentence that names the feeling all motion must support. Derive it from the brand words in `design/brief.md`.

| Brand words | Environment line | Motion consequence |
| --- | --- | --- |
| Calm, trusted, clear | "Nothing jumps; every change settles." | Ease-out only, no overshoot, durations at the long end of each row |
| Precise, fast, expert | "The tool answers at the speed of thought." | Short durations, few motions, no flourish outside onboarding |
| Playful, warm, bold | "Things have weight and a little give." | A spring on gestures, one signature flourish, a livelier stagger |

Each review asks one question per motion: "Does this support the environment line?" Record yes or no.

## 5. The nuance pass

Run this pass on every list of candidates, and again after the first build.

1. List every motion on the screen.
2. Name its purpose. Delete each motion with none.
3. Halve its amplitude, its duration or its number of moving parts. Ask whether it still communicates.
4. Keep halving until it stops communicating. Step back one notch.
5. Look for content shared between two states. Connect it instead of adding a new motion.
6. Test with the worst realistic data: the longest list, the most items, the most notifications.
7. Test in the lowest-attention context the research names: walking, glancing, on a slow phone.
8. Confirm that each remaining motion has a non-visual equivalent.

The goal is motion that is felt more than seen. When a first-time viewer names the motion instead of the result, it is too large.

## 6. Expressive motion budget

Tag each motion as functional or expressive.

- Functional: orientation, feedback, continuity, attention.
- Expressive: character.

Rules:

1. Map each expressive motion to a named moment in the user journey.
2. One expressive motion runs at a time on a screen.
3. Default: three to five signature motions in a whole product. The brand system names them and where each may appear.
4. A daily success gets no flourish. A first or a rare success may.

## 7. Worked example: a project dashboard

Inventory and decisions for one screen used daily by a project lead.

| Change | Trigger | Frequency | Decision | Purpose |
| --- | --- | --- | --- | --- |
| Row hover highlight | Pointer | Hundreds a day | Color change only, no movement | Feedback |
| Keyboard move between rows | Arrow keys | Hundreds a day | Instant | None needed |
| Filter menu opens | Click | Tens a day | Short surface motion from the trigger | Orientation |
| Filter applies | Click | Tens a day | Instant results; skeleton only if slow | Feedback |
| New task added | Save | Several a day | Row expands into place; others close up | Continuity |
| Task detail opens | Click on a row | Several a day | Row expands into the panel | Continuity |
| Overdue count rises | Data update | Rare | Number rolls up | Attention |
| Sprint completed | Final task done | Rare | One signature flourish | Character |
| Theme switch | Settings | Rare | Instant | None needed |

Removed: a fade-up entrance on each card at page load (no purpose, seen daily), a hover lift on every card (decoration), a pulsing "live" dot (attention with nothing to act on).

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Effects first | The plan starts from "add a parallax hero" | Start from the state-change inventory |
| Motion as delay | A daily action waits for an animation | Apply the frequency ladder; make it instant |
| Scroll fade on everything | Each section fades and slides up | One authored entrance; remove the rest |
| Hover lift everywhere | Every card rises on hover | Hover changes color or border only, on cards that are links |
| Attention noise | Pulsing dots, shimmering badges, a marquee | Keep attention motion for changes a person must act on |
| Hidden primary action | A key action appears only on hover or after an animation | Show it at rest |
| Meaning only in motion | A shake is the only error signal | Set the error state and the message text |
| Two flourishes at once | Confetti plus a bouncing badge | One expressive motion at a time |
