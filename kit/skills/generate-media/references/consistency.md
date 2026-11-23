# Consistency across a set

Read this file at step 5 of `generate-media`. It covers the style kit, reference images and reusable reference elements, model and setting locks, the set test, color matching, and the checks for a consistent set.

Evidence. The tool features (reusable reference elements for a character, environment or prop, referenced in prompts; trained identity models for a person; a brand kit that does not apply itself and must be worded into each prompt; batches as distinct prompts rather than a count of variations; elements supported only on some models) come from the connector cards, read 2026-11-23. The failure of generated clips cut together with no consistent character or style comes from the motion research. No generation was run, so how well any of these methods holds a set together is UNTESTED.

## 1. Why sets drift

Each call samples afresh. Without fixed inputs, a set drifts in:

| Drift | Example |
| --- | --- |
| Style | One illustration flat, the next with gradients |
| Palette | The accent shifts from orange to red |
| Light | Left light in one photo, top light in the next |
| Subject identity | A character's face, a product's shape changes |
| Scale and framing | Objects fill the frame in one, float small in another |
| Line and texture | Stroke weight and grain differ |

## 2. The style kit

Write it in `prompt-sheet.md` once per set. Every prompt of the set uses it.

| Part | Holds | Rule |
| --- | --- | --- |
| Style line | One sentence: medium, light, palette, texture, framing | Word for word in every prompt |
| Palette | Token names, hex values, color words, roles | Same words every time; hex list in the tool's color field when it has one |
| Negative list | Short form | Same in every prompt |
| References | Two to four images that show the style; their license status | Same set for every call; own work or licensed only |
| Model | The model name read live, and its version when shown | One model per set |
| Settings | Aspect ratio, quality, size, style or seed fields the tool offers | Fixed for the set |
| Subject anchors | Reusable reference elements or identity references | Same element ids every time |
| Framing rule | Where the subject sits, its margin, its scale | Same for every asset |

## 3. References and reusable elements

1. Style references: images that show the look. Use own work, the approved styleframe or mood-board tiles that are licensed for this use. A gallery screenshot is a reference for people, never an input to a tool.
2. Subject references: the client's product photos, the approved character sheet, a location plate. These keep identity.
3. Reusable elements: some tools store a character, environment or prop once and let prompts refer to it. Use one when the tool supports it on the chosen model. Read the card for which models accept elements.
4. Identity models for a real person: only with that person's written consent on record.
5. Uploading a reference is exposure when it is client material or unreleased work. Ask first.

## 4. Locks

| Lock | How |
| --- | --- |
| Model | One model for the whole set. Note it in the prompt log. |
| Settings | Same aspect ratio, quality and size fields |
| Seed | When the tool exposes a seed, record it; reuse it for near-variants |
| Brand kit | When the tool stores a brand kit, still word the colors and rules into each prompt; a kit does not apply itself in every tool |
| Composition | Same framing rule; same margin; same ground |

Model catalogs change. A set started on one model should finish on it. When the model disappears mid-set, test the replacement on one asset and compare before continuing.

## 5. The set test

Before generating a set, prove the kit holds.

1. Generate two assets with different subjects, using the full kit. This is the cheap test from the spend gate.
2. Put them side by side at delivered size.
3. Ask: would a stranger believe one hand made both? Check style, palette, light, line, framing.
4. When they drift, fix the kit (style line, references, settings), not the individual prompt.
5. Only when the pair holds, generate the rest in a batch of distinct prompts.

## 6. Matching color to tokens

Generated color is approximate. Match it in finishing.

1. Sample the key colors of each output.
2. Compare with the tokens: ground, ink, accent.
3. Shift the image toward the tokens with a color adjustment, not by regenerating.
4. For flat illustrations, a recolor to exact token values is often possible: posterize to the palette, or vectorize and set fills.
5. For photos, grade the set together: one adjustment applied to all.

## 7. Video and multi-shot consistency

1. Generate a still per shot first. Approve the stills as a set on one contact sheet.
2. Animate each approved still with the same model and settings.
3. Keep one reusable element per recurring subject.
4. Grade all clips together at the end.
5. `motion-video` owns the cut. This skill supplies consistent shots.

## 8. The set checklist

- [ ] Every asset uses the style line word for word.
- [ ] One model and one settings set across the set.
- [ ] Palette matches the tokens after finishing.
- [ ] Light direction and color temperature match.
- [ ] Subject identity holds across assets.
- [ ] Framing and margin match; assets align on a grid.
- [ ] Stroke weight and texture match.
- [ ] The set passes the "one hand made these" test at delivered size.

## 9. Worked example: six empty-state illustrations

| Step | Decision |
| --- | --- |
| Kit | Style line from the prompt sheet; palette ground, ink, one accent; negative list; two own sketches as references; one model; 4:3; transparent ground |
| Test | Two prompts: "empty tray" and "magnifier over a blank card". One output each. |
| Review | The second had a gradient shadow. The kit gained "flat shadows, no gradients". |
| Retest | Two outputs again; they matched. |
| Batch | Four more prompts as one batch of distinct prompts, one output each |
| Finish | Recolored to exact token values; trimmed to the same margin |
| Record | Six records, one prompt log entry per prompt, model and settings once at the top |

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Prompt-level fixes | Each asset tweaked separately; the set diverges | Fix the kit; regenerate the pair |
| Model switch mid-set | The last three look different | One model per set; test any replacement |
| Count of variations | One prompt run as several variations; all one idea | Distinct prompts in a batch |
| Kit not worded | A stored brand kit assumed to apply itself | Word the colors and rules into each prompt |
| Gallery as input | A screenshot of another studio's work used as a reference | Own work or licensed references only |
| Clips before stills | Shots animated before the set was approved | Approve stills first |
