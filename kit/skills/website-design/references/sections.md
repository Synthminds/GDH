# Section design

Read this file at step 7 of `website-design`. It turns the copy deck into sections whose form comes from their content. It names the template skeleton, gives the tests that catch it, and shows one worked page.

Precedence. A form that the user or the design system requires is `brand-required`. It is never a tell and never a finding. The tell list is a GDH default; its dated version lives in `design-critique`. Avoiding tells is not the method. The method is: derive each form from this subject and this content.

## 1. The method in five moves

1. Name the content shape of the section. Use the table in part 2.
2. Pick a form that fits the shape. Reject the form you would pick for any product.
3. Decide what the visitor sees first, second and third inside the section.
4. Run the three tests in part 5.
5. Write one plan line: job, content shape, form, the first thing seen.

Plan line format for `site-plan.md`:

```
<n>. <section name> | answers: <ladder question> | shape: <content shape> | form: <form> | first seen: <element> | action: <label or none>
```

## 2. Content shape decides form

| Content shape | Forms that fit | Default to avoid, and why |
| --- | --- | --- |
| One claim and one proof | A large statement with the evidence beside it | A card. One claim does not need a box |
| A real sequence | A numbered list, a timeline, steps along a line | Unnumbered equal cards. They hide the order |
| Items that are not a sequence | A plain list, a grid without numbers | Markers 01, 02, 03. Numbers claim an order that does not exist |
| One main item and supporting items | An uneven grid: one large, the others small | Three equal cards. Equal boxes claim equal weight |
| Many like items | A uniform grid, a table, a list with filters | A carousel. It hides most items |
| A comparison across attributes | A table with real row and column headings | Side-by-side cards with long bullet lists |
| The product itself | The real interface, photograph or object, large, with annotations | An abstract gradient shape that stands in for the product |
| A figure | The figure in a sentence with its source, or a small chart | A big number, a small label and an accent. It is the stat-tile template |
| A quote | A pull quote in the reading flow, with a name and a role | A rotating quote slider with stock portraits |
| Questions and answers | A definition list, or an accordion of real questions | Invented questions that restate features |
| A price | A table of real plans, with the unit and the terms | "Contact us" where a price exists |
| A place or a person | A photograph with a caption in the copy | A stock image of a handshake |

Rules:

1. A uniform grid is right when the items are alike. It is wrong when it is the frame for everything.
2. A number, a border, a label or a divider appears only where it carries information.
3. Section structure differs where content differs. Two sections of the same kind may share a form.
4. One memorable element for the page. Keep the rest quiet. Spend boldness in one place.
5. Default: four items at one decision point. A longer list needs grouping or a filter.

## 3. The opening view

The first view answers "what is this?" before the visitor scrolls. Open with the most characteristic thing in the subject's world.

What the first view must hold: the claim, who it is for when that is not obvious, the primary action, and one sight of the real thing.

| Opening form | Use it when | Do not use it when |
| --- | --- | --- |
| Product as the hero | The product is visual and the interface or object explains itself | The screen is a generic table or form |
| Statement in type alone | The claim is surprising and the typeface carries the voice | The claim is ordinary. Large ordinary words are still ordinary |
| Photograph or film | The place, the people or the material is the offer | Only stock imagery exists |
| Working demo | A visitor can try the core action in seconds without an account | The demo needs set-up or sample data to make sense |
| Split: claim and evidence | A claim needs proof beside it at once | The evidence is weak or absent |
| Form first | The visitor is hot and the job is one short form | The visitor does not yet know what this is |

Rules:

1. The headline passes the swap test before any styling.
2. One primary action. A second action is quieter and names a different need.
3. The big number with a small label and a gradient accent is the default hero. Use it only when a real, sourced figure is the claim.
4. A centered headline over a centered button is one option, not the starting point. Try the split and the product forms first.
5. The opening image is the largest file on the page. Budget it with the performance reference.

## 4. Rhythm down the page

- Alternate dense and open sections. Three dense sections in a row tire the reader.
- Change the alignment or the scale where the topic changes. Keep it where the argument continues.
- Repeat the primary action after proof and after price. Use the same label each time.
- End the page with the action and the facts a visitor needs to act: place, hours, contact, terms.
- The footer is a utility: site map, legal, contact. It is not a second home page.

## 5. Three tests for each section

| Test | How to run it | Fail sign | Fix |
| --- | --- | --- | --- |
| Swap | Read the section with a competitor's name in it | Nothing needs to change | Rewrite the copy and the visual from this subject |
| Delete | Remove the section from the plan | No ladder question loses its answer | Cut the section |
| Squint | Blur the wireframe, or view it at thumbnail size | It looks like the section above and below | Change the form to match the content shape |

Run the swap test on the whole page plan too. A plan that fits any product in the category is rewritten before the build. Say what changed and why.

## 6. The template skeleton

This is the page a model produces when nothing decides the form. Each part has a counter-move.

| Part of the skeleton | Counter-move |
| --- | --- |
| Centered hero with a gradient headline | Open with the subject's real thing. Solid token color. Emphasis by size, weight or position |
| A row of three equal icon cards | Find the content shape. Unequal content gets unequal space |
| A strip of big numbers | Show a figure only with a source, in a sentence or a chart |
| A logo wall | Only real logos, with permission. Otherwise no strip |
| A testimonial slider | One real quote in the reading flow, or no quote |
| A small tracked label above every heading | Delete each label that repeats its heading. Keep one that names a real category |
| The same fade and slide on every section | One authored entrance. Run the motion pass with `ui-motion` |
| An arrow after every link | An arrow only where it marks a real change of place |
| A hover lift on every card | Hover feedback only on things that act |
| One radius and one gray shadow on everything | Radius and elevation tokens by role |

The reaction to the skeleton is also a template. Three current ones: a cream ground with a serif headline and a terracotta accent; a near-black ground with one acid accent; a newspaper layout with hairline rules. Use one only when the brief leads there, and record the reason.

## 7. Navigation and footer

- Navigation labels are the page names from the inventory, in the visitor's words.
- Navigation uses real links. Middle-click and "open in a new tab" must work (read: Vercel).
- The current page is marked by more than color.
- The primary action may sit in the header. It keeps its label.
- A skip link is the first focusable element. It jumps to the main content.
- Default: collapse the navigation into a labelled "Menu" button only when the items do not fit. Four items or fewer usually fit.

## 8. Worked example

The invented repair shop. The first plan came out as the skeleton. The second plan came from the content.

Before:

```
1. Hero: centered "Expert camera repair you can trust", button "Get started"
2. Three cards: Fast, Reliable, Affordable
3. Stats: 5,000+ cameras, 98% satisfaction, 20 years
4. Testimonials slider
5. Call to action banner
```

Findings: the headline passes for any repair business. The three cards are adjectives, not content. The figures have no source. No quote exists. Every section fails the swap test.

After:

```
1. Opening | answers: what is this | shape: claim and proof | form: split 5 and 7 | first seen: bench photograph with a camera open | action: Book a repair
2. Models we service | answers: is it for me | shape: many like items | form: filterable list by maker | first seen: the maker names | action: none
3. How a repair goes | answers: how does it work | shape: real sequence | form: numbered steps, one photograph at "test roll" | first seen: step 1 | action: none
4. Repair log | answers: can I believe it | shape: the product itself | form: three recent repairs, before and after, dated | first seen: one before and after pair | action: none
5. Prices and wait | answers: what does it ask | shape: comparison | form: table by repair type | first seen: the price column | action: Book a repair
6. Post it or bring it | answers: what next | shape: place | form: address, hours, posting steps | first seen: the address | action: Book a repair
```

Reasoning:

- Section 2 exists because the visitor arrived with a model name. A grid fits: the items are alike.
- Section 3 keeps its numbers. The steps are a real order.
- Section 4 replaces the invented figures and the absent quotes with proof the shop already has.
- The one memorable element is the open camera in the first view. Everything else is quiet.

## 9. Named failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Hero, three cards, done | A centered headline over a three-column grid | Part 2 and part 3 |
| Adjective cards | Card titles are adjectives: fast, simple, secure | Replace each with a fact and its evidence, or cut it |
| Stat strip | Three or more big numbers with no source | A sourced figure in context, or nothing |
| Icon tile stack | A rounded square icon above each heading | Remove the tiles. Use an image only where it explains |
| Card in a card | A boxed item inside a boxed section | Remove one box. Use space |
| Bento for its own sake | Tiles of mixed size with no ranking behind the sizes | Size by importance, or use a plain list |
| Centered everything | Every block centered, every line short | Choose one alignment system from the layout reference |
| Label chrome | Small labels, numbers and dividers that encode nothing | Delete them |
| Proof at the bottom | Claims at the top, all proof in one late strip | Put each proof beside its claim |
| Softened tell | A default gradient at half strength | Rebuild the element from the brief. Do not soften it |

## 10. Checks

Gates:

- Each section answers one ladder question and has one plan line.
- No section holds an invented figure, quote, logo or customer.
- The page plan passed the swap test, or each failing part has a reason from the brief in the record.

Defaults:

- Default: one primary action in a view.
- Default: one memorable element for a page.
- Default: four items at one decision point.
- Default: a tell that the brief does not ask for is rebuilt, not softened.
