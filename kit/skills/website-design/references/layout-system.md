# Layout system

Read this file at step 6 of `website-design`. It sets five things in a fixed order: the measure, the container, the grid, the spacing rhythm and the breakpoints. It then shows the modern CSS that carries them.

Precedence: layout tokens in `DESIGN.md` and `design/tokens.json` win. This file fills the gaps. Every value in the build is a named token. When a value is missing, add the token through `design-system` and record it in `DESIGN.md`.

Evidence classes in this file. "Read" means a primary source was read during the research. "Memory" means the source was cited from memory. "Rule of thumb" has no primary source. All three are written as defaults.

## 1. Decide in this order

1. Measure: the width of a line of body text.
2. Container: the widest the page content grows.
3. Grid: the columns that content snaps to.
4. Rhythm: the spacing scale and the roles of its steps.
5. Breakpoints: the widths where the layout changes.

The order matters. The measure comes from reading. The container comes from the measure. The grid divides the container. A grid chosen first forces the text to fit the columns.

## 2. Measure and container

- Default: body measure is 45 to 75 characters. Set it in `ch` on the text block, not on the page.
- Default: body text is 16 px or more on the web (read: Vercel Web Interface Guidelines).
- A text page needs one narrow container. A marketing page needs a wide container and a narrow text container inside it.
- Default: the page container is between 1200 and 1440 px wide. This is a rule of thumb from common tool defaults.
- The page gutter is fluid. It never drops below the smallest touch-safe inset of the system.

```css
:root {
  --measure: 65ch;                                   /* token: text container */
  --container: 80rem;                                /* token: page container */
  --gutter: clamp(var(--space-4), 4vw, var(--space-8));
}
.wrap { inline-size: min(100% - 2 * var(--gutter), var(--container)); margin-inline: auto; }
.prose { max-inline-size: var(--measure); }
```

Use logical properties (`inline-size`, `margin-inline`, `padding-block`). They hold when the page runs right to left.

## 3. Grid

Choose the grid from the content, with these rules.

| Content | Grid | Why |
| --- | --- | --- |
| Mixed marketing sections | 12 columns at wide widths, 4 at narrow | Twelve divides into halves, thirds, quarters and uneven splits |
| A list of like items of unknown count | An intrinsic grid with `auto-fit` and `minmax` | The count and the width decide the columns. No breakpoint needed |
| One main thing and supporting things | An uneven split: 7 and 5, or 8 and 4 | Unequal content gets unequal space |
| Long reading text | One column at the measure, with an optional margin column | Reading needs no grid |
| A page shell with fixed regions | Named grid areas | The names document the layout |

Rules:

1. One alignment system for each view. Every edge sits on a grid line or on another edge (read: Vercel).
2. Do not default to equal halves and equal thirds. Use an equal split only for equal content.
3. Use `gap` for space between grid and flex children. Do not use margins on the children.
4. Use `subgrid` when the inner parts of sibling cards must line up: titles, bodies, actions.
5. Use flex for one-dimensional runs and grid for two dimensions. No script measures elements to place them.
6. Give a flex child that holds long text `min-inline-size: 0` and a wrap or truncation rule.

```css
.cards { display: grid; gap: var(--space-6);
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr)); }

/* Sibling cards share row tracks: title, body, action line up across the row. */
.cards > article { display: grid; grid-row: span 3; grid-template-rows: subgrid; gap: var(--space-3); }

.feature { display: grid; gap: var(--space-8); grid-template-columns: repeat(12, minmax(0, 1fr)); }
.feature > .main { grid-column: span 7; }
.feature > .side { grid-column: span 5; }
```

The `18rem` in the example stands for a token such as `--card-min`. Name it in the build.

## 4. Spacing rhythm

- Default: one spacing scale on a 4 px base: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 (memory: Refactoring UI). Use only these steps.
- Default: space between groups is at least twice the space inside a group. This is a rule of thumb.
- Put more space above a heading than below it. The heading belongs to what follows (read: Impeccable craft floor).
- Give spacing steps roles. A role name survives a change of value.

| Role token | Used for | Typical step |
| --- | --- | --- |
| `--space-inset` | Padding inside a control or a card | Small steps |
| `--space-stack` | Gap between items in one group | Small to middle steps |
| `--space-group` | Gap between groups in one section | Middle steps |
| `--space-section` | Gap between sections | Large steps, fluid |

Vary the section gap with the relation between sections. Two sections that continue one argument sit closer. A change of topic gets the full section gap. Equal space everywhere hides the structure.

```css
:root { --space-section: clamp(var(--space-12), 4rem + 6vw, var(--space-24)); }
section + section { margin-block-start: var(--space-section); }
```

## 5. Breakpoints

Breakpoints come from the content. Device names are not breakpoints.

Method:

1. Build the narrowest layout first, in one column.
2. Widen the viewport slowly.
3. Stop where the layout fails: a line passes the measure, a card grows too wide, a gap looks empty.
4. Add a layout change at that width. Name the breakpoint by what changes: `--bp-two-col`, not `--bp-tablet`.
5. Repeat to the widest width in the brief.

Rules:

1. Page-level layout changes use media queries. Component-level changes use container queries.
2. Write media query widths in `em` or `rem`. Then browser zoom triggers the narrow layout.
3. Default: three or four page breakpoints are enough. More points mean the layout is not fluid enough.
4. Between breakpoints the layout is fluid. It is never a fixed frame that jumps.
5. Test one width just below and one just above each breakpoint.

## 6. Container queries

A component adapts to the space it gets, not to the viewport. The same card then works in a sidebar and in a main column.

```css
.card-host { container: card / inline-size; }

.card { display: grid; gap: var(--space-4); }
@container card (min-width: 28rem) {
  .card { grid-template-columns: 2fr 3fr; align-items: center; }
}
/* Container query units size type against the container. Keep a rem part for zoom. */
.card h3 { font-size: clamp(var(--text-lg), 1rem + 2cqi, var(--text-2xl)); }
```

Rules:

1. Name the container. An unnamed query matches the nearest container, which changes when markup moves.
2. An element cannot query itself. The host wraps the component.
3. Use a container query when a component appears in two or more widths. Use a media query for the page shell.

## 7. Fluid values with clamp

`clamp(min, preferred, max)` gives a value that grows with the viewport between two limits.

Rule: the preferred part is a `rem` value plus a `vw` value. Never `vw` alone. A `vw`-only size does not respond to zoom.

How to compute it. Choose a size at the narrow viewport and a size at the wide viewport, all in `rem`.

```
slope     = (maxSize - minSize) / (maxViewport - minViewport)
intercept = minSize - slope * minViewport
preferred = intercept rem + (slope * 100) vw
```

Worked case: a display size of 2 rem at a 20 rem viewport and 4 rem at a 90 rem viewport.

```
slope     = (4 - 2) / (90 - 20) = 0.02857
intercept = 2 - 0.02857 * 20   = 1.4286
result    = clamp(2rem, 1.429rem + 2.857vw, 4rem)
```

Check it at both ends: 2.0 rem at 320 px wide, 4.0 rem at 1440 px wide.

Rules:

1. Use one viewport range for type and for space. Then they scale together.
2. Fluid type must still pass at 200 percent zoom. Test it; do not assume it.
3. Store each clamp as a token. Components use the token.

## 8. Other properties worth their place

| Property | Use it for | Note |
| --- | --- | --- |
| `aspect-ratio` | Reserve space for media before it loads | Prevents layout shift |
| `text-wrap: balance` | Headings and short lines | Read: Vercel. Not for long paragraphs |
| `min()`, `max()` | A width with a limit, without a media query | See the `.wrap` rule above |
| `dvh`, `svh` | Full-height areas on phones | The address bar changes the viewport height |
| `env(safe-area-inset-*)` | Padding near notches and home indicators | Read: Vercel |
| `scroll-margin-block-start` | Anchored headings under a sticky header | Otherwise the header covers the target |
| `@supports` | A fallback for a feature the audience may lack | Write the simple layout first |

Default: treat container queries, subgrid and clamp as present in current evergreen browsers. This kit did not test browser support. Confirm it against the browser list in the brief, and write the fallback when the list is older.

## 9. Radius, elevation and optical fixes

- Radii are tokens by role: control, card, sheet. One radius for every role is a tell.
- Nested radii are concentric. An inner radius is the outer radius minus the padding between them, and never larger than the outer one (read: Vercel).
- A shadow has an offset and a blur. Build elevation from two layers: one ambient, one direct (read: Vercel).
- Where geometry looks wrong, adjust by eye: an icon beside text, a play triangle in a circle. Record the offset as a token when it repeats.

## 10. Worked example

The invented repair shop again. Brand words: exact, patient, hands-on.

- Measure: 62 ch. The copy is explanatory, so reading comfort leads.
- Container: 76 rem. The bench photographs need width; the text does not.
- Grid: 12 columns. The opening view splits 5 and 7: the claim and booking action on 5, the bench photograph on 7. The model list is an intrinsic grid, because the count will change.
- Rhythm: the process steps continue one argument, so they sit at the group gap. The price table starts a new topic, so it gets the full section gap.
- Breakpoints, named by what changes: `--bp-split` where the opening view becomes two columns, `--bp-nav` where the navigation fits on one line.
- Rejected: three equal cards for "inspect, repair, test". The steps are a real sequence with unequal detail. They became a numbered list with one photograph for the step that needs it.

## 11. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Device breakpoints | `768` and `1024` appear with no reason from the content | Find the widths where this content breaks |
| Equal air | One gap value between everything | Give steps roles. Group by proximity |
| Viewport-only type | A font size in `vw` with no `rem` part | Use the clamp formula |
| Wide prose | Body lines pass 90 characters on a desktop | Put a measure on the text block |
| Grid first | Text widths that match columns, not reading | Set the measure first |
| Card soup | Every item boxed, boxes inside boxes | Remove the boxes. Use space and alignment |
| Magic numbers | Raw px values in component styles | Replace with tokens. Run the `design-system` audit |
| Jumping layout | A fixed frame that snaps between widths | Make it fluid between breakpoints |

## 12. Checks

Gates:

- Every layout value in the build is a named token.
- No sideways page scroll at the narrowest supported width.
- The layout holds with short, average and very long content, and with empty content.

Defaults:

- Default: measure 45 to 75 characters; body 16 px or more.
- Default: the narrowest supported width is 320 CSS px (memory: WCAG 2.2 reflow criterion).
- Default: spacing steps come from one scale of 12 values or fewer.
- Default: each fluid size keeps a `rem` part.
