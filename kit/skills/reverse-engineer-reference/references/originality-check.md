# The originality check

Read this file at step 16 of `reverse-engineer-reference`. The check compares the built result with every reference that was studied. It answers one question: "Did we learn from this reference, or did we copy it?"

Run it after the first full build of a view and again before delivery. Run it again after any refinement round that moves toward a reference.

## What the check needs

- Every teardown sheet under `design/directions/references/`, with sections 9, 10 and 11 filled.
- The rendered result at the same widths as the captures.
- `design/tokens.json` and `DESIGN.md`.
- A fresh pair of eyes: the user, or a subagent that has not seen the sheets.

For a code deliverable, check the rendered result, not the source. For an artifact type, follow that type's own check rule and compare its exported view.

## Three kinds of evidence

| Kind | What it is | Weight |
| --- | --- | --- |
| Hard facts | A shared file, a shared sentence, a shared code block, a listed signature element | Gate. One hit fails the check. |
| Structured comparison | The seven axes below, each with a verdict | A person decides, with the thresholds as defaults |
| Blind perception | What a fresh viewer says the result resembles | Decides close calls |

No number in this file was verified against real cases. Every threshold is a default (a rule of thumb, UNTESTED). The hard facts need no number.

## The seven axes

Give each axis one verdict for each reference: `distinct`, `shared convention` or `too close`.

`shared convention` needs proof: name a second, unrelated product that does the same thing. A top bar with the logo on the left is a convention. A layout that only the reference uses is not.

### Axis 1. Structure

1. Write the result's sections in order, with the job of each, as in section 1 of the sheet.
2. Lay the two lists side by side.
3. Find the longest run of sections with the same job in the same order.
4. Default: a run longer than four sections is `too close`. It is a `shared convention` when two other products use the same order: name both.
5. Check the first view on its own. The same elements in the same arrangement is `too close` at any length.

### Axis 2. Layout

Compare at each width: column count, maximum width, alignment, the composition of the first view, and what changes at each breakpoint.

- Default: `too close` when the first view matches in composition and three or more of the other four items match.
- Same column count alone is a convention.

### Axis 3. Type

- Same typeface family as the reference, chosen after the study, with no reason in the brief: `too close`.
- Same classification is a convention.
- Compare the scales. Default: `too close` when four or more sizes match exactly and the roles match.
- A translation that restates their ratios with this project's steps is the goal. Check that `design/tokens.json` holds this project's steps, not theirs.

### Axis 4. Color

- Compare roles, not single values: page, surface, text, border, accent.
- Default: `too close` when the accent sits within about 15 degrees of hue of the reference's signature color, at similar lightness and saturation, in the same role.
- Default: `too close` when four or more role colors match within a small visible difference.
- A neutral page with one accent is a convention. Their accent is not.
- A color that this project's design system requires is `design-system-required`. Report it. It does not fail.

### Axis 5. Motion

- List each motion in the result: trigger, property, duration, easing shape, order.
- `too close` when a motion matches a signature motion of the reference on trigger, property and choreography.
- The same duration alone is a convention. Durations come from this project's motion tokens.

### Axis 6. Assets and words (hard facts)

1. Run `assets.py check` from `find-assets`. A `REFERENCE_SHIPPED` finding fails this axis.
2. Confirm that no font file, image, icon or media file in the project came from the reference. The manifest names the source of each.
3. Open the reference page and the result side by side. Read the copy.
4. Default: any shared run of five or more words fails, unless it is a common phrase of the language or of the trade.
5. A paraphrase that follows their copy sentence by sentence fails too. Compare the sequence of claims, not only the words.
6. Search the project's source for names that came from the reference: class names, component names, variable names.

Do not store the reference's text to make this comparison. Read it live.

### Axis 7. Signature elements (hard facts)

For each element in section 11 of each sheet: is it in the result, in any form? One "yes" fails the check.

"In any form" includes a recolored, resized or mirrored version of the same device.

## Blind perception tests

Run these when any axis is in doubt, and always before delivery of a brand-facing page.

**The attribution test.** Show a fresh viewer the result's first view with the logo and the product name hidden. Ask: "Which existing product does this remind you of?" Do not offer names.

- A reference named without prompting: treat axes 1, 2 and 4 as `too close` until proven otherwise.
- Several different products named, or none: a good sign.
- With subagents, give the `design-critic` agent the screenshot alone. With none, ask the user or a colleague of the user.

**The swap test.** Put the reference's logo on the result. Put this project's logo on the reference capture. Ask whether either looks wrong.

- Neither looks wrong: the result carries the reference's identity. Fail.
- Both look wrong: pass.

**The thumbnail test.** Shrink both first views to about 320 px wide and place them side by side. Ask whether they read as the same product family.

A pixel difference between two screenshots is not an originality measure. A recolored copy differs in almost every pixel and is still a copy. Use pixel diffs for regressions only.

## The verdict

| Result | Rule |
| --- | --- |
| Pass | Axes 6 and 7 are clean. No axis reads `too close`. |
| Fix | Any axis reads `too close`. Send it to `refine-round` with the axis and the reference named. |
| Recorded exception | The user decides to keep a `too close` item on axes 1 to 5. Write the decision, the reason and the risk in `design/decisions.md`. |
| No exception | Axes 6 and 7. A shared asset, a shared sentence or a signature element is removed. The user cannot waive someone else's rights. |

When the reference is the user's own earlier product, resemblance is expected. Run axis 6 for license reasons only, and say so in the report.

When several references were studied, also ask: "Does the result resemble any one of them more than it reflects the brief?" A result that is an average of its references is not a copy. It is also not a design. Send that finding to `design-critique`.

## Fix moves

| Axis | Move |
| --- | --- |
| Structure | Order sections by this project's content priority from the brief. Merge or drop sections that exist only because the reference has them. |
| Layout | Change the composition principle of the first view: axis of symmetry, where the product sits, what leads. |
| Type | Return to this project's scale and face. Keep the ratio lesson. Drop the values. |
| Color | Use this project's tokens. When the accent is close, move the hue or move the role. |
| Motion | Rebuild the moment from this project's motion tokens with a different property or order. |
| Words | Write from this project's brief and persona. Do not edit their copy into yours. |
| Signature | Remove it. Ask what it did for the visitor. Meet that need another way. |

Change the cause, not the surface. A new accent color on the same structure is still a skin swap.

## The report

Write `design/reviews/<YYYY-MM-DD>-originality.md`.

```
# Originality check: <scope>, <date>

References: <slugs>; result checked at: <widths>; themes: <list>
Checked by: <agent | user>; fresh viewer: <who>

| Reference | Structure | Layout | Type | Color | Motion | Assets and words | Signature |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <slug> | distinct | shared convention: <second product> | distinct | too close: accent hue | distinct | clean | clean |

Attribution test: <what the viewer named, unprompted>
Swap test: <result>
Hard facts: assets.py check <0 findings>; shared word runs <none | list>; signature elements <none | list>
design-system-required: <items that resemble a reference by rule of DESIGN.md>
Verdict: pass | fix: <axis, reference> | recorded exception: <decision entry>
Evidence: VERIFIED <what was compared on rendered output> | UNTESTED <what was judged by eye or not compared>
```

Then add the round to `design/decisions.md` in the fixed entry format, with the check as its evidence line.

## Worked example

The outcomes here are illustrative.

A marketing page was built after three teardowns. The check finds:

- Reference A, structure: a run of six sections in the same order (claim, logos, three features, proof, price, action). Two unrelated products use the same six. Verdict `shared convention`, with both named.
- Reference A, first view: the same split, with the claim on the left and a tilted product shot on the right, cut off by the viewport. The tilt and the cut are in A's signature list. Axis 7 fails.
- Reference B, color: this project's accent is a violet that sits near B's. `DESIGN.md` requires it. Reported as `design-system-required`, and the user is told once.
- Reference C: `distinct` on all axes.
- Attribution test: the viewer names A, unprompted.

Verdict: fix. The move is on the cause: the first view leads with the live product at full width and the claim under it, taken from the brief's primary job. After the fix, the viewer names no product, and axis 7 is clean.
