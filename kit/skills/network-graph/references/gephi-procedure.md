# Desktop graph tool procedure (Gephi)

Read this file at step 15 of `network-graph`, when the user runs Gephi or a similar desktop graph tool. It turns the method of the other reference files into tool steps: workspace order, import, statistics, layout, filters, partition and ranking, time, preview and export.

Evidence. Every step comes from Cherven (2015), written against Gephi 0.8.2 and its 2015 plugin set. Menu paths, panel names, plugin names and default values were not checked against a current release. Label every step UNTESTED until the user confirms it in their installed version. Gephi is not in the GDH tool catalog: the user runs it on their machine, and the agent guides and checks.

## 0. Before you start

- Ask the user for the installed version. Read its own documentation for any step that fails.
- List the plugins a recipe needs (ARF, Concentric, Radial Axis, clustering plugins, exporters). Confirm each exists for that version, or name the fallback: a core layout, a core statistic, or code.
- Prepare the node and edge tables outside the tool first (`data-preparation.md`). The tool is a weak data editor.
- Keep a work log: one line per action, with settings and counts.

## 1. Work in the tool's three areas, in order

1. Data table area (Data Laboratory): load and inspect the tables.
2. Overview: layout, statistics, filters, partition and ranking styling.
3. Preview: final rendering settings and export.

Styling set in Overview carries into Preview and export.

## 2. Import

1. Name the columns as the importer expects: nodes `Id`, `Label` plus attributes; edges `Source`, `Target`, `Type` (Directed or Undirected), optional `Weight` and `Label`.
2. Import the node file first, then the edge file. Edges loaded first create a bare node table that is hard to update.
3. Set each column type at import. Numbers imported as text cannot be ranked. In the book's version, a BigInteger column could not drive ranking; copy it to Integer.
4. Graph files (GEXF, GraphML, GML, Pajek, Tulip) open directly from the File menu.
5. Compare node and edge counts with the source. A drop means a key or parse problem.

## 3. First look

1. Run any force layout briefly to see the raw shape.
2. Record counts, sparse or dense, components, visible clusters or hubs (`when-a-graph.md`, section 6).

## 4. Statistics

1. Run each statistic from the Statistics panel before you filter, color or size by it. Its column appears only after the run.
2. Answer "directed or undirected" when the dialog asks, to match the data.
3. Tier 1: average degree, network diameter (also gives betweenness, closeness, eccentricity), graph density, connected components, average path length.
4. Tier 2: degree or in and out degree, eigenvector centrality, HITS, PageRank where offered.
5. Tier 3: modularity (with a resolution value), clustering coefficient, and plugins for other clustering methods.
6. Record each result and the version in the statistics block (`statistics.md`, section 9). Check the direction of closeness in this version before you map it.
7. When statistics fail on a large graph, raise the tool's memory limit in its configuration file, or fall back to degree-based measures.

## 5. Layout

1. Shortlist with `layouts.md`. Run each candidate with defaults, then tune one setting at a time.
2. Force-based layouts in the book's version:
   - Force Atlas: separate repulsion, attraction and gravity; "adjust by sizes" prevents overlap. Accurate, slow.
   - ForceAtlas2: one Scaling setting for repulsion, Gravity, Prevent Overlap, Dissuade Hubs, Edge Weight Influence (0 ignores, 1 normal, above 1 amplifies), thread count.
   - Fruchterman-Reingold: one Area setting, Gravity, Speed. Slow; gave a hairball on a sparse graph.
   - Yifan Hu: Optimal Distance, Relative Strength (default 0.2, higher spreads nodes); stops itself. Proportional and Multilevel variants.
   - OpenOrd: five stages (Liquid, Expansion, Cooldown, Crunch, Simmer) that total 100 percent; raise Edge Cut for white space between clusters.
   - ARF (plugin): neighbour attraction (default 3.0), general attraction (default 0.2; 0.1 spreads the graph a lot), repulsion.
3. Focus layouts (Concentric, Dual Circle, plugins): set the focus node by its id. Never let the tool pick it.
4. Radial and circular layouts: order or group by a meaningful attribute, such as the modularity class, not by the default.
5. Finish with the overlap tools: Noverlap or Prevent Overlap for nodes, Label Adjust for labels. Use rotate and expand to frame the graph.
6. Many force layouts run until stopped. Stop when a few more seconds bring no visible change. Save the project.

## 6. Filters

1. Build every filter the same way: drag it from the filter library to the Queries area, set its value, then press Select and Filter.
2. Explore single filters first: attribute equal or partition, degree range, ego network with a stated depth, giant component, edge weight range.
3. Combine conditions only by nesting. A filter dragged onto another becomes a subfilter, and both conditions apply. Separate top-level queries replace each other's result.
4. Use an INTERSECTION operator for AND across different attributes. Use UNION for OR within one attribute. Give each operator its own top-level query and drag the conditions under it.
5. When an attribute filter repeats inside a query, set the same value in both places. Different values give a blank graph.
6. Check the result in the data table: no row breaks a condition, and the count matches.
7. Save a working query. Remove old filters before you build a new one.
8. Treat the timeline as a filter. Put category filters under the time filter to combine them.
9. Use the plain terms within-group edges and between-group edges. The book's tool labels these "Intra" and "Inter" and its text uses them inconsistently. Check the result by eye.

## 7. Partition and ranking

1. Partition (categorical): pick a non-numeric field; the panel lists groups by share of nodes. Set each color explicitly from the project tokens. To partition by a number, copy it to a text column.
2. Ranking (numeric): pick a numeric field for node size or a color ramp. Set the size range from `encoding-and-filtering.md`, section 4. The tool scales linearly; set a range whose max to min radius ratio is close to the square root of the value ratio, or note the exaggeration.
3. Spotlight a group: filter to it, recolor and enlarge it, remove the filter, then set edge color to the source node.
4. Reset colors and sizes between passes.
5. Clustering plugins: run three settings or more and log the cluster counts (`statistics.md`, section 5). The book's Markov clustering parameter directions look reversed; trust only what you observe.

## 8. Time

1. Confirm a start field and, if nodes leave, an end field.
2. In the data table, merge start and end into a time interval. Choose number or date parsing to match the fields.
3. Alternatives: open a GEXF that already holds intervals, or import a series of static files as time frames, each with a later timestamp.
4. Enable the timeline. Drag the window to the earliest slice. Press play. Adjust the play settings for speed and step.
5. For attribute dynamics, turn on auto apply for ranking before you play, so sizes follow the values.
6. Stop at chosen points and read the node and edge counts for the interval table.
7. Use both window handles to isolate a period.

## 9. Preview and export

1. In Preview, choose a light preset for print; a dark one is allowed for screen. Set label font, size, outline and edge thickness and opacity.
2. Refresh and check overlaps at the export size.
3. Export SVG or PDF for print and editing; PNG for quick sharing.
4. Export the styled graph as GEXF so positions, colors and sizes survive a reload.
5. Web export plugins: confirm the plugin exists for the installed version. Export to a new numbered folder each time; the exporters overwrite their target. Fill the content sheet (`web-and-export.md`, section 4).
6. Serve the exported page over HTTP to test it.

## 10. Hand back to the method

After the tool work, return to `SKILL.md` step 16. Bring back: the project file, the styled GEXF, the exports, the statistics block, the work log and the screenshots of each bake-off candidate. Label tool behaviour you saw as VERIFIED for that version, and the rest as UNTESTED.

## 11. Tool pitfalls

| Pitfall | Sign | Counter-move |
| --- | --- | --- |
| Edges imported first | Node attributes missing | Re-import nodes first |
| Statistic not run | The field is absent from filter or ranking lists | Run the statistic, then map it |
| Separate queries | Only the last condition applies | Nest the conditions or use an operator |
| Mismatched repeated filter | Blank graph window | Same value in both places |
| Text numbers | A numeric field cannot rank | Recast the column type |
| Overwritten export | Custom page edits vanished | New folder per export; tracked patch |
| Plugin missing | A recipe step has no menu entry | Name the fallback before promising the output |
