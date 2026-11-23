# Checks for video, audio and motion

Read this file at step 2 of `accessibility-gate` when the work holds a video, an audio piece, interface motion, a scroll-driven story or a 3D scene. Classes and source classes follow the legend in the web and app reference.

Motion design belongs to `ui-motion`, `motion-video` and `three-d`. This file checks whether people can perceive the result, control it and stay well while it plays.

Three risks are specific to this medium. A person may not hear the sound. A person may not see the picture. Motion itself can cause dizziness, nausea or a seizure. The third risk is why some checks here are gates with no exception for brand.

## 1. Video and audio

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| V1 | Speech has captions, or the piece has a transcript | Gate | GDH gate | Caption check |
| V2 | Nothing flashes | Gate | Kernel floor | Flash check |
| V3 | Caption text and on-screen text are 4.5:1 or more, or sit on a solid backing | Gate | Kernel | Worst point |
| V4 | A player on a page works by keyboard: play, pause, seek, volume, captions | Gate | Kernel | Keyboard pass |
| V5 | A video on a page stops under reduced motion and shows its poster, unless the person starts it | Gate | Kernel | Reduced motion |
| V6 | No meaning by color alone in graphics and lower thirds | Gate | Kernel | Grayscale frame |
| V7 | Captions are accurate, complete and in time with the speech | Default | Memory: WCAG 2.2 | Caption check |
| V8 | Captions name the speaker when it is unclear, and note sounds that matter | Default | Memory: captioning practice | Caption check |
| V9 | The flash threshold is three in one second | Default | Memory: WCAG 2.2 | Flash check |
| V10 | A transcript exists for audio-only content | Default | Memory: WCAG 2.2 | Look |
| V11 | Visual information that the audio does not carry is described: in the narration, in audio description, or in the transcript | Default | Memory: WCAG 2.2 | Eyes-closed pass |
| V12 | The message is clear with the sound off | Default | Rule of thumb | Muted pass |
| V13 | Caption text is about 4 to 5 percent of the frame height or more | Default | Rule of thumb | Measure a frame |
| V14 | Captions sit inside the safe area and clear of platform controls | Default | Rule of thumb: vendor guides disagree | Check in the real app |
| V15 | Each line of on-screen text stays long enough to read twice | Default | Rule of thumb | Read aloud twice |
| V16 | Media that plays by itself is muted, and has a pause control when it runs more than 5 seconds | Default | Read: Vercel. Memory: WCAG 2.2 | Load the page |
| V17 | The voice is clear over music and effects | Default | Rule of thumb | Listen on a phone speaker |
| V18 | Burned-in captions are used only where the platform cannot show real ones | Default | Rule of thumb | Look |

Captions that are a separate text track can be resized, translated and searched. Captions burned into the picture cannot. Prefer the track. For short social video, where players often start muted and tracks are unreliable, burned-in captions are the practical default. Then supply a transcript as well.

Generated captions are a draft. A person checks names, numbers and terms before they ship. Kernel rule 11 applies: a caption that states what was not said is an invented fact.

## 2. Interface motion

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| U1 | Under the reduced-motion setting, movement and scaling are removed. Opacity and color changes may stay | Gate | Kernel. Read: Emil Kowalski standards, Vercel | Reduced motion |
| U2 | No essential information exists only in motion. A state change also has text, an icon or a static difference | Gate | Kernel. Read: Animation Handbook | Reduced motion, screen reader |
| U3 | Nothing flashes | Gate | Kernel floor | Flash check |
| U4 | Animation never blocks input. The next action works while the last one settles | Default | Read: Animation Handbook, Emil Kowalski standards | Rapid input |
| U5 | Motion that starts by itself and runs more than 5 seconds can be paused, stopped or hidden | Default | Memory: WCAG 2.2. Read: Vercel | Watch |
| U6 | Large-area movement, zoom, spin and parallax are rare and never tied to scroll without need | Default | Rule of thumb: these are known triggers of discomfort | Watch |
| U7 | Scroll-driven effects never take over the scroll | Default | Search: scrollytelling guidance | Scroll with keyboard and wheel |
| U8 | A motion-signalled error also sets the field's invalid state and shows text | Gate | Kernel, by U2 | Screen reader |
| U9 | A message that leaves by itself stays long enough to read and to be announced | Default | Read: Animation Handbook | Screen reader |
| U10 | Looping motion pauses off screen and when the tab is hidden | Default | Read: Rauno Freiberg | Inspect |
| U11 | Keyboard-driven actions do not animate | Default | Read: Emil Kowalski standards | Keyboard pass |
| U12 | A theme switch triggers no transition | Default | Read: Rauno Freiberg | Switch the theme |
| U13 | The reduced-motion variant was designed, not left to chance | Default | Read: Emil Kowalski standards | Review the variant |

Reduced motion does not mean no feedback. A press still responds. A panel still appears. It appears without travel.

## 3. Scroll stories and 3D scenes

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| T1 | A scroll story reads in a static form, with script off or motion reduced | Gate | Kernel, by U1 and U2 | Reduced motion, script off |
| T2 | Each scroll step changes one thing | Default | Rule of thumb | Scroll slowly |
| T3 | Native scrolling is kept. Swipe and tap hijacking are not used | Default | Search: scrollytelling guidance | Scroll |
| T4 | A 3D canvas has a text alternative that says what it shows | Gate | Kernel floor | Inspect |
| T5 | 3D controls work by keyboard, or the same information exists outside the scene | Gate | Kernel | Keyboard pass |
| T6 | Auto-rotation and camera motion stop under reduced motion | Gate | Kernel | Reduced motion |
| T7 | A static poster shows first and stays as the fallback | Default | Read: research notes on 3D for the web | Block WebGL |
| T8 | Rendering pauses when the canvas is off screen | Default | Read: Rauno Freiberg | Inspect |

## 4. The flash rule in practice

A flash is a fast, large change in brightness, or a saturated red change.

1. Look for strobes, fast cuts between light and dark frames, lightning, muzzle and camera flashes, and glitch effects.
2. Step through the suspect second frame by frame. Count the light-to-dark pairs.
3. Default threshold: three in one second. It comes from memory of WCAG 2.2, which also gives a size exception that this kit did not read.
4. When in doubt, remove or soften the effect. Lower the brightness difference, slow it down, or make it small.
5. A frame-by-frame count is a spot check. It is not an analysis tool. Say so in the report.
6. Generated footage needs the same check. A model can produce a strobe that nobody asked for.

This gate has no brand exception. A user cannot accept a seizure risk on behalf of an audience. When a brief asks for a strobe effect, say why it is unsafe and offer a version below the threshold.

## 5. Caption check, step by step

1. Play the piece with captions on and the sound on. Mark each mismatch.
2. Play it with captions on and the sound off. The message must still be complete.
3. Check names, numbers, product terms and anything spelled unusually.
4. Check the timing at each cut. A caption must not hang over the next shot.
5. Check the position. Captions must clear lower thirds and platform controls.
6. Check one frame for contrast at the worst point of the picture behind the text.
7. Record what was checked: the whole piece, or a sample with its time ranges.

## 6. Worked example

A 30 second product video, invented for this example, for a page embed and for vertical social formats.

- V1: the voice-over has burned-in captions and no transcript. Pass for captions. Default V10 does not apply; V18 notes that a text track is missing for the page embed.
- V2: the logo sting cuts between white and dark frames five times in the first second. Fail. This is a gate with no exception. The sting is rebuilt as one slow fade.
- V3: white captions over a bright shot measure 1.8:1 at the worst point. Fail. A solid backing is added.
- V5: the page embed plays by itself and ignores the reduced-motion setting. Fail.
- V11: two shots show prices as on-screen text that the voice does not read. Default not met. The narration or the transcript must carry them.
- V14: UNTESTED. Nobody opened the export in the real apps.
- Verdict: fail. Three gates failed, two defaults not met, one check untested.

## 7. Common failures

| Name | Sign | Check |
| --- | --- | --- |
| Silent film | Speech with no captions and no transcript | V1 |
| Auto captions shipped | Wrong names and numbers in machine captions | V7 |
| Captions under the buttons | Text hidden by platform controls | V14 |
| White on bright | Caption text with no backing over a light shot | V3 |
| Strobe sting | A flashing logo or glitch transition | V2, U3 |
| Motion only | A shake, a pulse or a slide is the only sign of an error or a change | U2, U8 |
| No reduced variant | The setting is ignored, or it turns off all feedback | U1, U13 |
| Scroll hijack | The page moves at its own speed, not the reader's | U7, T3 |
| Endless loop | A background animation with no pause | U5, U10 |
| Blank canvas | A 3D scene with no alternative and no poster | T4, T7 |
