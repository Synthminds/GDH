# Scroll-driven motion and view transitions

Read this file at step 10 of `ui-motion`. It covers when scroll motion earns a place, scroll-driven animation in CSS, scrollytelling, smooth-scroll libraries, parallax, and route and view transitions.

Evidence. The scrollytelling rules (one change per step, no scroll hijacking, a static fallback, reduced-motion behavior) come from The Pudding and Chrome for Developers guidance, confirmed by search on 2026-11-23. The asset catalog records the View Transitions API and CSS scroll-driven animations as web platform features that need a support check and a fallback. The API names and code below are from memory of MDN. Read the MDN pages and check current browser support before you ship. Label the result UNTESTED until it runs in the target browsers.

## 1. When scroll motion earns a place

Scroll is the person's own input. Motion tied to it must stay under their control.

| Use | Earns a place when | Owner skill |
| --- | --- | --- |
| A progress indicator for a long read | The page is long and linear | `ui-motion` |
| A sticky header that compacts | Space is scarce on small screens | `ui-motion` |
| A reveal as a section enters | One authored moment on the page, not every section | `ui-motion` |
| A scroll-linked story with a sticky graphic | The content is a sequence of steps | `infographic`, timing here |
| A scroll-linked 3D camera | The 3D itself has a job; see `three-d` | `three-d`, timing here |
| Parallax on decoration | Rarely. Only as a flourish with a reduced-motion stop | `ui-motion` |

Rules:

1. Native scrolling is never replaced. No scroll hijacking, no snapping the page to sections against the person's input.
2. Scroll motion never hides content at rest. A person who scrolls fast or prints the page sees everything.
3. Text never moves at a different speed from the scroll (no parallax on text).
4. Each scroll step changes one thing.
5. Under reduced motion, scroll-linked movement stops. Content shows in its final state.

## 2. CSS scroll-driven animation

Scroll-driven animations bind an animation's progress to a scroll position instead of time. They can run off the main thread.

Two timelines, from memory of MDN:

| Timeline | Progress follows | Typical use |
| --- | --- | --- |
| `scroll()` | The scroll position of a scroll container | A reading progress bar |
| `view()` | An element's passage through the viewport | A reveal as a section enters |

```css
/* reading progress: the bar grows as the page scrolls */
.progress {
  transform-origin: 0 50%;
  animation: grow linear both;
  animation-timeline: scroll(root block);
}
@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }

/* one authored reveal: the element finishes entering before it is a third into view */
@supports (animation-timeline: view()) {
  .reveal {
    animation: rise linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 30%;
  }
}
@keyframes rise { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }

@media (prefers-reduced-motion: reduce) {
  .reveal, .progress { animation: none; }
  .progress { transform: none; }
}
```

Rules:

1. Wrap every scroll-driven rule in `@supports`. Without support, the element shows in its final state.
2. Linear easing is right here: the person's scroll supplies the acceleration.
3. Animate `transform` and `opacity` only.
4. Durations do not apply; ranges do. Write the range in the spec row (for example "entry 0% to cover 30%").
5. A scroll-driven reveal must end with the content fully visible while it is still well inside the viewport.

## 3. Scrollytelling

A story where each step of text changes one thing in a sticky graphic.

1. Write the steps first. Each step has one sentence and one change in the graphic.
2. Keep the graphic sticky with `position: sticky`. Keep the text in normal flow.
3. Trigger each change when its step crosses a fixed line in the viewport. An intersection observer or a step library does this.
4. Each change is a short transition (surface role), not a scroll-scrubbed animation, unless the data itself is continuous.
5. Keep CSS and script breakpoints in sync. On a phone, the graphic may sit above the text instead of beside it.
6. Provide a static form: the full graphic per step, in order, readable with scripts off or motion reduced.
7. The text alone carries the story. The graphic illustrates it.

## 4. Smooth-scroll libraries and parallax

1. A smooth-scroll library replaces native scroll physics. Default: do not use one. When the user asks for one, honor reduced motion and keep keyboard, find-in-page and anchor links working.
2. Parallax moves decoration at a different speed from the scroll. Use it only as a flourish, on decoration, with a reduced-motion stop.
3. Parallax and scroll-linked scaling are common triggers of motion sickness. They are the first things to remove under reduced motion.
4. Read the library license through `find-assets` before adding it.

## 5. View transitions

A view transition animates between two states of the page, or between two pages, with snapshots of the old and the new state.

Same-document transition, from memory of MDN:

```js
function show(view) {
  if (!document.startViewTransition ||
      matchMedia('(prefers-reduced-motion: reduce)').matches) {
    render(view);           // instant fallback
    return;
  }
  document.startViewTransition(() => render(view));
}
```

```css
/* name the shared element on both states so it moves instead of cross-fading */
.card-image  { view-transition-name: product-image; }
.detail-image { view-transition-name: product-image; }

::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: var(--motion-duration-page);
  animation-timing-function: var(--motion-ease-out);
}
```

Cross-document transitions between pages of one site use a CSS opt-in (`@view-transition { navigation: auto; }`). Check support per browser before you plan on them.

Rules:

1. Use a view transition for orientation: a shared element that moves, or a direction that tells forward from back.
2. Give each shared element one unique `view-transition-name` on each state. Two elements with one name on one state break the transition.
3. Keep the root cross-fade short. The shared element carries the motion.
4. Under reduced motion, skip the transition or keep a cross-fade only.
5. The page stays usable if the transition does not run. It is an enhancement.
6. In React, a view-transition skill from Vercel exists for route and shared-element transitions; it is offered, not installed.

## 6. Route transitions without the API

1. Default: no route transition in a professional tool used all day. The new page appears.
2. In a content site, one short cross-fade or a directional slide for forward and back.
3. Never hold the new page's content back for an exit animation of the old page.
4. Restore the scroll position on back navigation. Motion does not fight it.

## 7. Spec rows for scroll and view motion

| Element | Trigger | Range or duration | Easing | Purpose | Reduced motion | Fallback |
| --- | --- | --- | --- | --- | --- | --- |
| Reading progress | Root scroll | 0 to 100% of scroll | linear | Orientation | Static bar hidden | Hidden |
| Feature reveal | Section enters | entry 0% to cover 30% | linear | Attention | Final state | Final state |
| Product image to detail | Click on card | `motion.duration.page` | `motion.ease.out` | Continuity | Cross-fade | Instant |

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Scroll hijack | The page snaps or slows against the person's input | Native scroll; triggers, not control |
| Hidden at rest | Content waits at opacity 0 until scrolled | Final state is the default; motion is an enhancement |
| Reveal everywhere | Every section fades up | One authored reveal per page |
| Parallax text | Headlines drift at another speed | Parallax on decoration only |
| No support check | Elements stay invisible in a browser without the feature | `@supports` and a final-state default |
| Duplicate transition names | The shared element flickers or the transition aborts | One unique name per element per state |
| Exit holds the route | The new page waits for an exit animation | Show the new content at once |
