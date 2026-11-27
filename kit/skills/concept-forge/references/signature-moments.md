# Signature moments

Read this file at step 11 of `concept-forge`. It holds the patterns a signature moment can take, where it goes in the journey, the four moment checks and examples.

A signature moment is the one thing a viewer would describe to a friend. Each concept has exactly one. Spend boldness there and keep the rest quiet. Two signatures compete and neither is remembered.

## 1. Why one moment

- Usable is the floor, not the goal. A deliberate pleasurable element is what people remember and recommend (Designing for Emotion, ch. 1).
- The high point near the end of a key step shapes the memory of the whole (Designing for Emotion, ch. 5, the peak-end rule).
- Surprise fixes attention because it breaks a pattern. Used often, it becomes the pattern (Designing for Emotion, ch. 5).
- Personality shows in visuals, copy and interaction together (Designing for Emotion, ch. 3). The best moments use two of the three.

## 2. Patterns

Choose a pattern, then fill it from a mined item. The pattern is a shape; the mined item is the content.

| Pattern | Shape | Example from a mined item |
| --- | --- | --- |
| The real object | A mined tool or material becomes the interface itself | The timetable is the harbor's chalk board, written stroke by stroke |
| The ritual echo | The interface repeats a ritual insiders perform | The confirmation tears a ticket stub along its punch line |
| The honest number | One true figure, with its source, shown at the size it deserves | The live count of bikes already on the lower deck |
| The insider word | One line of vernacular, placed where a newcomer meets it, with its meaning | "She's on the slip" in the status line, with a plain gloss |
| The change of scale | A jump from the whole to one detail, or back | Zoom from the whole route to the one pier you stand on |
| The live trace | The work shows a real change as it happens | The boat mark moves along the crossing line in real time |
| The made mark | A drawn or stamped mark that only this subject would make | A tally-mark logo built from the crew's bike count |
| The end gift | A designed last state at the end of a key task | After booking, the ticket shows the sunrise time for that crossing |
| The quiet room | One space with almost nothing in it, where the subject speaks | A full-screen fog photograph with only the next departure time |
| The answer first | The one question people bring is answered before they ask it | "The late boat runs tonight" is the first line on the page |

## 3. Where the moment goes

Place the moment at a peak. Map the journey in a few steps first: before, first view, main task, end of task, after.

- Good places: the first view, the end of a key task, an empty state, a first-run state, a long wait.
- Bad places: an error, a payment form, a slow load, a validation message, a data readout the user acts on. These are valleys. In a valley, remove the pain; add no wit and no show (Designing for Emotion, ch. 5).
- Default: one moment per concept, and one per release of a product.

## 4. The four moment checks

Run each check and write the result in the concept file.

1. Retell: a viewer can describe it in one sentence with no color word, no font name and no effect name. "The ticket tears when you confirm" passes. "A glowing gradient" fails.
2. Subject: it traces to one mined item by id. With a competitor's name on the page, it stops fitting.
3. Peak: it sits at a good place from section 3, not in a valley.
4. No harm: it adds no step, hides no control, delays no feedback and holds no needed information behind a joke. When it moves, it has a still form for reduced motion. Emotional design that harms the task is cut (Designing for Emotion, ch. 1).

A moment that fails a check is rewritten or replaced. It is never softened. A gradient at half strength is still a gradient.

## 5. Moments that are not signatures

These read as generic. Reject them as signature moments, unless the design system requires one; then mark it `brand-required`.

- A gradient, glow, blur or glass effect on any element.
- A fade and slide-up on every section, or parallax on the hero.
- A cursor trail, a custom cursor or magnetic buttons, with no subject reason.
- Confetti on any success.
- A counter that runs up to an unsourced number.
- A typing animation of a headline.
- A dark mode toggle presented as a feature.
- An animated blob behind the hero.
- A three-dimensional tilt on cards.

## 6. Writing the moment down

In each concept file:

```
Signature moment: <one sentence a viewer would say>
Pattern: <pattern name>; from: <mined item id>
Where: <journey step>; trigger: <what starts it>
Still form: <what shows with reduced motion, or "does not move">
Checks: retell <pass>; subject <pass>; peak <pass>; no harm <pass>
```

## Sources

- Designing for Emotion (Aarron Walter), ch. 1: the hierarchy of needs, the deliberate pleasurable element, cut what harms the task; ch. 3: personality across visuals, copy and interaction; ch. 5: ownable moments, the peak-end rule, surprise used sparingly, valleys without wit.
- Principles of Product Design (DesignBetter), ch. 2: a story with a turning point and an outcome.
