# Craft of the Slides type

Read this file at step 12 of `claude-design` when the type is Slides. It restates the deck type's story, type, color, space, image, motion and export rules in my own words, with GDH failure patterns and a worked outline.

Evidence. Rules come from the Slides type's rule file and its craft, layout, styles, fonts, images and diagrams references, read 2026-11-23: DOCUMENTED. Sizes in px are the type's own. No deck was built for this kit; export behavior is UNTESTED.

Terms. A deck is one Slides artifact. A content slide has a heading and a body. A statement slide carries one large idea.

## 1. Stance

You design posters that a room reads from the back, not web pages. Each slide is fixed. Nothing scrolls and nothing shrinks to fit. When content does not fit, split the slide.

## 2. Story first

1. Write the outline before any slide. The titles alone must tell the story.
2. Share the title list in the chat before or while you build.
3. Use one grammar for all titles: topic titles, or action titles. Not a mix.
4. A title introduces the slide. Avoid fake tension, verdicts and heavy reframing.
5. One idea per slide. A statement beats bullets. Several short slides beat one crowded slide.
6. Turn text into structure: a table, a diagram, a quote, an image, a row of cards, a big number.
7. Default: keep a deck under about fifty slides.

Speaker notes: add them only when asked. Then the deck becomes visual-first and the notes carry the spoken script.

## 3. Type

| Rule | Value from the type |
| --- | --- |
| Sizes for the whole deck | Four or five, for example 120, 72, 44, 32, 24 px |
| Floor | Never under 24 px. Text that fits only at 20 px is too much text |
| Display line height | About 1.05 to 1.15, with negative tracking |
| Body line height | About 1.3 to 1.45 |
| Faces | Two is the norm. A third needs a clear job. The type caps the face count |
| Emphasis | Weight, italic or color, never a new size |
| User sizes | A size the user gives is in points. The type converts at 2 px per point |
| Quotes | Typographic quotes and apostrophes in reader-facing text |

Eyebrow labels: the type gives a small caps style for them. GDH precedence applies: use them when the design system wants them; otherwise ask whether the slide needs one.

## 4. Color

1. Choose colors once: one dark, one light, zero to two accents that share chroma and lightness. Tone whites and blacks toward the palette.
2. Two ground tones per deck plus one accent statement slide. Set the ground on every slide.
3. Default rhythm: dark to open and close, light for content, accent for the one thing to remember.
4. Body text 4.5:1. Display 3:1. Dark text on a light accent.
5. Color never carries meaning alone. State the status in words.

## 5. Space

| Rule | Value from the type |
| --- | --- |
| Margins | 128 px on a 1920 x 1080 slide, leaving the inner area |
| Body column | 800 to 1000 px wide |
| Display line | About 1400 px wide |
| Heading position | At the top margin, at the same height on every content slide |
| Fill | About 70% of the column, or spread with space-between or a flexible spacer |
| Footer | One pinned row near the bottom; that slide takes extra bottom padding |

Height budget, before you write a slide:

- A heading takes about size x lines x 1.1.
- A table row takes about 2.1 x font size per text line.
- Never set a fixed height smaller than the content.

Rules:

1. Never center a column that has a heading above its body. The heading then jumps between slides.
2. A matrix is one grid, not several column stacks.
3. Bar charts: one baseline, one scale per slide, values above, labels below.

## 6. Elements and limits

- Each slide file holds one section and nothing else. Notes go in one aside, last.
- No `z-index`: source order is paint order.
- Too many absolutely placed children in one container makes it disappear. The card states the limit.
- An element cap applies per slide. A face cap applies per deck. Read both in the card.
- No script runs. Hover does nothing.
- Style by class in the shared deck stylesheet, not by id.

## 7. Paint and effects

- Flat toned grounds are the norm. One gradient slide is plenty.
- Hairline borders one step off the ground. Touching boxes share one stroke.
- One soft shadow at most. Never on text.
- Most decks need no effects. A good deck uses one effect idea, consistently.
- Icons at least 32 px with real contrast.

## 8. Images

1. Use only the user's images, the design system's, or the photo library the type offers. Never invent an image.
2. A deck with no images and good structure is acceptable.
3. Photos fill their box (cover). Screenshots and diagrams fit inside it (contain) on a contrasting ground.
4. Protect text over a photo the same way every time: a card, a scrim or a blur panel.
5. Diagram labels are real text over the image, never inside the SVG. Fonts do not load in SVG, and deck export cannot reach them.
6. Video: short clips in the type's formats and size cap, always with a still picture.

## 9. Motion

- Use motion where it helps the point. Animate opacity, transform, color, filter and shadow; not size or position.
- The whole slide shows within one second.
- Click steps use the fragment class. Slide transitions use the type's transition attribute.
- The plain rule is the finished look: a slide reads fully with motion off.
- No more than three flashes per second.

## 10. Diagrams

1. Write the boxes first, with a node list as a comment, then the connectors read off that list.
2. Flow layout for a chain or a small tree. A pinned rows recipe for bigger trees. A pinned host for loops and swimlanes.
3. Boxes on a regular grid. No box narrower than its longest word. Fewer columns before smaller text.
4. Connectors run edge midpoint to edge midpoint through gaps, never through a box.

## 11. Fonts and the design system

- Install the system: an index record plus server-side copies of tokens, fonts and pictures.
- Declare every token you use in the deck stylesheet, or its value is lost.
- Font files listed by path install with the system. Fonts held as assets are copied with one server-side call.
- With no system, the type lists pairings by mood. GDH order still holds: design system, brief, `typography`, then the type's list.

## 12. Export

The type and the Help Center name PPTX, PDF, PNG, Google Slides and slides as pictures. Facts to plan around:

- PPTX maps font sizes at 2 px per point.
- Borders and shadows on images are approximated. Double borders export as solid.
- Named CSS colors are skipped. SVG is rasterized. SVG with foreign objects is skipped.
- A font whose license reserves its name does not travel in the PPTX file.

After an export, open the file and check fonts, cut content and missing images. Label the export VERIFIED only after you opened it.

## 13. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Web page on a slide | Scrolling text, small type | Split into slides; 24 px floor |
| Bullet wall | Six bullets per slide | One statement, or structure |
| Hopping heading | Heading height differs between slides | Pin to the top margin |
| Unfinished slide | Content stops at 60% height | Fill to about 70% or spread |
| Effect salad | Gradients, glows and shadows on many slides | One effect idea |
| Labels in the SVG | Diagram text lost in export | Real text over the image |

## 14. Worked outline

Brief: a board update, eight minutes, action titles.

1. "Revenue grew `[X]`% on two new accounts" (dark, big number). The figure stays a placeholder until the user gives its source.
2. "Churn fell after the onboarding change" (light, line chart, one baseline).
3. "Support load is now the constraint" (light, table of three rows).
4. "We propose two hires in Q1" (accent statement slide).
5. "Decision needed today: approve the hires" (dark close).

Share these five titles in chat first. Build after the user says yes.
