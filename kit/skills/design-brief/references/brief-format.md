# Brief format

This file sets the rules for each part of `design/brief.md`. The template lives at `kit/templates/project/design/brief.md`. `align` collects the answers in the same section order.

## The status line

The first line under the title is the status line. It is the authority on the state of the brief.

| Status line | Means | Other skills may |
| --- | --- | --- |
| `Status: template` | No brief exists | Treat the file as absent. Start `align` |
| `Status: draft` | Written, waiting for the user's yes | Read it. Start no visual work |
| `Status: confirmed YYYY-MM-DD by <who>` | The user said yes on that date | Rely on it |
| `Status: confirmed YYYY-MM-DD by <who>, ended early` | The user ended the interview; ASSUMED lines stand | Rely on it. Read section 15 first |

Rules:

1. `<who>` is the person who said yes, by role or by the name they gave. Write no email address.
2. The front matter `status` repeats the first word: `template`, `draft` or `confirmed`. When the two disagree, the status line wins and the brief counts as draft.
3. Any change to a confirmed section sets `Status: draft` until the user confirms the change.
4. The date in the status line starts the age count that `align` uses for re-alignment.

## Front matter

| Field | Values | Set by |
| --- | --- | --- |
| `status` | `template`, `draft`, `confirmed` | This skill, with the status line |
| `project` | The project name | This skill |
| `updated` | The date of the last write | This skill |
| `size` | `asset`, `page`, `product`, `brand` | `align`, from the job size |
| `mode` | `explore`, `refine` | `align`, from question 11.3 |

## The marks

| Mark | Means | After the yes |
| --- | --- | --- |
| `(proposed)` | The agent wrote it and the user has not answered | Removed. A line still unanswered becomes ASSUMED |
| `ASSUMED` | The user skipped it or said "you decide" | Kept, and listed in section 15 |
| `file:<path>` | A file holds it and the user confirmed it | Kept as the source |
| `observed`, `reported`, `assumed` | The evidence behind a claim about the people served | Kept |

## Section rules

| # | Section | Holds | Fails when |
| --- | --- | --- | --- |
| 1 | Subject | What it is and what it is not, one sentence each | No "is not" line |
| 2 | People and context | One user with two details, also touched by, not for, context, evidence tags | "Everyone", a demographic, or no "not for" |
| 3 | Need and point of view | Need as a verb phrase, two framings, the chosen one and why, the point of view | A product noun in the need; one framing only |
| 4 | Feel | Target feeling, must-not feeling, delight, sensory line | Only "satisfied" or "happy"; layout words |
| 5 | Primary job and success | One job, ranked others, do and feel measures, story, owner need | Two first jobs; an invented baseline |
| 6 | Design persona | The form in `design-persona.md`, at the size `align` named | A trait with no limit; no real strings on the full form |
| 7 | Brand, system and assets | Inventory with fixed or flexible, the broken promise, real content, history | A fixed item with no source |
| 8 | References and taste | References with the exact part, brand words with limits, competitors, this-not-that lines | A reference with no part; fewer than three trade-offs |
| 9 | Constraints | Legal, accessibility level, stack, content, deadline, cannot, will not | No accessibility level |
| 10 | Risks and the worst case | Worst case with group and response, misuse, misreadings, riskiest assumption | "Nothing bad" |
| 11 | Decision rights | One decider for each aspect, approvers and when, delegated choices, disputes | Two deciders for one aspect |
| 12 | Scope and fidelity | Ranked deliverables, not in this round, mode, first question, rungs, format | Ties at the top; no "not in this round" |
| 13 | Tools, spend and exposure | Paid generation line, exposure line, files never uploaded, tools | Either of the first two lines empty |
| 14 | Feedback plan | Who reacts, round questions, cadence, reframe trigger, working style | Empty on product or brand size |
| 15 | Assumptions and open questions | Every ASSUMED line, the hypothesis, open questions | A guess elsewhere with no mark |

A section that the depth table skipped for this job size reads "Not in scope for this job size." That line passes.

## What the brief never holds

- A hex value, a font file, a layout, a component count or a hero description. Those belong to a direction.
- A price, a credit amount or a model id. Tools read those live.
- An email address, an account id or a private link. The repository may be public.
- A statistic with no source. Write "baseline unknown".
