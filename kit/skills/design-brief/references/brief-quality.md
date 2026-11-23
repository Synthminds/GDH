# Brief quality

Run the five tests on the draft before the user sees the summary. A worked brief and the failure patterns follow. Section numbers refer to the template.

## The five tests

### 1. The swap test (is it specific?)

1. Replace the subject with a competitor's name.
2. Read sections 1 to 5 and section 8 again.
3. Every sentence that is still true says nothing. Rewrite it, or send the topic back to `align`.

Pass when at least the user, the point of view, the brand word definitions and the trade-offs fail the swap.

### 2. The deniability test (does it choose?)

1. Count the "this, not that" lines in section 8. Three is the minimum.
2. For each line, ask: "Would a reasonable team choose the other side?" When nobody would, the line is not a trade-off.

"Fast, not slow" fails. "Fast to scan, not rich in detail" passes: a detail-first product is a real alternative.

### 3. The point-of-view test (is there a person?)

Section 3 holds two framings and one point of view.

- User: a person with two specific details. "Small-boat sailors who go out alone on weekday evenings."
- Need: a verb phrase. "To decide in one glance whether to leave the harbor."
- Insight: why the need is unmet. "Every app shows instruments. None gives an answer."
- Framings: two statements that open different solution sets, and the reason for the choice.

Fail when the user is a demographic, the need is a feature, the insight restates the need, or only one framing exists. Skip this test when the job size made section 3 optional and it holds one line of need.

### 4. The measure test (can we tell it worked?)

- One "do" line in section 5 names a behavior and how to observe it.
- One "feel" line names a feeling and how to test it.
- No baseline or target number is invented. "Baseline unknown" is an honest value.
- The worst case in section 10 names a group and a response.

### 5. The evidence test (what do we know?)

1. Each line is stated by the user, read from a file, proposed, or ASSUMED.
2. Lines from a file name the file.
3. Every proposed line carries `(proposed)` until the user answers it.
4. Every claim about people carries observed, reported or assumed.
5. Every guess about users, market or performance sits in section 15.

After confirmation, the decision entry labels stated and file-backed fields DOCUMENTED and ASSUMED lines UNTESTED. Nothing in a brief is VERIFIED until a test with real users or real output proves it.

## Worked brief

This example is invented for illustration. It continues the Tidewatch persona in `design-persona.md`. Job size: product. Sections 6, 7, 9, 11, 13 and 14 are shortened here.

```
Status: confirmed 2026-11-23 by the project owner

1. Subject
   A phone app screen that tells a small-boat sailor whether to leave the harbor in the next two hours.
   It is not a navigation chart and not a weather encyclopedia.

2. People and context
   User: sailors of boats under 8 m who go out alone on weekday evenings from tidal harbors. (reported)
   Also touched by: harbor staff who answer the same question by radio.
   Not for: racing crews who want raw data streams.
   Context: phone, one hand, outdoors, bright sun or dusk, wet fingers, weak signal.
   Before: walking down the dock. After: casting off, phone in a pocket.

3. Need and point of view
   Need: to decide in one glance whether to leave, and by when to be back.
   Framing A: sailors need a clearer marine weather app.
   Framing B: sailors need a go or no-go answer they can trust on the dock.
   Chosen: B, because A keeps the instrument panel that causes the problem.
   Point of view: a lone evening sailor needs a way to decide go or no-go in seconds,
   because every app shows instruments and leaves the judgment to a tired person on a dock.

4. Feel
   Target: in control. Must never feel: misled by stale data. Sensory line: quiet, steady, matte.

5. Primary job and success
   Job: decide go or no-go for a two-hour window. Then: 2. plan the return time. 3. log the trip.
   Do: four of five test sailors state the answer within ten seconds of opening the app. (proposed target; baseline unknown)
   Feel: testers describe it with a word like calm or clear, unprompted.

8. References and taste
   Brand words:
   Calm: one answer at a time. Not sleepy or pale. Shows up as one dominant element on each screen.
   Exact: numbers with units and times. Not technical jargon. Shows up as tabular figures and plain labels.
   Weathered: built for sun, salt and gloves. Not nautical kitsch. Shows up as high contrast and matte surfaces.
   This, not that:
   One answer, not a full instrument panel.
   Readable at arm's length in sun, not elegant on a desk.
   Honest about stale data, not always confident.

10. Risks and the worst case
   Worst case: a sailor trusts stale data and leaves. Response: data age is shown first when it is older than the forecast interval.

12. Scope and fidelity
   Deliverables: 1. the go or no-go screen. 2. the return planner.
   Not in this round: trip logging.
   Start: rung 1 (the content is known; the order on screen is not). Stop: rung 4.

15. Assumptions and open questions
   ASSUMED: most checks happen within 30 minutes of departure. (user said "you decide")
   Open: which tide data source is licensed for the app?
```

What makes it good:

- A competitor's name does not fit section 2, 3 or the trade-offs. It passes the swap test.
- Framing B removed the format and changed the design: one answer, not a panel.
- Each brand word predicts a visible choice. A reviewer can check "one dominant element".
- The use context rules things out before any design exists: no thin type, no low-contrast grey, no small targets.
- The target is marked proposed and the baseline unknown. Nothing is invented.
- The worst case changed the design: data age comes first.

## Brief failure patterns

| Pattern | Sign | Correction |
| --- | --- | --- |
| The universal brief | "A clean, modern site for users who want a seamless experience" | Swap test. Rewrite every sentence that survives it |
| One framing | Section 3 restates the request | Write framing B without the format. Compare |
| No exclusions | Section 8 holds only virtues | Draft three trade-offs and ask which is wrong |
| Feature as need | "Users need a dashboard" | Ask what they decide with it. Write the verb phrase |
| Demographic as person | "Millennials" | Ask for the situation: where, when, doing what |
| Unmeasurable success | "Users love it" | Write one behavior and one feeling test |
| Invented numbers | "Increase conversion by 30%" with no source | Ask for the baseline. Else write "baseline unknown" |
| Silent budget | No paid generation line, then a spend call is proposed | Section 13 always holds the budget and exposure lines |
| Brief as layout | Hero, grid and card counts in the brief | Move to the direction. Keep job and feel here |
| Unconfirmed brief | `(proposed)` marks remain and work starts | The status line is a gate |
| Hidden ASSUMED | A skipped field reads like a decision | Mark it ASSUMED and list it in section 15 |
| Stale brief | Scope changed, the brief did not | `align` re-aligns; this skill amends |
| Hidden approver | Someone with a veto appears at the end | Section 11 names every approver and when they see work |
