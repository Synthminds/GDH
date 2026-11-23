# Pairing: three methods and their tests

Read this file at step 5 of `typography`. It covers how to decide the number of faces, the three pairing methods, the tests that prove a pair, role assignment and worked pairs.

Evidence. The limit on families comes from the Anthropic frontend-design skill and the Design Systems Handbook, chapter 2. The pairing methods and their tests are typographic practice written from memory. Treat every number here as a default. A pair is UNTESTED until you see both faces on real copy.

Terms. Structure is how a letter is built: its skeleton, stroke contrast, serifs and terminals. Proportion is how a letter is sized: x-height, width and the length of ascenders. A superfamily is a set of related families drawn by one design team to work together.

## 1. Decide how many faces first

1. Start with one family. Add a second only for a job the first cannot do.
2. Write the job of each face in one line. "Display: place names and poster lines. Text: everything else."
3. A third family needs a written job. Code, data and measurement are the usual job of a monospace.
4. Default: never more than three families. A slide deck format may cap families lower or higher; read the format.

## 2. Choose the method

| Situation | Method | Why |
| --- | --- | --- |
| Dense product interface, many languages, tight loading budget | One family | One file, one rhythm, full coverage |
| Editorial site, reports, documents with long text and interface parts | Superfamily | Contrast with no risk of clash |
| Marketing page, poster, brand with a strong voice | Contrast pair | The display face carries the voice |
| Two brand words pull apart, such as exact and warm | Contrast pair | Each face carries one word |
| The design system names one family only | One family | The system decides |

## 3. Method A: one family with weight and width contrast

Use one family and build contrast from weight, width, size and case.

Rules:

1. Skip at least two weight steps between two levels. Use 400 with 700, not 400 with 500.
2. Use width for display when the family has widths. A condensed heading above regular text is a clear contrast.
3. Use the optical size axis or the display cut for large sizes when the family has one.
4. Keep one weight for body text and one for emphasis. Do not use five weights on one screen.
5. Check that the family has the italic, the numerals and the coverage the copy needs.

Test: set a heading and a paragraph in gray on white. A reader must rank them without color and without size labels.

Risk: the result looks flat. Fix it with a larger size step or a width change, not with a second family.

## 4. Method B: a superfamily

Use the serif, the sans and the monospace of one related set.

Rules:

1. Give each member a role by content type, not by taste. Serif for long text, sans for interface, mono for code.
2. Do not mix two members inside one text block.
3. Check each member on its own. A strong sans can come with a weak serif.

Test: set one line of each member at the same size on one baseline. The x-heights and the weights match without adjustment.

Risk: low character. The set reads as a system, not as a voice. Add character with scale, space and one display treatment.

## 5. Method C: a contrast pair

Pair two families that differ in structure and share proportion.

Differ clearly in at least one of these:

- serif against sans
- high stroke contrast against low stroke contrast
- condensed against regular width
- heavy against regular weight
- a drawn, irregular display face against a plain text face

Share these:

- x-height, as a share of the cap height
- letter width rhythm in the round letters
- the same underlying skeleton: humanist with humanist, geometric with geometric

Rules:

1. One face leads. The display face carries the voice. The text face stays quiet.
2. Two faces of one classification need a strong difference in width or weight. Two similar sans faces read as a mistake.
3. Never pair two loud faces.
4. Size the two faces by x-height, not by the number. One of them may need a 5% size change to look equal.
5. Match the weights by eye in a mixed line. Regular in one family can look like medium in another.

## 6. Tests for a contrast pair

Run each test on real copy. Record the result in the decision entry.

| Test | How | Pass |
| --- | --- | --- |
| Overlay | Set the same word in both faces at one size. Compare x-heights and the width of `o` and `n`. | Default: x-heights differ by 5% or less, or you adjusted a size to match |
| Cover | Cover the size and the color. Show one line of each face. | A reader tells heading from text by structure alone |
| Skeleton | Compare `a`, `g`, `e` and `R` in both faces | The two faces share a construction logic, or they differ on purpose |
| Mixed line | Set a display word inside a line of text, such as a product name | The line keeps one baseline and one apparent weight |
| Numerals | Set a price and a date in both faces | The digits look related, or only one face ever sets numbers |
| Stress | Set the longest heading and the densest table | Nothing overflows; the pair still reads as two roles |
| Swap | Ask: would this pair fit a competitor? | You can name what the pair says about this subject |

A pair that fails Overlay can still work at very different sizes. Then the faces never share a line. Write that limit as a rule in `DESIGN.md`.

## 7. Assign roles and write the rules

Write one rule for each role. A consuming agent must be able to follow it with no judgment.

- "Headings h1 to h3 and place names: the display face, weight 700."
- "Body, lists, forms and tables: the text face, weight 400; emphasis 600."
- "Never set the display face below 20px."
- "Never set the display face in a paragraph."
- "Code and measurements: the monospace, weight 400."

Then name each family in the `families` map of the `type` family. Name the keys by role: `display`, `text`, `mono`.

## 8. Show the options

1. Build each candidate pairing as a specimen on the same real copy and the same layout.
2. In an explore round, show two or three pairings that differ in idea. Name each idea in one sentence.
3. In a refine round, show two variants that differ in one attribute: the display face, or the ratio, or the weight.
4. Keep the option names stable across rounds. Never renumber.
5. State the main tradeoff of each option: voice against neutrality, character against loading weight.
6. ASK: "For each pairing: keep, change or remove the display face, the text face and the contrast between them?"

## 9. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Near twins | Two sans faces that differ slightly | Drop one, or pair across classifications |
| Shouting match | Two expressive faces | Keep one voice. Make the other face plain. |
| Orphan role | A family that appears once, with no written job | Remove it |
| Weight creep | Regular, medium, semibold and bold on one screen | Two weights for text, one for display |
| Mismatch in line | A display word in a text line looks larger or bolder | Size by x-height; match weights by eye |
| Generated pair | "The tool suggested it" is the reason | Run the tests. Write the reason from the brief. |
| Pair as the only idea | A serif headline on sans text and nothing else decided | Build scale, space and one signature treatment |

## 10. Worked pairs

The outcomes below are illustrative. They show the reasoning, not verified facts about a family.

One family. A clinic booking app with eleven languages. One humanist sans with a wide weight range. Headings use weight 700 at one scale step up. Buttons use 600. The loading budget holds one variable file. The voice comes from generous leading and plain words, not from a second face.

Superfamily. A research institute's reports. The serif sets the report text. The sans sets tables, captions and the web navigation. The mono sets data codes. Test result: the sans looked lighter than the serif in mixed lines, so captions moved from 400 to 500.

Contrast pair. A brass band festival. A heavy condensed grotesque sets band names. A wide plain grotesque sets times and stages. They share a grotesque skeleton and differ in width and weight. Overlay result: the display x-height was 8% taller, so the two faces never share a line. That limit is a rule in `DESIGN.md`.
