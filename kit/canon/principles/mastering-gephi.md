# Mastering Gephi Network Visualization (Packt, 2015)

Book id `mastering-gephi`, id prefix `P-GEPHI`. 28 principles, 11 of them gates. The machine-readable copy is in [principles.json](../principles.json); this file matches it word for word.

Gates: P-GEPHI-01, P-GEPHI-03, P-GEPHI-04, P-GEPHI-10, P-GEPHI-12, P-GEPHI-15, P-GEPHI-17, P-GEPHI-18, P-GEPHI-20, P-GEPHI-24, P-GEPHI-25.
Every other principle is a default. Query them with the `design-principles` skill.

## Chapter 1: Fundamentals of complex networks and Gephi

**P-GEPHI-01 Confirm the data is relational.** Confirm the data holds relationships, or can be converted into them, before committing to a network graph. Test: The brief names the relationship each edge represents.

**P-GEPHI-02 Several centralities before importance.** Call a node important only after more than one centrality measure agrees, and pick the measure that matches the question. Test: Every claim that a node is important cites at least two measures or a measure matched to the question.

**P-GEPHI-03 Layout never changes the statistics.** Read structure from computed statistics, and remember that moving nodes changes only the picture. Test: Each structural claim in the caption is backed by a computed statistic.

## Chapter 2: A network graph framework

**P-GEPHI-04 One purpose per graph.** State one purpose for the graph, whether to inform, to persuade, to teach or to delight, for one audience and one story, before touching the data. Test: The brief holds one purpose sentence naming audience and story.

**P-GEPHI-05 Decide static or interactive first.** Choose static or interactive delivery, and where it will be shown, before choosing a layout, and plan annotation up front for static work. Test: The brief names the delivery format and, for static work, the planned title, legend and callouts.

**P-GEPHI-06 Nodes and edges as tables.** Model the data as a node table and an edge table, with direction, weight and the grouping and ranking fields stored as data rather than as manual styling. Test: Color, size and group encodings in the graph all trace to named data fields.

## Chapter 3: Selecting the layout

**P-GEPHI-07 Bake off several layouts.** Test several layouts on the real data before picking one, and never accept the first run. Test: The record holds renders of several layouts on the real data and the reason for the winner.

**P-GEPHI-08 Layout family follows structure.** Pick the layout family from the data and the story: force-directed to discover structure, circular or concentric for a meaningful order or one subject, layered for multipartite data, geographic only when location is the story. Test: The decision record ties the chosen layout family to a property of the data or the story.

**P-GEPHI-09 Tune one force at a time.** Tune a force layout one setting per iteration, spacing first, keep a render of each step, and stop when an iteration brings no visible gain. Test: The tuning log changes one setting per step with a render each time.

**P-GEPHI-10 A hairball is a defect.** Treat an unreadable tangle as a defect to fix with filtering, layering or partitioning, not as a finished result. Test: No published view is an unreadable tangle, and each fix is logged.

**P-GEPHI-11 Edges whisper, nodes speak.** Reduce edge visual weight so that edges recede and nodes carry the reading. Test: At the target size, node groups are distinguishable through the edges.

**P-GEPHI-12 Never trade honesty for looks.** Style a graph only to make its meaning clearer, and do not publish a view whose structure cannot be shown honestly. Test: A reviewer finds no styling choice that hides or implies a relationship the data lacks.

## Chapter 4: Network patterns

**P-GEPHI-13 Classify the structure first.** Classify the network as random, hub and spoke, small world or clustered before designing its view. Test: The design notes name the structure type and the evidence for it.

**P-GEPHI-14 Spread rules beside spread graphics.** Show change over time as snapshots that share one layout and one legend, and state the spread rule and time step next to them. Test: Every spread graphic states its rule and time step and every snapshot shares one layout.

## Chapter 5: Working with filters

**P-GEPHI-15 Say what was filtered out.** Tell the viewer what a filter removed, and recompute statistics on the filtered subgraph when a claim is about it. Test: Every filtered view states its filter in the caption.

**P-GEPHI-16 Several small views beat one.** Prefer several small filtered views, such as an ego network, the most connected nodes and in-group versus cross-group edges, over one view of everything. Test: The deliverable answers its questions with focused views rather than one dense overview alone.

## Chapter 6: Graph statistics

**P-GEPHI-17 Components before distance measures.** Count connected components and report the giant component's share before running distance measures or reading the picture as one network. Test: Any reported diameter or path length follows a stated component count.

**P-GEPHI-18 State every score's direction.** Write down the direction of every score before mapping it, and run a numeric ramp from light for low to dark for high. Test: Each numeric encoding's legend states which end is high.

## Chapter 7: Segmenting and partitioning a graph

**P-GEPHI-19 Segment by data type.** Encode a categorical attribute with distinct colors, a numeric attribute with size or a ramp, and use an algorithmic clustering only when no attribute fits. Test: Every encoding in the graph matches the type of its source field.

**P-GEPHI-20 Scale area, not radius.** Scale node area to the data value, give the smallest node a visible size and cap the largest so it does not hide its neighbors. Test: Node sizes are proportional to value by area, with a visible minimum and a cap.

**P-GEPHI-21 Highlight one group, gray the rest.** Direct attention to the story subset by changing two channels, such as color and size, for that group and leaving every other node neutral. Test: Only the story subset carries the highlight, and the rest of the graph is neutral.

**P-GEPHI-22 Clusterings are one reading.** Run a clustering at several settings, reject over- and under-segmented results, and present the chosen one as one reading with its method in the caption. Test: The caption names the clustering method, and the record shows several settings compared.

## Chapter 8: Dynamic networks

**P-GEPHI-23 Time only when it changes.** Add a time dimension only when the network changes often within the period shown, and fix node positions before comparing steps. Test: A dynamic graph shows visible change between steps and keeps node positions fixed.

**P-GEPHI-24 Gaps stay visible.** Gray out periods with no observations instead of dropping them or plotting them as real values. Test: Periods with no data are marked as gaps in every time view.

## Chapter 9: Taking your graph beyond Gephi

**P-GEPHI-25 Legend says node, edge, color.** State in every network legend what a node is, what an edge means and what color encodes, and give the graph a title, credit and short description. Test: Every published network graph names its node, edge and color meanings and has a title.

**P-GEPHI-26 Interactive graphs focus on demand.** On hover or select, dim everything except the node and its neighbors, reveal labels by zoom level, and provide search when the network is large. Test: Selecting a node dims non-neighbors and labels appear in order of importance as the viewer zooms.

**P-GEPHI-27 Vector master for print.** Keep a vector master of any network that will be edited, annotated or printed, and finish static versions with title, callouts and labels outside the graph tool. Test: A vector master exists for each printed or edited network graph.

## Chapter 10: Putting it all together

**P-GEPHI-28 Static graph carries whole story.** Make a static network deliverable carry the full story through snapshots, supporting statistics, a narrative and callouts. Test: The static deliverable includes snapshots, statistics, narrative and callouts.

Sources: Mastering Gephi Network Visualization (Packt, 2015); Chapter 1: Fundamentals of complex networks and Gephi, Chapter 2: A network graph framework, Chapter 3: Selecting the layout, Chapter 4: Network patterns, Chapter 5: Working with filters, Chapter 6: Graph statistics, Chapter 7: Segmenting and partitioning a graph, Chapter 8: Dynamic networks, Chapter 9: Taking your graph beyond Gephi, Chapter 10: Putting it all together. Paraphrased in the kit's own words; no sentence is quoted.
