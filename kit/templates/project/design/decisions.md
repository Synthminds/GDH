# Design decisions

This file is the decision record. Add one entry for each round. Newest entry last. Never edit an old entry; add a new one that replaces it.

Entry format (fixed):

```
## YYYY-MM-DD round <n>: <scope>
Stage: explore | refine | finalize
Shown: <options>
Feedback asked: <the question>
Keep / Change / Remove: <per part>
Decision: <choice> (by <who>)
Rejected: <option>: <reason>
Open: <questions>
Evidence: VERIFIED | DOCUMENTED | UNTESTED <what>
```

Rules:

- One `Rejected:` line for each rejected option. Write `Rejected: none` when nothing was rejected.
- `Decision:` names the person who decided. An agent proposal with no user answer is written as `Decision: pending`.
- `Evidence:` says what was checked for this round and what was not.
- Before you propose an option, search this file. Do not propose a rejected option again without new evidence.
- Alignment and re-alignment entries from `align` are numbered `round 0`. Round 0 is outside the design rounds. A skill that counts rounds skips it. The date and the scope tell round 0 entries apart.
- A consent entry uses this format. Its scope starts with `consent,`. Its round number and stage are those of the current round. A revocation is a new consent entry with `Decision: consent revoked (by <who>)`.
