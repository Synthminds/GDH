# The generic archetypes

Read this file when a match looks wrong, or when a new generic look starts to repeat. It lists the archetypes in [generic-fingerprints.json](generic-fingerprints.json) and says how to add, change or retire one.

Library version: 2026-11-26. Each archetype is a description written for GDH and a fingerprint computed from a small sample page that shows the look. No page from a real product was copied.

## 1. The list

| Id | Name | What marks it |
| --- | --- | --- |
| `ai-saas-landing` | AI SaaS landing page | Nav, centered hero, logo strip, three feature cards, quotes, three tiers, accordion, closing call to action, footer columns. Default sans, indigo to violet, large corners, filler copy |
| `centered-hero-gradient-blob` | Centered hero with gradient blob | A dark page whose one idea is a centered headline over blurred glowing shapes. Pill buttons, glass, a floating loop |
| `bento-grid` | Bento grid feature page | Centered hero, then feature tiles of mixed sizes with hairline borders and faint gradients on near-black |
| `three-tier-pricing` | Three-tier pricing page | Centered pricing headline, three plan cards with a raised middle card, accordion, footer columns |
| `dark-glass-dashboard` | Dark glassmorphism dashboard | Blurred sidebar and top bar, frosted KPI cards with glows, chart, table. Cyan and violet on near-black |
| `purple-gradient-ai-startup` | Purple-gradient AI startup | Gradient headline in violet to magenta, logo strip, glowing feature grid, unsourced big numbers |
| `default-shadcn-admin` | Default component-kit admin | The example admin layout of a popular component kit: sidebar, search bar, four metric cards, chart, table. Neutral zinc, small corners, faint shadows |
| `stock-testimonial-carousel` | Stock testimonial carousel page | Split hero with a product image, a sliding row of quotes with round avatars and job titles, logos |
| `blue-product-split` | Blue product split page | Split hero beside a screenshot, logo strip, three alternating image and text rows, blue accent |
| `warm-editorial` | Warm editorial studio page | Cream ground, display serif, one italic accent word, monospace issue labels, square buttons |
| `night-signal` | Night signal agency page | Near-black ground, one acid accent, huge grotesque type, numbered monospace labels |

The last two are the second-wave looks: the reflex choices that replaced the gradient once agents learned to avoid it. The tell list in `design-critique` and the known default looks in `mood-board` name the same family. Change the three together.

## 2. When a match looks wrong

- A dashboard that matches `default-shadcn-admin` because it uses that kit by brand rule is `brand-required` on type, radius and palette. The skeleton driver still counts. Ask whether the layout is the kit's example or this product's own.
- A page that matches `warm-editorial` because the subject is a print studio may be right to use a serif. Check the signature moment and the swap test before you accept the match.
- A skeleton of only `content-block` means the script could not read the structure. Fingerprint the rendered HTML instead.

Record a false match in the review with the reason. Do not raise the threshold to pass one page.

## 3. How to add an archetype

Add an archetype when one look appears in three or more reviews, or when a new generic look is widely shipped. Default: three sightings.

1. Write a short sample page that shows the look and nothing else. Use plain HTML and one style block. Write your own placeholder copy; copy no text and no code from a real site.
2. Put in the parts that make the look: its section order, its type families, its palette, its effects, its corners and its motion.
3. Run `python3 scripts/originality.py fingerprint sample.html --json` from the skill folder.
4. Read the skeleton. When a section lands on the wrong archetype, fix the sample markup, not the script.
5. Add an entry to `generic-fingerprints.json`:
   - `id`: kebab-case, unique, the name of the look, not of a product.
   - `name`: a short human name.
   - `description`: one paragraph in your own words. Name the parts, not a company.
   - `fingerprint`: the printed object. Set `files` to `["sample:<id>"]`.
6. Run `python3 scripts/originality.py compare` between the new entry and each near archetype. Default: a new entry that scores 0.90 or more against an old one is a duplicate. Merge it instead.
7. Set the library `version` to today's date.
8. Run the tests: `python3 -m unittest discover -s tests`. The library symmetry test reads every entry.
9. Add a row to the table in section 1 and a line to the skill's `refinement-log.md`.

Do not add the sample page to the repository. The fingerprint is the record.

## 4. How to change or retire one

- Change an archetype when the look shifts: rebuild its sample, refingerprint it and replace the entry. Keep the id.
- Retire an archetype when it stops showing up in reviews for two review cycles. Default: two cycles of 90 days. A stale library becomes a template of its own.
- Log each change in `refinement-log.md` with the reason.

## 5. Competitors and earlier directions

The library holds only generic looks. Competitor pages and earlier directions belong to the project, not the kit.

- Save a competitor page as HTML, fingerprint it with `-o design/reviews/fingerprints/<competitor>.json`, and pass the folder with `--against`.
- A competitor page is a reference. It never ships, and its fingerprint holds no copy text.
- Fingerprint each rejected direction once. A new direction that scores high against a rejected one repeats a decision the user already made.

## Sources

- Anthropic frontend-design skill: the default looks of generated pages.
- Designing for Emotion (Aarron Walter), ch. 1: framework defaults as an unfinished look.
