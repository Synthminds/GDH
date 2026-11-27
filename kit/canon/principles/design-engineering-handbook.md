# Design Engineering Handbook (InVision DesignBetter)

Book id `design-engineering-handbook`, id prefix `P-DEH`. 29 principles, 6 of them gates. The machine-readable copy is in [principles.json](../principles.json); this file matches it word for word.

Gates: P-DEH-05, P-DEH-11, P-DEH-12, P-DEH-14, P-DEH-24, P-DEH-25.
Every other principle is a default. Query them with the `design-principles` skill.

## Chapter 1: Introducing design engineering

**P-DEH-01 Give the design-code seam an owner.** Name who owns the overlap between design and code for this project, with its concrete duties such as tokens, component docs and preview builds. Test: The handoff plan lists each seam duty with one owner.

## Chapter 2: The design engineering process

**P-DEH-02 Answer the four product questions.** Answer four questions for every piece of work: does it solve a real user problem, can users work it out, can it be built with the time and stack available, and does it help the business. Test: The brief or review note holds an explicit answer to each of the four questions.

**P-DEH-03 Separate fit from build quality.** Give two separate verdicts on any deliverable: whether it is the right solution for the problem, and whether it is built well. Test: Each review holds one verdict on problem fit and a separate verdict on build quality.

**P-DEH-04 Follow research over stakeholder taste.** When research and a stakeholder's direction conflict, follow the evidence and say openly that you did. Test: Every decision that departs from stated direction cites its evidence in the decision record.

**P-DEH-05 Write a prototype purpose statement.** Before building a prototype, write which problem it explores or validates, for which user, and the hypothesis it tests. Test: The prototype header holds a filled purpose, user and hypothesis.

**P-DEH-06 Distrust the first solution.** Treat the first solution as the weakest one and branch into alternatives before choosing. Test: At least two distinct directions exist before one is chosen, and each dropped one has a recorded reason.

**P-DEH-07 Carry forward from failed branches.** When a direction fails, name the cause and carry what worked into the next version instead of discarding it whole. Test: Each rejected direction has a cause of failure and a note on what carried forward.

**P-DEH-08 Raise fidelity with confidence.** Match fidelity to confidence: sketch while many answers are possible, wireframe as they narrow, and code an interactive build only once the direction is agreed. Test: No coded and styled prototype exists for an idea that has no agreed direction.

**P-DEH-09 Pick the prototype by question.** Choose the prototype kind by what you must learn: a clickable static build for structure and flow, real content for content questions, and code for interaction, motion and responsiveness. Test: The purpose statement names a question and the prototype kind matches it.

**P-DEH-10 Layout in boxes before content.** Validate layout and flow with box-level wireframes that only label the content type in each region before adding detailed content. Test: A box-level version of each key screen exists and predates the detailed version.

**P-DEH-11 No placeholder copy at high fidelity.** Use real or realistic copy in every high-fidelity artifact. Test: A search of the high-fidelity artifact finds no lorem ipsum or generic filler strings.

**P-DEH-12 Mock data in shared prototypes.** Use mock data, not real personal data, in any prototype that others will see. Test: The shared prototype's data holds no real names, email addresses or account numbers without a recorded approval.

**P-DEH-13 Look at the data first.** Explore the real data's range, variance and shape before choosing a chart. Test: The design note states range, variance and shape, and the chart choice cites them.

**P-DEH-14 Test charts on hard data.** Render every chart with real or realistic data, including a low-variance case, an empty case and an extreme case, before it ships. Test: Captures exist for each chart with realistic, flat, empty and extreme data.

**P-DEH-15 Mark undecided regions as placeholders.** Put a plain marked placeholder in any region of a prototype that is still undecided, and list it as an open question. Test: Every undecided region is visibly marked and appears in the open-questions list.

**P-DEH-16 Spike risky parts early.** Build a small working spike for any element with unclear feasibility, such as heavy motion, 3D, live data or a new interaction, before promising it. Test: Each element flagged as risky has a working spike dated before the commitment.

**P-DEH-17 Design and build in handshake.** Run design and build in parallel with repeated sync points instead of a single transfer at the end. Test: The project log shows more than one design-to-build sync point before delivery.

**P-DEH-18 Write outcomes per user type.** Write the intended outcome for each type of user, tied to a pain point, and report each with a measured value after launch. Test: The success list has one row per user type, each linked to a pain point.

## Chapter 3: Engineering collaboration

**P-DEH-19 Agree the shared vocabulary.** Agree a glossary so that design files and code use the same name for the same thing. Test: Five sampled terms have the same name and meaning in the design files and in the code.

**P-DEH-20 Write a new-or-reuse test.** Write down when a need justifies a new component and when it must reuse an existing one, and cite that test for every new component. Test: Every new component in a change cites the new-or-reuse test and the search result.

**P-DEH-21 Turn repeat fixes into rules.** When the same correction happens twice, add a rule, check or shared component so a third manual correction is not needed. Test: No correction appears three times in the review log without a matching rule or component.

**P-DEH-22 Refuse with an alternative.** When declining a request on feasibility or quality grounds, state the constraint and offer at least one workable alternative. Test: Each refusal in the session names the constraint and gives at least one alternative.

## Chapter 4: Design engineering organizational models

**P-DEH-23 Learn constraints before proposing.** As an outsider to a product, collect its technical and operational constraints by asking before you assume them. Test: The brief marks each constraint as stated, found in the project or assumed.

## Chapter 5: Design engineering leadership

**P-DEH-24 Name the quality bars explicitly.** Report accessibility, responsiveness, performance and internationalization as separate lines in every UI review, even when the brief does not ask. Test: The review record holds one result line per bar.

**P-DEH-25 Label prototype or production.** Label every code artifact as prototype or production, and never ship prototype code without passing the production checks. Test: Every delivered code file carries a prototype or production label.

**P-DEH-26 One edit changes one value.** Build prototypes so that changing one design value, such as a speed, color, size or line of copy, takes one edit in one place. Test: Changing one sampled value in the prototype takes exactly one edit.

**P-DEH-27 State cuts made for speed.** When a deadline forces a cut, list what was cut and the quality it costs instead of trading quality away silently. Test: Every cut made for time appears in the handoff with its cost.

## Chapter 6: A design engineering manifesto

**P-DEH-28 Extract a reusable tool afterward.** After solving a task, extract the component, script, template or rule that would solve it next time, or record why not. Test: The project close note names an extracted reusable item or a reason for none.

**P-DEH-29 Fit the process to the need.** When a step of the process does not fit the task, say so, adapt or skip it, and record the reason. Test: Each skipped or adapted step has a recorded reason.

Sources: Design Engineering Handbook (InVision DesignBetter); Chapter 1: Introducing design engineering, Chapter 2: The design engineering process, Chapter 3: Engineering collaboration, Chapter 4: Design engineering organizational models, Chapter 5: Design engineering leadership, Chapter 6: A design engineering manifesto. Paraphrased in the kit's own words; no sentence is quoted.
