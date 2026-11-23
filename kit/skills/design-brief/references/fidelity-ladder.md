# Fidelity ladder

The ladder says how finished each step is. Lower rungs cost less to change. Start low. Climb for a reason. The brief records the start rung and the stop rung in section 12.

## The rungs

| Rung | Name | What exists | Feedback to ask for | Not yet |
| --- | --- | --- | --- | --- |
| 0 | Words | The brief, a content outline, a flow list | Is this the right problem and the right content? | Any visual |
| 1 | Grey box | Wireframes or thumbnails in grey, real copy | Is the structure and the order right? | Color, final type, imagery |
| 2 | Direction | Boards or styleframes that differ in idea, same parts on each | Which idea fits? Keep, change, remove for each part | Full screens |
| 3 | One real screen | The chosen direction on the hardest real screen | Does the direction survive real content? | Other screens |
| 4 | Prototype | The key flow, interactive, with real states | Can a first-time user finish the job? | Edge screens, final assets |
| 5 | Build | All screens, all states, production assets | Defects only | New ideas |

## Rules

1. The brief records the start rung and the stop rung.
2. Start at the lowest rung that still has open questions. A project with a confirmed brief and a strict design system can start at rung 3.
3. Climb one rung at a time. Record the reason in `design/decisions.md`: which questions this rung answered, and that the user said go.
4. Ask only for the feedback type of the current rung. Mark rung 0 to 2 work as draft, so reviewers judge the idea and not the finish.
5. A new idea at rung 5 is a new round at a lower rung. Do not patch it in.
6. Default: no paid generation below rung 2. At rung 2 and above, the spend gate applies to each call.
7. Each rung answers the first question in section 12, or a new question the user states. A rung with no question is skipped.

Map to the decision record: rungs 0 to 2 are stage explore, rungs 3 and 4 are stage refine, rung 5 is stage finalize.

## How to recommend a start rung

| Situation | Recommend |
| --- | --- |
| The problem or the content is unclear | Rung 0 |
| The content is known, the structure is not | Rung 1 |
| Structure is known, no look exists | Rung 2 |
| A strict design system exists | Rung 3 |
| A refine job on built screens | Rung 5 scope, with one round at rung 3 for the changed area |
| An asset job with a fixed format | Rung 2, with two or three options |

## How to recommend a stop rung

| The engagement ends with | Stop rung |
| --- | --- |
| A chosen look for another team to build | 2 |
| A tested direction on the hardest screen | 3 |
| A flow that real users tried | 4 |
| Shipped files or code | 5 |

## Failure patterns

| Pattern | Sign | Correction |
| --- | --- | --- |
| Polish first | A finished hero exists before the structure is agreed | Drop to rung 1. Agree the order |
| Rung jump | Rung 0 to rung 4 in one step | Climb one rung at a time, with a recorded reason |
| Wrong feedback | Color comments on a grey box | Restate the rung's question |
| Late idea | A new concept appears at rung 5 | Open a new round at rung 2 |

## Sources

- Design Thinking Handbook (DesignBetter), ch. 5: fidelity follows the question.
- Principles of Product Design (DesignBetter), ch. 3: low fidelity first.
