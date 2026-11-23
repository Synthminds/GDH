# 0004: Evidence labels, and gates versus defaults

Date: 2026-11-23. Status: accepted.

## Context

The research behind GDH is uneven. Some rules were read from a primary source. Many numbers were stated from memory or from secondary pages. No tool was exercised with a spend call, and no design was built. A harness that presents all of this with one confident voice would block work on numbers nobody verified, and would claim tool behavior nobody saw.

## Decision

### Three labels

| Label | Meaning |
| --- | --- |
| VERIFIED | Someone exercised it and saw the result. The note says what and when. |
| DOCUMENTED | A primary source states it. Nobody exercised it here. |
| UNTESTED | It comes from memory, a secondary page or a rule of thumb. |

Every tool entry, every tool card and every closing report of a skill carries a label. A label rises only after a real call or a real render.

### Two kinds of rule

- A gate blocks delivery. A gate carries a number only when that number is verified, or is the published accessibility floor, which is labelled DOCUMENTED. Most gates have no number: a brief exists, a direction was chosen, a license was read, a quote was shown, a record was written.
- A default is a starting value. It is written with "Default:" in front. The user, the design system or the brief can replace it.

A research fact that is marked unverified, from memory or as a rule of thumb is always written as a default.

### Precedence comes first

The user ranks first, then the project design system, then the brief, then GDH defaults and the tell scan. A choice that the user or the design system requires is reported as brand-required and never as a tell. Gates stay in force at every rank: a required palette that fails the contrast floor is still a failure.

## Consequences

- A skill cannot fail a design on a rule-of-thumb number. It notes the default and continues.
- Reports are longer, because they say what was not proven.
- The kernel holds no number that differs by medium, no tool name, no model id and no price.
- The contrast ratios are the one numeric gate. They are the published values, and the kit says plainly that the standard was not opened during the build.
- Work remains: read the primary sources, exercise the tools, and raise labels. The open-work list in `docs/GDH.md` tracks it.

## Alternatives considered

- Treat all research numbers as gates: rejected. It would enforce unverified values and conflict with real brand systems.
- Drop unverified numbers: rejected. A labelled default is more useful than silence.
