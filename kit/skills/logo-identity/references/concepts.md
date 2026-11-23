# Rough concepts in black, culling and presenting

Read this file at steps 5, 7 and 8 of `logo-identity`. It covers the quantity rule, black-first drawing, how an agent sketches, the concept sheet, the cull, the three directions, the presentation and the review round.

Evidence. "Sketch many ideas fast in black, at thumbnail size, with no color or effects" is attributed to Aaron Draplin's public teaching and is recalled, not re-read. The three criteria (appropriate, distinctive, simple) are attributed to Sagi Haviv and come from secondary pages. The seven questions attributed to Paul Rand come from secondary reports with varying wording. "Show two to four options that differ in idea" and "same parts, real copy" come from the GDH kernel. Every count in this file is a default.

Terms. A concept is one rough drawing of one idea. A direction is a concept developed enough to compare: drawn cleanly in black and shown in context. A seed is a line that names what to draw.

## 1. Quantity before refinement

1. Default: thirty rough concepts or more, from five different seeds or more.
2. Spend minutes on each, not hours. A rough concept answers one question: is there an idea here?
3. Do not refine a concept before the cull. Refinement hides weak ideas and wastes strong ones.
4. Draw the obvious ideas first and set them aside. The field has used them.
5. Push each seed three ways: as letters, as a symbol, as a system.
6. Stop when new concepts repeat old ones. Then draw five more.

Why quantity: the first ideas are the ones every competitor also had. A distinctive idea usually sits past them.

## 2. Black first

1. Draw every concept in solid black on white. No gray, no color, no gradient, no shadow, no texture.
2. Draw small. Default: each concept fits a 64px square on the sheet.
3. Use closed shapes. A hairline that needs a large size is not part of a rough concept.
4. Judge the silhouette. Fill the concept solid in your mind: is the outline still that mark?
5. Color comes last, after the black mark passed its tests. An idea that needs color to work is not yet an idea.

Reason: one-color use is the hardest test and it is unavoidable. Stamps, stencils, engraving, a single-ink print, a favicon in a dark tab. A mark that works in black gains from color. A mark that needs color fails without it.

## 3. How an agent sketches

Write each concept as a small SVG. Use few shapes and round numbers.

1. Use one `viewBox` for every concept, for example `0 0 64 64`.
2. Build from rectangles, circles, lines with a thick stroke, and simple paths.
3. Use `fill="black"` only. A stroke is allowed in a sketch and is outlined later.
4. For a wordmark concept, set the name in a licensed or system face as a stand-in. Mark it "stand-in letters". Describe the one change you would draw.
5. Do not polish curves. A sketch may be crude. It must be clear.
6. Write one line under each concept: its seed and its idea.
7. Tile the concepts on one page: the concept sheet. Number them. Keep the numbers for the whole project.

Check the sheet as rendered before you show it. A code deliverable is reviewed as rendered. On a design canvas, follow the canvas type's own check rule.

A generated image can widen this pool. It is for ideation only and is a spend call. Read the generation reference first.

## 4. The concept sheet

| Part | Content |
| --- | --- |
| Header | Project, date, round, the three brand words, the avoid list |
| Grid | Every concept at one size, in black, numbered |
| Caption | Seed and idea in one line for each |
| Small row | The strongest ten again at 16px and 32px |
| Field row | The competitor marks at the same height, as reference |

Save the sheet under `design/directions/`. It is the record of the search. Rejected concepts stay on it, crossed out, with a reason.

## 5. The cull

Cull in three passes. Write the reason for each cut.

Pass 1, at 16px. Look at every concept at 16px. Cut what turns into a blob or reads as another thing.

Pass 2, three criteria. Score each survivor yes or no:

| Criterion | Question | Common wrong reading |
| --- | --- | --- |
| Appropriate | Does the form feel right for this organization and this field? | It does not have to show what the organization does |
| Distinctive | Would a person recognize it among the competitor marks and describe it afterward? | Unusual is not enough; it must be describable |
| Simple | Does it survive tiny sizes, one color and rough reproduction? | Simple is not empty; one idea remains |

Keep concepts with three yes answers. A concept with two may stay as a wild card.

Pass 3, against the field. Put each survivor on the competitor sheet. Cut what could be mistaken for a neighbor.

Further questions for a tie. Is it visible at a distance? Does it adapt to a square, a wide and a tall space? Will it look dated when today's fashion passes? Could a person draw it from memory?

## 6. Choose three directions

1. Default: three directions. Two when the brand rules are strict. Four at most.
2. The three differ in idea, not in styling. Three weights of one monogram are one direction.
3. Test: describe the difference between two directions in one sentence that names no color and no font.
4. Spread them: one close to what the field expects, one further, one bold.
5. Name each direction with two or three words. The name holds no color word. It never changes.
6. Write one concept sentence for each: what the mark says about the organization.

## 7. Develop each direction for the presentation

Develop all three to the same level. Still in black.

1. Redraw the concept with cleaner geometry. Full construction waits until one is chosen.
2. Set or draw the wordmark beside or under it. Use the real name.
3. Show each direction in the same five contexts, in black and white:

| Context | Why |
| --- | --- |
| The mark alone, large | The idea |
| The lockup at 16px, 32px and 64px | Survival at small sizes |
| An app icon or avatar square | The square form |
| A page header with real navigation words | Use beside text |
| One hard use from the brief: a stamp, a sign, an embroidered patch | The real constraint |

4. Use real words from the brief. No placeholder text.
5. A mockup generated by an image tool is a spend call. It shows context. It is not the mark.
6. Do not show a direction you would not stand behind. It may be chosen.

## 8. Present and ask

1. Show the three with equal care, on one board, in black.
2. State each idea in one sentence and its main tradeoff in one line.
3. Give your recommendation in a separate, labelled line, after the three.
4. ASK about parts:

- "For each direction: is the idea right for the organization? Keep, change or remove."
- "The mark: keep, change or remove?"
- "The letters: keep, change or remove?"
- "Which direction is the base?"

5. Quote the answers in the decision record.
6. A request to merge two directions makes a new direction. Name it, draw it, test it and show it again.
7. A request for color at this stage: explain that color is added after the black mark passes. Offer one neutral color preview if the user insists, and label it a preview.
8. Record the rejected directions with reasons. Do not propose them again.

## 9. Refine rounds after the choice

1. One direction is the base. Each round names what it wants feedback on.
2. Variants in a refine round differ in one attribute: the weight, or the letter spacing, or the corner.
3. Show each variant at 16px and at large size, side by side.
4. Change only what was asked. The idea stays.
5. Stop when the black tests pass and the user approves. Then build the system.

## 10. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Three of one | Three directions that are one idea in three styles | Return to the seeds. Pick different ideas. |
| Early polish | One concept refined before the others exist | Finish the quantity pass first |
| Color crutch | The idea depends on a gradient or two colors | Redraw in black. If nothing is left, drop it. |
| Literal picture | The mark shows the product | Use the part, the action or the letter link |
| Generic geometry | A circle, a hexagon or an abstract swoosh beside a default sans | Tie the form to a seed from the subject |
| Clever and unreadable | A hidden idea nobody sees, and a form nobody can describe | The plain reading must work first |
| White page only | The mark shown alone, never in use | Show the five contexts |
| Which do you like | A vote on whole boards | Ask about idea, mark and letters |
| Compromise mark | Parts of all three merged into one | A merge is a new direction. Test it as one. |
| Favourite straw man | Two weak options beside the one the agent wants | Show only directions you would ship |
