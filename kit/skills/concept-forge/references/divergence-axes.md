# Divergence axes

Read this file at step 9 of `concept-forge`. It holds the seven axes, value words with examples, the axis matrix, the pair table and a worked example.

Concepts that differ only in color are one concept. The axes force each concept to commit to a different answer on the parts that carry an idea. Generating many distinct options before choosing one is the core of early exploration (Principles of Product Design, ch. 3; Design Collaboration Handbook, ch. 6).

## 1. The seven axes

Give each concept one value on each axis. Write the value as a short phrase from the concept's own idea, then name its class from the list. Two concepts differ on an axis when their classes differ.

| Axis | The question | Classes |
| --- | --- | --- |
| Composition logic | What organises the space? | `object` (one hero object), `sequence` (a path in time or steps), `map` (places), `index` (a list or table), `stage` (one scene), `collage` (layered fragments), `document` (a page, form or ledger), `field` (an open surface) |
| Type voice | How does the lettering speak? | `instrument` (engraved, stamped, stencilled), `hand` (written, signed), `editorial` (long reading), `signal` (signage, short and large), `technical` (data, measure), `quiet` (recedes behind content) |
| Color logic | Where does color come from and what does it do? | `material` (the subject's own matter), `signal` (safety or status marks), `time` (light at an hour or season), `data` (color encodes values), `mono` (one ink), `none` (black and white) |
| Image source | Where do pictures come from? | `photo-real` (photographs of the real subject), `artifact` (scans of the subject's documents and objects), `drawn` (illustration), `diagram` (explanatory drawing), `data` (generated from data), `type-only` (no pictures), `3d` (models) |
| Motion idea | What moves, and why? | `physical` (moves like a mined material), `reveal` (uncovers in reading order), `live` (shows real change), `response` (answers input only), `still` (nothing moves) |
| Material metaphor | What is the surface made of? | `paper`, `metal`, `glass` (only when the subject is glass), `fabric`, `stone`, `wood`, `light`, `liquid`, `screen-native` (no metaphor) |
| Interaction model | How does the person act on it? | `browse`, `search`, `follow` (a guided path), `manipulate` (drag, turn, set), `converse`, `compare`, `wait` (glanceable, ambient) |

Rules:

- The class must follow from the concept. "Image source: artifact, because the ticket stub is the interface" is a value. "Image source: photo-real, because photos look nice" is not.
- A design system that fixes type or color fixes those two axes for every concept. Mark them `fixed` and count only the open axes. State the count in force in `summary.md`.
- When no class fits, write the nearest and note the difference. Propose a new class in the skill's `refinement-log.md`.
- `glass` as a material needs a subject made of glass. As a costume it is a tell (`TELL_GLASS_EVERYWHERE`).

## 2. Examples of values

| Axis | Weak value | Strong value |
| --- | --- | --- |
| Composition logic | "modern grid" | "sequence: the page is the crossing, pier to pier, top to bottom" |
| Type voice | "clean sans" | "signal: departure-board lettering, set large and few" |
| Color logic | "brand blue" | "time: the fog gray of the dawn pier, and the horn-signal orange" |
| Image source | "hero image" | "artifact: scans of punched paper tickets" |
| Motion idea | "smooth animations" | "live: the boat mark moves with the real position" |
| Material metaphor | "cards" | "paper: tickets, stubs and chalk" |
| Interaction model | "intuitive" | "wait: the page answers one question at a glance from the door" |

Note: a strong color value names objects and roles, not hue words. The concept sentence still holds no color word; the axis value may name an object whose color is known.

## 3. The axis matrix

Put the matrix in `design/concepts/summary.md`. Rows are axes, columns are concepts, cells are classes with a short value.

```
| Axis | 1 Chalk board | 2 Ticket stub | 3 The crossing |
| --- | --- | --- | --- |
| Composition | index: the board's rows | object: one stub per trip | sequence: pier to pier |
| Type voice | hand: chalk lettering | instrument: punched and stamped | signal: departure lettering |
| Color logic | mono: chalk on slate | material: card stock and punch ink | time: dawn fog and dusk lamps |
| Image source | type-only | artifact: ticket scans | data: live position line |
| Motion | still | response: the stub tears on tap | live: the boat mark moves |
| Material | stone: slate | paper | light |
| Interaction | wait | manipulate | follow |
```

## 4. The pair table

For each pair, count the axes whose classes differ. Default: each pair differs on three axes or more.

```
| Pair | Differs on | Count | Pass |
| --- | --- | --- | --- |
| 1 and 2 | composition, type, color, image, motion, material, interaction | 7 | yes |
| 1 and 3 | composition, type, color, image, motion, material, interaction | 7 | yes |
| 2 and 3 | composition, type, color, image, motion, material, interaction | 7 | yes |
```

When a pair fails:

1. Find the axes the pair shares.
2. Ask which concept owns that shared answer more strongly. Keep it there.
3. Replace the other concept with a struck or unpicked seed that answers the shared axes differently.
4. Re-score the matrix. Do not rename a class to pass. Two concepts with one answer under two names are one concept.

A matrix where every pair differs on all seven axes is not a goal. Concepts that share one or two quiet axes can still be distinct ideas.

## 5. Choosing which seeds to score

Pick the seeds before you build the matrix, by category (Design Thinking Handbook, ch. 4; Design Collaboration Handbook, ch. 6):

- Easy: the seed that is cheapest to build and still answers the brief.
- Delightful: the seed most likely to make a viewer smile or retell it.
- Long shot: the seed that breaks the most category conventions.

Rules:

- Never pick only the safe seeds. At least one picked seed is not the lowest-risk choice.
- For a wild seed, write what is attractive in it. That quality can survive into a safer concept.
- A user seed from step 2 is always scored. It may lose, but it gets a column.

## 6. Failure patterns

| Pattern | Sign | Fix |
| --- | --- | --- |
| One idea in three palettes | The pairs differ only on color logic | Replace two seeds; start each from a different mined list |
| All index | Every concept is a list or a grid | Give one concept a sequence or an object composition |
| Default image source | Every concept uses photographs of people at screens | Use an artifact, a diagram or no picture in one concept |
| Motion as a reflex | Every concept reveals content on scroll | Give one concept `still` and one `live` or `response` |
| Metaphor drift | Glass, glow or neon as the material with no subject reason | Pick the material from the mined materials list |

## Sources

- Principles of Product Design (DesignBetter), ch. 3: start wide, distinct options differ in structure, not only in color or font.
- Design Collaboration Handbook (DesignBetter), ch. 6: diverge, then converge; vote in categories; keep a bold option alive.
- Design Thinking Handbook (DesignBetter), ch. 4: select across several criteria; carry more than the safest idea.
