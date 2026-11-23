# The motion spec, prototype first, and the review

Read this file at steps 12 to 18 of `ui-motion`. It covers the motion spec format for handoff, the prototype-first workflow, the review method and checklist, and the main failure patterns.

Evidence. The four building blocks of a spec row (behavior, easing, duration, sequencing), the four-step workflow (layer, mock, prototype, ship), the constraint field and the checklist groups come from the Animation Handbook, chapter 3 and its checklists. The slowed review and the next-day review come from published animation review standards, read 2026-11-23. The filmstrip method is this kit's own agent route to the same checks. The spec table shape is this kit's own format.

## 1. The motion spec

One row per motion. Every field is filled. A missing field is an incomplete handoff.

| Field | Holds | Example |
| --- | --- | --- |
| id | Kebab-case name | `filter-menu-open` |
| element | What moves | Filter menu panel |
| trigger | The input or event | Click on "Filter"; Enter key |
| frequency | How often one person sees it | Tens a day |
| purpose | Orientation, feedback, continuity, attention or character | Orientation |
| behavior | What moves, from where, to where | Scales 0.96 to 1 and fades in from the trigger's top left |
| role | control, surface, page or flourish | surface |
| duration | Token name | `motion.duration.surface` |
| easing | Token name | `motion.ease.out` |
| sequencing | Order, delay, stagger | Starts at 0; items inside do not stagger |
| interruption | What happens on a retrigger or reverse | Second click closes from the current state |
| keyboard | Behavior when triggered by keyboard | Opens instantly |
| reduced motion | The variant | Opacity only |
| equivalent | The non-visual signal | `aria-expanded="true"` on the button |
| constraints | Engineering notes and exceptions | None |
| prototype | Path to the prototype, when one exists | `prototypes/filter-menu.html` |

Write the table in the motion plan and copy it into `design/handoff.md` through `handoff-to-code`. Add a second table, "Removed", with each cut motion and the reason (frequency, no purpose, budget).

Compact form for a large product: group rows by interaction type (feedback, hints, hierarchy, relationships, navigation) and state the shared fields once per group.

## 2. Prototype first

Motion that answers input can only be tuned by feel. Tune it outside the product, then port the values.

1. Layer. While the static layout is made, write motion notes beside it: what moves, from where, why. This is the inventory from `purpose-and-frequency.md`.
2. Mock. For a flow or a signature motion, make a short motion mock or a storyboard of key states. Use it to agree the idea with the user.
3. Prototype. Build each gesture, signature motion or tricky choreography as a standalone HTML file with its timing values exposed.
4. Ship. Port the approved values into tokens. Production values equal the values signed off in the prototype.

A prototype file exposes its variables so the user can tune them:

```html
<!doctype html>
<meta charset="utf-8">
<title>Prototype: filter menu</title>
<style>
  :root { --dur: 180ms; --ease: cubic-bezier(0.23, 1, 0.32, 1); --from-scale: 0.96; }
  .menu { transform-origin: top left; transition: opacity var(--dur) var(--ease), transform var(--dur) var(--ease); }
  .menu[data-open="false"] { opacity: 0; transform: scale(var(--from-scale)); pointer-events: none; }
</style>
<label>Duration <input type="range" min="80" max="500" value="180" oninput="document.documentElement.style.setProperty('--dur', this.value + 'ms'); out.textContent = this.value + ' ms'"></label>
<output id="out">180 ms</output>
<button aria-expanded="false" onclick="const m = document.querySelector('.menu'); const o = m.dataset.open !== 'true'; m.dataset.open = o; this.setAttribute('aria-expanded', o)">Filter</button>
<div class="menu" data-open="false">Menu content</div>
```

Rules:

1. One prototype per motion question. Do not build the whole screen.
2. Show two variants only when one named attribute differs: duration, curve, or distance. That is a refine-stage comparison.
3. Record the chosen values in the round entry of `design/decisions.md`.
4. A gesture prototype runs on a touch device. A desktop pointer cannot judge a swipe.
5. Offer an installed motion skill for variant pickers or audits when the user has one. Do not install it.

## 3. The review

Run the review on the render, never only on the code. An agent runs it with a capture tool that loads the page, fires input and evaluates script in the page. The evidence is a filmstrip and a value trace per motion, not a judgment from the source.

### 3.1 Filmstrip: pause, step, capture

The Web Animations API lists CSS transitions, CSS animations and script animations made with `element.animate()`. `document.getAnimations()` returns them; each one can be paused and moved to a time. Evidence: DOCUMENTED (MDN, Web Animations API). Not exercised in this build.

Install this helper in the page through the capture tool's evaluate call:

```js
window.gdhMotion = {
  freezeAt(fraction) {
    const list = document.getAnimations();
    for (const a of list) {
      const t = a.effect.getComputedTiming();
      const span = Number.isFinite(t.activeDuration) ? t.activeDuration : t.duration;
      a.pause();
      a.currentTime = (t.delay || 0) + span * fraction;
    }
    return list.length;
  },
  resume() { document.getAnimations().forEach(a => a.play()); },
  slow(rate) { document.getAnimations().forEach(a => { a.playbackRate = rate; }); },
  trace(selector) {
    const el = document.querySelector(selector);
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return { opacity: cs.opacity, transform: cs.transform, x: r.x, y: r.y, w: r.width, h: r.height };
  }
};
```

For each motion in the spec:

1. Load the start state. Install the helper.
2. Fire the trigger with the capture tool: a click, a key or a scroll.
3. Call `gdhMotion.freezeAt(0)`. A result of 0 means no animation was found. Wait one frame and call it again.
4. Capture a screenshot and call `gdhMotion.trace(<selector of the moving element>)`.
5. Repeat step 4 at 0.25, 0.5, 0.75 and 1. Name the frames `<id>-000.png` to `<id>-100.png`.
6. Read the five frames and the five traces. Look for a jump at the start, a wrong origin, a layout shift, a blur edge, a flash, two things moving at once.

Still 0 after one frame: a library drives the motion frame by frame from script. Use the library's own time scale, or record a video with the capture tool and take frames at the same five points. With neither, label the filmstrip UNTESTED.

### 3.2 Slowed play and retrigger

1. Slowed play: call `gdhMotion.slow(0.25)` right after the trigger. Record or capture at a fixed interval. This replaces the browser's animation panel.
2. Retrigger: fire the trigger, call `gdhMotion.freezeAt(0.5)` and take a trace. Call `gdhMotion.resume()`. Fire the reverse trigger at once: a second click, Escape, or a reversed gesture.
3. Call `gdhMotion.freezeAt(0)` on the new animations. Take a trace. Compare it with the mid-flight trace.
4. Default: a jump is a change of more than 2 px in position or 0.05 in opacity between the two traces. Rule of thumb; tune per product.
5. Capture the reverse filmstrip at 0, 0.25, 0.5, 0.75 and 1.

### 3.3 The rest of the review

1. Keyboard: tab through the flow with the capture tool's key presses. Keyboard actions do not wait for motion. Focus stays visible in every captured frame.
2. Reduced motion: emulate `prefers-reduced-motion: reduce` in the capture tool. Run 3.1 again. Each variant matches the spec.
3. Non-visual equivalent: after each change, read the ARIA state or the live region text from the page. With no screen reader, label the spoken check UNTESTED.
4. Load the worst realistic data: the longest list, the most notifications. Run the stagger at 1, 3, 12 and 20 items and capture the last item's first frame.
5. Slow device: throttle the CPU in the capture tool when it can. A real phone stays UNTESTED unless the user runs it.
6. Fresh pass: give the filmstrips, the traces and the spec to a reviewer who did not write the motion. Use the `design-critic` subagent, or the user. The author does not approve its own motion.
7. Optional, for a human: look again the next day. Motion that felt right at design time often feels slow later.
8. Ask a first-time viewer what moved. They name the primary element and the result, not the effect.
9. Record what you ran. Label what you could not run as UNTESTED.

### 3.4 Evidence form

Store the frames in `design/reviews/<date>-motion/` and write one line per motion in the review report:

```
<id>: filmstrip 000-100 <done | UNTESTED, reason>; slowed 0.25 <done>; retrigger delta <px, opacity>; reduced motion <done>; fresh pass <design-critic | user | none>
```

A gate that cites the review cites these lines. VERIFIED needs the frames on disk and the trace values.

## 4. The review checklist

A. Purpose and restraint, per motion
- [ ] It has one purpose from the list.
- [ ] It shows origin or destination when an element appears or leaves.
- [ ] It is the smallest motion that still communicates.
- [ ] It does not compete with a more important element.
- [ ] It supports the environment line.

B. Timing and easing
- [ ] Meaningful motion lasts 100 ms or more; press feedback may be shorter.
- [ ] Duration and easing are tokens with a role.
- [ ] No linear easing on movement; no ease-in on an entrance.
- [ ] Springs only where the design system allows, on movement only, barely perceptible.
- [ ] In-place content swaps have an out phase or a gap.
- [ ] Number changes move in the direction of the change.

C. Choreography
- [ ] Shared elements are connected across states.
- [ ] Stagger decays and stays inside the cap at 1, 3, 12 and 20 items.
- [ ] Secondary motion is weaker than primary motion.
- [ ] Panels exit toward the edge they entered from.

D. Interaction and fluidity
- [ ] Every input gets a visible response on the next frame.
- [ ] No motion blocks the next input.
- [ ] Gestures track the pointer and can be reversed or cancelled.
- [ ] Thresholds are signalled before release; limits resist and spring back.
- [ ] Look-alike components respond alike.
- [ ] Every wait shows motion.

E. Accessibility
- [ ] Reduced-motion variants exist for every motion.
- [ ] Every meaningful change has a non-visual equivalent.
- [ ] Motion-signalled errors set the error state in markup.
- [ ] Every gesture has a labelled alternative.
- [ ] Animated messages stay long enough for a screen reader.
- [ ] Nothing flashes; loops have a control.

F. Spec completeness
- [ ] Every row has purpose, behavior, easing, duration, sequencing, interruption, reduced motion and equivalent.
- [ ] Engineering constraints are noted per row.
- [ ] Gestures have a runnable prototype.
- [ ] Production values match the prototype sign-off.

G. Design system
- [ ] Three to five motion principles with reasons and examples.
- [ ] Signature motions listed with their allowed places.
- [ ] Guidance per interaction type.
- [ ] A change log and an exception process.

## 5. Worked review finding

```
Finding: dashboard cards fade up on every load (src/Dashboard.tsx, CardGrid).
Criterion: purpose test; frequency ladder (seen daily); tell list (entrance on every section).
Severity: medium. Effort: low.
Fix: remove the entrance; keep the skeleton-to-content swap with no movement.
Evidence: VERIFIED in a filmstrip and a recording at 0.25 speed, design/reviews/<date>-motion/. Real phone: UNTESTED.
```

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Tacked on | Motion appears first in the build phase | Motion notes at the layout stage |
| Video spec for a gesture | A screen recording is the only spec for a swipe | A runnable prototype |
| Drifted values | Production timing differs from the signed-off prototype | Port values as tokens; compare |
| Half rows | Spec rows with no reduced-motion or equivalent field | Every field filled, or the handoff is incomplete |
| Same-model self-review | The agent approves its own motion from code | Filmstrip and trace on the render; a fresh pass by `design-critic` or the user |
| Fast-machine bias | Smooth on the design laptop only | Throttle; real phone |
| Polish without end | Rounds continue after the gates pass | Stop when the gates pass and the user approves |
