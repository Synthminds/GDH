# Formats: tall scroll, poster, carousel, slide, print and scroll story

Read this file at steps 13 and 14 of `infographic`. It covers the format table, the tall scroll graphic, the poster and print page, print with bleed and minimum sizes, the social carousel, the slide, the scroll story, recomposing between formats, and failure patterns.

Evidence. Print sheet sizes, edge margins, the 12 px floor, the body size and the gray text floor come from the Claude Design type print rules (read 2026-11-23, DOCUMENTED; they bind on a Claude Design print artboard). Slide size, the 24 px floor and margins come from the Claude Slides type rules (read 2026-11-23). Scrollytelling rules come from The Pudding and Chrome for Developers (search summaries). Bleed, print resolution and social sizes are from memory: defaults to confirm with the printer or the platform.

## 1. Choose the format first

| Format | Seen | Size default | Reading | Key constraint |
| --- | --- | --- | --- | --- |
| Tall scroll graphic | Article, phone, web | 800 to 1200 px wide, any height | Top to bottom | Readable on a phone without zoom |
| Poster | Wall, event, office | A3, A2, tabloid; or a screen at 1080 by 1920 | Headline from a distance, detail up close | Two reading distances |
| Print page or one-pager | Hand-out, report page | A4 or Letter | Top to bottom, Z path | Bleed, safe margin, minimum sizes, grayscale |
| Social image | Feed | Confirm the platform's current size; default 1080 by 1350 (4:5) or 1080 by 1080 | One glance | The headline works as a thumbnail |
| Social carousel | Feed, swiped | Same size per frame; default 5 to 10 frames | Frame by frame | Each frame stands alone; frame 1 is the hook |
| Slide | Presentation | 1920 by 1080 | One idea per slide | Nothing under 24 px; readable from the back of the room |
| Scroll story | Web | Responsive | Steps beside a sticky graphic | Native scroll; static fallback |

Record the format, sizes and destinations in `infographic-plan.md`. One piece often needs several formats; design the main one first, then recompose.

## 2. Tall scroll graphic

- Width: design at the size it will be shown. Default: 800 to 1200 px wide for a web article; check it on a 375 px phone.
- On a phone, text must stay at or above 12 px at the displayed width. A 1200 px image scaled to 375 px shrinks text to under a third. Prefer real HTML and SVG text that reflows, or make a phone version.
- Break the column into sections of one idea each, with a section label.
- Keep the headline and hero within the first screen.
- Put the takeaway and sources at the end; a reader who scrolls that far wants them.

## 3. Poster and print page

Two reading distances:

- From a distance: headline, hero visual and the takeaway. Default: the headline is the dominant line, about six words or fewer, set large (the Design type's flyer rule uses 80 px or more on the artboard).
- Up close: annotations, numbers, sources.

Layout:

- Choose the sheet size before the first artboard. Claude Design sheet sizes at 96 px per inch: Letter 816 by 1056, A4 794 by 1123, Tabloid 1056 by 1632, A3 1123 by 1587, A5 559 by 794.
- On a Claude Design print artboard: keep content 40 px inside each edge and 72 px around running text; body 16 px (12 pt) at line height 1.5 to 1.65; nothing under 12 px; table rules at least 1 px; no gray text lighter than `#767676`. It must still read in grayscale. These are gates on that route.
- A multi-page piece is a series of fixed pages in reading order.

## 4. Print with bleed and minimum sizes

For a printer, not only a PDF on screen:

| Item | Default | Note |
| --- | --- | --- |
| Bleed | 3 mm (0.125 in) on each side | Backgrounds and images that touch the edge extend into it; confirm with the printer |
| Safe margin | 3 to 5 mm inside the trim, more for binding | Text and key marks stay inside it |
| Raster resolution | 300 ppi at printed size | Photos; vector for charts, icons, text |
| Color | Ask whether the printer wants RGB or CMYK; ask for a proof | Bright screen colors may dull in print |
| Rich black | Ask the printer; never for small text | Small text in plain black |
| Smallest text | About 7 pt as a rule of thumb outside a canvas artboard; 12 px on a canvas artboard | Larger for low-quality paper or older readers |
| Thinnest line | About 0.25 pt as a rule of thumb | Thinner lines may vanish |
| Fonts | Embedded or outlined in the final PDF | Check the font license allows embedding |

Steps:

1. Set the document to the trim size plus bleed.
2. Mark trim, bleed and safe margin with guides.
3. Export a press PDF with bleed and crop marks, as the printer asks.
4. Check the PDF at 100 percent and in grayscale.
5. GATE: sending files to a print service or placing an order is exposure and often spend. Ask first; show the price.

## 5. Social carousel

- Frame 1 is the hook: the message as a headline, or a question the next frames answer. It also works as a thumbnail.
- One idea per frame. Each frame stands alone if shared.
- Keep a consistent grid: headline in the same place, frame number or progress mark, brand mark small.
- The last frame holds the takeaway and the sources.
- Keep important content away from edges and areas the platform covers with buttons; confirm the platform's current safe area.
- Text is large: test on a phone at the size shown in the feed.
- Export each frame at the platform's current size; keep the source file for edits.
- The post caption carries the alternative text where the platform allows it, plus the sources.

## 6. Slide

- Follow the slide rules: 1920 by 1080, nothing under 24 px, 128 px margins, one idea per slide, titles that tell the story when read alone.
- Split a tall infographic into a short sequence of slides rather than shrinking it.
- Put sources at the bottom of each slide that carries a number.
- Build it as a deck through `claude-design` (slides route) when the user wants an editable deck.

## 7. Scroll story

A scroll story ties text steps to changes in one graphic.

Pattern:

1. A sticky graphic stays in view; text steps scroll past it.
2. Each step changes one thing in the graphic: highlight a bar, add a layer, zoom to a region.
3. Keep native scrolling. Never take over the scroll speed or direction; no scroll hijacking, no swipe capture.
4. Make each step's change readable before the next step arrives.
5. Provide a static form: with scripts off or under reduced motion, show each step's graphic as a static image with its text.
6. Make the graphic responsive: update it for small screens instead of rebuilding it; keep CSS and script breakpoints in sync.
7. On phones, place the graphic above the text step, or full width with the text overlaid on a solid backing that passes contrast.
8. Under reduced motion, change states without animated transitions.
9. The first screen states the message, so a reader who never scrolls still gets it.

Route: a sourced data page with a scroll story shape (for example the Claude Data type) when numbers must show provenance; project code with a scroll library or CSS scroll-driven animation when it ships on a site. Libraries are outside assets: `find-assets` reads their licenses.

## 8. Recompose between formats

| From | To | Change |
| --- | --- | --- |
| Tall scroll | Carousel | One section per frame; headline becomes frame 1 |
| Poster | Social image | Hero and headline only; details in the caption or a link |
| Report page | Slides | One chart or number per slide; titles state findings |
| Desktop story | Phone | Graphic above text; fewer labels; larger type |

Never shrink one format into another. Recompose and recheck the minimum sizes.

## 9. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Desktop image on a phone | 6 px text after scaling | Real text that reflows, or a phone version |
| Poster without distance read | All text the same size | Headline and hero for distance; details up close |
| No bleed | White slivers at the trim | Extend backgrounds into the bleed |
| Carousel frame 1 is a logo | People swipe past | Hook with the message |
| Scroll hijack | The page scrolls at its own speed | Native scroll, sticky graphic |
| Motion-only story | Nothing readable without animation | Static fallback for each step |
