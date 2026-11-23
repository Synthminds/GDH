# Components and states

Read this file at steps 10 and 13 of `website-design`. It gives the order in which to source a component, the reference rule, the state matrix and the form rules.

License and fetch detail belongs to `find-assets`. This file covers the design decisions.

## 1. Sourcing order

Search in this order. Stop at the first tier that meets the need. Record the result of each search in `site-plan.md`.

| Tier | Where to look | What you may do | Record |
| --- | --- | --- | --- |
| 1 | The project: the component folder, `DESIGN.md`, the design system bundle | Reuse as it is. Extend through its props | "Reused: name" |
| 2 | The design system named in `DESIGN.md`, when the project does not yet hold the component | Add the system's own component | "Added from system: name" |
| 3 | The catalog, by capability `ui-components` | Study it as a reference. Re-implement with project tokens and primitives | Credit: author, URL, what was learned |
| 4 | Nothing fits | Build a new component | "New: name", with the reason no tier fit |

Example cards for tier 3: [21st-dev](../../../references/tools/21st-dev.md), [getlayers](../../../references/tools/getlayers.md), [dam](../../../references/tools/dam.md). Pick a tool by capability, confirm it is present, and read its card first.

Decision rules:

1. Search tier 1 before every new component. A second button component is a defect.
2. Prefer unstyled primitives with correct behavior when the brand words ask for a distinct look.
3. A styled kit brings its own look. Map every value to a project token before the first review.
4. Default: one animated effect component in a view. A second one needs a reason from the brief.
5. Add no dependency that the task does not need. Name the need for each one you add.
6. GATE: a metered retrieval of component source is a spend call. Shortlist from free metadata. Ask before the call.

## 2. The reference rule

Kernel rule 10: reference, credit, re-implement.

What you take from a reference:

- Structure: which parts exist and how they nest.
- Technique: how the effect or the behavior works.
- States: which states the author handled.

What you do not take:

- The code, unless the item's own license allows it and the user agrees. Then `find-assets` records it.
- The look as a whole: palette, type, spacing and motion together.
- Any asset inside it: a font, an icon, an image.

How to re-implement:

1. Write down what the component must do, in your own words.
2. Build it from the project's primitives and tokens.
3. Change at least the layout or the motion. A popular component unchanged makes the page look like other pages.
4. Write a credit line: source, author, URL, date, and what was learned.
5. A marketplace item with no stated license is a credited reference. It is never vendored.

Direct install is an exception. It needs a license read by `find-assets`, a diff read after the install, and the user's recorded yes.

## 3. New or reuse

Apply this test before a new component.

| Question | Yes means |
| --- | --- |
| Does an existing component do this job with a prop or a slot? | Reuse it |
| Does the need differ only in look? | Add a variant, not a component |
| Will it appear in two or more places? | A component is justified |
| Is it one use, and special to one page? | Build it in the page. Do not add it to the library |

Record the answer. A repeated correction becomes a rule in `DESIGN.md`.

## 4. The state matrix

Design every state before the build is called done. A state that is not designed gets designed by accident.

### Controls

| State | Applies to | Rule |
| --- | --- | --- |
| Default | All | The resting look |
| Hover | Pointer devices only | Gate with `@media (hover: hover)`. Contrast rises, never falls |
| Focus-visible | All | A visible ring that meets 3:1 against adjacent colors. Never remove an outline without a replacement |
| Active or pressed | Buttons, links | Immediate feedback |
| Selected or current | Tabs, navigation, toggles | Marked by more than color |
| Disabled | Controls that can be unavailable | Say why nearby. Prefer an enabled control with an explained error |
| Loading or pending | Controls that start work | Keep the label. Keep the size. Block a second submit |

### Content regions

| State | Rule |
| --- | --- |
| Loading | A skeleton that matches the final layout, so nothing shifts |
| Empty | Say what will appear here and offer the next action |
| Error | Say what failed and how to retry. Keep what the visitor typed |
| Partial | Show what loaded. Mark what is missing |
| Long content | The longest heading, a long word, a long list. Wrap or truncate on purpose |
| Short content | One item, one word. The layout must not collapse or look broken |
| Missing image | A reserved box with the token ground. Alt text still present |

### Forms

| State | Rule |
| --- | --- |
| Pristine | Visible labels. Help text where a format is needed |
| Invalid, inline | The message sits next to the field. It names the problem and the fix |
| Submitting | The button shows progress. Input stays as typed |
| Success | Confirm what happened and what happens next |
| Server error | Keep every value. Focus moves to the first problem |

### Page level

| State | Rule |
| --- | --- |
| Not found | A real page with navigation and a way forward |
| Server error | Plain words and a retry |
| Script blocked or failed | Content and navigation still readable |
| Consent banner | Designed in the system. It never covers the primary action without a way to dismiss |
| Slow network | The first view is useful before images arrive |
| Reduced motion | Movement removed. Opacity and color changes may stay |
| Each theme | Every state above, checked again in each theme |

State spec format for `site-plan.md` and for the handoff:

```
<component or region> | states: <list> | missing: <list or none> | note: <what changes in each>
```

## 5. Forms

These rules come from the Vercel Web Interface Guidelines, read during the research. They are number-free, so they hold as defaults that the design system may refine.

1. Every input has a visible label. A placeholder is not a label.
2. Set the correct `type`, `inputmode` and `autocomplete`. Password managers and autofill must work.
3. Never block paste.
4. Validate on blur or on submit. Do not show an error while the visitor is still typing the first time.
5. The Enter key submits a single-field form.
6. On a failed submit, focus the first invalid field and announce the error.
7. Keep every typed value after an error.
8. Ask only for what the job needs. Each removed field raises completion. Confirm required fields with the code owner.
9. Default: inputs are 16 px or more on mobile web, so the phone does not zoom on focus (read: Vercel).
10. Say what happens after the form is sent, before the visitor sends it.

## 6. Links and navigation behavior

- A link is an anchor element with a real address. A `div` with a click handler is not a link.
- A button does something on the page. A link goes somewhere. Do not swap them.
- The address reflects state: the open tab, the filters, the page of a list.
- The Back button restores the scroll position.
- A destructive action asks first or offers undo.
- No dead end: every state offers a next step.

## 7. Worked choice

The invented repair shop needs a booking form and a filterable model list. The project is a static site with tokens and no component library.

- Tier 1: no components exist.
- Tier 2: `DESIGN.md` names no library.
- Tier 3: a catalog search returns several filter bars with previews. Their structure helps: a search field, maker chips, a count of results.
- Decision: build both from native elements. Native `input`, `select` and `details` give keyboard behavior at no cost. The catalog items are credited as structure references only.
- Change from the reference: the chips became a plain list of maker links. Each link has a real address, so a filtered view can be shared.
- States listed: the list has loading, empty ("No models match. Tell us your model"), long (a maker with forty models) and script-blocked (the full list shows).
- Nothing was retrieved for a fee. No spend call ran.

## 8. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Happy path only | The default state is polished; error and empty do not exist | Fill the matrix |
| Kit look | Default radius, default neutral palette, unchanged spacing | Map each value to a token |
| Second kit | Two styled libraries in one site | Choose one. Record why |
| Marketplace default | The first search result, unchanged | Judge fit. Re-implement. Change layout or motion |
| Placeholder as label | Gray text inside the input and no label | Add a visible label |
| Click div | A `div` or `span` that acts as a link or a button | Use the native element |
| Lost input | An error clears the form | Keep every value |
| Skeleton mismatch | The loader has a different layout from the content | Match the final layout |

## 9. Checks

Gates:

- Each component has a recorded sourcing tier and, for tier 3, a credit line.
- No copied marketplace code ships without a read license and a recorded yes.
- Every row of the state matrix that applies is designed, in every theme.
- Every input has a programmatic label. An error keeps the input.

Defaults:

- Default: one effect component in a view.
- Default: mobile inputs at 16 px or more.
- Default: a hover style applies only where hover exists.
