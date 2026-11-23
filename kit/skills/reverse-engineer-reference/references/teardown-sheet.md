# The teardown sheet

Read this file at step 13 of `reverse-engineer-reference`. One sheet for each reference. Copy the blank sheet from `templates/teardown-sheet.md` and fill it.

## Where it lives

```
design/directions/references/
  <slug>/
    teardown.md            the sheet: notes in the project's words; may be committed
    shots/                 screenshots and recordings; private; ignored in a public repository
    inventory-<width>.json output of the inventory script; private
```

- The slug is kebab-case, from the reference name: `acme-docs`, `northwind-pricing`.
- `design/directions/` is the reference area. `assets.py check` treats a copy of any file in it, found in an asset folder, as a finding.
- Set `status: confirmed` in the front matter when the user confirms the lessons.

## The rule for each section

| Section | Write | Do not write |
| --- | --- | --- |
| 0. Why this reference | The user's words, the exact part, the effect on a visitor | "It looks good" |
| 1. Structure | Sections in order, the job of each, the most prominent element | Their headings |
| 2. Layout system | Columns, maximum width, alignment, the change at each width | A copy of their grid values as a set |
| 3. Type | Classification, count of sizes, ratios, line-height ratios | Font files, or a family named as fact from a screenshot |
| 4. Spacing rhythm | The base unit, the multiples, the two or three section gaps | Every spacing value |
| 5. Color roles | Roles, proportions, where the accent appears | Their palette as a list of values |
| 6. Motion | What moves, the trigger, the duration, the easing shape, the order | Their animation code |
| 7. Technique | One technique note for each effect, in your words | Quoted script or style code |
| 8. Content pattern | The kind of statement in each place, its length, its voice | Their sentences |
| 9. What we learn | Three rows at most: observation, principle, translation | A row whose translation repeats the observation |
| 10. What stays | Code, assets, wording, values as a set | Nothing: every sheet fills this section |
| 11. Signature elements | The few things that identify the reference | Conventions that every product shares |
| 12. Open questions | What you could not measure or decide | Guesses presented as facts |

Observations may hold numbers. A measured size or duration is a fact about the page, and the sheet is where it belongs. Numbers stop at the observation rung: principles and translations hold none of theirs.

## Quality tests for a finished sheet

Run all six before you show the sheet.

1. **Permission line.** The front matter names the permission and who confirmed it.
2. **Evidence on every finding.** Each row or line carries VERIFIED, DOCUMENTED or UNTESTED.
3. **Own-words test.** Sections 8 to 11 hold no sentence from the reference.
4. **Ladder complete.** Each row in section 9 has all three rungs and a second product in the last-but-one column.
5. **Section 10 filled.** It names what stays, for this reference, in concrete terms.
6. **Signatures named.** Section 11 lists one to three elements. A sheet with none has not looked hard enough, or the reference has no identity worth studying.

## After the user confirms

Set `status: confirmed` and `lessons-confirmed-by`. Then add the round to `design/decisions.md` in the fixed format:

```
## 2026-11-23 round 2: lessons from references
Stage: explore
Shown: teardown sheets for northwind-docs, <slug 2>, <slug 3>; three lessons each
Feedback asked: Which of these lessons should shape the directions, and what must stay with each reference?
Keep / Change / Remove: Keep lessons 1 and 3 of northwind-docs. Change lesson 2: apply to report pages only. Remove all of <slug 3>.
Decision: five lessons carried into the directions (by <who>)
Rejected: <slug 3>: the admired part is its signature illustration style
Open: reduced-motion behavior of the outline marker
Evidence: VERIFIED computed styles at 1280 px and 390 px; UNTESTED motion durations
```

## What makes a lesson worth a row

A row earns its place when it changes a decision in this project.

- Weak: "Good use of white space." It changes nothing.
- Better: "Topics are separated by a gap three to four times the gap inside a topic." It can be tested and applied.
- Strong: the same, plus the translation: "Use `space-section` between topics and `space-block` inside. Our pricing page breaks this: the plan cards sit closer to the next topic than to their own heading."

Prefer lessons about relations (ratios, order, scarcity) over lessons about values. Relations transfer. Values belong to the brand they came from.

## A filled example

The reference in this example is fictional. It shows the level of detail, not facts about a real product.

```
---
status: confirmed
reference: "Northwind Docs (fictional)"
url: "https://docs.northwind.example/guides/start"
captured: 2026-11-23
route: browser
permission: "public page"
permission-confirmed-by: "project owner, 2026-11-23"
lessons-confirmed-by: "project owner, 2026-11-23"
---
```

**0. Why this reference.** Admired: "I always know where I am and what to read next." The exact part: the three-part page frame. Effect on a visitor: no dead ends. Category: other (developer documentation; this project is an analytics product).

**1. Structure.**

| # | Section | Its job | Most prominent element | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Top bar | Search and product switch | The search field, by width | VERIFIED 1280 px |
| 2 | Left tree | Where am I in the whole | The current page, by weight and a marker | VERIFIED 1280 px |
| 3 | Article | The content | The page title, by size | VERIFIED 1280 px |
| 4 | Right outline | Where am I in this page | The current heading, by color | VERIFIED 1280 px |
| 5 | Next and previous | What to read next | "Next", by position and size | VERIFIED 1280 px |

First view holds: title, one-sentence summary, the first code sample. Absent: any hero image, any banner.

**2. Layout system.**

| Width | Columns | Max content width | Alignment | What changes here | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1920 | 3 | Fixed; side space grows | Centered frame | Nothing | VERIFIED |
| 1280 | 3 | Fills the window | Left edges shared | Baseline | VERIFIED |
| 768 | 2 | Fills the window | Left edges shared | The right outline moves above the article as a menu | VERIFIED |
| 390 | 1 | Fills the window | One edge | The left tree becomes a drawer | VERIFIED |

**3. Type.** One sans family for text, one mono for code (classification only; the family names are in the inventory). Six sizes. Body 16 px with a line-height ratio of 1.7. Title 40 px with 1.2. Steps are hand-set, not one ratio: small steps near body, one large jump to the title. Evidence: VERIFIED 1280 px, computed styles.

**4. Spacing rhythm.** Base unit 4 px. Multiples 2, 3, 4, 6, 8, 12. Gap inside a topic 16 px; between topics 48 px: a ratio of three. Density: generous for reading, tight in navigation. Evidence: VERIFIED.

**5. Color roles.** Two neutrals carry almost the whole view. One accent hue. The accent appears three times in a view: current tree item, current outline item, links. Dark theme: same structure. Evidence: VERIFIED for roles; share of the view UNTESTED (by eye).

**6. Motion.** One motion: the outline marker moves as the reader scrolls. About 150 ms, fast start and slow end. Reduced motion: UNTESTED.

**7. Technique.**

```
Effect: The current heading in the right outline is marked as the reader scrolls.
Trigger: scroll position
Made with: a platform observer for element visibility, UNTESTED guess (no tool was connected)
How: Each heading is watched. The last heading to cross the top third of the viewport becomes current.
Cost: light script; no layout work during scroll
Our version: mark the current chart group in our report outline the same way, with our accent token
```

**8. Content pattern.** Title: a task, as a verb phrase, under eight words. Summary: one sentence that says what the reader will have at the end. Primary action: none in the first view; the "next" link is the action.

**9. What we learn.**

| # | Observation | Principle | Our translation | Second product | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | Three frames mark the current place at once | Show location at every level, all the time | Our report view marks the current workspace, report and chart group; each with `color.accent` and a weight change | Most code editors: file tree, tabs, breadcrumb | VERIFIED |
| 2 | Topic gap is three times the inner gap | Separate topics by a clear multiple of the inner gap | `space-section` is three steps above `space-block` on report pages | Long-form news articles | VERIFIED |
| 3 | The accent appears only on "where you are" and links | Reserve the accent for orientation | Remove `color.accent` from our decorative chart borders | Map applications: one color for the current position | VERIFIED |

**10. What stays with the reference.** Code: all of it, including the outline script. Assets and fonts: both families, the icons. Wording: every title and summary. Values as a set: the six type sizes and the neutral pair.

**11. Signature elements.** 1. The thin vertical marker that slides beside the outline. 2. The mono face used for all navigation labels.

**12. Open questions.** Reduced-motion behavior. Whether the tree remembers its open state.
