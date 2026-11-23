# Accessibility and performance of motion

Read this file at step 11 of `ui-motion`. It covers the reduced-motion gate and its variant table, non-visual equivalents, display time for animated messages, flashing and autoplay, and the performance budget with how to measure it.

Evidence. The reduced-motion rule, the property rule and the frame budget come from the Vercel Web Interface Guidelines and published animation review standards, read 2026-11-23. The equivalents, the error-state rule and the minimum display time come from the Animation Handbook, chapters 1, 3 and 4. The WCAG criterion numbers (2.2.2, 2.3.1, 2.3.3) and their thresholds are from memory and were not read in this build. They are defaults until someone reads the standard. The toast display time is a rule of thumb.

## 1. The reduced-motion gate

The gate: every stylesheet and script that moves something reads `prefers-reduced-motion`. The variant is designed with the motion, not added at the end.

| Motion | With reduced motion |
| --- | --- |
| Slide, scale, rotate | Removed. The element appears in its final place. An optional short fade remains. |
| Fade, color change | Kept. It may shorten. |
| Stagger | Removed. Items appear together. |
| Parallax, scroll-linked movement | Removed. |
| Shared-element move, view transition | A short cross-fade, or instant. |
| Autoplay video, looping animation | Stopped on its first frame or a poster, with a play control. |
| Spinner, progress bar | Kept. It carries information. A slower spin is fine. |
| Spring | Removed. The value is set. |
| Signature flourish | Its named reduced form: usually a cross-fade of the same content. |

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    scroll-behavior: auto !important;
  }
}
```

This blanket rule is a safety net, not the design. It can break motion that carries information (a progress bar). Write each variant from the table, then keep the net for third-party code.

In script:

```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
function animateOrSet(el, keyframes, options) {
  if (reduce.matches) { Object.assign(el.style, keyframes[keyframes.length - 1]); return; }
  return el.animate(keyframes, options);
}
reduce.addEventListener('change', () => { /* stop loops, rebuild timelines */ });
```

Rules:

1. Listen for changes to the setting. A person can switch it while the page is open.
2. A canvas or WebGL loop reads the setting too. Stop camera drift and auto-rotation.
3. An in-product motion setting, when the product has one, defaults to the system setting.

## 2. Non-visual equivalents

Motion must never be the only carrier of meaning. For each meaningful change, find the matching signal in code.

| Visual change | Equivalent |
| --- | --- |
| A toast appears | A polite live region announces its text |
| A field shakes on error | `aria-invalid="true"` on the field, the error text linked with `aria-describedby`, focus moved to the first error |
| A panel expands | `aria-expanded` on its control |
| A tab indicator slides | `aria-selected` on the new tab |
| A count rolls up | The new value is in the DOM text; a live region announces it when it matters |
| A row is deleted | A live-region message, and focus moves to a sensible neighbor |
| A drag reorders a list | Move up and move down controls, and an announcement of the new position |
| A loading skeleton | `aria-busy` on the region, and an announcement when content arrives |

Check: count the meaningful motions in the spec and count their equivalents. The two numbers match. On mobile platforms, use the platform's accessibility labels and hints in place of ARIA.

## 3. Display time for animated messages

1. A message that animates away must stay long enough to read, and long enough for a screen reader to finish it.
2. Default: an information toast stays at least 5 seconds, plus time for long text, and pauses while hovered or focused. Rule of thumb; test with a screen reader.
3. A message that needs action does not auto-dismiss.
4. Test: turn on a screen reader, trigger the message, and confirm it is read in full before it leaves.

## 4. Flashing, autoplay and vestibular safety

1. Nothing flashes. Default threshold: no more than three flashes in any one second (from memory of WCAG 2.2, criterion 2.3.1).
2. Motion that starts by itself and runs beside other content has a pause, stop or hide control. Default: this applies when it runs longer than 5 seconds (from memory of criterion 2.2.2). Simpler rule: give every loop a control.
3. Large movements across the screen, zooms, spins and parallax are the main vestibular triggers. They are the first to go under reduced motion, and they stay small without it.
4. Loops pause when off screen and when the tab is hidden.

```js
const io = new IntersectionObserver(([entry]) => {
  entry.isIntersecting ? loop.play() : loop.pause();
});
io.observe(loopElement);
document.addEventListener('visibilitychange', () => {
  document.hidden ? loop.pause() : loop.play();
});
```

## 5. The performance budget

The budget: each frame finishes in 16.7 ms at 60 Hz and 8.3 ms at 120 Hz, on a mid-range device, while the motion runs.

| Rule | Why |
| --- | --- |
| Animate `transform` and `opacity` | They can run on the compositor without layout or paint |
| Do not animate `top`, `left`, `width`, `height`, `margin` or `padding` | They force layout on every frame |
| Documented exceptions: `clip-path` for a reveal, a measured height for an accordion | Note each use in the spec's constraints field |
| List the properties; never `transition: all` | `all` animates properties you did not intend, including layout |
| Keep blur small; default under 20 px | Large blur is expensive to paint each frame |
| Use `will-change` only on an element about to animate, and remove it after | Each promoted layer costs memory |
| No layout reads inside an animation loop | Reading layout after a write forces a synchronous layout |
| No state updates or allocations per frame in a framework | They trigger renders and garbage collection |
| Lists over about 50 items are virtualized before they animate | Animating hundreds of nodes drops frames |

Accordion example with a measured height, the documented exception:

```js
// measure once, animate the height with a transition, then clear it
panel.style.height = panel.scrollHeight + 'px';
panel.addEventListener('transitionend', () => { panel.style.height = 'auto'; }, { once: true });
```

A modern alternative, when supported: animate `grid-template-rows` from `0fr` to `1fr` on a grid wrapper. Check support and label it UNTESTED until it runs.

## 6. How to measure

1. Open the browser performance panel. Turn on CPU throttling (for example four times slower) to mimic a mid-range phone.
2. Record while you trigger each motion. Look for long frames, layout and paint inside the motion.
3. Turn on the paint-flashing and layer-border overlays. Repaints during a transform motion point to a non-composited property.
4. Run on a real phone and a laptop with integrated graphics. A simulator hides dropped frames.
5. Record the device, the frame rate seen and any long frames in the closing report.
6. Label performance UNTESTED when no real device was used.

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| No variant | Reduced motion changes nothing | The variant table, written at design time |
| Blanket kill | The safety net stops a progress bar | Design each variant; keep the net for third-party code |
| Shake only | A failed field shakes and nothing else changes | `aria-invalid`, error text, focus |
| Toast too fast | A message leaves before a screen reader finishes | Minimum display time; pause on hover and focus |
| Endless loop | A background animation runs forever, off screen too | Pause control; pause off screen and in a hidden tab |
| Layout animation | `width` or `top` transitions | `transform`; a documented exception when unavoidable |
| `transition: all` | Unintended properties animate | List the properties |
| Simulator review | "Smooth" on a fast laptop, stutters on a phone | Throttle and test on a real device |
