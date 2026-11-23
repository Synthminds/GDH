# Brand and consistency in video

Read this file at step 13 of `motion-video`. It covers tokens in the frame, logo use and the logo sting, brand motion character, and consistency across shots, above all generated ones.

Evidence. The rule that brand elements match tokens and the logo keeps its clear space comes from the motion research checks. The idea of translating a web design file into frame rules comes from the HyperFrames README ("frame.md"), read 2026-11-23. The sting rule (two seconds or shorter, ending on the static lockup) is this kit's default, shared with `logo-identity`. The consistency methods for generated shots come from the generation connector cards: reference elements, fixed style lines and same-model runs. No generation was run. Every number is a default.

## 1. Tokens in the frame

Video uses the same tokens as the product. Translate them for the frame once, in `video/frame-rules.md`.

| Token family | Translation for the frame | Example |
| --- | --- | --- |
| Color | The same values. Pick the frame's ground and the one accent. Check text pairs for contrast. | Ground `color.ink`, accent `color.signal`, text `color.paper` |
| Type | The same families. A video scale built for a phone-sized frame. | Display 96 to 140 px at 1080 wide; body 32 to 40 px |
| Motion | The same curves. Durations may run longer in video than in the interface. | Signature move uses `motion.ease.out` at 600 to 900 ms |
| Radius, stroke, shadow | The same values, scaled with the frame | Cards in UI shots keep the product's radius |
| Imagery rules | The same do and do-not list | No stock people; product screens are real |

Rules:

1. Read `DESIGN.md` and `design/tokens.json` first. The design system's rules win over video habits.
2. A tell that the brand requires is `brand-required`, not a finding. Example: a brand gradient used on the hero number.
3. A tell the brand does not require is removed: a default font, a purple-to-blue gradient wash, glow on dark, an entrance on every element.
4. Fonts are the licensed brand files, embedded as the route requires. Never a look-alike.

## 2. The logo in video

1. Use the supplied logo file. Never redraw it, regenerate it or trace it.
2. Keep the clear space the usage sheet states.
3. Use the version the sheet names for the ground: full color, one color, reversed.
4. Place it where the platform interface does not cover it.
5. The logo appears at the end, or small and fixed in a corner. Not as a long intro.

### The logo sting

A sting is a short animated logo moment.

1. Default: two seconds or shorter.
2. It ends on the exact static lockup, at rest, held long enough to read.
3. It animates parts of the supplied vector, not a new drawing. Masks, draws and reveals of the real paths only.
4. It follows the brand's motion character. No bounce for a brand with no springs.
5. It has a still version for reduced motion and for thumbnails: the static lockup.
6. The user approves the sting separately from the video. Record it in `design/decisions.md`; `logo-identity` owns the motion version of the mark.

## 3. Brand motion character

| Brand motion character | Video consequence |
| --- | --- |
| Calm, ease-out, no springs | Slow pushes, soft reveals, hard cuts, no overshoot |
| Precise, technical | Linear draws, grid-aligned moves, crisp cuts on the beat |
| Playful, springy | Overshoot on prominent moves, a lively stagger, one signature bounce |

Read the brand's signature motions from `DESIGN.md`. Use them at the key moments: the hook, the payoff, the end card.

## 4. Consistency across shots

Generated clips cut together drift: a different face, a different light, a different color cast in every shot. Plan against drift before the first generation.

1. Fix a style line: one sentence that describes medium, lighting, lens, color and texture. Reuse it word for word in every prompt. `generate-media` owns the prompt sheet.
2. Fix the references: the same reference images for every shot of one subject.
3. Use the tool's reusable reference feature for a recurring character, product or place when it has one. Read the card for which models support it.
4. Use one model for all shots of one sequence. Models differ in color and grain.
5. Generate a still for each shot first. Approve the stills as a set on one contact sheet. Then animate each approved still.
6. Grade all shots together at the end: one color treatment across the piece.
7. Keep text, logos and interface out of generated footage. Add them in composition.
8. Record each clip's prompt, model, reference ids and job id in the prompt log.

A product in generated footage must look like the real product. Use the user's product photos as references. When the result is not faithful, use a real product shot or a 3D render through `three-d` instead.

## 5. Consistency checklist

Run it on the contact sheet of all shots before the final render.

- [ ] The same subject looks the same in every shot: face, product, place.
- [ ] Light direction and color temperature match across cuts, or change on purpose.
- [ ] The grade is one treatment.
- [ ] Type, color and logo match the frame rules.
- [ ] Motion character matches the brand in every scene.
- [ ] No generated text, no generated logo, no invented interface.
- [ ] Real product screens are real captures, not generated look-alikes.

## 6. Worked example: frame rules for a technical brand

```
Frame rules (video/frame-rules.md)
Ground: color.ink; text: color.paper; accent: color.signal (solid); gradient: hero number only (brand-required)
Type: display family at 120 px (1080 wide), weight 700, tracking -0.02em; text family 36 px
Motion: token motion.ease.out; signature move: line draw then fill, token motion.duration.page
Cuts: hard cuts on the beat; one match cut at the payoff
Logo: reversed lockup, end card only, clear space = cap height of the wordmark
Imagery: real product screens; no stock people; generated footage only for the abstract hook
Reduced motion and thumbnail: static end card
```

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Template look | A vendor preset style with the brand logo pasted on | Translate the tokens into frame rules first |
| Logo redrawn | A smoother or recolored logo in the sting | Animate the supplied vector paths only |
| Long logo intro | Five seconds of logo before content | Hook first; sting at the end, two seconds or less |
| Shot drift | A different face or product in each clip | Style line, references, one model, stills first |
| Generated interface | A fake product screen in footage | Real captures composited in |
| Off-brand bounce | Springy type for a calm brand | Follow the brand's motion character |
| Font swap | A renderer falls back to a system face | Embed the licensed font files as the route requires |
