# Decide whether 3D earns its place, and set the budget

Read this file at steps 1, 2, 4 and 16 of `three-d`. It covers the decision test, the cost of 3D, the budget sheet with its defaults, and the measurement protocol on real devices.

Evidence. The budgets apply the GDH resolution of conflict 20: 30,000 to 50,000 triangles for a hero model, 100,000 in view as the ceiling, measured on the device. Every budget number is a rule of thumb with no primary source, and stays a default. The draw-call guidance of a few hundred, with about 1,000 as an upper limit, and the pixel-ratio cap come from the React Three Fiber documentation, read 2026-11-23. The use-based triangle table comes from a 3D connector's photo-to-model workflow, read 2026-11-23; it is vendor guidance, not a standard.

## 1. The decision test

3D costs download, battery, build time and accessibility work. It must buy something a still or a video cannot.

Ask these questions in order. Stop at the first clear answer.

| # | Question | If yes | If no |
| --- | --- | --- | --- |
| 1 | Does the person need to turn, open or configure the object to decide? | 3D viewer or configurator | Continue |
| 2 | Does a third spatial dimension carry information (fit, volume, assembly, layout of a place)? | 3D scene | Continue |
| 3 | Does the data have a real third dimension that a 2D chart loses? | 3D data scene, with a 2D alternative | Continue |
| 4 | Is the 3D the brand's signature, named in the brief or the design system? | One hero scene, with a poster | Continue |
| 5 | Would a still, a short video or a turntable image sequence do the same job? | Use that instead | 3D may be justified; ask |

ASK the user with the answer and the cost: "A product viewer lets buyers turn the chair and see the back. It adds about 2 MB and a loading step. A turntable video would show the same angles without interaction. Which do you want?"

Cheaper alternatives:

| Alternative | Gives | Loses |
| --- | --- | --- |
| A set of rendered stills | Exact angles, tiny files, perfect quality | Free rotation |
| A turntable image sequence scrubbed by drag | Rotation feel, no WebGL | Free camera, lighting changes |
| A short muted video | Motion and mood | Interaction |
| A 2D chart or diagram | Clarity for most data | The spatial view |

## 2. The cost of 3D

| Cost | What it means |
| --- | --- |
| Download | The model, textures, environment map, decoders and the 3D library itself |
| CPU and GPU | Frame time, battery, heat on phones |
| Build time | Pipeline, scene code, testing on devices |
| Accessibility | A text alternative, keyboard control, reduced motion, a non-3D path |
| Content | Real dimensions and materials, often from the client |
| Maintenance | Library upgrades; asset changes need the pipeline again |

## 3. The budget sheet

Write the budget in `three-d-plan.md` before any model exists. Fill the "measured" column at step 16.

| Item | Default for a phone hero | Default for a desktop viewer | Measured |
| --- | --- | --- | --- |
| Triangles, hero model | 30,000 to 50,000 | up to about 100,000 | |
| Triangles, all in view | 100,000 ceiling | a few hundred thousand, if the device holds | |
| Download, model and textures | about 2 MB | about 5 MB | |
| Texture size | 1024 px | up to 2048 px | |
| Texture format | KTX2 (GPU-compressed) | KTX2 | |
| Draw calls | 50 to 100 | a few hundred | |
| Frame rate | 30 stable floor, 60 target | 60 | |
| Device pixel ratio | capped at 1 to 2 | capped at 1 to 2 | |
| Time to first frame of the model | after the poster; poster within the page's first paint | same | |

Default: every value above is a rule of thumb. Replace it with the user's or the design system's number. Measure on the device.

Budgets by use, from the 3D connector's workflow text (vendor guidance):

| Use | Triangles | Textures | Topology |
| --- | --- | --- | --- |
| Game or real-time hero | 10,000 to 30,000 | PBR | Triangles |
| Game prop on mobile | 2,000 to 8,000 | Simple | Triangles |
| Web or AR viewer | 30,000 to 50,000 | PBR | Triangles |
| 3D print | 200,000 or more | None needed | Triangles |
| Offline render or archviz | 100,000 to 500,000 | PBR | Quads if it will be edited |

Rules:

1. Set the budget from the weakest target device, not the design laptop.
2. A scene with several models shares one budget. A background model gets far fewer triangles than the hero.
3. Detail that does not change the silhouette goes into a normal map, not into triangles.
4. A configurator budgets for the heaviest configuration.

## 4. How to measure

Measure at step 16 and after every pipeline change that touches the model.

Devices:

1. A mid-range phone from two or three years ago, on its own browser.
2. A laptop with integrated graphics.
3. The user's main device, when known.

What to record:

| Metric | How |
| --- | --- |
| Frame rate during interaction | A frame-rate overlay or the browser performance panel while rotating and zooming |
| Long frames | Performance panel recording; frames over 16.7 ms at 60 Hz |
| Draw calls and triangles | The renderer's statistics: in three.js, `renderer.info.render.calls` and `.triangles` |
| GPU memory | The renderer's memory statistics, `renderer.info.memory` (geometries, textures) |
| Download | Network panel, compressed transfer size of the model, textures and decoders |
| Time to model | From navigation to the model's first frame, on a throttled connection |
| Heat and battery | Two minutes of interaction on the phone; note if it throttles |

A small statistics readout for development builds:

```js
// log renderer statistics once a second in a development build only
setInterval(() => {
  const { calls, triangles } = renderer.info.render;
  const { geometries, textures } = renderer.info.memory;
  console.log({ calls, triangles, geometries, textures });
}, 1000);
```

Rules:

1. Turn on CPU throttling and a slower network profile for laptop tests that stand in for phones. A real phone still beats a simulation.
2. Test with the tab visible, then hidden, then the canvas scrolled off screen. Rendering stops in the last two.
3. Record each device and number in the closing report. Without a real device, write UNTESTED.

## 5. When the budget fails

Fix in this order, cheapest first:

1. Render on demand instead of every frame, for a static scene.
2. Lower the device pixel ratio cap, or let it drop under load.
3. Reduce texture size one step on phones.
4. Decimate the background models first, then the hero.
5. Merge or instance repeated meshes to cut draw calls.
6. Remove real-time shadows; bake shadows and ambient occlusion into textures.
7. Use level of detail: a lighter mesh when the camera is far.
8. Ask the user to drop a feature (an effect, a second model) when the rest fails.

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| 3D as decoration | A spinning shape with no job | The decision test; a still or video |
| Budget after the fact | The model is chosen, then found too heavy | Write the budget before any model |
| Laptop-only testing | Smooth on the design machine, 12 fps on a phone | Measure on a mid-range phone |
| One number for all | The same budget for a hero and a background | Split the budget by role |
| Detail in triangles | A million triangles for surface texture | Normal maps |
| Numbers as law | A rule of thumb treated as a gate | Defaults; measure and decide with the user |
