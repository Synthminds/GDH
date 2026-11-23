# Group: inspiration galleries

Catalog group `inspiration`: reference galleries. Read this file at step 6 of `find-assets` when someone wants to look at how others solved a problem.

How to read this file. An id is a catalog id. Every id in this group is marked `*`: no gallery's terms were read for the catalog. Every entry has `commercialUse` set to `reference-only`. That value does not depend on the terms: the work in a gallery belongs to the people who made it.

**Nothing from this group enters a project.** No image, no layout, no copy, no code. A gallery is a place to look and learn.

## Galleries by question

| Question | Catalog ids | Good for | Limit of the evidence |
| --- | --- | --- | --- |
| How do shipped apps handle this flow? | `mobbin*`, `refero*` | Real screens of real products, in order | The catalog note for `mobbin*` says its terms forbid derivative works, re-hosting, scraping and AI use. Unread. |
| How do landing pages open and sequence? | `land-book*`, `lapa-ninja*`, `godly*`, `siteinspire*`, `minimal-gallery*`, `dark-mode-design*`, `awwwards*` | Section order, first-view composition, density | Curated for novelty. A gallery pick is not proof that a pattern works. |
| What moods exist for this subject? | `are-na*`, `savee*`, `pinterest*`, `behance*`, `dribbble*` | Color temperature, texture, image style | Many pins are third-party work with no source. Many shots are concepts that never shipped. |
| Which typefaces are used where? | `fonts-in-use*` | Real uses of named typefaces | It names the face. The license still comes from the foundry. |
| How are identities built and argued? | `brand-new*`, `logo-archives*` | Before-and-after identity cases; historic marks | Every mark is a trademark |

## Rules

1. Browse by a question from the brief, not by "what looks good".
2. Record a lesson, not a picture. Use the note form below.
3. Write the lesson in your own words. Name the pattern, the mood, the type classification or the color temperature.
4. Keep a thumbnail only for a private review with the user. Never commit it to a public repository. Never ship it.
5. Do not rebuild from a gallery screenshot. Go to the live product and run `reverse-engineer-reference`.
6. Never scrape a gallery. Never bulk-save. Never build a reference set by script.
7. Default: do not pass a gallery's screenshots to a model or a generation tool. One catalog note names a clause against it. Unread.
8. Default: take references from three galleries or more. One gallery has one taste.
9. Default: take one reference or more from outside the product's category. References from inside the category lead to the category's default look.
10. Treat a list of looks for a category as the looks to move away from, unless the brief asks for convention.
11. A concept shot is an idea. It was never tested with users. Do not cite it as proof.
12. The user's own liked and disliked references in the brief outrank anything you find here.

## The lesson note

Write one note for each reference in the direction notes under `design/directions/`.

```
Ref: <URL> (seen <YYYY-MM-DD>)
Question: <the brief question this answers>
Lesson: <the pattern or quality, in your own words>
Use: <where it could apply in this project>
Avoid: <what belongs to them and stays with them>
```

A good lesson passes three tests:

- It holds no proper noun from the reference.
- It holds no pixel value and no color value.
- A second, unrelated product could have taught the same lesson.

| Weak note | Strong note |
| --- | --- |
| "Like their hero" | "One sentence, one action, and the product itself as the image. No decoration." |
| "Use that purple gradient" | "A single saturated accent on a near-neutral page. The accent marks only the primary action." |
| "Copy the onboarding" | "Ask for one thing on each screen. Show progress as a count, not a bar." |

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Screenshot board | A folder of saved gallery images with no notes | Write a lesson note for each. Delete the rest. |
| Single-source direction | Every reference comes from one site or one product | Apply rules 8 and 9 |
| Category echo | The result looks like the gallery's page for that category | Add references from outside the category. Return to the brand words. |
| Concept as proof | "A well-liked shot does this" as the reason | Find a shipped product that does it, or test it |
| Shipped reference | A gallery image in an asset folder | `REFERENCE_SHIPPED` or `FILE_UNRECORDED`. Remove it. |
| Traced layout | A build that matches a reference section for section | Run the originality check in `reverse-engineer-reference` |

## Handoffs

- To `mood-board`: lesson notes become inputs for directions.
- To `reverse-engineer-reference`: a reference worth a close study gets a teardown sheet.
- To `typography`: a face seen in use goes there for a decision. It returns here for sourcing.
