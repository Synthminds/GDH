# Page plan, story and copy

Read this file at steps 3 to 5 of `website-design`. It covers the site shape, the page inventory, the order of the story, the copy deck and the placeholder rule. The output is the first half of `site-plan.md`.

Terms. A page job is the one thing a visitor can do or know after the page. A primary action is the one control that completes the job. A copy deck is all the words of the site in one plain file. A placeholder is a labelled gap that names what is missing.

## 1. Choose the site shape

| Site shape | Use it when | Default page set |
| --- | --- | --- |
| Single landing page | One offer, one audience, one action | One page, plus legal pages as plain documents |
| Product marketing site | One product, several audiences or use cases | Home, product, pricing, proof, about or contact |
| Company or service site | A firm sells its work or its people | Home, services, work or cases, about, contact |
| Content site | The content is the product | Index, article, category, about, search |
| Launch or waitlist page | The product is not ready | One page with one form and a stated date or state |

Decision rules:

1. Start from the smallest shape that holds every page job.
2. Add a page only for a job that no current page can hold.
3. Merge two pages that share one job.
4. A page with no job is cut. "Every site has an About page" is not a job.
5. Default: four top-level navigation items at one decision point. The brief can raise the number.

## 2. The page inventory

Write one row for each page. Fill every cell. An empty cell is an open question for the user.

| Column | What to write | Test |
| --- | --- | --- |
| Page | A name in the visitor's words | A visitor would use this word in a search |
| Arrives from | Search, an ad, a link in a message, the navigation | Names a real entry route from the brief |
| Question in the head | The one question the visitor brings | Written as a question, in the first person |
| Job | "After this page the visitor can ..." | One clause. No "and" |
| Primary action | The one control that completes the job | A verb and an object: "Book a repair" |
| Proof needed | What makes the claim believable | Names a real item the user holds, or a placeholder |
| Content owner | Who supplies the facts | A person or a file, never "TBD" |
| Status | planned, copy ready, built, verified | Updated at each round |

The one-job test: finish the sentence "After this page the visitor can". When the sentence needs "and", do one of two things. Split the page, or rank the jobs and make the second one a secondary action.

Secondary actions are allowed. They are visually quieter, and there is one primary action in each view.

## 3. Order the story by the visitor's questions

A page is an argument. Order its sections by the questions a visitor asks, not by a template.

The question ladder:

| Order | Visitor question | Section that answers it | Evidence it needs |
| --- | --- | --- | --- |
| 1 | What is this? | Opening view: the claim and the real thing | The product, the place or the work, shown |
| 2 | Is it for me? | Who it serves and the situation it fits | A named situation from the brief or from research |
| 3 | How does it work? | The mechanism, in the fewest real steps | A real sequence, a real screen, a diagram |
| 4 | Can I believe it? | Proof | A sourced figure, a named customer, a quote with permission |
| 5 | What does it ask of me? | Price, time, effort, risk | Real numbers or a labelled placeholder |
| 6 | What do I do next? | The primary action, repeated | One action, named the same way each time |

Default: change the order by how much the visitor already knows. This is a rule of thumb, not a tested result.

| Visitor | They know | Open with | Move earlier |
| --- | --- | --- | --- |
| Cold (an ad, a broad search) | Nothing about you | Their situation, then what this is | Question 2 and question 3 |
| Warm (a referral, a comparison) | The category and your name | What makes this one different | Question 4 |
| Hot (a returning visitor, a price search) | They want to act | The action and the price | Question 5 and question 6 |

Rules:

1. Cut any section that answers no question on the ladder.
2. Answer each question once. Repeat only the primary action.
3. Put proof beside the claim it supports, not in a separate strip at the end.
4. State the order and its reason in one line for each page in `site-plan.md`.

## 4. Write the copy deck first

Write the words before any layout. Layout that waits for copy fits the copy. Copy poured into a finished layout becomes filler.

The copy deck holds, for each page:

- The page title for the browser tab and the meta description.
- The headline and the supporting line of the opening view.
- For each section: the claim in one sentence, the support, and the action label.
- Every button and link label.
- Form labels, help text, each error message and the success message.
- Empty, loading and error text for each content region.
- Alt text for each planned image.
- Navigation and footer labels.

Copy rules. The design system and the brand voice in the brief rank above these.

1. Use the visitor's words. Take them from the brief, from interviews or from the user's own messages.
2. A button names what happens: "Book a repair", never "Submit".
3. An action keeps one name through the whole flow.
4. An error says what went wrong and how to fix it. It does not blame the visitor.
5. An empty state invites the next action.
6. Write sentence case and plain verbs. Cut each word that carries nothing.
7. Write figures with their source and their date.

Three headline tests:

| Test | How to run it | Fail sign |
| --- | --- | --- |
| Swap | Put a competitor's name in place of the subject | The headline still reads as true |
| So what | Ask "so what?" after the headline | The answer is a better headline than the headline |
| Aloud | Read it aloud once | You would not say it to a person |

A failed headline is rewritten from the subject: its material, its place, its method, its proof.

## 5. Placeholders

Kernel rule 11 holds: invent nothing factual. A gap becomes a labelled placeholder.

Format: `[PLACEHOLDER: what is needed, who can supply it]`. Example: `[PLACEHOLDER: turnaround time in days, from the shop owner]`.

Rules:

1. A placeholder is visible in the copy deck, in the build and in the placeholder list.
2. Never fill a gap with a plausible figure, a sample quote, a stock logo or a made-up customer.
3. Sample data in a demo carries the label "Sample".
4. Each placeholder is an open question in `design/decisions.md`.
5. Gate: no unlabelled placeholder ships. A labelled one ships only with the user's recorded yes.
6. Design the section to work with the real item. Size a quote block for a real quote length, not for two lines.

## 6. Content to collect before layout

ASK for these items in one message. Mark each as received, promised or absent.

- The logo files and the brand pack, or the design system link.
- Product screens, product photographs or photographs of the place and the people.
- Prices, plans, terms, opening hours, service area.
- Proof: figures with sources, customer names with permission, quotes with permission, awards, press.
- Legal text: privacy notice, terms, imprint, cookie rules for the target market.
- Contact routes and what happens after a form is sent.
- Existing analytics or search terms, when a site already exists.
- The old URL list, when this site replaces one.

Absent proof changes the design. With no customer quote, do not draw a quote section. Use what exists: the method, the maker, the material, a guarantee.

## 7. Worked example

The subject is invented for this example: a repair shop for film cameras. Brand words: exact, patient, hands-on. Primary job: get a visitor to book a repair.

Inventory, shortened:

| Page | Arrives from | Question in the head | Job | Primary action | Proof needed |
| --- | --- | --- | --- | --- | --- |
| Home | Search for a camera model and "repair" | "Can they fix mine?" | See that their model is serviced and book | Book a repair | Model list; bench photographs |
| Repairs and prices | Home, search | "What will it cost and how long?" | Know the price range and the wait | Book a repair | Price table `[PLACEHOLDER: prices, from the owner]` |
| How a repair goes | Home | "Is it safe to post my camera?" | Trust the process | Book a repair | The real steps; insurance terms |
| Contact | Any page | "Where are they?" | Reach the shop | Send a message | Address, hours |

Reasoning:

- "About" was cut as a page. Its only content, the technician's history, is proof. It moved beside the claim on Home.
- The visitor is warm: they own a broken camera and searched a model name. The home page opens with the serviced models, not with a mission line.
- The headline "Expert camera repair you can trust" fails the swap test. The rewrite names the subject: "We repair mechanical film cameras, one at a time, on a bench in [PLACEHOLDER: city]."
- No customer quote exists. The plan has no testimonial section. The repair log with before and after photographs is the proof.

## 8. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Template order | Hero, three features, testimonials, pricing, footer, with no reason from the content | Order by the question ladder. State the reason for each section. |
| Two jobs, one page | The job line needs "and"; two buttons compete | Split, or rank and quiet the second action |
| Lorem launch | Layout exists and the copy does not | Stop the build. Write the copy deck. |
| Feature tour | Section after section of features, no proof and no price | Add questions 4 and 5, or cut features |
| Orphan page | A page that nothing links to and no route reaches | Give it an entry route or cut it |
| Borrowed proof | A logo strip or a quote that the user cannot source | Remove it. Use a labelled placeholder or real proof. |
| Mission opening | The first view talks about the company, not the visitor | Open with the visitor's question |

## 9. Checks

Gates:

- Every page has one job and one primary action.
- Every fact in the copy has a source, or is a labelled placeholder.
- The copy deck exists before the first high-fidelity layout.
- The user saw the inventory and answered keep, change or remove.

Defaults:

- Default: four top-level navigation items.
- Default: a new visitor can say what the site is, who it is for and what to do next after 5 seconds. This is a rule of thumb. Test it with a person who has not seen the page.
- Default: one copy deck file for the site, inside `site-plan.md`.
