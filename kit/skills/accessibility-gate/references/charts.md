# Checks for charts, maps and graphs

Read this file at step 2 of `accessibility-gate` when the work holds a chart, a dashboard tile, a map, a network graph or an infographic figure. Classes and source classes follow the legend in the web and app reference.

Chart design belongs to `data-viz`, `dashboard-design`, `network-graph` and `infographic`. This file only checks whether people can perceive and operate the result.

A chart is an image that carries meaning. Three groups of people meet it differently: people who cannot tell some colors apart, people who cannot see it, and people who use a keyboard. Check for each.

## 1. Checks

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| C1 | Series and categories differ by more than hue: a direct label, a marker shape, a line style, a pattern or a position | Gate | Kernel: no meaning by color alone | Grayscale, color-vision simulation |
| C2 | Marks that carry data are 3:1 or more against the ground: lines, bars, points, map borders | Gate | Kernel floor: meaningful graphics | Contrast, kind `ui` |
| C3 | Text in the chart is 4.5:1 or more: titles, axis labels, data labels, annotations | Gate | Kernel | Contrast |
| C4 | The chart has a text alternative that states the finding, not only the chart type | Gate | Kernel floor | Read the alternative alone |
| C5 | An interactive chart can be operated by keyboard: focus reaches the points or the series, and details open | Gate | Kernel | Keyboard pass |
| C6 | Status is never shown by color alone: an alert tile also has an icon or a word | Gate | Kernel | Grayscale |
| C7 | An animated chart honors reduced motion and shows its final state at once | Gate | Kernel | Reduced motion |
| C8 | The data is available as a table, or as a download, near the chart | Default | Read: research notes on chart practice | Look |
| C9 | Chart text is 12 px or more | Default | Rule of thumb | Measure |
| C10 | Series are labeled directly. A legend is used only when direct labels do not fit, and it sits near the data | Default | Search: Datawrapper guidance | Look |
| C11 | The tooltip is not the only place a value appears. Key values are labeled on the chart | Default | Rule of thumb | Look without hover |
| C12 | A categorical palette holds 8 colors or fewer | Default | Rule of thumb | Count |
| C13 | The palette is safe for common color-vision deficiencies | Default | Memory: published color-safe palettes | Simulation |
| C14 | Adjacent colors differ in lightness as well as hue | Default | Documented: design canvas contrast rule | Grayscale |
| C15 | Red and green are not the only pair that separates two meanings | Default | Rule of thumb | Simulation |
| C16 | Axis labels are horizontal. A layout that needs rotated labels is changed | Default | Search: Datawrapper guidance | Look |
| C17 | A line chart holds 4 to 5 lines at most. More go to small multiples | Default | Rule of thumb | Count |
| C18 | Sequential and diverging scales are perceptually ordered | Default | Memory | Grayscale: the order must survive |
| C19 | Numbers use tabular numerals and the locale's format | Default | Read: Vercel | Look |
| C20 | A live chart states when the data was last updated, in text | Default | Rule of thumb | Look |

C2 has one common exception in practice: a light gridline is decoration, not data. It may sit below 3:1. A reference line that the reader must see is data.

## 2. The text alternative

Gate C4 is the check that fails most often, because "Bar chart of revenue" passes for an alternative and tells nobody anything.

Write three levels. Use as many as the chart needs.

| Level | Holds | Example |
| --- | --- | --- |
| 1. Short alternative | The chart type and the finding in one sentence | "Line chart: failed inspections fell from 14 a month to 3 after the March retraining." |
| 2. Summary nearby | Two to four sentences: the trend, the extremes, the exception, the source and the date | Visible text under the chart, read by everyone |
| 3. Data | A table or a download with the values | For a person who needs the numbers |

Rules:

1. The alternative states what a sighted reader would take away. Write it from the chart's title sentence.
2. Do not list every value in level 1. That is what level 3 is for.
3. The figures in the alternative come from the data. Never write a trend that the data does not show.
4. A chart with no finding is an exploration tool. Its alternative says what can be explored and offers the table.
5. A decorative sparkline with no data meaning is hidden from assistive technology. A sparkline with meaning gets level 1.
6. The summary is visible text when possible. It helps every reader, and it cannot be lost in an export.

## 3. Color-vision check

Run both tests. One is not enough.

1. Grayscale: convert the chart to gray. Each series must still be told apart, by label, shape, style or lightness.
2. Simulation: view the chart under simulated red-green and blue-yellow deficiencies, with a tool of the `capture` capability or a browser's rendering emulation. Each series must still be told apart.

A palette that is safe in theory can still fail in a real chart: thin lines, small points and light tints lose their difference. Test the chart, not the swatches.

With no simulation tool, run the grayscale test and label the simulation UNTESTED.

Fix order when C1 fails: add direct labels first, then vary shape or line style, then change lightness, and only then change hue.

## 4. Keyboard and screen reader

For a static chart, C4 and C8 are the whole job. For an interactive chart:

| Need | Pass |
| --- | --- |
| Reach | Tab moves focus into the chart once. Arrow keys move between points or series |
| See | The focused point has a visible indicator that meets 3:1 |
| Read | The focused point announces its series, its category and its value |
| Leave | Tab moves out. Escape closes any open detail |
| Filter | Every filter, legend toggle and range control works by keyboard |
| Skip | A person can jump past the chart to the table or the next section |

Default: when a chart library cannot do this, the table in C8 becomes a requirement, not an option. Say so in the report.

## 5. Maps and network graphs

| # | Check | Class | Note |
| --- | --- | --- | --- |
| M1 | A choropleth map has a legend with labeled steps, and a table of the values by region | Default | A map alone cannot be read without sight |
| M2 | Map colors are a perceptually ordered scale, checked in grayscale | Default | By C18 |
| M3 | Points on a map differ by shape or label, not only by color | Gate | By C1 |
| M4 | Pan and zoom have buttons, not only drag and pinch | Gate | Every gesture has a visible control |
| M5 | A network graph has a text summary of its findings: the largest groups, the top nodes, the bridges | Gate | By C4 |
| M6 | Community colors are 8 or fewer, and labels mark the nodes named in the story | Default | Rule of thumb |
| M7 | Hover highlight in a graph also works on focus | Default | Nothing by hover alone |
| M8 | A layout animation stops under reduced motion and settles by itself | Gate | By C7 |

## 6. Worked example

A dashboard tile, invented for this example: failed inspections by month for three regions, as a line chart with a color legend, on light and dark themes.

- C1: the three lines differ only in hue. Grayscale shows two of them as the same gray. Fail. Fix path: direct labels at the line ends, and a dashed style for one series.
- C2: the lightest line is 2.1:1 on the light ground. Fail in the light theme only. The dark theme passes at 5.6:1. Both results go in the report, by theme.
- C4: the alternative reads "Line chart". Fail. Rewritten from the tile's own title sentence, with the real figures from the data.
- C5: the chart is static. Not applicable, with that reason.
- C8: no table. Default not met.
- C13: no simulation tool in the session. UNTESTED. The grayscale test ran.
- Verdict: fail. Three gates failed, one default not met, one check untested.

## 7. Common failures

| Name | Sign | Check |
| --- | --- | --- |
| Legend by color | Small color squares far from the lines | C1, C10 |
| Chart-type alt | "Bar chart" or "Graph" as the alternative | C4 |
| Tooltip only | Values exist only on hover | C11, C5 |
| Rainbow scale | An ordered measure on a rainbow | C18 |
| Pale series | A light tint that vanishes on the ground | C2 |
| Red and green status | Good and bad told apart by those two colors alone | C6, C15 |
| Tiny labels | Axis text below the floor | C9 |
| Swatch test | The palette was checked, the chart was not | Part 3 |
| Mouse-only chart | Points that only a pointer can reach | C5 |
