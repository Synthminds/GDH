# Choreography and interruption

Read this file at step 9 of `ui-motion`. It covers stagger and its cap, shared elements, sequencing, staging, interruption, gestures, thresholds and limits.

Evidence. The stagger test counts (1, 3, 12 and 20 items), the decay formula, the shared-element rule and the gesture rules come from the Animation Handbook, chapters 2 and 4. The 30 to 80 ms stagger step, the transition-over-keyframe rule and the input rule come from published animation review standards, read 2026-11-23. The cascade cap is a rule of thumb. Every number is a default.

## 1. Choreography rules

1. One focal motion at a time. Two large things do not move at once.
2. One entrance per container. The container enters; its children do not each make their own entrance.
3. Related elements share a duration and a curve.
4. Secondary motion is weaker than primary motion. A viewer names the primary element first.
5. Input works during every choreography. Never disable a control for the length of an animation.
6. A page gets one authored entrance at most. Do not repeat the same fade on every section.

## 2. Stagger

Stagger starts similar items at slightly different times, so they read as linked yet separate.

Default step: 30 to 80 ms per item. Default cap: the whole cascade ends within about 500 ms, whatever the count.

A fixed step that suits three items drags at twelve. Use a decaying delay so the cascade gathers pace.

```js
// delay for item n (0-based), in ms; base = first step, cap = last start
function staggerDelay(n, base = 60, cap = 300) {
  return Math.min(cap, Math.round(base * Math.sqrt(n)));
}
```

Check the stagger with four counts:

| Items | Starts at (base 60, cap 300) | Last item ends (item duration 200 ms) |
| --- | --- | --- |
| 1 | 0 | 200 ms |
| 3 | 0, 60, 85 | 285 ms |
| 12 | 0 ... 199 | 399 ms |
| 20 | 0 ... 262 | 462 ms |

Rules:

1. Total cascade time is the last start plus one item duration. It stays inside the cap at every count.
2. A list that continues below the fold staggers only the visible items. Items scrolled into view later appear without a stagger.
3. The last item may take slightly more emphasis to close the sequence. Skip this when the list continues.
4. A list that rerenders often (search results while typing) does not stagger.
5. Under reduced motion, there is no stagger. Items appear together, with an optional short fade.

## 3. Shared elements and continuity

When two states share content (an image, a title, a card), move and resize that content between the states. Do not slide a new screen in over it.

| Transition | Shared element | Motion |
| --- | --- | --- |
| List to detail | The tapped card | The card grows into the detail panel |
| Thumbnail to full view | The image | The image scales and moves to its full place |
| Tab to tab | The active indicator | The indicator slides to the new tab |
| Collapsed to expanded row | The row | The row grows; rows below move down |

Rules:

1. Find the shared element first. A generic push or slide where a shared element exists is a defect.
2. The view transition API can carry a shared element across routes. See `scroll-and-view-transitions.md`.
3. Under reduced motion, a shared-element move becomes a short cross-fade.

## 4. Spatial model

1. An element that slides in from an edge lives beyond that edge. It leaves the same way.
2. Layers keep their order: a sheet over content, a dialog over a sheet. Motion never contradicts the stacking.
3. Forward navigation moves one way; back navigation moves the other way. Keep the direction consistent across the product.

## 5. Sequencing

Order a multi-part change so the eye has one path.

1. The element that leaves goes first.
2. The space closes or opens.
3. The new element enters.
4. Secondary details (a badge, a count) settle last.

Write the order and the offsets in the spec row's sequencing field: "out 0 ms; close 80 ms; in 120 ms".

## 6. Staging

1. When the eye is elsewhere, stage a change: a short gap or a small preparatory move before it happens.
2. Content swapped in place gets an out phase or a brief gap before the in phase.
3. A change the person must act on may get a short attention cue. A change they need not act on gets none.

## 7. Interruption

Every motion can be stopped, reversed or retriggered at any moment.

1. Use CSS transitions, or an animation library that animates from the current value, for motion that can be retriggered. A keyframe animation restarts from zero and jumps.
2. A second click during an opening starts the close from the current position, not from the end.
3. Never queue animations. A new input cancels the running motion and starts from where it is.
4. A route change during a transition completes the route at once.
5. Test: trigger each motion, then trigger it again at half way. No jump, no flash.

```css
/* retriggerable: transitions animate from the current value */
.menu { transition: opacity var(--motion-duration-surface) var(--motion-ease-out),
                    transform var(--motion-duration-surface) var(--motion-ease-out); }
.menu[data-state="closed"] { opacity: 0; transform: scale(0.96); pointer-events: none; }
```

## 8. Gestures

1. The element follows the pointer or finger continuously during the gesture.
2. The person can reverse, cancel or change target mid-gesture. Release settles to the right state.
3. On release, the motion takes the release speed. A flick goes further than a slow drag.
4. Every gesture has a labelled control that does the same thing. Pull to refresh also has a refresh button.
5. Design a gesture in a runnable prototype, with the engineer, from the start. A video cannot show a gesture's feel.
6. Modals and drawers that scroll set `overscroll-behavior: contain`, so a drag does not move the page behind.

## 9. Thresholds and limits

1. When a gesture crosses a threshold (it will now delete, or now cancel), show it before release: a color, an icon, a scale or a haptic.
2. At a limit (the end of a list, a drag past its range), the element resists and springs back. No silent dead end.
3. Resistance grows with distance. The element moves less than the finger past the limit.

## 10. Waiting

1. Every visible wait shows motion: a skeleton in the shape of the final layout, progress, or staged content.
2. A wait caused by another person or an agent shows an activity cue (a typing indicator).
3. Content arriving replaces the skeleton with no layout shift.
4. An optimistic change applies at once and rolls back with a plain message on failure.

## 11. Worked example: deleting a list item

| Order | Motion | Offset | Duration | Easing |
| --- | --- | --- | --- | --- |
| 1 | The row fades and shrinks to 0.98 | 0 ms | 150 ms | `motion.ease.out` |
| 2 | Rows below move up to close the gap | 80 ms | 200 ms | `motion.ease.in-out` |
| 3 | The count in the header rolls down by one | 200 ms | 150 ms | `motion.ease.out` |
| 4 | An undo toast enters from the bottom edge | 200 ms | 220 ms | `motion.ease.out` |

Interruption: a second delete during step 2 starts its own step 1 at once; the gap motions merge. Reduced motion: the row disappears, rows move instantly, the count changes, the toast appears with a fade. Non-visual equivalent: a polite live-region message "Task deleted. Undo available."

## 12. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Linear stagger | A 20-item list takes over a second to appear | Decaying delay and a cap |
| Everything moves | Header, cards and sidebar all enter at once | One focal motion; one entrance per container |
| Generic push | Detail slides in from the right over a tapped card | Shared-element continuity |
| Restart jump | A retriggered keyframe snaps to its start | A transition that animates from the current value |
| Locked input | Buttons disabled while a panel animates | Interruptible, non-blocking motion |
| Canned gesture | A swipe plays a fixed animation after release | Track the finger; settle with release speed |
| Wrong exit edge | A drawer enters left and leaves right | Exit toward the entry edge |
| Gesture only | Swipe is the only way to delete | A labelled control does the same |
