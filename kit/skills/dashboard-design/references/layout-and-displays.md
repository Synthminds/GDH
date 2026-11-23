# Layout, reading order, tiles, displays, density, color and tables

Read this file at steps 7 to 10 of `dashboard-design`. It covers layout by priority and reading order, the grid, stat tiles with comparison and context, the display for each kind of metric, density, color roles with status colors reserved, tables, the gray-box round and failure patterns.

Evidence. Top-left priority for left-to-right readers, neutral screens with color reserved for alerts, and the list of common dashboard mistakes come from Few (book review summary and memory). The hero-metric tile as a generic habit comes from the Impeccable craft floor and the Anthropic frontend-design skill (read 2026-11-23). Tabular numerals, table virtualization and skeletons come from the Vercel guidelines (read 2026-11-23). Bullet graphs and sparklines come from Few and Tufte (from memory). Numbers are defaults.

## 1. Layout by priority and reading order

1. Write the reading order as a list before any grid: status line, top metric group, its breakdown, secondary groups, detail table.
2. Put the most important group where reading starts: top left for left-to-right readers; top right for right-to-left readers.
3. Put the summary above the detail and the cause next to the effect.
4. Keep related metrics in one region. A gap between regions says the subject changes.
5. Keep a fixed position for each metric across visits. People learn where to look.
6. For a monitoring screen, keep everything on one screen at the target size. For analysis and report screens, a scroll is fine; the first screen still answers the main question.

A common reading structure:

```
[ Title, one-sentence summary, data time, active range and filters ]
[ Headline group: 3 to 5 tiles, each with comparison         ]
[ Main chart: the trend behind the headline   ][ Breakdown    ]
[ Secondary group                               ][ Exceptions  ]
[ Detail table, sortable, linked from the charts above        ]
```

Use this as a starting point, not a template. Break it when the reading order says otherwise.

## 2. Grid and spacing

- Use the design system's grid and spacing tokens. Default: a 12-column grid on desktop, one or two columns on a phone.
- Align tiles and charts on shared edges and baselines. Equal heights within a row.
- Space inside a group is smaller than space between groups.
- Size each view by its importance and its content, not to fill a uniform card grid. A screen of identical cards hides the hierarchy.
- Chart boxes have a minimum height so loading and empty states do not collapse the layout.

## 3. Stat tiles

A tile shows one metric and enough context to judge it.

Anatomy:

```
Metric name                     window ("Last 7 days")
Value with unit                 large, tabular numerals
Comparison: signed change and its reference ("-8 min vs last week")
Context: target bar, sparkline, or status word with icon
Link: to the detail view
```

Rules:

- Every tile has a comparison and states its window. A tile with only a big number fails the gate.
- The status word and icon carry meaning; color supports them. "Behind target" in text, not only an amber dot.
- Sparklines carry real data at a stated range, with the last point marked. Never a decorative squiggle.
- Show the unit and precision from the inventory. Default: three to four significant digits.
- Keep tiles quiet when things are normal. Strong color only for an exception.
- Avoid the generic tile habit: identical rounded cards of big number, small label, tiny trend and a gradient accent, repeated across the top of every dashboard. Vary size by importance and let the data shape each tile. When the design system prescribes such tiles, report it as brand-required, not as a tell.

## 4. Choose the display per metric

| The metric needs | Display | Notes |
| --- | --- | --- |
| One value against a target | Bullet graph, or value with "62 of 75" | Bullet graphs replace gauges in less space |
| One value and its recent direction | Value with sparkline | State the sparkline range |
| A trend over time | Line chart | Send to `data-viz` |
| Comparison across categories | Sorted horizontal bars | Long labels fit |
| Share of a whole with two or three parts | Single stacked bar | Not a donut wall |
| Distribution (response times) | Histogram or percentile bars | Median and tail, not an average |
| A status per item (servers, stores) | Status table or a grid of named cells with text status | Sort exceptions to the top |
| Many items with several measures | Table with inline bars | Sorting and search |
| Place | Map of a rate, or a ranked list | A ranked list often answers faster |
| Exceptions needing action | A list of items that crossed a threshold, with owner and age | The most useful block on many monitors |

Default: no decorative gauges or dials, no 3D charts, no pie with more than five slices, no radar charts for comparison. Each wastes space or encodes poorly.

## 5. Density

- Match density to the user. Operators and analysts read dense, crisp screens fast. Executives read fewer, larger numbers with a sentence.
- Density comes from removing decoration, not from shrinking text. Keep text at or above its floor.
- Default: motion is minimal in professional tools. A refresh updates values in place, without bouncing tiles.
- Use the design system's compact and comfortable spacing scales when it has them; offer a density switch only when users differ.

## 6. Color roles

| Role | Use | Rule |
| --- | --- | --- |
| Neutral | Most of the screen: grounds, text, gridlines, normal values | Default: the large majority of the screen |
| Data colors | Categories and series in charts | From `data-*` tokens; eight at most |
| Highlight | The one series or item in focus | One accent |
| Status: success, warning, danger, info | Only for status: a metric crossing a threshold, a failing service | Never as a category color; always with a word or icon |
| Selection and focus | Selected item, keyboard focus | Distinct from status colors |

Rules:

- Reserve status colors for status. When red also means "product line C", alerts stop standing out.
- Problem states use contrast; normal states stay quiet. A screen that is all green trains people to ignore it.
- Status pairs stay distinguishable for color-vision deficiency, and in grayscale, because a word or icon carries the state.
- Check every pair in every theme: text 4.5:1, marks and control outlines 3:1.

## 7. Tables

- Right-align numbers; use tabular numerals; same precision per column.
- Left-align text. Put the identifying column first and keep it fixed when the table scrolls sideways.
- Headers name the unit. Sort on any column; show the sort direction.
- Default: a table of more than fifty rows paginates or virtualizes.
- A wide table scrolls inside its own wrapper, never the whole page.
- Inline bars or sparklines in cells use the same scale down a column.
- Row status shows a word or icon plus color.
- Empty table: a sentence with the reason and the active filters.

## 8. The gray-box round (step 10)

1. Draw the layout as gray boxes with the real metric names, real numbers and real labels.
2. Show it with the reading order list and the metric inventory.
3. ASK: "Keep, change or remove, for each block?" Also ask: "What do you look at first? What do you do next?"
4. Record the answers per block in `design/decisions.md`.
5. Change only what was asked. Build high fidelity only after the answer.

## 9. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Card wall | A grid of identical tiles with no hierarchy | Size by importance; group by question |
| Hero-metric habit | Big number, small label, gradient accent on every tile | Comparison and context in each tile; quiet styling |
| Scroll to status | The answer to "is anything wrong" is below the fold | Status first in the reading order |
| Rainbow screen | Many colors, alerts invisible | Neutral screen; status colors reserved |
| Gauge garden | Dials for every metric | Bullet graphs or values with targets |
| Decorative sparkline | A squiggle with no range | Real data, stated range, last point marked |
| Table as afterthought | Unsorted, misaligned numbers | Table rules in section 7 |
