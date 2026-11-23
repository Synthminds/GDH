# Non-Latin scripts and multilingual text

Read this file at step 11 of `typography`, when the brief lists a language outside basic Latin. It covers the rules for every script, notes for each script group, the companion-face method, text expansion and the review rule.

Evidence. The research behind GDH holds no source on non-Latin typography. Everything in this file is practice written from memory. Every number is a default. A setting in a script you cannot read is UNTESTED until a reader of that language reviews the rendered specimen. Say so in the report.

Terms. A script is a writing system. Coverage is the set of languages a face sets with its own glyphs. A companion face is the face that sets a second script beside the main face.

## 1. Rules for every script

1. ASK for the full language list before you shortlist a face. Add languages the product plans within a year.
2. Set the `lang` attribute on the page and on each passage in another language. Line breaking, hyphenation, quotes and glyph variants depend on it.
3. Check coverage with real strings. Take the hardest strings from the project copy, not from a sample sentence.
4. Never let the browser synthesize a style. Set `font-synthesis: none`. Many scripts have no italic and few weights.
5. Build one font stack for each script. Order it so each script gets its own face.
6. Match a companion face by apparent size, weight and gray value. Do not match by name.
7. Use logical CSS properties: `margin-inline-start`, `padding-inline`, `text-align: start`. They follow the writing direction.
8. Do not reuse Latin settings. Leading, measure, tracking and emphasis differ by script.
9. Put a string of each script in the specimen, at body size and at the smallest size.
10. A reader of the language reviews the specimen. Until then, the report says UNTESTED for that script.

## 2. Choose a companion face

| Route | When | Check |
| --- | --- | --- |
| One family that covers every script | The family was drawn for those scripts | Each script looks designed, not derived |
| A superfamily with a matched script family | The main face has a sibling for the script | Weights and heights match in a mixed line |
| A separate face for the script | No sibling exists | Match apparent size, weight and stroke contrast by eye |
| The system face of the script | The loading budget is tight, or files are very large | Rendering differs by operating system; test on each |

Method for a separate face:

1. Set a mixed line with both scripts at one size.
2. Scale the companion until both scripts look the same size. Record the factor as a token or a rule.
3. Pick the weight that gives the same gray value. A regular may pair with a medium.
4. Compare stroke contrast and terminals. A low-contrast sans needs a low-contrast companion.
5. Check numerals and punctuation. Decide which face sets them in mixed text.

## 3. Chinese, Japanese and Korean

- Files are large. Default: do not ship a full file. Use a package that splits the font by character range, or use system faces.
- There is no italic. Mark emphasis with weight, with emphasis marks or with brackets.
- Default: body line-height 1.6 to 1.8. The characters fill the square and need more room.
- Count the measure in full-width characters. Default: 15 to 40 characters a line.
- Do not track body text. Proportional spacing for headings is a font feature in some Japanese faces.
- The same code point draws differently in Simplified Chinese, Traditional Chinese, Japanese and Korean. The `lang` attribute selects the form. A missing attribute shows the wrong form.
- Line breaking has rules about which characters may start or end a line. Leave them to the browser, with `lang` set.
- Korean breaks between words in most layouts. Default: `word-break: keep-all` for Korean headings.
- Latin text inside these scripts often looks small. Choose a Latin face with a large x-height, or scale it.
- Fewer weights exist. Plan the hierarchy with size and space.

## 4. Arabic, Hebrew and other right-to-left scripts

- Set `dir="rtl"` on the document or the block. The layout mirrors: navigation, alignment, progress, directional icons.
- Do not mirror media controls, clocks, phone numbers or brand marks.
- Arabic is a connected script. Never add tracking. Tracking breaks the joins.
- Neither script has capitals. A spaced all-caps label has no equivalent. Use weight, size or color.
- Neither script has an italic. Do not slant the text.
- Default: set Arabic 10 to 20% larger than the Latin beside it, and judge by eye.
- Default: line-height 1.6 to 1.8 for Arabic body text. Vowel marks need room above and below.
- Decide the numerals for each locale: Western digits or Eastern Arabic digits. Ask the user.
- Numbers and Latin words inside right-to-left text run left to right. Test mixed lines, with punctuation at both ends.
- Justification stretches joins in good Arabic typesetting. Default: do not justify on the web.
- Hebrew with vowel points needs extra leading.

## 5. Scripts of South and Southeast Asia

- Devanagari, Bengali, Tamil and related scripts stack marks above and below the base line. Default: line-height 1.6 to 1.8.
- Devanagari and Bengali join words under a head line. Never add tracking.
- Conjuncts need a font with full shaping support. Test the conjunct-heavy strings of the real copy.
- Default: set these scripts slightly larger than the Latin beside them, and judge by eye.
- Thai, Lao and Khmer write no spaces between words. Line breaking needs the `lang` attribute.
- Thai has looped and loopless styles. Default: a looped style for body text, because it reads more easily.
- Thai marks stack high. Check that the line box does not clip them.
- Bold weights are often heavy in these scripts. Use one step less than in Latin.

## 6. Cyrillic, Greek and extended Latin

- A face can list Cyrillic or Greek and still draw it poorly. Compare its letters with a face made for the script.
- Bulgarian and Serbian prefer local letter forms. The `lang` attribute selects them when the font has them.
- Check that the italic exists for the script. Cyrillic italic forms differ from the upright forms.
- Greek may need polytonic marks for some content. Ask.
- Vietnamese stacks two marks on one vowel. Check coverage and line-height with real strings.
- Languages with long compound words need hyphenation. Set `lang` and `hyphens: auto` on narrow columns.
- Capitals with marks need room. A tight display line-height can clip them.

## 7. Text expansion and layout

- A translation can run much longer than the English. Default: allow 30% more length, and far more for short labels.
- Test the longest real string of each language in each component.
- Buttons, tabs and table headers grow with their text. Do not set fixed widths.
- A wrap rule or a truncation rule exists for every label.
- Dates, numbers, currency and quotes follow the locale. Use the platform's formatter. Do not format by hand.
- Each language has its own quote marks. With `lang` set, the browser picks them for the `q` element.

## 8. Loading for more than one script

- Load a script's font only on pages that use the script. Use `unicode-range` in each `@font-face` rule.
- A package that ships range slices loads only the slices a page needs.
- The fallback for each script is a system face of that script. Name it in the stack.
- Fallback metric overrides apply to each script's pair of fonts. See the loading reference.
- Record every script font with `find-assets`. Each has its own license.

## 9. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Tofu | Empty boxes or fallback letters inside words | Check coverage with real strings. Change face or add a companion. |
| Fake italic | Slanted text in a script with no italic | `font-synthesis: none`. Use weight or marks for emphasis. |
| Broken joins | Tracked Arabic or Devanagari | Tracking 0 for connected scripts |
| Clipped marks | Vowel marks or accents cut at the line edge | Raise the line-height for that script |
| Wrong regional form | Characters drawn in another country's style | Set the `lang` attribute |
| Tiny companion | The second script looks smaller than the Latin | Scale the companion. Record the factor. |
| Mirrored by hand | Margins swapped with left and right properties | Use logical properties and `dir` |
| Latin rules everywhere | One line-height and one measure for all scripts | Write settings for each script |
| Unreviewed script | A script shipped with no reader review | Get the review, or report UNTESTED |

## 10. Worked note

A clinic booking app adds Arabic and Hindi to English.

- The main face is a humanist sans with no Arabic and no Devanagari.
- Its superfamily has matched families for both scripts. Route: superfamily.
- Mixed-line test: the Arabic looked small. It is set 12% larger. The factor is a rule in `DESIGN.md`.
- Line-height: 1.5 for English, 1.7 for Arabic and Hindi. Each is a token with a usage note.
- Labels in spaced capitals become bold labels in Arabic and Hindi.
- The layout uses logical properties. One Arabic screen is tested end to end.
- The report says: "Arabic and Hindi settings: UNTESTED. No reader of either language has reviewed the specimen."
