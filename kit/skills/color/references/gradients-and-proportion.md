# Proportion defaults and gradient discipline

Read this file at step 13 of `color`. It covers how much of each color a view holds, how to check it, when a gradient earns its place, how to build one, how to store it as a token, and the failure patterns.

Evidence. The 60-30-10 split is a rule of thumb with no primary source. "Limit the high-contrast elements in a view" comes from Designing for Emotion, chapter 2. "Dominant colors with sharp accents beat an evenly spread palette" and "one gradient slide is plenty" come from the Claude Design and Slides craft rules. Gradient text, gradient washes and the purple-to-blue gradient as tells come from the Impeccable and Anthropic lists. "Dark gradients show no banding" comes from the Vercel guidelines. All were read 2026-11-23. The interpolation advice is web platform behavior written from memory: UNTESTED until seen in the rendered page.

Precedence. A gradient, a glow or a color split that the design system prescribes is `brand-required`. It is not a tell. It still passes the contrast gate.

Terms. Proportion is the share of a view's area that each color group covers. A gradient is a transition between two or more color stops. A stop is one color at one position.

## 1. Proportion defaults

| Surface type | Default split | Note |
| --- | --- | --- |
| Product screen, dashboard, form | 85 to 90% neutral, up to 10% secondary, 5% accent or less | Color marks action and state only |
| Content and marketing page | About 60% neutral ground, 30% secondary surfaces and imagery, 10% accent | The rule-of-thumb split |
| Poster, cover, hero, social graphic | One dominant color may cover most of the area, with one sharp accent | Bold on purpose, when the brief asks |
| Slide deck | Two ground tones for the deck, plus one accent slide for the one thing to remember | From the Slides craft rules |
| Chart | Ground neutral, marks muted, one highlight | See the data colors reference |

Rules:

1. Decide the dominant color first. A palette where every color has an equal share has no idea.
2. One accent means one thing. Default: the accent marks the primary action and nothing else.
3. Links and the primary button share a hue. The user learns one signal for "interactive".
4. Status colors appear only where a status exists. A screen with no error shows no red.
5. Large areas take low chroma. Small marks take high chroma.
6. A second accent needs its own meaning, written in `DESIGN.md`.

## 2. Check the proportion

Run the check on one real screen with real content.

1. Squint test, or blur the screenshot. Name the first three things you see. They must be the three priorities of the view.
2. Count the accent uses on the view. Each maps to a stated priority. Default: three or fewer on a product screen.
3. Estimate the area share of the accent. Default: under the split for the surface type.
4. Gray test. Remove color. The view still works. Color then adds meaning; it does not carry it alone.
5. Compare with the default theme of the component library in use. When only the hue differs, the palette work is not finished.

Failure: everything is accent. Fix: pick the one primary action. Demote the rest to neutral or outline styles.

## 3. When a gradient earns its place

A gradient needs a job. Write the job in one line before you build it.

| Job | Example | Note |
| --- | --- | --- |
| The design system prescribes it | A brand gradient in the logo and hero | `brand-required`; follow its stops exactly |
| It shows light, depth or material | A soft light falling across a surface; a sky | Small lightness range, one hue family |
| It encodes data | A sequential color scale in a heat map | Build it by the data colors reference |
| It is the one signature moment | A hero ground that carries the idea of the direction | One on a view |

Not jobs: "it looks modern", "the card was empty", "the heading needed emphasis".

Defaults:

- Default: one gradient with a job on a view. In a deck, one gradient slide.
- Default: no gradient text. Emphasis comes from weight, size or a solid color.
- Default: no gradient wash on a kit of cards.
- Default: no gradient on a control. A control state must be readable as one color.
- Default: no glow shadow as decoration. A shadow has an offset and a blur.

## 4. Build a gradient

1. Take every stop from a token. A stop is a ramp step or a role, never a new raw color.
2. Keep the hues close. Default: stops within 90 degrees of hue, or one hue at two lightness values.
3. Two far hues pass through gray when mixed in sRGB. Interpolate in a perceptual space: `linear-gradient(in oklch, <stop>, <stop>)`.
4. Give a plain fallback first for browsers that do not read the color space syntax. Then verify the render.
5. With far hues, choose the hue path on purpose. The shorter path is the default. Check which hues appear in the middle.
6. Keep lightness steady, or moving in one direction, across the area where text sits.
7. Use two or three stops. More stops need a reason.
8. State the angle and the stop positions as part of the token. An unstated angle gets guessed.
9. On a dark ground, check for banding on a real screen. Reduce the lightness range, add stops, or add a fine noise layer.
10. A gradient under text is a ground. Check the text against its weakest stop.

## 5. Text and controls on a gradient

1. Find the stop with the least contrast against the text color.
2. Add that pair to the pairs file as a literal: `#ffffff on #5ecbcb`.
3. A failing pair gets a scrim, a solid chip, or a move of the text to the passing side.
4. A control on a gradient keeps a solid fill and a 3:1 edge against the nearest stop.
5. Gradient text that the brand requires is checked at its lightest stop against the ground. A failing result is an accessibility finding. Report it and ASK.

## 6. Store a gradient as a token

The `color` family holds single colors. Put gradients in their own family. `ds.py validate` accepts an extra family in the plain token-list shape.

```json
"gradient": {"tokens": [
  {"name": "gradient-hero",
   "value": "linear-gradient(135deg, #117878 0%, #0b5f5f 100%)",
   "usage": "Hero ground only. Text on it uses on-accent. Weakest stop: #117878."}
]}
```

Rules:

1. Write the literal stops in the value. `var()` is not valid in a token value.
2. Keep the stops equal to color tokens. Name the source tokens in the usage note.
3. A gradient that differs by theme is two tokens, one for each theme.
4. Name the weakest stop in the usage note, so the next check finds it.
5. Record an inferred angle or stop position as INFERRED until the owner confirms it.

This shape was validated on 2026-11-23 with `ds.py validate`: zero errors.

## 7. A brand gradient that is on the tell list

A design system can prescribe a violet to magenta gradient, glass surfaces or glow tokens. Then:

1. Use them exactly as the system states. Do not soften them.
2. Report each as `brand-required`, with the source: `brand-required: gradient hero (DESIGN.md, Color)`.
3. Apply them where the system says, and nowhere else. A brand gradient for the logo and hero is not a license for gradient cards.
4. Run the contrast gate on text over them. A failing pair is an accessibility finding, not a tell.
5. A misuse list in the brand rules can forbid some gradient uses, such as a gradient fill on the wordmark. Read it first.

## 8. Checks

1. Each gradient has a written job.
2. Every stop is a token value.
3. Text on a gradient passes at the weakest stop. The pair is in the pairs file.
4. No banding shows on a real dark screen, or the report says UNTESTED.
5. The proportion check ran on one real screen. The first three things seen match the priorities.
6. Each accent use maps to a priority.
7. Each `brand-required` item names its source.

## 9. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Default gradient | A purple-to-blue gradient as the brand statement, with no source in the brief | Derive the palette from the subject. Remove the gradient or give it a job. |
| Gradient text | A headline filled with a gradient for emphasis | Solid color and weight, unless brand-required |
| Wash kit | Every card carries a faint gradient | Flat surfaces; one signature moment |
| Mud middle | A gray band between two far hues | Interpolate in OKLCH, or bring the hues closer |
| Banding | Visible steps in a dark gradient | Shorter range, more stops, or fine noise |
| Unchecked ground | Text passes at one end of the gradient and fails at the other | Check the weakest stop |
| Accent everywhere | Ten accent elements on one screen | One accent, one meaning |
| Even spread | Five colors with equal area | Choose a dominant color |
| Raw stops | Gradient colors that exist in no token | Build stops from tokens |
| Softened brand | A required brand gradient toned down because a rule flagged it | Restore it. Report `brand-required`. |
