# Axes, baselines, scales and honesty checks

Read this file at step 6 and step 14 of `data-viz`. It covers axes and baselines, scale types, dual axes, aspect ratio, normalisation, uncertainty, smoothing, sizes of marks, and the honesty checks that run before delivery.

Evidence. The zero-baseline rule for bars and the line-baseline rule come from Datawrapper Academy and think-cell guidance (search summaries). The lie factor comes from Tufte, chapter 2, from memory; its band is a default. The point-to-point line rule comes from the Claude Data type design defaults (read 2026-11-23). Other rules are GDH practice written as defaults.

## 1. Baselines

| Form | Rule | Reason |
| --- | --- | --- |
| Bar, column, area, stacked area | Start at zero. Gate. | Length or area encodes the value; a cut baseline multiplies the visual difference |
| Line | A non-zero baseline is allowed when change is the point. Mark it, and show the zero line when the data comes near zero | Position encodes the value; slope carries the finding |
| Dot plot | Any baseline; the axis states it | Position only |
| Diverging bar | The reference value (zero, target, average) is the baseline and is labelled | The difference from it is the finding |
| Index chart | Start every series at 100 on a stated date | Shows relative change; the base date is in the subtitle |

Rules:

- Never break a bar axis with a zigzag. Use a dot plot or a log scale, or annotate the outlier and clip it with a label.
- When a line chart's baseline is not zero, a reader must see it: a labelled axis minimum, no shaded area down to the frame.

## 2. Scale types

| Scale | Use when | Must do |
| --- | --- | --- |
| Linear | Default | Round tick values (0, 25, 50) |
| Logarithmic | Values span orders of magnitude, or the finding is about rates of growth | Say "log scale" on the axis; ticks at 1, 10, 100; never for bars from zero |
| Percent change | Comparing growth of series with different sizes | State the base period |
| Per capita or rate | Comparing places or groups of different size | State the denominator: "per 100,000 people" |
| Time | Continuous time | Equal spacing for equal time; gaps shown, not closed |

Rules:

- Normalise before comparing groups of different size. A map or bar of raw counts often shows population, not the effect.
- Keep one scale per panel. Small multiples share one scale unless the finding is about shape, then say "scales differ".
- Use equal intervals of time on the axis. A missing month keeps its slot.

## 3. Dual axes

Default: no dual axis. Two y-axes let the author choose where lines cross, which invents a relationship.

Use instead:

1. Two panels stacked with a shared x-axis.
2. An index chart (both series start at 100).
3. A scatter of one measure against the other.

A dual axis needs a written reason in `charts.md` and an axis label in the color of its series.

## 4. Aspect ratio and size

- Choose the aspect ratio so the slopes that matter are readable: neither flat nor near vertical. Default: bank the key slope toward about 45 degrees, a rule of thumb.
- Do not stretch a chart to fill a slot. Recompose it (see `composition-and-interaction.md`).
- A bar's thickness is constant; spacing between bars is about half to equal the bar thickness (default).
- Default: at least 12 px chart text, line strokes 1.5 to 2.5 px, point markers 6 to 10 px. Thin hairlines vanish on low-density screens.

## 5. Ticks, gridlines and axes

- Default: three to six ticks per axis, at round values.
- Gridlines: light, behind the data, only on the value axis. Remove them when values are labelled directly.
- Axis titles only when the unit is not in the subtitle or labels.
- Axis labels horizontal. When category labels do not fit, switch to horizontal bars.
- Put the value axis on the side the eye reaches first for the finding. A time series that ends at the latest value often reads better with a right-hand axis.
- Format tick labels with units and abbreviations: "1.2M", "40%", "Q3 2025".

## 6. Lines and points

- Draw lines point to point. A smoothed curve shows values the data does not have.
- Mark the observed points when there are few (under about 20). With many, a plain line is enough.
- Break the line where data is missing. Do not draw across the gap.
- Show a projection or estimate in a different line style (dashed) and label it.

## 7. Uncertainty

- Show intervals when the data has them: error bars, a shaded band, or a range dot plot. Name the interval: "90 percent interval".
- Show a lift or a difference with its interval. A point estimate alone overstates certainty.
- Small samples: show the count ("n = 23") and widen the caveat.
- Survey data: state the margin of error in the note.

## 8. Area and pictorial marks

- When a mark's size encodes a value (bubbles, proportional symbols), scale area, not radius or height. Radius ratio is the square root of the value ratio.
- Pictograms: repeat equal icons (one icon = a stated quantity). Never scale one icon by height; its area grows with the square.
- Treemaps and waffles: area equals share; label shares in numbers.

## 9. Honesty checks

Run all of these at step 14 on the rendered chart. Record each result in `charts.md`.

| Check | Pass when | Class |
| --- | --- | --- |
| Values | Every labelled and plotted value matches the data | Gate |
| Order and units | Category order, units, period and labels match the data | Gate |
| Baseline | Bars and areas start at zero; other baselines are marked | Gate |
| Invented points | No smoothing or interpolation draws values that do not exist; gaps stay gaps | Gate |
| Source | Source, unit and period are on the chart | Gate |
| Lie factor | The visual size of an effect matches the data size of the effect, near 1 (Tufte's band 0.95 to 1.05) | Default |
| Truncation | No axis cut makes a small change look large | Default |
| Normalisation | Rates used where groups differ in size | Default |
| Cherry-picking | The period shown does not hide a contrary trend just outside it; state the reason for the window | Default |
| Comparison fairness | Compared series share units, scales and definitions | Default |
| Causation | Correlation is not titled as cause | Default |
| Uncertainty | Intervals shown where the data has them | Default |
| Precision | Decimals match the data's real precision (three to four significant digits) | Default |

Lie factor in practice: measure the change in the mark (bar length, area) and divide by the change in the data. A bar that doubles in length for a 20 percent rise has a lie factor near 5.

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Truncated bars | A 3 percent difference looks like 3 times | Bars from zero, or a dot plot |
| Dual-axis romance | Two lines cross at a "meaningful" point | Two panels or an index chart |
| Raw counts on a map | The map shows where people live | Use a rate per population |
| Smoothed story | A curve peaks between two real points | Straight segments, observed points marked |
| Closed gaps | A line runs straight across a missing quarter | Break the line; note the gap |
| Height-scaled icons | A person icon twice as tall reads four times bigger | Repeat equal icons |
| False precision | "37.482 percent" from a survey of 80 | Round to the data's precision |
