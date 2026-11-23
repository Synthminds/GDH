# Forms, density and targets

Read this file at step 13 of `app-design`. It gives the rules for forms, the way to choose a density level, and the target sizes for touch and pointer input.

Precedence: the design system's form components, density scale and target tokens win. This file fills the gaps.

## 1. Forms

A form is a conversation in which the app asks and the person answers. Ask less, ask clearly, and never lose an answer.

### 1.1 Before the form

1. Take the required field list from the feasibility check. The system's required fields are not a design choice.
2. Remove every field that the job does not need. ASK before you remove a field that the business wants.
3. Do not ask for what the system already knows. Prefill it and let the person correct it.
4. Order the fields by the person's logic, not by the database's.
5. Say before the form what it is for and what happens after.

### 1.2 Structure

| Decision | Default | Why |
| --- | --- | --- |
| Columns | One column | A single path down the page is easy to scan and to tab through |
| Side-by-side fields | Only for parts of one thing: day, month, year; city and postal code | Two unrelated fields in a row get skipped |
| Label position | Above the field | It holds at narrow widths and with long translations |
| Grouping | A group with a group label for related fields | Assistive technology reads the group name |
| Required and optional | Mark the smaller set, in words | An asterisk alone needs a legend and is easy to miss |
| Long forms | Steps, each with one topic, a progress sign and a way back that keeps answers | A long page of fields hides how much is left |
| Field width | Sized to the expected answer | The width is a hint of what to type |

These are rules of thumb unless a class is named. The design system can replace each.

### 1.3 Fields

1. Every field has a visible label and a programmatic label. A placeholder is not a label. This is a gate.
2. Help text sits under the label, before the field, and stays visible while typing.
3. Use the right control: a switch for an immediate on or off, a checkbox for a choice that is submitted, radio buttons for one of a few, a select for one of many, a search field for one of very many.
4. Default: show a choice of five or fewer as visible options, not inside a select. This is a rule of thumb.
5. Set the input type, the input mode and the autocomplete hint. The right keyboard appears, and autofill works.
6. Never block paste. Password managers must work.
7. Format for the person: accept spaces in a card number, any common date order that is unambiguous, a phone number with or without a prefix. Clean it in code.
8. Use the platform's date, time and file pickers unless the job needs more.
9. Default: text inputs are 16 px or more on mobile web (read: Vercel).
10. A destructive field action, such as "remove", is undoable or confirmed.

### 1.4 Validation and errors

| Moment | Do |
| --- | --- |
| While typing, first time | Nothing. Do not show an error before the person finishes |
| On leaving a field | Check format. Show a message beside the field when it fails |
| While fixing a shown error | Clear the error as soon as the value is valid |
| On submit | Check everything. Move focus to the first problem. Summarize when there are several |
| After a server error | Keep every value. Say what failed and what to do |

Rules:

1. The message names the problem and the fix: "Enter a date after today", not "Invalid".
2. The message is tied to its field for assistive technology, and it is announced.
3. An error is marked by an icon and words, not by a red border alone.
4. Keep the submit button enabled. A disabled button cannot say what is missing. Explain on press.
5. Gate: no error path clears the person's input.
6. Confirm a successful submit and say what happens next.

### 1.5 Saving

- Choose one model for the app and state it in `DESIGN.md`: save on a button, or save on change.
- Save on change shows that it saved, and when.
- A long form saves a draft. Leaving with unsaved work warns once.
- A multi-step flow keeps each step's answers when the person goes back.
- With queued offline work, show "saved on this device" until it is sent.

## 2. Density

Density is how much information and how many controls share the screen. It is chosen for the person and the job, not for looks.

### 2.1 Choose the level

| Signal from the brief | Lean toward |
| --- | --- |
| Used all day by trained people | Compact |
| Rows are compared with each other | Compact |
| Pointer and keyboard input | Compact or default |
| Used now and then, or by the public | Comfortable |
| Touch input, or use on the move | Comfortable |
| Stress, gloves, a moving vehicle, one hand | Comfortable, with larger targets |
| Mixed audience | Default, plus a density setting |

### 2.2 What changes with density

| Changes | Does not change |
| --- | --- |
| Row height and cell padding | The minimum target size for the input |
| The gap between groups | The type size floor of the medium |
| How many columns show by default | Contrast |
| Whether secondary detail is shown or folded | The meaning or order of information |

Rules:

1. Density is a set of tokens: a spacing set for each level. Components read the tokens.
2. Compact is not small type. Keep body text at the platform floor or above.
3. In a compact table for a pointer, the row can be short while the row's click area stays the full row.
4. On touch, a compact row still gives each control its minimum target, through padding or spacing.
5. Fold detail before you shrink it. Show it on demand.
6. Default: four choices at one decision point, at every density.

Starting values, as rules of thumb. Set the real ones with the design system.

| Level | Row height for a pointer | Row height for touch |
| --- | --- | --- |
| Compact | About 32 px | At the touch minimum |
| Default | About 40 px | At the touch minimum or above |
| Comfortable | About 48 px | Above the touch minimum |

### 2.3 Dense data

- Numbers that are compared use tabular numerals and align on the decimal point (read: Vercel).
- Truncate text in the middle or at the end on purpose. The full value is reachable.
- A wide table scrolls inside its own container, with the first column fixed when it names the row.
- Past 50 rows, virtualize or paginate (read: Vercel).
- Show units once, in the column heading.
- Professional tools stay crisp and fast, with little motion (read: Emil Kowalski standards).

## 3. Targets

A target is the area that responds to a tap or a click, not the icon drawn inside it.

### 3.1 The defaults

| Input | Default minimum | Class | Note |
| --- | --- | --- | --- |
| Pointer on the web or the desktop | 24 by 24 CSS px, or enough spacing around a smaller target | Search: WCAG 2.2 target-size criterion at level AA. Read: Vercel | A larger target is still faster to hit |
| Touch on the web | 44 by 44 CSS px | Read: Vercel | |
| Touch on iOS | 44 by 44 pt | Search: platform guide | |
| Touch on Android | 48 by 48 dp | Search: platform accessibility help | |
| One value for every platform | 48 by 48, with 8 between targets | Rule of thumb: the stricter platform value | |

With GCH loaded, its `ux-laws` skill sets one stricter number for every touch or click target. That number governs for screens built under GCH. The table above stays valid as the GDH default elsewhere.

None of these numbers is a GDH gate. The gate is in `accessibility-gate`: every control can be operated, by pointer, by touch and by keyboard.

### 3.2 Rules

1. Extend the hit area with padding. Do not enlarge the icon.
2. Two targets never overlap. Adjacent small targets need spacing between them.
3. The whole row is the target when a row opens its item. Controls inside the row keep their own targets.
4. A label is part of its control's target. Tapping the label toggles the checkbox.
5. Put the most frequent action nearest the hand or the pointer's usual position.
6. Keep a destructive target away from the primary one.
7. Inline text links in a paragraph are exempt from the size default. Give them clear focus and enough line height.
8. Measure on the render, at the target viewport. A value in the source is not a measurement.

### 3.3 Gestures and pointers

- Gate: every gesture has a visible control that does the same thing. A swipe action also exists in a menu. A drag also exists as a move command.
- A press shows feedback at once.
- A drag can be cancelled before release.
- Hover reveals only extras. The action itself is visible, or reachable by focus.
- On the desktop, a right click adds a context menu. It does not hide the only route to an action.

## 4. Worked example

The invented inspection app.

Form. The checklist step asks 14 questions. Each is one tap: pass, fail, or not applicable. The first draft used a select for each. Three visible options replaced it. The fail option opens one note field and an optional photo. The signature field is required by the system; its error says "Sign to submit", and nothing else is lost.

Density. The technician works with gloves, one hand on a panel. Level: comfortable. Each answer button is taller than the Android default. The office web app is used all day with a pointer to compare lifts. Level: compact, with tabular numerals and a fixed first column.

Targets. The three answer buttons span the row, with spacing between them, so a gloved thumb does not hit two. The "remove photo" control sits away from "submit" and offers undo.

What was measured: target sizes on a rendered checklist at a 360 dp viewport. Label: VERIFIED in a browser at that viewport. A gloved test on a real phone: UNTESTED.

## 5. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Placeholder label | The label is gray text inside the field | A visible label above |
| Angry form | Errors appear on the first keystroke | Validate on leaving the field |
| Mute button | A disabled submit with no reason | Keep it enabled. Explain on press |
| Select for three | A dropdown that hides three options | Show the options |
| Database order | Fields in the order of the table | Order by the person's logic |
| Tiny icon target | A 16 px icon that is also the whole hit area | Pad the target |
| Density by font | "Compact" made with smaller type | Change spacing tokens, not the type floor |
| One density | A kiosk and an analyst tool share one row height | Choose from the signals in part 2.1 |
| Gesture only | An action that exists only as a swipe or a drag | Add the visible control |
| Wiped form | A failed submit returns an empty form | Keep every value |

## 6. Checks

Gates:

- Every input has a visible and a programmatic label.
- An error names the field and the fix, and keeps the input.
- Every gesture has a visible control that does the same thing.
- Every control can be operated by pointer, by touch and by keyboard.

Defaults:

- Default: targets are 24 px for a pointer, 44 px or pt for touch, 48 dp on Android.
- Default: one column; labels above fields.
- Default: mobile text inputs at 16 px or more.
- Default: density follows the signals in part 2.1 and is a token set.
