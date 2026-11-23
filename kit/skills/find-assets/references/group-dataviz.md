# Group: dataviz

Catalog group `dataviz`: chart, map and graph libraries, plus chart-choice guidance. Read this file at step 6 of `find-assets` when the need is a library for charts, maps, networks or diagrams.

How to read this file. An id is a catalog id. An id marked `*` has `verifiedOn` null: read its license before use. Every pick is a default from desk research. Evidence: UNTESTED in a build. License notes are DOCUMENTED on the catalog date, except where marked `*`.

Which chart answers the question belongs to `data-viz`. Network layout belongs to `network-graph`. Screen layout belongs to `dashboard-design`. This file covers which library to pull and what its license asks.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| Full control over every mark | `d3`, `visx` | Low-level building blocks; `visx` wraps them for React | You build each chart yourself |
| Fast editorial and exploratory charts | `observable-plot` | A short grammar for most chart types | Less interaction by default |
| Composable charts in React | `recharts`, `shadcn-charts`, `nivo` | Familiar React patterns; `shadcn-charts` matches copy-in tokens | `recharts` draws SVG only and slows on large data. `nivo` has larger bundles. |
| Charts as a JSON spec | `vega-lite` | A declarative spec an agent can write and check | Custom styling takes effort |
| Large data on canvas | `echarts`, `uplot` | `echarts` covers many types. `uplot` is built for dense time series. | `echarts` needs its default style replaced. `uplot` has a small API. |
| A simple chart with little setup | `chartjs` | Easy to start | Few chart types |
| Scientific and 3D charts | `plotly` | Wide scientific coverage | A very large bundle |
| Financial charts | `lightweight-charts` | Fast price charts | Read its NOTICE file for a credit duty before it ships |
| Quick dashboard parts | `tremor`, `unovis`, `bklit-ui` | Ready dashboard components | `tremor` has a recognisable default look. `bklit-ui` is a new project. |
| Maps | `maplibre`, `deckgl` | An open vector map renderer; large-scale geo layers | A map needs a tile source with its own terms and credit. `deckgl` is heavy on the GPU. |
| Networks | `sigma`, `cytoscape`, `react-force-graph`, `g6` | WebGL rendering for large graphs; analysis and layouts | Layout is separate in `sigma`. `react-force-graph` gives little layout control. |
| Diagrams from text | `mermaid` | A diagram from a text description | Limited visual control |

Guidance, reference only. Study it and write your own words:

| Need | Catalog ids | Limit |
| --- | --- | --- |
| From data type to chart type | `from-data-to-viz` | A credit is recommended when you cite it. Reuse terms for the site text were not checked. |
| Chart types by data relationship | `ft-visual-vocabulary` | The content is all rights reserved. Do not republish the poster or its text. |
| A wide chart vocabulary; practical advice | `data-viz-project*`, `datawrapper-academy*` | Terms unread. Reference only. |

## Decision rules

1. `data-viz` chooses the chart first. Pick the library after, for that chart and that data size.
2. Use the library the project already ships when it can draw the chart.
3. Default: one chart library for each product. A second one needs a reason in `design/decisions.md`.
4. Match the renderer to the data. SVG suits small data and fine styling. Canvas or WebGL suits large data.
5. The catalog gives no point count for that switch. Measure on the target device with the real data.
6. Replace the library's default style. Axis, grid, type and color come from project tokens.
7. A library's default palette is a tell. Use the data color tokens from the design system.
8. Every chart needs a text alternative and must not carry meaning by color alone. `accessibility-gate` checks it.
9. Load only the chart packages the product uses.
10. Record each library as a package at one exact version.
11. A map tile service is a remote load by design. Write it as a hotlink exception with the provider's terms as the reason.
12. Show the tile provider's credit where its terms ask for it.

## License traps

- Permissive libraries dominate this group. The traps are at the edges.
- A NOTICE file can carry a credit duty (`lightweight-charts`).
- Map data and map tiles have their own licenses and credit lines, apart from the renderer.
- Chart guidance is someone's writing. Learn the method. Do not copy the taxonomy text or the poster.
- Example galleries on library sites are documentation. Their code has the documentation's license, and their data is often real.

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Library look | Default palette, default grid, default tooltip | Restyle from tokens |
| Wrong renderer | A chart that stutters with real data | Measure. Move to canvas or reduce the data. |
| Chart by library | The chart type was picked because the library offers it | Go back to `data-viz` |
| Two libraries | Two axis styles and two tooltip styles in one screen | One library |
| Uncredited map | A map with no provider credit | Add it where the terms say |
| Sample data shipped | A demo data set left in the product | Use real data or a labelled placeholder |

## Worked choice

The outcomes below are illustrative. They show the reasoning, not verified facts about a source.

Need: a latency chart for an operations screen: one point each second for a day, several series. Ships in a client product that already uses a React chart library.

- Tier 1: the installed library draws SVG. A day of one-second points is far more marks than it draws smoothly, per its catalog note.
- Measure first: a quick test with the real data on the target laptop confirms the stutter. Evidence: VERIFIED by that test.
- Catalog: `A search <catalog> --group dataviz --query "dense time series" --commercial --verified`. First result: a small canvas library built for this case.
- License: permissive. Verdict `clear`.
- Reason for a second library, recorded in `design/decisions.md`: the installed one cannot draw this data size.
- Change planned: axis, grid and series colors from tokens; a text summary beside the chart.
