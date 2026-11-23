# Craft of the Design canvas

Read this file at step 12 of `claude-design` when the type is the Design canvas. It restates the canvas type's craft, layout, diagram, print and prototype rules in my own words, and adds the failure patterns and checks GDH applies.

Evidence. Every rule here comes from the Design type's rule file and its reference files (format, craft, diagrams, print, shaders, make-from-this), read 2026-11-23: DOCUMENTED. Numbers are the type's own. The type file wins on any difference. No canvas was built for this kit.

Terms. An artboard is one frame on the canvas, stored as one file. A page artboard is fluid; every other artboard is fixed. A Tweak is an editor the type shows for a declared property.

## 1. Settle the direction before the build

1. Without a design system, references or a stated look, get the user's input first. Ask, or draw two to four truly different low-fidelity direction artboards.
2. A concrete subject, an asset or a brand counts as input.
3. With nobody to ask, commit to one nameable direction and say so in the reply.
4. Once a decision is settled, it stays settled. Do not reopen it unless the user does.
5. Then commit to a small system: one type pairing, one tone, a few accents. Record it in `design/decisions.md`.

The small system, as the type describes it:

| Part | Rule |
| --- | --- |
| Type | One to three families. Each has a metric-close system fallback. Work added to an existing design keeps its faces. |
| Tone | Warm, cool or neutral for foreground and ground. Tinted whites and blacks. |
| Accents | Zero to two, in oklch, sharing chroma and lightness and differing in hue. |
| Brand colors | Prefer them. Too few: derive harmonious oklch colors from them. Never invent unrelated ones. |

The type names a neutral default pairing for a neutral Latin subject. GDH order: the design system, then the brief, then `typography`, and only then that default. A default face chosen by habit is a tell.

## 2. When no brand governs

The type asks for a bold, deliberate choice. Answer three questions in the reply:

1. Purpose: what problem, for whom.
2. Tone: pick an extreme and name it, for example brutal minimal, editorial, industrial, organic, luxury, playful, retro-futurist.
3. Difference: the one thing a person will remember.

Then apply:

- Intent beats intensity. Minimal and maximal both work when chosen.
- Dominant colors with sharp accents beat a timid, even palette.
- Spend motion on one strong moment, not scattered micro-motion.
- Composition: asymmetry, overlap that never covers text, diagonal flow, grid-breaking elements, generous space or controlled density.
- Atmosphere: meshes, noise, geometric pattern, layered transparency, grain, strong shadow.
- Vary light and dark and the aesthetic between pieces. Never settle into one house look.
- Match build effort to the vision. Maximal needs elaborate effects; minimal needs exact spacing.

## 3. Hi-fi work starts from real context

1. Gather the codebase, brand assets, screenshots of the product and the design system first. Ask for what is missing.
2. A full product designed from nothing is the last resort.
3. State assumptions early. Show work as soon as there is something to react to.
4. A missing icon, asset or component becomes a labelled placeholder, not a weak imitation.

## 4. Options on one canvas

| Stage | How many | How they differ |
| --- | --- | --- |
| Open direction | Two to four candidates | Each on a named axis, low fidelity is enough |
| Early exploration | Three to five wireframe approaches | Simple shapes, little color |
| Direction settled | Three or more variations | Across several dimensions, so the user can mix parts |

- Give each option an honest motivation and its main trade-off, in the reply, not on the artboard.
- Keep option names stable across turns. Never renumber.
- Use a `title1` note over each group of artboards that forms one option.

## 5. Layout that survives hand editing

The owner edits the canvas by hand. The layout must survive that.

1. Lay out sibling groups with flex or grid plus `gap`. Inline flow is only for runs of text.
2. Use modern CSS: grid, `text-wrap: pretty`.
3. Put editable values in inline `style`. The page-level style block holds only basics and link colors.
4. Build all interface as markup. Never build it by script.
5. Icons come from the mounted system by name, else inline stroke SVG. Never emoji.
6. No iframe, object or embed. No global key handlers.
7. Close every non-void tag. Quote every attribute. Keep the support script line exactly.

Rules 4 to 7 fail silently when broken. Check them before each write.

## 6. Fixed or fluid

| Artboard | Root | Notes |
| --- | --- | --- |
| Device mockup, poster, social post, print piece | Fixed size | The frame is the canvas size |
| Page (landing page, site page) | Fluid, set to fill | No px width on the root. A `max-width` container. Percent, rem and fr units |
| Phone app screen | Fixed | The type names a phone size; read it in the card |

Spacing on the canvas: the type asks for a set gap between frames in a row and a larger gap between rows. Read both in the card.

## 7. Scale and access as drawn

- Size text for its real viewing distance.
- Touch targets meet the type's minimum (the card states it). Print body meets the print minimum.
- Draw controls with real buttons, links, inputs and labels, even in a static mockup. An icon-only button has an accessible name.
- Contrast: 4.5:1 for body text, 3:1 for large text, in every theme. Large text uses the WCAG definition. Grey captions and white text on colored fills fail most often.
- Colors that must be told apart also differ in lightness. Prefer blue and orange to red and green.

## 8. Landing pages and marketing artboards

1. Anatomy: a hero with the offer in one sentence and one call to action. Then proof from the user's own material. Then benefit sections that answer real doubts.
2. One primary action per page, repeated down the page.
3. The copy is the product. Write it from what the user said. A missing fact is a bracketed placeholder.
4. A landing page is a page artboard with a fluid root. Its grids collapse to one column on a phone, with an auto-fit grid pattern.
5. Use viewport height only for a whole-screen app shell. An over-tall frame beats a clipped one.

## 9. Prototypes and recreations

- An artboard that links to another artboard file becomes a clickable prototype.
- Each artboard keeps its own state. A flow that shares state is one artboard.
- Mobile prototypes: no fake status bar, no fake keyboard.
- Recreating an existing interface: build from the real source, copy exact values, never snap to a 4 or 8 px grid. If you cannot read the source, stop and say so.

## 10. Diagrams on a canvas

1. Build a diagram from separate placed elements, never one SVG. One SVG is right only for icons, logos, illustrations and a chart's plot.
2. One host element with relative position and a px size. Each card is placed absolutely with px offsets. Write each element as literal markup.
3. Paint order: background bands, arrows, cards, labels.
4. Plan the numbers first, on a grid: shared center lines, wide gaps, wider where a line runs along a gap.
5. Each straight arrow segment is its own small SVG. It has its own marker id and a label for what it joins. A bend is a chain of straight segments.
6. A decision diamond is a card with a clip path, never a rotated square.
7. Arrows do not follow cards. After you move a card, recompute every arrow.
8. When the diagram does not fit, enlarge the artboard. Never shrink the text.

## 11. Print

Choose one of two shapes before the first artboard.

| Shape | Use for | Rules |
| --- | --- | --- |
| Fixed pages | Posters, flyers, certificates, brochure faces | One artboard is one PDF page at a standard sheet size. Content stays inside a safe margin; running text has a wider margin. A multi-page piece is artboards in reading order. A trifold is two artboards of three panels. |
| Flow | Reports, memos, letters | One artboard marked as flow with a paper size. One column. No repeated header, no page number, no forced break. Use image elements, not background images. |

Type for print: body 16 px (12 pt) at line height 1.5 to 1.65, a 60 to 75 character measure, nothing under 12 px on the artboard, table rules at least 1 px, no grey lighter than the type's limit. It must still read in greyscale. Flyer: one dominant line of six words or fewer at large size; group the five Ws; flat color and vector shapes over photos.

## 12. Shaders

Offer a shader artboard only when the view context says shaders are on. Otherwise do not mention it. One shader is one interactive artboard. Change only the fragment code, its uniforms, its Tweaks and its markup. Quality: a lit subject with depth, two to four colors from the brief, slow large shapes, a pointer effect that reads in the first second. Safety: nothing flashes over a large area more than three times a second.

## 13. Make something else from a canvas

A deck, a video or a document made from artboards is built in its own type, never as pictures of the canvas. It is not delivered until a link card to the new artifact sits on the canvas under the source artboard. Link cards are left out of exports.

## 14. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| House look | Every canvas has the same cream ground and serif | Answer the three questions; vary the tone on purpose |
| Script-built UI | Markup created by script | Rewrite as markup; the owner cannot edit it otherwise |
| One giant SVG diagram | The whole chart selects as one block | Rebuild as placed cards and segment arrows |
| Fixed landing page | The page root has a px width | Make it fluid and fill |
| Clipped frame | Content cut at the frame edge | Make the frame taller |
| Rationale on the artboard | "Design notes" boards in new work | Move it to the reply and the decision record |
| Look-alike components | Drawn buttons beside a mounted system | Mount the real components |

## 15. Check before the reply

- The direction question was settled, or one direction was named and stated.
- Options carry stable names and the same parts.
- The silent-failure rules of section 5 hold.
- Page artboards are fluid; others are fixed.
- Contrast and target sizes meet the floors.
- No invented fact; placeholders are labelled.
- The rationale is in the reply and in `design/decisions.md`.
