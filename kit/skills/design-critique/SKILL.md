---
name: design-critique
description: Reviews design work against the brief, the design system, the checks of its discipline and the dated tell list. Restates goal and constraints, and looks before it judges. Reports findings by severity, with a screenshot region or a selector as evidence. Writes each finding as observation, impact and suggestion. Scores the work with a rubric. Runs a heuristic tell scan on HTML, CSS, JSX, TSX and Tailwind classes. Use before work is called done, or when the user asks for a review, critique, audit or second opinion. Also use when output looks generic or templated, or to compare options. It judges only. It never redesigns; changes go through refine-round.
---

# design-critique

This skill judges a design and writes a review. It critiques the work, not the maker. It changes no design file and proposes no redesign. `refine-round` applies the changes the user picks. `accessibility-gate` runs the full accessibility checks for the medium.

## Before you start

- Input: the work to review, and the decision the review must support.
- Read: `design/brief.md`, `DESIGN.md`, `design/tokens.json`, `design/decisions.md`. Read the latest file in `design/reviews/` when one exists.
- Precedence: the user, then the design system, then the brief, then GDH defaults. The tell scan is a GDH default.
- A choice that the user or the design system requires is `brand-required`. It is never a finding and it lowers no score.
- With no confirmed brief, say so. Review against the stated request only, and label the review "no brief".

## Procedure

`TELLS` means `python3 <skill folder>/scripts/tells.py`. In Claude Code the skill folder is `${CLAUDE_SKILL_DIR}`.

1. Name the stage: explore, refine or finalize. Name the decision needed. ASK: when either is unclear.
2. Set one to four review questions. Take them from the user, or propose them.
3. Restate the goal and the constraints in three lines: user goal, business goal, constraints.
4. Get the work in its running medium. For code, capture the render at each breakpoint and theme. For an artifact type, follow the type's own check rule.
5. Look in silence. Write what a first-time viewer sees first, second and third. Judge nothing yet.
6. Check brief coverage. Mark each requirement met, partly met or missing.
7. Run the precedence pass. List each choice the user or the design system requires.
8. Run the tell scan from the project root: `TELLS <paths> --tokens design/tokens.json --design DESIGN.md`. Drop `--tokens` or `--design` when that file does not exist. Then read [references/tells.md](references/tells.md) for the tells that no script can see.
9. Run the checks of the discipline. The owning skill holds them. Cite the check for each finding.
10. Check the gates listed under Checks.
11. Write each finding as observation, impact and suggestion, with evidence and severity. The format is in [references/critique-format.md](references/critique-format.md).
12. Name what works. A review with no "working well" list is not finished.
13. Score with [references/rubric.md](references/rubric.md). State the verdict band.
14. Write `design/reviews/<date>-<scope>.md`. Report the top findings in the chat.
15. ASK: "Which findings do you want changed?" Hand the chosen ones to `refine-round`.

Match the review to the stage. Explore: judge the idea and its fit to the brief. Refine: judge only the parts in scope. Finalize: judge defects only.

Independence: the maker should not grade its own work alone. When the host supports subagents, give this review to the `design-critic` agent. Otherwise start with a fresh read of the brief, and label the review "single-context".

## Tools

Capabilities, in preference order: `critique`, `capture`. Vocabulary: [capabilities.json](../../catalogs/capabilities.json).

- Tell scan: [scripts/tells.py](scripts/tells.py). It needs no tool and no network. Exit 0: clean. Exit 1: findings at or above `--fail-on`. Exit 2: a usage or input error, or no file was scanned. Exit 2 never means clean: fix the path and run it again. A skipped file is listed in the output; read the list and check each skipped file by eye.
- Render capture: any tool of the `capture` capability. Example card: [headless-browser](../../references/tools/headless-browser.md) for local full-page captures at each width and theme. With GCH installed, use `gch:browser-lane`.
- A deeper scored review or a second detector, offered and never started for the user: [impeccable](../../references/tools/impeccable.md), [design-taste-frontend](../../references/tools/design-taste-frontend.md).
- Artifact review: follow the type card, for example [claude-design](../../references/tools/claude-design.md).

Pick the tool by kernel rule 8. Read its card before the first call. With no capture tool and no local browser, ask the user for screenshots and label the render checks UNTESTED.

GATE: this skill makes no spend call. A reply in a comment thread, a share link or an upload of project files is exposure. Ask first.

## Checks

Gates. A failed gate is a blocker finding, whatever the score:

- Body text contrast is 4.5:1 or more. Large text and control outlines are 3:1 or more. This holds in every theme.
- Color is never the only carrier of meaning. Every control works by keyboard with visible focus. Reduced motion is honored.
- No invented fact: no made-up logo, statistic, testimonial, client name or data. A labelled placeholder is allowed.
- Every color, size, space, radius and duration in the deliverable comes from a named token.
- Every outside asset has a license record in `design/assets/manifest.json`.
- A code deliverable was reviewed as rendered, at each breakpoint and theme. Source reading alone does not pass.
- Every finding has evidence, a severity and a criterion. No finding rests on taste alone.
- No finding reports a `brand-required` choice.

Defaults. The user, the design system or the brief can replace each one.

- Default: report seven findings at most in the chat, worst first. Put the rest in the review file.
- Default: four review questions at most.
- Default: two or three viewer passes from the rubric, chosen by the audience in the brief.
- Default: `tells.py` flags more than 8 literal font sizes and more than 12 literal colors outside tokens.
- Default: the tell list is reviewed every 90 days. Its version is the date in `tells.py --list`.

A scan that skipped a file or read zero files is not a pass. Name each skipped file, and check it by eye.

The tell scan is a heuristic. It reads source text and renders nothing. A clean scan does not prove distinctive work. A finding from the scan is a lead to check, not a verdict.

## Output

File: `design/reviews/<YYYY-MM-DD>-<scope>.md`, from the template in [references/critique-format.md](references/critique-format.md). The skill writes no other file. A review is not a round, so it adds no entry to `design/decisions.md`. `refine-round` logs the decision.

Closing report:

```
Review: <scope>, stage <explore | refine | finalize>, <independent | single-context>
Goal: <user goal>; decision needed: <decision>
First look: <1st>, <2nd>, <3rd>
Brief coverage: <met>/<total>; missing: <list>
Gates: <pass | failed: list>
Tell scan: list <version>; <n> files, <n> skipped; <n> high, <n> medium, <n> low; brand-required <n>; heuristic only
Score: <total>/20 (<five scores>); verdict: <band>
Top findings: <severity, title, evidence> x up to 7
Working well: <list>
Evidence: VERIFIED <what was rendered or run>; UNTESTED <what was not>
Next: refine-round on <chosen findings> | accessibility-gate | mood-board | design-brief
```

## References

- [references/critique-format.md](references/critique-format.md): read at step 11. Finding format, severity scale, evidence rules, wording rules, the review file template, a worked review.
- [references/rubric.md](references/rubric.md): read at step 13. Five scored dimensions, band descriptors, viewer passes, verdict bands.
- [references/tells.md](references/tells.md): read at step 8. Each tell, why it reads as generic, the counter-move, and the tells the script cannot see.
- [scripts/tells.py](scripts/tells.py): the scan. `--list` prints the rules. `--json` prints one object.

## Sources

- Principles of Product Design (DesignBetter), ch. 4: frame the problem, silent look, feedback not solutions, critique the work.
- Design Leadership Handbook (DesignBetter), ch. 4: fidelity matched to feedback, review in the running medium.
- Anthropic frontend-design skill: the list of default looks; the brief wins.
- Impeccable (Paul Bakaus): README, craft floor and critique rubric, as read on 2026-11-23. Ideas only; no text is copied.
- Vercel Web Interface Guidelines: the engineering quality floor.
- Liz Lerman, Critical Response Process: observation before opinion.
