# Performance, SEO and social previews

Read this file at step 16 of `website-design`. It gives performance defaults and the order in which to apply them, the metadata each page needs, and the social preview.

Evidence in this file. The Core Web Vitals numbers come from memory of the web.dev source; no one read the page for this kit. The size and length figures are rules of thumb. All are defaults. A lab run in this session is VERIFIED for the lab only. Field performance stays UNTESTED until real traffic exists.

With GCH loaded, GCH governs how the code meets these targets. This file says what the design must not make impossible.

## 1. Performance targets

| Measure | Default target | Source class | What the design controls |
| --- | --- | --- | --- |
| Largest Contentful Paint | 2.5 s or less at the 75th percentile | Memory: web.dev | The size and priority of the opening image or headline font |
| Interaction to Next Paint | 200 ms or less at the 75th percentile | Memory: web.dev | Script weight, heavy effects, long lists |
| Cumulative Layout Shift | 0.1 or less at the 75th percentile | Memory: web.dev | Reserved space for media, fonts, banners, embeds |
| Server action feedback | Under 500 ms, or an optimistic update | Read: Vercel | A pending state for every action |
| Long lists | Virtualize or paginate past 50 items | Read: Vercel | The list design allows paging |

ASK: when the brief has no performance line, propose these targets and get them confirmed. Write them into the brief.

## 2. Apply in this order

The order follows leverage: the first items usually move the numbers most. This order is a rule of thumb.

1. The opening view. Decide what the largest element is. Make it cheap: one image at the right size, or text in a loaded font.
2. Images. Explicit dimensions, modern formats, responsive sources, lazy loading outside the first view.
3. Fonts. Self-host, subset to the languages in use, preload only the files of the first view, set `font-display`, match the fallback metrics.
4. Layout stability. Reserve space for every late element: images, embeds, banners, consent notices.
5. Script. Ship static HTML first. Add script only where a control needs it. Defer the rest.
6. Third parties. Each embed, tag and widget needs a named reason. Load a heavy embed on demand behind a still preview.
7. Motion. Animate `transform` and `opacity` only. Pause loops off screen.
8. Styles. Remove the unused parts of a kit. Scope component styles.

## 3. Design decisions that cost performance

Decide these with open eyes. Each one is allowed when the brief earns it.

| Decision | Cost | Cheaper form |
| --- | --- | --- |
| A full-bleed video in the first view | The heaviest asset on most pages | A still poster first; the video loads after; a short loop |
| A carousel in the first view | Several large images and script, most never seen | One image |
| Four or more font files | Delay before text shows, layout shift | One variable file, or two static files |
| A 3D scene in the first view | Script, shaders and a model | A poster image first; load the scene on idle or on demand. See `three-d` |
| A scroll-driven effect on every section | Work on every frame | One authored moment |
| A chat widget, a map and several trackers | Script from other hosts | Load each on demand |
| A blur over a large moving area | Costly on low-end phones | A solid token ground |

Default budget lines for `site-plan.md`. Set the numbers with the user. The starting values are rules of thumb.

```
Opening image: <format>, <width> px wide at narrow, under <n> KB       (start: under 200 KB at phone width)
Font files in the first view: <n>                                       (start: 2 or fewer)
Third-party scripts: <list with a reason each>                          (start: none in the first view)
Largest element of the first view: <image | headline text | video poster>
```

## 4. How to check

1. Run a lab audit with a tool of the `capture` capability, or the host's browser tooling. With GCH installed, use `gch:browser-lane`.
2. Record the values, the device profile and the network profile.
3. Read the layout-shift sources and the largest element that the tool reports.
4. Fix, then run again. Compare like with like.
5. Label the result: "VERIFIED lab, <profile>". Label field performance UNTESTED.
6. With no tool, list what was done from part 2 and label every number UNTESTED.

A good lab value on a fast machine proves little. Use a throttled phone profile when the tool has one.

## 5. Metadata for every page

Write these in the copy deck. Each page has its own values.

| Item | Rule | Default |
| --- | --- | --- |
| `title` | Unique. The page job first, the site name last | About 60 characters or fewer (rule of thumb) |
| Meta description | One or two sentences that answer the page's question | About 150 to 160 characters (rule of thumb) |
| `lang` on the root | The language of the page | Required for assistive technology |
| One `h1` | States what the page is | Headings then follow in order |
| Canonical address | One preferred address for each page | Set on every page |
| Link text | Says where the link goes | Never "click here" |
| Image alt text | From the copy deck | See the imagery reference |
| `theme-color` | Matches the page ground in each theme | Read: Vercel |
| Icons | An SVG icon, a 32 px fallback, a 180 px touch icon, 192 and 512 px manifest icons, a maskable icon | Memory. Confirm the current set |

Site-level items:

- A sitemap file and a robots file.
- A real not-found page.
- A redirect map from each old address, when this site replaces one. ASK for the old address list.
- Preview deployments carry a no-index rule. Production does not.
- Clean addresses in the visitor's words, from the page inventory.

## 6. Structured data

Structured data states facts to machines. Kernel rule 11 applies with full force.

1. Mark up only facts that are true and visible on the page.
2. Never mark up a rating, a review, a price or an award that the user did not supply.
3. Choose the type from the page job: an organization, a local business, a product, an article, a list of questions, a breadcrumb trail.
4. Use the JSON-LD form in the page head.
5. A placeholder in the copy is a missing field in the markup. Leave it out until the fact exists.
6. Validation needs an outside tool. Label it UNTESTED unless one ran.

## 7. The social preview

A shared link shows a card. Design the card. It is often the first view of the site that a person sees.

Tags for each page: a title, a description, an image, the page address and the content type in Open Graph form, plus a large-image card tag for platforms that read it. Add alt text for the image.

Design rules:

1. Default: the image is 1200 by 630 px. This is a rule of thumb. Platforms change their sizes; confirm for the platforms in the brief.
2. Build the image from the design system: token colors, the display face, the mark.
3. Keep the key content in the center. Platforms crop the edges differently.
4. The image carries the page's claim in a few words, or the real product. It is not the logo alone.
5. The title fits without truncation. Test the longest page title.
6. Text on the image passes the contrast gate.
7. One template serves most pages. Key pages get their own image.
8. The image is an asset. Record it in the manifest when any outside material is in it.

Checking the card needs each platform's preview tool, which is a network call to a third party. GATE: a preview tool that fetches the page needs a public address, so it is exposure. Ask first. Otherwise label the card UNTESTED.

## 8. Consent, analytics and trackers

- ASK which analytics and consent rules apply. Do not add a tracker on your own.
- A consent notice is a designed state. It uses tokens. It can be reached and dismissed by keyboard.
- The notice reserves its space or overlays without shifting the layout.
- Name one feedback source that keeps running after launch, and where its results land.

## 9. Worked example

The invented repair shop, one static site.

- Largest element of the first view: the bench photograph. Decision: a 4:5 crop at phone width, a modern format with a fallback, explicit dimensions, high fetch priority.
- Fonts: one variable text face, self-hosted and subset to Latin. The fallback stack is metric-matched, so the swap does not move the headline.
- Script: none in the first view. The model filter works as plain links; script only enhances it.
- Third parties: a map. It loads on demand behind a still image of the street with the address in text.
- Metadata: the home title leads with the job, "Film camera repair", then the shop name placeholder. The description answers "Can they fix mine?".
- Structured data: local business, with address and hours. No rating: none was supplied.
- Social card: the open camera on the token ground, with the six-word claim in the display face.
- Result labels: "VERIFIED lab, throttled phone profile" for the three vitals. "UNTESTED" for field data and for the platform cards.

## 10. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Heavy opening | The first view waits on a video, a carousel or a 3D scene | A poster first. Load the heavy part after |
| Font flash | Text jumps when the font arrives | Metric-matched fallback. Fewer files |
| Jumping page | Content moves as media and banners load | Reserve the space |
| Tag pile | Trackers and widgets with no named reason | Remove each one that has no owner |
| Same title everywhere | Every page shares one title and description | Write each in the copy deck |
| Invented schema | A rating or a review in the markup that no one supplied | Remove it |
| Logo card | The social image is the logo on a flat ground | The claim or the product, from the system |
| Lab only | A fast-machine score reported as "fast" | State the profile. Label the field UNTESTED |

## 11. Checks

Gates:

- No structured data states a fact that the user did not supply.
- Every page has a unique title, one `h1` and a language attribute.
- Moving media stops under reduced motion.
- No preview tool, deploy or public link ran without a yes.

Defaults:

- Default: the three Core Web Vitals targets in part 1.
- Default: the social image is 1200 by 630 px.
- Default: title about 60 characters; description about 150 to 160 characters.
- Default: no third-party script in the first view.
