# 3D patterns

Read this file at step 3 of `three-d`. It covers four patterns: the product viewer, the hero scene, the data scene and the scroll scene, plus the configurator as a variant of the viewer. Each has its job, stack, budget, interaction, fallback, failure patterns and a worked example.

Evidence. The viewer and loading rules apply the React Three Fiber and Khronos guidance read on 2026-11-23. "At most one scene above the fold" and "about two scenes per page" come from a 3D library connector's build guide, read 2026-11-23; treat them as defaults. The scroll rules come from scrollytelling guidance confirmed by search. Every budget number is a rule of thumb.

## 1. Product viewer

Job: let a person turn, zoom and inspect a real object before they buy or decide.

| Part | Default |
| --- | --- |
| Stack | A web component for model viewing when the needs are rotate, zoom and AR; a 3D library when you need custom scenes or effects |
| Budget | 30,000 to 50,000 triangles; about 2 MB on a phone; 1024 to 2048 px KTX2 textures |
| Camera | Starts at the angle of the best product photo; orbit limited so the object never flips or leaves the frame |
| Interaction | Drag to orbit, pinch or wheel to zoom within limits, buttons for named views (front, side, back, detail) |
| Hotspots | Up to a few labelled points that move the camera to a detail and show text |
| Lighting | Neutral studio environment map; soft contact shadow under the object |
| Fallback | The product photo set; a turntable image sequence |
| AR | Offer it only when the device supports it and the model is at real scale |

Rules:

1. The model is the real product. Colors and materials match the photos. Scale is real.
2. Named-view buttons give keyboard and screen-reader users the same views as dragging.
3. Auto-rotate, if used, stops on the first interaction and under reduced motion.
4. The page shows price, name and buy action without waiting for the model.

Configurator variant: the person changes materials, colors or parts.

1. Load each option's texture or part on demand, not all at once.
2. Budget for the heaviest configuration.
3. Each option control is a real form control with a label. The 3D view is its preview.
4. Keep a summary of the chosen configuration in text.

## 2. Hero scene

Job: set the mood and state the brand idea on a first-impression page.

| Part | Default |
| --- | --- |
| Stack | A 3D library, or a library WebGL scene recolored through its config |
| Budget | Lighter than a viewer: the page still has to load fast. One model or one procedural shape. |
| Placement | At most one scene above the fold; about two scenes per page |
| Interaction | Light: a pointer parallax or a slow drift; never required |
| Text | Real HTML over or beside the canvas; never text inside the 3D |
| Fallback | The poster image is the first paint and stays when 3D cannot run |

Rules:

1. The poster carries the page's first paint. The 3D never delays the largest content paint.
2. The hero states one idea from the brief. A random abstract blob is a tell.
3. Under reduced motion, the scene shows a still frame.
4. The scene pauses when scrolled off screen.

## 3. Data scene

Job: show data that has a real third dimension: a terrain, a building, a network in space, a volume.

| Part | Default |
| --- | --- |
| Stack | A 3D library with instancing for many marks |
| Budget | Instanced marks: one draw call for many objects |
| Encoding | Height or depth encodes one measured value; color encodes a second at most |
| Interaction | Orbit within limits; hover or focus shows the value; reset view button |
| Alternative | A 2D chart or table of the same data, always available |

Rules:

1. Run the decision test hard. Most data reads better in 2D. A 3D bar chart distorts comparison.
2. Perspective changes apparent size. Never encode a value only by apparent size.
3. Labels and values stay in HTML, positioned over the canvas, so they stay sharp and readable.
4. `data-viz` owns the chart rules. This skill owns the 3D build.

## 4. Scroll scene

Job: tell a sequence where each scroll step changes the 3D view: an assembly, a tour, a product story.

| Part | Default |
| --- | --- |
| Stack | A 3D library with the camera or model state tied to scroll progress |
| Budget | As a hero scene; one model, steady frame rate while scrolling |
| Structure | Steps of text in normal flow; the canvas sticky beside or behind them |
| Motion | Each step changes one thing: a camera move, a part that separates, a highlight |
| Fallback | One still per step, in order, with the step text |

Rules:

1. Native scrolling is never hijacked. Scroll drives the scene; the scene never drives scroll.
2. Each step's text carries its meaning alone. The 3D illustrates.
3. Under reduced motion, show the still per step, or jump between states with no movement.
4. Interpolate the camera between step states with easing. Keep moves slow and short to avoid motion sickness.
5. An image sequence scrubbed by scroll is a valid, lighter alternative when the camera path is fixed.
6. `ui-motion` gives the timing and reduced-motion rules for scroll motion. `infographic` owns a data story.

## 5. Choosing a pattern

| The brief says | Pattern |
| --- | --- |
| "Let buyers see it from every side" | Product viewer |
| "Let them pick the color and fabric" | Configurator |
| "Make the first screen unforgettable" | Hero scene, after the decision test |
| "Show the site's terrain and where the units are" | Data scene with a 2D map alternative |
| "Walk them through how it is assembled" | Scroll scene |

## 6. Worked example: a chair viewer

Brief: an online furniture shop; buyers hesitate because they cannot see the back of the chair. The values below are illustrative. They show the shape of a filled plan, not a real measurement.

| Decision | Choice |
| --- | --- |
| Decision test | Question 1 is yes: buyers need to turn the object |
| Pattern | Product viewer with named views |
| Route | Generated from four product photos, then repaired; the shop supplied real dimensions |
| Budget | 40,000 triangles; 1.6 MB with KTX2 textures at 1024 px; 6 draw calls |
| Stack | A model-viewing web component; AR on supported phones |
| Camera | Three-quarter front at eye height; polar angle limited; zoom between 0.6 m and 2.5 m |
| Views | Buttons: Front, Back, Side, Seat detail |
| Lighting | Neutral studio environment map, soft contact shadow |
| Fallback | The six product photos, shown first and kept |
| Accessibility | Text alternative names the chair and its material; named-view buttons; no auto-rotate under reduced motion |
| Measured | Mid-range phone 55 to 60 fps; integrated-graphics laptop 60 fps; model visible 1.9 s after the poster on a throttled connection |

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Floating blob hero | An abstract shape with no link to the brief | One idea from the brief, or a still |
| Two heavy scenes above the fold | The first paint waits on WebGL | One scene; poster first |
| 3D bar chart | Values read wrong because of perspective | 2D chart; 3D only for real 3D data |
| Text in the scene | Headlines rendered in WebGL | HTML text over or beside the canvas |
| Scroll hijack | The page stops scrolling while the camera flies | Scroll drives progress; native scroll stays |
| Flip-over camera | The object turns upside down or leaves the frame | Orbit limits and a reset view |
| Viewer as gate | Price and buy button load after the model | Commerce content renders first |
