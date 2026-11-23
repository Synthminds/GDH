# Usage sheet

Read this file at step 16 of `logo-identity`. The usage sheet is one page that tells any person or agent how to place the logo correctly. It goes into `DESIGN.md` under a "Logo" heading, and into the brand pack `README.md` when a pack exists.

## 1. What the sheet holds

Keep it to one page. Show, then tell: each rule sits beside a small picture.

| Section | Content |
| --- | --- |
| The idea | One sentence: what the mark means. No history. |
| Lockups | Each lockup with its name and when to use it. |
| Choosing a version | The decision table in section 2. |
| Clear space | The rule, drawn with the unit taken from the mark. |
| Minimum size | One value for screen and one for print, for each lockup. |
| Color versions | Color, black, white. Which grounds each one reads on. |
| On images | Which version, and which backing, on a photo. |
| Misuse | The misuse list in section 4, drawn. |
| Files | Where the files are and how they are named. |

## 2. Choosing a version

| Situation | Use |
| --- | --- |
| Wide space, first contact with the brand | primary lockup |
| Narrow or square space | stacked lockup |
| The name is already present nearby | mark only |
| Very small size, under the lockup minimum | mark only, or the small-size redraw |
| One-color print, engraving, stamp | black version |
| Dark ground or a brand-color ground | white version |
| Busy photo | white or black version on a solid or scrim backing, as the sheet states |

Write the real minimums into the last two rows. Take them from the tiny-size test.

## 3. Clear space and minimum size

- Define clear space from a part of the mark. Default: the cap height of the wordmark on every side.
- State the unit in the sheet with a drawing. A person must be able to measure it without a tool.
- State the minimum size as a width. Give a screen value in px and a print value in mm.
- The minimums come from the test suite. Do not copy them from another brand.

## 4. The misuse list

Draw each misuse with a cross. Keep the list to the mistakes that this mark invites.

1. Do not stretch, squash or rotate the logo.
2. Do not change the colors or apply a color that is not a brand token.
3. Do not add a shadow, an outline, a glow or a gradient that the master does not have.
4. Do not move, resize or respace the mark and the wordmark inside a lockup.
5. Do not retype the wordmark in a font.
6. Do not place the color version on a ground where it fails the contrast floor.
7. Do not place the logo on a busy image with no backing.
8. Do not put anything inside the clear space.
9. Do not use the logo under its minimum size.
10. Do not crop the logo, and do not use a part of the mark as a pattern unless the sheet allows it.
11. Do not rebuild the logo from a screenshot. Use the delivered files.

Add the brand-specific items after these. Example: "Do not separate the flame from the frame."

## 5. Rules for agents

Write these lines into `DESIGN.md`, so that a coding agent reads them.

```
Logo files: design/assets/logo/. Use the SVG. Never redraw, recolor or regenerate the logo.
Lockups: <names>. Default lockup: <name>. Under <n> px wide, use <lockup>.
Clear space: <rule>. Minimum width: <px> on screen, <mm> in print.
On a dark ground use <file>. On a photo use <file> on <backing>.
A missing logo file is a labelled placeholder. Never invent a logo.
```

## 6. Co-branding and partner use

- State the order, the divider and the size relation for two logos side by side.
- Each logo keeps its own clear space. The larger clear space wins.
- Do not make a new lockup with a partner logo without the user's yes. It is a brand decision.

## 7. Check before you hand over

- Every value on the sheet comes from a test or from a token.
- Every lockup named on the sheet exists as a file.
- The misuse list is drawn, not only written.
- The sheet says where the files are.
- A person who has never seen the brand can place the logo correctly from the sheet alone.
