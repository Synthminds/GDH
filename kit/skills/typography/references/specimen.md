# The type specimen as the review artifact

Read this file at step 15 of `typography`. It covers what a specimen is for, its parts, how to build it, how to run the review round and the decision entry.

Evidence. Scoped rounds, same parts for each option, real copy and stable option names come from the GDH kernel and the Claude Design craft rules, read 2026-11-23. The blur, gray and five-second tests are rules of thumb. The verification split follows the kernel: rendered review for code, the type's own rule for an artifact type.

Terms. A specimen is one page that shows a type system on real copy. A comparison specimen shows two or three candidates side by side. A system specimen shows the chosen system in full.

## 1. Why a specimen

A list of font names decides nothing. The user must see the faces doing the real jobs: a heading, a paragraph, a form, a table, a number. The specimen is where the user says keep, change or remove. It is also the proof for the checks.

Two kinds:

| Kind | When | Shows |
| --- | --- | --- |
| Comparison specimen | Step 6, before the choice | Two or three pairings, same copy, same layout |
| System specimen | Step 15, after the scale and the setting | Every style, every theme, the stress strings, the loading facts |

## 2. Parts of the system specimen

Every part uses real project copy. Take it from the brief or the product. Never use placeholder text.

| Part | Content | Proves |
| --- | --- | --- |
| Header | Project, direction name, date, round number, each family with its source and license class | Provenance |
| Style ladder | Every style: its name, size, line-height, weight, tracking, and one real line | The scale and the role names |
| Reading block | The real headline, a lead, three real paragraphs with a list, a link and emphasis | Voice, measure, leading, stamina |
| Narrow and wide | The reading block at the smallest and the largest supported width | Fluid behavior and the measure at both ends |
| Interface block | A button, an input with a label and an error, a tab row, a table with numbers | That the text face works in controls |
| Numbers block | A column of prices, a date, a time that updates, a code or id | Tabular numerals and distinct glyphs |
| Stress strings | The longest heading, the shortest heading, a very long word, a URL, quotes and an ellipsis | Wrapping and detail rules |
| Languages | One real string for each language in the brief, at body size and at the smallest size | Coverage and the script settings |
| Themes | The reading block on each theme ground | Contrast and weight in each theme |
| Loading facts | Files, weights, subsets, total size, fallback stack | The loading plan |

Rules:

1. Print the token name beside each sample, not only the size.
2. Print the contrast ratio beside each text and ground pair. Take it from `DS contrast`.
3. Mark a part that you could not prove as UNTESTED on the page.
4. Keep the page self-contained. Do not link a remote stylesheet.
5. A font that is not yet licensed appears only in a comparison specimen kept inside the project. It never ships.

## 3. Parts of the comparison specimen

1. One column for each candidate. Two or three candidates.
2. The same parts in each column, in the same order: one headline, one paragraph, one interface row, one numbers row.
3. The same copy in each column.
4. A stable name and one idea sentence above each column. "A. Quay sign: one sturdy sans, wide for names."
5. One line under each column with its main tradeoff.
6. No recommendation inside the page. Give it in the reply, in a separate, labelled line.

Explore round: the candidates differ in idea, such as one family against a contrast pair. Refine round: the candidates differ in one attribute, such as the ratio or the display weight. Say which stage it is.

## 4. Build routes

Use the first route that fits.

| Route | When | How |
| --- | --- | --- |
| Token specimen | `design/tokens.json` holds the type family | `DS specimen design/tokens.json -o design/reviews/<date>-type-specimen.html` |
| Local HTML | A comparison, or parts the token specimen lacks | One self-contained HTML file with the fonts loaded from project files |
| Canvas artboards | Artifacts are available and the user wants to edit in place | One artboard for each candidate. Example card: [claude-design](../../../references/tools/claude-design.md) |

Notes:

- The token specimen shows what the tokens say. Add the reading block and the stress strings in local HTML when it lacks them.
- On a canvas, follow the type's own check rule. Do not render or screenshot to verify unless the user asks.
- For code, open the specimen in a browser. Review it at each breakpoint and in each theme. That is a gate.
- GATE: publishing a specimen, or sharing its link, exposes the brand. Get a yes first.

## 5. Check before you show it

Run these yourself first. Fix what fails. Then show the page.

1. Every size meets the minimum-size table in `SKILL.md`.
2. `DS contrast` passes for each text pair in each theme.
3. The reading block holds 75 characters a line or fewer.
4. The numbers block aligns. Set `1111` above `0000` to confirm.
5. No fallback glyph appears in any language string.
6. Blur test: blur a screenshot until the words cannot be read. The ranking of levels is still clear.
7. Gray test: remove color. The ranking is still clear.
8. Count the sizes on the page that one screen would show. Default: four at most.
9. The computed font is the chosen face in every sample.
10. Default: the tell scan of `design-critique` reports no type finding that the design system does not require.

## 6. Run the review round

Name the feedback you want. Ask about parts, not about the whole.

ASK, for a comparison specimen:

- "Which pairing sounds most like the brand words? Which sounds least like them?"
- "For each pairing: keep, change or remove the display face? The text face?"
- "Is anything missing that you expected to see?"

ASK, for a system specimen:

- "Voice: keep, change or remove?"
- "Hierarchy: are the first three things you read the right three?"
- "Reading comfort: is the paragraph easy on a phone and on a wide screen?"
- "Numbers and forms: keep, change or remove?"

Rules:

1. Quote the user's answer. Do not paraphrase it from memory.
2. Change only what the user asked to change.
3. A request that conflicts with a gate is not applied in silence. Say which gate. Ask.
4. A rejected face or pairing goes in the record with its reason. Do not propose it again.
5. Stop when the checks pass and the user approves. Do not polish further.

## 7. The decision entry

Write one entry in `design/decisions.md` for each round. The format is fixed.

```
## 2026-11-23 round 2: type pairing
Stage: explore
Shown: A. Quay sign (one family); B. Almanac (serif text, sans labels); C. Signal (condensed display, plain text)
Feedback asked: Which pairing sounds like "steady, coastal, exact"? Keep, change or remove each face.
Keep / Change / Remove: A text face: keep. A display style: change to the wider cut. B: remove. C display: remove.
Decision: A with the wide cut for place names (by the user)
Rejected: B: "reads like a newspaper, not a timetable". C: "too loud for a daily tool".
Open: Welsh diacritics at 12px need a reader's review.
Evidence: VERIFIED contrast on 6 pairs, measure 62 characters at 1240px. UNTESTED Welsh strings, font swap on a slow network.
```

## 8. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Alphabet page | The specimen shows the alphabet and a pangram | Use real copy and real components |
| Name list | Font names with no rendered text | Build the page |
| One option | A single pairing shown as the answer | Show two or three in an explore round |
| Unequal options | One candidate polished, the others rough | Same parts, same copy, same care |
| Which do you like | A question about the whole page | Ask about parts: keep, change, remove |
| Proof by claim | "Contrast passes" with no ratio on the page | Print the ratio from the script |
| Fallback specimen | The page renders in the fallback and nobody saw | Check the computed font first |
| Redesign on feedback | A small change request answered with a new system | Change only what was asked |
