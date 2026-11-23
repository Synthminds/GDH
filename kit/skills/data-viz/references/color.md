# Color sets for charts

Read this file at step 7 of `data-viz`. It covers which color set fits which data, highlight and context colors, color-vision safety, contrast for marks, light and dark themes, the token table and failure patterns.

Evidence. The contrast floors are the GDH kernel gate (WCAG 2.2 AA values, DOCUMENTED). The rule to start from the Okabe-Ito set when no brand hues exist, and to prefer blue and orange over red and green, comes from the Claude Design System and Design type rules (read 2026-11-23). The Okabe-Ito hex values, ColorBrewer and viridis come from memory; treat them as defaults and verify the values before you rely on them. Count limits are rules of thumb.

## 1. Precedence for chart colors

1. A color the user asked for.
2. Data-color tokens in the project design system.
3. The host chart skill's validated palette, re-tuned to the brand through its validator, when that skill is present.
4. A seed set from this file, turned into tokens by the `color` skill.

The design system supplies the hues. Every set still passes the checks in section 6, in every theme.

## 2. Pick the set by data type

| Data | Set | Build | Example use |
| --- | --- | --- | --- |
| Categories with no order | Categorical | Distinct hues of similar lightness and chroma; also distinct in lightness for the pairs that sit side by side | Product lines, regions |
| Ordered values from low to high | Sequential | One hue (or two neighbouring hues), lightness steps evenly from light to dark | Rates, densities, scores |
| Values around a meaningful midpoint | Diverging | Two hues, neutral at the midpoint, equal lightness steps on each side | Change versus last year, above or below target |
| One series in focus, the rest context | Highlight | One accent; all other series in one neutral gray | "Our product versus the market" |
| Yes or no, present or absent | Binary | One color and a neutral, or two that differ in lightness | Met target or not |

Rules:

- Never use a rainbow (many hues in spectrum order) for ordered data. It has no perceived order and creates false bands.
- The midpoint of a diverging set is a real value (zero, target, average). Say which in the legend.
- Sequential ramps run light for low and dark for high on a light ground. On a dark ground, reverse the lightness direction or test both; state the direction in the legend.
- Default: five to seven steps for a binned sequential or diverging map; continuous ramps for continuous data.

## 3. Categorical limits

- Default: eight categories at most in one chart. Beyond that, group the tail into "Other", use small multiples, or label directly and color only the ones the finding names.
- Keep one category-to-color mapping across every chart in the project. Store it as tokens: `data-cat-1` to `data-cat-8`, plus a named mapping table in `DESIGN.md`.
- Assign colors by meaning, not by order of appearance. A filter that removes a category must not shift the others' colors.
- Reserve status colors (success, warning, danger) for status. Do not reuse them as category colors.

## 4. Highlight first

The strongest chart color move is restraint.

1. Draw every series in one neutral gray.
2. Color the one series, bar or period that carries the finding.
3. Label the colored element directly; the title names it.
4. Use at most two accents per chart. A third accent means the chart has two findings.

## 5. Color-vision safety

- Series and categories must differ by more than hue. Add direct labels, position, line style, markers or patterns. Gate in `SKILL.md`.
- Colors that must be told apart also differ in lightness. Prefer blue and orange to red and green.
- Run a simulation for deuteranopia, protanopia and tritanopia, and a grayscale pass. In grayscale, the highlighted series still stands out.
- Default seed when no brand hues exist: the Okabe-Ito set, from memory: orange `#E69F00`, sky blue `#56B4E9`, bluish green `#009E73`, yellow `#F0E442`, blue `#0072B2`, vermilion `#D55E00`, reddish purple `#CC79A7`, black `#000000`. Verify the values; check each against the ground (yellow fails on white).
- Default sequential and diverging seeds: ColorBrewer ramps or the viridis family, which are perceptually ordered. Check each step against the ground.

## 6. Contrast for marks and text

| Element | Floor | Class |
| --- | --- | --- |
| Text: titles, labels, ticks, annotations | 4.5:1 against its ground | Gate |
| Large text (24 px, or about 18.66 px bold) | 3:1 | Gate |
| Marks that carry meaning: lines, bars, points, map fills that must be read | 3:1 against the ground | Gate |
| Adjacent marks that must be told apart (stacked segments, neighbouring map areas) | Default: 3:1 between them, or a separating stroke | Default |
| Gridlines and axes | Quiet, but 3:1 when they carry the reading (a target line) | Default |
| Context gray in a highlight chart | May be lighter, as long as the finding does not depend on reading it; label its values if it does | Default |

Rules:

- Check every pair in every theme. A palette tuned for light often fails on dark.
- Light sequential steps fail contrast against a white ground. Add a thin stroke around light marks, or start the ramp one step darker.
- Text placed on a colored bar uses the color's `on-` token, and passes 4.5:1.

## 7. Light and dark themes

- Define data colors per theme, not one set for both. Dark themes need lighter, less saturated hues.
- Keep the same mapping of category to hue in both themes; only lightness and chroma change.
- Check gridlines, labels and the context gray again in dark.
- A data page may follow a host theme, such as the Claude Data type. Then use its theme tokens and chart color function. Never type a brand color into the page.

## 8. The token table

Write data colors as tokens in `design/tokens.json` through `design-system`. Default names:

```
data-cat-1 ... data-cat-8      categorical, in assignment order
data-seq-1 ... data-seq-7      sequential, light to dark
data-div-neg-3 ... data-div-pos-3, data-div-mid   diverging
data-highlight                 the one accent
data-context                   the neutral for context series
data-target                    reference and target lines
```

Each token carries a usage note: the ground it was checked on and its contrast ratio.

## 9. Worked decisions

| Chart | Set | Reason |
| --- | --- | --- |
| Monthly sales of five products | Categorical, five tokens, direct labels | No order; five fits the budget |
| Unemployment rate by county | Sequential, seven steps | Ordered rate; a choropleth of a rate |
| Change in turnout versus last election | Diverging around zero | The midpoint is "no change" |
| Our app's rating versus twelve competitors | Highlight: one accent, eleven in context gray | The finding is about one series |
| Twelve regions over ten years | Small multiples, one accent per panel for the region | Twelve colors would be unreadable |

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Rainbow ramp | Ordered values in spectrum hues | Sequential ramp, one hue family |
| Every series colored | Twelve hues, no focus | Gray context, one accent |
| Status colors as categories | A "red" product line reads as a problem | Reserve status colors |
| Shifting colors | A filter changes which color means which category | Fixed mapping by meaning |
| Light step invisible | The lowest bin disappears into the white ground | Stroke or darker first step |
| Hue-only difference | Red and green lines, no labels | Labels, styles, lightness difference |
| One palette for two themes | Dark mode glows or vanishes | Per-theme data tokens |
