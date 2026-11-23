# Topic tree and depth

This file sets the order of the interview, the prerequisites of each topic, the brief section each topic fills, and how deep to go for each job size.

## Topic 0: the subject

Before topic 1, restate the request in one sentence: what is being designed, and what it is not. Ask one question to confirm it. The answer fills brief section 1.

## The tree

Walk the topics in this order. A topic opens only when the topics in "Needs settled" are answered or ASSUMED. Within a topic, a question opens only when the questions it builds on are settled.

| # | Topic | Needs settled | Fills brief section | Look up first |
| --- | --- | --- | --- | --- |
| 1 | People served and context | 0 | 2 | `PRODUCT.md`, personas, support docs, onboarding copy, analytics notes |
| 2 | Need and point of view | 1 | 3 | The request, the README, `PRODUCT.md`, earlier decisions |
| 3 | Feel | 1, 2 | 4 | Voice in `DESIGN.md`, the tone of existing copy |
| 4 | Primary job and success | 2 | 5 | `PRODUCT.md`, analytics notes, the request |
| 5 | Design persona | 1, 3 | 6 | `DESIGN.md`, a brand guide, a brand pack |
| 6 | Brand, existing system and assets | 0 | 7 | `DESIGN.md`, `design/tokens.json`, brand packs, a hosted design system, asset folders, the live site |
| 7 | Taste | 3, 6 | 8 | `design/decisions.md`, references the user named |
| 8 | Constraints | 4 | 9 | The package manifest, framework config, policy files, test config |
| 9 | Risks and the worst case | 1, 4 | 10 | Support messages, reviews, incident notes |
| 10 | Decision rights | 0 | 11 | `design/decisions.md`, an owners file |
| 11 | Scope, out of scope and fidelity | 4, 8 | 12 | The request |
| 12 | Tools, spend budget and exposure | 11 | 13 | The tool catalog and the tools present in this session |
| 13 | How feedback rounds run | 10, 11 | 14 | `design/decisions.md` |

Brief section 15 holds every ASSUMED line and every open question. Each topic adds to it.

Topic 6 has no prerequisite beyond the subject. Do its look-up in step 1 of the skill, so that topics 3, 5 and 7 can start from what exists.

## Name the job size

| Size | Means | Examples | Default: question cap |
| --- | --- | --- | --- |
| asset | One deliverable that stands alone | An icon, one image, one chart, a social card, one email header | 6 |
| page | One page, screen or piece | A landing page, one app screen, a one-pager, a short video, an infographic | 15 |
| product | A set of screens or pages that work together | A site, an app, a dashboard suite, a design system, a slide template | 30 |
| brand | An identity that other work will follow | A new brand, a logo and identity system, a rebrand | 40 |

Rules:

1. When a request spans sizes, use the largest. "A logo and a landing page" is brand.
2. State the size in the plan line. The user can correct it with one word.
3. A later request of a larger size reopens the topics that the larger size requires. See `realign.md`.

## Depth table

R = required: ask until the answer is usable, or record ASSUMED. O = optional: propose from evidence and ask only when there is no evidence. S = skipped: write "not in scope for this job size".

| # | Topic | asset | page | product | brand |
| --- | --- | --- | --- | --- | --- |
| 1 | People served and context | R (user and context only) | R | R | R |
| 2 | Need and point of view | O | R | R | R |
| 3 | Feel | O | R | R | R |
| 4 | Primary job and success | R (job only) | R | R | R |
| 5 | Design persona | S (read back one that exists) | O (short form) | R (short form) | R (full form) |
| 6 | Brand, system and assets | R | R | R | R |
| 7 | Taste | O | R | R | R |
| 8 | Constraints | R | R | R | R |
| 9 | Risks and the worst case | S | O | R | R |
| 10 | Decision rights | O (who approves) | R | R | R |
| 11 | Scope and fidelity | R | R | R | R |
| 12 | Tools, spend and exposure | R | R | R | R |
| 13 | Feedback rounds | O | O | R | R |

Topics 6, 8, 11 and 12 are required at every size. Topic 12 holds the spend and exposure answers that later gates rely on.

Persona forms: the short form is fields 2, 4 (three traits) and 5. The full form is all eight fields. `design-brief` holds the form and its checks.

When the need topic is required, compare two framings and write one point of view. On an asset job, one line of need is enough.

## The quick mode

`--quick` on a project with no confirmed brief:

1. Ask the required topics only.
2. For each optional topic, write a proposal from evidence and mark it ASSUMED. Do not ask.
3. Show the summary. The ASSUMED list is the first thing the user reads after the yes question.

`--quick` on a project with a confirmed brief runs tier two. Tier two is already short.

`--quick` on a re-entry in the same session has no effect. The re-entry runs only the topics of its trigger. See `realign.md`, section 5.

## Depth signals

Go one step deeper than the table when:

- The user's answer contradicts a file. Name both and ask which governs.
- The audience includes people at risk: health, money, children, safety, legal status. Make topic 9 required.
- The work will be public under a brand that does not exist yet. Treat the job as brand size.

Go one step lighter when:

- A strict design system fixes the look. Topic 7 becomes optional; topic 5 is read back.
- The user says the brief from another project applies. Read it, then confirm only what differs.
