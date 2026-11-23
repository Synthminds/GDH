# Design QA of the build against the handoff

Read this file at step 19 of `handoff-to-code`. It covers when to run design QA, how to scope it, how to compare the build with the package, how to class each difference, and how to close the handoff.

Evidence. The pre-launch design QA, the scoped review block and the locked list come from the DesignOps Handbook (DesignBetter), chapters 2 and 3: DOCUMENTED as method. The two verdicts (right thing, thing right) come from the Design Engineering Handbook, chapter 2: DOCUMENTED. The difference classes are this kit's own.

Terms. A difference is any place where the build differs from the package. A capture is a screenshot or recording of the rendered build.

## 1. When

| Moment | Scope |
| --- | --- |
| First rendered screen | That screen only, at every breakpoint and theme. Catch systemic errors early |
| Each milestone | The screens built since the last QA |
| Before release | Everything in scope; the full acceptance check set |

Default: never wait for the whole build before the first QA. A systemic error found on screen one saves every later screen.

## 2. Scope the review

Open every QA report with this block, before any finding.

```
Feedback wanted: does the build match the package for <screens>?
From whom: the design owner for look and copy; the builder for feasibility
Not useful now: new ideas, scope changes, items in the out-of-scope list
Locked: <decisions and screens already accepted>
```

A comment against a locked item asks "reopen?" and states the cost. It is never a silent change.

## 3. Inputs

1. The package: `design/handoff.md` at its current date.
2. The builder's check results for section 7.
3. Captures at each breakpoint and theme, per state in the matrix. Name them `<screen>-<state>-<width>-<theme>`.
4. The reference files for the same screens.

With no capture tool, ask the user for screenshots. Mark what nobody saw UNTESTED.

## 4. Procedure

1. Read the builder's check results. A failed gate is a finding before any visual review.
2. Run `design-critique` on the captures. It runs the tell scan; brand-required choices are not findings.
3. Run `accessibility-gate` on the build.
4. Compare each capture with its reference file, region by region: layout rule, tokens, type, copy, states, motion.
5. Class each difference with the table in section 5.
6. Write each finding as: where, expected (with the package section), seen, class, owner.
7. Run `refine-round` for the fixes the owner chooses.
8. A difference that is better than designed goes back into the design files and the package.
9. Repeat until the gates pass and the owner says yes.
10. Close: set the package section 10 to the evidence of this QA. Log the round.

## 5. Classes of difference

| Class | Meaning | Action |
| --- | --- | --- |
| Intent lost | The build breaks a decision, a gate or a state | Fix in code; blocks release when it is a gate |
| Package gap | The package did not say; the builder guessed | Decide; add a dated package section |
| Acceptable | Differs from the reference with no loss | Record; no change |
| Better than designed | The build solved a case better | Take it into the design files |
| Out of scope | Concerns something the package excluded | Park it; a new scope if wanted |

Count each class in the report. Many package gaps mean the package was thin: improve the template use for the next scope.

## 6. Two verdicts

State both. Neither stands in for the other.

1. Right thing: does the build serve the brief's primary job for its users?
2. Thing right: does the build match the package and pass its checks?

## 7. The report

Write `design/reviews/<date>-design-qa.md`:

```
Scope: <screens>, build <commit or preview>, package updated <date>
Checks: <n> PASS, <n> FAIL, <n> UNTESTED (list the fails)
Differences: intent lost <n>, package gap <n>, acceptable <n>, better <n>, out of scope <n>
Findings:
1. <screen, region, width, theme>: expected <section and rule>, seen <what>. Class: intent lost. Owner: builder.
Verdict, right thing: <yes | no, why>
Verdict, thing right: <yes | no, why>
Locked after this round: <items>
Evidence: VERIFIED <captures reviewed>; UNTESTED <not seen>
Next: <fix round | close handoff>
```

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Big-bang QA | The first review happens at release | QA the first screen |
| Taste review | Findings with no package reference | Every finding cites a section, or is a package gap |
| Reopening settled work | A locked decision changes in QA | Ask "reopen?" with its cost |
| Lost improvements | A better build choice is reverted to match the mockup | Take it into the design files |
| Unseen states | Only the default state was captured | Capture each state in the matrix |
