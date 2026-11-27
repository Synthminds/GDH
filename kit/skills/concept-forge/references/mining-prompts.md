# Mining prompts

Read this file at step 3 of `concept-forge`. It holds the seven mining lists, prompts that fill them for each discipline, and how to find the surprising fact.

Mining comes before ideas. A concept that traces to nothing in the subject's world is a style, not an idea. Evidence about the people and the subject comes before any proposed solution (Design Thinking Handbook, ch. 2).

## 1. The seven lists

| List | What goes in it | A good item | A weak item |
| --- | --- | --- | --- |
| Materials | What the subject is made of, handles or produces | "wet clay slip", "carbon-copy receipt paper" | "quality", "innovation" |
| Tools | Instruments, devices, documents and forms people use | "tide table", "torque wrench", "diff view" | "software", "a platform" |
| Rituals | What people do before, during and after, in order | "the barista purges the steam wand before each milk jug" | "people use it daily" |
| Places | Where it happens, in what light, at what hour | "a loading dock at 5 a.m. under sodium lamps" | "online", "anywhere" |
| Vernacular | The words, signs, marks and jokes insiders use | "86 the salmon", "LGTM", "the dog-ear" | the brand words of the brief |
| Tensions | Two needs that pull against each other | "fast service, but no one may feel rushed" | "good, but better" |
| Surprising true fact | One fact a newcomer would not guess, with a source | "the paint below a hull's waterline is there to stop barnacles growing, not for looks" | an invented figure |

Rules:

- Write concrete nouns and verbs. An item a camera could record is a good item.
- Default: three items or more in each list. A list that stays empty is a research gap; name it in `mine.md`.
- Mark each item observed or assumed. Observed means from the brief, the user, the user's files or a named source.
- Keep the user's own words in vernacular. Words that users use for the product are the words to reuse (Principles of Product Design, ch. 1).
- A tension names both sides. It is the best source of a reframe.

## 2. Prompts for every subject

Ask yourself these, then ask the user the ones the brief cannot answer. ASK one question at a time.

- What would a camera see in the first minute of use, and in the last?
- What does the work leave behind: a stain, a stamp, a file, a sound, a receipt?
- What do insiders carry in their pockets or on their desks?
- What goes wrong most often, and how do insiders talk about it?
- What do people do the moment before they need this? The moment after?
- What would a newcomer misread? What would an expert notice at once?
- Which object in this world is older than the product? Which is newer?
- What is the subject's slowest moment, and its fastest?
- Where is it quiet? Where is it loud?

## 3. Prompts by discipline

| Discipline | Extra prompts |
| --- | --- |
| Brand and logo | What mark do insiders already make by hand: a tally, a stamp, a signature, a knot? What shape recurs in their tools? What would the product sign its name with? |
| Typography | Where does this subject's lettering already live: engraved plates, stencils, receipts, chalkboards, labels, screens? Who wrote it, with what tool? |
| Color | What colors does the subject's world hold at the hour of use, and why: safety marking, a material's natural tone, a stain, a uniform? Name each by its object, not its hue |
| Website | What does a visitor need to believe in the first view? What does the subject show at a counter, in a shop window or on a notice board? |
| App | Which ritual does the app join or replace? What step do people repeat? Where do their hands and eyes rest during it? |
| Dashboard | What does the operator glance at between tasks today: a wall clock, a whiteboard, a gauge? Which number changes a decision, and which only reassures? |
| Data viz and infographic | What physical analog does the data have: a ledger, a tide line, a queue, a pile? What is the one finding a reader must take away? |
| Network graph | What are the real links between things, and who draws them today? Which node would an insider point to first? |
| Motion and video | What moves in the subject's world, and at what pace: a pour, a press, a tide, a scroll? What has a natural start and stop? |
| 3D | Which object would a viewer want to pick up and turn? What surface, weight and wear does it have? |
| Design system | Which parts of the brand recur across every product? Which rituals repeat across screens? What would a new team member need to recognize at once? |

## 4. The surprising true fact

The fact is the seed most likely to produce an idea no competitor has. It must be true.

1. Look in the brief, the user's files, `DESIGN.md` and the product's own data first.
2. ASK the user: "What does a newcomer get wrong about this?" and "What surprised you when you started?"
3. When a web source is available and the user accepts it, read one primary source. Record its title or address in `mine.md`.
4. Write the fact in one sentence, with its source.
5. With no source, write `[FACT NEEDED]` and one question that would find it. Never write a figure you cannot source (kernel rule 11).

A good fact changes how a newcomer sees the subject. A statistic about market size is rarely a good fact; it says nothing about the subject's world.

## 5. Reframes

Write three reframes after the lists. A reframe changes the problem so that new ideas open up.

Forms:

- How-might-we: "How might we <verb> <a mined tension> for <the audience>?" One question covers part of the problem, not all of it (Design Thinking Handbook, ch. 4).
- Point of view: "<A specific person> needs a way to <need, with no product or format word>, because <insight from a mined item>." Add how they should feel when the need is met (Design Thinking Handbook, ch. 3).
- Zoom: write one reframe a level wider (the goal behind the request) and one a level narrower (a sharp sub-problem).

Rules:

- Drop the format the brief names. "A landing page that ..." caps the solutions; "a way for a first-time visitor to trust ..." does not.
- Each reframe cites one mined item or tension.
- Name the reframe you expect the user to prefer, and why, in a separate line.

## 6. Worked example

Brief: a cooperative ferry service wants a timetable site. Audience: commuters and visitors. Brand words: steady, local, frank.

- Materials: tarred rope (M1), salt-stained timetable boards (M2), paper ticket stubs with a punched hole (M3).
- Tools: the harbor master's chalk departure board (M4), the deckhand's tide table (M5), the horn signal (M6).
- Rituals: the crew counts bikes onto the lower deck (M7); regulars stand in the same spot on the pier (M8).
- Places: the pier at dawn in fog (M9); the cabin window during the crossing (M10).
- Vernacular: "the late boat" for the last run (M11); "she's on the slip" for a boat under repair (M12).
- Tensions: exact times, but the sea sets the real pace (M13); visitors want a view, commuters want a clock (M14).
- Fact: crew members own the cooperative and vote on the timetable each spring (M15; source: the user's founding document).

Reframes:

- How might we make the sea's delay as plain as a clock time (M13)?
- A regular commuter needs to know before leaving home whether the late boat runs, because the chalk board is the only live source today (M4, M11). They should feel calm, not hurried.
- Wider: how might the site carry the cooperative's vote into every timetable (M15)?

## Sources

- Design Thinking Handbook (DesignBetter), ch. 2: evidence before solutions, extreme users, feelings as well as tasks; ch. 3: point of view, reframing, zoom out and in; ch. 4: how-might-we questions.
- Principles of Product Design (DesignBetter), ch. 1: reuse the words users use.
- Anthropic frontend-design skill: ground the design in the subject's world.
