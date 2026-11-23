# Components: README and preview contract

Read this before you add a component to a pack or to a Claude Design System artifact.

## Folder

```
components/<Name>/README.md      guidelines
components/<Name>/preview.html   a live preview
```

`<Name>` is PascalCase and matches the name in code. Keep the README and the preview together. Write the README when you write the component.

## README

Write for the agent that will use the component. Keep the first sentence complete: Claude reads the first sentence of a component note before it uses the component.

1. First sentence: what the component is and when to use it.
2. When not to use it, and what to use instead.
3. What the consumer provides: props, children, container and data.
4. Variants and sizes, with the token each one uses.
5. States it supports.
6. Accessibility: role, keyboard keys, label and focus order.
7. Copy rules: casing, length and tone of the label.

## Preview

- The file is one HTML document. It loads the system's stylesheet and takes every value from the tokens.
- For a Claude Design System artifact, line 1 is an HTML comment that holds `@dsCard group="<Group>" height=<N>`. The page builds its card index from that line. `N` is the card height in pixels.
- Show every state side by side, with a short label for each.
- Use real copy from the brand book. Do not use placeholder text.
- Show each theme, or let the page theme switch reach the preview.
- Keep the preview static unless the component needs script to show a state.

## States to show

Show each state that applies:

| State | Show |
| --- | --- |
| Default | The resting look |
| Hover | Pointer feedback |
| Focus | A visible focus ring at 3:1 against its ground |
| Active or selected | The pressed or chosen look |
| Disabled | Lower emphasis, with the reason available in text |
| Error | The message, the icon or word, and the field outline |
| Loading | The skeleton or the progress mark |
| Empty | The message and the next action |

Contrast rises on hover, active and focus. It never falls.

## Readiness checks

1. The component has a name, a description, a use rule, a rendered example and code.
2. Every state that applies is in the preview.
3. The component renders alone and nests inside others.
4. It has more than one documented use.
5. No raw color, size or duration: `ds.py audit components/<Name>` reports zero raw literals.
6. It works with the keyboard and at phone width.
7. The list of components in code equals the list in `components/`.
8. No component name carries a number suffix or the words new or old.

## Bundled components in a Claude artifact

Evidence: DOCUMENTED, UNTESTED. Read from the type's reference files; no bundle was built in the session that produced this skill.

- A system may ship `components/bundle.js`, `bundle.css`, `index.d.ts` and packed libraries under `components/lib/`.
- The bundle is one classic script. It assigns one global: `window.<Namespace>`.
- The README of the system names that global. A canvas then mounts the real component instead of a look-alike.
- GATE: building a bundle runs the package's build. Ask the owner before you run it.
- Without a build, ship the read-only route: a README and a static preview for each component.

## Sources

- Claude Design System artifact type: skill, format and from-code references, read 2026-11-23.
- Design Systems Handbook (InVision DesignBetter), chapter 2 "Creating a user interface library", chapter 3 "Reusable" and "Maintaining documentation".
