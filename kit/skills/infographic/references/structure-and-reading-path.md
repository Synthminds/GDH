# Structure, visual metaphor, copy and reading path

Read this file at steps 5 to 8 of `infographic`. It covers structures and when to use each, the visual metaphor, writing the copy first, hierarchy, reading path patterns, the sketch round and failure patterns.

Evidence. The structure list and "explain, do not decorate" come from the GDH research (Nigel Holmes and Alberto Cairo, from memory). Metaphor to make an abstract or feared subject approachable, and "show, do not tell" with a demonstration, come from "Designing for Emotion", chapters 3 and 6. Contrast for the few things that matter, and limiting loud elements, come from the same book, chapter 2. The shape-of-the-idea rule comes from the Claude Whiteboard type rules (read 2026-11-23). Numbers are defaults.

## 1. Choose the structure from the content

| Structure | Content shape | Main visual | Example message |
| --- | --- | --- | --- |
| Comparison | Two or more things side by side | Paired bars, mirrored columns, a table with marks | "Train beats plane on carbon by 8 to 1 on this route" |
| Timeline | Events in order of time | A time axis with marked events | "The policy took 12 years from proposal to law" |
| Process | Steps that lead to an outcome | Numbered steps along a path | "A permit takes 6 steps; 3 wait on one office" |
| Statistic set | A few key numbers around one theme | One hero number, supporting numbers at lower weight | "One in five adults volunteered last year" |
| Anatomy | Parts of one object or system | A labelled drawing with leader lines | "Where the energy in a phone battery goes" |
| Hierarchy | Levels or containment | Nested shapes, a tree, a pyramid only if levels are truly ranked | "How the budget splits from total to programs" |
| Map | Where things happen | A map of rates, or a ranked list beside a small map | "Flood risk rises fastest on the east coast" |
| Flow | Movement between states | Sankey, flow arrows with widths | "Where recycled plastic actually ends up" |
| Cause and effect | Drivers and results | A chain or a branching diagram | "Three habits explain most of a household's water use" |
| Myth versus fact | Correcting a belief | Paired panels, the fact emphasized | "Most microplastic comes from tyres, not bottles" |

Rules:

- Choose the structure from the message, not from a template. A process message drawn as a statistic set loses the order.
- A piece may combine structures (a statistic set with a small timeline). One structure leads; the others support.
- Give the whole piece the shape the idea has: a loop for a cycle, a line for a process, a tree for composition. Avoid a grid of equal boxes for content that is not equal.

## 2. The visual metaphor

The metaphor is the picture idea that carries the message. It must explain, not decorate.

Steps:

1. Name what the reader finds abstract, confusing or feared about the subject.
2. List five to ten concrete pictures from the subject's own world: objects, places, tools, everyday comparisons.
3. Pick the one that makes the message obvious at a glance: a bathtub for a budget that drains, a staircase for a process that rises, a city map for a system with districts.
4. Test it: would a reader get the message from the picture plus the headline alone? Does the metaphor distort any quantity?
5. ASK: in an explore round, show two or three metaphor directions with the same copy. Directions differ in idea, not in color.

Rules:

- A metaphor must not encode numbers it cannot draw honestly. A glass that is "half full" must be filled to half its volume, not half its height, when the glass narrows.
- Literal is fine when it is clearest. A labelled drawing of the real object often beats a clever metaphor.
- One metaphor per piece. Mixed metaphors (a ladder that becomes a river) confuse.
- Show, do not tell: a worked example or a demonstration beats a paragraph of claims.
- Humor and characters help an approachable subject; they are out of place in grief, danger, money loss or error.

## 3. Write the copy first

Write every word before layout. Copy sets the space the design needs.

| Part | Length default | Job |
| --- | --- | --- |
| Headline | One line, up to about 10 to 12 words | The message |
| Introduction | One to two sentences | Context: who, where, when |
| Section labels | Two to five words each | Signposts along the path |
| Annotations | One clause each | Explain a mark or a number |
| Numbers | As in the fact table | The evidence |
| Takeaway | One sentence | What to do or believe |
| Sources | One line per source | Credibility |

Rules:

- Use the audience's words. Define any term the reader may not know where it first appears.
- Numbers in sentences use the same values and rounding as the fact table.
- Cut every sentence the picture already says.
- No filler copy and no placeholder text in a sketch shown to the user; use the real words.

## 4. Hierarchy

- One hero element: the main visual or the main number. It is the largest and has the most contrast.
- Default: three levels of emphasis: hero, supporting, detail. More levels blur.
- Limit loud elements. Each high-contrast element maps to a stated priority; a second element at equal weight competes with the message.
- Supporting parts sit at lower weight: smaller, lighter, fewer colors.
- Sources and notes are quiet but readable, never below the minimum size.

## 5. The reading path

The eye must move in one clear order. Pick a pattern that fits the format and the structure.

| Pattern | Fits | How |
| --- | --- | --- |
| Top to bottom column | Tall scroll, phone, poster with one column | Headline, hero, sections in order, takeaway, sources |
| Z path | Wide poster, landscape slide | Headline top left, hero top right or center, supporting bottom left, takeaway bottom right |
| Numbered sequence | Process, timeline | Large step numbers; arrows only where the order is not obvious |
| Center out | Anatomy, one object | Hero object in the center, labels around it with leader lines |
| Left to right | Comparison, before and after, timeline | Two or more columns read in order |
| Slide by slide | Carousel, deck | One idea per frame; each frame titled |

Rules:

- Number steps only when they are a real sequence. Numbers on unordered items invent an order.
- Align elements on a grid so the path has clear edges.
- Use space to group: tight inside a section, wide between sections.
- Test: a cold reader traces the path with a finger without help. Where they hesitate, the path breaks.

## 6. The sketch round

1. Draw gray boxes with the real copy, at the real format size.
2. Mark the reading path with numbers on a copy of the sketch.
3. Show the sketch with the message and takeaway written above it.
4. ASK: "Keep, change or remove, for each part?" Also: "What do you read first, second, last?"
5. Log the answers per part in `design/decisions.md`. Change only what was asked.
6. In an explore round, show two or three metaphor directions on the same copy; in a refine round, variants differ in one named attribute.

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Template structure | Every infographic is a tall column of icon plus number | Structure from the message |
| Decoration as metaphor | Clip art around the numbers | A metaphor that explains, or a literal drawing |
| Mixed metaphor | Ladder, river and rocket in one piece | One metaphor |
| Two heroes | Two elements fight for first glance | One hero; demote the other |
| Lost path | The reader jumps around | A pattern from section 5; grid alignment |
| Layout before copy | Text crammed into decorative boxes | Copy first; space from copy |
| Invented order | 01, 02, 03 on items that are not steps | Numbers only for real sequences |
