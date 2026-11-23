# Timing and easing

Read this file at steps 7 and 8 of `ui-motion`. It covers the timing table by element and distance, the resolutions of the source conflicts, exits, easing choice, springs and implied weight.

Evidence. The element ranges, the curves, the press scale and the spring default come from published animation review standards, read 2026-11-23. The 100 ms floor comes from the Animation Handbook, chapter 2. The 200 ms feedback rule comes from Rauno Freiberg's Web Interface Guidelines, read 2026-11-23. The distance adjustment and the toast and page rows are rules of thumb derived from those sources. Every number is a default. The design system and the user can replace each one.

## 1. How the source conflicts are resolved

| # | Conflict | Resolution used in this skill |
| --- | --- | --- |
| 3 | One guideline says interaction motion is 200 ms or less; the review standards allow up to 300 ms and longer for dialogs and drawers | Default: 200 ms for direct feedback to an input. Larger surfaces use the element table below. |
| 4 | Brand tokens can run 300 ms to a second; interface rules say under 300 ms | Brand tokens win for page and flourish moments. The short rule applies to controls. Map each token to a role. |
| 5 | The review standards default to springs for gestures; the owner's design systems ban springs | The design system decides. With no rule, a spring only for gesture-driven or interruptible motion. |
| 6 | The handbook sets about 100 ms as the shortest visible change; press feedback runs 100 to 160 ms; Material lists 50 ms | Default floor: 100 ms for motion that carries meaning. Shorter values serve press feedback only. |
| new | The handbook eases exits in; the review standards say never ease-in for interface motion | Default: ease-out for entering and for exits the person watches. Ease-in only for an element that leaves the screen while attention moves elsewhere, and keep it short. |

The last row is a resolution made in this skill. Record it in `design/decisions.md` when you apply it, so that `PRINCIPLES.md` can adopt it.

## 2. The timing table by element

| Element | Default duration | Role | Basis |
| --- | --- | --- | --- |
| Button press feedback | 100 to 160 ms | control | Review standards |
| Hover or focus color change | 100 to 200 ms | control | Rule of thumb inside the 200 ms feedback rule |
| Toggle, checkbox, switch | 100 to 200 ms | control | Rule of thumb |
| Tooltip, small popover | 125 to 200 ms | control | Review standards |
| Dropdown, select, context menu | 150 to 250 ms | surface | Review standards |
| Toast arriving | 200 to 300 ms | surface | Rule of thumb |
| Accordion, inline expand | 200 to 300 ms | surface | Rule of thumb |
| Dialog, drawer, sheet | 200 to 500 ms | surface | Review standards |
| List item added or removed | 150 to 300 ms | surface | Rule of thumb |
| Route or view transition | Design system, else 300 to 600 ms | page | Owner brand sets; rule of thumb |
| Brand flourish | Design system only | flourish | Ask |

Rules:

1. Direct feedback starts within one frame of the input. The motion may run longer; the first visible change may not wait.
2. Motion that carries meaning lasts 100 ms or more. Under that, a person reads it as a jump.
3. A meaningful change shorter than 100 ms is a defect unless it is press feedback.
4. Long durations on small things feel sluggish. 500 ms on a tooltip is a failure.

## 3. Adjust for size and distance

Small and near is short. Large and far is longer. The element table gives a range. Pick inside it by travel.

| Travel and size | Pick |
| --- | --- |
| Under about a quarter of the viewport, or a small element | The low end of the row |
| A quarter to half the viewport | The middle of the row |
| Most of the viewport, or a full-screen surface | The high end of the row |
| Across the whole screen on a large display | The high end. Do not exceed the row's maximum. Move less instead. |

Default: this banding is a rule of thumb. On phones, distances in pixels are smaller but relative to the screen they are large; judge by the share of the viewport.

When the motion must be long because the distance is long, reduce the distance. Start the element nearer its final place (for example 8 to 16 px of travel plus a fade) instead of flying it across the screen.

## 4. Exits

1. An exit is as fast as its entrance or faster. Default: about two thirds to three quarters of the entrance.
2. The element that leaves goes first. The elements that fill its space follow.
3. A panel exits toward the edge it entered from.
4. An element that returns goes back to where it came from: a dialog shrinks toward its trigger only when it grew from it.
5. A dismissed toast may slide off fast with an accelerating curve. Nothing waits on it.

## 5. Easing

| Kind of motion | Curve | Example token |
| --- | --- | --- |
| Entering the screen | ease-out: fast start, soft landing | `motion.ease.out` |
| Exit the person watches (a menu closes) | ease-out | `motion.ease.out` |
| Exit off screen while attention moves elsewhere | ease-in, short | `motion.ease.in` |
| Moving or morphing on screen | ease-in-out | `motion.ease.in-out` |
| Hover and color change | the plain `ease` curve | `motion.ease.standard` |
| Constant motion: spinner, progress, marquee | linear | `motion.ease.linear` |
| Sheet or drawer | a drawer curve with a strong ease-out | `motion.ease.drawer` |

Rules:

1. Never ease-in on an entering element. It delays the visible start and feels laggy.
2. Never linear on movement through space. Uniform speed reads as mechanical.
3. Linear is allowed on opacity and color when the project permits, and on constant loops.
4. A non-default curve names its real-world analog in the spec: a door, a drawer, a sheet of paper. With no analog, use the default token.
5. Default curves when the system has none: ease-out `cubic-bezier(0.23, 1, 0.32, 1)`; ease-in-out `cubic-bezier(0.77, 0, 0.175, 1)`; drawer `cubic-bezier(0.32, 0.72, 0, 1)`. Source: the review standards.

## 6. Springs

1. Read the design system first. When it bans springs, use none, and say so in the spec.
2. With no rule, use a spring when the motion follows a gesture, must stay interruptible, or settles after a release with speed.
3. Default spring: duration 0.5 s, bounce 0.2. Keep bounce between 0.1 and 0.3. Source: the review standards.
4. One small overshoot, then settle. A first-time viewer should not describe the element as bouncing.
5. No bounce on forms, tables, navigation or any control used daily.
6. Springs move position, scale and rotation. Never opacity or color.
7. A spring takes its initial speed from the gesture. A spring that ignores release speed is a curve in disguise.

## 7. Start state, origin and scale

1. Start near the final state: opacity 0 and scale 0.95 to 0.97, or 8 to 16 px of travel. Never from scale 0.
2. Press feedback scales to 0.95 to 0.98, typically 0.97. Never below 0.9.
3. A popover, menu or tooltip grows from its trigger. Set `transform-origin` there.
4. A dialog grows from the centre of the viewport. A drawer slides from its edge.
5. Default: no blur in transitions. When used, keep it under 20 px.

## 8. Implied weight

Objects that look alike respond alike. Give each moving surface a weight class in the spec.

| Weight | Behavior | Examples |
| --- | --- | --- |
| Light | Moves fast, may lag and pivot slightly behind a pointer | A chip, a card being dragged, a notification |
| Heavy | Tracks rigidly, starts and stops firmly | A full-screen sheet, a sidebar, a modal |

Rules:

1. A control that cannot do more still responds: it resists and springs back in the same physical language.
2. Within one visual group, the same input gives the same class of response. No member is inert.

## 9. Number and content changes

1. A value that rises rolls or slides up. A value that falls rolls or slides down. The final value is exact and stable.
2. Content that replaces content in place (a status line, a caption) gets a short out phase or gap before the in phase. A hard swap is easy to miss.
3. Tabular numerals keep a rolling number from shifting the layout.

## 10. Worked example: a filter menu

| Field | Decision |
| --- | --- |
| Element | Filter menu, about 280 by 320 px |
| Trigger and frequency | Click on "Filter"; tens of times a day |
| Purpose | Orientation |
| Role and duration | surface; 180 ms open, 130 ms close (low end: small and near) |
| Easing | `motion.ease.out` both ways |
| Start state | opacity 0, scale 0.96, origin at the top left of the trigger |
| Spring | None; the design system bans springs |
| Keyboard | Opens instantly when triggered by the keyboard |
| Reduced motion | Opacity only, 120 ms |

## 11. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Slow small things | A 500 ms tooltip | The element table; low end for small and near |
| Late start | Ease-in on an entrance | Ease-out |
| From nothing | Scale 0 to 1 | Start at 0.95 to 0.97 |
| Mechanical travel | Linear slide across the screen | Ease-out or ease-in-out |
| Elastic controls | Buttons that wobble | No spring on controls |
| Slow exit | The close takes longer than the open | Exit at two thirds to three quarters of the entrance |
| Far flight | A long duration to cover a long path | Shorten the path: start near the final place |
| Flash of change | A value swaps with no direction | Roll in the direction of the change |
