---
name: typography
description: Chooses, pairs, licenses, loads, scales and sets type for a brand or a product. Picks typefaces from the subject and the brand words, and pairs a display face with a text face. Builds a modular or fluid type scale. Sets measure, leading, tracking and numerals. Plans font loading and fallback metrics, and handles non-Latin scripts. Produces the type specimen for review. Use when a brand or product needs a typeface, a pairing, a type scale or a font license check.
disable-model-invocation: true
argument-hint: "[choose | pair | scale | load | specimen] <project or surface>"
---

# Typography

This skill takes type from a brief to tested tokens. It chooses faces from the subject and the brand words, pairs them, plans their loading, builds the scale and sets the detail. The type specimen is its review artifact.

Boundary. `mood-board` chooses the direction. `find-assets` reads each font license and writes its record. `design-system` owns the token grammar and the generated files. `logo-identity` draws a wordmark. `design-critique` and `accessibility-gate` judge a finished screen.

## Before you start

1. Read `DESIGN.md`, `design/brief.md`, `design/decisions.md` and `design/tokens.json` when they exist.
2. Read the chosen direction under `design/directions/` when one exists.
3. Precedence: user instruction, then the project design system, then the brief, then GDH defaults.
4. A face that the design system names is fixed. Do not replace it. Start at step 7.
5. No confirmed brief: stop and run `align` first.
6. Collect five inputs: content languages, media, reading mode for each surface, font hosting, and whether the repository is public.

Terms. A face is one typeface family. A text face sets running text. A display face sets headings. A style is one named role.

## Procedure

`DS` means `python3 ../design-system/scripts/ds.py` from this folder. In Claude Code: `${CLAUDE_SKILL_DIR}/../design-system/scripts/ds.py`.

1. Write the type brief: subject, three brand words, reading mode, languages, media, license limits.
2. Turn each brand word into type attributes. Name one classification for the text face, with a reason. Read [references/choosing-a-face.md](references/choosing-a-face.md).
3. Shortlist three text faces. Reject first by coverage, license, missing weights and missing numerals.
4. Test each on real copy at body size. Choose the text face before any display face.
5. Choose the pairing method: one family, a superfamily or a contrast pair. Read [references/pairing.md](references/pairing.md).
6. ASK: show two or three pairings on the same real copy. In an explore round they differ in idea. Get one choice.
7. Hand each chosen family to `find-assets` for the license read and the manifest record. License classes are in [references/sourcing-and-licenses.md](references/sourcing-and-licenses.md).
8. GATE: a paid license, a font activation or a hosted font kit is a spend or exposure point. Read the cost live. Show it. Get a yes. Call once.
9. Build the scale: one ratio for the medium, one style for each role. Read [references/scale-and-setting.md](references/scale-and-setting.md).
10. Set measure, leading, tracking and numerals for each style.
11. Add script rules when the brief lists a non-Latin language. Read [references/non-latin.md](references/non-latin.md).
12. Decide static or variable files. Read [references/variable-fonts.md](references/variable-fonts.md).
13. Plan loading: self-host, subset, `font-display`, fallback metric overrides. Read [references/loading-and-performance.md](references/loading-and-performance.md).
14. Write the `type` family in `design/tokens.json`. Run `DS validate`. Generate `tokens.css` through `design-system`.
15. Build the type specimen. Read [references/specimen.md](references/specimen.md).
16. ASK: "Keep, change or remove?" for voice, hierarchy, reading comfort and numerals. Change only what was asked.
17. Record the round in `design/decisions.md`. Record each type rule in `DESIGN.md`.
18. Close with the report in Output.

## Tools

Capabilities, in preference order: `fonts`, `design-system`, `canvas`. Vocabulary: [capabilities.json](../../catalogs/capabilities.json).

- `fonts`: search, preview and entitlement checks in a hosted library. Example card: [adobe](../../references/tools/adobe.md).
- `design-system`: type tokens and the token specimen, through [ds.py](../design-system/scripts/ds.py).
- `canvas`: a comparison specimen as artboards. Example card: [claude-design](../../references/tools/claude-design.md).

Pick the tool by kernel rule 8. Read its card before the first call. Read prices and plan limits live. With no `fonts` tool, use the font sources in `kit/catalogs/assets.json` through `find-assets`. With no `canvas` tool, build the specimen as local HTML.

## Checks

Gates. Each one blocks delivery.

1. Every size meets the gate rows of the minimum-size table.
2. Text contrast passes in every theme: 4.5:1 for normal text, 3:1 for large text. Large means 24px, or 18.66px bold. Run `DS contrast`.
3. No font size is set in viewport units alone. Such text does not grow when the user zooms.
4. Running text holds 75 characters a line or fewer.
5. Numbers compared in columns, and numbers that update in place, use tabular numerals.
6. Each family has a license record in `design/assets/manifest.json` before its first use.
7. The rendered text uses the chosen font, not a fallback. No font loads from a third-party host without a written exception.
8. Every size, line-height, weight and tracking value in the deliverable is a token.
9. For code, the specimen was reviewed as rendered at each breakpoint and theme. For an artifact type, follow that type's own check rule.
10. The user reviewed the specimen. The round is in `design/decisions.md`.
11. A script that you cannot read stays labelled UNTESTED until a reader of that language reviews it.

Minimum sizes by medium. This is the only copy of this table.

| Medium | Body text | Smallest text | Class | Basis |
| --- | --- | --- | --- | --- |
| Web | 16px; mobile web inputs 16px | 12px | Body and inputs: gate. Smallest: default. | Vercel guidelines; Design Systems Handbook |
| App, iOS | 17pt | 11pt | Default | From memory. Confirm in the platform guideline. |
| App, Android | 16sp | 12sp | Default | From memory. Confirm in the platform guideline. |
| Slide, 1920px wide | 24px | 24px | Gate in a Claude Slides deck. Default elsewhere. | Slides type rules |
| Print | 12pt (16px on the artboard) | 12px on the artboard; 7pt in other print | Gate on a Claude Design print artboard. Default elsewhere. | Design type print rules; 7pt is a rule of thumb |
| Chart | none | 12px | Default | Rule of thumb |

Defaults. The user, the design system or the brief can replace each one.

- Default: two families. A third needs a written job. Never more than three.
- Default: four sizes at most on one screen, five to seven styles in a system, four or five sizes in a deck.
- Default: measure 45 to 75 characters. A narrow phone may hold fewer.
- Default: line-height 1.4 to 1.6 for body, 1.25 to 1.4 at 20 to 32px, 1.05 to 1.25 above 32px, 0.95 to 1.1 above 64px.
- Default: ratio 1.125 to 1.2 for dense interfaces, 1.2 to 1.333 for content sites, 1.5 or more for slides and posters.
- Default: all caps take 5 to 12% added tracking. Display tracking stays above -0.04em. Web display type stays under 6rem.
- Default: no weight under 400 at text sizes. Weight does not change on hover.
- Default: self-hosted WOFF2 files; a variable file for three weights or more.
- Default: a fluid step's maximum is 2.5 times its minimum or less.
- Default: the font swap moves no line of text.

## Output

- `design/tokens.json`: the `type` family. `design/tokens.css` and `DESIGN.md`: generated through `design-system`.
- `design/directions/<n>-<name>/type-specimen.html`: one for each candidate pairing.
- `design/reviews/<date>-type-specimen.html`: the specimen of the chosen system.
- `design/assets/manifest.json`: one record for each family, written through `find-assets`.
- One entry in `design/decisions.md`.

Closing report:

```
Type: <text face> + <display face>, method: <one family | superfamily | contrast pair>
Reason: <brand word> -> <attribute>, for each face
Scale: base <size>, ratio <r>, <n> styles, fluid <range or none>
Files: <files, weights, total size>; license class for each family
Checks: sizes; contrast <checked>/<failed>; measure <chars>; tabular; font loaded
Languages: <script>: VERIFIED | UNTESTED
Not done: <what remains and why>
Evidence: VERIFIED | DOCUMENTED | UNTESTED <what>
```

## References

Read each file at the step named.

- [references/choosing-a-face.md](references/choosing-a-face.md): type brief, attributes, classifications, hard filters, worked choices. Steps 1 to 4.
- [references/pairing.md](references/pairing.md): the three pairing methods and their tests. Step 5.
- [references/sourcing-and-licenses.md](references/sourcing-and-licenses.md): sources and what each license class allows. Step 7.
- [references/scale-and-setting.md](references/scale-and-setting.md): ratio, fluid type, measure, leading, tracking, numerals, hierarchy. Steps 9 and 10.
- [references/non-latin.md](references/non-latin.md): script notes. Step 11.
- [references/variable-fonts.md](references/variable-fonts.md): axes, when to use one file, pitfalls. Step 12.
- [references/loading-and-performance.md](references/loading-and-performance.md): self-hosting, subsets, `font-display`, fallback metrics. Step 13.
- [references/specimen.md](references/specimen.md): the parts of the specimen and the review round. Step 15.

## Sources

- Anthropic, frontend-design skill, "Typography" and "Subject".
- Vercel Web Interface Guidelines; Rauno Freiberg, Web Interface Guidelines, "Typography".
- Impeccable, craft floor reference, "Verify: Type".
- Butterick's Practical Typography, "Line length", "Line spacing", "Letterspacing".
- Utopia, "Clamp"; Smashing Magazine, fluid type and accessibility (2023); Capsize README.
- Design Systems Handbook (InVision DesignBetter), chapter 2.
- Claude Design, Slides and Design System artifact types, read 2026-11-23.
- WCAG 2.2, success criteria 1.4.3, 1.4.4 and 1.4.12.
