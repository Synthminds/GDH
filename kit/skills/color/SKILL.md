---
name: color
description: Builds palettes, themes and contrast-checked semantic colors for a brand or a product. Derives a palette from the brand words and the subject. Builds OKLCH ramps and a neutral tinted toward the brand hue. Maps colors to semantic roles and adds a dark or high-contrast theme. Checks contrast and color-blind safety in every theme. Separates data colors from brand colors, and sets proportion and gradient rules. Use when a brand or product needs a palette, a theme, a semantic color or a contrast fix.
disable-model-invocation: true
argument-hint: "[palette | ramps | roles | theme | check | data] <project or brand>"
---

# Color

This skill takes color from a brief to checked tokens. It derives a palette from the brand words and the subject, builds ramps in OKLCH, maps them to roles, builds each theme and proves the result with the contrast script.

Boundary. `mood-board` chooses the direction. `design-system` owns the token grammar, the exports and the script. `data-viz` chooses and builds charts. `accessibility-gate` runs the full accessibility check. `logo-identity` applies color to a mark. `find-assets` reads the terms of an outside palette source.

## Before you start

1. Read `DESIGN.md`, `design/brief.md`, `design/decisions.md` and `design/tokens.json` when they exist.
2. Read the chosen direction under `design/directions/` when one exists.
3. Precedence: user instruction, then the project design system, then the brief, then GDH defaults.
4. A color that the design system fixes is never changed. Derive only the roles it lacks, and ASK first.
5. No confirmed brief: stop and run `align` first.
6. Collect four inputs: fixed brand colors, the use scene, the media, and whether charts exist.

Terms. A ramp is one hue in ordered lightness steps. A role is a semantic token such as `text` or `border-control`. A ground is the color under a text or a control. A pair is one foreground on one ground.

## Procedure

`DS` means `python3 ../design-system/scripts/ds.py` from this folder. In Claude Code: `${CLAUDE_SKILL_DIR}/../design-system/scripts/ds.py`.

1. Write the color brief: brand words, five colors seen in the subject's world, fixed colors, use scene, media.
2. Write the category default: the palette most competitors share. Read [references/palette-from-brand-words.md](references/palette-from-brand-words.md).
3. Turn each brand word into a hue, chroma and lightness intent. Name four to six colors, each with a reason.
4. Decide light or dark as the first theme from the use scene, not from the product category.
5. ASK: show two or three palettes on the same real sample. In an explore round they differ in idea. Get one choice.
6. Build a ramp for the brand hue, the accent and each status hue. Build a neutral tinted toward the brand hue. Read [references/oklch-ramps.md](references/oklch-ramps.md).
7. Map ramp steps to roles: surface, text, border, accent, status. Read [references/roles-and-themes.md](references/roles-and-themes.md).
8. Write each role in `design/tokens.json`. Write a usage note that names the grounds: "Text on bg and surface."
9. Build each further theme as its own mapping. Dark is not an inversion.
10. Run `DS validate`, then `DS contrast`. Fix a failing pair by lightness first. Read [references/contrast-and-color-blind.md](references/contrast-and-color-blind.md).
11. Run the color-blind check. Give every meaning a second cue.
12. Charts exist: build the data colors as a separate set. Read [references/data-colors.md](references/data-colors.md).
13. Set the proportion rule and the gradient rule. Read [references/gradients-and-proportion.md](references/gradients-and-proportion.md).
14. Run `DS specimen`. Test the palette on one real screen.
15. ASK: "Keep, change or remove?" for each role group. Change only what was asked.
16. GATE: a generated sample image is a spend call. An upload of brand files or a publish is exposure. Get a yes for each.
17. Generate `tokens.css` and `DESIGN.md` through `design-system`. Record the round in `design/decisions.md`.
18. Close with the report in Output.

## Tools

Capabilities, in preference order: `design-system`, `brand-kit`, `canvas`. Vocabulary: [capabilities.json](../../catalogs/capabilities.json).

- `design-system`: tokens, contrast and the specimen through [ds.py](../design-system/scripts/ds.py). A hosted system is read as data. Example card: [claude-design-system](../../references/tools/claude-design-system.md).
- `brand-kit`: read a stored kit's colors as data. Example card: [picsart](../../references/tools/picsart.md).
- `canvas`: palette options side by side. Example card: [claude-design](../../references/tools/claude-design.md).

Pick the tool by kernel rule 8. Read its card before the first call. Read prices and limits live. The script needs no tool and no network. With no `canvas` tool, show options as local HTML. Scale and palette tools in `kit/catalogs/assets.json` give starting values only; reach them through `find-assets`.

## Checks

Gates. Each one blocks delivery.

1. `DS contrast` passes in every theme: 4.5:1 for normal text; 3:1 for large text, control outlines, focus rings and icons that carry meaning. Large means 24px, or 18.66px bold.
2. No meaning rests on color alone. Each status has an icon or a text label.
3. Every color in a deliverable is a token. Components use roles, never ramp steps or raw values.
4. Every text and control color has a usage note that names its grounds.
5. Every role has a value in every theme. `DS validate` reports zero errors.
6. A state change keeps or raises contrast: hover, active, focus.
7. Text on a gradient or an image passes contrast at its weakest point.
8. A fixed brand color is exact. A failing brand pair stays exact, is flagged in its note and in the report, and gets a passing role beside it.
9. A palette copied whole from another brand or a palette site does not ship. Read the source's terms through `find-assets`.
10. The color-blind result is labelled VERIFIED only after a simulation was viewed. Otherwise it is UNTESTED.

Defaults. The user, the design system or the brief can replace each one. A choice they require is reported as `brand-required`, never as a tell.

- Default: work in OKLCH. Keep each value inside sRGB. Offer wide gamut only as an enhancement.
- Default: one brand hue and at most one accent. Two accents share chroma and lightness.
- Default: a twelve-step ramp is working material. Tokens hold only the steps a role uses.
- Default: neutral chroma 0.003 to 0.015 at the brand hue.
- Default: a fill at OKLCH lightness 0.55 or lower takes white text.
- Default: about 60% neutral ground, 30% secondary surface, 10% accent. A product screen runs more neutral.
- Default: status colors differ in lightness, not only in hue. Prefer blue against orange to red against green.
- Default: eight categorical data colors at most. Status colors are never series colors.
- Default: one gradient with a job on a view. No gradient text.
- Default: on a dark theme, body text aims above the floor, at 7:1 or more.
- Default: APCA values are advice. The gate is the WCAG ratio.
- Default: a high-contrast theme is an added theme at 7:1.

## Output

- `design/tokens.json`: the `color` family with themes, plus a `gradient` family when used.
- `design/tokens.css` and `DESIGN.md`: generated through `design-system`.
- `design/directions/<n>-<name>/palette.html`: one for each candidate palette.
- `design/reviews/<date>-color.md`: contrast output, the color-blind result and the proportion check.
- One entry in `design/decisions.md`.

Closing report:

```
Palette: <brand hue>, <accent>, neutral tinted to <hue>; themes: <ids>
Reason: <brand word> -> <hue, chroma or lightness choice>, for each named color
Checks: validate <errors>/<warnings>; contrast <pairs>/<checks>/<failed>
Color-blind: VERIFIED | UNTESTED <method>; second cue for <each meaning>
Kept exact and flagged: <failing brand pairs>
Data colors: <set, count> or none
Not done: <what remains and why>
Evidence: VERIFIED | DOCUMENTED | UNTESTED <what>
```

## References

Read each file at the step named.

- [references/palette-from-brand-words.md](references/palette-from-brand-words.md): color brief, word to color translation, category default, worked palette. Steps 1 to 5.
- [references/oklch-ramps.md](references/oklch-ramps.md): OKLCH, the ramp recipe, the tinted neutral, computed thresholds. Step 6.
- [references/roles-and-themes.md](references/roles-and-themes.md): the role set, the step map, themes, dark mode rules. Steps 7 to 9.
- [references/contrast-and-color-blind.md](references/contrast-and-color-blind.md): the script, the pairs file, fixes, the color-blind procedure. Steps 10 and 11.
- [references/data-colors.md](references/data-colors.md): data colors against brand colors. Step 12.
- [references/gradients-and-proportion.md](references/gradients-and-proportion.md): proportion defaults and gradient discipline. Step 13.

## Sources

- Tailwind CSS docs, "Theme variables" (OKLCH palette).
- Radix Colors, "Understanding the scale".
- Vercel Web Interface Guidelines, "Design" and "Dark Mode & Theming".
- Impeccable, craft floor reference, "Surface habits" and "Verify: Contrast".
- Anthropic, frontend-design skill, "Before coding".
- APCA in a Nutshell (Myndex), used as advice only.
- Design Systems Handbook (InVision DesignBetter), chapter 2, "Color".
- Aarron Walter, Designing for Emotion, chapter 2 (contrast) and chapter 3 (softened palettes).
- Claude Design, Design System, Slides and Data artifact types, read 2026-11-23.
- WCAG 2.2, success criteria 1.4.1, 1.4.3 and 1.4.11, as applied by the GDH kernel.
