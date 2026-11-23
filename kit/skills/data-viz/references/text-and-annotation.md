# Titles, labels, annotation and numbers

Read this file at step 8 of `data-viz`. It covers the text stack of a chart, titles that state the finding, subtitles, direct labels, legends, annotation, the source line, number and date formats, and failure patterns.

Evidence. "Text is part of the design", direct labels by default, and horizontal labels come from the Datawrapper blog and Academy (search summaries). The one-sentence summary under a title, signed change with its comparison, plain-word definitions and printed values come from the Claude Data type design defaults (read 2026-11-23). Tabular numerals and locale formats come from the Vercel Web Interface Guidelines (read 2026-11-23). Numbers here are defaults.

## 1. The text stack

Every presented chart carries these parts, top to bottom.

| Part | Content | Example |
| --- | --- | --- |
| Title | The finding, in one sentence | "Tickets closed within a day rose from 33 to 51 percent" |
| Subtitle | Measure, unit, population and period | "Share of support tickets closed within 24 hours, by quarter, 2024 to 2025" |
| Chart | Marks with direct labels and annotations | |
| Notes | Definitions, caveats, method | "A ticket counts as closed when the customer confirms." |
| Source | Data owner and date of extraction | "Source: support desk export, 2026-01-08" |

## 2. Titles

- State the finding: subject, direction, size. "Revenue grew 18 percent in 2025", not "Revenue 2025".
- Keep it to one line where you can; two at most.
- Use the reader's words, not database field names.
- A title must be true for the whole chart. If one region fell while the rest rose, the title says so or the chart is split.
- An exploratory or reference chart (a lookup table, an appendix) may take a descriptive title. Label it as such.
- In a dashboard, a panel title can be the metric name; the one-sentence summary at the top of the screen carries the finding (see `dashboard-design`).

## 3. Direct labels

- Label series at the end of the line or beside the bars. Use the series color when it passes 4.5:1. Otherwise use the text color with a colored key mark.
- Label the values worth reading: the latest point, the maximum, the one the title names. Not every point.
- Use a legend only when direct labels do not fit: dense small multiples, a small phone layout, or many overlapping series. Place it above the chart, in the order of the data.
- Bars: put the value at the bar end, inside for long bars and outside for short ones, consistently.
- Avoid labels that collide. Measure margins from the labels as drawn; nudge or drop the lower-priority label.

## 4. Annotation

Annotation turns a chart into an explanation. Add it where the reader would ask "why there?"

| Annotation | Use for | How |
| --- | --- | --- |
| Event line | A launch, a policy change, an outage | A thin vertical line with a short label |
| Callout | One point the finding names | Label plus a short line to the point |
| Shaded band | A period (a recession, a campaign) or a target range | Light fill behind the data, labelled |
| Reference line | Target, average, last year | Labelled line, distinct style |
| Range note | Uncertainty, a data gap | Short text beside the gap |

Rules:

- Default: one to three annotations per chart. More competes with the data.
- Keep annotation text short: a clause, not a paragraph.
- Annotation text passes 4.5:1 and sits clear of marks.

## 5. Numbers

- Use tabular numerals for numbers compared in columns, axes and changing values.
- Format for the reader's locale: decimal and thousands separators, date order.
- Default: three to four significant digits. "1.24M", not "1,243,871".
- Show units once: in the subtitle, the axis title, or the first label ("$4.2M", then "3.1M").
- Signed change shows its sign and its comparison: "+12% vs Q3". Color the change by whether it is good for the reader's goal, not by its sign; a fall in costs is good.
- Percent versus percentage points: a rate from 10 to 12 percent is "+2 points" or "+20 percent". Say which.
- Parse date-only strings as UTC in code, so a date does not shift by a day for some readers.
- Typographic detail: proper minus sign in negative values, non-breaking space between a number and its unit, the ellipsis character.

## 6. Definitions and caveats

- Define a metric in plain words where it first appears: "Active user: opened the app at least once in 28 days."
- Put each caveat beside the figure it changes, not in a footer far away.
- State the denominator of every rate.
- State filters and exclusions: "Excludes test accounts."

## 7. Source line

- Name the data owner, the dataset and the extraction date.
- When you transformed the data (rates, seasonal adjustment, rounding), say so: "Rates per 100,000, Analysis: <team>."
- A chart that leaves the project always carries its source line, even as a social image.

## 8. Typography in charts

- Use the project type tokens. One family is usually enough; the text face's tabular figures matter more than a display face.
- Default: chart text 12 px or more on screen; titles larger by the scale step; slides 24 px or more (see the `typography` size table).
- Horizontal text only. A rotated axis label means the layout must change.
- Sentence case for titles and labels, unless the design system says otherwise.

## 9. Worked rewrite

Before:

```
Title: Q-o-Q NPS by Segment
Legend: SMB, MM, ENT, (blue, red, green)
No source
```

After:

```
Title: Enterprise customers now rate us highest, up 14 points since Q1
Subtitle: Net promoter score by customer segment, quarterly, 2025
Labels: "Enterprise 52" (accent), "Mid-market 38", "Small business 31" (gray), at line ends
Annotation: event line at Q2, "New onboarding"
Note: NPS = percent promoters minus percent detractors; n per quarter 180 to 240
Source: Customer survey, exported 2026-01-12
```

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Topic title | "Revenue by quarter" | State the finding |
| Legend hunt | Colors explained in a box far from the lines | Direct labels |
| Field names | "cnt_ord_7d" on an axis | Reader words; definitions in notes |
| Tooltip-only values | Key numbers appear only on hover | Print them on the chart |
| Unit soup | Units on every tick and label | State the unit once |
| Sign as judgment | A cost decrease in red | Color by good or bad for the goal |
| Missing source | A chart image shared without origin | Source line on every chart |
