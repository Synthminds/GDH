---
name: design-brief
description: Owns the GDH brief, with the format of design/brief.md, the design persona form and the fidelity ladder. Writes the brief from the answers that align collects. Runs the persona and quality checks, and sets the status line on the user's yes. Amends a confirmed brief when a field changes. Use when a confirmed brief must change, or when another skill must read or check the brief. align calls it when its interview closes. It runs no interview itself.
---

# design-brief

This skill is the home of the brief. It turns an answer record into `design/brief.md`, checks it, and keeps it current. It produces words only. It chooses no color, typeface or layout.

Boundary. `align` runs the interview and calls this skill to write the file. `mood-board` turns the brief into directions. `design-system` turns a chosen direction into tokens. A skill that needs a fact the brief lacks sends the topic back to `align`. This skill does not ask interview questions.

## Before you start

- Input: the answer record from `align`, or one changed field from the user or another skill.
- No record and no confirmed brief: start `align` and stop. It runs first in every session.
- Read: `design/brief.md`, `DESIGN.md`, `design/decisions.md`, and the template at [templates/project/design/brief.md](../../templates/project/design/brief.md).
- Precedence: the user, then the design system, then the brief, then GDH defaults.
- A brief records what the user decided. It never overrides the user or the design system.

## Procedure

Write mode, called by `align`:

1. Copy the template when `design/brief.md` is absent. Never overwrite a filled brief; amend it.
2. Fill each section from the answer record. The field rules are in [references/brief-format.md](references/brief-format.md).
3. Mark each line the user has not yet confirmed `(proposed)`. Mark each skipped line `ASSUMED`, and list it in section 15.
4. Fill section 6 with the persona form in [references/design-persona.md](references/design-persona.md). Use the form size that `align` names: short, full, or read back.
5. Run the persona checks and the contrast test in the same file.
6. Run the five quality tests in [references/brief-quality.md](references/brief-quality.md). Fix each failure, or send the topic back to `align`.
7. Set the start and stop rungs with [references/fidelity-ladder.md](references/fidelity-ladder.md).
8. Write the file with `Status: draft` and front matter `status: draft`. Return the draft and the test results to `align`.
9. On the user's yes, relayed by `align`: remove every `(proposed)` mark. Set `Status: confirmed YYYY-MM-DD by <who>` and front matter `status: confirmed`. Keep every ASSUMED mark. When the user ended the interview early, the end counts as the yes: add the suffix `, ended early`.

Amend mode, when a confirmed field changes:

10. Change only the named sections. Set `Status: draft` while the change waits.
11. Run the checks that touch those sections.
12. ASK: show the changed lines only. Ask "Is this right?"
13. On yes, set a new status line with today's date. Ask `align` or the calling skill to log the change in `design/decisions.md`.

Read mode, for another skill:

14. Report the status line, the job size, the sections that answer the caller's question, and the ASSUMED lines that touch it.

## Tools

The brief needs no tool. It writes two local files.

GATE: write nothing outside the project. Upload no brief to a connector without a yes.

## Checks

Gates:

- No visual work starts unless the status line starts `Status: confirmed YYYY-MM-DD by <who>`, with or without `, ended early`.
- Each section the depth table of `align` marked required holds an answer or an ASSUMED line.
- Section 2 names one person with two details, and a "not for" line. No line reads "everyone".
- Each brand word and each persona trait carries its "but not" limit.
- When section 3 is required: two framings, the chosen one with a reason, and a point of view with user, need and insight.
- Section 5 holds one "do" and one "feel" measure. No baseline number is invented.
- Section 8 holds three or more "this, not that" lines.
- Section 11 names one decider for each aspect in scope.
- Section 13 holds the paid generation line and the exposure line. "none" is valid.
- No `(proposed)` mark remains after confirmation.
- No fact about the user's company, market or users is invented. A guess is ASSUMED in section 15.

Defaults. The user, the design system or the brief can replace each one.

- Default: the full persona form for brand size, the short form for product and page size, a read back for asset size.
- Default: accessibility level WCAG 2.2 AA when the user states none.
- Default: paid generation "none" when the line is ASSUMED.
- Default: start at the lowest rung with open questions. No paid generation below the direction rung.

## Output

Files:

- `design/brief.md`, from the template, with the status line set.
- No decision entry. `align` writes the alignment entry. A calling skill logs an amendment.

Report to the caller:

```
Brief: <status line> (size: <asset|page|product|brand>, mode: <explore|refine>)
One line: <subject> for <user>, so they can <primary job>
Persona: <form>; checks <passed n of n>
Quality tests: swap <pass|fail>; deniability <pass|fail>; point of view <pass|fail|skipped>; measure <pass|fail>; evidence <pass|fail>
Ladder: start <rung>, stop <rung>
ASSUMED: <n>; open questions: <n>
```

## References

- [references/brief-format.md](references/brief-format.md): read at step 2. The status line, the marks, and the rule for each section.
- [references/design-persona.md](references/design-persona.md): read at step 4. The eight-field form, its checks, the contrast and dose tests, a worked example.
- [references/brief-quality.md](references/brief-quality.md): read at step 6. The five tests, a worked brief and failure patterns.
- [references/fidelity-ladder.md](references/fidelity-ladder.md): read at step 7. The six rungs, the rules to climb, and how to recommend a start rung.

## Sources

- Aarron Walter, Designing for Emotion, 2nd ed., ch. 3: the design persona.
- Design Collaboration Handbook (DesignBetter), ch. 4, 5 and 7: written kickoff, point of view, worst case.
- Design Thinking Handbook (DesignBetter), ch. 3 and 5: point of view, reframing, fidelity.
- DesignOps Handbook (DesignBetter), ch. 2 and 5: intake, ranking, stakeholders.
- Principles of Product Design (DesignBetter), ch. 1 and 3: evidence list, low fidelity first.
- Anthropic frontend-design skill, "Before coding": subject, audience, primary job.
