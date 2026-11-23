# Checks for web and app UI

Read this file at step 2 of `accessibility-gate` when the work is a website, a web app, a mobile app or a desktop app. Each check has a class and a source class. Test methods are in the how-to-test reference.

## How to read the tables

| Column | Meaning |
| --- | --- |
| Class | `Gate` blocks delivery. `Default` is a starting value that the user, the design system or the brief can replace |
| Source class | `Kernel`: carried by the GDH kernel. `Read`: a primary source was read in the research. `Memory`: cited from memory of the standard or the platform guide. `Rule of thumb`: no primary source |
| Test | The method name in the how-to-test reference |

A number from memory is never a gate. Read the standard before you cite a criterion number in a report. Report a default that is not met as "default not met", with its source class. It is advice, not a failure of the gate.

## 1. See: color, contrast and text

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| W1 | Body text is 4.5:1 or more against its ground, in every theme | Gate | Kernel | Contrast |
| W2 | Large text is 3:1 or more. Large is 24 px, or about 18.66 px bold | Gate | Kernel | Contrast |
| W3 | Control outlines, focus indicators, icons that carry meaning and chart marks are 3:1 or more against the adjacent color | Gate | Kernel | Contrast |
| W4 | Text on a gradient, an image or a translucent surface passes at its worst point | Gate | Kernel, by W1 | Worst point |
| W5 | No meaning by color alone: status, required fields, links in text, current item, errors | Gate | Kernel | Grayscale |
| W6 | Placeholder text, helper text and disabled-looking but active text pass W1 | Gate | Kernel, by W1 | Contrast |
| W7 | Contrast does not fall on hover, active or focus | Default | Read: Vercel | Contrast, on each state |
| W8 | Secondary text on a colored surface is tinted from that hue, not plain gray | Default | Read: Impeccable craft floor | Look |
| W9 | Web body text is 16 px or more | Default | Read: Vercel | Measure |
| W10 | Body measure is 45 to 75 characters | Default | Rule of thumb, from several typographic sources | Measure |
| W11 | Text resizes to 200 percent with no loss of content or function | Default | Memory: WCAG 2.2 | Zoom |
| W12 | Wider text spacing breaks nothing: line height 1.5, paragraph space 2 times the size, letter space 0.12 em, word space 0.16 em | Default | Memory: WCAG 2.2 | Text spacing |
| W13 | Text is real text, not a picture of text | Default | Memory: WCAG 2.2 | Inspect |
| W14 | An inactive control is exempt from the ratio, but stays legible | Default | Memory: WCAG 2.2 | Look |

## 2. Structure and alternatives

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| W15 | One main heading. Headings in order, none skipped | Gate | Kernel floor, structure | Outline |
| W16 | Landmarks exist: header, navigation, main, footer | Gate | Kernel floor, structure | Outline |
| W17 | The page states its language | Gate | Kernel floor, structure | Inspect |
| W18 | Every image that carries meaning has a text alternative | Gate | Kernel floor | Inspect, screen reader |
| W19 | Decorative images are hidden from assistive technology | Gate | Kernel floor | Inspect |
| W20 | Every icon-only control has an accessible name | Gate | Kernel floor | Screen reader |
| W21 | Every page has a unique, descriptive title | Default | Memory: WCAG 2.2 | Inspect |
| W22 | Link text says where the link goes | Default | Memory: WCAG 2.2 | Links list |
| W23 | Native elements come before ARIA. A custom control exposes its name, role and state | Default | Read: Vercel | Inspect, screen reader |
| W24 | A data table has header cells. A layout table is not used | Default | Memory | Inspect |

## 3. Operate: keyboard, focus, pointer

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| W25 | Every function works by keyboard | Gate | Kernel | Keyboard pass |
| W26 | No keyboard trap. Focus can always leave | Gate | Kernel | Keyboard pass |
| W27 | Focus order follows the reading order | Gate | Kernel floor | Keyboard pass |
| W28 | Focus is always visible | Gate | Kernel | Keyboard pass |
| W29 | A focused element is not hidden behind a sticky header, a bar or a banner | Default | Memory: WCAG 2.2. Read: Vercel | Keyboard pass |
| W30 | The focus indicator is a 2 px outline with 3:1 contrast | Default | Memory: WCAG 2.2 enhanced level | Measure |
| W31 | A skip link is the first focusable element | Default | Read: Vercel | Keyboard pass |
| W32 | A dialog takes focus, holds it, closes with Escape and returns focus to its trigger | Default | Read: Vercel. Memory: ARIA practices | Keyboard pass |
| W33 | A menu, a tab set and a combobox follow the expected arrow-key patterns | Default | Memory: ARIA practices | Keyboard pass |
| W34 | Every gesture has a visible control that does the same thing: swipe, drag, pinch, long press | Gate | GDH gate. Read: Vercel | Gesture list |
| W35 | Targets are 24 CSS px for a pointer, 44 px for touch, 48 dp on Android | Default | Search and read: see the target table in `app-design` | Measure |
| W36 | Nothing is reachable by hover alone. A tooltip holds no interactive content | Default | Read: Rauno Freiberg | Keyboard pass, touch profile |
| W37 | Zoom is never disabled | Gate | Read: Vercel. A rule with no number | Inspect, zoom |
| W38 | No sideways page scroll at the narrowest supported width | Gate | GDH gate | Reflow |
| W39 | The narrowest supported width is 320 CSS px | Default | Memory: WCAG 2.2 | Reflow |
| W40 | Orientation is not locked without need | Default | Memory: WCAG 2.2 | Rotate |

A failure of W32 or W33 often causes a failure of W25 or W26. Then report the gate.

## 4. Motion and time

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| W41 | The reduced-motion setting is honored | Gate | Kernel | Reduced motion |
| W42 | No essential information exists only in motion | Gate | Kernel | Reduced motion |
| W43 | Nothing flashes | Gate | Kernel floor | Watch, slow motion |
| W44 | The flash threshold is three in one second | Default | Memory: WCAG 2.2 | Count |
| W45 | Motion that starts by itself and lasts more than 5 seconds has a pause, stop or hide control | Default | Memory: WCAG 2.2. Read: Vercel | Watch |
| W46 | Looping animation pauses when off screen | Default | Read: Rauno Freiberg | Inspect |
| W47 | A time limit warns first and can be extended | Default | Memory: WCAG 2.2 | Wait |
| W48 | A message that leaves by itself stays long enough to read and to hear | Default | Read: Animation Handbook | Screen reader |

## 5. Forms and feedback

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| W49 | Every input has a programmatic label | Gate | Kernel floor | Inspect, screen reader |
| W50 | An error names the field and the fix | Gate | Kernel floor | Form error path |
| W51 | An error keeps the input | Gate | Kernel floor | Form error path |
| W52 | An error is tied to its field and is announced | Default | Read: Vercel | Screen reader |
| W53 | A status message is announced without moving focus | Default | Read: Vercel | Screen reader |
| W54 | Autocomplete hints are set. Paste works. A password manager works | Default | Read: Vercel | Try it |
| W55 | Sign-in does not depend on a memory test or a puzzle alone | Default | Memory: WCAG 2.2 | Try it |
| W56 | Required fields are marked in words, not by color or a symbol alone | Gate | Kernel, by W5 | Grayscale |
| W57 | Help is found in the same place on each screen | Default | Memory: WCAG 2.2 | Compare screens |

## 6. Added checks for native and desktop apps

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| A1 | Text follows the system text size setting, with no clipping or overlap | Default | Memory: platform guides | Large text setting |
| A2 | Every control has a name, a role and a state for the platform screen reader | Gate | Kernel floor, by W20 and W49 | Screen reader |
| A3 | The screen reader's reading order matches the visual order | Default | Memory: platform guides | Screen reader |
| A4 | The app follows the system settings for dark mode, higher contrast and reduced motion | Gate for reduced motion. Default for the others | Kernel. Memory | System settings |
| A5 | A switch or an external keyboard can reach every control | Gate | Kernel, by W25 | Keyboard pass |
| A6 | Desktop: every command is reachable by keyboard, and shortcuts do not take over system ones | Gate for reach. Default for shortcuts | Kernel. Memory | Keyboard pass |
| A7 | A custom gesture or a shake action has a control and can be turned off | Gate for the control | GDH gate | Gesture list |
| A8 | Haptic or sound feedback is never the only signal | Gate | Kernel, by W5 | Mute and test |

Platform values come from memory of the platform guides. Read the current guide before release, and date the note.

## 7. What changes for an AI feature

- Streamed text is announced in useful pieces, not word by word. Label: UNTESTED unless a screen reader ran.
- The stop control is reachable by keyboard for the whole time the model works.
- A generated image has a text alternative written or checked by a person.
- A citation is a real link with text that names the source.
- The "generated" label is text, not color alone.

These five are GDH defaults. No primary source for them was read.

## 8. Common failures

| Name | Sign | Check |
| --- | --- | --- |
| Outline removed | Focus rings are turned off with no replacement | W28 |
| Click div | A `div` or `span` acts as a button or a link with no role, name or key support | W25, W23 |
| Placeholder label | The only label is gray text inside the field | W49, W6 |
| Gray on white | Light gray body or helper text | W1 |
| White on brand | White text on a mid-tone brand fill | W1 |
| Nameless icon | An icon button with no accessible name | W20 |
| Focus lost in a modal | Tab leaves an open dialog, or focus does not return on close | W32, W26 |
| Hidden focus | The focused control sits under a sticky header | W29 |
| Hover only | Content that appears only on hover | W36 |
| Drag only | An action that exists only as a drag | W34 |
| Red means error | Color is the only sign of a problem | W5 |
| Zoom lock | The viewport setting disables zoom | W37 |
| One theme checked | Dark mode fails checks that light mode passes | W1 to W4, per theme |
| Clean scan | An automated scan passed, so the work is called accessible | See the limits in the report format |

## 9. Order of work

When time is short, run the checks in this order. It follows harm: a person who cannot operate the screen at all comes first.

1. Keyboard: W25 to W28.
2. Names and labels: W18 to W20, W49.
3. Contrast in every theme: W1 to W6.
4. Color-only meaning: W5, W56.
5. Zoom and reflow: W37, W38.
6. Motion: W41 to W43.
7. Errors: W50, W51.
8. Structure: W15 to W17.
9. Every default.

List whatever you did not reach as UNTESTED. A short honest report beats a long guessed one.
