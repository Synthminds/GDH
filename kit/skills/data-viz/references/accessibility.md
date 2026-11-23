# Accessible charts

Read this file at step 11 of `data-viz`. It covers the text alternative, the table fallback, chart semantics in code, keyboard access, color and contrast, motion, and the accessibility review for a chart.

Evidence. The contrast floors and "color is never the only carrier" are the GDH kernel gate (WCAG 2.2 AA values, DOCUMENTED). `role="img"` with an `aria-label` per chart SVG comes from the Claude Data type design defaults (read 2026-11-23). Other rules are standard practice written as defaults; `accessibility-gate` runs the full test.

## 1. Two alternatives for every chart

| Alternative | Content | Where |
| --- | --- | --- |
| Text summary | Two to four sentences: what the chart shows, the finding with its numbers, the range, and any notable exception | Next to the chart, visible or reachable; or as the description of the chart element |
| Data table | The values behind the chart, with units, sorted the way the finding reads | A "Show data" control, a table below the chart, or a downloadable file in an image-only medium |

A short label ("Line chart of revenue") is not enough. The summary carries the finding.

Template for the summary:

```
<Form> of <measure> by <dimension>, <period>.
<The finding, with its key numbers.>
<Range or context: lowest, highest, typical.>
<Any exception or caveat.>
```

Example: "Line chart of the share of support tickets closed within a day, by quarter, 2024 to 2025. The share rose from 33 percent to 51 percent, with the largest jump after the new help center launched in Q2 2025. The lowest quarter was Q1 2024 at 31 percent. Q4 2025 data covers ten weeks."

## 2. Semantics in code

- Give each chart a container with a heading (the title) and the summary as text.
- Each chart SVG has `role="img"` and an `aria-label` or a linked description that carries the summary.
- Hide purely decorative parts (gridlines, background shapes) from assistive technology.
- Keep text as text: titles, labels and annotations are real text elements, not paths or pixels.
- Interactive charts: each focusable mark or group has an accessible name that includes its value: "Q2 2025, 47 percent".
- A data table is a real table with header cells.

## 3. Keyboard

- Every interactive control (filter, toggle, zoom, series selector) works by keyboard with visible focus.
- Interactive marks: Tab reaches the chart; arrow keys move between points or series; Enter selects; Escape clears.
- Tooltips appear on focus as well as on hover, and stay until focus moves.
- Focus is never hidden behind a sticky header or the chart's own overlay.

## 4. Color and contrast

- Text, including tick labels and annotations, is 4.5:1 or more against its ground. Large text is 3:1 or more.
- Marks that carry meaning are 3:1 or more against the ground.
- No meaning by color alone: series also differ by label, position, line style, marker or pattern. Status also carries a word or icon.
- Check every theme. Run color-vision simulations and a grayscale pass (see `color.md`).
- Respect forced-colors and high-contrast modes in code: marks keep a visible outline.

## 5. Motion and time

- Honor the reduced-motion preference: no animated entry, no autoplay; show the final state.
- Animated or auto-updating charts that run more than about five seconds beside other content have pause and stop controls.
- Nothing flashes more than three times a second.

## 6. Zoom, reflow and size

- The chart stays readable at 200 percent browser zoom; text grows with the page, not stuck in a scaled SVG.
- At narrow widths the chart recomposes (see `composition-and-interaction.md`) rather than forcing horizontal page scroll; a wide table scrolls inside its own wrapper.
- Chart text stays at or above its floor: default 12 px on screen, larger in slides and print per the `typography` size table.

## 7. Images and documents

- A chart exported as an image carries alternative text with the summary. The table travels with it: in an appendix, a linked file or the body text.
- In a PDF, charts have alternative text and a reading order; tables are tagged where the tool allows.
- In a slide, the speaker notes or the slide text state the finding.

## 8. Chart accessibility review

Record each result in the review file.

- [ ] Summary present, with the finding and numbers.
- [ ] Data table reachable, with units and source.
- [ ] Text is text; chart element has an accessible name.
- [ ] Contrast: text 4.5:1, marks 3:1, in each theme.
- [ ] Meaning survives grayscale and color-vision simulation.
- [ ] Keyboard reaches every control and, for interactive charts, every data point.
- [ ] Tooltips on focus; values not hover-only.
- [ ] Reduced motion honored; no flashing.
- [ ] Readable at 200 percent zoom and at about 400 px wide.
- [ ] Screen reader pass: UNTESTED unless someone ran one. Say so.

## 9. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Label only | `aria-label="chart"` | A summary with the finding and numbers |
| Image of text | Titles and labels baked into a PNG | Real text in code; alt text and table for images |
| Hover-only | Values need a mouse | Focus states, printed values, table |
| Color legend | "Green = on track" | Add the word and an icon |
| Unstoppable motion | A live chart animates forever | Pause control; reduced-motion state |
