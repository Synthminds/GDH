# Content and assets in the package

Read this file at step 10 of `handoff-to-code`. It covers the copy a builder needs, how strings are listed and keyed, how placeholders are marked, and how assets enter the package with their licenses.

Evidence. The real-content rule and the placeholder scan come from the Design Engineering Handbook, chapter 2: DOCUMENTED. The writing rules for interface copy restate the Anthropic frontend-design skill's writing section: DOCUMENTED. The manifest commands were run on 2026-11-23: VERIFIED for the script.

Terms. A string is one piece of interface text with a key. The copy deck is the list of strings. A placeholder is a labelled gap where a fact is missing.

## 1. Real content, not lorem

1. High fidelity uses real content. Search the reference files for lorem ipsum and generic placeholder strings. Zero hits.
2. A missing fact is a bracketed placeholder that names what is missing: `[PRICE PER SEAT]`, `[CUSTOMER QUOTE, APPROVED]`.
3. Every remaining placeholder is listed in section 9 with who supplies it.
4. Never invent a statistic, testimonial, client name or logo.
5. Sample data in a prototype is mock data. Label it sample. No real personal data in shared builds.

## 2. The copy deck

Write section 4.4 of `design/handoff.md`, "Content and the copy deck", as one row per string. Group by screen.

| Key | Screen | Text | Notes |
| --- | --- | --- | --- |
| `calendar.empty.title` | Calendar | No bookings this week | Sentence case |
| `calendar.empty.action` | Calendar | Add a booking | Same verb as the toolbar button |
| `booking.cancel.confirm` | Booking detail | Cancel this booking? The guest gets an email. | Names what happens |
| `error.network` | All | We could not reach the server. Check your connection and try again. | Says what and how to fix |

Rules for interface copy:

1. Write from the end user's view, in their terms.
2. Active voice. A button says what happens.
3. An action keeps one name through the whole flow.
4. An error says what went wrong and how to fix it. It does not apologize.
5. An empty state invites the next action.
6. Sentence case, plain verbs, no filler.
7. A count handles one and many: "1 booking", "3 bookings".

When copy is long or changes often, keep the deck in a separate file under `design/` and link it from section 4.4.

## 3. Localization

1. Say which languages are in scope, or "one language" in the out-of-scope list.
2. Leave room for longer strings. Default: plan for about 40% growth in labels.
3. No text inside images. Diagram labels are real text.
4. Dates, numbers and currency follow the locale. Name the format, not a hard-coded string.
5. Right-to-left: in scope or out of scope. Say which.

## 4. Assets

Write section 6 of `design/handoff.md` as one row per shipped asset, keyed by its manifest id.

| Manifest id | File | Format | Size | Used in | License line |
| --- | --- | --- | --- | --- | --- |
| `logo-primary` | `design/assets/logo/svg/logo-primary.svg` | SVG | 3 KB | Header, footer | own |
| `hero-harbor` | `design/assets/photo/hero-harbor.jpg` | JPEG | 1600 x 900 | Home hero | Photo library license, no credit required, read 2026-11-20 |
| `icons-ui` | package `@icon-set@x.y.z` | package | n/a | All | MIT; notice in the third-party notices file |

Rules:

1. Every shipped asset has a manifest record. Run `A check design/assets/manifest.json --root .`, with `--scan <source folder>` once code exists.
2. A reference image from a mood board never ships. The check reports files under the reference folder.
3. A generated asset carries origin `generated` and the tool name in its note.
4. A font file names its license and its loading rule from `typography`.
5. A 3D model names the decoders it needs and its size against the budget.
6. A person in a photo or a video has a consent or license note.
7. Write a notices file for any license that needs one: `A notices design/assets/manifest.json -o ATTRIBUTION.md`.

`A` is the script of the `find-assets` skill. Record a new asset with its `record` command, never by hand.

## 5. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Lorem at high fidelity | Placeholder Latin in a reference file | Real copy or a labelled placeholder |
| Copy in screenshots only | Strings exist only as pixels | A copy deck with keys |
| Two names for one action | "Remove" on the list, "Delete" in the dialog | One verb |
| Mood board leak | A reference image in the build | The asset check; replace it |
| License by memory | "Probably free" | Read the license page; record it |
