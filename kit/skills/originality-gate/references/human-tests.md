# The human tests

Read this file at step 8 of `originality-gate`. It holds the five tests that the script cannot run (swap, squint, logo removal, first five seconds and signature moment), the rule that turns their results and the script result into one verdict, and the review file template.

Each test needs the work in its running medium: a render, a screenshot, a printed proof or a played clip. Source reading does not pass a test. A test with no render is UNTESTED, and the review says why.

## 1. How to run a test

- Run each test on the render, not on the description of the work.
- Write the result as pass or fail, then one or two sentences of evidence a second reviewer can check.
- Name the exact element behind a fail: the selector, the screen region or the frame.
- Run the tests in the order below. The swap test frames the others.
- A `brand-required` element is out of scope for every test. List it, and judge the open choices only.
- Judge the work, not the maker. Write no verdict on taste alone.

## 2. Swap test

Question: does the work still fit when a competitor's name replaces this brand's name?

Steps:

1. Pick competitors from the brief, or products from the same category. Default: two.
2. Replace every brand name, product name and logo in the render with a competitor's. Do it on a copy, or describe it in words when a copy is not possible.
3. Read the page again from the top as that competitor's page.
4. List every part that still fits unchanged: the headline, the hero composition, the palette, the type, the imagery, the motion, the copy.

Pass: the page reads as wrong under both competitor names. At least the headline, the signature moment and one visual system (palette, type or imagery) stop fitting.
Fail: the page fits a competitor with no change beyond the name. Each part that still fits is a driver, and goes in the review.

Why it works: brand contrast is what makes a brand noticed and remembered (Designing for Emotion, ch. 2). A part that fits every brand in the category carries no contrast.

## 3. Squint test

Question: with the detail gone, do the hierarchy and the signature moment still read?

Steps:

1. Blur the render until no text is readable. A Gaussian blur on a screenshot, a step back from the screen, or half-closed eyes all work. Default: a blur radius of about one percent of the viewport width.
2. Write what is visible first, second and third.
3. Compare that list with the intended priority list in the brief and with the signature moment named in the concept file.

Pass: the first visible mass is the primary job or the signature moment, and the order matches the brief.
Fail: the blurred page is a stack of even gray bands, or a decorative effect (a glow, a gradient blob) wins over the content. A blurred page that matches a generic archetype shape (centered block, three equal boxes, a band of logos) is a fail as well.

Why it works: contrast tells the eye what matters, and a few strong breaks in pattern beat many weak ones (Designing for Emotion, ch. 2).

## 4. Logo-removal test

Question: with every logo and brand name removed, is the work still recognisably this brand?

Steps:

1. Remove the logo, the wordmark and every brand name from the render.
2. Show the result to a person who knows the brief, or read it yourself against `DESIGN.md` and the concept file.
3. Ask: which brand is this? Which parts told you?

Pass: the brand is named from non-logo parts (Default: two or more): the palette roles, the type voice, the imagery source, the composition, the copy voice, the motion or the signature moment.
Fail: the brand cannot be named, or it is named only from a product photo. The identity then rests on the logo alone.

Why it works: personality lives in visual design, copy and interaction together (Designing for Emotion, ch. 3). A brand that exists only in its logo has no visual lexicon.

## 5. First five seconds

Question: what does a first-time viewer remember after a short look?

Steps:

1. Show the first view to a person who has not seen the work. Default: five seconds, then hide it. With no person available, look at the render for five seconds yourself, after a break, with the brief closed.
2. Ask for three things: what the product is, who it is for, and one thing they remember.
3. Write the answers word for word.

Pass: the viewer names the subject and the audience, and the remembered thing belongs to this subject or is the signature moment.
Fail: the viewer names the category only ("some AI tool", "a SaaS page"), or remembers a generic effect ("the purple gradient").

A self-run test is weak evidence. Label it "self-run" in the review.

Why it works: people decide fast and by instinct when options look alike (Designing for Emotion, ch. 6). Showing the thing before explaining it is how the test reads real reactions (Design Thinking Handbook, ch. 6).

## 6. Signature-moment check

Question: does the work hold the one moment its concept promised, and does it hold up?

Steps:

1. Read the signature moment in the concept file (`design/concepts/<n>-<name>.md`) or in the direction file.
2. Find it in the render. Name the element, the screen and the trigger.
3. Check four things:
   - It exists in the build, not only in the concept file.
   - A viewer could describe it to a friend in one sentence without a color word.
   - It sits at a peak of the journey, such as the first view, a completed task or the end of a flow, and not in a moment of pain such as an error or a payment form.
   - It does not slow, hide or block the primary job, and it has a reduced-motion form when it moves.

Pass: all four hold.
Fail: any one fails. A missing moment is the most common fail: the build dropped it for time.

Why it works: one designed peak at the end of a key step shapes the memory of the whole experience, and surprise works only when it is rare (Designing for Emotion, ch. 5). Emotional design that harms the task turns delight into a complaint (Designing for Emotion, ch. 1).

## 7. The verdict rule

The script is evidence, not the judge. The five human tests decide, and the script result sets how much they must prove. Combine them in this order. The first rule that applies sets the verdict.

| Rule | Verdict |
| --- | --- |
| The script says derivative, and any of the five human tests fails | derivative |
| The script says derivative, and all five human tests pass | watch. Write why the script is wrong: the drivers it names and the evidence that they belong to this subject or are `brand-required` |
| Two or more human tests fail (Default: two), at any script result | derivative |
| The swap test fails and the signature moment is missing, at any script result | derivative |
| The script says watch, or one human test fails | watch |
| The script says none (no page structure read) and all five tests pass | original, labelled "tests only" |
| Everything else | original |

Notes:

- The five tests are swap, squint, logo removal, first five seconds and signature moment. A test marked UNTESTED does not pass. With a derivative script result and an untested test, the verdict is derivative.
- The score in the verdict line is the script's nearest similarity, unchanged. The human tests change the verdict word, never the number. With a script result of none, write `score n/a` and `nearest none`.
- The nearest name in the verdict line is the archetype id or the file name of the nearest fingerprint.
- The verdict line keeps its format: `Originality: original | watch | derivative (score 0.xx, nearest <archetype>)`. The script word none never appears in the review verdict line; the rule above turns it into one of the three words.
- A watch verdict may ship when the user accepts it in writing. Log the acceptance in `design/decisions.md`.
- A derivative verdict does not ship (kernel rule 17).

## 8. Review file template

Write `design/reviews/<YYYY-MM-DD>-originality.md`:

```
Originality: <original | watch | derivative> (score <0.xx>, nearest <archetype>)

# Originality review: <scope>

Date: <YYYY-MM-DD>; stage: <explore | refine | finalize>; reviewer: <agent or person>; <independent | single-context>
Files: <paths>; render: <screenshot paths or UNTESTED>
Concept: <design/concepts/<n>-<name>.md or none>; signature moment: <one sentence>

## Script
Command: originality.py check <paths> --against <folder>
Nearest: <id> (<library | file>), similarity <0.xx>
Drivers: <dimension score> x up to 3
Next matches: <id score> x up to 3
Brand-required drivers: <dimension: source> or none

## Human tests
| Test | Result | Evidence |
| --- | --- | --- |
| Swap | pass or fail | <which parts fit a competitor> |
| Squint | pass or fail | <first, second, third mass> |
| Logo removal | pass or fail | <parts that name the brand> |
| First five seconds | pass or fail | <answers, word for word; self-run or person> |
| Signature moment | pass or fail | <element, trigger, the four checks> |

## Verdict
Rule applied: <row of section 7>
What makes it this subject's: <list>
What makes it generic: <element: source pattern> x n
To rebuild from the subject: <part: the mined item to start from> x n

Evidence: VERIFIED <what was run or rendered>; UNTESTED <what was not>
```

## Sources

- Designing for Emotion (Aarron Walter), ch. 1: the hierarchy of needs and harm to the task; ch. 2: contrast, brand contrast; ch. 3: personality across channels; ch. 5: peak moments and surprise; ch. 6: gut decisions.
- Design Thinking Handbook (DesignBetter), ch. 6: show before you tell, watch reactions.
- Principles of Product Design (DesignBetter), ch. 4: critique against stated goals, look before you judge.
- Anthropic frontend-design skill: the swap test.
