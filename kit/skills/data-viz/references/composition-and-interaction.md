# Clutter, small multiples, interaction and responsive charts

Read this file at steps 9 and 10 of `data-viz`. It covers removing clutter, the series budget, small multiples, chart sets, interaction that answers a question, motion, and recomposing charts for small screens.

Evidence. Small multiples and data-ink come from Tufte (from memory). The line-count budget is a rule of thumb found by search. Recompose-not-shrink, horizontal labels and direct labels on mobile come from Datawrapper (search summaries). Overview first, then zoom and filter, then details on demand, is Shneiderman (1996, from memory). The 400 px reading width, printed values over tooltip-only values and reduced-motion entry come from the Claude Data type design defaults (read 2026-11-23). Numbers are defaults.

## 1. Remove clutter

Remove each item that carries no data or no reading aid.

| Remove | Keep instead |
| --- | --- |
| Boxed plot area and chart borders | White space |
| Heavy or dense gridlines | Few light gridlines on the value axis, or none with direct labels |
| Legend boxes | Direct labels |
| Repeated units on every tick | The unit once in the subtitle |
| Shadows, gradients, 3D, glossy bars | Flat fills |
| Decorative icons inside the chart | Nothing, or one meaningful marker |
| Default library styling (tiny gray labels, heavy axes) | Token-based type and color |

Test: remove an element. If no reader question gets harder, it stays removed.

## 2. The series budget

- Default: four to five lines in one line chart; more becomes spaghetti.
- Default: eight categorical colors per chart.
- Default: five slices at most in a pie or donut; three or fewer is better.
- Past the budget, choose one of: small multiples, highlight one series and gray the rest, aggregate the tail into "Other", or split into several charts.

## 3. Small multiples

A grid of small charts of the same form, one per category or period, on the same scales.

Rules:

- Same chart type, same scales, same axis ranges, same order of panels across the grid. Say "scales differ" when the finding is about shape and you free them.
- Order panels by meaning: by the value the finding is about, by region, or by time. Not alphabetically by default.
- Put the shared axis labels once, on the outer edge of the grid.
- Highlight within each panel: the panel's own series in the accent, other series as faint context, or no context.
- Default: two to four columns on desktop, one or two on a phone. Panel titles name the category.
- Use them for: many series over time, the same distribution across groups, a dynamic process at fixed moments.

## 4. Chart sets

When several charts sit together (a report page, a slide set, a story):

- Each chart has its own finding. The set has an overall message stated first.
- Shared encodings: the same category keeps the same color across every chart.
- Align axes and baselines when charts sit side by side, and use the same scale where comparison across charts is intended.
- Order charts as an argument: context, the main finding, the explanation, the implication.

## 5. Interaction that answers a question

Add interaction only when a reader question needs it. For each control, write the question it answers.

| Interaction | Answers | Rule |
| --- | --- | --- |
| Tooltip on hover or focus | "What exactly is this value?" | Key values are also printed on the chart; tooltips reach no phone or screenshot |
| Highlight on hover or select | "Which series is this?" | Dims others; keyboard selection does the same |
| Filter or toggle | "What about my segment?" | Active filter visible, with counts; default state answers the main question |
| Zoom or brush | "What happened in this period?" | Reset control; the default view shows the finding |
| Drill-down | "What makes up this total?" | Breadcrumb back; the parent stays reachable |
| Show the data | "Can I check the numbers?" | A table view or a download, labelled with source |

Order of interaction design (Shneiderman, from memory): overview first, then zoom and filter, then details on demand.

Rules:

- The static default view must state the finding with no interaction.
- Every interaction works by keyboard, with visible focus.
- Interaction state that a reader may share goes in the URL.
- Give every plotted chart a tooltip in an interactive page, and still print the values worth reading.

## 6. Motion

- Use motion to show change between states (a filter, a new period), not to decorate the entry.
- Play entry motion once, inside a reduced-motion preference check. Under reduced motion, show the final state at once.
- Animate positions of the same marks between states so the eye can follow; do not fade everything out and in.
- Default: transitions of 200 to 400 ms for data changes; never let motion delay reading. Timings defer to `ui-motion` and the design system's tokens.
- Nothing flashes more than three times a second.

## 7. Responsive charts

Recompose; do not shrink. A wide chart scaled down to a phone has unreadable text and crowded marks.

| Desktop form | Small-screen form |
| --- | --- |
| Vertical columns with long labels | Horizontal bars |
| Many ticks on a time axis | Fewer ticks; first and last labelled |
| Legend at the side | Direct labels or a legend above |
| Wide small-multiple grid | One or two columns, stacked |
| Dense line chart of many series | Highlight one series; others gray or in a selector |
| Annotation text beside points | Numbered markers with notes below |
| Wide table | Horizontal scroll inside its own wrapper, first column fixed |

Rules:

- Set breakpoints where the chart breaks, not at device names.
- Keep CSS and script breakpoints in sync for charts drawn in code.
- Default: the chart reads at full width and at about 400 px wide (a side panel or a phone). Test both.
- Chart text stays at or above its floor at every width; no scaling of text with the SVG.
- Use no fixed pixel widths for chart containers; measure the container and redraw on resize.
- Keep the aspect ratio sensible on tall phones: a time series may need more height and fewer points.

## 8. Print and static export

- A chart for print or PDF uses a light ground, a vector format (SVG or PDF) and text as text.
- Check it in grayscale: the highlight still reads.
- Social images: recompose for the frame size and add the title and source into the image.

## 9. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Spaghetti | Ten tangled lines | Small multiples or highlight one |
| Shrunk desktop chart | 8 px labels on a phone | Recompose per breakpoint |
| Interaction as rescue | The finding appears only after three clicks | Default view states the finding |
| Hover-only data | Values hidden from touch and screenshots | Print key values; tooltips add detail |
| Decorative entry motion | Bars grow on every scroll | Motion for change only; once; reduced-motion check |
| Free scales by accident | Small multiples look equal but are not | Shared scales, or say "scales differ" |
