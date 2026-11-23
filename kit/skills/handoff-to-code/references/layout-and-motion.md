# Layout, breakpoints and the motion spec

Read this file at step 9 of `handoff-to-code`. It covers how to write layout rules a builder can implement without guessing, the breakpoint table, and how the motion spec from `ui-motion` enters the package.

Evidence. The motion row fields come from the `ui-motion` spec format, built on the Animation Handbook (DesignBetter), chapter 3: DOCUMENTED. The layout table shape is this kit's own. Breakpoint values are defaults: the project's design system or the GCH `ux-laws` skill governs when present.

Terms. A breakpoint is a width where the layout rule changes. A container is the element that sets the maximum line of content. A layout rule says how a region behaves as the width changes.

## 1. Write rules, not pictures

A builder can implement a rule. A builder must guess from a picture. For each region, state what happens as width changes.

| Region | Rule | Tokens |
| --- | --- | --- |
| Page container | Max width `layout.content-max`, centered, side padding `space.5`; padding `space.3` below 600 px | `layout.content-max`, `space.5`, `space.3` |
| Booking grid | Auto-fit columns with a minimum card width of 280 px; one column below that | `space.4` gap |
| Side panel | Fixed 320 px at 1024 px and up; becomes a bottom sheet below | `surface`, `radius.sheet` |
| Hero heading | Fluid size between the `display` and `h1` styles | type styles |

Rules:

1. Name the token for every space, size and radius. A raw value goes to "to tokenize".
2. Say what grows, what wraps, what stacks and what hides at each change.
3. A hidden region says where its content goes. Hiding without a home loses content.
4. Body text keeps a 45 to 75 character line. Default: 45 to 75 characters.
5. No sideways page scroll at any width. A wide table scrolls inside its own container.
6. State the order of regions when stacked. Reading order must match visual order.

## 2. The breakpoint table

Write section 4.3 of `design/handoff.md` with one row per breakpoint. Use the design system's breakpoints when it has them.

| Name | Min width | Columns | Gutter | Container | Changes |
| --- | --- | --- | --- | --- | --- |
| phone | 320 | 4 | `space.3` | fluid | Side panel is a sheet; three-day calendar |
| tablet | 600 | 8 | `space.4` | fluid | Two-column grid |
| desktop | 1024 | 12 | `space.5` | `layout.content-max` | Side panel fixed |
| wide | 1440 | 12 | `space.5` | `layout.content-max` | Nothing new; content stays centered |

Default: test at 320, 390, 768, 1024 and 1440 px, and at 200% zoom. The QA captures use the same widths.

Each screen in the matrix names the breakpoints it was designed at. A breakpoint not designed is an open question, not a builder's choice.

## 3. Touch, pointer and density

- Default: 24 px minimum target for pointer, 44 px for touch, 48 dp on Android. When GCH is loaded, its single `ux-laws` number governs.
- State the density mode when the product has one: comfortable or compact, and which tokens change.
- Hover-only meaning is not allowed. Each hover reveal has a focus and touch route.

## 4. The motion spec in the package

Copy the motion table from the `ui-motion` plan into section 5. Do not invent motion here. With no plan, write "no authored motion" and say that default transitions follow the duration and easing tokens.

Each row carries these fields. A missing field is an incomplete handoff.

| Field | Holds |
| --- | --- |
| id | Kebab-case name |
| element | What moves |
| trigger | The input or event |
| purpose | Orientation, feedback, continuity, attention or character |
| behavior | What moves, from where, to where |
| duration | A duration token name, never a number |
| easing | An easing token name, never a curve |
| sequencing | Order, delay, stagger rule |
| interruption | What happens on a retrigger or a reverse |
| reduced motion | The variant under the reduced-motion setting |
| equivalent | The non-visual signal, for example an expanded state on the button |
| constraints | Engineering notes, filled at a sync point |
| prototype | The path of the tuned prototype, when one exists |

Rules:

1. Production values equal the values signed off in the prototype.
2. Add the "Removed" table from the plan, so a builder does not add back a cut motion.
3. Brand motion tokens govern page and flourish moments. Control motion follows the control role.
4. A stagger has a cap on total time at any item count. State the cap.
5. A gesture-driven motion ships with a runnable prototype, not a video.

## 5. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Desktop-only design | No phone rule for a region | Add the rule or an open question |
| Numbers in motion rows | "300 ms ease-out" | Token names only |
| Hide without a home | A filter bar vanishes on phone | Say where it goes |
| Missing reduced motion | A row with no variant | Every row has one |
| Breakpoints by device name | "iPhone layout" | Widths, not devices |

## 6. Worked example

Region: "Filters". Desktop: a left column of checkboxes, 240 px, `space.4` gap. Tablet: the same column collapses into a "Filters" button that opens a sheet. Phone: same as tablet, sheet full height. Motion row `filter-sheet-open`: trigger "Filters" button; purpose orientation; behavior slides up from the bottom edge and leaves the same way; duration `motion.duration.surface`; easing `motion.ease.out`; reduced motion opacity only; equivalent `aria-expanded` on the button.
