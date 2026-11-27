# How to read the fingerprint

Read this file at step 5 of `originality-gate`. It explains each field the script writes, how `compare` scores two fingerprints, and what the script cannot see.

Evidence class: the parse rules, the weights and the thresholds are GDH defaults. They were tuned on the sample pages behind the library and on the test fixtures in `tests/test_originality.py`. They were not validated on real projects.

## 1. The fields

`originality.py fingerprint <paths> --json` prints one object.

| Field | What it holds | How it is read |
| --- | --- | --- |
| `skeleton` | The ordered section archetypes of the page | From the HTML or JSX tree. See section 2 |
| `typefaces` | Declared families, most used first, lower case | `font-family`, Google Fonts links, `next/font` imports, Tailwind `font-[...]`. Generic names such as `sans-serif` are dropped. `(default)` means the Tailwind `font-sans` stack |
| `fontSizeCount` | Distinct literal font sizes | CSS `font-size`, the `font` shorthand, Tailwind `text-xs` to `text-9xl` and `text-[...]` |
| `palette` | Up to 24 colors as `#rrggbb`, most used first | Hex, `rgb()`, `hsl()`, `oklch()`, bare HSL custom properties, Tailwind color classes. Alpha is dropped. A Tailwind step is approximated from its family |
| `ground` | `light`, `dark` or `unknown` | The background of `html`, `body`, `:root`, or the outer `min-h-screen` or `main` element |
| `chromaShare` | Share of color uses that are chromatic | A color counts as chromatic at HLS saturation 0.25 or more and lightness 0.12 to 0.92 |
| `hueHistogram` | 12 bins of 30 degrees, chromatic uses only | Soft binning: each hue splits between its two nearest bins |
| `hueSpread` | The arc in degrees that holds every chromatic hue | 0 is one hue; null is no chromatic color |
| `dominantHue` | The weighted mean hue | null with no chromatic color |
| `gradients` | Count of gradient functions and gradient classes | `linear-`, `radial-`, `conic-gradient`, `bg-gradient-*`, SVG gradients |
| `backdropBlur` | Count of backdrop blur uses | The glass effect |
| `decorBlobs` | Count of large blurred shapes | `filter: blur()` of 30 px or more, `blur-2xl`, `blur-3xl`, classes named blob, orb, glow or aurora |
| `glowShadows` | Count of shadows with no offset, and Tailwind colored shadows | The glow effect |
| `radii` | Distinct corner radii in px, most used first | 9999 means a pill |
| `dominantRadius` | The most used radius | null when none is set |
| `shadowCount` | Count of box and drop shadows | |
| `motion` | `transition` and `animation`, true or false | CSS, `@keyframes`, Tailwind `transition`, `animate-*`, motion library props |
| `copyCliches` | Generic marketing phrases found in the visible text | A fixed list in the script, matched in lower case |

## 2. The skeleton

The script walks the page from `body`. A section, header, footer, nav, aside, article or form starts a block. So does a `div`, `main` or `ul` whose class or id holds a section word such as hero, pricing, faq, logos or footer. An element that holds two or more sections or headers is a wrapper, and the walk goes inside it. Loose content between blocks forms one block.

Each block gets one archetype. The first rule that matches wins:

| Archetype | Matched by |
| --- | --- |
| `footer-columns`, `footer-simple` | A footer; columns when it holds two lists or three similar groups |
| `sidebar-nav` | An aside, or a sidebar class |
| `nav-bar`, `topbar` | A nav, or a header with no h1 and few words. Topbar after a sidebar |
| `faq-accordion` | A faq or accordion class, two or more `details`, or the phrase about frequent questions |
| `pricing-tiers` | A pricing or plans class, or two or more prices |
| `testimonial-grid`, `testimonial-carousel` | A testimonials or reviews class, or two or more quotes. Carousel with a slider class inside |
| `logo-strip` | A logos, clients or partners class, a "trusted by" line, or four or more images with few words |
| `timeline-rail`, `map-led` | A timeline or map class |
| `hero-split`, `hero-media`, `hero-centered`, `hero-plain` | An h1. Split with two columns and media; media with a background image; centered with centering classes or styles |
| `kpi-cards`, `stat-row` | Three or more short number strings and few headings. KPI after a sidebar |
| `data-table`, `chart-panel` | A table; a canvas or a chart class |
| `steps-list` | A steps class, or an ordered list of three or more items |
| `bento-grid`, `three-card-row`, `card-grid` | Mixed column or row spans; three similar items; four or more |
| `pull-quote`, `media-text-split`, `form-block`, `cta-band`, `media-gallery`, `prose-block`, `content-block` | One quote; media in two columns; two or more inputs; a heading with one to three buttons; three or more images; long text; anything else |

Read the skeleton as a shape, not a label. Two pages with the same skeleton tell the same story in the same order.

## 3. How `compare` scores

Each dimension scores 0 to 1. The total is the weighted mean of the dimensions that both sides can score. A dimension with no data on either side is `n/a` and drops out of the mean.

| Dimension | Weight (Default) | Score |
| --- | --- | --- |
| `skeleton` | 0.36 | Longest common order and shared counts, on archetypes and on archetype families (hero, cards, proof, nav, data). Raised by the generic run; see section 4 |
| `palette` | 0.14 | Overlap of the hue histograms, closeness of the chromatic share, the same ground |
| `type` | 0.12 | Shared families, or shared classes: default sans, second-wave sans, second-wave serif, default mono |
| `gradient` | 0.08 | Both use gradients, or neither |
| `copy` | 0.07 | Shared marketing phrases over the shorter list; 0.5 or more when both sides use any. `n/a` when neither side has one; 0 when one side has none |
| `radius` | 0.07 | The same dominant radius bucket (square, small, medium, large, pill) and shared buckets |
| `effects` | 0.06 | The same presence of glass, blobs and glow |
| `shadow` | 0.03 | The same shadow band: none, one to three, four or more |
| `motion` | 0.03 | The same transition and animation flags |
| `fontSizes` | 0.02 | Close counts of distinct sizes |
| `hueSpread` | 0.02 | Close hue spreads |

The score is symmetric: `compare a b` equals `compare b a`. Identical fingerprints score 1.0.

`drivers` lists up to three dimensions with a score of 0.6 or more, ordered by their weighted share. These are the parts to name in the review.

## 4. The generic run and the stacking rules

A template is a sequence. A page that opens with a centered hero, then three cards, then a logo strip, then three price tiers tells the template's story even when it is shorter than the template. The skeleton score reads that sequence directly.

The generic sections are the archetypes that make up templates: `sidebar-nav`, `topbar`, `hero-centered`, `hero-split`, `three-card-row`, `card-grid`, `bento-grid`, `logo-strip`, `testimonial-grid`, `testimonial-carousel`, `stat-row`, `pricing-tiers`, `faq-accordion`, `cta-band`, `footer-columns`, `kpi-cards`, `chart-panel`, `data-table`, `media-text-split`. A nav bar, a plain footer and subject-led blocks (timeline, map, prose) are left out.

- `genericRun` is the longest run of generic sections that both skeletons share in the same order. Other sections may sit between them.
- Containment: the run as a share of the shorter list of generic sections. A run shorter than three counts in proportion. Containment can raise the skeleton score, never lower it, so identical skeletons still score 1.0.
- Run floor. Default: a run of three or more sets the skeleton score to at least 0.75, plus 0.08 for each further section, up to 1.0.

The stacking rules make a pair derivative whatever the weighted average says. Each one needs a generic run of three or more. Default: the run length, the phrase count and the violet share are GDH starting values.

| Rule | Also needs, on both sides |
| --- | --- |
| `STACK_SKELETON_COPY` | Two or more marketing phrases from the list |
| `STACK_SKELETON_GRADIENT` | One or more gradients, and half or more of the chromatic mass in the violet band (hue bins 7 to 10, about 210 to 330 degrees) |

`compare` reports `genericRun` and `stacking` for each pair. The rules read both sides the same way, so the result stays symmetric.

## 5. Verdicts

| Nearest similarity | Script verdict | Exit code |
| --- | --- | --- |
| 0.75 or more (Default, `--threshold`) | derivative | 1 |
| 0.60 or more (Default, `--watch`) | watch | 0 |
| below 0.60 | original | 0 |
| any score, with a stacking rule on any match | derivative | 1 |

When the nearest match by score is below the threshold and another match meets a stacking rule, `check` names that match as the nearest and reports its own similarity. The score is never raised to fit the verdict. The text output prints the generic run and the rules met.

`check --json` prints `verdict`, `score`, `nearest` (with its per-dimension scores and drivers), `matches` (every reference, best first), `line` (the verdict line) and `findings`. A derivative verdict gives one finding of severity high with code `ORIG_DERIVATIVE`. Its message names any stacking rule. A watch verdict gives one of severity medium with code `ORIG_WATCH`. An original verdict gives an empty list.

## 6. Reading a result

- Start with the stacking rules. A rule met means a template sequence plus template copy or a template palette. Rebuild the sequence first.
- Then read the drivers. A high total driven by `skeleton` and `copy` is a structural copy. One driven by `gradient`, `effects` and `palette` is a surface copy. Each needs a different fix.
- Read the next matches. Two archetypes close together mean the work blends two defaults.
- Check the type field against `DESIGN.md`. A required face is `brand-required`; it still counts in the score.
- A high score against an earlier direction means the new work repeats a rejected idea. Read the reason in `design/decisions.md`.
- A low score is not praise. A page can avoid every archetype and still say nothing about its subject. The human tests decide.

## 7. What the script cannot see

- Rendered layout. A grid built in JavaScript, a component library that hides its markup, or CSS that the script did not read leaves the skeleton thin.
- Imagery. The script counts images. It cannot tell a stock photo from a commissioned one.
- Copy voice beyond the phrase list. A page in fresh words with the old message passes the copy dimension.
- Motion quality. It sees that something moves, not how.
- Tokens defined in a file you did not pass. Pass the CSS that defines the variables.
- Components imported from another file in JSX. Pass the folder, or the rendered HTML.

When the skeleton is empty or holds only `content-block`, fingerprint the rendered HTML instead: save the page from a browser and pass that file.

## Sources

- Designing for Emotion (Aarron Walter), ch. 1: do not ship framework defaults as the finished look; ch. 2: brand contrast.
- Anthropic frontend-design skill: the default looks that the library describes.
