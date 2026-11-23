# Lockups, clear space, minimum size, color and motion versions

Read this file at steps 11 and 14 of `logo-identity`. It covers the five lockups, how to fix each, the lockup ladder, clear space, minimum size, placement, co-branding, the color versions and the motion version.

Evidence. The system parts (primary lockup, stacked version, symbol alone, one-color, reversed, minimum sizes, clear space, misuse examples) come from the GDH research on logo method. "Clear space is defined from a part of the mark" is stated there with no number. The pattern of a ladder with a width below which the mark stands alone, and of clear space as a multiple of a named gap, was read in one published brand book on 2026-11-23. The numbers in this file are defaults. The project's own tests set the real values.

Terms. A lockup is one fixed arrangement of mark and wordmark. Clear space is the area around a lockup that stays empty. The minimum size is the smallest size at which a lockup may be used. The ladder is the rule that picks a lockup for an available width.

## 1. The five lockups

| Lockup | Shape | Use | Build note |
| --- | --- | --- | --- |
| Primary | Mark beside wordmark, horizontal | Default wherever width allows: headers, documents, signs | The reference drawing. Others derive from it. |
| Stacked | Mark above wordmark, centered | Square and tall spaces: covers, social cards, packaging faces | Re-space it. Do not just move the parts. |
| Mark only | The symbol | Avatars, app icons, small spaces, page furniture, where the name is already present | Needs enough recognition, or a name nearby |
| Wordmark only | The drawn name | Where the mark would be too small, or beside a large mark elsewhere | Same letters as in the primary lockup |
| Favicon | The smallest form | Browser tabs, tiny lists | Drawn for the pixel grid; often a simplified mark or one letter |

A brand with a wordmark and no symbol still needs a square form. Derive it from a letter or a cut of the wordmark. Draw it as a lockup of its own.

An optional sixth: the lockup with a tagline or descriptor. Give it its own drawing and its own minimum size. The tagline goes illegible first.

## 2. Fix each lockup

1. Each lockup is one drawing with fixed geometry. Users choose a lockup. They do not arrange parts.
2. Define the gap between mark and wordmark in units of the mark. Name the unit: `x`.
3. Common choices for `x`: the stroke width of the mark, the cap height of the wordmark, or the gap of the primary lockup itself.
4. Align by eye, then state the alignment: mark centered on the cap height, or sitting on the baseline.
5. In the stacked lockup, the wordmark is usually smaller relative to the mark. Re-balance the weights.
6. Export each lockup as its own file. The view box is tight to the artwork. Clear space is a rule, not canvas.
7. Draw one diagram that shows the gap, the alignment and `x`. It goes in the usage sheet.

## 3. The lockup ladder

Write one table that picks the lockup from the available width or the context. Fill the widths from the tiny-size test.

| Available space | Use |
| --- | --- |
| Wide, at or above the primary minimum | Primary |
| Square or tall, at or above the stacked minimum | Stacked |
| Narrower than the primary minimum | Mark only, with the name in text nearby |
| An avatar, an app icon | Mark only, inside the icon safe area |
| A browser tab, a 16px list | Favicon |
| Below the favicon minimum | No logo. Use the name in text. |

Default starting values: primary at 120 to 150px wide on screen and 20 to 25mm in print; mark at 16 to 24px and 6mm. Replace them with what the tests show.

## 4. Clear space

1. Define clear space from a part of the mark, never as a fixed pixel value.
2. Default: clear space on every side equals the cap height of the wordmark. For the mark alone: half the mark's height.
3. Write it with the same `x` as the gap rule when you can: "clear space is 2x on every side".
4. Nothing enters the box: text, an image edge, another logo, the edge of the format.
5. Show it as a diagram with the box drawn.
6. State the one allowed exception when there is one, for example a favicon that fills its square.
7. Test it: place the lockup in a real header and a real footer with the box visible.

## 5. Minimum size

1. Find the minimum by the tiny-size test. Do not choose it by wish.
2. State it for each lockup, for screen in px and for print in mm.
3. The lockup with a tagline has a larger minimum than the one without.
4. Below the minimum, the ladder names the next lockup.
5. State the print minimum only after a real print at that size, or mark it INFERRED.
6. Special processes have their own minimums: embroidery, engraving, embossing, screen print. Ask the vendor. Default for embroidery: strokes of 1mm, text of 5mm.

## 6. Placement and co-branding

Placement. Default: give the lockup one home on each medium, and say so.

| Medium | Default home |
| --- | --- |
| Web and app chrome | Top, at the start of the reading direction |
| Documents and slides | One fixed corner, the same on every page |
| Video | Centered on the opening or closing frame |
| Social avatar | Mark only, centered in the circle |

Co-branding:

1. Each logo keeps its own clear space. The gap between two logos is the sum of both.
2. Match the logos by visual mass, not by height.
3. State the order and the separator, if any.
4. A partner's logo comes from the partner's own brand page. Use it unchanged, by its own rules. Record it through `find-assets`.
5. Never redraw, recolor or crop a partner's logo.

## 7. Color versions, added last

Color is added after the black mark has passed its tests. The palette comes from `color`.

| Version | Use |
| --- | --- |
| Full color, for light grounds | The default on white and light surfaces |
| Full color, for dark grounds | The same mark with the parts that would vanish switched to light |
| One color, dark | One-ink print, stamps, low-ink documents |
| One color, light (reversed) | Dark grounds, photos with a dark backing |
| One color, brand color | Where one brand ink is available |
| Greyscale | Only when a process needs tones; often the one-color version serves |

Rules:

1. Every color in the logo is a token of the palette. The logo adds no new color.
2. Write a ground table: for each brand ground, one version. No other pairing is allowed.
3. A gradient version always has a flat twin. The flat twin is the reference.
4. Run the greyscale test and the on-photo test of the suite.
5. State the backing for photos: a solid shape, a scrim, or "dark and calm areas only".
6. Print values: give CMYK and a spot color only from a print professional or a proof. Until then, mark them INFERRED.
7. An existing brand's logo colors are fixed. This skill changes them only in the `refresh` mode, with a yes.
8. Do not tune the logo to pass a text contrast ratio by changing a brand color. State the allowed grounds.

## 8. The motion version, last and only on request

A logo animation is a version of the mark. It is not a new mark.

1. Start only after the static system is approved.
2. Read the misuse list first. Some brands forbid animated, three-dimensional or gradient treatments.
3. Write the motion idea in one sentence, from the concept. The mark draws itself, assembles, or does the one thing the idea names.
4. Default: two seconds or shorter. One move. No bounce, unless the design system says so.
5. The last frame is the exact static lockup. Hold it.
6. Provide a reduced-motion fallback: the static lockup.
7. State where it may play: an app launch, a video end frame, a loading state. Not in a page header on every visit.
8. Build it from the master's paths, so the shapes match. A vector animation tool can import the SVG paths. Example card: [picsart](../../../references/tools/picsart.md).
9. Hand the build to `ui-motion` for in-product motion, or to `motion-video` for a video sting.
10. GATE: a render or an export can be a spend call. A hosted project is exposure. Ask first.
11. Deliver it with the static files: the source, a video with alpha when needed, and the still.

## 9. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Loose parts | A mark file and a wordmark file, arranged differently on each page | Fixed lockup files |
| One lockup | Only the horizontal version exists; squares and tabs improvise | Build the five |
| Pixel clear space | "20px on every side" | Define it from the mark |
| Canvas as clear space | Exports with built-in empty margins of unknown size | Tight view box; a written rule |
| Wished minimum | A minimum size the mark cannot survive | Test, then state |
| Moved, not re-spaced | A stacked version made by dragging the wordmark under the mark | Re-space and re-balance |
| New logo colors | The logo uses a color that is in no token | Use palette tokens |
| Gradient only | No flat version exists | Draw the flat twin |
| Animation first | Motion designed before the static mark is settled | Static first |
| Different end frame | The animation ends on a shape that is not the lockup | End on the exact lockup |
