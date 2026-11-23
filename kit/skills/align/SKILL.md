---
name: align
description: Opens every GDH session with an alignment interview, before any other GDH skill and before any look is chosen. With no confirmed design/brief.md it runs the full interview. It asks one question at a time with a recommended answer, scaled to the job size. It covers thirteen topics, from people, need and feel to decision rights, scope, spend and feedback rounds. With a confirmed brief it re-aligns in three questions. Use at the first design-led request of a session. Later in a session, use it when the audience, job or brand changes.
argument-hint: "[--full | --quick]"
---

# align

This skill opens a GDH session. It aligns the agent with the user before any other GDH skill runs. Tier one is the full interview for a project with no confirmed brief. Tier two re-aligns a confirmed brief. It designs nothing.

Boundary. `design-brief` owns the brief format, the persona form and the fidelity ladder, and writes `design/brief.md`. `ask-gdh` plans and routes the work after this skill closes. `refine-round` runs feedback on a design.

## Before you start

- Input: the first design-led request of the session, in the user's words, and any argument. `--full` or the words "full interview" force tier one. `--quick` runs the required topics only.
- Read before you ask: `design/brief.md`, the last three entries of `design/decisions.md`, the design system, and every source in the look-up table of [references/interview-loop.md](references/interview-loop.md).
- Precedence: the user, then the design system, then the brief, then GDH defaults.
- A session runs the full skill once. It is done when its closing report is in the conversation.
- Re-entry: align starts again in a session that holds its closing report. It runs only the topics of the named trigger ([references/realign.md](references/realign.md), section 3), then closes. It ignores `--full` and `--quick`.
- The user may end the interview at any time. It is never skipped entirely.

## Procedure

1. Read the project. Make no spend call and no write. List each fact you found with its file.
2. Choose the tier. Tier one: the brief is absent or not confirmed, or the user asked for the full interview. Tier two: any other case.
   A brief is confirmed when its status line starts `Status: confirmed YYYY-MM-DD by <who>`, with or without `, ended early`.
3. Name the job size: asset, page, product or brand. Read the depth table in [references/topics.md](references/topics.md). It marks each topic required, optional or skipped.
4. Tell the user the tier, the job size and the topic count, and that "skip" or "you decide" always works.
5. Pick the loop. Default: run the loop in [references/interview-loop.md](references/interview-loop.md) yourself. Hand the interview to `gch:grilling` only when its description in this session's skill list contains the words "caller contract". See section 6 of that file.

Tier one, the full interview:

6. ASK: walk the topics in the order of `topics.md`. Questions, tags and probes are in [references/question-bank.md](references/question-bank.md).
7. Ask one question at a time, or use the host question tool with two to four options.
8. Open each question with what you found, as a proposal. Give a recommended answer and its reason.
9. Ask a question only when its prerequisites are settled. Restate each answer in one line before you move on.
10. Probe a weak answer with the follow-up in the bank. Never accept "everyone" as an audience. Never accept an adjective without its "but not" limit.
11. On "skip" or "you decide", record your proposal as ASSUMED and move on.
12. When the user ends the interview, mark every open required field ASSUMED. Go to step 13.
13. Hand the answer record to `design-brief`. It writes `design/brief.md` with `Status: draft` and runs its persona and quality checks.
14. ASK: read back the one-screen summary in Output. Ask: "Is this right? Yes, or tell me what to change." Edit until the user says yes.
15. On yes, `design-brief` sets `Status: confirmed YYYY-MM-DD by <who>`. Write the alignment entry in `design/decisions.md`.
16. STOP: no design work, no look and no spend call before the yes. An ended interview counts as the yes. The status line then reads `Status: confirmed YYYY-MM-DD by <who>, ended early`.

Tier two, re-alignment:

17. Read the brief and the last three decision entries. State in three lines where the project stands.
18. ASK: three questions at most, one at a time. What changed since the last session? What is today's goal, and what does done look like? What is locked, and what is open for feedback today?
19. Escalate to the affected topics of tier one when a trigger in [references/realign.md](references/realign.md) fires.
20. A changed brief goes back through steps 13 to 15 for the changed sections only.
21. Write the re-alignment entry in `design/decisions.md`.

Close:

22. Print the closing report. Start `ask-gdh` with the request and the report.

## Tools

The interview needs no tool. These capabilities help you read before you ask, read-only.

- `capture` or `reverse-engineer`: view a site or reference the user names. Example card: [rea](../../references/tools/rea.md).
- `asset-library` or `brand-kit`: read a connected brand source. Example card: [dam](../../references/tools/dam.md).
- `design-system`: read a hosted design system. Example card: [claude-design-system](../../references/tools/claude-design-system.md).

Pick the tool by kernel rule 8. Read its card before the first call. Vocabulary: [capabilities.json](../../catalogs/capabilities.json).

A list call shows account content. Make it only in the user's own account. GATE: do not upload a user's file or screenshot to a connector without a yes.

## Checks

Gates:

- The closing report of this skill is in the conversation before `ask-gdh` routes or another GDH skill starts.
- Tier one: every topic the depth table marks required has an answer or an ASSUMED line.
- The audience names one person with two specific details and a "not for" group. "Everyone" fails.
- Each brand word and each persona trait carries its "but not" limit.
- When the need topic is required: two framings are compared and one point of view holds user, need and insight.
- The spend budget and the exposure line are answered. "none" is a valid answer. Neither is a yes to any call.
- One decider is named for each aspect in scope.
- The user said yes to the summary, or ended the interview, before any design work.
- No fact about the company, market or users is invented. A guess is ASSUMED.
- An alignment or re-alignment entry exists in `design/decisions.md`.

Defaults. The user, the design system or the brief can replace each one.

- Default: question caps by job size: asset 6, page 15, product 30, brand 40. Stop sooner when required fields are filled.
- Default: a brief older than 90 days triggers escalation in tier two.
- Default: accessibility level WCAG 2.2 AA when the user states none.
- Default: paid generation "none" when the user skips the budget question.

## Output

Files: `design/brief.md`, written by `design-brief`. One entry in `design/decisions.md`, written by this skill.

The one-screen summary for step 14:

```
Alignment summary: tier one, <job size>
Who: <user with two details>; not for: <group>
Need: <point of view in one line>
Feel: <target feeling>, not <feeling to avoid>
Job: <primary job>. Success: do <measure>; feel <measure>
Persona: <three traits with their limits>
Constraints: <accessibility level>; <stack>; <deadline>; <legal>
Out of scope: <list>
Decider: <who, for which aspect>
Budget: paid generation <none | ask each time | ceiling>; exposure <what may leave>
Feedback: <who reacts, how often, what each round asks>
ASSUMED: <n>: <list>
```

The alignment entry format is in [references/interview-loop.md](references/interview-loop.md). The re-alignment entry format is in [references/realign.md](references/realign.md).

Closing report:

```
GDH aligned: tier <one | two>, <job size>, <YYYY-MM-DD>
Brief: <status line>; ASSUMED <n>; escalated topics <list or none>
Today: <goal>; done when <test>
Locked: <list>. Open for feedback: <list>
Next: ask-gdh
```

## References

- [references/interview-loop.md](references/interview-loop.md): read at steps 1, 5 and 15. The look-up table, the loop rules, the ended-early status line, the answer record, the `gch:grilling` caller contract, the alignment entry, and failure patterns.
- [references/topics.md](references/topics.md): read at step 3. The topic tree, the depth table and `--quick`.
- [references/question-bank.md](references/question-bank.md): read at step 6. Questions with recommended answers, probes and source tags.
- [references/realign.md](references/realign.md): read at step 17 and on a re-entry. Tier two, the escalation triggers, the re-alignment entry and re-entry in a session.

## Sources

- Design Thinking Handbook (DesignBetter), ch. 2 to 6: point of view, reframing, client questions, fidelity, tests.
- Aarron Walter, Designing for Emotion, 2nd ed., ch. 3: the design persona.
- Design Collaboration Handbook (DesignBetter), ch. 3, 4, 5 and 7: written kickoff, worst case, do and feel measures.
- DesignOps Handbook (DesignBetter), ch. 2 and 5: intake, strict ranking, a decider for each aspect.
- Design Leadership Handbook (DesignBetter), ch. 2 and 3: mode, scope, working with the user.
- Principles of Product Design (DesignBetter), ch. 1: evidence before design.
- GCH `grilling` skill: an interview that walks a decision tree with recommended answers.
