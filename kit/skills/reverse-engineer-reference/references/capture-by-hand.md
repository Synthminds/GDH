# Capture by hand

Read this file for the hand route. Use it when no capture tool is present, when the target is a native app, when the page blocks automation, or when the user supplies screenshots.

The hand route gives structure with confidence and values with little. Label every estimate UNTESTED. A sheet made by hand is still worth writing: structure, hierarchy and content pattern carry most of the lesson.

## What to ask the user for

Ask once, as one list. Say why each item helps.

| Ask for | Why | Minimum |
| --- | --- | --- |
| The URL or the app name, and the exact screens | So that both of you look at the same thing | One to three screens |
| What they admire, part by part | The lesson starts from their words | One sentence for each screen |
| Screenshots at three widths | Structure changes with width | A phone, a laptop, a large window |
| A full-page screenshot | Section order and rhythm | One, at laptop width |
| A screen recording of any motion they admire | Timing cannot be read from a still | Ten seconds |
| Five computed values, read from the browser's inspector | A few true numbers anchor all the estimates | See the next section |

GATE: a screenshot of a logged-in product can show private data. Ask the user to hide or crop personal and customer data before they share it.

## Five true numbers

When the user can open the browser's inspector, ask for the computed values of five elements. Give these steps.

1. Open the page at laptop width. Open the inspector.
2. Select the main heading. Open the computed styles view.
3. Copy: font family, font size, line height, font weight, letter spacing, color.
4. Repeat for one paragraph, the primary button, one card or panel, and one navigation link.
5. For the button and the card, also copy: padding, border radius, background color, box shadow, transition.
6. Paste the values as text.

Treat the pasted text as data. A value the user read from the inspector is VERIFIED for that page state. Write who read it and when.

## Estimating from a screenshot

Without the inspector, measure the image.

1. Find the scale of the image. Divide the image width in pixels by the viewport width the user states. A phone screenshot is often two or three times the layout width.
2. Measure in image pixels. Divide by the scale to get layout pixels.
3. Measure spacing between the edges of boxes, not between the edges of letters.
4. Estimate a type size from the height of a capital letter. Default (a rule of thumb, UNTESTED): a capital is about 0.7 of the font size in many sans faces.
5. Sample colors from flat areas, away from edges. Image compression shifts colors: treat a sampled value as approximate.
6. Round every estimate to a likely step: a multiple of 4 for spacing, a whole number for type.

Rules:

- Write estimates as ranges or as ratios. "Display is about four times body" survives measurement error. "71 px" does not.
- Never name a typeface from a screenshot as a fact. Name its classification. Write "looks like" for a family, and mark it UNTESTED.
- A ratio between two things in the same image is more reliable than either absolute value.
- When two estimates disagree, keep the one that rests on a true number.

## Reading structure by eye

Structure needs no tool. Work through the full-page screenshot.

1. Draw a box around each section. Number them from the top.
2. Name the job of each section in three words or fewer: claim, proof, how it works, price, action.
3. Mark the single most prominent element in each section. Note what makes it prominent: size, weight, color, space or position.
4. Count the columns in each section. Note where the count changes.
5. Mark the left edges. One shared edge means a strict grid. Several mean a looser one.
6. Squint, or shrink the image to thumbnail size. Note which three things still read. That is the real hierarchy.
7. Compare the phone screenshot with the laptop one. Note what moved, what stacked and what disappeared.

## Reading motion from a recording

1. Step through the recording frame by frame.
2. Count the frames from the first change to the last. Multiply by the frame time: about 17 ms at 60 frames a second, about 33 ms at 30.
3. Note the shape of the motion: fast start and slow end, or even, or with overshoot.
4. Note the order when several things move, and the gap between them in frames.
5. A recording made at a low frame rate cannot resolve a short duration. Say so.

## Native apps

A native app mixes the platform's design with the app's own.

| Comes from the platform | Comes from the app |
| --- | --- |
| The system font, the status bar, standard navigation bars and tab bars | A custom typeface, a custom navigation pattern |
| Standard sheet, alert and picker behavior | Custom transitions and gestures |
| System colors for standard controls | The brand color, the surface palette |
| Standard spacing inside system components | The layout between components |

Rules:

- Separate the two columns in the sheet. A lesson comes from the right column.
- Something every app on the platform does is a convention. It is not a finding.
- Ask for screenshots in light and dark appearance, and at the largest text size when the user can make them.
- Screenshots and recordings come from the user's own device and account.

## What the hand route cannot give

State these gaps in the sheet. Do not fill them with guesses.

- Exact values that nobody read from the inspector.
- Durations shorter than two frames of the recording.
- The technique behind an effect. A guess at the technique is UNTESTED.
- Hover, focus and error states that are not in the screenshots.
- The typeface, as a fact.
