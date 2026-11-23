# Re-alignment

Tier two runs when the brief is confirmed and the user did not ask for the full interview. A brief is confirmed when its status line starts `Status: confirmed YYYY-MM-DD by <who>`, with or without `, ended early`. It costs three questions at most. It escalates to the full interview only for the topics an answer touches.

## 1. State where the project stands

Read the brief and the last three entries of `design/decisions.md`. Then write three lines:

```
Brief: <subject> for <user>, so they can <primary job>. Confirmed <date> by <who>.
Last round: <date>, <scope>, <stage>: <decision>.
Open: <open questions from the last entry, or none>.
```

When the decision record is empty, say "Last round: none".

## 2. The three questions

Ask one at a time. Each carries a recommended answer built from the record.

**R1. What changed since the last session?** [Derived]
- Rec: "Nothing in the brief changed", when no file changed since the last entry.
- Listen for: a new audience, a new job, a new brand rule, a new decider, a new deadline, new feedback from users.

**R2. What is today's goal, and what does done look like?** [Adapted, DC ch. 5; DT ch. 6]
- Rec: the next step after the last entry, with one observable end state.
- Weak: "keep going". Probe: "What will you look at tonight to know today worked?"

**R3. What is locked, and what is open for feedback today?** [Adapted, DO ch. 2; DL ch. 3]
- Rec: lock every part the decision record marks as decided. Open the parts in today's scope.
- Weak: "everything is open". Probe: "Which decided part would you hate to see change?"

Restate each answer in one line. Skip a question that the user's first message already answered.

## 3. Escalation triggers

Escalate when a trigger fires. Run only the topics in the right column, with the full interview loop. Keep every other section as confirmed.

| Trigger | Reopen topics |
| --- | --- |
| An answer contradicts the brief | The topics behind the contradicted sections |
| The audience changes | 1, 2, 3, 5, 9 |
| The primary job changes | 2, 4, 11 |
| The brand changes: new name, new owner, new rules | 5, 6, 7 |
| A new decider or approver appears | 10, 13 |
| A new legal, accessibility or stack constraint | 8, 9 |
| The spend budget or the exposure rule changes | 12 |
| The job size grows, such as a page brief now asked for a product | The topics the larger size marks required that the brief lacks |
| Default: the brief is older than 90 days | 1, 4, 8, 10, 12: read each back in one line and ask "Still true?" |
| Rounds stall: the default count of rounds passes with no base direction, from `mood-board` or `refine-round` | 3, 4, 7 |

Rules:

1. Name the trigger to the user in one line before you ask. Example: "The audience changed, so I will ask about people, need, feel, persona and risks again."
2. The user can decline an escalation. Record the trigger and the decline in the entry. Mark the affected sections in section 15 as possibly out of date.
3. The age is counted from the date in the status line.
4. A changed brief goes back to `design-brief`. It updates only the changed sections, sets `Status: draft`, and runs its checks.
5. Read back only the changed lines. On yes, `design-brief` sets a new status line with today's date.

## 4. The re-alignment entry

Write one entry in `design/decisions.md`. Number it `round 0`, as every alignment entry is. Round 0 is outside the design rounds, so it never repeats a design round number. The date tells round 0 entries apart.

```
## YYYY-MM-DD round 0: re-alignment
Stage: <stage of the last entry>
Shown: the three-line status
Feedback asked: What changed? Today's goal and done? Locked and open?
Keep / Change / Remove: locked <parts>; open <parts>; changed <brief sections, or none>
Decision: today's goal <goal>, done when <test> (by <who>)
Rejected: <declined escalation or dropped scope>: <reason>, or none
Open: <questions>
Evidence: DOCUMENTED <answers stated today>; UNTESTED <sections marked possibly out of date>
```

## 5. Re-entry in the same session

A session runs the full skill once. A later request in the same session does not restart it. Another skill can start align again with a named trigger from section 3. That is a re-entry.

1. A skill finds a trigger. Examples: `ask-gdh` finds that the brief does not cover the new request; `mood-board` or `refine-round` find that rounds stall; `infographic` or `network-graph` find a new audience.
2. It returns to align with the trigger in words, such as "return to `align` with the trigger 'the audience changes'".
3. align names the trigger to the user, runs only the topics in its row, and follows rules 2 to 5 of section 3.
4. align writes a `round 0: re-alignment` entry and prints the closing report again. Then the calling skill continues.

A re-entry ignores `--full` and `--quick`. It never runs tier one or the three questions of section 2 again. With no named trigger, ask the caller for one. When none fits, ask the user R1 only.

## 6. Failure patterns

| Pattern | Sign | Correction |
| --- | --- | --- |
| Restart | A confirmed brief exists and the agent runs the full interview unasked | Run tier two. Escalate only on a trigger |
| Silent drift | The audience changed in the user's words and the brief still names the old one | Fire the trigger. Reopen the topics |
| Nothing locked | Every decided part is open again | Ask R3. Lock what the record decided |
| Stale brief | The status line is a year old and nobody asked | Default: escalate after 90 days |
| Lost thread | A rejected direction is proposed again | Read the last three entries first |
