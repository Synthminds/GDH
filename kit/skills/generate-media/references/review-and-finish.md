# Review, selection and finishing

Read this file at steps 14 to 17 of `generate-media`. It covers the review of each output, the artifact checklist by medium, the selection round with the user, finishing (retouch, background removal, expand, upscale, color match, vector clean-up, compression), and placing text and logos.

Evidence. The tell list comes from the Anthropic frontend-design skill and the Impeccable craft floor, read 2026-11-23. The finishing capabilities and their spend status come from the connector cards: background removal, expand, upscale, vectorize and the warning that a re-called batch edit bills twice. The artifact list is common knowledge of generated media, not a sourced list. The image and SVG commands are from memory; check them with `--help`.

## 1. Review each output

Review at delivered size, in place, not only as a thumbnail.

| Question | Reject when |
| --- | --- |
| Does it do the job in the brief? | It decorates but does not help the person |
| Does it fit the chosen direction? | It could belong to another brand |
| Does it match the style kit? | Style, palette, light or framing drift from the set |
| Is the subject faithful? | The client's product shape, color or label is wrong |
| Is there room for text where planned? | The subject fills the text area |
| Is it free of artifacts? | Any item in section 2 |
| Is it free of tells the brand does not require? | Purple-to-blue wash, glow on dark, glassy blobs, generic stock pose |
| Is anything invented? | Text, a logo, a fake interface, a fake person |

Write a one-line reason for each rejection. Reasons feed the next prompt and the record.

## 2. Artifact checklist by medium

Images:

- [ ] Hands, fingers, teeth, eyes and ears are correct, or not shown.
- [ ] No garbled text, letters, signatures or watermarks.
- [ ] Straight lines are straight; symmetry holds where it should.
- [ ] Objects obey physics: shadows match light, reflections match objects.
- [ ] Product details (labels, holes, seams) match the real product.
- [ ] No melted edges, doubled objects or smeared backgrounds.

Vectors:

- [ ] Paths are clean, with no slivers, hidden shapes or thousands of points.
- [ ] Fills use the palette; no stray near-duplicate colors.
- [ ] Shapes are closed where they should be.

Video:

- [ ] No flicker, morphing or identity change across frames.
- [ ] Motion obeys physics; no limbs or objects passing through each other.
- [ ] No text or logos forming in the frame.
- [ ] Start and end frames are usable for cuts and loops.

Audio and voice:

- [ ] Pronunciation of names, products and numbers is correct.
- [ ] No clicks, warbles, robotic artifacts or clipped endings.
- [ ] Music has a clean start and end at the planned length.

3D:

- [ ] The silhouette matches the real object from every side shown.
- [ ] No holes, floating fragments or doubled surfaces.
- [ ] Textures have no baked shadows or melted labels. See `three-d`.

## 3. The selection round

1. Show the kept outputs side by side at delivered size, in context when possible (on the page, in the frame).
2. Show the rejected ones too, briefly, with the reasons. The user may disagree.
3. Ask a scoped question: "Which of these keep the direction? Keep, change or remove, for each."
4. In an explore stage, options differ in idea. In a refine stage, two options differ in one named attribute.
5. Record the round: shown, question, choice, rejected with reasons, open questions.
6. Do not generate more until the user answers. More options are not a substitute for a decision.

## 4. Finishing

Finish only the selected outputs. Each paid edit goes through the spend gate again.

| Step | Capability | Free route | Paid route |
| --- | --- | --- | --- |
| Crop and resize to the delivered sizes | none | Any image tool | not needed |
| Retouch a small artifact | `image-edit` | Manual retouch in an editor | A generative fill or edit in a tool |
| Remove the background | `image-edit` | Manual mask | A background-removal tool |
| Expand the canvas for another ratio | `image-edit` | Not possible without generation | A generative expand tool |
| Upscale | `image-edit` | Not possible beyond simple resampling | An upscaler |
| Match color to tokens | none | A color adjustment toward sampled token values | not needed |
| Vectorize a flat illustration | `vector` | A tracer from the asset catalog, then clean-up | A vectorize tool |
| Clean an SVG | none | An SVG optimizer, with a reviewed config | not needed |
| Compress for the web | none | Encoders for AVIF, WebP, JPEG | not needed |

Rules:

1. Upscale only the chosen output, and only to the size the placement needs.
2. Expand rather than regenerate when another aspect ratio is needed for the same image.
3. Never call a batch edit twice to check it. A second call redoes and bills the work again.
4. Keep the original generated file in `source/`. Finished files are derivatives.

Commands from memory, on copies:

```
# convert and size a hero for the web, at 2x of a 720 px slot
magick hero-source.png -resize 1440x -quality 82 hero-1440.webp
magick hero-source.png -resize 1440x -quality 60 hero-1440.avif

# optimize an SVG; check that the viewBox and ids survive
npx svgo illustration.svg -o illustration.min.svg
```

## 5. Text and logos go on top

1. Final text is set in the design, in the brand fonts, from tokens. Never in the generated pixels.
2. The logo is the supplied file, placed in the design with its clear space.
3. Text over an image meets the contrast floor at the busiest point behind it. Add a scrim or a solid backing when it does not.
4. A generated mockup with readable text (a poster on a wall, a phone screen) gets its text replaced by the real design in compositing, or is not used.

## 6. Worked review

```
Set: empty-state illustrations, test pair
01-empty-tray-v1: keep. Matches kit; calm; margin correct.
02-magnifier-v1: reject. Gradient shadow under the card (kit says flat shadows); magnifier lens shows garbled letters.
Kit change: add "flat shadows, no gradients, blank card with no marks" to the style line and negatives.
Next: retest 02 with the changed kit; 1 output; spend check shown.
```

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Thumbnail review | Artifacts found after delivery | Review at delivered size, in place |
| Taste-only review | "Looks nice" with no criterion | The review questions and checklist |
| More instead of decide | Rounds of generation with no selection | A scoped selection round |
| Upscale everything | Paid upscales of rejected outputs | Finish only the selected |
| Regenerate for ratio | A new generation for each crop | Expand or recompose the chosen output |
| Text in pixels | A headline baked into the image | Set text in the design |
| Double-billed edit | A batch edit called twice to check | Read the job state; never re-call to check |
