# Light, color, camera and interaction

Read this file at step 13 of `three-d`. It covers image-based lighting, direct lights and shadows, color space and tone mapping, camera framing and limits, and the interaction design of a 3D element.

Evidence. "An image-based environment map plus at most a few direct lights" and "set the output color space and tone mapping on purpose" are from the GDH research, tagged as prior knowledge of the three.js manual, not read in this build. The note that area lights and procedural world lighting do not survive GLB export comes from a hosted scene builder's guide, read 2026-11-23. The CC0 status of the main environment-map library was confirmed in its API README on 2026-11-23. Field-of-view and orbit values are rules of thumb. Every number is a default.

## 1. Lighting

Physically based materials look gray and flat without an environment to reflect. Light the scene with an environment map first, then add a few direct lights only where needed.

| Layer | Job | Default |
| --- | --- | --- |
| Environment map (image-based lighting) | Fills reflections and soft light from all sides | A neutral studio HDR, self-hosted, 1k for phones, 2k for desktop |
| Key light | Shape and a clear shadow direction | One directional light, above and to one side |
| Fill or rim | Separate the object from the ground | Optional; one at most |
| Ground contact | Anchors the object | A soft contact shadow or baked occlusion under the object |

Rules:

1. Pick the environment for the mood of the brief. A neutral studio for products; a warmer interior or outdoor light only when the brand calls for it.
2. Keep the environment's own image off-screen for a product; show only its reflections and light. A blurred or solid background from the tokens sits behind.
3. Real-time shadows are expensive. Prefer a baked contact shadow or a precomputed shadow texture on a static object.
4. Area lights and procedural world lighting from a modeling tool may not survive glTF export. Rebuild the light in the scene.
5. Self-host the environment map and record it in the manifest. Do not load a helper library's preset from a CDN in production.

## 2. Color space and tone mapping

1. Output in sRGB. Base color and emissive textures are sRGB; normal, roughness, metalness and occlusion are linear.
2. Pick a tone-mapping curve on purpose. A filmic curve suits most products. A neutral curve keeps brand colors closer to their values. Compare both on the real product colors.
3. Set exposure so whites are not clipped and the darkest material still shows its texture.
4. Check brand colors after tone mapping. A brand red can shift under a filmic curve. Adjust the material, not the token.
5. Check the scene on a phone screen and a desktop screen; contrast and gamma differ.

Symptoms and causes:

| Symptom | Likely cause |
| --- | --- |
| Washed out, milky textures | sRGB texture read as linear, or a double conversion |
| Too dark, crushed shadows | Missing environment map, or exposure too low |
| Metal looks black | No environment to reflect |
| Brand color off | Tone mapping shifted it; compare curves |
| Banding in the background | Low-precision gradient; add slight noise or use an image |

## 3. Camera

| Setting | Default for a product | Why |
| --- | --- | --- |
| Field of view | 30 to 45 degrees | Less perspective distortion than a wide lens |
| Start angle | The angle of the best product photo, often three-quarter front at eye height | Familiar and flattering |
| Target | The object's visual centre, not its origin at the floor | The object sits centred |
| Distance | The object fills about two thirds of the frame | Room for the silhouette |
| Orbit limits | Polar angle limited so the camera never goes under the floor or over the top | No flip, no ground clipping |
| Zoom limits | From a close detail to the full object with margin | The object never leaves the frame |
| Damping | On, light | Motion feels smooth |
| Reset | A visible "Reset view" control | A way back from any state |

Frame for every aspect ratio. A phone in portrait shows less width: pull the camera back or lower the field of view so the object fits.

## 4. Interaction

Choose the smallest interaction that serves the job.

| Interaction | Use for | Accessible equivalent |
| --- | --- | --- |
| Orbit by drag | Turning a product | Buttons for named views; arrow keys rotate |
| Zoom by pinch or wheel | Seeing a detail | Plus and minus buttons; named detail views |
| Named views | Front, back, side, detail | They are the equivalent |
| Hotspots | A labelled point that explains a feature | Focusable buttons in reading order; text panel |
| Configurator options | Material, color, part | Labelled form controls; a text summary |
| Pointer parallax | A light hero effect | None needed; it carries no information |
| Scroll-linked camera | A scroll story | The step text and a still per step |

Rules:

1. On touch, a drag on the canvas must not trap page scroll. Use one-finger orbit only when the canvas is the main content; otherwise require two fingers or a tap to activate. Set `touch-action` on purpose.
2. The wheel zooms only when the canvas has focus or after a click. A page scroll must not turn into a zoom.
3. Auto-rotate, when used, is slow, stops on the first interaction, and is off under reduced motion.
4. Hotspots stay few. Each one points at a feature named in the brief.
5. Every control has a visible focus state and a label.
6. Moving the camera to a named view uses an eased transition. Under reduced motion it jumps.

## 5. Environment and mood from the brief

| Brand words | Light and camera |
| --- | --- |
| Clean, precise | Neutral studio, soft key, high key overall, orthogonal-ish views |
| Warm, crafted | Warmer environment, lower key angle, gentle contrast, three-quarter views |
| Bold, dramatic | Strong key with deep shadow, dark ground from tokens, low camera |
| Calm | Soft even light, slow damping, no auto-rotate |

Keep one lighting setup across all models of a product line, so they look like a set.

## 6. Worked example: lighting a ceramic planter

| Decision | Choice |
| --- | --- |
| Environment | Neutral studio HDR, 1k, self-hosted, CC0, recorded in the manifest |
| Key | One directional light from upper left; no real-time shadow |
| Ground | Baked contact shadow texture on a plane, opacity from a token |
| Tone mapping | Neutral, because the glaze color is a brand color; checked against the swatch |
| Camera | 35 degrees; three-quarter front at 20 degrees above the rim; zoom 0.4 m to 1.5 m |
| Interaction | Orbit, plus Front, Side, Drainage detail buttons; reset view |
| Reduced motion | No auto-rotate; view buttons jump |

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| No environment | PBR materials look gray and dead | Image-based lighting first |
| Light rig of ten | Many lights, slow frames, confused shadows | Environment plus one key |
| Wide lens | The product looks bloated at the front | 30 to 45 degree field of view |
| Free orbit | The camera flips under the floor | Polar and zoom limits; reset view |
| Scroll trap | The page cannot scroll past the canvas on a phone | Touch and wheel rules |
| Color drift | The brand color changes in the scene | Compare tone-mapping curves; adjust the material |
| Endless auto-spin | The product never rests | Stop on interaction; off under reduced motion |
