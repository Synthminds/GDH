# Data colors against brand colors

Read this file at step 12 of `color`, when the product shows charts, maps or data states. It covers why data needs its own colors, the three palette types, how to build each, how they relate to the brand, the tokens, the checks and the failure patterns.

Evidence. "Choose the palette by data type" and direct labelling come from Datawrapper material confirmed by search only. "Marks start muted with one accent on the subject", "the brand color first, then colors that differ clearly" and "color a change by whether it is good, not by its sign" come from the Claude Data type rules, read 2026-11-23. "Charts use color-blind-friendly palettes" comes from the Vercel guidelines. The limit of eight categorical colors and the perceptual ordering of sequential scales are recalled from memory. Every number here is a default. The hex values in the worked sets were computed from the worked ramp; their color-blind safety is UNTESTED.

Division of work. This skill builds the data color tokens. `data-viz` chooses the chart and applies the colors. `dashboard-design` places charts on a screen. When the host has its own chart skill, follow it for chart form and give it these tokens.

Terms. A series is one set of marks in a chart. A categorical palette separates groups. A sequential palette orders values from low to high. A diverging palette shows values on two sides of a midpoint.

## 1. Why brand colors are not data colors

| Brand and interface colors | Data colors |
| --- | --- |
| Chosen for identity and meaning in controls | Chosen so that marks can be told apart or ranked |
| One hue leads | Several hues with equal weight, or one hue in ordered steps |
| Status hues mean good, bad, warning | No built-in judgment, unless the data is a judgment |
| A ramp's light steps are grounds | Every step must be visible as a mark on the chart ground |

Rules:

1. Do not use the brand ramp's steps 1 to 7 as series colors. They vanish on the ground.
2. Do not use status colors as series colors. A red series reads as "bad".
3. Do use the brand color as the first series or as the highlight. It ties the chart to the product.
4. Use a status color in a chart only when the mark states that status: over budget, failed, late.
5. Color a change by whether it is good for the reader, not by its sign.

## 2. Choose the palette type

| The data is | Type | Example |
| --- | --- | --- |
| Groups with no order | Categorical | Product lines, regions, teams |
| One measure from low to high | Sequential | Density, count, share |
| A measure around a meaningful midpoint | Diverging | Change from last year, above and below target |
| One thing among many | Highlight and mute | This year against all other years |

Default: start with highlight and mute. One accent on the subject and a neutral for the rest answers most chart questions. Add hues only when the reader must tell groups apart.

## 3. Build a categorical palette

1. Default: eight colors at most. With more groups, show the top groups and merge the rest into "other".
2. Put the brand color first.
3. Pick the next hues far apart on the wheel. Default: 40 degrees or more between neighbors.
4. Alternate lightness between neighbors in the order of use. Default: a difference of 0.15 in OKLCH lightness or more. Then adjacent series differ without hue.
5. Keep chroma in one band. One neon series among quiet ones reads as the important one.
6. Check each color against the chart ground. A mark that must be told from the ground needs 3:1. A light color that fails takes a darker outline or a direct label.
7. Fix the order. Series one always takes color one. The same entity keeps its color across every chart.
8. Never rely on the palette alone. Label each series directly, or vary line style, marker or position.
9. Run the color-blind simulation on a real chart with all series shown.
10. With no brand hue to keep, start from a published color-blind-safe set. See the contrast reference.

## 4. Build a sequential palette

1. Use one hue, or two neighboring hues.
2. Lightness changes in one direction only. On a light ground, light means low and dark means high. On a dark ground, flip it.
3. Default: five to seven steps for a stepped scale. A continuous scale interpolates in OKLCH between the ends.
4. The lightest step must still show on the ground. Do not start at the ground color unless zero means "nothing".
5. Let chroma rise toward the middle or the dark end. A gray end reads as "no data".
6. Keep a separate neutral for "no data". Never use the lowest step for it.
7. Test: convert the palette to grayscale. The order must still read.

Worked set from the hull teal ramp, light ground. Computed 2026-11-23. Low to high:

`#ddf4f3`, `#a7dddc`, `#6dbebe`, `#429c9c`, `#117878`

## 5. Build a diverging palette

1. Use two hues that a color-blind reader can tell apart. Default: blue or teal against orange. Avoid red against green.
2. The midpoint is a neutral close to the ground. It means "at the reference value".
3. Both sides have the same number of steps and matching lightness at each step.
4. Name what the midpoint is: zero, the target, the average. A diverging palette with no meaningful midpoint is a sequential palette.
5. Do not attach good and bad to the two hues unless the data is a judgment.

Worked set, light ground. Computed 2026-11-23. Below the midpoint to above it:

`#9b4805`, `#d8732b`, `#f2bf96`, `#ebf2f1`, `#89cccb`, `#429c9c`, `#0b5f5f`

## 6. Highlight and mute

1. One highlight color: the brand color or the accent.
2. One mute color: a neutral step that still reads as a mark on the ground. Default: neutral 7 or 8 on a light ground.
3. The highlighted mark also gets a direct label. Color alone does not carry it.
4. To move focus, fade the others. Do not add a third color.

## 7. Chart furniture

| Element | Color role |
| --- | --- |
| Chart ground | `bg` or `surface`; no separate tint |
| Axis lines and grid lines | `border`; light, few |
| Axis labels and annotations | `text-muted`; 4.5:1 on the ground |
| Title and values | `text` |
| Reference line or target | `text-muted` or one fixed data color, with a label |
| "No data" | A neutral with a pattern or a label |

Text inside a chart follows the text gates. Chart text sizes follow the minimum-size table of `typography`.

## 8. Tokens

Data colors live in the same `color` family, with their own prefix. Each has a value for each theme.

| Token | Use |
| --- | --- |
| `data-1` to `data-8` | Categorical, in fixed order |
| `data-seq-1` to `data-seq-n` | Sequential, low to high |
| `data-div-neg-3` to `data-div-pos-3`, `data-div-mid` | Diverging |
| `data-highlight`, `data-mute` | Highlight and mute |
| `data-none` | Missing data |

Usage note pattern: "Series 2 in every chart. Icon on bg and surface." The word "Icon" makes the script check 3:1 on those grounds. Leave the pair phrase out for a color that never needs to stand alone, and write why.

A hosted dashboard type can take a list of chart colors from a design system. Put the brand color first in that list. Read the type's own rules before you set it.

## 9. Dark theme

1. Build the data colors again for the dark ground. Do not reuse the light values.
2. Categorical colors get lighter and a little less chroma.
3. Sequential scales flip: dark means low, light means high.
4. Check each mark against the dark ground at 3:1.
5. Thin lines need more contrast than areas. Default: lines are 2px or more, or a step lighter.

## 10. Checks

1. Each chart names its palette type, and the type fits the data.
2. Categorical colors number eight or fewer.
3. No status color is a series color, except to state that status.
4. Every series has a direct label or a second cue.
5. Sequential and diverging sets keep their order in grayscale.
6. Marks that must be told from the ground pass 3:1, or have an outline or a label.
7. The same entity has the same color in every chart.
8. The color-blind simulation was viewed on a full chart, or the report says UNTESTED.
9. Every data color is a token with a value in each theme.

## 11. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Brand ramp as series | Five tints of the brand color for five unrelated groups | A categorical set; brand color first |
| Rainbow | A full-spectrum scale for ordered values | A sequential set with one-direction lightness |
| Traffic light | Red, amber and green series with no judgment in the data | Neutral hues; keep status colors for status |
| Twelve colors | A legend with twelve hues | Top groups plus "other", or small multiples |
| Legend hunt | Colors explained only in a legend far from the marks | Direct labels |
| Shifting colors | The same region is blue in one chart and orange in the next | Fix the order and the mapping |
| Invisible low end | The lowest sequential step equals the ground | Start one step darker |
| Fake midpoint | A diverging scale on data with no reference value | Use a sequential scale |
| Gray means low | Missing data drawn in the lowest step | A separate "no data" style |
| Light theme values on dark | Dark series on a dark ground | Build the dark set |
