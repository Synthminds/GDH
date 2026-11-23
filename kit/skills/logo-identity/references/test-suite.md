# The logo test suite

Read this file at steps 10 and 14 of `logo-identity`. It lists each test with its method, its pass rule and its class, the order to run them, the test sheet and the report.

Evidence. The list of tests comes from the GDH research on logo method. The one-color, reversed, blur, competitor-sheet, clear-space and vector-hygiene tests are stated there with no number. The 16px favicon test, the 20mm print test and the embroidery minimums are rules of thumb with no source. The doodle test is attributed to Sagi Haviv and the seven questions to Paul Rand, both through secondary pages. For that reason every number in this file is a default. A gate here is a test that must be run and passed at the sizes the project itself states.

Terms. A gate blocks delivery. A default is a starting value that the user, the design system or the brief can replace. The stated minimum size is the size the usage sheet gives for a lockup.

## 1. How gates and numbers relate

A gate names a test. The project names the sizes. The defaults supply starting sizes.

Example: the tiny-size gate says each lockup is recognizable at its stated minimum size. The default says: start the favicon test at 16px. If the mark fails at 16px and passes at 20px, either redraw the small version or state 20px as the minimum and give a simpler form below it. The gate is met either way. A stated minimum that the real uses cannot respect is not a pass.

## 2. Black stage tests

Run these on the black master, before any color exists.

| Test | Class | Method | Pass |
| --- | --- | --- | --- |
| One color | Gate | Render the mark in solid black on white. No gray, no opacity. | The idea is complete. Nothing is missing that color would add. |
| Reversed | Gate | Render in solid white on black. | The mark reads the same. Counters stay open. |
| Tiny size | Gate | Render each lockup at its stated minimum size on a normal-density screen. | A person names the mark. Parts do not merge. |
| Tiny size, start values | Default | Favicon and mark at 16px, 24px and 32px. Lockup at 120px wide. | Use these when the brief gives no sizes. |
| Blur and squint | Default | Blur the mark until details vanish. | The silhouette is still distinct from each competitor's. |
| Competitor sheet | Gate | Place the mark on the competitor sheet, in black, at 32px. | A reviewer finds it at once and confuses it with no other. |
| Doodle | Default | Show the mark for ten seconds. Ask a person to sketch it. | The sketch holds the idea. |
| Three criteria | Default | Ask of the mark: appropriate, distinctive, simple. | Three yes answers, each with a reason. |
| Path hygiene | Gate | Run the hygiene list of the construction reference. | Every line is yes. |
| Square fit | Default | Place the mark in a square, a circle and a rounded square. | It sits well in each, with clear space, for avatars and app icons. |
| Print, small | Default | Print the lockup at 20mm wide in black. | The name is legible. Counters are open. |
| Rough reproduction | Default | Simulate a stamp or a stencil: thicken strokes by a small amount, then thin them. | The mark survives both. |
| Embroidery and engraving | Default | Check the stitched or engraved size: no stroke under 1mm, no text under 5mm. | Confirm with the vendor. The numbers are a rule of thumb. |

The agent cannot run the doodle test alone. Ask the user to try it with one person, or report it UNTESTED.

## 3. Color stage tests

Run these after `color` has supplied the palette and the color versions exist.

| Test | Class | Method | Pass |
| --- | --- | --- | --- |
| Greyscale | Gate | Convert the color version to greyscale. | Parts that differ in color still differ. Nothing merges. |
| On brand grounds | Gate | Place the right version on each ground the brand uses: light, dark, brand color. | The sheet names one version for each ground, and it reads. |
| Mark against ground | Default | Measure the contrast of the mark against each ground with `ds.py contrast`, kind `ui`. | Default: 3:1 or more. A logo is exempt from the text ratio, but it must be seen. |
| On photo | Gate | Place the mark on a light photo, a dark photo and a busy photo. | The sheet states the version and the backing. With that rule applied, the mark reads on all three. |
| Reversed on the brand color | Gate | White mark on the brand color. | It reads. If not, the sheet forbids that ground. |
| Color-blind | Default | View the color version in a color-blind simulation. | Parts that carry the idea stay distinct, or the idea does not depend on them. |
| One color in the brand color | Default | Render the whole mark in the single brand color. | It still reads on white. |
| Gradient fallback | Gate, when a gradient exists | Show the flat version beside the gradient version. | A flat version exists for every use where a gradient cannot print or render. |

## 4. System tests

Run these when the lockups and the files exist.

| Test | Class | Method | Pass |
| --- | --- | --- | --- |
| Clear space | Gate | Draw the clear space box around each lockup. Place it in a header beside real text. | The rule is written from a part of the mark. Nothing enters the box. |
| Lockup ladder | Default | Shrink the available width step by step. | At each width the sheet names one lockup, down to the favicon. |
| Favicon in a tab | Default | View the favicon in a browser tab, in a light and a dark browser theme. | It is recognizable in both. |
| App icon mask | Default | Apply a circle and a rounded-square mask to the app icon. | No part of the mark is cut. |
| Co-branding | Default | Place the lockup beside another organization's logo. | Each keeps its clear space. Neither dominates. |
| Wordmark license | Gate | Read the manifest record of the typeface. | The license allows logo use, or the letters are fully drawn. |
| File set | Gate | Open every exported file. | Each renders, has the right name and has a manifest record. |
| Motion end frame | Gate, when motion exists | Compare the last frame with the static lockup. | They are identical. A reduced-motion fallback shows the static lockup. |

## 5. Order of work

1. Black stage tests on each of the three directions, lightly: one color, tiny size, competitor sheet. A direction that fails is fixed or dropped before the presentation.
2. Full black stage on the chosen direction after construction.
3. Fix, then rerun the failed test and the tiny-size test. A fix for one size can break another.
4. Color stage after the palette exists.
5. System tests after the lockups and the exports exist.
6. Record every result.

## 6. The test sheet

Build one page that shows the evidence. Save it under `design/reviews/`.

| Row | Content |
| --- | --- |
| Sizes | Each lockup at 16, 24, 32, 64, 128 and 512px, in black |
| Reversal | Black on white beside white on black |
| Grounds | Each color version on each brand ground |
| Greyscale | The color version beside its greyscale conversion |
| Photos | The mark on three photos, with the stated backing |
| Field | The mark on the competitor sheet |
| Masks | The app icon under a circle and a rounded square |

Use photos the project may use. A photo from outside goes through `find-assets` first. The competitor row is reference and never leaves the review folder.

For a code-built sheet, review it as rendered. On a design canvas, follow the canvas type's own check rule.

## 7. The report

Write `design/reviews/<date>-logo-tests.md`:

```
Logo tests: <brand>, <date>, master: <path>
Stated minimum sizes: mark <px>/<mm>; primary lockup <px>/<mm>; stacked <px>/<mm>
Black stage:
  one color: PASS | FAIL <note>
  reversed: PASS | FAIL
  tiny size at stated minimum: PASS | FAIL
  competitor sheet: PASS | FAIL (<n> marks)
  path hygiene: PASS | FAIL (<points>, <paths>)
  blur, doodle, print 20mm, rough reproduction, embroidery: PASS | FAIL | UNTESTED
Color stage:
  greyscale: PASS | FAIL
  brand grounds: <ground: version, ratio> for each
  on photo: PASS | FAIL, backing: <rule>
System:
  clear space rule: <rule>; ladder: <widths>; favicon tab; app icon mask; wordmark license
Evidence: VERIFIED <tests viewed as rendered> | UNTESTED <tests not run and why>
```

A test you did not run is UNTESTED. It is not a pass.

## 8. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Color hides the fail | The mark only works in two colors | Return to the black stage |
| Minimum by wish | A stated minimum size at which the mark does not read | Raise the minimum, or draw a small version |
| Tested large only | Every test image is 500px wide | Add the size row |
| Lonely logo | Tested on white only | Add grounds and photos |
| Thin reversal | White-on-black strokes close up or glow | Adjust the reversed version |
| Unstated backing | The mark sits on photos with no rule | Write the backing rule |
| Assumed pass | "Works at small sizes" with no rendered proof | Show the size row, or write UNTESTED |
| Vendor surprise | Embroidery or engraving fails at the vendor | Ask the vendor for limits early |
