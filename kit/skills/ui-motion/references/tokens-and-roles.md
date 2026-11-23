# Motion tokens and roles

Read this file at steps 5 and 6 of `ui-motion`. It covers the four roles, how to map an existing brand token set to them, a starter set when none exists, the token file shape, signature motions and the motion section of `DESIGN.md`.

Evidence. The role split applies the GDH resolution of conflict 4 (brand motion tokens against short interface motion). The brand examples are real token sets seen in owner design systems on 2026-11-23, shown here without names. The Material 3 values are partly from search and partly from memory. The token shape follows the Design Tokens Format Module 2025.10, read 2026-11-23. Every number is a default.

## 1. The four roles

A role says where a token may be used. A brand token keeps its value; the role limits its reach.

| Role | Covers | Who decides the value | Default range |
| --- | --- | --- | --- |
| control | Press, hover, toggle, checkbox, small popover, tooltip | GDH defaults unless the design system sets a control value | 100 to 200 ms |
| surface | Dropdown, select, dialog, drawer, sheet, toast, accordion | The design system, else the element table | 150 to 500 ms |
| page | Route change, view transition, large layout shift, hero entrance | The design system first | 300 to 600 ms |
| flourish | Rare brand moments: onboarding, first success, launch | The design system only | No default. Ask. |

Rules:

1. Brand tokens win for the page and flourish roles.
2. Control motion stays short even when the brand's standard token is longer. Ask before you put a long brand token on a control.
3. A surface takes the brand token when it falls inside the surface range. Outside it, ask.
4. Never write a raw millisecond value or a raw curve in a component. Name a token.
5. A token with no role is unfinished. Assign one before the build.

## 2. Mapping an existing brand set

Read the brand's durations and curves. Sort them by value. Assign each to a role by its value and by the brand's own notes.

The examples below are invented. Their values are round numbers chosen to show the method. They describe no real brand.

Example A: a retail brand with four durations and one curve, and a rule of no springs.

| Brand token | Value | Role | Note |
| --- | --- | --- | --- |
| quick | 150 ms | control | Fits the control range |
| standard | 300 ms | surface | Dialogs, drawers, menus |
| page | 500 ms | page | Route changes, hero entrance |
| flourish | 1000 ms | flourish | Rare brand moments only |
| ease | an ease-out curve | all | One curve for every role |

Example B: a software studio brand with a range of 100 to 500 ms, a strong ease-out curve and a 10 s ambient loop.

| Brand token | Role | Note |
| --- | --- | --- |
| 100 to 150 ms steps | control | Press and hover |
| 200 to 400 ms steps | surface | |
| 500 ms | page | |
| 10 s ambient loop | flourish | A loop: it needs a pause control, an off-screen pause and a reduced-motion stop |

Example C: a food producer brand with 150, 250 and 400 ms, ease-out, and a rule of no springs and no parallax.

| Brand token | Role |
| --- | --- |
| 150 ms | control |
| 250 ms | surface (small) |
| 400 ms | surface (large) and page |
| none | flourish: ask the user; the brand defines none |

What the three have in common: short ease-out motion and no springs. Treat that as the brand's character, not as a gap to fill.

## 3. A starter set when none exists

ASK the user to approve this set or adjust it. Store it through `design-system`.

| Token | Value | Role |
| --- | --- | --- |
| `motion.duration.control` | 150 ms | control |
| `motion.duration.surface` | 250 ms | surface |
| `motion.duration.surface-large` | 400 ms | surface |
| `motion.duration.page` | 500 ms | page |
| `motion.ease.out` | `cubic-bezier(0.23, 1, 0.32, 1)` | entering, most exits |
| `motion.ease.in-out` | `cubic-bezier(0.77, 0, 0.175, 1)` | moving on screen |
| `motion.ease.drawer` | `cubic-bezier(0.32, 0.72, 0, 1)` | sheets and drawers |

Default: the three curves come from published animation review standards, read 2026-11-23. The durations sit inside the element table of `timing-and-easing.md`.

Alternative reference values, labelled UNTESTED: Material 3 lists short durations from 50 to 200 ms, medium 250 to 400 ms, long 450 to 600 ms and extra-long 700 to 1000 ms, and a standard curve `cubic-bezier(0.2, 0, 0, 1)`. Only four of those durations and the curve were confirmed by search. Read the Material page before you rely on them.

Adjust the set to the environment line:

| Environment | Change |
| --- | --- |
| Calm | Keep durations at the upper end of each row. Use no spring. |
| Precise, expert | Lower each duration by about a quarter. Drop the page token for most routes. |
| Playful | Add a spring token for gestures only, if the design system allows springs. |

## 4. The token file shape

Write durations and curves in the Design Tokens Format Module object forms. `design-system` owns the file and its validation.

```json
{
  "motion": {
    "duration": {
      "control": { "$type": "duration", "$value": { "value": 150, "unit": "ms" },
                   "$description": "Role: control. Press, hover, toggle." },
      "surface": { "$type": "duration", "$value": { "value": 250, "unit": "ms" },
                   "$description": "Role: surface. Menus, small dialogs, toasts." }
    },
    "ease": {
      "out": { "$type": "cubicBezier", "$value": [0.23, 1, 0.32, 1],
               "$description": "Entering and exiting elements." }
    }
  }
}
```

Name a curve by its job (`ease.out`, `ease.drawer`), not by its math. Put the role in the description. When the project uses the Claude Design System list shape, write one entry per token with `name`, `value` and `usage`, and put the role in `usage`.

CSS output, generated through `design-system`:

```css
:root {
  --motion-duration-control: 150ms;
  --motion-duration-surface: 250ms;
  --motion-ease-out: cubic-bezier(0.23, 1, 0.32, 1);
}
```

## 5. Springs as tokens

1. Read the design system first. When it says "no springs", write no spring token.
2. With no rule, add a spring token only for gesture-driven or interruptible motion.
3. Default spring: duration 0.5 s and bounce 0.2, from the review standards. Keep bounce between 0.1 and 0.3.
4. A spring token states its role in its description: "gesture: sheet drag release".
5. A spring never applies to opacity or color.

## 6. Signature motions

A signature motion carries the brand. It is brighter than function needs, and it appears only where the brand allows.

Rules:

1. Default: three to five signature motions in a product.
2. Each has a name, a role (page or flourish), the moments where it may appear, and a reduced-motion form.
3. Each appears at least once, and nowhere outside its listed places.
4. A signature motion is never on a control used daily.

Example row for `DESIGN.md`:

| Name | Role | Allowed at | Reduced motion |
| --- | --- | --- | --- |
| Bloom reveal | flourish | First project created; plan upgraded | A cross-fade of the same content |

## 7. The motion section of DESIGN.md

Write these parts. Keep each short.

1. Principles: three to five, each with one sentence of reason and one example. Write them in the brand's own voice.
2. The environment line.
3. The token table with roles.
4. Guidance per interaction type: feedback, hints, hierarchy, relationships between elements, navigation. One do and one do-not for each.
5. Signature motions with their allowed places.
6. Differences by user role or context, when the product has them.
7. Reduced-motion rules.
8. A change log. Each logged exception becomes a new token, a new rule or a recorded rejection.

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| One duration for everything | Every motion uses 300 ms | Several steps by role; small and near is shorter |
| Long brand token on controls | Buttons take 600 ms because the brand standard says so | Map the token to the page role; keep controls short |
| Raw values | `transition: transform 0.35s` in a component | A named token with a role |
| Invented flourish | A brand with no flourish gets confetti | Ask; the brand may want none |
| Springs smuggled in | A library default adds overshoot | Override the library default with the token |
| Token sprawl | Twelve durations for one product | Four to six durations; merge near values |
