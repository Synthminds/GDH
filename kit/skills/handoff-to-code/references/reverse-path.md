# The reverse path: from code to a design system or a design tool

Read this file at step 20 of `handoff-to-code`. It covers what to do when code leads: pulling tokens and components out of a codebase into a design system, pushing a built page into a design tool for a designer, and keeping the two in step afterwards.

Evidence. The audit and conversion commands were run on 2026-11-23: VERIFIED for the scripts. The design-tool routes come from tool descriptions and the Design System type's from-code reference: DOCUMENTED. No reverse run on a real product was done for this kit: UNTESTED.

Terms. Code leads when the product exists and holds the truth. The visual inventory is the count of raw values in the code. A round trip is code to design and back.

## 1. When to use the reverse path

| Situation | Route |
| --- | --- |
| A product exists, no design system | Extract tokens from code; build the system |
| A new design must fit an existing library | Pull the current tokens and components first |
| A designer wants to refine a built page by hand | Push the page into a design tool |
| A component library and a hosted design system must stay in step | A code sync through `design-system` |
| The build diverged from the package | Audit the build; decide which side wins |

## 2. Code to a design system

The `design-system` skill owns this, with its from-code protocol. This skill calls it and takes the result back into the package.

1. Run the visual inventory: `$DS audit <src> --inventory`. Record raw colors, sizes, radii and durations.
2. Find the token sources: custom properties, a theme file, a token file.
3. Convert: `$DS from-css <css files> --name "<Name>" -o design/tokens.json`. For a W3C token file: `$DS from-dtcg <file> -o design/tokens.json`.
4. Read the converter's report of what it could not convert. Resolve each by hand.
5. Write usage notes. Run `$DS validate` and `$DS contrast`.
6. Cluster near-duplicate raw values from the inventory into tokens. ASK the owner before merging two values.
7. Generate `design/tokens.css` and `DESIGN.md`.
8. Map each code component to the inventory format in [components-and-states.md](components-and-states.md): status `reuse`.
9. Re-run the audit with `--tokens design/tokens.json`. The count of literals with no token is the debt to pay down.

Code is truth here: exact values from the source, no snapping to a grid. A screenshot is lossy and never the source.

## 3. Code to a design tool

For a designer who refines on a canvas.

| Need | Capability | Example card | What comes across | What is lost |
| --- | --- | --- | --- | --- |
| Editable layers from a page | `code-to-design` | [figma](../../../references/tools/figma.md) | Plain layers from self-contained HTML | Components, variables and libraries |
| A runnable code layer | `code-to-design` | [figma](../../../references/tools/figma.md) | The code as a layer | Design shapes |
| A canvas in Claude from a page | `canvas` | [claude-design](../../../references/tools/claude-design.md) | Artboards rebuilt from the source | Runtime behavior |
| A component library into a hosted system | `code-to-design` | [design-sync](../../../references/tools/design-sync.md) | Components, tokens | Prose the sync does not own |

Procedure:

1. GATE: the page leaves the project. Ask first and name the target.
2. Read the tool's card. Call its first call. Some writes cannot be replaced once done: read the card's limits.
3. Export a self-contained HTML of the page: inline styles from the tokens, images inlined or as allowed by the card.
4. Ask the user whether they want editable design layers or a code layer, when the card offers both.
5. Push. Record the target link and what did not carry over.
6. When the designer finishes, bring changes back as token or component changes through `design-system`, never as pasted values.

## 4. Keep code and design in step

1. Decide which side is the source of truth, per item: tokens, components, copy. Record it in section 2 of `design/handoff.md`.
2. A hosted system kept by a code sync is read-only on its page. Change the code, then sync again.
3. After any change, compare `design/tokens.json` with the code's tokens. A difference is a finding: ask which wins.
4. Re-run the audit at each sync point. The literal count must not rise.

## 5. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Screenshot extraction | Colors picked from an image | Read the source code |
| Grid snapping | 5 px became 4 px | Keep exact values; ask before merging |
| One-way trip | Designer edits never return to code | Return changes as token or component changes |
| Two masters | Code and design both edited, nobody decides | Record the source of truth per item |
| Lost components | Pushed layers have no component link | Say what was lost; keep the library as the truth |

## 6. Worked example

A product has 41 distinct greys in its CSS and no tokens.

1. `$DS audit src --inventory` lists 41 greys, 17 font sizes and 9 radii.
2. `$DS from-css src/styles/vars.css --name "Product" -o design/tokens.json` converts 12 custom properties.
3. The 41 greys cluster into 6 roles. The owner accepts the merge of 35 near-duplicates.
4. `$DS audit src --tokens design/tokens.json` shows 210 literals with no token. That number goes in the package as debt with an owner.
5. The new design for the settings area builds only on the 6 grey tokens. The handoff lists the difference only.
