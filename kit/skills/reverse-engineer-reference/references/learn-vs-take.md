# What you may learn and what you may not take

Read this file before the first capture. It sets the line between study and copying, the way to cross from a measured fact to a usable lesson, and the limits on which targets you may study.

This file is working practice. It is not legal advice. The user carries the legal duty for the target: laws, contracts, terms of service and the rights of others.

## The two lists

| You may learn | Example of a lesson |
| --- | --- |
| Structure | The order of sections, the job each one does, what the first view contains |
| Layout system | Column count, gutter logic, maximum width, alignment, how the grid breaks |
| Type scale | How many sizes, the ratio between steps, which role gets which step |
| Spacing rhythm | The base unit, the multiples in use, how density changes by section |
| Color roles | How many hues, where the accent appears, how much of the page is neutral |
| Motion timing | Durations by element size, the easing family, the order of a sequence |
| Technique | Which platform feature or library makes an effect, and how it is composed |
| Content pattern | What kind of statement sits where: a claim, a proof, an action. Not the words. |
| States and behavior | What hover, focus, loading, empty and error look like |

| You may not take | Why |
| --- | --- |
| Code: markup, style sheets, scripts, shaders, class names | It is someone's protected work |
| Assets: images, illustrations, icons, fonts, video, models, sounds | Each has an owner and a license you do not hold |
| Wording: headlines, body copy, button labels, product names | It is their voice and their text |
| A distinctive look | The combination that makes people say "that is them" |
| Logos and marks | Trademarks |
| The whole of a value set | Their full palette, their full type scale, their full spacing scale |
| Their data | Numbers, testimonials, customer names |

One measured value is a fact about the world. A complete set of their values is their design system.

## The ladder: observation, principle, translation

Every finding climbs three rungs before it can be used. The sheet holds all three.

| Rung | What it is | Rule |
| --- | --- | --- |
| Observation | What you measured or saw | Stays in the sheet. Never enters the build. |
| Principle | The transferable idea behind it | Your own words. No proper noun, no pixel value, no color value. |
| Translation | How this project applies the principle | Names this project's tokens and this project's content |

Examples:

| Observation | Principle | Translation |
| --- | --- | --- |
| Headline 72 px, body 18 px, five sizes in all | A steep scale with few steps: display is four times body | Use `display-xl` and `body-md`. Drop the two middle steps on marketing pages. |
| The accent color appears on one button and one link in each view | The accent is scarce: one action in each view | `color.accent` marks the primary action only. Links use the text color with an underline. |
| Hero lines rise in turn: 600 ms, ease-out, 80 ms apart | Reveal in reading order, with a long ease-out for a page-level moment | Map to the page-level motion token. With reduced motion, show the final state at once. |
| Sections alternate between 96 px and 160 px of vertical space | Two densities: tight inside a topic, loose between topics | Use `space-section` between topics and `space-block` inside one. |
| The pricing table shows three plans and marks the middle one | Offer few choices and recommend one | Show the plans the client has. Mark the one the brief names as the default. |

A translation that ends in the same values as the observation is not a translation. Go back to the principle and start from this project's tokens.

## Three tests for a lesson

1. **Own-words test.** The lesson holds no proper noun from the reference, no pixel value and no color value.
2. **Substitution test.** Replace the reference's name with this project's name in the sheet. A lesson that still makes sense only for them is not a lesson.
3. **Two-source test.** Name a second, unrelated product that follows the same principle. When you cannot, the thing may be a signature. Default: leave it.

## Signature elements

A signature element is something that identifies the reference at a glance. Name them in the sheet. They are the first thing the originality check looks for.

Typical signatures:

- One unusual color, or one unusual pair of colors, used everywhere.
- A custom or rare typeface used at display size.
- A recurring shape, motif or illustration style.
- A motion that people describe when they describe the site.
- A layout device that few others use.
- A mascot, a photographic style, a tone of voice.

Rule: the more a thing is admired, the more likely it is a signature. When the user says "I love their X", ask what X does for the user. The lesson is the effect, not X.

Precedence still holds. When this project's design system already requires something that resembles a reference's signature, report it as `design-system-required`. It is not a failure. Tell the user about the resemblance once.

## Which targets you may study

| Target | Allowed route | Limits |
| --- | --- | --- |
| A public page, no login | Browser, tool or by hand | Capture only the pages you study. Never crawl the site. |
| The user's own site or app | Any route | Its tokens may seed the project, marked unreviewed |
| A product the user may use, behind a login | Screenshots the user takes and supplies | No automation behind the login unless the user is authorized to test it |
| A competitor's product behind a paywall or a trial wall | None | Do not sign up to study it. Use its public pages. |
| A screenshot in a gallery | Go to the live product | The gallery's image is a reference with no further use |
| A native app | Screenshots and screen recordings from the user | Separate what the platform supplies from what the app designed |
| A page that blocks automated access | By hand, by the user | Respect the block. Do not work around it. |

Rules for every target:

1. The user confirms the right to study it. Write the confirmation in the sheet.
2. Public does not mean permitted for every operation. Reading a page is not the same as exporting its scripts.
3. Never defeat an access control: a login, a bot wall, a license check, a paywall.
4. Observing a page can change its state. Use a separate browser profile with no personal session.
5. Keep what you capture private. A capture is someone's work shown on your screen.
6. Delete exported scripts when the study ends. Keep the notes.

## Where captures live

- Screenshots, recordings and the inventory file sit under `design/directions/references/<slug>/`.
- That folder is never an asset folder. Nothing in it ships.
- In a public repository, add `design/directions/references/*/shots/` to the ignore file. A screenshot of someone's product is not yours to publish.
- A screenshot never goes to a generation tool as a style source without a yes. That is an upload of someone else's work.
- The teardown sheet itself may be committed. It holds notes in your words, not their material.

## Failure patterns

| Name | What happens | The test that catches it |
| --- | --- | --- |
| Skin swap | Their layout with this project's colors and logo | Originality axis 1 and 2; the swap test |
| Pixel trace | A build made by laying a screenshot under the canvas | A pixel diff that is low against the reference |
| Token lift | Their palette or scale copied into this project's tokens | Compare `design/tokens.json` with the inventory |
| Copy echo | Their headlines paraphrased line by line | Originality axis 6; read both pages side by side |
| Signature theft | The one thing that makes them them | The signature list in the sheet |
| Single-source design | One reference studied, so the result converges on it | Step 2 of the skill: three to five references |
| Capture creep | A whole site crawled "to be thorough" | Capture only the pages named at step 1 |
| Shipped capture | A screenshot or a saved image in an asset folder | `assets.py check`: `REFERENCE_SHIPPED` or `FILE_UNRECORDED` |
| Script paste | Handler code copied because "it is only a few lines" | No reference code enters the project. Write the technique note, then write new code. |

## Worked examples

**1. "Make our docs site feel like theirs."** The user admires a developer documentation site. Asked what exactly, the user says: "I always know where I am." The lesson is not their sidebar. Observation: three levels of navigation are visible at once, and the current page is marked in each. Principle: location is shown at every level, all the time. Translation: this project's sidebar, breadcrumb and page outline each mark the current place with `color.accent` and a weight change. Their typeface, their green and their code block style stay with them.

**2. "How do they do that scroll effect?"** The user wants to know how a product page pins an image while text scrolls beside it. The tool route shows that no animation library is involved: it is sticky positioning with a scroll-linked opacity change. Technique note: "Pin the media column with sticky positioning. Fade between media states as each text block crosses the middle of the viewport." This project writes its own version with its own media, its own motion tokens and a reduced-motion path. No line of their script is kept.
