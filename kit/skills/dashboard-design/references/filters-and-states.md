# Filters, drill-down, data time and states

Read this file at steps 11 and 12 of `dashboard-design`. It covers filters, the time range control, drill-down, URL state, the data-time stamp, the seven states and their content, refresh behaviour, and failure patterns.

Evidence. Visible filter state in the URL, skeletons that match the final layout, tables virtualized past a size, and status not by color alone come from the Vercel Web Interface Guidelines (read 2026-11-23). States with skeleton placeholders, minimum chart heights and in-place failure messages come from the Claude Data type design defaults (read 2026-11-23). The failure-message content (what happened, what is safe, what is being done, when the next update comes) comes from "Designing for Emotion", chapter 6. Overview, then filter, then details is Shneiderman (from memory). Numbers are defaults.

## 1. Filters

Rules:

- Show every active filter on the screen, near the title, as removable chips or a summary line: "Region: EMEA; Plan: Pro; 1,204 of 9,880 accounts".
- Keep filter state in the URL, so a shared link opens the same view and the back button restores it.
- Give filters real defaults that answer the main question. An unfiltered "all time, all regions" view is rarely the right default.
- Put filters that apply to the whole screen in one place, above the content. A filter that applies to one view sits on that view and says so.
- Show counts beside filter options when they help ("Pro (412)"), and disable options that return nothing.
- "Reset filters" returns to the default view, not to an empty one.
- Filters work by keyboard; each has a visible label, not only a placeholder.

Filter types by data:

| Data | Control |
| --- | --- |
| Time range | Preset ranges plus a custom picker; the active range always visible |
| A few categories (under about seven) | Segmented control or chips |
| Many categories | Searchable multi-select |
| Numeric range | Two inputs or a range slider with typed values |
| Entity (one customer, one store) | Search with suggestions |

## 2. The time range control

- Offer presets that match the type: "Today", "Last 7 days", "Last 28 days", "Quarter to date", "Last 12 months".
- Show the active range in words and dates: "Last 28 days (27 Oct to 23 Nov 2026)".
- Show the comparison period beside it: "compared with the previous 28 days".
- Use the same range across the screen unless a view says otherwise.
- Label a partial period "to date".

## 3. Drill-down

Order: overview first, then filter and zoom, then details on demand.

| Pattern | Use when | Rules |
| --- | --- | --- |
| Click a tile to its detail view | A headline needs its breakdown | The detail view keeps the filters and range; a breadcrumb leads back |
| Click a bar or row to filter the screen | Cross-filtering helps compare | The filter appears as a chip; clicking again clears it |
| Expand a row | Detail fits inline | Keyboard operable; one level deep |
| Open a side panel | Detail of one item without losing context | The panel has a close control and keeps focus inside |
| Link to the source system | The action happens elsewhere | Open in a new tab only when stated; the link names the destination |

Rules:

- Each drill keeps the user oriented: title, breadcrumb, active filters.
- The detail view answers "why", with the breakdown that explains the headline.
- Drill targets look interactive (cursor, focus style, affordance), and hover is never the only way in.

## 4. Data time

Every screen shows when its data is from.

- Show "Updated <time> <time zone>" near the title. Use the reader's time zone, or state the zone.
- Show the refresh rate where it matters: "Updates every 15 minutes".
- Mark stale data: past its expected refresh, the stamp turns to a warning style with a word ("Stale: last update 3 hours ago").
- When sources refresh at different times, show the data time per view.
- A report states its period and its extraction date.

## 5. The seven states

Design each state for each view. Record them in `dashboard-plan.md`.

| State | When | Shows | Must not |
| --- | --- | --- | --- |
| Loading | Data requested | A skeleton of the final layout and size | Shift the layout when data arrives |
| No data | The source returned nothing for this range or filter | A sentence with the reason and the range: "No orders between 1 and 7 Nov." plus a next step | Show empty axes with no message |
| Filtered to nothing | Filters exclude every row | "No accounts match these filters." with a reset control | Look like an error |
| Stale | Data older than its expected refresh | The last data, the age, a warning word and style | Present old numbers as current |
| Partial | Some sources failed or some periods are missing | The available data plus a note: what is missing and why | Plot missing periods as zero |
| Error | A view failed to load | In place, in the view's box: what failed, what is safe, what to try, and when it retries | Break the whole screen for one failed view |
| No permission | The reader lacks access to some data | Which data is hidden and how to request access | Reveal hidden values in totals |

Rules for error and outage messages:

- State what happened, what is safe, what is being done, and when the next update comes.
- No jokes and no mascots in error states.
- Keep the message in place, so the rest of the screen stays useful.

Rules for partial and missing data:

- Keep a missing period's slot on the time axis, in neutral gray, with a note.
- Totals that exclude hidden or failed data say so: "Total excludes 2 regions you cannot view."

## 6. Refresh behaviour

- Update values in place. Do not reflow the layout or animate tiles on each refresh.
- Default: briefly mark changed values (a subtle background fade), inside a reduced-motion check. Under reduced motion, change the value only.
- Do not move the user's scroll, selection or open panels on refresh.
- A live screen that updates more often than people read it wastes attention. Match refresh to the decision cadence.
- A screen left open on a wall display shows the data time large enough to read across the room.

## 7. Empty and first-run screens

- A new dashboard with no history explains what will appear and when: "Charts fill in after the first full day of data."
- Show the inventory's definitions on first run, or link to them.
- Offer a sample data toggle only when it is clearly labelled as sample.

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Hidden filter | Numbers differ between two people, nobody knows why | Active filters always visible; state in the URL |
| Silent staleness | Yesterday's numbers look current | Data time, refresh rate, stale marking |
| Blank failure | One failed query leaves an empty box | In-place error with what to try |
| Gaps as zeros | Missing days plotted as a crash | Gray slot, note |
| Layout jump | Charts pop in and push content | Skeletons of final size; minimum heights |
| Refresh disco | Tiles flash on every update | In-place updates; subtle, reduced-motion aware |
| Leaky totals | Totals include data the reader may not see | Exclude and say so |
