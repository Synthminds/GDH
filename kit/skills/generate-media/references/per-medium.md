# Guides per medium

Read this file at step 6 of `generate-media`. It gives the working rules for each medium: image, vector, video, audio and voice, and 3D. Each part names the capability, what to decide before the call, how to prompt, what to check, and where the work goes next.

Evidence. The tool behaviors come from the connector cards, read from schemas, guides and workflow text on 2026-11-23: models differ per tool and change often; parameter names differ per provider; some tools offer a vector output mode that accepts no references; text-in-image models exist but text is unreliable; image-to-3D beats text-to-3D and one photo invents the back; some video models return silent clips; speech tools take voice ids only from their own live list; some audio models are restricted to certain uses by the tool. No generation ran in research. Model names are never written here; read them live.

## 1. Image (`image-gen`, `image-edit`)

Decide before the call:

| Decision | Options |
| --- | --- |
| Kind | Photograph, illustration, texture, mockup, concept |
| Aspect ratio | From the placement; the widest needed ratio when one image serves several crops |
| Size | The delivered size at 2x density, or the nearest the model offers; upscale later only if needed |
| Background | Full scene, plain ground, or transparent (ask for transparency or remove the background after) |
| References | Style references; subject references (the client's product photos) |
| Model | Read the tool's model list live. Pick by the job: photoreal, illustration, text in image, product mockup, many references. |

Prompt: follow `prompt-sheet.md`. One idea per prompt. Style line word for word. No text.

Check: `review-and-finish.md` image artifacts. Product fidelity against the real product.

Rules:

1. Text in an image is unreliable even in models made for it. Set text in the design.
2. A product mockup with readable text gets its text replaced in compositing.
3. A texture must tile: check the seams by repeating it four times.
4. A hero image leaves its text area calm and low in contrast variation.
5. A mood-board image is a reference for direction. It ships only after it is selected, finished and recorded.

Next: `website-design`, `infographic`, `motion-video` (as a still for a shot), `three-d` (as a reference view).

## 2. Vector (`vector`)

Decide before the call:

| Decision | Options |
| --- | --- |
| Kind | Spot illustration, icon set, pattern, concept for a mark |
| Route | A model's vector output mode; or a raster generation then vectorizing; or drawing by hand |
| Palette | A fixed list of hex values; some vector modes accept a color list |
| References | A vector mode may accept no reference images. Read the card. |

Rules:

1. A logo is never final from generation. Concepts only, inside `logo-identity`, then redrawn by construction.
2. A system icon set is drawn or licensed, not generated: icons need one grid, one stroke weight and pixel alignment.
3. Open every generated SVG in a text editor. Check the point count, hidden shapes, slivers, embedded rasters and stray colors.
4. Clean with an SVG optimizer and a reviewed config. Keep the `viewBox`.
5. Set fills to token values. Remove near-duplicate colors.
6. A vectorized raster is a tracing layer. Expect to redraw curves by hand for anything prominent.

Next: `logo-identity` (concepts), `website-design`, `infographic`, `ui-motion` (paths to animate).

## 3. Video (`video-gen`)

Decide before the call:

| Decision | Options |
| --- | --- |
| Shot | One subject, one action, one camera move |
| Source | Text-to-video; image-to-video from an approved still; video-to-video edit |
| Length | The shortest the shot needs; many models offer a few fixed lengths |
| Ratio and resolution | The delivery ratio; a lower resolution for the test |
| Sound | Some models return silent clips; plan sound in `motion-video` |
| Consistency | Reusable elements, references, one model for the sequence |

Rules:

1. Approve a still first. Animate the approved still. A still costs far less than a clip.
2. One camera move per shot: push in, pull back, pan, orbit, or static. Name it in the prompt.
3. Describe motion as physical action: "the paper slides into the tray and settles".
4. No text or logos in generated footage. Add them in composition.
5. Generate one short test clip at final settings before a batch.
6. Loops: ask for a seamless loop when the tool supports it, or plan a cross-fade at the loop point. Check the join.
7. Check every frame for morphing, identity drift and flicker before selection.

Next: `motion-video`, which owns the edit, sound, captions and export.

## 4. Audio and voice (`audio`)

Speech:

1. Read the tool's voice list live. Never use a voice id from memory or from another tool.
2. Choose by language, accent, age, tone and pace, from the brand words.
3. Write the line for the ear. Spell names phonetically when needed. Use the tool's markup for pauses and emphasis when it has some.
4. Set the number of takes explicitly; some tools default to more than one.
5. Test one paragraph before the full script.
6. A designed voice comes from a text description; its preview line comes from the user.
7. A cloned voice needs the person's written consent on record.

Music:

1. Brief the mood, tempo, instrumentation, length and ending. Instrumental under a voice.
2. Ask for the exact length with a clear ending, or plan to cut on a phrase.
3. Some music models are restricted by the tool to certain uses (games, for example). Read the card before using one for other work.
4. Read the output terms for music: commercial use, platforms, paid promotion.

Sound effects:

1. Short, specific descriptions: "soft paper slide, close, dry room".
2. Ask for a loop only for ambience.
3. One family of sounds per product or video.

Transcription:

1. Word-timed transcripts drive captions.
2. Correct names, numbers and product terms against the script.
3. Transcribing a client's recording uploads it: exposure gate.

Next: `motion-video` for mixing and captions; `ui-motion` for interface sounds, when the product has sound.

## 5. 3D (`3d-gen`)

Decide before the call:

| Decision | Options |
| --- | --- |
| Input | Photos (preferred: three views, front, side, back) or text (one object only) |
| Use | Web viewer, game, print, render; it sets the polygon target |
| Polygon target | From the use; set it with the parameter name the live schema shows |
| Textures | PBR textures for web; resolution for the device |
| Delivery | Web-ready options when the tool offers them: compressed geometry, reduced textures |

Rules:

1. Photos beat text. One photo invents the back: say so.
2. Parameter names for polygon count differ between providers. A wrong name may be dropped and the job runs with no limit.
3. Some 3D jobs cannot be cancelled once started. Say so in the spend check.
4. Download the model link at once; signed links can expire within an hour. Check it is a real GLB.
5. Never ship a generated mesh as delivered. `three-d` runs the pipeline: clean, reduce, UVs, textures, compression, validation.
6. Uploading the client's product photos is exposure. Ask first.

Next: `three-d`.

## 6. Avatar and presenter video (`avatar-video`)

No tested presenter or avatar tool is in the catalog. Do not promise one. `motion-video` gives the alternatives: a filmed presenter, voice-over with kinetic type, or a step the user runs in a tool's own app. Any likeness of a real person needs written consent.

## 7. Quick routing by medium

| Medium | Capability | First check | Hands off to |
| --- | --- | --- | --- |
| Photo or illustration | `image-gen` | Would a licensed asset or code do? | `website-design`, `infographic` |
| Edit or upscale | `image-edit` | Is this output selected? | the calling skill |
| Vector | `vector` | Is it a logo or a system icon? Then not here. | `logo-identity`, `website-design` |
| Clip | `video-gen` | Is the still approved? | `motion-video` |
| Voice, music, effect | `audio` | Consent and terms | `motion-video` |
| Model | `3d-gen` | Photos, use, polygon parameter | `three-d` |

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Model from memory | A call names a model that no longer exists | Read the model list live |
| One prompt, all media | The same prompt for a still and a clip | A prompt sheet section per medium |
| Text in footage | Words forming in a clip | No text in prompts; add in composition |
| Clip before still | Costly clips of an unapproved look | Still first |
| Voice id reused | A voice id from another tool fails | Live list per tool |
| Mesh as delivered | A dense generated GLB on the web | `three-d` pipeline |
| Generated icon system | Icons with uneven strokes and grids | Draw or license icons |
