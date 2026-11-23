# Craft of the Design System type

Read this file at step 12 of `claude-design` when the type is Design System. It restates what makes a hosted design system usable by the other types. Building, validating and publishing belong to `design-system`; this file is the craft standard that skill writes to.

Evidence. Rules come from the Design System type's rule file and its format, craft, cover and from-code references, read 2026-11-23: DOCUMENTED. The Help Center and the Academy design system tutorial were read the same day. No system was published for this kit: UNTESTED.

Terms. The brand book is the system's `README.md` plus other section files. A consumer is any type or agent that reads the system.

## 1. What a consumer reads, and in what order

1. Every consumer reads the README first, then `tokens.json`.
2. The reader takes the overview every time, then only the parts the task needs.
3. A reader reads the first sentence of a component's usage note before it uses the component.

So: keep the overview short. Put per-component rules in each component's usage note, first sentence first.

## 2. The brand book is usage rules

1. Write imperative sentences that name tokens, styles and assets.
2. No title, no provenance, no next steps. Those belong in `SOURCE.md` in the pack.
3. Length follows the source. A rich source gets three groups of sections:
   - Content: tone, casing, person, emoji policy, real copy examples.
   - Visual foundations: color, type, spacing, imagery, motion, states, borders, shadows, radii, layout.
   - Iconography.
4. To change future output, edit the usage note. A chat instruction does not persist.

Example usage sentences:

- "Use `accent` for the one primary action in a view. Never for text under 18 px."
- "Set body text in `body` on `bg` or `surface`. Never on `accent`."

## 3. The source defines the inventory

1. List the full inventory of the source first: tokens, styles, components, assets. Track against it.
2. Use the source's real token names, values and order.
3. Build only the component families the source has. Report what remains.
4. Exact values: the source beats any library it resembles. A 5 px radius stays 5 px. Code is truth; screenshots are lossy.
5. One source for every value. A value in `tokens.json` is removed from the stylesheets that previews load.

## 4. Tokens that the page can read

- `color` holds a list of themes and a list of tokens. Each token has a name, a value and a usage note. A value is a string or one value per theme. An alias names another token.
- `type` holds fonts, families and groups of styles.
- Every other family is a list of tokens.
- A name-to-value map (DTCG style) is valid JSON that the page cannot read. The family shows empty, and its entries are lost at the first edit. Convert maps to lists.
- Values that drop: named colors, `var()`, `color-mix()`, an alias of a missing token.
- There is no motion family. Record motion in the README and in the pack's `DESIGN.md`.
- The type caps themes, colors, families, styles and tokens per family. Read the caps in the card before a large system.

`ds.py validate` enforces this grammar on the pack before publish. See `design-system`.

## 5. Notes, themes and accessibility

1. Every token and every asset carries a usage note.
2. A text color's note names the grounds it reads on. `ds.py contrast` reads pairs from those notes.
3. Each text-on-ground pair holds 4.5:1 in every theme; large text, borders, focus rings and icons hold 3:1.
4. A real source's failing pair stays exact and is flagged in its note.
5. A high-contrast theme is an added theme at 7:1.
6. Color-blind-safe status colors carry a word or an icon. With no brand hues to keep, start from the Okabe-Ito set.
7. Fill every theme. Wire the type scale to real font files.

## 6. Components

1. Each component folder holds a usage README and a live preview. The first line of the preview declares its card group and height.
2. The usage README says what the consumer provides: props, children, container, data. Then when to use it.
3. A built bundle assigns one global namespace. The canvas mounts components from it.
4. Build two or three components, save, then build the rest.
5. A component a person made is moved aside, never deleted.

## 7. The cover

| Part | Rule |
| --- | --- |
| Size | A fixed width and a short height; the card gives both |
| Color blocks | Three to five large blocks in identity colors at full value, a quarter to half of the cover |
| Pattern | One pattern drawn from what the system says about itself |
| Name | The display face, bottom left, with one tagline line |
| Geometry | Sides from spacing tokens; corners from radius tokens |

Tests: squint, and the name reads first, then color, then pattern. Cover the name: blocks and pattern still identify the brand. Avoid a row of equal squares, a barcode of thin rules, confetti, words on blocks, and any motion.

## 8. Assets

1. Copy assets; never approximate them.
2. No logo in the sources: the name in plain type plus a note. Never redraw a mark from memory.
3. Fonts need files. A named font with no file is replaced in every consumer.
4. Assets go up as uploads with a usage note and a license on record.

## 9. Building from code or from a design tool

| Source | Route |
| --- | --- |
| A repository | Read-only clone or connector. Custom properties or a token file become `tokens.json`. Components are built (with the user's yes) or read-only (README and static preview). Provenance goes in the token metadata and the index. A re-sync merges and keeps prose. |
| A design tool file | One file link is enough. Traverse the whole file. Variables become one theme. Fonts do not come through; ask for them. Keep one "not synced" note in the README. |

A system kept by a code sync is read-only on its page. Change the code, then sync again. See [out-to-code-and-partners.md](out-to-code-and-partners.md), section on sync.

## 10. Clean-up and revision

1. Revise file by file. Never rebuild a whole system.
2. A clean-up deletes only the type's three record files. Any other file moves to `project/archived/`.
3. The final message lists DELETED, MOVED ASIDE and SAFE TO DELETE.

## 11. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Empty family | The page shows no colors | The tokens were a map. Convert to lists. |
| Brand book as history | README tells how the system was made | Move history to `SOURCE.md`; write usage rules |
| Snapped values | 5 px became 4 px | Restore the source value |
| AI tropes | Blue-purple gradient, decorative emoji, left-border cards, filler stats | Remove unless the source has them |
| Invented component | A family the source never had | Remove it; list it as a gap |

## 12. Check

- The README is usage rules and names real tokens.
- Every token, style and asset has a usage note.
- Every theme is filled; contrast passes or failures are flagged.
- Font files exist for every listed font.
- The cover exists and its geometry uses tokens.
- Nothing a person made was deleted.
