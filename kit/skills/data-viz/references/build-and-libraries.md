# Build routes, library choice, real data and the chart style

Read this file at steps 12 to 17 of `data-viz`. It covers the host chart skill, build routes, library choice by need, testing with real data, chart states, the chart style written into `DESIGN.md`, the final review and a worked example.

Evidence. Library licenses come from `kit/catalogs/assets.json` (read 2026-11-23). Library strengths are summary notes from that catalog; confirm versions and APIs in each library's own documentation. The real-data and edge-case rules come from the Design Engineering Handbook, chapter 2. The data page rules come from the Claude Data card. Route choices are GDH defaults.

## 1. The host chart skill

- When the session lists a host `dataviz` skill, load it before the first line of chart code or the first chart color.
- Treat it as the authority on chart mechanics: mark specifications, palette validation, interaction rules, stat tiles.
- GDH keeps: the finding, the choice table, honesty checks, tokens and precedence, the decision record.
- Colors: the design system supplies hues; the host skill's validator checks them. When the validator rejects a brand color, report it as an accessibility finding and propose the nearest passing token. Never drop the brand color in silence.
- Where the host skill is stricter than GDH, follow it. Where they disagree on something else, ask the user and record the answer.
- Its content was not read when this kit was written. Note its version in the closing report.

## 2. Build routes

| Route | Choose when | Rules |
| --- | --- | --- |
| Project code with a chart library | The chart ships inside a product or site | Tokens only; the project's existing library first |
| Sourced data page (`dataviz`, for example the Claude Data type) | Numbers are live or refreshed, every number needs provenance, readers filter and comment | Follow the type's rules: its bundled chart library only, its theme tokens, read its run checks before hand-over. See [claude-data](../../../references/tools/claude-data.md) |
| Static chart on a designed page (`canvas`, through `claude-design`) | A fixed chart in a poster, report page or infographic | One SVG for the chart plot; labels as real text where the format allows |
| Inline SVG by hand | One or two simple charts, no library wanted | Compute scales in code, not by eye |
| Map tool (`maps`) | The finding is about place | Rates, not raw counts; see [felt-maps](../../../references/tools/felt-maps.md) |
| Diagram tool (`diagram`) | A flow of a few stages drawn by hand | Not for quantities |
| Generated UI (`dataviz` in a code generator, for example [v0](../../../references/tools/v0.md)) | A quick coded prototype of a chart screen | Review against every gate; replace defaults with tokens |

## 3. Library choice by need

Every library is an outside asset: `find-assets` reads its license and writes the manifest record before the first install. Use the project's existing library when it can do the job.

| Need | Capability to look for | Example libraries (catalog id) |
| --- | --- | --- |
| Full control, custom forms, editorial graphics | Low-level scales, shapes and axes | `d3`, `visx` (React) |
| Fast, concise editorial and exploratory charts | Grammar of graphics with good defaults | `observable-plot`, `vega-lite` |
| Agent-friendly declarative specs | Charts as JSON | `vega-lite` |
| React product charts that follow component tokens | Composable chart components | `recharts`, `shadcn-charts`, `nivo`, `unovis` |
| Dashboards in React, quickly | Prebuilt dashboard parts | `tremor` (restyle; its default look is recognisable) |
| Large datasets, many chart types, canvas rendering | Canvas or WebGL rendering | `echarts`, `plotly` |
| Dense time series, very fast | Minimal canvas time-series renderer | `uplot` |
| Financial price charts | Candles, crosshair, time scale | `lightweight-charts` (read its NOTICE before shipping) |
| Simple canvas charts, few types | Small API | `chartjs` |
| Millions of points on a map or plane | GPU layers | `deckgl` |
| Vector maps | Map rendering with a tile source | `maplibre` (tile source has its own terms) |
| Scientific and 3D charts | Broad scientific coverage | `plotly` (large bundle) |

Rules:

- Choose by the need in the first column, then check bundle size, accessibility support (keyboard, SVG text) and theming by tokens.
- Replace every default color, font and gridline with tokens. Library defaults are a tell.
- Pin the version in the manifest record.

## 4. Real data before polish

1. Render the first sketch with the real data, not an invented "nice" series.
2. Render these cases and keep a screenshot of each in `design/reviews/`:
   - Typical: the current real data.
   - Flat: a low-variance series. Does the chart still say something, or does the finding need a new form?
   - Empty: no rows. The chart shows an empty state with a reason, not blank axes.
   - Extreme: one outlier ten times the rest; the longest category name; negative values if possible.
   - Many: the largest number of categories or points the product allows.
3. Fix what breaks before any styling work.
4. Use mock data in shared prototypes when the real data is private; swap in real data for the approved audience.

## 5. Chart states

| State | Shows |
| --- | --- |
| Loading | A placeholder of the chart's final size, so nothing shifts |
| Empty | A sentence: "No orders in this period." plus the period and filter |
| Error | In place, in the chart's box: what failed and what to try |
| Partial | The available data, with a note on what is missing |
| Stale | The data time, marked as stale past its expected refresh |

## 6. The chart style

When the job is a chart style for a product or report, write these rules into `DESIGN.md` under "Data visualization":

```
Data colors: tokens data-cat-*, data-seq-*, data-div-*, data-highlight, data-context
Type: chart title <style>, labels <style>, numbers tabular, minimum <size>
Marks: line width <...>, point size <...>, bar spacing <...>, corner radius on bars <none | token>
Axes and grid: <which axes, gridline token, tick count>
Labels: direct by default; legend position when needed
Annotation: <style for event lines, callouts, bands>
Number formats: <locale, abbreviations, significant digits, sign style>
Text stack: title as finding, subtitle, notes, source
States: loading, empty, error, partial, stale
Accessibility: summary and table for every chart; keyboard pattern for interactive charts
Library: <name, version>; host chart skill: <present | absent>
```

Prove the style on three real charts of different forms before you write it down.

## 7. Final review (steps 14 to 17)

1. Honesty checks from `encoding-and-scales.md`, section 9.
2. Accessibility review from `accessibility.md`, section 8.
3. Render review at every target width and theme, plus grayscale. For code, review the rendered result, not the source.
4. Cold read: show the chart to someone who has not seen the data for five seconds. They state the finding, or the title and highlight need work. Default: a rule of thumb, not a measured threshold.
5. For a set or a style: `design-critique`, then `accessibility-gate`.
6. Log the round in `design/decisions.md`: shown, feedback, keep, change, remove, decision, rejected options.

## 8. Worked example

Request: "Show how our delivery times changed after we opened the second warehouse."

1. Finding draft: "Median delivery time fell from 3.1 to 1.9 days after the second warehouse opened in June." Relationship: change over time, plus distribution.
2. Data check: 48,210 orders, January to December; 212 orders missing a delivery date (excluded and noted); a long tail to 14 days.
3. Form: line of the weekly median with a shaded band from the 25th to 75th percentile; an event line in June. Considered and rejected: columns of monthly averages (hide the tail and the turning point).
4. Scales: linear, y from zero (days), weeks on x with gaps kept for two missing weeks.
5. Color: median line in `data-highlight`, band in a light tint, event line in `data-target`.
6. Text: title as the finding; subtitle "Median and middle half of delivery times, days, weekly, 2025"; annotation "Second warehouse opens"; source "Order system export, 2026-01-05".
7. Small screen: fewer ticks (quarter labels), annotation as a numbered marker.
8. Alternatives: summary with the two medians and the band width; a weekly table.
9. Library: the project already uses `recharts`; used with tokens.
10. Cases rendered: typical, empty (a new region with no orders), extreme (one week with a 14-day outlier).
11. Honesty: baseline zero; band labelled; no smoothing; values checked against the export.

## 9. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Library look shipped | Default palette, gridlines, fonts | Tokens for every style value |
| Library by fashion | A heavy chart suite for one bar chart | Choose by need; prefer the existing library |
| Nice-data mockup | Perfect curve in the design, flat in production | Real data first; edge cases rendered |
| Blank empty state | Axes with no data and no message | Empty state with reason |
| Host skill ignored | Chart colors fail its validator | Load it first; validate the brand colors |
