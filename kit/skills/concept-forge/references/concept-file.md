# File formats

Read this file at steps 5 and 13 of `concept-forge`. It holds the format of every file the skill writes: the mining file, a concept file, the summary and the decision entry.

All files are Markdown in `design/concepts/`. Write real words from the brief. Use a bracketed placeholder for a missing fact, such as `[FACT NEEDED]`.

## 1. `design/concepts/mine.md`

```
# Subject mining: <subject>

Date: <YYYY-MM-DD>; brief: design/brief.md (<status>); discipline: <primary discipline>

## Subject in five lines
Subject: <one line>
Audience: <one line>
Primary job: <one line>
Use scene: <who, where, when, in what light>
Brand words: <three words>

## Materials
- M1 <item> (observed: <source> | assumed)
## Tools
- M4 <item> (...)
## Rituals
- M7 <before, during or after>: <item> (...)
## Places
- M9 <item> (...)
## Vernacular
- M11 "<word or phrase>": <meaning> (...)
## Tensions
- M13 <need A>, but <need B> (...)
## Surprising true fact
- M15 <one sentence> (source: <title, file or address>) | [FACT NEEDED]: <question that would find it>

## Gaps
- <list that stayed short, and what research would fill it>

## Reframes
- R1 How might we <...> (from M13)?
- R2 <person> needs a way to <need>, because <insight> (from M4, M11). They should feel <feeling>.
- R3 Wider or narrower: <...> (from M15)
Expected preference: R<n>, because <reason>
```

## 2. `design/concepts/<n>-<name>.md`

`<n>` is a number, `<name>` is two or three kebab-case words from the idea. Keep the name in every later round.

```
# Concept <n>: <Name>

Idea: <one sentence; no color word, no typeface name, no effect word>
From: <mined item ids>; reframe: R<n>; seed: S<n>
Category: easy | delightful | long shot

## Why this subject
<two or three sentences: which mined items it uses and what a newcomer would learn>

## Axes
Composition logic: <class>: <value>
Type voice: <class>: <value>
Color logic: <class>: <value>
Image source: <class>: <value>
Motion idea: <class>: <value>
Material metaphor: <class>: <value>
Interaction model: <class>: <value>

## Signature moment
Signature moment: <one sentence a viewer would say>
Pattern: <pattern>; from: <mined item id>
Where: <journey step>; trigger: <what starts it>
Still form: <reduced-motion form, or "does not move">
Checks: retell <pass | fail>; subject <pass | fail>; peak <pass | fail>; no harm <pass | fail>

## Story in three beats
Tension: <the problem in the subject's world>
Turn: <what the work does at the signature moment>
Resolution: <how the person feels and what they do next>

## Tests
Word check: pass
Generic check: pass | brand-required: <pattern, source>
Swap test: <competitor name>: does not fit, because <reason>

## Risk
<the one thing most likely to fail, and how to test it cheaply>

## Handoff to mood-board
Fixed by the concept: <the axes a direction must keep>
Open for the direction: <the axes mood-board may still decide>
```

## 3. `design/concepts/summary.md`

```
# Concepts summary: <subject>

Date: <YYYY-MM-DD>; axis count in force: <n> of 7 (fixed by the design system: <axes or none>)

## Seeds
- S1 <sentence> (from M<n>, R<n>)
- S2 ...
- U1 <the user's own idea, in their words>

## Struck
Struck: S<n> "<seed>"; pattern: generic #<row> or tell <code>; reason: <line>; kept quality: <quality or none>

## Picked
Easy: S<n>; delightful: S<n>; long shot: S<n>

## Axis matrix
<the table from divergence-axes.md, section 3>

## Pair table
<the table from divergence-axes.md, section 4>

## Recommendation
<one concept and one reason tied to the brief, in a separate line>
```

## 4. Decision entry

Append to `design/decisions.md`:

```
## YYYY-MM-DD round <n>: concepts
Stage: explore
Shown: 1 <name>; 2 <name>; 3 <name> (design/concepts/summary.md)
Feedback asked: Which concepts go to mood-board as directions? Keep, change or remove for each.
Keep / Change / Remove: <concept: choice (note)>
Decision: <names> go to mood-board (by <who>) | pending
Rejected: <name>: <reason>
Open: <questions, such as FACT NEEDED items>
Evidence: VERIFIED word check, pair table; UNTESTED any rendered sample
```

## 5. What mood-board and the art director read

- `mood-board` reads `summary.md` for the chosen concepts and gives each one a direction.
- The `art-director` agent reads each chosen concept file. The direction keeps the concept's idea sentence, its fixed axes and its signature moment.
- A direction that drops its concept's signature moment is a new direction. It needs its own concept file.

## Sources

- Principles of Product Design (DesignBetter), ch. 2: a product story before screens, set in the subject's world.
- Designing for Emotion (Aarron Walter), ch. 5: tell a story with a tension, a turn and an outcome.
- Design Collaboration Handbook (DesignBetter), ch. 6: record the picks, the reasons and the rejected options.
