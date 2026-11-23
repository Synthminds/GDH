# Report format

Read this file at step 15 of `accessibility-gate`. It holds the report template, the ranking rule, the exception rule and the limits statement.

## 1. The template

Write the report to `design/reviews/<YYYY-MM-DD>-a11y.md`. Keep the section order.

```
# Accessibility report: <scope>

Date: <YYYY-MM-DD>. Media: <web | app | chart | slides | print | video>. Themes: <ids>.
Mode: <independent (a11y-auditor) | single-context>. Target: <level from the brief, or the GDH floor>.
Verdict: <pass | fail | incomplete>

## Gates

| # | Gate | Result | Where | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Body text contrast | pass / fail / n.a. / UNTESTED | <screen, token pair> | <ratio, command, capture> |

## Failures, ranked

1. <what fails> at <where>. Harm: <who is blocked and from what>. Fix: <the smallest change>. Owner skill: <color | typography | ...>.

## Defaults not met

| Default | Where | Source class | Note |
| --- | --- | --- | --- |

## Exceptions

| Gate | Where | Reason | Accepted by | Date | Review date |
| --- | --- | --- | --- | --- | --- |

## Not tested

| Check | Reason | What would test it |
| --- | --- | --- |

## What this report cannot prove

<the limits statement>

## Method

Commands run, tools used, flows walked, viewports, the reader and browser pair, the sample sizes.
```

## 2. One result for each check

| Result | Use it when |
| --- | --- |
| pass | You measured or observed it on the render, and it met the gate. |
| fail | You measured or observed it, and it did not meet the gate. |
| n.a. | The medium has no such thing. Give the reason in one clause. |
| UNTESTED | You could not observe it. Give the reason and what would test it. |

A source reading alone gives DOCUMENTED evidence. It does not give a pass for a render check.

## 3. The ranking rule

Rank failures by harm to the person, not by ease of fixing.

1. Blocks a task: a person cannot complete the primary job. Example: a keyboard trap in the checkout.
2. Blocks content: a person cannot read or perceive something that matters. Example: body text under the ratio.
3. Slows or confuses: the task is possible, with effort. Example: an illogical focus order.
4. Friction: a default is not met and no gate fails.

Inside one rank, put the failure on the most used flow first. Each entry names the owner skill, so `refine-round` can route it.

## 4. The exception rule

1. Only the user can accept an exception. An agent never waives a gate.
2. An exception names the gate, the place, the reason, the person and a review date.
3. `refine-round` logs it in `design/decisions.md`. This report lists it and keeps the verdict `fail`, with the note "exception accepted".
4. A brand-required color that fails contrast is still a failure. Report it with the source, and propose the nearest passing value.
5. Do not offer an exception first. Offer the fix first.

## 5. The limits statement

End every report with this statement, filled in.

```
This report covers <scope> on <date>. It checked <n> gates on <media>.
It is a sample: <flows walked>, <viewports>, <reader and browser, or none>.
It makes no claim of conformance with any standard.
The ratios used are the published WCAG 2.2 AA values. This kit did not open the standard.
Not covered: <content added later, third-party embeds, untested flows, real assistive technology users>.
```

## 6. The verdict

| Verdict | Condition |
| --- | --- |
| pass | Every applicable gate has the result pass. |
| fail | One gate or more has the result fail. |
| incomplete | No gate failed, and one gate or more is UNTESTED. |

Never round `incomplete` up to `pass`.

## 7. The second run

After fixes, run the gate again. Write a new dated report. Add one table at the top.

| Gate | Earlier result | Result now | Change made |
| --- | --- | --- | --- |
