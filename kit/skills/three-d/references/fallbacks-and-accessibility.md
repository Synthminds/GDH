# Fallbacks and accessibility

Read this file at step 15 of `three-d`. It covers the loading order, the fallback tiers, the accessible form of a 3D element, and the checks.

Evidence. Poster first, a low-detail model next and the full model last (nested suspense) come from the React Three Fiber documentation, read 2026-11-23. A static poster as fallback that does not block the largest content paint, a text alternative, keyboard control and stopping auto-rotation under reduced motion come from the GDH 3D research checks. Pausing loops off screen comes from Rauno Freiberg's Web Interface Guidelines, read 2026-11-23. The device-tier rule of thumb is a default.

## 1. The loading order

1. The poster: a still render of the model from the start camera, in the canvas box, as part of the first paint.
2. The 3D library and decoders, loaded lazily when the box nears the viewport or on interaction.
3. A light version of the model, when the full one is large.
4. The full model, swapped in without a jump.
5. An interaction hint, only after the model can respond.

Rules:

1. The page's main content (headline, price, buy action, text) never waits for any 3D step.
2. The poster matches the first 3D frame: same camera, same light. The swap is not noticed.
3. A loader shows real progress or no number. No fake percentage.
4. Under a slow connection, the poster stays until the model is ready. Nothing blank shows.

## 2. Fallback tiers

| Tier | When | What shows |
| --- | --- | --- |
| Full | WebGL available, device holds the budget | The interactive scene |
| Reduced | WebGL available, frames drop under load | Lower pixel ratio, no shadows, lighter textures |
| Still | No WebGL, a failed load, data-saver on, or the person chose it | The poster, or a set of stills or a turntable image sequence |
| Text | Assistive technology, or no images | The text alternative and the same information as text |

Detect and choose:

```js
function webglAvailable() {
  try {
    const c = document.createElement('canvas');
    return !!(c.getContext('webgl2') || c.getContext('webgl'));
  } catch (e) { return false; }
}
const saveData = navigator.connection && navigator.connection.saveData;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!webglAvailable() || saveData) {
  showStills();          // the poster or stills stay
} else {
  loadScene({ autoRotate: !reduce });
}
```

Rules:

1. A load error falls back to the poster with a short message. It never leaves an empty box.
2. Let a person switch to the still view and back.
3. Default: treat a device that cannot hold 30 frames a second after the reduced tier as a still-tier device. Rule of thumb.

## 3. The accessible form

| Need | Provide |
| --- | --- |
| A name and description | A text alternative on the canvas container: what the object is, its material and color, what the views show |
| Keyboard control | Focusable buttons for named views, rotate left and right, zoom in and out, reset |
| Visible focus | A focus ring on every control, meeting the contrast floor |
| Screen reader feedback | A polite live region announces the current view: "Back view" |
| Information parity | Every fact the 3D shows (dimensions, materials, parts) also exists as text |
| Reduced motion | No auto-rotate, no camera drift, no parallax; view changes jump |
| Pointer alternatives | Every drag or pinch has a button that does the same |
| Hotspots | Real buttons in a logical order; their text in a panel, not only in the canvas |
| Color | Option swatches have text labels; no meaning by color alone |

Markup sketch:

```html
<figure class="viewer">
  <div class="viewer-canvas" role="img"
       aria-label="Oak dining chair with a woven seat. Use the view buttons to see the back and the seat detail.">
    <img src="/3d/chair/poster.webp" alt="" width="1200" height="900">
    <canvas aria-hidden="true"></canvas>
  </div>
  <div class="viewer-controls" role="group" aria-label="Chair views">
    <button type="button" data-view="front">Front</button>
    <button type="button" data-view="back">Back</button>
    <button type="button" data-view="side">Side</button>
    <button type="button" data-view="seat">Seat detail</button>
    <button type="button" data-action="reset">Reset view</button>
  </div>
  <p class="visually-hidden" aria-live="polite" id="view-status">Front view</p>
  <figcaption>Oak frame, hand-woven paper-cord seat. 46 cm wide, 52 cm deep, 80 cm high.</figcaption>
</figure>
```

## 4. Motion and safety

1. Auto-rotation and camera drift stop under reduced motion. Listen for changes to the setting.
2. A loop pauses off screen and in a hidden tab.
3. Large, fast camera moves can cause motion sickness. Keep transitions between views short and eased, and jump under reduced motion.
4. Nothing flashes: no strobing lights, no rapid material changes.

## 5. The checks

- [ ] The poster is in the first paint and the page is usable before the model loads.
- [ ] The fallback was seen working: WebGL off, a failed model URL, data-saver on.
- [ ] The text alternative names the object and what the views show.
- [ ] All interaction works by keyboard; focus is visible; the view is announced.
- [ ] Every fact in the 3D also exists as text.
- [ ] Reduced motion stops auto-rotate and drift.
- [ ] Rendering pauses off screen and in a hidden tab.
- [ ] Touch does not trap page scroll.

Record each check as passed, failed or UNTESTED in the closing report. Run `accessibility-gate` for the full pass.

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Blank box | A white rectangle while the model loads | Poster first |
| 3D blocks the page | The headline waits for WebGL | Main content first; 3D lazy |
| Mouse only | Views reachable only by dragging | View buttons and keys |
| Silent views | A screen reader hears nothing when the view changes | Live-region status |
| Facts only in 3D | Dimensions shown only as labels in the scene | The same facts as text |
| Fake progress | A percentage that jumps from 20 to 100 | Real progress or none |
| Broken fallback | WebGL off shows an error | Test each tier |
