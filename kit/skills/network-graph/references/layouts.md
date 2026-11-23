# Layouts: selection, parameters and the bake-off

Read this file at steps 6 to 8 of `network-graph`. It covers the seven shortlist questions, the layout selection table by graph size and structure, parameter defaults with reasons, the tuning loop, the bake-off, reproducibility, framing and failure patterns.

Evidence. The shortlist questions, the selection table rows, the tuning loop and the acceptance tests come from Cherven (2015), chapters 2 and 3. Parameter values are the book's 2015 tool defaults and examples, or tutorial starting points found by search. The mapping to code libraries is GDH's translation, not the book's. Every number is a default to test, never a gate.

## 1. Seven shortlist questions

Answer each in `network-plan.md` before you pick candidates.

1. Goal: show relationships, show divisions, show geography, or rank by an attribute?
2. Size class: small, medium, large or very large? (See `when-a-graph.md`.)
3. Density: sparse (edges per node near or below 1) or dense?
4. Expected clusters: shared location, employer, affiliation, topic?
5. Levels: single-level, bipartite or multipartite?
6. Time: does the story need change over time?
7. Delivery: static or interactive?

## 2. Map the answers to families

| Answer pattern | Family to shortlist |
| --- | --- |
| Discover structure, no fixed order | Force-directed |
| Small, with a meaningful order | Circular |
| One subject node | Concentric (ego) |
| A few key nodes against the rest | Dual circle |
| Known groups, and a force layout gives a hairball | Radial axis or hive plot |
| Directed, no cycles, levels matter | Hierarchical (tree or DAG) |
| Node types in tiers | Layered or multipartite |
| Coordinates matter | Geographic |
| Thousands of nodes or more | Fast force method plus filters and interaction |

Pick three or more candidates from different families when you can: one force-directed, one circular or radial, one focus or layered.

## 3. Selection table

Rows marked (B) restate the book's comparison of layout algorithms. Rows marked (G) are GDH synthesis to test.

| Graph size and structure | Layout | Parameter defaults to start from | Why | Avoid when | Basis |
| --- | --- | --- | --- | --- | --- |
| Small to medium, structure unknown, general view | Fruchterman-Reingold (classic force) | Area sized to the canvas; gravity low; run until stable | Accurate and easy to read | Large graphs: slow; sparse hubless graphs: hairball | B |
| Small to medium, quick first look | Yifan Hu, or Yifan Hu Proportional | Relative strength 0.2 (higher spreads nodes); optimal distance from node size | Fast; stops itself through adaptive cooling | You need separate attraction and repulsion controls | B |
| Small to medium, discovery, time available | Force Atlas (separate forces) | Repulsion, attraction and gravity set apart; adjust by sizes on | Many controls, high accuracy | Large graphs: very slow | B |
| Medium to very large, pattern detection | ForceAtlas2 | Scaling near 100 to start (tutorial value); gravity low; prevent overlap last; edge weight influence 1 | Fast on large graphs; groups show as regions | Top accuracy matters most | B |
| Large, overall structure fast | OpenOrd | Raise edge cut for more white space between clusters | Very fast on large graphs | Small graphs: coarse | B |
| Very large, speed over quality | Multilevel force (Yifan Hu Multilevel) | Defaults; check coarse areas by eye | Very fast | Quality matters | B |
| Small, meaningful order (cluster, size, rank) | Circular | Order by community, then by size; clockwise for ordered data | Simple and readable | Many nodes or edges: crossings pile up | B |
| Small world (short paths, no hubs) | Circular ordered by group | Group order from community id | Force layouts tend to hide small-world patterns | Medium or large graphs | G |
| One focus node, small diameter | Concentric by hop distance | Focus set by id; wide ring spacing when the farthest node is about 3 hops, tight at 6 or 7 | Shows how close everything is to one node | Large diameter: rings explode | B |
| A focus group in a larger graph | Dual circle | Inner ring holds the top N by a stated measure | Isolates the focus group | Very large graphs | B |
| Clustered, story about links across groups | Radial axis | One axis per group; order on the axis by a measure | Cross-group edges stay visible | Large graphs; stories inside one group | B |
| Dense hairball, groups known | Hive plot | Axes = groups; position on axis = a measure | Spreads connections, cuts central clutter | You need links inside one axis | B |
| Hierarchy, top-down levels, no cycles | Tree or DAG | Levels from depth; minimise crossings | Orders hierarchical data | Cyclic data such as "who talks to whom"; very large | B |
| Two or more node types, links between tiers | Multipartite or layered | One layer per type; order within layers to cut crossings | Minimises crossings for tiered data | You need fine styling control | B |
| Sparse or bipartite, small to medium, needs white space | ARF | General attraction 0.2; lowering it toward 0.1 spreads the graph a lot | Rounder shape; easy to read; the book chose it for a 350-node bipartite network | Not stated | G |
| Nodes carry coordinates | Geographic | State the projection | Readers read position as place | No coordinates | B |
| Crowded graph with natural layers | 3D splitter or isometric | z axis = a named attribute; rotation available | Adds a dimension to separate layers | You must compare positions or see all at once | B |

Rules:

- The chosen layout comes from a row whose first column matches the graph. Write a reason for any exception.
- Do not use a grouped layout (radial, circular by attribute) when the story is the overall topology. It hides the cross-network structure.
- Do not use a tree for cyclic data.
- Use a fast or approximate method only for large graphs, or when a slower method failed the time budget. On small graphs its coarseness shows.
- Avoid 3D unless the third axis encodes a named attribute and the viewer can rotate. 3D hides nodes behind nodes.

## 4. The three forces

Every force-directed layout balances three controls.

| Control | Raise it when | Lower it when |
| --- | --- | --- |
| Attraction (linked nodes pull together) | Clusters do not separate (raise with repulsion) | Unrelated nodes clump; peripheral nodes do not move out |
| Repulsion (all nodes push apart), or the scale setting | The centre is a dense knot | The graph flies apart |
| Gravity (pull toward the centre) | Small components drift off the canvas | The centre is crowded |

Two more switches:

- Overlap prevention: turn it on last, after the shape settles, so big nodes stop covering small ones.
- Edge weight influence: 0 ignores weight, 1 is normal, above 1 amplifies. If edge width shows weight, the layout should use weight too.
- Hub dissuasion (where offered) pushes hubs outward and gives their neighbours room.

Code mapping (GDH translation; confirm in the library's own documentation):

| Concept | D3 force simulation | graphology ForceAtlas2 (Sigma.js stack) | Cytoscape force layouts |
| --- | --- | --- | --- |
| Attraction | link strength and distance | edge weight influence | ideal edge length, edge elasticity |
| Repulsion | many-body strength (negative) | scaling ratio | node repulsion |
| Gravity | centering forces | gravity | gravity |
| Overlap prevention | collision force, radius = node radius plus padding | adjust sizes | node overlap or padding options |
| Stopping | alpha decay and minimum alpha | iteration count | iteration count or animation off |

## 5. The tuning loop

1. Run the layout with defaults on the real data. Save the render and the settings.
2. Name the main defect: crowded centre, overlaps, clusters not separated, too many crossings, components lost off canvas.
3. Change one setting to fix it. Spacing first (repulsion or scale), then attraction, then gravity, then the grouping or ordering attribute.
4. Save the render with its settings. One changed parameter between consecutive renders.
5. Stop when two changes in a row bring no visible gain.
6. Turn on overlap prevention. Save the final render.

When patterns exist but clutter hides them, tune spacing before you drop the layout. Clutter in a dense graph is often a settings problem.

## 6. The bake-off

1. Pick three to five candidates from section 3.
2. Give each the same canvas size and the same time budget. The book gave slow layouts ten minutes each; a fast one finished in about two.
3. Run the tuning loop on each.
4. Score each best render against the acceptance tests in section 7.
5. Write one line per loser: "Radial: clean, but groups links by attribute and hides the overall topology."
6. ASK: show the best render of each side by side, with one line on what each shows well and badly. Let the user choose. Record the choice and reasons in `design/decisions.md`.

## 7. Acceptance tests

Run all four on each candidate at delivery size. Pass only with a recorded answer to each.

1. Story: can you state the story in one sentence from the render alone? If not after tuning, change the layout.
2. Clutter: are real patterns hidden by clutter? Adjust the forces before anything else.
3. Hairball: is it a dense mass where named edges cannot be traced end to end? Plan a filter, a layer split or a partition (see `encoding-and-filtering.md`).
4. Format: is it interactive? It may carry more nodes, but its default view must pass tests 1 to 3 as a still image.

Build focus in this order before styling: lay out the graph, enlarge and recolor the subject node, color its direct neighbours, stop and review with the user. Only then add labels, paths and edge colors.

## 8. Reproducibility

- Fix the random seed. Record the algorithm, its version, every parameter and the iteration count or stop rule.
- Keep the final positions in the styled graph file. A re-run of a force layout gives a different picture.
- For a web page, compute the layout once (offline or on load with a fixed seed), then stop the simulation. A layout that jitters at rest costs battery and attention.
- Record the node count the layout was tested at. Re-test when the count grows about five times.

## 9. Framing

- Rotate and scale the finished layout: orientation is free. Put the featured cluster in a strong position, not clipped and not behind the legend.
- Use most of the canvas without touching its edges.
- Keep disconnected components inside the frame. Pack small components along one side, or show the largest component and state the rest.
- Expect a styling pass after layout. No algorithm produces a finished graphic.

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| First run shipped | One layout, default settings | Bake-off of three or more; tuning loop |
| Tree forced on a network | A hierarchy drawn for "who talks to whom" | Use a force or radial layout; trees need acyclic data |
| Grouped layout for a topology story | Clean rings, no overall structure | Force-directed or geographic |
| Endless physics | Nodes keep drifting in the page | Stop rule; compute once; freeze positions |
| Five knobs at once | Nobody knows which change helped | One parameter per render |
| 3D for depth's sake | Nodes hidden behind nodes | 2D unless z encodes a named attribute |
| Layout tuned at the wrong size | Fine on a large monitor, a knot on a phone or slide | Tune at the delivery size |
