# Craft of the Whiteboard type

Read this file at step 12 of `claude-design` when the type is Whiteboard. It restates the board type's rules on shape, marks, spacing, drawings and working beside people, in my own words.

Evidence. Rules come from the Whiteboard type's rule file and its drawing reference, read 2026-11-23: DOCUMENTED. No export path is described in the files read; the downloads capability is listed but unexplained: UNKNOWN. No board was built for this kit.

Terms. An element is one item on the board: a shape, a section, a text, a stroke, an arrow, an image, an embed, a table or a link card. A claim is a marker that shows people where work is happening.

## 1. Choose the Whiteboard when

- The job is thinking with people: a flow, a sitemap, a journey map, a concept map, a brainstorm, a vote, a rough storyboard, an explanatory sketch.
- It is the fastest shared surface for a feedback talk.
- Use a canvas when the output must be brand-exact or exported. Use a diagram tool from the catalog when the diagram must live in a repository.

## 2. Give the board the shape of the idea

The common failure is box, arrow, box in a grid. Pick the shape from the idea:

| Idea | Board shape |
| --- | --- |
| A cycle | A loop |
| A process | A line |
| Composition, hierarchy | A tree |
| Roles or phases in parallel | Lanes |
| Two axes of judgment | A matrix |
| Places or areas | A map |
| Point-by-point comparison | A table element, never a grid of blocks |

## 3. Reading rules

1. Lead with a title and one takeaway sentence of ten words or fewer.
2. Keep a new board within a modest area so its words open readable; the card gives the size.
3. A few words per item. A label sits on or beside its part.
4. Size says what matters. A gap says the subject changes. A box says "one thing".
5. At most four marks with meaning per board: colors or outlines. One strong color on what matters most.
6. Spacing grows with what sits in the gap. Neighbors get a small gap. A gap with an arrow is larger. A gap with a labelled arrow is largest.

## 4. Colors

The board uses its own named fills and inks, or any hex value. It installs no design system. When brand colors matter, type the hex values from the pack and say so; the board does not update when the system changes.

## 5. Working beside people

1. Before a change, write a claim, so people see where you work. End the claim when done.
2. Never rebuild a board. Write only what changes.
3. Position is meaning. Extend existing work where it stands. Do not add a second version beside it.
4. Keep what a person grouped.
5. Carry a change through to everything it makes stale.
6. Read the view context to resolve "this". With no context, ask which part.

## 6. Drawings

A drawing is an image element made from one inline SVG with a declared style.

1. Draw the real thing with true proportions and expert detail, caught in use.
2. Never draw people or parts of people.
3. Plain shapes, back to front, within the size budget the card states. A breach shows a grey box with no warning.
4. No text inside the drawing, no style attribute, no filter.
5. The description names the viewpoint and many real parts.
6. One board keeps mostly to one of the type's drawing styles.
7. Words go in separate text elements beside the picture, with short straight arrows to the parts.

## 7. Limits to plan around

- The type caps elements per board, size per element, total size, and writes per call. Read them in the card before a large board.
- Embeds are small sealed pages with a size cap.

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Grid of boxes | Every idea is box, arrow, box | Choose the board shape from section 2 |
| Rainbow board | Six colors with no key | Four marks at most; one strong color |
| Second version | A copy beside the old cluster | Extend in place |
| Rebuilt board | All elements rewritten | Write only the change |
| Drawn person | A figure in a drawing | Draw the object in use instead |

## 9. Worked example

Request: "Map the sign-up flow so we can see where people drop off."

1. Shape: a line, left to right, five steps.
2. Title: "Sign-up flow". Takeaway: "Most people leave at email check."
3. Marks: one strong color on the email-check step; grey for the rest.
4. A table element below compares drop-off per step. The numbers are `[FROM ANALYTICS]` placeholders until the user gives them.
5. Claim, write, end the claim. Reply with the rationale; log it.
