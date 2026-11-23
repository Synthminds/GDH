# Rendered verification gate

Read this file at step 18 of `website-design`. The gate: a code deliverable is reviewed as rendered, at each breakpoint and in each theme. Reading the source does not pass the gate.

Scope. This gate applies to code. A canvas mockup follows its artifact type's own check rule instead. A builder project is checked with the builder's own screenshot tool where it has one, and the result carries that label.

## 1. Build the view matrix

List the views before you capture. A view is one page, at one width, in one theme, in one state.

```
pages x widths x themes  = base views
plus: key states for each page (menu open, form error, empty list, loading)
plus: stress views (long content, 200 percent zoom, reduced motion)
```

Widths:

- Use the breakpoints of the design system first.
- Add the narrowest supported width, and one width just below and just above each breakpoint.
- Default, when the system is silent: 320, 375, 768, 1024, 1440 and 1920 px. This list is a rule of thumb.
- Default: one view at 50 percent browser zoom stands in for an ultra-wide screen (read: Vercel).

Themes: every theme id in `design/tokens.json`. A site with one theme has one column.

Keep the matrix honest. When it is too large to capture in full, capture every page at the narrowest and one wide width in each theme. Capture the first page at every width. Write what was left out.

## 2. Capture

1. Pick a tool with the `capture` capability from the catalog. Confirm that it is present. Read its card.
2. With GCH installed, use `gch:browser-lane`.
3. Serve the build locally and capture from the local address. A local capture exposes nothing.
4. GATE: a capture service that needs a public address is exposure. Ask first.
5. Capture the full page, not only the first view.
6. Name each file: `<page>-<width>-<theme>-<state>.png`.
7. Save captures in `design/reviews/<date>-render/`.
8. With no capture tool, ask the user for screenshots at the listed widths. Label the gate UNTESTED until they arrive.

## 3. Look at every capture

Open each file. Do not pass a view you did not look at. Check in this order.

| Look for | Pass | Common cause of a fail |
| --- | --- | --- |
| Overflow | No sideways scroll. Nothing is cut off | A fixed width, a long word, an unsized image |
| First view | The claim, the action and the real thing are visible | An oversized header or image pushes the action down |
| Measure | Body lines stay near 45 to 75 characters | No measure on the text block |
| Headings | Balanced lines, no single-word last line, no overlap with media | Missing balance rule, tight line height |
| Alignment | Edges line up on one system | Mixed paddings, a centered block in a left-aligned page |
| Rhythm | Groups are visible. Sections are separable | One gap value everywhere |
| Images | The subject is in frame. Nothing is stretched | No narrow crop, wrong fit rule |
| Targets | Controls are large enough for the input at that width | Icon buttons with no padding |
| Fixed elements | A sticky header or bar covers no content and no focus | Missing scroll margin |
| Theme | Text, borders, icons and images all work on this ground | A hard-coded color, a light screenshot on a dark page |
| Leftovers | No placeholder without its label, no sample text, no broken image | An unfinished section |

Then compare each capture with the section plan. A section that drifted from its plan line is a finding.

## 4. Checks that a still image cannot show

Run each one in a real browser session, or label it UNTESTED.

| Check | How | Pass |
| --- | --- | --- |
| Keyboard pass | Tab from the address bar to the footer and back | Every control is reached, in a sensible order, with a visible focus ring. Nothing traps focus |
| Skip link | Press Tab once on a fresh page | A link to the main content appears and works |
| Menu and dialogs | Open by keyboard. Press Escape | Focus moves in. Escape closes. Focus returns to the trigger |
| Form error path | Submit the form empty, then with one bad value | The error names the field and the fix. Input is kept. Focus moves to the first problem |
| Reduced motion | Turn on the reduced-motion setting and reload | Movement is gone. Content is all present |
| Zoom | Set browser zoom to 200 percent | No content is lost. No overlap |
| Text spacing | Apply wider line, letter and word spacing | Nothing clips |
| Navigation | Open a link in a new tab. Use Back after a scroll | Both work. Scroll position returns |
| Script off | Disable script and reload | Content and navigation are readable |
| Hover | Use a touch profile | Nothing needs hover |

The full accessibility checks belong to `accessibility-gate`. This table is the minimum for the render gate.

## 5. Fix in batches

1. List every finding from parts 3 and 4, with its file name.
2. Group findings by cause. One missing token often explains five views.
3. Fix one cause at a time.
4. Capture again: the changed views and their neighbors at the next width.
5. Compare before and after. Check that a fix at one width broke nothing at another.
6. Stop when no finding remains, or when each remaining finding has a recorded decision.

Do not tune one view at a time by eye. Fix the system, then look again.

## 6. The evidence log

Write `design/reviews/<date>-render.md`.

```
# Render check: <site>, <date>
Build: <commit, branch or folder>; served from: <local address | preview>
Tool: <capture tool, or "screenshots from the user">
Matrix: <pages> x <widths> x <themes>; captured <n> of <n>; left out: <list and reason>

| View | Width | Theme | State | Result | Finding | File |
| --- | --- | --- | --- | --- | --- | --- |
| home | 320 | light | default | pass | | home-320-light-default.png |
| home | 320 | dark | menu open | fail | focus ring invisible on the menu ground | home-320-dark-menu.png |

Interaction checks: keyboard <pass | fail | UNTESTED>; reduced motion <...>; zoom 200 <...>; form error path <...>; script off <...>
Fixed in this pass: <list>
Open, with decisions: <list>
Evidence: VERIFIED <views captured and looked at>; UNTESTED <real devices, screen reader, field performance>
```

## 7. What this gate does not prove

Say these limits in the report. Do not let a pass read as more than it is.

- A desktop browser at a phone width is not a phone. Touch, fonts and browser chrome differ.
- A capture shows one moment. It does not show a transition, a flash or a slow load.
- It does not prove screen reader behavior.
- It does not prove field performance.
- It does not prove that the content is true. The placeholder list and the source list do that.
- A pass at the listed widths does not prove the widths between them. The layout must be fluid by construction.

## 8. Worked example

The invented repair shop: four pages, two themes, breakpoints at 36 rem and 60 rem.

- Widths chosen: 320, 560 and 592 (around the first breakpoint), 944 and 976 (around the second), 1440.
- Base views: 4 pages x 6 widths x 2 themes = 48. States added: menu open, booking form error, model list empty. Stress views: longest model name, 200 percent zoom, reduced motion.
- Finding 1, in 9 views: the model name "Voigtlander Bessa" with its long suffix overflows at 320. Cause: one missing wrap rule on a flex child. One fix, 9 views pass.
- Finding 2, dark theme only: the price table rules vanish. Cause: a border color written as a literal, not a token. The fix is a token; the `design-system` audit then finds two more literals.
- Finding 3, keyboard pass: focus is hidden behind the sticky header after a jump to an anchor. Fix: a scroll margin token.
- Left out: 1920. Reason: the container stops at 76 rem; the 50 percent zoom view covers the wide case.
- Labels: VERIFIED for 48 base views and the three interaction checks. UNTESTED for a real phone and for a screen reader.

## 9. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Source pass | "Looks right in the code" with no capture | Render it |
| One width | Only a desktop capture exists | Build the matrix |
| One theme | Dark mode was never opened | Every theme is a column |
| Unseen captures | Files exist; nobody opened them | Look at each. Note what you saw first |
| Tweak loop | One pixel at a time, one view at a time | Batch by cause |
| Clean sample | Only the tidy copy was rendered | Add the stress views |
| Pass inflation | A lab capture reported as "works on mobile" | Report the limits in part 7 |

## 10. Checks

Gates:

- Every page was captured at the narrowest supported width and at one wide width, in every theme.
- Every capture was looked at. Each finding has a file name.
- The keyboard pass and the reduced-motion check ran, or they are labelled UNTESTED with a reason.
- The evidence log exists and names what was left out.

Defaults:

- Default: the width list in part 1.
- Default: one view at 50 percent zoom for the ultra-wide case.
- Default: two capture passes. A third pass with new findings means a cause was missed.
