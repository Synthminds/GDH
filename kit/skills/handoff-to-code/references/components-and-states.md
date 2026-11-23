# Component inventory and states

Read this file at step 8 of `handoff-to-code`. It covers the component inventory with props, variants and states, the state matrix for screens, the edge-case list, and the naming rule that keeps design and code in one vocabulary.

Evidence. The state list draws on the `app-design` states reference and the GCH screen-state rule, both read through the GDH research: DOCUMENTED as method. The rule that names must match between design and code, and the "new pattern or reuse" test, come from the Design Engineering Handbook, chapter 3: DOCUMENTED. The table shapes are this kit's own.

Terms. A component is a reusable part with props. A prop is an input the consumer sets. A variant is a named visual form of one component. A state is a condition the component or screen can be in at run time.

## 1. Reuse before new

Before a component enters the inventory as new:

1. Search the project's component library and the design system's components.
2. Apply the reuse test. A component is new only when no existing one takes the case with a new prop or variant.
3. Record the result in the inventory: `reuse`, `extend` (new prop or variant) or `new`, with the reason.

A design that ignores the existing library will be rebuilt or dropped.

## 2. One vocabulary

1. A component has one name in the design files, the package and the code.
2. When the code already has a name, the design takes it.
3. Name props by role, not look: `tone="danger"`, not `color="red"`.
4. Sample five names in the reference files and the code before the handoff. Each must match.

## 3. The inventory table

Write one row per component in section 4.1 of `design/handoff.md`.

| Component | Status | Props | Variants | States | Tokens | Reference file | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `BookingCard` | new | `booking` (object, required), `compact` (bool, default false), `onOpen` (handler) | default, compact | default, hover, focus, pressed, selected, overlapping, cancelled, loading | `surface`, `text`, `accent`, `radius.card`, `space.3` | `design/directions/2-tide/booking-card.html` | Long titles wrap to two lines, then truncate |
| `Button` | reuse | from the library | primary, secondary, ghost | default, hover, focus, pressed, disabled, busy | from the library | library | Busy state replaces the label with a spinner and keeps the width |

Rules for props:

1. Give each prop a type, whether it is required, and its default.
2. Say what the consumer provides: data shape, children, container, handlers.
3. A prop that only exists for one screen is a smell. Ask whether it is a variant.
4. Do not design the code API beyond this. The build side owns the final shape.

## 4. Component states

| State | When | What to specify |
| --- | --- | --- |
| Default | At rest | The reference file |
| Hover | Pointer over it, where hover exists | The change, and that touch gets no hover-only meaning |
| Focus | Keyboard focus | A visible focus indicator that meets the 3:1 outline floor |
| Pressed or active | During press | The change and its duration token |
| Selected or checked | Chosen | Not by color alone |
| Disabled | Cannot be used | Why it is disabled, said in words nearby when it matters |
| Busy or loading | Waiting on work | Whether the width holds; whether input is blocked |
| Error | Invalid or failed | The message, its placement, the error state in markup |
| Empty | No content | The copy and the next action |

List states by name for each component. "All states" is not a list. A state not designed is written "not designed" and appears again in section 9.

## 5. The screen state matrix

Write section 4.2, "Screen state matrix", as one row per screen and one column per state. Mark each cell `designed`, `n/a` (the screen cannot reach it), or `not designed`.

| Screen | Loading | Empty | Partial | Error | Success | Offline | Permission denied | Not found | Session expired |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Calendar | designed | designed | designed | designed | n/a | designed | n/a | n/a | designed |
| Booking detail | designed | n/a | n/a | designed | designed | designed | designed | designed | designed |

Rules:

1. A screen that loads data reaches loading, empty and error. Those three are never `n/a`.
2. Each action reaches pending and success or failure.
3. An error keeps the user's input.
4. A destructive action warns first and names what is lost.
5. The GCH screen-state rule, when loaded, sets the minimum list. This matrix must cover it.

## 6. Edge cases

List edge cases per feature in a subsection under the matrix. Each has a designed state or a recorded decision.

| Case | Example | Decision |
| --- | --- | --- |
| Long text | A name of 80 characters | Wrap to two lines, then truncate with the full text on focus |
| Short text | A one-letter name | Keep minimum widths |
| Huge numbers | 1,234,567 bookings | Compact notation above 10,000 |
| Zero and negative | A balance of -3 | Sign and word, not color alone |
| Many items | 200 rows | Pagination or virtual list; say which |
| One item | A list of one | No "1 items" copy |
| Slow network | 8 seconds to load | The long-wait tier copy |
| Small viewport | 320 px wide | The layout rule at that width |
| Large text setting | 200% zoom | Nothing clips; no sideways scroll |
| Right-to-left or long translations | A label 40% longer | Layout holds; see content |

Test charts with real, flat, empty and extreme data before calling a chart state designed.

## 7. AI entry points

An AI entry point is a component whose content comes from a model. It has five states beyond the usual ones: waiting, answered fast, answered slow, limited, failed or fell back. Specify each, and the decisions in the runtime sheet in [package.md](package.md), section 5.

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Happy-path inventory | Only the default state per component | Fill the state table |
| Look-named props | `big`, `blueVariant` | Rename by role |
| Duplicate component | A new card that is the library card with a margin | Reuse with a prop |
| Silent "n/a" | Error marked n/a on a screen that loads data | Loading, empty and error always apply |
| Names that drift | `BookingTile` in design, `BookingCard` in code | Take the code's name |
