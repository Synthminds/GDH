# Build routes, testing and performance

Read this file at steps 13 to 16 of `dashboard-design`. It covers the choice of build route, the coded route with a chart library, the sourced data page type and its rules, the mockup route, the build order, testing (glance test, user task, edge cases), performance and the handoff.

Evidence. The data page rules summarise the Claude Data type files and its tool card (read 2026-11-23, DOCUMENTED; no dashboard was created, so output quality is UNTESTED). The route choice table is GDH synthesis from the Claude design capabilities research. Real-data testing and the fidelity ladder come from the Design Engineering Handbook, chapter 2. Performance numbers are defaults.

## 1. Choose the route

| Route | Choose when | Not when |
| --- | --- | --- |
| Project code with a chart library (`dataviz` capability) | The dashboard ships inside a product; custom interaction; runs outside Claude; needs tests and deployment | A quick shared view of live connector data is enough |
| Sourced data page (`dataviz`, for example the Claude Data type) | Numbers are live or refreshed from a connector or file; each number must show its source; readers filter and comment; the owner works in Claude | It must ship inside a product, needs a chart library beyond the type's bundled one, or must run outside Claude |
| Static mockup (`canvas`, through `claude-design`) | Direction and layout need a reaction before any build; fixed numbers | The screen must work with live data |
| Coded prototype from a generator (for example [v0](../../../references/tools/v0.md)) | A clickable prototype in the target stack, fast | Production: review it against every gate first |

ASK: confirm the route when it is not obvious. Record the reason.

## 2. The coded route

1. Use the project's stack and its existing chart library. A new library goes through `find-assets` for its license.
2. Load the host chart skill when present; it governs chart mechanics.
3. Build components from the design system; tiles, tables and filters from the project's component library first. Component references from `ui-components` tools (for example [21st-dev](../../../references/tools/21st-dev.md)) are for structure and technique; re-implement, do not copy.
4. Wire tokens for every color, size, space, radius and duration. Data colors from `data-*` tokens.
5. Put filter state in the URL. Format numbers and dates by locale. Parse date-only strings as UTC.
6. Build every state from `filters-and-states.md` as a component state, with a story or fixture for each.
7. Use real data at production size in development, or a realistic fixture; mock data only in shared prototypes when the real data is private.
8. When the GCH kernel is loaded, GCH governs how the code is written, tested and reviewed.

## 3. The sourced data page route

Read the [claude-data](../../../references/tools/claude-data.md) card first. In brief:

1. Confirm the artifact tools are present. Get the current Data type link; create the page once with the type link and a title. Never create it twice.
2. Read the type's own `SKILL.md` and the reference files the job needs. The type's rules win over this file.
3. Datasets: a live connector query (runs for every reader with that reader's access), an uploaded file, or rows saved on the page.
4. Under the title, one sentence states what the numbers say now, filled from the data.
5. Each headline figure shows its signed change and comparison period; each card states its window. Color the change by good or bad, not by sign.
6. Define each metric in plain words where it first appears; put each caveat beside its figure.
7. Use only the type's guaranteed theme tokens and its chart color function. Never type a brand color into the page. A design system passes values only, when the view context holds one.
8. Charts use the type's bundled chart library only. Each chart SVG has `role="img"` and an accessible label. Print values worth reading; still give each chart a tooltip.
9. States: skeleton placeholders, a minimum height per chart box, and each chart says in place when it failed.
10. The page reads at full width and at about 400 px beside a chat.
11. After writing, read the page's run checks before hand-over. The author cannot see the page.
12. Hand over with: what the person can ask for next, that live queries run with each reader's access, and which rows are sample data.

GATE: a live query on a metered connector runs on every view by every reader. Tell the user and get a yes before wiring it. GATE: a share change, a deployed snapshot or a query on client data is exposure.

## 4. The mockup route

- Use it for the gray-box round and for direction when the look is open.
- Real metric names and realistic numbers from the inventory; never lorem ipsum.
- Show the states as separate artboards: loading, no data, stale, error.
- Record that the numbers are fixed; build the live version on another route.

## 5. Build order

1. Gray boxes with real names and numbers (approved in step 10).
2. Data wiring and the inventory's formulas, checked against the source.
3. States.
4. Charts, through `data-viz`.
5. Filters, drill-down and URL state.
6. Visual polish with tokens.
7. Accessibility pass, then performance pass.

## 6. Testing

Record every result in `design/reviews/<date>-dashboard.md`.

| Test | How | Pass |
| --- | --- | --- |
| Glance test (default, rule of thumb) | Show the screen for five seconds to a target user, then hide it | They name the top status and whether to act |
| User task | Give each user type its outcome task from the plan | They complete it without help; note time and errors |
| Real data | Load production-size data | No overflow, truncation or overlapping labels |
| Edge cases | Empty range, one huge outlier, the longest names, negative values, many categories, stale source, one failed source | Each shows its designed state |
| Values | Pick five numbers; recompute them from the source | All match |
| Themes and sizes | Each target size and theme, plus grayscale | Gates hold |
| Keyboard | Reach every filter, drill and table control | Visible focus throughout |

For code, review the rendered screen, not the source. For an artifact type, follow its own check rule.

## 7. Performance

- Measure with production-size data, on the target device.
- Default: first meaningful content within about two seconds on the target connection; interactions respond within about 100 ms, or show progress. Rules of thumb; when GCH is loaded its numbers govern.
- Paginate or virtualize tables over about fifty rows. Aggregate on the server, not in the browser.
- Load views independently, so one slow query does not block the screen.
- Cache stable reference data. Refresh only what changed.

## 8. Handoff

When another agent builds production, run `handoff-to-code` with:

- `dashboard-plan.md` (type, users, inventory, ranges, layout, states).
- The approved mockup or prototype, and the decision record.
- Data color tokens and chart style rules from `DESIGN.md`.
- The test list from section 6 with results so far.

## 9. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Artifact for a product | A data page asked to ship inside an app | Code route; the page is a prototype at most |
| Polish before data | Beautiful screen, numbers do not match the source | Wire and verify data before polish |
| Typed brand colors | Colors that do not follow the theme | Theme tokens only |
| Untested states | The first outage shows a blank screen | Fixtures for every state |
| One slow query blocks all | The screen waits for the slowest view | Independent loading per view |
