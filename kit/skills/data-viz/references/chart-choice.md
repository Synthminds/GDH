# Chart choice: finding, relationship, form and encoding

Read this file at steps 1 to 5 of `data-viz`. It covers the finding sentence, the data check, the nine relationships, the full choice table, encodings ranked by accuracy, when a table or a sentence beats a chart, and worked choices.

Evidence. The nine relationships and their chart families come from the Financial Times Visual Vocabulary (read 2026-11-23, paraphrased). The encoding ranking comes from Cleveland and McGill (1984), stated from memory: a default, not a gate. The "explore the data before choosing" rule comes from the Design Engineering Handbook, chapter 2.

## 1. Write the finding

One sentence, with a subject, a direction and a size. It is the chart's job and, later, its title.

| Weak | Strong |
| --- | --- |
| "Revenue by quarter" | "Revenue grew in every quarter of 2025, fastest in Q4" |
| "Response times" | "Half of tickets now close within a day, up from a third in 2024" |
| "Survey results" | "Younger staff rate remote work twice as high as older staff" |

Rules:

- No sentence means the task is exploration. Explore with quick, plain charts; present nothing yet. Return when a sentence exists.
- One finding per chart. A chart asked to prove two things proves neither. Split it.
- A finding with a cause ("because") needs evidence of cause. A correlation chart shows association only; readers assume a causal link, so say "linked with", not "caused by".

## 2. Check the data before the form

Write these facts in `charts.md` for each chart:

- Unit and measure: "orders, count", "revenue, EUR, nominal".
- Range and shape: min, max, typical value, skew, outliers.
- Variance: does the series move enough to see? A nearly flat series needs a different form or a different finding.
- Gaps: missing values, missing periods, changes of definition.
- Sample size: small groups get a caveat or are merged.
- Source and date of extraction.

Why: a chart that looked good with invented data can be flat or broken with real values. One team in the Design Engineering Handbook shipped line charts that were flat for almost every beta user.

## 3. The nine relationships

| Relationship | The finding talks about | Typical words |
| --- | --- | --- |
| Deviation | Difference from a reference (zero, target, average) | above, below, surplus, deficit, versus target |
| Correlation | Two measures moving together | linked with, rises with, associated |
| Ranking | Order of items | largest, top 10, ranked, leads |
| Distribution | Spread and shape of values | range, typical, outliers, skew, most |
| Change over time | A trend or a turning point | grew, fell, since, peaked |
| Magnitude | Size comparison of separate items | more than, twice, compared |
| Part to whole | Shares of a total | share, percent of, makes up |
| Spatial | Where something happens | region, map, nearest, hot spot |
| Flow | Movement between states or places | from, to, moved, converted, lost |

Name one. If two fit, the finding is ambiguous; rewrite it.

## 4. The choice table

Start from the first row of the relationship. Move down only for a stated reason.

| Relationship | First choice | Also good | Use when | Avoid |
| --- | --- | --- | --- | --- |
| Deviation | Diverging bar from a zero or target line | Dot plot with a reference line; surplus and deficit line with shaded gap | Values sit on both sides of a reference | Two separate bar series that make the reader subtract |
| Correlation | Scatter plot | Connected scatter (with time); bubble (third measure as area); heatmap of binned pairs for many points | Two continuous measures | Dual-axis line chart, which invents a correlation from scale choices |
| Ranking | Ordered horizontal bar | Dot strip or lollipop; slope chart (two times); bump chart (rank over time) | Labels are long; order matters | Unordered bars; pies; vertical bars with rotated labels |
| Distribution | Histogram | Box plot or dot strip per group; violin; beeswarm; cumulative curve | Shape and spread matter | Mean alone; bars of averages without spread |
| Change over time | Line | Column (few, discrete periods); area (one series, total matters); slope (two points); small multiples of lines | Continuous time | More than about five lines in one panel; smoothed curves |
| Magnitude | Bar or column from zero | Dot plot (when zero is meaningless); paired bars; proportional symbols for rough scale | Separate items compared | Truncated bars; 3D bars; pictograms scaled by height |
| Part to whole | Stacked bar (one bar per whole) | 100 percent bar; treemap (many parts); waffle (a share of 100); pie or donut only for two or three parts | Shares add to a meaningful whole | Pies with more than five slices; several pies compared side by side |
| Spatial | Choropleth of rates | Proportional symbols for counts; dot density; flow map | Location carries meaning | Choropleth of raw counts (it maps population); maps where a ranked bar answers better |
| Flow | Sankey | Alluvial (several stages); chord (few groups, both ways); flow map; funnel bars for strict stages | Volume moves between stages or groups | Network drawings for simple stage flows (route relations to `network-graph`) |

Rules:

- A ranked bar answers more questions than a clever form. Choose a less common form only when it shows the finding faster.
- Horizontal bars suit long category names and rankings. Columns suit time.
- Area and angle encode less exactly than length. Use them only when exact comparison is not the job.
- A map is right when the finding is about place. "Which state is highest" is a ranking; a sorted bar answers it better than a map.

## 5. Encodings ranked by accuracy

Default ranking, from most to least accurate for reading a quantity (Cleveland and McGill, from memory):

1. Position on a common scale (aligned dots, bar ends on one baseline).
2. Position on identical but unaligned scales (small multiples).
3. Length (bars without a common baseline, stacked segments).
4. Angle and slope.
5. Area.
6. Volume, curvature.
7. Color intensity (lightness), then hue for quantity.

Use it this way:

- Put the comparison that carries the finding on the top channel: position on a common scale.
- Use lower channels for secondary or categorical information: hue for group, lightness for a sequential measure, area for a rough third variable.
- Stacked bars: only the bottom segment sits on a common baseline. Put the segment that matters at the bottom, or use small multiples.
- Hue carries categories, not quantities. A rainbow for an ordered measure has no order.

## 6. When a table or a sentence beats a chart

| Situation | Better form |
| --- | --- |
| The reader needs exact values to look up | A table with tabular numerals and sorting |
| One or two numbers | A sentence or a big number with its comparison |
| Many measures per item, no single comparison | A table with inline bars or sparklines |
| The data has no pattern worth showing | A sentence saying so, and a table |

Always offer a table as the accessible form of a chart (see `accessibility.md`).

## 7. Worked choices

| Finding | Relationship | Form | Why not the obvious one |
| --- | --- | --- | --- |
| "Support tickets fell 30 percent after the help-center launch in May" | Change over time | Line with an annotated event line in May | Columns would hide the turning point inside the bars |
| "Three of twelve regions miss the target" | Deviation | Diverging bars from the target line, the three misses colored | Bars from zero make the reader find the target by eye |
| "Most orders arrive in two days; a long tail takes a week" | Distribution | Histogram with the median marked | An average of 2.9 days hides the tail |
| "Product A holds 61 percent of revenue" | Part to whole | One stacked bar or a waffle of 100 | A pie of eleven slices hides the point in noise |
| "Larger stores have lower staff turnover" | Correlation | Scatter with labelled outliers and a note "association, not cause" | A dual-axis line chart would draw a link from two scale choices |
| "Germany leads, France and Italy follow" | Ranking | Sorted horizontal bars | A map makes the reader compare colors across a continent |

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Form before question | "Make a donut of this" | Write the finding first; then the table picks the form |
| Topic title | "Sales by region" | Rewrite as the finding |
| Novelty form | A radial or 3D chart where bars would read faster | Use the first choice; keep novelty for a written reason |
| Many findings, one chart | A legend of twelve series | Split into small multiples or several charts |
| Cause implied | A correlation titled with "drives" | "Linked with", plus a note |
| Designed on invented data | Lovely mockup, flat real chart | Check the data's variance first; render real data |
