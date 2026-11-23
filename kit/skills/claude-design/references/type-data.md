# Craft of the Data type

Read this file at step 12 of `claude-design` when the type is Data. It restates the data page type's rules on provenance, page shapes, states, looks and the played data short, in my own words. Chart method comes from `data-viz`; dashboard layout comes from `dashboard-design`.

Evidence. Rules come from the Data type's rule file and its design defaults, design system, looks, visual short and exporting references, read 2026-11-23: DOCUMENTED. No data page was built for this kit: UNTESTED.

Terms. A dataset is one source of rows. A mark is the smallest element that shows a value. A look is the set of theme values the page uses.

## 1. Choose the Data type when

| Condition | Data type | Something else |
| --- | --- | --- |
| Numbers are live or refreshed | Yes | |
| Each number must show where it came from | Yes | |
| Readers filter and comment | Yes | |
| Fixed numbers in a designed infographic | | Canvas with `infographic` |
| A dashboard inside a product with custom interaction | | Code with a chart library |
| It must run outside Claude | | Code; a static snapshot loses data |

## 2. Sources and provenance

1. Each dataset has one source kind. It is a live connector call, an uploaded file, or rows people save on the page. A live call runs for each reader with that reader's access.
2. Every mark carries its source and field. A derived number is a declared calculation, never a typed value.
3. Every number in a caption is filled from data. A rounded spoken figure comes from a calculation.
4. Label sample data as sample. The hand-over says which rows are sample.
5. Live queries run with each reader's access. Two readers can see different numbers. Say so in the hand-over.

Failure pattern: "typed number". Sign: a figure appears in text with no source. Counter-move: bind it to a field or a calculation, or mark it `[SOURCE NEEDED]`.

## 3. Defaults the type sets for every page

- Under the title, one sentence says what the numbers say now, filled from the data.
- A headline figure shows its signed change and its comparison period. Color the change by whether it is good, not by its sign.
- A card states its window, for example "Last 28 days".
- Define a metric in plain words where it first appears. Put a caveat beside the figure it changes.
- Show a lift with its interval. Draw lines point to point; a smoothed curve implies values the data lacks.
- Measure chart margins from the labels as drawn. Stop labels colliding.
- Print values worth reading. A tooltip does not reach a phone or a screenshot. Still give every plotted chart a tooltip.
- A wide table scrolls inside its own wrapper.
- Each chart has an image role and a label that says what it shows.
- Format numbers and dates. Parse date-only strings as UTC.
- The page reads at full width and at a narrow width beside a chat. No fixed widths.

## 4. Tokens and looks

1. Use only the type's guaranteed tokens for color, panels, gaps and radius. Never type a brand color into the page; a typed color cannot be themed later.
2. A design system is applied only when the view context names one. Then the type takes values only: colors, sizes, corners, font names.
3. Fill both light and dark. Derive a missing theme from the system's own neutrals.
4. Put the brand color first in the chart colors. Pick later chart colors that differ clearly.
5. The page replaces unreadable colors by itself. A system's font files never load here.
6. The type offers a few ready looks. Use one only when no system governs.

## 5. Page shapes

| Shape | Use when | Structure |
| --- | --- | --- |
| Visual analysis | One finding matters | Top to bottom, one argument |
| Scroll story | A finding unfolds in chapters | Chapters beside one sticky chart |
| Letter | The numbers sit inside prose | Numbers inside sentences, no tiles |
| Tool | People track, check or calculate | Tracker, checklist or calculator |

Pick the shape from the brief's primary job. A tile grid is not a default; it is a shape the job must earn.

## 6. States

- Use the type's skeleton placeholders while data loads.
- Give each chart box a minimum height, so the page does not jump.
- Each chart says in place when its data failed. The rest of the page still works.
- Put motion inside the reduced-motion preference check. Play entry motion once.
- Write a print layout for any page with tabs or steps. Only the page-break-before rule works in print.

## 7. The played data short

A short, narrated piece that plays only on Play.

1. One finding, a few chapters, one stage. Each chapter is a drawing that builds while a caption says what it shows.
2. The title chapter states the subject, the period and the run time.
3. Each chapter is a function of time, so it can be held, replayed or jumped.
4. Motion follows the caption's words.
5. Drawing choices: a dot grid for a share; one counted number for a total; horizontal bars from zero for a comparison; two bars and a bracket for a gap.
6. Marks start muted with one accent on the subject. To focus, fade the rest; never add a color.
7. Marks arrive fast with ease-out. No camera moves, no 3D, no bounce.

## 8. Export and hand-over

| Route | Result | Note |
| --- | --- | --- |
| PDF from the share menu | The browser print dialog | Only page-break-before works |
| CSV | A reader downloads a source's rows | Per source |
| A hosting import (example card: [vercel](../../../references/tools/vercel.md)) | A styled static snapshot | No live data, no queries, no filters. GATE: exposure |
| Another BI product | Rebuild there with its connector | Say first what carries over and what is lost |

The hand-over tells the reader three things: what they can ask for next, that live queries run with each reader's access, and which rows are sample.

## 9. Check before the hand-over

The type requires you to read its run results after writing. Read them. Then confirm:

- Every mark has a source and field.
- The summary sentence is filled from data.
- Each chart has a label, a tooltip and a failure state.
- The page reads at a narrow width.
- Sample rows are named.

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Brand color typed in | A hex value in the page | Use the look tokens |
| Smoothed lines | Curves through sparse points | Point-to-point lines |
| Tooltip-only values | Key numbers appear only on hover | Print them |
| Tile wall | Twelve equal cards | Pick a page shape; rank the metrics |
| Silent failure | A blank chart box | An in-place failure message |
