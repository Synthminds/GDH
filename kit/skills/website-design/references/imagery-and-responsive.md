# Responsive behavior and imagery

Read this file at steps 12 and 14 of `website-design`. Part A covers how the page changes across widths and inputs. Part B covers which images the page needs, where they come from and how they are delivered.

## Part A. Responsive behavior

### A1. Principles

1. Build the narrow layout first. Add layout changes where the content breaks.
2. Content parity: a phone visitor gets the same content and the same actions. Do not hide a section on small screens.
3. The layout is fluid between breakpoints. It never snaps between fixed frames.
4. Design for the input as well as the width: touch, pointer, keyboard.
5. Zoom is never disabled. This is a gate.

### A2. What changes, and where

Write this table for the site in `site-plan.md`. The breakpoint names come from the layout reference.

| Element | Narrow | Wide | Rule |
| --- | --- | --- | --- |
| Navigation | A labelled "Menu" button, or a short visible list | A full row | The button is a `button` with its open state exposed to assistive technology |
| Grids | One column | Columns by content | Use an intrinsic grid where the count varies |
| Split sections | Stacked. Decide which part comes first | Side by side | The text that names the image comes before the image |
| Tables | Scroll inside their own container, or re-form as a list | Full table | The page never scrolls sideways |
| Type | Fluid between limits | Fluid between limits | Use a smaller scale ratio at narrow widths |
| Images | Cropped for the narrow frame | The wide crop | Art direction, part B4 |
| Actions | Reachable by a thumb | Near their content | A sticky action bar is one option. It must not cover content or focus |
| Hover content | Shown on tap or always visible | Shown on hover and on focus | Nothing is reachable by hover alone |

### A3. Input rules

- Default: a target is 24 px or more for a pointer and 44 px or more for touch. On Android use 48 dp. A small icon may sit in a larger tappable area.
- With GCH loaded, its single target number governs.
- Default: inputs are 16 px or more on mobile web.
- Gate hover styles with `@media (hover: hover)`.
- Sticky headers stay short on a phone. A sticky header must not hide a focused element.
- Respect safe areas with `env(safe-area-inset-*)`.
- Modals and drawers contain their own scroll.

### A4. Content stress

Test each layout with the extremes, not with the tidy sample.

| Stress | Example | Look for |
| --- | --- | --- |
| Longest heading | The real longest title in the copy deck | Wrapping, overlap with media |
| Shortest heading | One word | A heading that looks lost |
| A long word | A long compound word, a URL, an address | Overflow at the narrowest width |
| Many items | Forty items in a list built for six | Rhythm, load time |
| No items | An empty list | The empty state |
| Another language | A string about 30 percent longer, or a right-to-left string | Truncation, mirrored layout |
| 200 percent zoom | Browser zoom, not a narrow window only | Lost content, overlap |

The 30 percent figure is a rule of thumb for translated text. Use the real target language when the brief names one.

### A5. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Shrunk desktop | Small targets, hover-only controls, a wide table off screen | Rebuild from the narrow layout up |
| Hidden on mobile | A section set to not display on small screens | Re-form it. Do not remove it |
| Hamburger by default | Four links hidden behind a menu button on a wide screen | Show the links |
| Sticky pile | A header, a banner and an action bar all fixed | Keep one fixed element on a phone |
| Tidy sample | The layout was checked only with ideal copy | Run the stress table |

## Part B. Imagery

### B1. Give each image a role

Every image has one of three roles. An image with no role is cut.

| Role | It does | Examples | Test |
| --- | --- | --- | --- |
| Evidence | Shows the real thing | The product, the place, the people, the work | The visitor learns a fact from it |
| Explanation | Makes a mechanism clear | An annotated screen, a diagram, a step photograph | The text nearby gets shorter because of it |
| Atmosphere | Sets tone | A texture, a material, a color field | It comes from the subject's world, not from a stock mood |

Rules:

1. Evidence first. A page with real evidence needs little atmosphere.
2. Default: one atmosphere treatment for a site.
3. An image that only decorates a heading is cut.

### B2. Source order

1. The client's own material: product screens, photographs, drawings, archive.
2. A commissioned or user-made image.
3. A licensed image found with `find-assets`. The license is read and the file is recorded before use.
4. A generated image made with `generate-media`. GATE: it is a spend call.

Rules that hold at every step:

- Never present a stock or generated image as the client's place, product, staff or customer.
- Never draw a look-alike of a real logo. Use the real file with permission, or nothing.
- A generated image of a person is never used as a testimonial or as staff.
- A reference image from the mood board never ships.
- Every file that ships has a record in `design/assets/manifest.json`: source, license, attribution, date, path, hash.
- With no usable image, design the section in type and layout. A labelled placeholder marks the gap.

### B3. One treatment

Images on one site share a treatment, or they read as a collage of sources.

Decide once, and record it in `DESIGN.md`:

- Crop logic: tight on the object, or wide with context.
- Aspect ratios, as tokens: one for the opening view, one for cards, one for inline figures.
- Color treatment: natural, one grade, or duotone from brand tokens.
- Screens: real, current, at twice the display size, cropped to the point, with annotations in the type system.
- Icons: one set, one stroke weight. No emoji and no Unicode glyphs as icons, unless the brief asks.
- Illustration: one hand, one line weight, one palette from tokens.

### B4. Art direction across widths

A wide photograph cropped by the browser often loses its subject on a phone.

1. Mark the focal point of each image.
2. Supply a separate narrow crop when the subject would shrink or leave the frame.
3. Use the `picture` element to switch crops. Use `srcset` and `sizes` to switch resolutions.
4. Keep text out of images. Text in an image cannot reflow, translate or be read aloud.

```html
<picture>
  <source media="(min-width: 60em)" srcset="bench-wide-1600.avif 1600w, bench-wide-2400.avif 2400w" sizes="58vw" type="image/avif">
  <source srcset="bench-tall-800.avif 800w, bench-tall-1200.avif 1200w" sizes="100vw" type="image/avif">
  <img src="bench-tall-800.jpg" width="800" height="1000" alt="A rangefinder camera open on the repair bench, shutter removed" fetchpriority="high">
</picture>
```

### B5. Delivery rules

| Rule | Class | Source class |
| --- | --- | --- |
| Every image has explicit `width` and `height`, or an `aspect-ratio` | Default | Read: Vercel |
| The image in the first view is preloaded or has high fetch priority. Others load lazily | Default | Read: Vercel |
| Photographs ship in a modern format with a fallback. Marks and icons ship as SVG | Default | Rule of thumb |
| Animated media is a muted, looping, inline video with a poster. It is not a GIF | Default | Read: Vercel |
| Moving media stops under reduced motion and shows the poster | Gate | Kernel rule 12 |
| Dark gradients show no banding | Default | Read: Vercel |
| No hotlinked file from a connector's storage. Download it into the project | Default | Read: connector cards |

### B6. Alt text

1. An evidence or explanation image has alt text that states what the image shows and why it matters here.
2. An atmosphere image has an empty alt attribute. It is hidden from assistive technology.
3. Do not start with "Image of".
4. An image that is a link has alt text that names the destination.
5. A complex diagram has a short alt and a full text version on the page.
6. Write alt text in the copy deck, with the rest of the copy.

### B7. Themes

Check each image on each theme ground. A screenshot with a white ground glares on a dark page. Supply a second file, a framed treatment, or a token ground behind it.

### B8. Worked choice

The invented repair shop. Brand words: exact, patient, hands-on.

- Evidence exists: the owner can photograph the bench and three finished repairs. That sets the plan: photographs carry the page.
- Treatment: tight crops on the mechanism, natural color, one 4:5 ratio in the opening view and 3:2 in the repair log.
- The wide bench photograph loses the camera on a phone. A tall crop is supplied.
- Rejected: a generated "vintage camera" hero. It would show a camera that the shop never repaired, as if it were evidence.
- Rejected: stock photographs of hands with tools. They would present a stranger's bench as the shop's.
- Placeholder: `[PLACEHOLDER: three before and after pairs, from the owner]`. The section is sized for real photographs.
- Atmosphere: none. The evidence is enough.

### B9. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Stock stand-in | A stock image shown as the client's own | Remove it, or label it and move it out of the evidence role |
| Decoration images | An image above each heading that teaches nothing | Cut them |
| Mixed sources | Photographs, 3D renders and flat illustrations with no shared treatment | One treatment. Fewer images |
| Text in the image | A headline baked into a picture | Real text over the image |
| Lost subject | The focal point leaves the frame on a phone | A narrow crop |
| Unsized media | The page jumps as images arrive | Explicit dimensions or an aspect ratio |
| Glaring screenshot | A light screenshot on a dark ground | A theme-specific file or a framed treatment |

## Checks

Gates:

- Every shipped image has a manifest record. No reference image ships.
- No stock or generated image is presented as the client's own.
- Every image with meaning has alt text. Decorative images are hidden from assistive technology.
- Zoom is never disabled. Nothing is reachable by hover alone.

Defaults:

- Default: targets 24 px for a pointer, 44 px for touch, 48 dp on Android.
- Default: explicit dimensions on every image; lazy loading outside the first view.
- Default: one atmosphere treatment for a site.
