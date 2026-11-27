# Generic concept defaults

Read this file at step 7 of `concept-forge`. It holds the word check for seeds and the list of generic concepts a seed may not rely on.

The tell list in [../../design-critique/references/tells.md](../../design-critique/references/tells.md) names surface habits: gradients, glass, default faces. This file names the ideas behind them. A concept can avoid every surface tell and still be the default idea of its category. Read both.

List version: 2026-11-26. Default: review it with the tell list, every 90 days.

## 1. The word check

A seed and a concept sentence hold none of these words. The words belong to the direction stage, where `mood-board` derives them from the idea.

- Color words: any hue name (red, blue, purple, teal and the rest), any tone name (pastel, neon, muted, vibrant), any shade name (cream, charcoal, navy), and the words dark, light, monochrome and gradient.
- Typeface words: any family name, and serif, sans, grotesque, mono, slab, script, display face, variable font.
- Effect words: glass, glow, blur, gradient, shadow, neon, noise, grain, parallax, 3D tilt, glossy.
- Empty qualifiers: modern, clean, sleek, minimal, bold, premium, elegant, playful, cutting-edge, next-generation. A brand word from the brief may stay, but it is not an idea.

Test: delete every word on the list from the sentence. When nothing concrete is left, the seed was a style. Rewrite it from a mined item.

## 2. Generic concepts

A seed relies on a pattern below when the pattern is its main idea, not a detail. Strike such a seed and record the row number in `summary.md`. A pattern the design system requires is `brand-required`; record its source.

| # | Generic concept | Why it is generic | Ask instead |
| --- | --- | --- | --- |
| 1 | "Clean and modern": the product, explained simply, on a calm page | It is the brief restated. It fits every brand | What in the subject's world is plain by nature, and why? |
| 2 | "The future of <category>" | A claim, not an idea. Every launch page makes it | What does the subject do today that will still matter in ten years? |
| 3 | "AI magic": sparkles, orbs or a glowing brain stand for intelligence | The default symbol of the category | What does the product's output look like? Show that |
| 4 | "Everything in one place": a hub, a dashboard of all things | Every tool claims it. It names no ritual | Which one ritual does the product make shorter? |
| 5 | "Seamless flow": waves, ribbons or lines that connect icons | A picture of the word "integration" | What two real objects get joined, and what does the join look like? |
| 6 | "Trusted by": logos, ratings and quotes carry the page | Proof replaces the idea. Often the proof is invented | Which one true fact would earn trust, with its source? |
| 7 | "Premium dark": luxury through a dark ground and gold | A costume for the word premium | Which material in the subject's world shows care? |
| 8 | "Warm craft": cream ground, a serif, a hand-drawn squiggle | The second-wave reflex for any human brand | Which real craft tool or mark does this subject use? |
| 9 | "Terminal hacker": monospace, a blinking cursor, green on black | A costume for "technical" | What does a real expert in this field look at? |
| 10 | "Bento of features": a tile grid, one feature per tile | The content shape of a feature list, not of the subject | Which feature is the subject, and which are details? |
| 11 | "Happy people at laptops": stock photography of users | It shows the category's customer, not this one | Which object, place or document belongs only to this audience? |
| 12 | "Abstract 3D shapes": floating spheres, blobs and glass prisms | Decoration with no referent | Which real object would a viewer want to turn in their hands? |
| 13 | "Big number hero": a huge count of users, uptime or speed | A template whose figures are often invented | Which number changes a decision for this audience? |
| 14 | "Journey of steps": 01, 02, 03 with an icon each | The order is often false; the steps fit any product | Is there a real sequence? Number only that |
| 15 | "Map pin and route line" for any local business | The default symbol of local | Which route or place is this subject's own, and what happens there? |
| 16 | "Leaf and green" for anything sustainable | The default symbol of the category | What does this subject save, reuse or repair, concretely? |
| 17 | "Shield and lock" for anything secure | The default symbol of the category | What does safety look like at this subject's door or desk? |
| 18 | "Chat bubble hero" for any assistant | The interface of the category, not the subject | What does the assistant produce, and for whom? |
| 19 | "Mascot with a big smile" for any friendly brand | A shortcut for warmth, often out of place in the task | Is there a real figure in this world? Keep any character out of the work path |
| 20 | "Editorial magazine" for any brand that wants taste | A costume of publishing on content that is not news | Does the subject publish? If not, what does it make? |

## 3. Near-misses

These are not generic on their own. They become generic when they carry the whole concept.

- A grid of products in a shop. Fine as a page part; generic as the idea.
- A photograph of the founder. Fine as evidence; generic as the concept of a personal brand.
- A dark theme for a night-time use scene. Fine when the use scene is dark; generic when it comes from the category.
- A timeline for a company history. Fine when the history is the point; generic when it fills a gap.

## 4. Recording a strike

In `summary.md`, for each struck seed:

```
Struck: S<n> "<seed sentence>"; pattern: generic #<row> or tell <code>; reason: <one line>; kept quality: <what was attractive, or none>
```

Keep the kept quality. It can seed a better concept.

## 5. Keeping the list current

- Add a row when a concept shape appears in three or more projects. Default: three sightings.
- Retire a row when the shape stops appearing. A stale ban list becomes the next template.
- Log each change in the skill's `refinement-log.md`. Change the tell list and the originality library when the same look changes there.

## Sources

- Designing for Emotion (Aarron Walter), ch. 1: unmodified defaults look unfinished; ch. 2: brand contrast against category norms; ch. 3: keep a character out of the task path.
- Anthropic frontend-design skill: the default looks of generated work.
