---
name: design-principles
description: "Selects the design principles that apply to a task from the GDH principles canon, by discipline and stage, and lists each as a gate or a default with its source. Use at the start of a direction, before a build, or when a review needs the rule behind a finding."
disable-model-invocation: true
---

# design-principles

This skill picks the principles from the GDH canon that govern one task, and says how to use them. The canon holds the load-bearing rules of twelve design books, each with a test and a source. The skill runs a query script by discipline and stage, turns the gates into checks, and passes the defaults on as guidance. The calling skill then cites principle ids in its direction files and reviews. This skill designs nothing and judges no work. `design-critique` and `originality-gate` judge; `concept-forge` and `mood-board` make directions.

## Before you start

- Input: the task, its discipline and its stage. A calling skill usually supplies all three.
- Read: `DESIGN.md`, `design/brief.md` and `design/decisions.md` when they exist.
- Precedence: the user, then the project design system, then the brief, then the kernel, then this canon. A principle never overrides a choice the user or the design system requires.
- Disciplines are the keys of `disciplines` in [capabilities.json](../../catalogs/capabilities.json). Stages are `brief`, `explore`, `refine` and `finalize`.

## Procedure

`PRIN` means `python3 <skill folder>/scripts/principles.py`. In Claude Code the skill folder is `${CLAUDE_SKILL_DIR}`.

1. Run `PRIN --validate`. Exit 0 means the canon is sound. On exit 1 or 2, report the findings and work from the kernel alone.
2. Name the discipline and the stage. Take them from the calling skill or the brief. ASK: when either is unclear.
3. Map a task with no discipline key. Brief work, refinement rounds and handoffs have none. Leave out `--discipline` and filter by tag: `process` for briefs, `collaboration` for rounds, `handoff` for handoffs, `accessibility` for an accessibility pass.
4. Pull the gates: `PRIN --discipline <d> --stage <s> --check gate`. Each gate is a check for this stage.
5. Pull the discipline defaults: `PRIN --discipline <d> --stage <s> --check default --specific`. These name the discipline directly.
6. Add the cross-discipline defaults by tag. Use `--tag originality` at explore and `--tag emotion` for brand, website and app work. Use `--tag data` for charts, dashboards and networks, and `--tag motion` for motion work.
7. Read `--full`, or the book list, for any principle whose rule alone does not say how to apply it.
8. Run the precedence pass. List each principle that a user or design-system choice overrides. Mark it `yields`, with the choice that wins. A yielded principle is never a finding.
9. Apply the gates as checks. Mark each one pass, fail or not applicable, with a reason. A failed gate blocks the stage like any kernel gate.
10. Apply the defaults as guidance. Choose the ones that change what gets made. Name what each changes.
11. Write the principles block (see Output) and hand it to the calling skill.
12. Cite ids where the work is recorded. A direction or concept file names the principles it applies. A review finding names its criterion as a principle id when one fits.
13. When no principle covers a decision, write "not covered". Never invent an id. Propose a new principle in the project retrospective; the canon changes only by an edit with a book source.

Example for a website direction: `PRIN --discipline website --stage explore --check gate`, then `PRIN --discipline website --stage explore --specific --check default`, then `PRIN --stage explore --tag originality`.

Filters combine with AND. A comma list or a repeated flag matches any of its values. `--id P-EMO` lists one book. `--json` prints one object for a script or a subagent.

## Tools

Capabilities: none. This skill reads local files and calls no connector.

- Query and validation: [scripts/principles.py](scripts/principles.py). Python 3.9 or later, standard library only. Exit 0: pass. Exit 1: validation findings. Exit 2: a usage or input error.
- Data: [kit/canon/principles.json](../../canon/principles.json). Use `--canon` and `--capabilities` to point at other copies.

GATE: this skill makes no spend call and exposes nothing.

## Checks

Gates:

- `PRIN --validate` exits 0 before any principle is used.
- Every gate returned for the discipline and stage has a mark: pass, fail or not applicable, with a reason.
- Every cited id exists in the canon. Confirm with `PRIN --id <id>`.
- No principle is applied against a user or design-system choice. Each override is marked `yields`.
- A number in a default principle is a starting value only. It is never reported as a gate failure.

Defaults:

- Default: hand on at most twelve defaults in the block, the ones that most change the work. List the rest by id only.
- Default: at explore, include at least two principles tagged originality.
- Default: when the canon and a discipline skill give different numbers, the discipline skill's number holds, and the canon principle is cited for the reason only.

## Output

The skill writes no project file. It returns this block, which the calling skill copies into its direction file, concept file or review:

```
Principles: <discipline | tag>, stage <stage>, canon <n> checked, validate <pass | fail>
Gates: <id> <pass | fail | n/a: reason> x n
Defaults applied: <id>: <what it changes in this work> x up to 12
Also in scope: <ids>
Yields: <id>: <the user or design-system choice that wins>
Not covered: <decision with no principle>
```

Closing report in the chat: the counts of gates and defaults, any failed gate, and the next skill.

## References

- [scripts/principles.py](scripts/principles.py): read before step 1. Run it with `--help` for every flag.
- [kit/canon/principles.json](../../canon/principles.json): the canon. Each principle has rule, why, apply, test, check, scope and source.
- Book lists, one per book, matching the canon word for word: [design systems](../../canon/principles/design-systems-handbook.md), [design engineering](../../canon/principles/design-engineering-handbook.md), [animation](../../canon/principles/animation-handbook.md), [collaboration](../../canon/principles/collaboration-handbook.md), [product design](../../canon/principles/principles-of-product-design.md), [leadership](../../canon/principles/design-leadership-handbook.md), [DesignOps](../../canon/principles/designops-handbook.md), [design thinking](../../canon/principles/design-thinking-handbook.md), [emotion](../../canon/principles/designing-for-emotion.md), [Gephi](../../canon/principles/mastering-gephi.md), [AI app](../../canon/principles/ai-app-5-steps.md), [MCP mapping](../../canon/principles/mapping-to-mcps.md). Read one at step 7 when a principle needs its neighbors for context.
- `docs/PRINCIPLES-COVERAGE.md` in the GDH repository (not shipped in the plugin): which chapter of each book yields which ids, and why a chapter was not used. Read it before proposing a new principle.

## Sources

- Design Systems Handbook; Design Engineering Handbook; Animation Handbook; Principles of Product Design; Design Leadership Handbook; DesignOps Handbook (InVision DesignBetter).
- Design Collaboration Handbook; Design Thinking Handbook (Design Better).
- Designing for Emotion, second edition (A Book Apart).
- Mastering Gephi Network Visualization (Packt).
- Build an AI app in 5 steps (Redis whitepaper).
- Mapping to MCPs in Claude Cowork and Claude Code (field guide).
- Chapter detail for each source is in the coverage audit. Every principle is written in the kit's own words.
