---
name: logo-identity
description: Takes a logo from a brief to a tested vector system. Use for a new mark or wordmark, a refresh, or the system around an approved mark. Covers discovery, word maps, many rough concepts in black, and vector construction with optical correction. Covers the lockups, clear space, minimum size and the reproduction test suite. Adds color and motion versions, and the file set with favicon and app icon. Writes the usage sheet with a misuse list. Runs a trademark knockout search and states its limits.
disable-model-invocation: true
argument-hint: "[new | refresh | system | files] <brand name>"
---

# Logo and identity

This skill takes a mark from a brief to a tested vector system: lockups, rules, files and a usage sheet. The idea is found in black, at small size, before any refinement.

Boundary. It writes no brand strategy and invents no name; the user supplies both. `color` builds the palette. `typography` chooses the type system. `design-system` stores tokens and the brand book. `find-assets` reads licenses and runs outside searches. `ui-motion` and `motion-video` build motion. A trademark attorney clears a mark; this skill does not.

## Before you start

1. Read `DESIGN.md`, `design/brief.md`, `design/decisions.md` and `design/assets/manifest.json` when they exist.
2. Precedence: user instruction, then the project design system, then the brief, then GDH defaults.
3. An existing logo is a file to copy, never a mark to redraw. Change it only in the `refresh` mode, with the owner's yes.
4. No confirmed brief: stop and run `align` first.
5. Pick the mode: `new`, `refresh`, `system` (rules and files for an approved mark) or `files` (exports only).
6. Collect: the exact name, the places the mark must work, competitors, the decider, the budget for paid generation.

Terms. A mark is the symbol. A wordmark is the name in drawn letters. A lockup is one fixed arrangement of mark and wordmark. The master is the vector file that every export comes from.

## Procedure

1. Run discovery. Write the logo lines of the brief. Read [references/discovery-and-word-maps.md](references/discovery-and-word-maps.md).
2. Build the competitor sheet as references with source notes. It never ships.
3. Decide the type of mark: wordmark, lettermark, symbol with wordmark, or emblem.
4. Build word maps from the name and the brand words. List twenty visual seeds or more.
5. Draw many rough concepts in black on white, at thumbnail size. Default: thirty or more, across five ideas or more. Read [references/concepts.md](references/concepts.md).
6. GATE: generated concepts are a spend call and are for ideation only. Quote, show, get a yes, call once. Read [references/generation-and-vector-route.md](references/generation-and-vector-route.md).
7. Cull to three mark concepts that differ in idea. They work inside the brand direction chosen in `mood-board`, when one exists. Judge each as appropriate, distinctive and simple.
8. ASK: show the three in black, at the same sizes and in the same contexts. Ask keep, change or remove for each part. The user chooses one mark.
9. Redraw the chosen mark as a clean vector. Apply optical corrections. Read [references/construction.md](references/construction.md).
10. Run the black tests of the suite. Fix and rerun. Read [references/test-suite.md](references/test-suite.md).
11. Build the lockups: primary, stacked, mark only, wordmark only, favicon. Define clear space and minimum sizes. Read [references/lockups-and-versions.md](references/lockups-and-versions.md).
12. Run the trademark knockout search. Read [references/trademark-screening.md](references/trademark-screening.md).
13. GATE: an image search uploads the unreleased mark. Ask first. State that the result is not legal advice. The user confirms with counsel.
14. Add color last, through `color`. Run the greyscale and on-photo tests. Add a motion version only on request.
15. Export the file set and record each file. Read [references/deliverables.md](references/deliverables.md).
16. Write the usage sheet with the misuse list. Read [references/usage-sheet.md](references/usage-sheet.md).
17. ASK for final approval. Record the round in `design/decisions.md`. Close with the report in Output.

## Tools

Capabilities, in preference order: `vector`, `image-gen`, `image-edit`, `fonts`, `logo-search`, `canvas`. Vocabulary: [capabilities.json](../../catalogs/capabilities.json).

- `vector`: hand-written SVG is the first route and needs no tool. A vector tool converts or cleans. Example cards: [adobe](../../references/tools/adobe.md), [figma](../../references/tools/figma.md).
- `image-gen`: concept candidates only, inside the tool's own brand workflow. Example card: [higgsfield](../../references/tools/higgsfield.md).
- `logo-search`: looks up existing third-party marks for the competitor sheet. It designs nothing. Example card: [21st-dev](../../references/tools/21st-dev.md).
- `canvas`: concept boards and the usage sheet. Example card: [claude-design](../../references/tools/claude-design.md).

Pick the tool by kernel rule 8. Read its card before the first call. Read prices live. With no tool, write the SVG by hand and export with the vector tools in `kit/catalogs/assets.json`, through `find-assets`.

## Checks

Gates. Each one blocks delivery.

1. One color: the mark works in solid black. No gradient, tint, opacity or effect carries the idea.
2. Reversed: the mark works in white on black and on the brand color.
3. Tiny size: each lockup is recognizable at the minimum size the usage sheet states.
4. Greyscale: the color version keeps its parts distinct in greyscale.
5. On photo: the sheet states the version and the backing for a photo. The mark reads on a light, a dark and a busy image.
6. The master is a vector with clean paths. No raster logo is delivered as the master.
7. No stock icon, no traced third-party mark and no generated raster is in the mark. Each generated concept was redrawn.
8. The license of a typeface used in the wordmark allows logo use. The record is in the manifest.
9. Clear space and minimum size are defined from a part of the mark.
10. The competitor sheet test passed: the mark is not confused with a competitor's mark.
11. The knockout search ran and its limits are stated, or the user declined it and the record says so.
12. Every file has a manifest record with its origin: own or generated.
13. Nothing was uploaded, shared or published without the user's yes.

Defaults. The user, the design system or the brief can replace each one.

- Default: three mark concepts. Two when brand rules are strict. Four at most.
- Default: test the favicon at 16px and the lockup at 20mm wide in print.
- Default: for embroidery, no stroke under 1mm and no text under 5mm. Confirm with the vendor.
- Default: clear space equals the cap height of the wordmark on every side.
- Default: overshoot of round shapes is 1 to 3% of the height.
- Default: the doodle test. A person can sketch the mark after a ten-second look.
- Default: favicon set: an SVG icon, a 32px ICO, a 180px touch icon, 192px and 512px icons, one maskable icon.
- Default: a motion version is two seconds or shorter and ends on the exact static lockup.

## Output

- `design/assets/logo/`: `source/`, `svg/`, `png/`, `favicon/`, `app-icon/`. Names follow the pattern in the deliverables reference.
- `design/directions/<n>-<name>/`: the concept sheet and the concept boards.
- `design/reviews/<date>-logo-tests.md` and `design/reviews/<date>-trademark-knockout.md`.
- `design/assets/manifest.json`: one record for each file. `DESIGN.md`: the logo rules and the misuse list.
- One entry in `design/decisions.md` for each round.

Closing report:

```
Mark: <type of mark>, idea: <one sentence>
Lockups: <list>; clear space: <rule>; minimum sizes: <screen, print>
Tests: one color, reversed, tiny, greyscale, on photo: <pass/fail each>
Files: <count> under design/assets/logo/; master: <path>
Origin: own | generated then redrawn (<tool>)
Trademark: <no obvious conflict found | possible conflict: ...>. Not legal advice. Counsel: <confirmed | pending>
Not done: <what remains and why>
Evidence: VERIFIED | DOCUMENTED | UNTESTED <what>
```

## References

Read each file at the step named.

- [references/discovery-and-word-maps.md](references/discovery-and-word-maps.md): questions, competitor sheet, type of mark, word maps. Steps 1 to 4.
- [references/concepts.md](references/concepts.md): rough concepts in black, culling, presenting. Steps 5, 7 and 8.
- [references/generation-and-vector-route.md](references/generation-and-vector-route.md): where generation fits and the route to a vector. Steps 6 and 9.
- [references/construction.md](references/construction.md): vector drawing, optical correction, wordmark craft, path hygiene. Step 9.
- [references/test-suite.md](references/test-suite.md): each test, its method and its class. Steps 10 and 14.
- [references/lockups-and-versions.md](references/lockups-and-versions.md): lockups, clear space, minimum size, color and motion versions. Steps 11 and 14.
- [references/trademark-screening.md](references/trademark-screening.md): the knockout search and its limits. Step 12.
- [references/deliverables.md](references/deliverables.md): file set, naming, SVG cleaning, favicon and app icon. Step 15.
- [references/usage-sheet.md](references/usage-sheet.md): the sheet and the misuse list. Step 16.

## Sources

- Sagi Haviv, three criteria for a mark, from interviews found by search (secondary).
- Paul Rand's logo questions, from secondary reports; wording varies.
- Print Magazine, "When to Wordmark?" (search-confirmed).
- Aaron Draplin and Michael Bierut on process: books and talks, recalled, not re-read.
- GDH asset catalog, group `logo-aids`, and its license rules, step 7.
- Claude Design System craft rules: copy assets, never approximate. Read 2026-11-23.
- Connector cards for the vector route; see `kit/references/tools/`.
