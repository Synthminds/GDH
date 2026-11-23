# Filtering and visual encoding

Read this file at steps 9 to 12 of `network-graph`. It covers hairball rescue, filter families and disclosure, node size, node color, edges (weight, opacity, curved or straight, direction), highlights, labels by rank, overlap removal, the legend, the caption and the text summary.

Evidence. The filter rules, the area-scaling test, the partition limits, the highlight method, label tiers and legend content come from Cherven (2015), chapters 2, 3, 5, 7, 9 and 10. Curved-edge guidance and the label budget are GDH practice; treat them as defaults. Every number here is a default unless a check calls it a gate in `SKILL.md`.

## 1. Reduce before you style

A hairball is a defect. No layout alone removes it on dense data. Use these moves, cheapest first.

| Move | Use when | How | Disclose |
| --- | --- | --- | --- |
| Giant component | Many tiny components add noise | Keep the largest component | "Largest component: <n> of <N> nodes" |
| Degree range | Hubs or periphery are the story | Keep nodes with degree at or above a threshold, or read the low band separately | "Nodes with degree 5 or more: <n> of <N>" |
| Edge weight floor | Many weak, incidental ties | Keep edges at or above a weight | "Edges with weight 2 or more: <e> of <E>" |
| Statistic range | Bridges or brokers are the story | Keep the top betweenness band | "Betweenness above 250: 17 of 236 nodes (cut chosen)" |
| Ego network | One node's reach is the story | Keep the node and neighbours within a depth | "Depth 1 around <node>" |
| Attribute | A known group is the story | Keep one or more partition values | "Department = research" |
| Aggregate | The story is between groups | One node per community; edge width = links between communities | "Each circle is one community" |
| Split views | Cohesion and contact both matter | Within-group edges in one view, between-group edges in another, same positions | Each view titled |
| Soft filter | Context must stay | Draw all nodes; make only the top few prominent by size | "Size shows degree" |

Rules:

- A filter changes the view, never the stored data. Keep the full dataset unchanged.
- Explore with single filters before you combine them. One condition at a time shows which combination is worth a published view.
- Filter by structure (degree, ego, component) when the question is about behaviour. Filter by attribute when it is about a known group. Formal labels can hide what single nodes do.
- Prefer several small focused views, each with its own one-sentence finding, to one view of everything. For a medium or large graph, ship an overview plus at least two focus views.
- State every filter, its threshold and the kept count in the caption or legend. A silent filter misleads.
- Default: pick thresholds that keep about the top 5 to 10 percent, and write "cut chosen".
- Choose "emphasize in context" or "isolate" on purpose. In emphasize mode, default: at most about 5 percent of nodes are prominent.

## 2. Hairball rescue for an existing dense graph

1. State what the graph already shows (sized hubs, outlying clusters) and what the data lacks (categories, dates).
2. Derive fields: from labels by word-boundary match, from structure by degree band, community or hop distance (see `data-preparation.md`, section 7).
3. For each derived flag: filter to it, verify the rows, apply one accent color while the filter is on, then remove the filter.
4. Repeat for a few flags. Default: five accent colors at most. Leave every other node one neutral gray.
5. Alternative: pick a focus node with the user, color every node by hop distance from it with an ordered ramp, and give unreachable nodes a neutral with a legend entry.
6. Compare with the starting image. ASK which version answers the question. Keep the derived fields in the saved graph file.

## 3. Encoding table

Fill one row per channel in `network-plan.md`. One channel, one meaning.

| Channel | Carries | Scale | Default |
| --- | --- | --- | --- |
| Node size | One measure (degree, strength, PageRank) | Area proportional to value | Diameter 4 to 40 px on screen |
| Node color | One attribute: community, type, partition, or one ordered measure | Categorical or sequential | Eight categories at most |
| Node shape | Node type in multipartite data, only when color is used for something else | Categorical | Two or three shapes |
| Edge width | Weight | Narrow range | 0.5 to 3 px on screen |
| Edge opacity | Nothing; it reduces clutter | Constant | Low; raise only for story edges |
| Edge color | Neutral, or derived from the source node, or one highlight | Neutral first | Gray at low opacity |
| Highlight | One named subset | Two channels changed | One accent outside the main palette |
| Label | Identity of ranked and named nodes | Narrow size range | 10 to 30 labels per screen |

Do not map size and color to the same measure, with one exception: for a first-glance read of hubs when no categorical field needs color, degree on both size and color makes hubs and odd tight clusters stand out. State it in the legend.

## 4. Node size

- Scale area, not radius. For two nodes, radius ratio equals the square root of the value ratio. Values 1 to 23 map to a radius ratio of about 4.8 to 1, not 23 to 1.
- Give the smallest node a visible, non-zero size. Default: 2 px radius or more at default zoom. A value of zero still needs a mark.
- Cap the largest node so a dominant hub does not bury its neighbours. The book used a 2 to 20 size range for degrees 2 to 56.
- A cap, a clipped range or an exaggerated range for visibility is allowed only with a note: "Sizes capped above degree 40" or "sizes exaggerated for visibility".
- Widen the range when most nodes score low and the distribution is skewed; hubs must be visible at default zoom.
- Name the measure in the legend, with its min and max and its direction.

## 5. Node color

Choose the method from the field type.

| Field | Method | Rule |
| --- | --- | --- |
| Categorical (type, department) | Discrete palette | Two to about 20 groups; default eight colors, small groups share a neutral "Other" |
| Detected communities | Discrete palette, treated as categorical | Legend says "detected" and names the method |
| Ordered measure (centrality, hop distance) | Sequential ramp, one hue family | Light for low, dark for high on a light ground; reverse on dark |
| Measure with a meaningful midpoint (change, balance) | Diverging ramp | Neutral at the midpoint |

Rules:

- Check balance before you ship a partition. When one group holds about 85 percent or more of nodes, say so, filter to where the split matters, or pick another field.
- Sort the legend by group size, unless the field is ordinal (decades, distance bands); then follow data order.
- Set every legend color explicitly from tokens. Never ship a tool's default palette.
- Keep one group-to-color mapping across every graph in the project.
- Reset colors and sizes to a uniform baseline before each new encoding pass. Leftovers mix two meanings.
- Colors must stay distinct for color-vision deficiency. Groups that matter also differ by label, position or shape.
- Node fills are 3:1 or more against the ground (gate in `SKILL.md`).

## 6. Edges

Edges cause most clutter. Make them recede.

- Default edges: thin, low opacity, muted. Story edges: thicker or stronger, and few.
- Width follows weight in a narrow range. Wide edges merge into blobs.
- Edge color: neutral by default. Coloring edges by their source node helps when one group's ties must stand out.
- Straight or curved:

| Edge shape | Use when | Avoid when |
| --- | --- | --- |
| Straight | Default; dense graphs; exact reading of which nodes connect | Two directed edges A to B and B to A overlap |
| Curved (constant bend, one direction) | Directed graphs with reciprocal edges, so both show; arc diagrams | Dense graphs: curves add visual weight and hide structure |
| Bundled | Very large graphs where only the main flows matter | Individual links must be traced |

- Show direction only when it is part of the question. Prefer a small arrowhead or a taper toward the target. Default: no arrows in a force overview of more than a few hundred nodes.
- Self-loops and parallel edges are drawn only if they carry meaning (see `data-preparation.md`).

## 7. Highlight one subset

1. Define the subset by a written rule (a filter), not by hand-picking.
2. Change two channels for the subset: fill and size. A unique color alone is one color among many.
3. Set every other node to one neutral fill.
4. Use one highlight color that no group in the main palette uses.
5. For a focus story: the subject node largest or most saturated, its direct neighbours in one highlight color, everything else neutral.
6. List manual styling by node id with a reason in the plan.

## 8. Labels

1. Label the top nodes by the size measure. Default: about 10 to 30 on one screen.
2. Label every node the story or caption names, whatever its rank. Zero unlabelled story nodes.
3. Keep label sizes in a narrow range, and never below the smallest text size of the medium (see the `typography` size table).
4. Give long names a short form on the canvas; keep the full name in the detail panel or table.
5. Remove node overlap first, then label overlap: move the label, shorten it, or drop the lower-ranked label.
6. In an interactive view, reveal labels by tier as the viewer zooms: the top tier at load, the next at the first zoom step, all at close zoom.
7. Labels sit on a halo or a plain ground strip when they cross edges, so contrast holds (4.5:1 for label text).

## 9. Overlap removal

- Turn on overlap prevention at the end of the layout, or run a separate overlap-removal pass.
- Test with bounding circles at delivery size: zero overlapping node pairs.
- Run a label-adjust pass, then check label boxes: zero overlaps at delivery size.
- A manual move for label room is allowed. Note it. Never move a node to strengthen a point.

## 10. Legend, caption and summary

Legend, always:

```
Node = <entity>          Edge = <relation>
Size = <measure>, <min> to <max>, higher = more <...>
Color = <attribute or "communities (detected, <method>)">
Highlight = <rule>       Filter = <rule, kept of total>
```

Caption, in two or three sentences:

- The layout algorithm and that positions are not data: "Force-directed layout; distance between nodes is approximate."
- Filters with thresholds and counts; the date or period of the data; the source.

Text summary, three to five sentences, each with a number: the largest groups and their sizes, the top nodes by the size measure, the bridges, and anything the filter hid. Pair it with a ranked table of the top nodes.

## 11. Review the rendered artifact

- [ ] No region where nodes and edges cannot be told apart.
- [ ] Zero node overlaps; zero label overlaps.
- [ ] Hubs or other features visible at default zoom.
- [ ] Story edges traceable end to end.
- [ ] Groups distinguishable, and the legend names each.
- [ ] Non-story edges thin, muted and low opacity.
- [ ] Size legend names the measure and its direction.
- [ ] Highlight color used for one named subset only.
- [ ] Every filter stated with its threshold and counts.
- [ ] A cold reader states the main finding in thirty seconds.
- [ ] No claim rests on position alone.

## 12. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Rainbow communities | Thirty hues | Eight colors; the tail in one neutral; or aggregate |
| Label flood | A label on every node | Tiered labels by rank |
| Radius scaling | Hubs look many times too big | Scale area; note any cap |
| Size and color doubled | Both show degree while a category goes unshown | Free one channel for the category |
| Silent filter | Nodes missing, no note | State rule, threshold and counts |
| Edges louder than nodes | Thick, opaque, colored edges everywhere | Thin, muted, low opacity; strong edges only for the story |
| Hand-picked highlight | Favourite nodes glow | Define the subset by a rule |
