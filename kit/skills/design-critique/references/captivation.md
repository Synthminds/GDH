# The captivation rubric

Read this file after the tell scan in `design-critique`. It scores whether the work holds attention for the right reasons: it belongs to its subject, it has a personality and one moment worth retelling, and it is finished with care. It sits beside the main rubric in [rubric.md](rubric.md). It does not replace it.

Evidence class: the six dimensions and their bands are GDH defaults. They come from Designing for Emotion and Principles of Product Design, as named in each section. They were not validated on real projects.

## 1. The order of needs

Designing for Emotion (ch. 1) orders user needs: functional, reliable, usable, then pleasurable. Captivation lives in the top layer. It never pays for a failure below it.

- Score captivation only after the gates pass and the primary job works on the first view.
- When a lower need fails, write "not scored: <need> fails" and stop. A delightful page that a first-time user cannot use is not captivating; it is broken.
- An element that adds pleasure and slows, hides or blocks the task is a finding, at any captivation score (Designing for Emotion, ch. 1).

## 2. Rules of scoring

- Score each dimension from 0 to 3. Use whole numbers.
- A 3 is rare. Most good work scores 2.
- Each score below 3 points to at least one finding. Each 3 points to one "working well" item.
- A `brand-required` choice never lowers a score.
- Score what you saw on the render. A dimension you could not check is "not scored", with the reason.
- Total: 18. Default: 12 or more is captivating; 8 to 11 is competent but forgettable; 7 or less is generic. The bands are defaults.

## 3. The six dimensions

### A. Subject truth

Question: do the visible choices trace to this subject's own world?

| Score | What it looks like |
| --- | --- |
| 0 | Nothing traces to the subject. Swap the name and it is another product's page |
| 1 | The copy names the subject; the visuals are the category default |
| 2 | Two or more visible systems (palette, type, imagery, composition) trace to mined items or the brief |
| 3 | A newcomer learns something true about the subject from the design alone, before reading the copy |

Test: name the source of each visible system. Read `design/concepts/mine.md` when it exists. Run the swap test from `originality-gate`.

### B. Personality

Question: does the work have a character that matches the brand words, in visuals, copy and interaction together?

| Score | What it looks like |
| --- | --- |
| 0 | No character. Neutral parts and neutral words |
| 1 | Character in one channel only, such as a playful headline on a stock layout |
| 2 | The same character in two channels, with no channel contradicting it |
| 3 | The character holds across visuals, copy and interaction, and the voice shifts with the situation: plainer in errors, warmer at success |

Test: on one screen, mark one visual, one copy and one interaction detail that each express a named brand word (Designing for Emotion, ch. 3). Read one error or empty state for the voice shift.

### C. Signature moment

Question: is there one moment a viewer would describe to a friend?

| Score | What it looks like |
| --- | --- |
| 0 | No moment. Or every section competes with an effect |
| 1 | A moment exists, but it is a generic effect, or it sits in a valley such as an error or a form |
| 2 | One moment from the subject, at a peak, that a viewer can retell in a sentence |
| 3 | As 2, and it sits at the end of a key step, it is the thing a fresh viewer names first, and nothing else competes with it |

Test: the signature-moment check in `originality-gate`, `references/human-tests.md`, section 6. The peak at the end of a step shapes the memory of the whole (Designing for Emotion, ch. 5).

### D. Surprise held within usability

Question: does the work break one expectation on purpose, without breaking the task?

| Score | What it looks like |
| --- | --- |
| 0 | Nothing unexpected; or a surprise that blocks, hides or delays the task |
| 1 | A surprise that is decoration only, or one repeated so often that it is the pattern |
| 2 | One or two deliberate breaks with category convention, named, and the task stays as fast |
| 3 | The break carries meaning: it explains the subject or the product better than the convention would, and a first-time user still finishes the task unaided |

Test: list each break with the category convention it breaks. For each, time the primary task or count its steps with and without it. Surprise works because it is rare (Designing for Emotion, ch. 5). Contrast with the category is what gets a brand noticed (Designing for Emotion, ch. 2).

### E. Emotional fit to the brand words

Question: does the feeling the work gives match the brand words and the user's state at each step?

| Score | What it looks like |
| --- | --- |
| 0 | The feeling contradicts a brand word, or jokes appear where the user is anxious |
| 1 | The feeling is neutral; no brand word shows |
| 2 | Each brand word shows somewhere, and no step mismatches the user's likely state |
| 3 | The work answers the user's state at the moments that change it: calm at worry, clear at error, warm at success. A reviewer can say which brand word each moment serves |

Test: list the journey steps of the main flow with the likely feeling at each. Mark peaks and valleys. A valley gets a fix, not wit (Designing for Emotion, ch. 5). Read the brief line for the target feeling (Design Thinking Handbook, ch. 3, as used in the brief).

### F. Craft finish

Question: is the work finished with visible care?

| Score | What it looks like |
| --- | --- |
| 0 | Visible defects: misaligned edges, broken images, clipped text, default focus rings on a custom design, placeholder copy |
| 1 | Clean at the main breakpoint; rough at others, or in empty, loading and error states |
| 2 | Consistent spacing, type and alignment from tokens, at every breakpoint and theme checked |
| 3 | As 2, and the small states are designed too: empty, loading, error, focus, hover, reduced motion. Nothing looks left at its default |

Test: the aesthetic pass with named criteria: proportion, type, color, spacing and finish (Designing for Emotion, ch. 2). Care in the visible parts suggests care in the hidden ones (Designing for Emotion, ch. 6). Review the running medium, not a static mock (Principles of Product Design, ch. 4).

## 4. Writing the score

Add this block to the review file, after the main rubric:

```
Captivation: <total>/18 (subject <n>, personality <n>, moment <n>, surprise <n>, fit <n>, craft <n>); band <captivating | forgettable | generic>
Lowest: <dimension>: <finding number>
Signature moment: <one sentence, or "none found">
```

Rules:

- Each score below 3 cites a finding by number.
- The suggestion in a captivation finding is a direction in one sentence, tied to a mined item or a brief line. It is not a design.
- At stage finalize, run the `originality-gate` skill as well. A captivation score never replaces an originality verdict.

## 5. Common misreads

- High craft is not captivation. A flawless default page scores 3 on craft and 0 on subject truth.
- Loud is not captivating. Many effects lower the moment score, because they compete.
- A strong personality will not please everyone. A comment such as "this may not suit every visitor" is not, alone, a reason to lower personality (Designing for Emotion, ch. 3).
- A dashboard or tool can score well. Its moment may be the honest number or the end of a task, not an animation.

## Sources

- Designing for Emotion (Aarron Walter), ch. 1: the hierarchy of needs, emotion that harms the task; ch. 2: contrast, brand contrast, aesthetics as usability; ch. 3: personality across channels, voice shifts, accepting that a strong personality repels some; ch. 5: ownable moments, the peak-end rule, surprise, valleys; ch. 6: trust through visible craft.
- Principles of Product Design (DesignBetter), ch. 2: story first; ch. 4: critique against goals in the running medium.
- Design Thinking Handbook (DesignBetter), ch. 3: the feeling the outcome should produce.
