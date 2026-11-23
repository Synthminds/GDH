# 0005: align opens every session

Date: 2026-11-23. Status: accepted.

## Context

The first build started each design session with `ask-gdh`, a router that ran a pre-flight and asked brief questions only when they came up. The owner wants every session to begin with an alignment interview: the agent learns who the work serves, what it must do, how it should feel, what is locked and what may be spent, before it chooses any look. A returning project with a confirmed brief needs a short check, not the full interview again.

## Decision

- A new model-invoked skill, `align`, opens every GDH session. It runs before any other GDH skill and before any look is chosen.
- Tier one: without a confirmed `design/brief.md`, `align` runs the full interview. It asks one question at a time, each with a recommended answer, and scales the topics to the job size.
- Tier two: with a confirmed brief, `align` re-aligns in a few questions and escalates to tier-one topics only when a trigger fires.
- `--full` forces tier one. `--quick` asks the required topics only.
- The user may end the interview at any time. Each open required field is then recorded as ASSUMED.
- `design-brief` gives up its interview. It keeps the brief format, the status line, the persona form and the fidelity ladder.
- `ask-gdh` routes only after `align` closes.
- `align` runs its own question loop by default. It hands the loop to `gch:grilling` only when that skill's description holds the words "caller contract". Then GDH owns the topics and the brief, and GCH runs the loop. Amended 2026-11-23 after review: the current grilling text asks the whole frontier at once, which contradicts the align contract.
- The rule is stated in four places that must agree: kernel rule 0, the first moment in `kit/kit.json`, the first line of the managed `AGENTS.md` block that `gdh.py export` writes, and the README files.

## Consequences

- GDH has 26 skills, six of them model-invoked. Their descriptions use about 3,500 of the 5,000 characters in the budget.
- The first turn of every GDH session is a question. The GCH offer text says so, so that the user knows before choosing GDH.
- GCH must not run a second design interview when `align` is listed. The contract is in [docs/HANDOFF-GCH.md](../HANDOFF-GCH.md), sections 2.6 and 2.7.
- Discipline skills that say "No brief: run design-brief first" still work, because `design-brief` sends the user to `align`.
- The interview has not been run with a real user. Its question caps are defaults.

## Alternatives considered

- Keep the interview inside `design-brief`: rejected, because the brief skill then both owns a file format and runs a session ritual, and the router could skip it.
- Ask brief questions only when a skill needs them: rejected, because the agent then chooses a look before it knows the audience.
