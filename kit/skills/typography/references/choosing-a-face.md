# Choosing a face from the subject and the brand words

Read this file at steps 1 to 4 of `typography`. It covers the type brief, the attribute table, the classifications, the hard filters, the test on real copy, the failure patterns and four worked choices.

Evidence. The "subject first" rule and the two-family limit come from the Anthropic frontend-design skill, read 2026-11-23. The attribute table and the classification table are common typographic practice written from memory. Treat both tables as defaults. A choice is UNTESTED until you see the face on real copy.

Terms. A face is one typeface family. A text face sets running text. A display face sets headings. Coverage is the set of languages a face can set with its own glyphs.

## 1. Write the type brief

Write six lines before you open a font catalog.

| Line | Write | Example |
| --- | --- | --- |
| Subject | What it is, and five type objects from its world | A tide table app. Harbour signs, chart legends, ferry tickets, engine plates, a paper almanac. |
| Brand words | Three words, each with its "not" | steady, not stiff; coastal, not nautical-themed; exact, not cold |
| Reading mode | For each surface: long read, scan or glance | Timetable: glance. Notices: scan. About page: long read. |
| Languages | Every content language and script | English and Welsh. Latin with extended diacritics. |
| Media | Web, app, slide, print, chart | Mobile web first. One printed poster. |
| License limits | Public repository, host, client hand-over, budget | Public repository. No budget for fonts. |

Rules:

1. Take the brand words from `design/brief.md`. Do not invent new ones.
2. Take the five type objects from the subject. Ask the user for photos when you have none.
3. A type object is evidence, not a face to copy. Note its structure: width, weight, contrast, terminals.
4. An unknown language list blocks the choice. ASK before you shortlist.

## 2. Turn each brand word into attributes

A brand word alone picks no face. Translate it into letterform attributes first.

| The word points to | Look for | Avoid |
| --- | --- | --- |
| warm, human, handmade | Humanist construction, open apertures, some stroke modulation, a true italic | Rigid geometry |
| exact, engineered, systematic | Even stroke, clear digit shapes, tabular numerals, plain terminals | Quirky display detail |
| calm, quiet | Regular width, moderate x-height, low contrast, regular weight | Condensed widths, heavy weights |
| urgent, energetic | Condensed width, heavy weight, tight leading | Wide and light styles |
| trusted, established | Old-style or transitional serif, moderate contrast | Novelty faces |
| refined, luxurious | High stroke contrast, small x-height, spaced capitals | Small sizes, where hairlines break |
| sturdy, direct | Slab serif or grotesque, strong horizontals | Hairlines |
| friendly, approachable | Large x-height, round terminals, open counters | Sharp terminals; childish forms |
| rational, modern | Geometric construction, even widths | Long reading, where similar round letters tire the eye |
| local, of a trade | A structure seen in the subject's own type objects | A neutral face with no tie to the subject |

Rules:

1. Write one row for each brand word. Write the attribute, not a face name.
2. Use the "not" of the word to cut. "Coastal, not nautical-themed" cuts rope scripts and stencil faces.
3. Two words can pull apart. "Exact" and "warm" may need two faces. Note it for the pairing step.
4. A row that fits every brand is not finished. "Clean and modern" describes most faces.

## 3. Name a classification

Name one classification for the text face. Give the reason in one sentence that cites a brand word or a type object.

| Classification | Structure | Reads as | Strong at | Risk |
| --- | --- | --- | --- | --- |
| Old-style and humanist serif | Angled stress, bracketed serifs, low to moderate contrast | Bookish, trusted, warm | Long reading | Looks dated when set tight and small on screen |
| Transitional serif | Vertical stress, sharper serifs | Serious, institutional | Reports, news | Can feel stiff |
| High-contrast serif (didone) | Hairline serifs, strong thick and thin | Fashion, luxury | Large display sizes | Hairlines vanish at text sizes |
| Slab serif | Thick block serifs, low contrast | Sturdy, direct, mechanical | Headlines, labels | Heavy in long text |
| Humanist sans | Pen-based shapes, open apertures | Warm, clear | Interfaces, long reading on screen | Less neutral; carries a voice |
| Grotesque and neo-grotesque sans | Closed apertures, even widths | Neutral, industrial | Dense interfaces, signage | The category default of software |
| Geometric sans | Circles and straight lines | Rational, modern, friendly | Short display lines, logos | Similar letters; weak in long text |
| Monospace | Fixed advance width | Technical | Code, data, measurement | A costume when used for brand voice |
| Script and display | Drawn for one effect | A specific mood | One line | Fails as text; ages fast |

Decision rules:

1. Long read: choose a serif or a humanist sans with open apertures and a true italic.
2. Glance and scan with many numbers: choose a face with clear digits and tabular numerals.
3. Dense interface: choose a face with a large x-height and several weights.
4. Display only: any classification can work. Test it at the real size and with the real words.
5. Use monospace only for code, data and measurement.

## 4. Apply the hard filters

Reject a face on a filter before you judge its voice.

| Filter | How to check | Reject when |
| --- | --- | --- |
| Coverage | Set the hardest real strings of each language | Any glyph falls back to another font |
| Styles | List the weights and italics the scale needs | A needed weight is absent, or the italic is a slanted roman |
| Numerals | Set `1111` above `0000` in a column | The two lines differ in width and the product has data columns |
| Confusable glyphs | Set capital I, lowercase l, digit 1; capital O, digit 0; `rn` beside `m` | Pairs cannot be told apart and the product shows codes or ids |
| Small sizes | Render 12px and 14px on a normal-density screen | Counters fill in or strokes break |
| License | Read the license class against hosting and repository | The class forbids the planned use |
| Weight | Add up the files the design needs | The total breaks the loading budget |

Record each rejected face with its filter in `design/decisions.md`. Do not propose it again.

## 5. Test on real copy

Test each shortlisted text face with the same five strings. Use real project copy.

1. One paragraph of real body copy at body size and at the planned measure.
2. The longest real heading and the shortest real heading.
3. A set of interface strings: a button, a label, an error message, a table row.
4. A numbers block: prices, dates, a phone number, a column of figures.
5. The hardest string of each extra language.

Look for four things:

- Even color. The paragraph reads as an even gray with no dark spots and no rivers.
- Word shapes. Words separate cleanly at body size.
- Voice. The paragraph sounds like the brand words when you read it.
- Stamina. The third paragraph is as easy as the first.

Run two tests on the survivor:

- The swap test. Would this face fit any competitor without change? If yes, write what the face adds for this subject. With no answer, choose again.
- The blind test. Default: show the specimen without the brand words. Ask for three adjectives. Compare them with the brand words.

Then choose the text face. Choose a display face only after that. A display face must do a job that the text face cannot do.

## 6. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Default face | The most common interface sans in every role, with no reason from the brief | Write the attribute table. Choose from it. |
| Fashion swap | One popular face replaced by this season's popular face; nothing else changed | Run the swap test. Tie the face to a type object. |
| Costume | Serif, monospace or texture used to signal "editorial" or "technical" | Name the link to the subject or remove it |
| Display first | The headline face was chosen first; body text then fails | Start again from the text face |
| System face as voice | The brand face was never sourced; the fallback renders | Source the font or choose one you can source |
| Ransom note | Four or more families on one screen | Cut to two. Give each a role. |
| Thin body | A light weight at text sizes | Use 400 or more, unless the design system requires the light weight |
| Missing glyphs | Fallback letters inside words of a second language | Check coverage first |
| Accent word | One headline word in italic or a second color as the only idea | Remove it, or make the idea structural |
| Label habit | A tracked all-caps label above every heading | Keep a label only where it carries information |

A habit that the design system requires is not a failure. Report it as `brand-required`.

## 7. Worked choices

The outcomes below are illustrative. They show the reasoning. Confirm coverage and license on each family's own page.

Tide table app. Brand words: steady, coastal, exact. Reading mode: glance. Many numbers. Public repository.

- Attributes: even stroke, clear digits, tabular numerals, open apertures, sturdy weights.
- Classification: humanist sans. Reason: harbour signs are plain sans capitals, and "steady, not stiff" asks for open shapes.
- Filters: tabular numerals and a capital I that differs from lowercase l decide the shortlist.
- Method: one family. A condensed or heavy style of the same family sets the place names, as on a quay sign.
- Rejected: a geometric sans, because its digits and round letters look alike at a glance.

Legal aid clinic site. Brand words: plain, on your side, serious. Reading mode: long read. Languages include one with stacked diacritics.

- Attributes: moderate contrast, sturdy serifs, large x-height, a true italic for case names.
- Classification: transitional serif for text. Reason: legal documents are serif text, and "serious, not cold" excludes a high-contrast face.
- Filters: coverage decides. One candidate lacks the stacked diacritics: rejected.
- Method: superfamily. The matching sans sets forms and navigation.
- Rejected: a high-contrast serif, because hairlines break at 16px.

Brass band festival. Brand words: loud, communal, a bit rough. Reading mode: glance on posters, scan on the site.

- Attributes: condensed width, heavy weight, slightly irregular edges.
- Classification: condensed grotesque for display. Reason: the festival's old letterpress posters use wood type of that structure.
- Method: contrast pair. A plain, wide grotesque sets the programme, where times and names must scan.
- Filters: the display face has one weight. That is enough, because it never sets text.
- Rejected: a script face, because it reads as a wedding, not a band.

AI interview findings assistant. The subject is the one in `mood-board`, directions reference, section 8, and the color reference, section 10. Brand words: traceable, candid, collegial. Reading mode: long read for transcripts, scan for findings. Many time codes and counts. Public repository. English only.

- Type objects from the subject: the printed transcript, the interview guide, the research sheet, the readout deck, the time code on a recording.
- Attributes: open apertures for long reading, a true italic for quoted speech, tabular figures for time codes and tallies, a regular width.
- Classification: humanist sans for text. Reason: transcripts are read for an hour at a time, and "collegial, not cosy" asks for a warm but plain voice.
- Shortlist: three humanist sans faces from the `find-assets` font shortlist. Filters: tabular figures decide first, then a true italic. A face with "Check" for figures stays only after the specimen shows `tabular-nums` working.
- Method: one family. Time codes and tallies use the tabular figures of the text face, not a monospace face. A monospace face here would be a costume, and `TELL_MONO_LABELS` would flag it on labels.
- Rejected: an interface sans from the overused list, because no line of the brief gives a reason for it. Also rejected: a geometric sans, because its round letters tire the eye in long transcripts.
- Evidence: UNTESTED. No candidate was rendered on real transcript copy for this example.
