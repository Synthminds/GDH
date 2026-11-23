# Directions: from brand words to comparable proposals

Read this file at steps 2 and 11 of `mood-board`. It covers how to find ideas, what each direction must hold, the spread rule, the skeleton list, the known default looks, two worked examples and the direction file format.

Terms. A direction is one coherent visual proposal with a stated idea. A part is one of the fixed sections of a direction. The category norm is the look that most products in the category share today. A known default look is a look that generated work repeats across categories. The word "Default:" keeps its kit meaning: a starting value. The board file stores the category norm in the field `categoryDefault`, and the script names it in its finding codes.

## 1. Turn brand words into attributes

The brief holds three brand words. Each has "means", "does not mean" and "shows up as". Extend each word into five channels. Write the table before you look at any reference.

| Brand word | Type | Color | Shape | Image | Motion |
| --- | --- | --- | --- | --- | --- |
| dependable (not corporate) | sturdy weights, tabular numerals | few colors, high contrast | square, aligned edges | real places, no models | short, exact, no bounce |
| local (not touristy) | a face tied to the place or the trade | colors seen at the site | forms from local objects | the actual harbour | pace of the place |
| plain-spoken (not cute) | one family, no display tricks | no decorative tints | no ornament | diagrams over mood shots | one move, then still |

Then set each word on an opposites scale. Write the scale as a pair: calm to urgent, classic to modern, dense to airy, quiet to loud, engineered to natural. Mark where the brand sits. The adjectives of a direction come from these scales.

Rule: a row that would fit any brand is not finished. "Clean, modern, friendly" describes every product. Replace it with what the word means here.

## 2. Find ideas, not styles

An idea is a claim about what the product is like. A style is a set of surface choices. Directions differ in idea.

Look for ideas in this order:

1. The subject's own objects: its tools, documents, signs, packaging, uniforms, instruments. For software, the product's own output counts: logs, diffs, transcripts, receipts.
2. The subject's materials and places: what it is made of, where it is used, in what light.
3. The subject's rituals: what people do before, during and after they use it.
4. A metaphor that explains the product to a first-time user.
5. A behavior: one thing the interface does that no competitor does.

List five to ten concrete things from the subject's world before you draft. Each direction must trace to one of them.

Write each idea as one sentence. Then run three tests on the sentence:

- The no-color test. The sentence names no color, no font and no effect. "Dark with neon accents" fails. "The ticket is the interface" passes.
- The swap test. Put a competitor's name in the sentence. If it still fits, the idea is the category norm. Rewrite it.
- The consequence test. The idea forces at least one choice in each part. If it changes only the palette, it is a skin.

Draft the directions apart. Write the first one in full before you start the second. A direction that reacts to another ("like A, but warmer") is a variant. Variants belong to `refine-round`.

## 3. The parts of a direction

Every direction holds the same parts, so that the user can compare them part by part.

| Part | Write | The test that proves it |
| --- | --- | --- |
| Name | Two or three words that name the idea | The name holds no color word. It stays the same in every round. |
| Concept sentence | One sentence: what the product is like | It passes the three tests in section 2. |
| Three adjectives with opposites | "exact, not approximate" | Each pair comes from a brand-word scale. No pair is shared with another direction. |
| Palette | Four to six named colors with roles: bg, text, muted, accent, on-accent | Text on bg is 4.5:1 or more. Each color has a reason from the idea. |
| Type pairing | Display and body face, each with a stack and a fallback; the class of the display face | The specimen shows the real headline, a body line and numerals. The license is noted. |
| Imagery and texture | What pictures show, how they are made, what the surface feels like | A builder can tell a fitting image from a wrong one with this text alone. |
| Layout and shape | A skeleton from the list in section 5, plus corners, rules and edges | The skeleton differs from the category norm's skeleton. |
| Motion character | What moves, how, and what happens with reduced motion | One sentence names the single authored moment. |
| Signature element | The one thing a person will remember | It appears in the sample or can be described in one line. Only one. |
| Sample | One hero or one card in real copy | The same copy sits in every direction. No placeholder text. |
| Difference lines | One line against the other directions, one against the category norm | Neither line needs a color word. |

Numbers in this table: the 4.5:1 ratio is a gate (kernel rule 12). "Four to six colors" and "two families" are defaults from published design guidance.

Notes on the parts:

- Palette. Name colors by what they are in the subject's world: "ticket stock", "signal amber". Decide light or dark ground from the use scene: who, where, in what light. Do not decide it from the product category.
- Type. Choose the body face first and read real copy in it. A default family (Inter, Roboto, Arial, a system stack) needs a reason from the brief. Monospace fits code, data and measurement.
- Signature. Spend boldness in one place. Keep the rest quiet. Two signatures compete.
- Sample. Low fidelity is enough to choose. Do not build a full page. Do not generate paid images for a sample unless the user agreed.

## 4. The spread rule

Default: one safe, one expected, one outside the safe zone. This rule comes from agency practice reported in secondary pages. Treat it as a default.

| Spread | Meaning | Test |
| --- | --- | --- |
| safe | Closest to the current brand or to what the audience knows | A current user would recognize it at once. |
| expected | A clear step away, still inside what the brief implies | It changes at least one of layout skeleton or type class against the safe one. |
| outside | Leaves the safe zone on purpose | It breaks two or more named category conventions. It still answers the primary job on the first screen. |

Rules:

- The outside direction is a real proposal. It is not a decoy that makes the safe one look good.
- With two directions, one of them is outside.
- With four, add a second expected direction built on a different idea.
- A strict design system narrows the spread. Then state which parts are fixed, and spread the parts that are open.
- When the user gives no directional feedback after one round, add one direction labelled "provocation". It breaks one stated assumption of the brief.

## 5. Vocabulary for the uniqueness test

`moodboard.py diff` compares three fields. Fill them with these terms, so that equal things get equal names.

Type class, for the display face: `humanist-sans`, `grotesque-sans`, `neo-grotesque-sans`, `geometric-sans`, `rounded-sans`, `condensed-sans`, `old-style-serif`, `transitional-serif`, `modern-serif`, `slab-serif`, `mono`, `script`, `blackletter`, `display`.

Layout skeleton, a closed list. Use one of these names exactly:

| Skeleton | Shape |
| --- | --- |
| `centered-stack` | One centered column of blocks |
| `hero-split` | A hero with text on one side and media on the other, then sections |
| `split-screen` | Two equal panes for the whole screen |
| `asymmetric-split` | Two unequal panes, one dominant |
| `editorial-columns` | Several text columns with rules, as in print |
| `single-column-longform` | One reading column, long text |
| `full-bleed-media` | Edge-to-edge pictures or video carry the page |
| `poster-type-led` | Very large type is the main shape |
| `sidebar-shell` | A fixed side navigation and a work area |
| `chat-thread` | A message thread with an input at the bottom |
| `card-list` | One column of similar cards |
| `card-grid` | A grid of cards of one size |
| `bento-grid` | A grid of cards of mixed sizes |
| `object-stack` | Overlapping objects, such as tickets or sheets, that the user flips |
| `table-led` | Rows and columns carry the content |
| `timeline-rail` | A line in time with marks on it |
| `map-led` | A map carries the content |
| `canvas-led` | A free surface where items are placed and moved |

Rules:

- The idea's own name for its layout goes in `layout.notes`. The skeleton field holds the list name.
- When no name fits, take the nearest and write the difference in `layout.notes`. Propose a new name in the skill's refinement log.
- A coined name hides a clone from `diff`. Two directions with one layout under two names are near-identical.

Palette family is computed. It is the hue of the accent color plus the ground, light or dark.

A check that reads no labels. `diff` trusts the names you type. Read each pair yourself as well:

- Default: when two concept sentences share half or more of their content words, the pair states one idea. Treat it as near-identical.
- When the adjectives or the sample copy of two directions are the same, treat the pair as near-identical.
- When every swatch of one direction looks like the matching swatch of the other, the pair shares one palette.

Replace one idea. Do not rename a field to pass.

## 6. Known default looks

Generated work repeats a few looks in every category. Check each direction against this table, as well as against the category norm. The table is dated 2026-11-23. The tell list in `design-critique` names the same looks. Refresh both together.

| Look | Ground | Accent, OKLCH hue | Type class | Skeleton |
| --- | --- | --- | --- | --- |
| Warm editorial | light, cream | terracotta or orange, 20 to 60 | `old-style-serif`, `transitional-serif`, `modern-serif` | `editorial-columns` |
| Night signal | dark, near-black | acid green, 110 to 150; or vermilion, 15 to 45 | `grotesque-sans`, `neo-grotesque-sans` | `split-screen`, `asymmetric-split` |
| Violet tech: gradient, glass, glow | light or dark | indigo to magenta, 265 to 330 | `geometric-sans` | `card-grid`, `bento-grid`, `hero-split`, `chat-thread` |
| Blue product | light, white | blue, 240 to 270 | `geometric-sans`, `neo-grotesque-sans` | `hero-split`, `card-grid`, `card-list` |

Default: the hue bands. They follow the palette-family threshold and are a rule of thumb.

The match rule. A direction matches a look when it shares the palette family plus the type class or the skeleton. The palette family is the ground side plus an accent hue inside the band. A match fails the board. The exception: `allowCategoryDefault` holds a reason from the brief, and the decision record logs it.

Also count a match when the direction uses a gradient, glass or glow as its signature, unless the design system requires it. Report a required habit as `brand-required`.

## 7. Worked example: a physical subject

Brief: a timetable and ticket app for one island ferry line. Audience: daily commuters and first-time visitors, outdoors, one hand on a rail. Primary job: see the next sailing and know that it runs. Brand words: dependable, local, plain-spoken.

Category norm: a blue brand color on a white ground, a geometric sans, a feed of rounded cards under a map.

Things from the subject's world: the quay-side departure board, the printed tide table, the paper ticket and its punch, pier numbers painted on bollards, the harbour light, wind warnings.

| | A Departure Board (safe) | B Tide Line (expected) | C Punched Ticket (outside) |
| --- | --- | --- | --- |
| Idea | The quay board in your pocket: sailings are rows | The day is one line, like a tide chart | The ticket is the interface |
| Adjectives | exact, public, steady | calm, natural, spacious | tactile, frank, owned |
| Ground and accent | chalk ground, signal amber fills | sea-mist ground, harbour green | ticket-stock ground, date-stamp red |
| Type class | grotesque-sans (signage) | transitional-serif (almanac) | slab-serif with printer mono |
| Skeleton | table-led | timeline-rail | object-stack (the ticket stack) |
| Signature | one full-width split-flap row | the tide line with a marker for now | the punch hole in a used ticket |
| Main tradeoff | can feel like any transit board | a visitor needs one line of help | the timetable is one tap away |

Why this board passes:

- Each idea comes from a different object: the board, the tide table, the ticket.
- Each idea forces every part. C needs card stock, stamped type and a stack. It could not use A's table.
- No difference line needs a color word. "A lists rows. B draws the day. C gives you an object."
- The mono face in C prints times, as a ticket printer does. It is data, not a costume.
- The amber in A is 1.68:1 on its ground. The board marks it "fills only". Dark text sits on it at 9.77:1.

The same brief, done badly:

- "Ocean Blue", "Sunset Coral", "Forest Green": one card feed in three accent colors. The diff fails, and the board teaches the user nothing.
- "Minimal", "Bold", "Playful": three intensities of one layout. No idea is stated.
- Near-black with one bright accent, cream with a serif, and a glass card kit: the known default looks of section 6. None comes from a ferry. Each one fails the match rule.

The filled board for this example is the template file `templates/board.json`.

## 8. Worked example: an abstract subject

Software has no quay and no ticket. Its world still holds objects. Look in four places:

- The users' workplace and documents: the files they open, the forms they fill, the room and the hour.
- The product's own output: diffs, logs, transcripts, receipts, the record it leaves behind.
- The rituals of the workflow: what happens before, during and after the product does its job.
- The data: the counts, units and time codes that the users argue about.

Brief: an AI assistant that turns recorded customer interviews into findings for a product team. Audience: a product researcher at a small software company, between calls, who must convince engineers. Primary job: turn this week's interviews into findings the team trusts. Brand words: traceable, candid, collegial.

Category norm: a chat thread beside the document on a white ground, a violet to indigo gradient, a geometric sans, a sparkle icon on every AI action. It also matches the violet tech look of section 6.

Things from the subject's world:

- Workplace and documents: the interview guide, the consent form, the shared research sheet, the readout deck.
- The product's output: the transcript with time codes, the tagged quote with speaker and minute, the finding with its count.
- Rituals: the debrief after each call, the affinity session with notes on a wall, the readout where an engineer asks "who said that?".
- Data: people per finding, quotes per tag, minutes of audio.

| | A Marked Transcript (safe) | B Evidence Wall (expected) | C Tally Ledger (outside) |
| --- | --- | --- | --- |
| Idea | Every finding is a highlight you can play from its time code | Findings are notes on a wall; the assistant proposes clusters, people move them | Every finding is a claim with its tally of people, like a ledger line |
| From the subject's world | the transcript and the highlighter | the affinity session | the readout question "how many said it?" |
| Adjectives | traceable, quiet, close | collegial, loose, visible | candid, counted, terse |
| Ground and accent | printout white, highlighter yellow fills | foam-board gray, pin red | ledger white, tally green |
| Type class | humanist-sans (reading) | grotesque-sans (marker labels) | mono (counts and time codes) |
| Skeleton | single-column-longform | canvas-led | table-led |
| Signature | the time-code tab that plays the clip | the cluster the assistant proposed, outlined until a person accepts it | the tally column, "7 of 9", before every claim |
| Main tradeoff | slow for a reader who wants the summary | needs space; weak on a phone | blunt; a weak finding shows its low count |

How each one avoids the default looks:

- No gradient, glass or glow. Each accent is one flat color with a role: a highlight, a pin, a tally.
- No chat thread as the skeleton. The assistant's work lands in the team's own objects: a transcript, a wall, a ledger.
- No sparkle icon. An AI action is a named verb: "Cluster", "Find the quote", "Count".
- No cream and serif. A uses a cool printout white and a humanist sans.
- B shares the palette family of the warm editorial look: light ground, red accent at hue 28. It shares neither type class nor skeleton, so it passes the match rule.

The scratch board for this example passed `diff` with three distinct pairs, and each direction shares nothing with the category norm. Contrast: ink on the highlighter is 12.34:1; pin red text on foam board is 4.54:1; tally green on ledger white is 5.58:1. The highlighter is 1.27:1 on its ground, so it is a fill only.

The same brief, done badly: a chat window with a purple gradient header, glass cards of "insights", and a sparkle on the summarize button. Swap in any competitor and nothing changes.

## 9. Failure patterns

| Pattern | How to see it | Counter-move |
| --- | --- | --- |
| Three skins | The concept sentences differ only in color or mood words | Return to section 2. Pick three different objects from the subject's world. |
| The collage | Pretty images, no type, no layout, no rule a builder could follow | Fill every part. A direction is a proposal for the system, not a feeling. |
| The decoy | The outside direction is weak on purpose | Give each direction equal effort and an honest tradeoff. |
| One gallery | Every reference comes from one showcase site | Add references from the subject's own world and from outside the category. |
| The costume | Grain, serif or mono added with no link to the subject | Name the object in the subject's world that the choice comes from. If none exists, remove it. |
| The fashion pick | A reference appears only because it is current | Drop it. Ask what it says about this subject. |
| The default look | A direction matches a look in section 6 or the category norm | Run the swap test and the match rule. Rewrite the idea. |
| The early polish | A full page built for each direction | Stop at one hero or one card. Polish closes the conversation. |

## 10. The direction file

Write one file for each direction at `design/directions/<n>-<name>/direction.md`. Keep rejected directions. They stop later work from drifting back.

```
# Direction <letter>: <name>

Status: proposed | chosen | rejected | merged into <name>
Spread: safe | expected | outside
Round: <n>, <date>

## Idea
<the concept sentence>
From the subject's world: <the object, material or ritual it comes from>

## Character
<word>, not <opposite>. <word>, not <opposite>. <word>, not <opposite>.

## Palette
| Role | Name | Hex | Reason |

## Type
Display: <family>, <class>, <stack>. Body: <family>, <stack>. License: <read on date | to read>.

## Imagery and texture
## Layout and shape
Skeleton: <name from section 5>. Notes: <the idea's own name for the layout>.
## Motion
## Signature element
## Sample
<path to the sample file>, built with the copy "<headline>".

## How it differs
From the other directions: <one line>
From the category norm: <one line>

## Tradeoff
<the main cost of this direction>

## References
| File | Source | Terms | What to take |

## Feedback
Round <n>: <keep / change / remove for each part, in the user's words>
```

When a direction is chosen, `design-system` reads this file and writes tokens and `DESIGN.md`. The direction file stays as the record of why.
