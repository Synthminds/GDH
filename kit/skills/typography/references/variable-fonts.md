# Variable fonts

Read this file at step 12 of `typography`. It covers what a variable font is, the decision between static and variable files, the axes, how to write the CSS, the pitfalls and the token form.

Evidence. The rule "use the variable package for three weights or more" is a GDH default from the asset catalog notes. The rule "weight does not change on hover" comes from Rauno Freiberg's guidelines, read 2026-11-23. The rest is web platform behavior written from memory. Treat it as UNTESTED until you see it in the rendered page and in the network panel.

Terms. A variable font is one file that holds a range of styles. An axis is one dimension of that range. An instance is one point in the range, such as weight 600.

## 1. Decide: static or variable

| Situation | Choose | Why |
| --- | --- | --- |
| One or two weights of a family | Static files | Smaller total download |
| Three weights or more of a family | Variable file | One request, any weight in the range |
| Width or optical size contrast in one family | Variable file | The axis does the pairing work |
| Fluid weight, or weight tuned by theme | Variable file | Needs a continuous range |
| Export to a slide file, an email or a native design tool | Static files | Many such targets do not read variable fonts |
| A native app | Check the platform | Support differs by platform and version |

Compare real sizes before you decide. Add up the static files the design needs. Compare the sum with the variable file after subsetting.

## 2. The axes

| Axis | Tag | Controls | CSS to use |
| --- | --- | --- | --- |
| Weight | `wght` | Stroke weight | `font-weight` |
| Width | `wdth` | Condensed to expanded | `font-stretch` |
| Italic | `ital` | Upright or italic forms | `font-style: italic` |
| Slant | `slnt` | Angle of an oblique | `font-style: oblique <angle>` |
| Optical size | `opsz` | Detail and spacing tuned to the size | `font-optical-sizing: auto` |
| Grade | `GRAD` | Weight change with no change in width | `font-variation-settings` |

Custom axes use capital letters in the tag. Each family documents its own axes and ranges. Read them from the family's page or the file, not from memory.

## 3. Write the CSS

1. Declare the range in the `@font-face` rule: `font-weight: 100 900;` and, with a width axis, `font-stretch: 75% 125%;`.
2. Use the high-level properties from the table. They inherit and cascade as expected.
3. Use `font-variation-settings` only for an axis with no high-level property.
4. `font-variation-settings` replaces the whole list. Setting one axis there resets the others. Carry the full list through custom properties.
5. An italic often ships as a second file. Declare it with `font-style: italic` and the same family name.
6. Leave `font-optical-sizing` on `auto` when the family has the axis.
7. Name the format in the source list so that old browsers skip the file. Give a static fallback when the audience needs one.

## 4. Use the range with discipline

- Use named stops. Default: three or four weight values in the tokens, not any number that looks right.
- Each stop is a token. A weight of 437 in a component is a raw value.
- Width stops need a job each: condensed for display, regular for text.
- Do not animate weight or width on hover. The text reflows and neighbors move.
- A weight change on a state must not change the width of the control. A grade axis can do this. Otherwise reserve the space.
- Default: light text on a dark ground looks heavier. Reduce the weight or the grade one small step in the dark theme, and compare by eye.
- Optical size follows the font size. Do not pin it unless a size looks wrong.

## 5. Pitfalls

| Pitfall | Sign | Fix |
| --- | --- | --- |
| Faux bold | The declared range is missing; the browser thickens the regular | Declare the weight range in `@font-face` |
| Reset axes | Setting one axis in `font-variation-settings` drops another | Carry all axes in one declaration through custom properties |
| Two files loaded | Static and variable files of one family both load | Remove one. Check the network panel. |
| Heavier total | A variable file loaded for one weight | Use the static file |
| Export loss | A deck or a document export shows a fallback face | Supply static files to that target |
| Unsubsettable license | The license limits changed builds | Use the foundry's own subsets or the package's subsets |
| Raw stops | Many unnamed weight values across components | Name the stops as tokens |

## 6. Tokens

Write weights as numbers in the type styles. Record the file and its range in `type.fonts`:

```json
{"family": "Example Sans", "file": "fonts/ExampleSans-Variable.woff2", "weight": "100 900", "style": "normal"}
```

Write the width stops and the grade values as tokens in an extra family when the design uses them. Give each a usage note. Then run `DS validate`.

## 7. Checks

1. The network panel shows one file for each family and style, not a static and a variable copy.
2. Bold text uses a real weight. Zoom in: a synthesized bold looks smeared and has rounded corners.
3. Each weight in the rendered page is a token value.
4. Hover and focus states cause no reflow.
5. The export targets in the brief render the right face. Test one export of each kind.
6. The license record covers the variable file and any subset you built.
