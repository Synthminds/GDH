# How to test

Read this file at steps 3 to 11 of `accessibility-gate`. Each test lists its steps, what it shows and what it cannot show. Measure on the render. A source file is not evidence of what a person sees.

Evidence. The contrast commands were run on 2026-11-23 against the kit's own token files. The other tests are procedures. No screen reader, browser or device was driven for this file, so their steps are DOCUMENTED.

## 1. Contrast of token pairs (gates 1 to 3)

```
DS="python3 <design-system skill folder>/scripts/ds.py"
$DS contrast design/tokens.json
$DS contrast design/tokens.json --pairs design/reviews/pairs.txt
$DS contrast design/tokens.json --json
```

1. Run the first command. It reads pairs from the usage notes, for example "Text on bg and surface."
2. Read the exit code. 0 means every pair passed. 1 means a pair failed or no pair was found.
3. "No pairs found" is not a pass. Write the usage notes or a pairs file, then run it again.
4. Write a pairs file for pairs that the notes cannot express. One pair on each line: `<fg> on <bg> [text|large|ui]`.
5. Use `text` for body copy, `large` for large text and `ui` for outlines, focus rings and chart marks.
6. A value in the pairs file can be a token name or a literal color.

Shows: the ratio of each named pair in every theme.
Cannot show: a pair that nobody listed, text on an image, or what a font weight does to legibility.

## 2. The worst point on a gradient, an image or a translucent surface

1. Find the place where the text meets the lightest or the darkest part of the ground.
2. Sample the ground color at that place from a capture of the render.
3. For a translucent surface, sample the composited color, not the token.
4. Add the sampled color to the pairs file as a literal. Run the contrast command.
5. Repeat for each theme and for each image that can appear behind the text.

Shows: the ratio at the sampled point.
Cannot show: every image a content editor uploads later. State this limit in the report.

## 3. Grayscale pass (gate 4)

1. Capture each screen, chart or slide. Convert the capture to grayscale.
2. List each place where two states or two series now look the same.
3. For each one, name the second carrier: a label, an icon, a shape, a pattern or a position.

Shows: meaning that only hue carries.
Cannot show: confusion between hues for a specific color vision deficiency. Use a simulator for that, and label the result as a simulation.

## 4. Keyboard pass (gates 5 and 6)

1. Put the pointer away. Start at the top of the page.
2. Press Tab through the whole flow. Write the order of the stops.
3. At each stop, check that a focus indicator is visible against its ground.
4. Operate each control: Enter or Space for buttons, arrow keys inside a composite control, Escape to close.
5. Open each overlay. Focus moves into it, stays inside it and returns to the trigger on close.
6. Note each trap, each skipped control and each stop that has no visible purpose.

Shows: reachability, order, focus visibility and traps for the flows you walked.
Cannot show: flows you did not walk. List them as UNTESTED.

## 5. Zoom and reflow (gate 11)

1. Set the viewport to the narrowest supported width. Default: 320 CSS px.
2. Check that the page scrolls in one direction only, except for a data table, a map or a diagram.
3. Set browser zoom to 200 percent at a desktop width. Check that no text is cut or overlapped.
4. Check that the viewport meta tag does not disable zoom.

Shows: reflow and resize behavior at the tested sizes.
Cannot show: behavior with a user stylesheet or a large system font setting.

## 6. Reduced motion (gate 7)

1. Turn on the reduced-motion setting in the operating system or the browser tools.
2. Reload. Walk the top flow.
3. Record each thing that still moves. Opacity and color changes may stay. Movement, scaling and parallax must stop or shorten.
4. Check that no information exists only in the motion that was removed.
5. Watch each animation and each video for flashing. Default: no more than three flashes in one second.

Shows: what the product does when the setting is on.
Cannot show: comfort for a person with a vestibular condition. The setting is a floor.

## 7. Screen-reader spot check (gates 8 to 10)

1. Pick the top task from the brief. Use the screen reader that ships with the test device.
2. Read the page by headings. Check for one main heading and an order with no gaps.
3. Move by landmarks. Check that the main region and the navigation are announced.
4. Complete the task. Write what is announced at each control: name, role and state.
5. Trigger one error. Check that the message is announced and names the field.
6. Listen to each meaningful image and chart. Check that the alternative says what the visual shows.

Shows: the experience of one task with one reader and one browser.
Cannot show: conformance. A spot check is a sample. Name the reader and the browser in the report.

With no screen reader in the session, inspect the accessibility tree in the browser tools. Label the result "tree inspection, not a reader".

## 8. Media: captions, transcript and controls (gate 12)

1. Play each video with the sound off. Check that captions carry the speech and each sound that matters.
2. Check caption timing against the picture at three points.
3. Check that a transcript exists for audio-only content.
4. Check that motion that starts by itself and lasts has a pause, stop or hide control.

Shows: presence and rough accuracy of captions.
Cannot show: caption quality for every line. State the sample size.

## 9. Target size (default)

1. Measure the rendered box of each control with the browser tools, including its padding.
2. Compare it with the default for the input type: pointer, touch or Android.
3. Check the space between two small targets that sit side by side.

Shows: the measured size at one viewport.
Cannot show: reach and comfort on a real device. Ask for a device check when the product is touch-first.

## 10. When no render tool exists

1. Ask the user to run tests 3 to 9 and to send captures and notes.
2. Run test 1 yourself. It needs only the token file.
3. Label every check you did not see as UNTESTED, with the reason.
4. Set the verdict to `incomplete`. An untested gate never passes.

## 11. What automated scanners prove

A scanner finds missing names, missing labels and some contrast failures. Default: treat a clean scan as a start, not as a pass. A scanner cannot judge focus order, the meaning of an alternative text or whether a flow can be completed.
