# Build routes, export, the accessible form and review

Read this file at steps 15 to 19 of `infographic`. It covers the build routes, the order of work, export per destination, the accessible text form, the review checks with their class, a worked example and failure patterns.

Evidence. Route facts come from the GDH tool cards for the design canvas, slides and data page types (read 2026-11-23, DOCUMENTED; nothing was created, so output quality is UNTESTED). The rule "real text, not text in an image; alt text or a text version" comes from Chrome for Developers scrollytelling guidance (search summary). The cold-read test is a rule of thumb. The review list gathers the gates from `SKILL.md` and the defaults from the other reference files.

## 1. Build routes

| Route | Choose when | Rules that bind |
| --- | --- | --- |
| Design canvas (`canvas`, through `claude-design`) | Poster, print page, tall graphic, social frames; the owner wants to edit by hand and export PDF or PNG | Read the type's rules first; a fixed-size artboard per page or frame; install the design system's tokens; print rules from `formats.md` section 3; diagrams as placed elements, not one SVG. See [claude-design](../../../references/tools/claude-design.md) |
| Slides (`claude-design`, slides route) | A deck or a slide version | Slide type rules: 1920 by 1080, nothing under 24 px. See [claude-slides](../../../references/tools/claude-slides.md) |
| Sourced data page (`dataviz`) | A scroll story or a played data short where each number shows its source | Type rules: bundled chart library only, theme tokens, run checks before hand-over. See [claude-data](../../../references/tools/claude-data.md) |
| Local HTML with inline SVG | No canvas tool, or the piece ships on a site | Real text; tokens as CSS custom properties; export PNG or PDF from the browser |
| Design app template (`templates`) | The user will keep editing in that app | Read the tool card; check the export and the license of any template asset. See [canva](../../../references/tools/canva.md), [adobe](../../../references/tools/adobe.md) |

Rules:

- Choose the route from where the piece lives and who edits it next. Record the reason.
- A chart is drawn from data in code or by the chart tool, not traced by hand.
- On an artifact route, the type's own check rules govern verification. On a code route, review the rendered result.

## 2. Order of work

1. Fact table approved; copy written (from `message-and-facts.md` and `structure-and-reading-path.md`).
2. Gray-box sketch approved.
3. Main visual and charts, with real data.
4. Supporting parts, type and color from tokens.
5. Icons, illustration and photos, each with a license record.
6. Format layouts and recompositions.
7. Accessible form.
8. Review and export.

## 3. Export per destination

| Destination | Export | Check |
| --- | --- | --- |
| Web article | HTML and SVG with real text; or PNG at 2x display size with alt text and a text version | Text at or above 12 px at the displayed width on a phone |
| Social image or carousel | PNG or JPG per frame at the platform's current size | Headline legible as a thumbnail; sources on the frame or in the caption |
| Print | Press PDF with bleed and crop marks, fonts embedded, as the printer asks | Proof checked; grayscale pass |
| Screen PDF | PDF from the canvas or the browser | Tagged where the tool allows; alt text on images |
| Slides | Deck file and PDF | Nothing under 24 px; sources per slide |
| Editable source | The canvas link, the HTML, or the design app file | Saved under `design/` or linked in the plan |

Record each export in `design/assets/` and in `design/decisions.md`. Assets placed from outside sources are in `design/assets/manifest.json`.

## 4. The accessible text form

Every infographic has a text form that carries the same message and numbers.

Contents:

1. The headline (the message).
2. The introduction.
3. Each section as a short paragraph or list, in reading order, with its numbers.
4. Charts as their summaries (finding plus key numbers), with a table where the reader needs the values.
5. The takeaway.
6. The sources.

Where it goes:

- Web: the piece is built from real text; the text form is the page itself, or a "Read as text" section.
- Image: alternative text with a short summary (the message and the main number), plus a linked or attached text version.
- Social: the post caption holds the summary and sources; the platform's alt text field holds the frame's content.
- Print: a digital text version is available on request or by a link.

## 5. Review checks

Run at the delivered size and on the real medium. Record each result in `design/reviews/<date>-infographic.md`.

| Check | How | Class |
| --- | --- | --- |
| Message | Headline plus main visual state the message alone | Gate |
| Sources | Every number has a source on the piece | Gate |
| Numbers | Each number matches the fact table and its source | Gate |
| No invention | No unsourced statistic, quote, logo or name | Gate |
| Proportion | Scaled shapes by area; equal icons in unit charts; bars from zero | Gate |
| Text form | Real text on the web; alt text and a text version for images | Gate |
| Contrast | Text 4.5:1; large text and meaningful graphics 3:1 | Gate |
| Color not alone | Meanings also carried by words, icons or position | Gate |
| Medium floors | Canvas print artboard: nothing under 12 px; slides: nothing under 24 px | Gate on those routes |
| Motion | No scroll hijacking; static form under reduced motion | Gate |
| Licenses | Every outside asset recorded | Gate |
| Tokens | Every color, size and space a token | Gate |
| Cold read | Show for about five seconds, then hide; the reader states the message | Default |
| Path | A cold reader traces the reading path without help | Default |
| Type and color limits | Two families; one main hue, one accent | Default |
| Icons | One set, one weight, no emoji | Default |
| Grayscale | The hierarchy still reads | Default |
| Phone | Readable on a 375 px wide screen where the piece is shown on phones | Default |
| Print proof | Colors and small text checked on paper | Default |

Then run `design-critique` and `accessibility-gate`, and send chosen findings to `refine-round`.

## 6. Worked example

The case (invented): a training team asks for a one-page how-to that explains a seven-step annual review process to new staff. It will print on tabloid paper for a wall and be shared as a PDF. A design system with tokens exists.

1. Message: "A review takes seven steps over six weeks; three of them depend on your manager, so start early." Takeaway: "Book the first meeting in week one." Audience: new staff, at a desk or in a hallway.
2. Facts: seven steps from the official handbook (sourced, page numbers recorded); "six weeks" from the policy (sourced); "most late reviews stall at step 4" from the training team's tracker: unsourced. ASK: the team confirmed it with last year's count (38 of 52 late reviews); the fact table records the tracker as the source.
3. Structure: process, with one statistic. Metaphor directions shown: a path with milestones; a calendar strip; a relay race with handoffs. The team chose the calendar strip: it shows time and who holds each step.
4. Copy first: headline (11 words), introduction (2 sentences), seven step labels (3 to 5 words each), one annotation on step 4, takeaway, sources.
5. Reading path: top to bottom; the calendar strip runs left to right across the middle with numbered steps; the step-4 callout sits below it.
6. Sketch round: keep the strip; change the step-4 callout to show the 38 of 52 count as a unit chart of 52 small squares; remove a decorative header illustration.
7. Build route: design canvas, one tabloid artboard (1056 by 1632 px), the design system installed. Content 40 px inside each edge; body 16 px; smallest text 12 px; no gray lighter than the type's floor.
8. Proportion: the unit chart uses 52 equal squares, 38 in the accent, in rows of 10.
9. Color: one main hue from the system, one accent for "depends on your manager", neutrals. Each manager step also carries a small label "Manager", so color is not alone.
10. Exports: tabloid PDF for print (a printer asked for 3 mm bleed; background extended), an A4 PDF recomposed for screens, and a text version for the intranet.
11. Review: cold read by two new staff: both said "seven steps, start early". Grayscale pass. Print proof checked for the accent's legibility.

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Picture of text | The whole piece is one PNG with no text form | Real text, or alt text plus a text version |
| Traced chart | A chart drawn by eye | Draw from data |
| Export at wrong size | Fine on the designer's screen, tiny on a phone | Check at the delivered size |
| Last-minute facts | Numbers added after the review | Re-run the number check on every change |
| Route by habit | A print poster built where it cannot export with bleed | Choose the route from the destination |
