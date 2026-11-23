# Dynamic and time-based networks

Read this file at step 13 of `network-graph`. It covers when to add time, the two kinds of dynamics, data needs, encoding change, the time unit, display modes, fixed positions, the time control, spread stories, the static time-lapse report and failure patterns.

Evidence. All rules come from Cherven (2015), chapters 4, 8 and 10, except the reduced-motion rules, which come from the GDH kernel and the `ui-motion` skill. Numbers are the book's examples; treat them as defaults.

## 1. Add time only when it earns its place

- Ask: how many nodes or edges appear, disappear or change value per time step in the period shown?
- "Few or none": stay static. Time adds complexity and little insight to a slow network.
- "Many, and the change is the story": add time.
- When you drop time, say so in the plan: "Timestamps present; dropped because the network changed little in 2024."

## 2. Name the kind of dynamics

| Kind | What changes | Question it answers | Data it needs |
| --- | --- | --- | --- |
| Topology | Nodes and edges appear and leave | How did the network grow, move, shrink? | A start on every element; an end when elements leave |
| Attribute | Values on fixed nodes and edges change | How did each node or tie change? | A value per element per time step |
| Both | Structure and values | Network-level and node-level change together | Both |

Write one of "dynamic topology", "dynamic attributes" or "both" in the plan, with the question.

## 3. Data rules

- Every dynamic element has a start time. Elements that leave have an end time; an empty end means "still present".
- Time fields are numbers, dates or timestamps, never text.
- Period snapshot files share one schema, keep the same `id` for the same entity, and carry a strictly later timestamp each.
- For attribute dynamics, check that the change is visible after mapping. Compute each node's range across time steps as a share of the global range. When the median share is tiny, use a finer time unit, another field, or a static before-and-after view. The book's monthly airline example changed too subtly to see.

## 4. Encode change

| Change in | Channel | Example |
| --- | --- | --- |
| Stature (a quantity) | Node size | Passenger volume per airport |
| Status (a category or bounded score) | Node color | Susceptible, infected, removed |
| Relationship strength | Edge width | Carriers per route |

Rules:

- Recompute size and color at every time step. An encoding applied once does not follow the data. Test it: scrub to two times where a known node differs, and see its size or color change.
- In code, the style function reads the value for the current time, not a cached value.
- One legend covers every state across all frames.

## 5. Choose the time unit

- Match the unit to the event rate and the story: minutes or hours for a spreading hashtag, months for airline traffic, days for a school term.
- During playback, an element should stay visible for several frames. When most elements blink for one frame, coarsen the unit or switch to cumulative mode. Raw 20-second contacts in the book's school data flickered and entertained more than they informed.
- Write the unit and the reason in the plan.

## 6. Choose the display mode

| Mode | Shows | Rule |
| --- | --- | --- |
| Active in window | Current activity | Edge count rises and falls |
| Cumulative since start | How patterns build and where ties repeat | Edge count never falls |

Label the mode on the control or in the caption: "active in window" or "cumulative since start".

## 7. Fix positions for comparison

- Compute the layout once on the full network, then play time over it. A node present in two frames sits at the same coordinates in both.
- Hide edges while computing the full layout when they slow it; show them for the frames.
- A live layout during playback suits exploration only. The page must then say that positions move.

## 8. The time control

- The scrubber runs left to right, earliest at the left. For a right-to-left locale, confirm the direction with the user.
- Controls: play and pause, speed (or step delay), and a time window with two movable ends. Pausing keeps the current frame.
- The time window acts as a filter and combines with other filters. With a period set, a category filter returns the intersection, and the shown counts update. The book narrowed 1,668 nodes to 777 by period, then to 101 with a category condition.
- Accessibility: every control works by keyboard and has a visible label. Under reduced motion, nothing plays by itself. Offer step buttons (previous, next) beside play.
- Show the current time as text near the graph, and the node and edge counts for the frame.

## 9. Report time-series statistics

- Per time step: node count and edge count. Where useful: average degree, components, clustering coefficient, density, diameter, average path length.
- Chart them as small multiples on one shared time axis, same chart type, same order (`data-viz` builds them). Default: four to six measures.
- Keep no-data periods in their slot on the axis, in neutral gray, with a note. Never drop them and never plot them as zero.

## 10. Spread stories (contagion and diffusion)

1. Fix the network and its layout.
2. Write the rule: states, transmission probability or adoption threshold, duration of each state, time step, cumulative or not. The book used probabilities of 0.3, 0.5 and 0.7 and an adoption threshold of one third of neighbours.
3. Mark the seed nodes at the start.
4. Produce one frame per time step. Keep positions fixed; change only state color.
5. Caption each frame with the count of nodes in each state.
6. Close with what the structure did to the spread: "Low-contact nodes stopped the spread in two of three runs."
7. State the rule beside the graphic. Without it, the picture cannot be read or reproduced.

## 11. The static time-lapse report

A static file cannot play. It must carry the whole story.

1. Agree the display mode and the snapshot boundaries with the user. Choose boundaries that mean something in the domain: end of each day, each quarter, each release.
2. Compute the layout once on the full network. Size by degree with a moderate range. Color by the formal grouping.
3. Export one image per boundary with identical framing.
4. Record the structure measures at each boundary.
5. Chart the measures as small multiples on one page. Gray out no-data periods.
6. Write the narrative: what built up, when the big changes happened, which groups mix and which do not. Mark any cause as a hypothesis.
7. Add callouts on the snapshots where the named changes occur.
8. Caption each snapshot with its boundary: "End of day 1".
9. Review: the user reads the report without any interactive tool and says what story they got. Revise when it differs.

## 12. Motion rules

- Default: each frame stays long enough to read the change and its count; give the viewer speed control.
- No autoplay under reduced motion. Offer the static snapshots as the reduced-motion form.
- Animate color and opacity between states; do not animate positions in a comparison view.
- Nothing flashes more than three times a second.

## 13. Checklist

- [ ] The plan says why time is needed and names the kind.
- [ ] Every element has a start; ends exist where elements leave; time fields typed.
- [ ] Changing fields mapped: stature to size, status to color, strength to width.
- [ ] Size and color update per step (tested on a known node).
- [ ] Time unit justified; elements stay visible long enough to read.
- [ ] Display mode labelled.
- [ ] Positions fixed for comparison.
- [ ] Control: left to right, play, pause, speed, two-ended window, keyboard, no autoplay under reduced motion.
- [ ] Time window combines with other filters.
- [ ] Counts per step reported; no-data periods grayed and explained.

## 14. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Time for show | An animated graph of a network that barely changes | Static graph plus a before-and-after pair |
| Moving positions | Nodes jump between frames; nothing can be compared | Layout once on the full network |
| Flicker | Edges blink on for one frame | Coarser unit or cumulative mode |
| Stale encoding | Sizes frozen at the first frame | Recompute per step; test on a known node |
| Missing rule | A spread animation with no probability or threshold | State the rule beside the graphic |
| Gaps read as findings | Weekends plotted as zero activity | Gray the slot and explain it |
