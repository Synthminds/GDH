# Create a system from a brief

Use this for a new brand or product. You need `design/brief.md` and a chosen direction in `design/decisions.md`. Without a confirmed brief, start `align` and stop. Without a chosen direction, run `mood-board` first.

`DS` means `python3 <skill folder>/scripts/ds.py`.

## Steps

1. Read the brief: subject, audience, primary job, use context, brand words, constraints.
2. Read the chosen direction: its colors, typefaces, shape and motion notes, and what was rejected.
3. ASK: "Which values are fixed by the brand already?" Fixed values are facts. Enter them exactly.
4. Scaffold: `DS init brands/<slug> --name "<Name>"`. For a project system use `DS init design --name "<Name>"`.
5. The scaffold values are starter defaults. Replace each one or confirm it with the owner.
6. Color. Take the hues from the direction. Call the `color` skill to build the scale when one is needed.
   - Decide light or dark first from the use context.
   - Write 4 to 6 named raw colors. Then write role colors that alias them.
   - Minimum roles: page ground, raised ground, border, text, muted text, accent, text on accent, one status color.
   - Fill every theme. A dark theme is its own mapping.
7. Type. Take the typefaces from the direction. Call the `typography` skill for the scale when one is needed.
   - GATE: a font file needs a license that covers the use. Record it before you add the file.
   - Add files under `fonts/` and list them in `type.fonts`.
   - Write 5 to 7 styles. Give each a usage note.
8. Spacing, radius, shadow and motion. Write 4 spacing steps and 3 radii first. Add a step only for a named need.
   - Default: tint shadows toward the text color instead of pure black.
   - Default: controls move in under 300 ms. Page-level brand motion may be longer. Name each motion token by role.
9. Write a usage note on every token. Text colors name their grounds.
10. Run `DS validate` and `DS contrast`. Fix until both pass.
11. Write the README as usage rules that name tokens. Follow [../references/craft.md](../references/craft.md).
12. Generate `tokens.css` and `DESIGN.md`. Run `DS specimen` and show the page.
13. ASK: "Keep, change or remove?" for each of color, type, spacing and shape. One scoped question for each round.
14. Apply the changes. Rerun the checks. Record the round in `design/decisions.md`.
15. Fill `SOURCE.md`: the brief, the direction, each owner decision with its date, and every INFERRED value.
16. Offer the next step: components ([extend.md](extend.md)) or Claude ([publish-to-claude.md](publish-to-claude.md)).

## What not to do

- Do not start from a palette template. Each color needs a reason from the brief or the direction.
- Do not ship the scaffold values as a brand.
- Do not build components before a real screen needs them.
- Do not add a second accent hue without a job for it.

## Done when

The gates in `SKILL.md` pass, the owner accepted the specimen, and the decision record holds the round.

## Sources

- Design Systems Handbook (InVision DesignBetter), chapter 2 "Step by step" and "Design tokens".
- Claude Design System artifact type, craft reference, read 2026-11-23.
