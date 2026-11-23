# Proportion honesty, type, color, icons and imagery

Read this file at steps 9 to 11 of `infographic`. It covers proportion rules for pictorial quantities, unit charts, charts inside the piece, type limits, color limits, icons, illustration and photos, representation of people, and failure patterns.

Evidence. "Sizes of pictorial elements proportional to the data: areas, not widths" and "icons from one set with one stroke weight, no emoji" come from the GDH research (Impeccable craft floor, read 2026-11-23, and GDH practice). The lie factor comes from Tufte, from memory. Type and color limits are GDH defaults from the research. The representation rule comes from "Designing for Emotion", chapter 4. Contrast floors are the GDH kernel gate. Numbers are defaults unless `SKILL.md` names them as gates.

## 1. Pictorial quantities must be proportional

The eye reads area. A shape that grows in both width and height to show a value doubles its area when the value grows by about 41 percent.

Rules (gate in `SKILL.md`):

| Mark | Proportional when | Wrong |
| --- | --- | --- |
| Scaled circle, square or icon | Area is proportional to the value: side or radius ratio equals the square root of the value ratio | Width or height proportional to the value |
| Repeated icons (unit chart) | Each icon is the same size and stands for the same stated quantity | Icons of different sizes in one count |
| Bar or column | Length from a zero baseline | A cut baseline; a bar drawn as a scaled 3D object |
| Filled shape (a glass, a battery, a map region) | The filled area or volume matches the share | Fill height in a shape that narrows |
| Perspective or 3D object | Avoid; perspective makes near parts look larger | Pie or bars tilted in 3D |

Checks:

- Compute the expected ratio before drawing: for values 100 and 400, a scaled circle's radius ratio is 2, not 4.
- Lie factor: the visual change divided by the data change. Default: near 1 (Tufte's band 0.95 to 1.05).
- Label the values on scaled shapes. Area is read roughly; the number carries the exact value.
- When a dramatic size difference is the point, use a bar or a unit chart; the honest area version may look smaller than the author hoped.

## 2. Unit charts (isotype-style counts)

- One icon = one stated unit. Write it: "Each figure = 1,000 people."
- Same icon, same size, same spacing. Partial icons are cropped by width only for the remainder, and labelled.
- Arrange icons in rows of a round number (10 per row) so readers can count.
- Default: use a 10 by 10 grid for a share of 100.
- Color shows the category within the count; the count itself is in the position.

## 3. Charts inside the piece

- Every chart goes through `data-viz`: form from the choice table, baselines, direct labels, source.
- Restyle charts to the piece's type and color tokens; keep the honesty rules.
- Keep charts simple: one finding per chart, the highlighted element in the accent, context in gray.
- A chart in print is vector, with real text where the format allows.

## 4. Type limits

- Default: two families at most: one for headlines and display numbers, one for text and labels. One family is often enough.
- Default: three to four sizes on one piece: headline, hero number, body, small (labels and sources).
- Use tabular numerals for numbers that are compared or aligned.
- Big numbers: set them in the display face, with the unit smaller beside them and a label that says what they count.
- Minimum sizes come from the `typography` size table for the medium. In brief: screen 12 px; slides 24 px; on a design canvas print artboard nothing under 12 px and body at 16 px; other print about 7 pt as a rule of thumb.
- Keep text horizontal. Rotated text slows reading.
- Line length for paragraphs: 45 to 75 characters.

## 5. Color limits

- Default: one main hue, one accent, and neutrals. Add data colors only where a chart needs categories.
- The accent marks the message: the hero number, the highlighted bar, the key step.
- Use the same color for the same meaning across the whole piece. A color that means "water" in one section means "water" everywhere.
- Status colors (red, green) only for good and bad, and never alone: add a word or icon.
- Text is 4.5:1 or more against its ground; large text and meaningful graphics 3:1 or more.
- Check in grayscale and with a color-vision simulation. Prefer blue and orange to red and green for paired meanings.
- Print: colors shift on paper. Ask the printer for a proof, and avoid meaning carried by subtle tints.

## 6. Icons

- One icon set, one stroke weight, one corner style, one size grid. Mixed sets read as stock clip art.
- No emoji and no Unicode glyphs as icons.
- Icons label or count; they do not decorate every heading. An icon above every section title is a tell when no higher source asks for it.
- Every icon has a meaning a reader can name. If two readers name it differently, add a word.
- Read each icon set's license through `find-assets`. Some sets forbid use in a logo; some need attribution.

## 7. Illustration and photos

- Illustration explains: a cutaway, a labelled object, a scene that shows the process. Decoration that adds no meaning is cut.
- Use one illustration style per piece.
- Draw real things with true proportions. A wrong-looking object costs trust.
- Photos: use real photos of the real subject when the piece makes claims about it. A stock photo of a generic scene adds nothing.
- Generated images: concept use only unless the user approves them as final; label them where the platform or the client requires.
- Every outside asset has a license record in `design/assets/manifest.json` before it is placed. References from galleries never ship.

## 8. People in the piece

- Represent varied people: skin tone, age, gender presentation, body type and visible disability across all figures. A single default figure repeated tells readers who belongs.
- Icons of people use a neutral figure, or a varied set.
- Never use a real person's image without the right to use it.

## 9. Restraint

- One memorable element; everything else quiet.
- Effects (shadow, glow, gradient, texture) only when the design system or the metaphor calls for them. When the design system prescribes them, they are brand-required, not tells.
- White space is part of the reading path; do not fill it with decoration.

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Inflated icons | A person icon twice as tall for twice the value | Area scaling or a unit chart |
| 3D pie | Tilted slices, front slice looks largest | Flat bar or waffle |
| Half-full glass by height | A narrowing glass filled to half its height | Fill by volume, or use a bar |
| Clip-art salad | Five icon styles and emoji | One set, one weight |
| Rainbow sections | Each section in its own color | One main hue, one accent |
| Font zoo | Four families for one page | Two at most |
| Decorative people | One default figure everywhere | Varied figures, or none |
