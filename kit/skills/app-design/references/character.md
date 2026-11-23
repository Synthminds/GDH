# Product character

Read this file at step 11 of `app-design`, before the first high-fidelity screen. It covers where an app's character lives, how to restyle a component library away from its stock look, the swap test for screens, a worked example and the failure patterns.

Evidence. The rule "derive each choice from the subject" comes from the Anthropic frontend-design skill and the Impeccable craft notes, read 2026-11-23. The list of places where character lives is GDH method, written for this kit. Treat it as a default. A screen is UNTESTED for character until a second person runs the swap test on it.

Terms. Character is the set of visible choices that make the product its own. A stock look is the theme a component library ships with, before any token is changed. An open choice is a choice that no higher source fixes (see kernel rule 1).

## 1. Where an app's character lives

A product screen has less room for a hero image or a display face than a web page. Its character lives in the parts that people use every day.

| Place | What to decide | Trace it to |
| --- | --- | --- |
| Signature interaction | One action that only this product has, and how it looks and moves | The primary job in the brief |
| First run | What the first screen shows before the user has data | The use context and the brand words |
| Empty states | The words and the picture when a list holds nothing yet | The voice in `DESIGN.md` |
| Data presentation | How the main numbers, times or units are set | The subject's own documents and instruments |
| Iconography | Stroke, corner, fill, metaphor | Objects from the subject's world |
| Copy voice | Button labels, errors, confirmations | The voice and the brand words |
| Density | How much fits on one screen | The reading mode: glance, scan or work |
| Motion | The one moment that moves with intent | The signature interaction, through `ui-motion` |

Rules:

1. Pick one signature interaction. Design it first. Every other screen can stay quiet.
2. Write the first-run screen and the empty states in the product voice. They are where people meet the product.
3. Set the main data like the subject sets it. A tide table, a lab result and a sports score each have their own form.
4. Draw or choose icons that share one construction. A mixed icon set reads as stock.
5. Change only open choices. A platform convention stays unless the user or the design system asks to change it.

## 2. Restyle the component library

A component library saves build time. Its stock theme is common, so a screen that keeps it looks like many other screens.

Do this before the first review:

1. Map every library variable to a project token from `design/tokens.json`. Leave no stock value in place.
2. Set the radius, the border weight and the shadow from the design system. Do not keep the library's values by default.
3. Set the type scale and the families from the design system. Check numerals in tables.
4. Replace the stock focus ring with the token focus style. Keep it visible at 3:1 or more.
5. Replace the library's default icon set when the subject calls for another construction.
6. Keep the library's behavior, keyboard support and states. Change the look, not the controls.

Default: a screen in a library's stock theme is a finding in `design-critique` when the design system leaves the theme open.

## 3. The swap test for screens

Run it on each open choice in the key screens: the first run, the signature interaction, one dense screen and one empty state.

1. Put a competitor's name and data on the screen.
2. Ask: does the screen still fit the competitor unchanged?
3. A "yes" means the choice does not come from the subject. Choose again from section 1.
4. Record each choice that failed and the new choice in `design/decisions.md`.

The swap test is a default, not a gate. It applies to open choices only. A choice that the user, the design system or the brief requires passes as `brand-required`.

## 4. Worked example: a tide app for small-boat sailors

The brief: a mobile app that tells a sailor when the water is deep enough to leave the dock. Brand words: calm, exact, weathered. Primary job: "Can I leave at 14:00?"

| Place | Generic choice | Choice traced to the subject |
| --- | --- | --- |
| Signature interaction | A card list of tide times | A drag along a tide curve that shows depth at the dock for each minute |
| First run | A welcome carousel | The nearest harbor's curve for today, with one question: "Which dock?" |
| Empty state | A cheerful illustration and "Nothing here yet" | A flat chart line and "No saved docks. Add the one you leave from." |
| Data presentation | Large rounded numbers | Tabular figures set like an almanac column, depth in meters with the unit |
| Iconography | The library's stock outline icons | A small set drawn from chart symbols: buoy, depth sounding, harbor light |
| Motion | Cards that fade in | The tide line draws once on first open, then stays still |

The component library stays. Its tokens change: the radius drops to the pack's small value, the shadows go flat, and the numerals switch to tabular.

## 5. Failure patterns

- **Stock theme shipped.** The library's default radius, gray and focus ring reach the review. Fix: map every variable to a token (section 2).
- **Character in the wrong place.** A gradient hero on the login screen, and stock screens after it. Fix: put the effort into the signature interaction and the empty states.
- **Decoration for its own sake.** An illustration that does not come from the subject. Fix: trace it to the brief, or remove it.
- **Convention broken for style.** A custom tab bar that hides the platform's back gesture. Fix: keep the convention; change the look through tokens.
- **Every screen loud.** Each screen tries to be the signature. Fix: one signature interaction; quiet screens around it.

## Sources

- Anthropic, frontend-design skill: subject-first choices and the list of generic looks. Read 2026-11-23.
- Impeccable, craft notes and design tells. Read 2026-11-23.
