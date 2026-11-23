# Scale and setting

Read this file at steps 9 and 10 of `typography`. It covers the modular scale, the ratio by medium, fluid type with `clamp()`, measure, leading by size, tracking, numerals, hierarchy, detail rules and the token form.

Evidence. The gates are in `SKILL.md`. The minimum sizes for each medium are in the one table in `SKILL.md`; this file does not repeat them. Every other number here is a default. Sources of the defaults: rule-of-thumb ranges for leading, search-confirmed ranges from Practical Typography and Utopia, and rules read in the Vercel and Rauno Freiberg guidelines, the Impeccable craft floor, the Design Systems Handbook and the Claude Slides and Design type rules. The clamp arithmetic in this file was computed and checked on 2026-11-23.

Terms. A style is one named role with a size, a line-height, a weight and a tracking value. The measure is the number of characters in one line. Leading is the line-height.

## 1. Build the scale from one ratio

1. Set the base. On the web the base is 16px, written as `1rem`.
2. Pick one ratio for the medium from the table.
3. Compute each size as base times ratio to the power n. Round to a half pixel.
4. Keep five to eight steps. Name each step by role, not by size.
5. Test the steps on real copy. Move a step when the content needs it. Record the exception.

| Medium | Default ratio | Why |
| --- | --- | --- |
| Dense interface, dashboard | 1.125 to 1.2 | Many levels sit close together; large jumps waste space |
| Product and content site | 1.2 at a phone width, 1.25 at a desktop width | Enough contrast for headings without crowding a phone |
| Editorial and landing page | 1.25 to 1.333 at a phone width, 1.333 to 1.5 at a desktop width | Display lines carry the voice |
| Slide deck | 1.5 or more | Each level must read from the back of a room |
| Poster and print display | 1.5 to 1.618 | Viewing distance varies; few levels, strong steps |
| Chart | No scale | Two or three sizes: title, label, annotation |

Steps from a 16px base, for reference:

| Ratio | -1 | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.125 | 14.2 | 16 | 18 | 20.2 | 22.8 | 25.6 | 28.8 |
| 1.2 | 13.3 | 16 | 19.2 | 23 | 27.6 | 33.2 | 39.8 |
| 1.25 | 12.8 | 16 | 20 | 25 | 31.2 | 39.1 | 48.8 |
| 1.333 | 12 | 16 | 21.3 | 28.4 | 37.9 | 50.5 | 67.3 |

Role names. Default set: `caption`, `body`, `lead`, `h3`, `h2`, `h1`, `display`. A product interface often adds `label` and `code`. Do not name a style by its size.

Failure: a scale with no ratio, where each size was picked alone. Test: divide each size by the next smaller size. The results should match within rounding, except for recorded exceptions.

## 2. Fluid type with clamp

Use fluid sizes for headings and display. Body text needs little or no fluid range.

The formula, for a size that grows from `min` at viewport `vmin` to `max` at viewport `vmax`, all in pixels:

```
slope     = (max - min) / (vmax - vmin)
intercept = min - slope * vmin
font-size: clamp(min/16 rem, intercept/16 rem + slope*100 vw, max/16 rem)
```

Worked values, for a range from 320px to 1240px:

| Style | Min to max | Declaration |
| --- | --- | --- |
| body | 16 to 18px | `clamp(1rem, 0.9565rem + 0.2174vw, 1.125rem)` |
| h1 | 32 to 56px | `clamp(2rem, 1.4783rem + 2.6087vw, 3.5rem)` |
| display | 40 to 80px | `clamp(2.5rem, 1.6304rem + 4.3478vw, 5rem)` |

Rules:

1. The middle value always has a `rem` part and a `vw` part. A size in `vw` alone does not grow on zoom. That is a gate.
2. Default: the maximum of a step is 2.5 times its minimum or less. A larger range can fail a 200% zoom test at some widths.
3. Take the two viewport widths from the design system. Use the same pair for fluid spacing.
4. Use a smaller ratio at the minimum width and a larger ratio at the maximum width. Each step then gets its own slope.
5. For a component that lives in containers of different widths, use container query units in place of `vw`.
6. Test at the minimum width, the maximum width and one width beyond each. Then zoom to 200% at three widths.
7. Store the minimum and the maximum of each style as tokens. The clamp line is generated from them.

A fluid scale calculator from the asset catalog can compute the lines. The values still become tokens through this skill.

## 3. Measure

1. Gate: running text holds 75 characters a line or fewer.
2. Default: aim for 45 to 75 characters. A phone at body size may hold 35 to 45. Accept that.
3. Set the measure on the text block, for example `max-width: 65ch`. One `ch` is the width of the digit zero, so the true count differs by face.
4. Count on the rendered page. Count the characters, with spaces, in three full lines of real copy. Take the average.
5. A longer measure needs more leading. A shorter measure needs less.
6. Headings follow their own limit. Default: a heading breaks into three lines or fewer.
7. Tables, code and interface rows are not running text. The measure rule does not apply to them.

## 4. Leading by size

Leading falls as size rises. Write line-height as a unitless number.

| Text | Default line-height | Basis |
| --- | --- | --- |
| Body, 14 to 19px | 1.4 to 1.6 | Rule of thumb; the handbook gives 1.4 to 1.5 |
| Lead and small headings, 20 to 32px | 1.25 to 1.4 | Rule of thumb |
| Headings above 32px | 1.05 to 1.25 | Rule of thumb; the handbook gives about 1.125 to 1.25 |
| Display above 64px | 0.95 to 1.1 | Rule of thumb |
| Slide body | 1.3 to 1.45 | Slides type rules |
| Slide display | 1.05 to 1.15 | Slides type rules |
| Print body on a Claude Design print artboard | 1.5 to 1.65 | Design type print rules |
| Captions and labels, one or two lines | 1.3 to 1.4 | Rule of thumb |

Adjust inside the range:

- more leading for a long measure, a large x-height, light text on a dark ground, and scripts with stacked marks
- less leading for a short measure, all-caps lines and very heavy weights

Default check: the layout survives a user override of line-height 1.5, paragraph spacing 2 times the font size, letter spacing 0.12em and word spacing 0.16em. The numbers are recalled from WCAG 2.2 and not re-read.

Space between paragraphs. Default: half to one line of the body leading. Use space or an indent, never both.

## 5. Tracking

| Text | Default tracking |
| --- | --- |
| Body text | 0. Do not track lowercase body text. |
| All caps and small caps | Add 5 to 12% |
| Headings above 32px | Tighten by 1 to 3% |
| Display | Tighten more with size, never tighter than -0.04em |
| Text under 12px | Add 1 to 2% |
| Connected scripts, such as Arabic and Devanagari | 0, always |

Rules:

1. Write tracking in `em`, so it scales with the size.
2. Keep kerning on. Do not disable font features to gain speed.
3. A face with an optical size axis already tightens at large sizes. Reduce your own tightening.
4. Default: web display type is 6rem or smaller. A poster or a brief can replace this.

## 6. Numerals

1. Gate: numbers compared in columns, and numbers that update in place, use tabular numerals. Set `font-variant-numeric: tabular-nums`.
2. Test the face: set `1111` above `0000`. With tabular numerals the two lines have equal width.
3. A face with no tabular numerals cannot set data. Choose another face, or set the data in the monospace.
4. Right-align numeric columns. Align on the decimal point. Keep one number of decimals in a column.
5. Use lining numerals in interfaces, tables and headings.
6. Default: old-style numerals suit long literary text. Use them only when the face has them and the voice asks for it.
7. Use a slashed or dotted zero where codes and ids appear.
8. A counter, a timer or a price that changes must not shift the text beside it. Tabular numerals prevent that.

## 7. Weight

- Default: no weight under 400 at text sizes. Light weights are for large sizes.
- Default: headings at 500 to 700. Emphasis in text at 600 or 700.
- Weight does not change on hover. A weight change shifts the layout.
- Default: two weights for text, one for display. More weights need a reason.
- Never let the browser synthesize a bold or an italic. Set `font-synthesis: none` and load the real style.
- A design system that requires a light body weight wins. The contrast gate still applies.

## 8. Hierarchy from few sizes

Default: four sizes at most on one screen. Five to seven styles in a system. Four or five sizes in a deck.

Build each level from more than size:

| Lever | Use |
| --- | --- |
| Size | One scale step or more between levels |
| Weight | Two weight steps or more |
| Color | The muted text token for the lower level |
| Space | More space above a heading than below it |
| Case and tracking | Spaced capitals for a short label, when the label carries information |
| Face | The display face for the top level only |

The tests that prove hierarchy:

1. Rank test. Write the first, second and third thing a reader must see on the view.
2. Blur test. Blur a screenshot until words cannot be read. The ranking must still match.
3. Gray test. Remove all color. The ranking must still match.
4. Default: five-second test. Show the view for five seconds. The person names the first item you wrote.
5. Count test. Count the distinct sizes on the view. More than four: merge two.

Failure: every level differs by a little. Fix: remove a level, then make the remaining steps larger.

## 9. Detail rules

These come from the Vercel Web Interface Guidelines and common practice.

- Curly quotes and apostrophes, never straight ones in reader-facing text.
- The ellipsis character, not three periods.
- A non-breaking space between a number and its unit, and inside names that must not split.
- `text-wrap: balance` on headings. `text-wrap: pretty` on paragraphs where supported.
- No heading ends with one short word on its own line.
- Left-aligned, ragged-right text for left-to-right languages. Justify only with hyphenation and a full measure.
- Centered text for three lines or fewer.
- Set the `lang` attribute, so hyphenation and quotes follow the language.
- Long words and URLs wrap. No text is cut off without an ellipsis and a way to read the rest.

## 10. Write the tokens

Write each style in the `type` family of `design/tokens.json`. The grammar belongs to `design-system`.

```json
{"name": "h1", "fontSize": "3.5rem", "lineHeight": 1.1, "fontWeight": 700,
 "letterSpacing": "-0.02em", "usage": "Page title. One on a view. Fluid from 2rem at 320px."}
```

Rules:

1. One style for each role. No style without a usage note.
2. Group styles by family: display, text, mono.
3. Write the fluid minimum and the viewport pair in the usage note, or in extra tokens the build reads.
4. Run `DS validate`. Fix every error.
5. Components use styles by name. A raw size in a component is a finding.

## 11. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| No ratio | Sizes picked one at a time | Rebuild from one ratio |
| Loose headings | Display type with body line-height | Tighten to the range for its size |
| Long lines | 100 characters or more on a wide screen | Set a measure on the text block |
| Viewport-only type | A size in `vw` with no `rem` part | Rewrite as a clamp with both parts |
| Ratio worship | The scale is exact and the content does not fit | Move the step. Record the exception. |
| Proportional data | Columns of numbers that do not align | Tabular numerals |
| Size as the only lever | Seven sizes, one weight, one color | Use weight, color and space |
| Shrink to fit | Text reduced below the floor to fit a box | Cut the text or enlarge the box |
