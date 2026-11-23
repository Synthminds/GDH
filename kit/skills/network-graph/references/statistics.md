# Statistics that drive the design

Read this file at step 5 of `network-graph`. It covers the three tiers of statistics, what each measure answers, what it drives in the encoding, the traps in reading it, and how to run and validate community detection.

Evidence. The three tiers, the question-to-measure table, the score-direction warning, the component rule and the clustering tuning loop come from Cherven (2015), chapters 4, 6, 7 and 10. PageRank, weighted degree and the Louvain and Leiden methods are standard graph practice written from memory; they are labelled. The modularity resolution direction comes from Gephi tutorials found by search. Every number is a default.

## 1. Why compute before drawing

- Layout changes appearance only. Every statistic is the same under every layout. So a claim about structure needs a number, not a position.
- Beyond a few dozen nodes, the eye cannot judge structure. Numbers confirm or challenge the first impression.
- A statistic must exist before you can size, color or filter by it.

## 2. Tier 1: the whole network

| Measure | Definition | What it tells you | Report it as |
| --- | --- | --- | --- |
| Node and edge count | As drawn, after cleaning | Size class | "<n> nodes, <e> edges" |
| Components | Groups with no path between them | Whether it is one network | "<c> components; the largest holds <share> of nodes" |
| Density | Existing edges divided by possible edges, 0 to 1 | How saturated the links are | "<x> percent of possible edges exist" |
| Average degree | Mean links per node (directed: mean in or out) | Typical connectedness | "<d> links per node on average" |
| Diameter | The longest shortest path | The reach of the network | Always beside the node count, and only for one component |
| Average path length | Mean shortest-path length over all pairs | How easily things flow | Beside the diameter |
| Clustering coefficient | Closed triangles over all connected triples, 0 to 1 | Local cohesion | Network value and the node range |

Reading rules:

- Count components first. On a disconnected graph, distance measures run per component or on the largest one. Label them "largest component only". Never quote one diameter for a disconnected graph.
- Write density as a share of possible edges. The book's phrase "percent of nodes are connected" is wrong; do not copy it.
- Read diameter with node count. A diameter of 6 on 200 nodes means a less efficient network than 6 on 2,000.
- Compare average path length with diameter. An average close to the diameter suggests several loosely joined clusters. An average well below it suggests easy flow, unless a few bridge nodes carry the paths.
- Compare networks only of the same kind and edge definition, with normalised values. A collaboration network is expected to be sparser than a friendship network.

## 3. Classify the structure

| Type | Evidence | Design consequence |
| --- | --- | --- |
| Random | Degrees cluster around the mean; low clustering | No strong story from structure; question the form |
| Hub and spoke (scale free) | A few nodes with far higher degree; long tail | Size by degree; spread hubs; label hubs |
| Small world | Short average paths, high clustering, few or no hubs | Default: try a circular layout ordered by group; force layouts can hide it |
| Clustered (homophily) | High modularity; dense groups, few links between | Color by community; mark bridges |
| Layered | Edges run only between node types or levels | Layered, multipartite or tree layout |

## 4. Tier 2: node centrality

Pick the measure that matches the question. The measures do not compete; they answer different questions.

| Question | Measure | What it drives | Trap |
| --- | --- | --- | --- |
| Who has the most direct ties? | Degree | Node size in a first look | Says nothing about tie strength; small differences prove little |
| Who has the strongest ties overall? | Weighted degree (strength): the sum of edge weights | Node size when weight matters | Dominated by one heavy edge; check the distribution |
| Who is sought out? (directed) | In-degree | Size for influence or popularity | Use it instead of degree on a directed graph |
| Who reaches out or collects? (directed) | Out-degree | Size for activity | High out with low in is rarely influence |
| Who reaches everyone in few steps? | Closeness | Color or size for reach | Needs a connected graph; some tools report it inverted |
| Who sits on paths between others? | Betweenness | Highlight bridges and brokers | Can be high where every other measure is low; that is the point |
| Who is tied to well-connected nodes? | Eigenvector centrality | Size for prestige | Rises with degree; weak on directed graphs with sources and sinks |
| Who is important by recursive endorsement? (directed) | PageRank (from memory, not from the book) | Size for influence on directed graphs | Its damping parameter changes ranks slightly; record it |
| Which nodes are good sources, which good pointers? (directed) | HITS authority and hub scores | Two views of a citation or link network | On an undirected graph both scores are equal and add nothing |
| Which edges carry the most paths? | Edge betweenness | Edge width or highlight for fragile links | A few edges near the maximum mean a fragile network |

Rules:

- Write the direction of every mapped score: "higher = more central" or "lower = more central". In the book's tool version, closeness was an average distance, so lower meant more central. Record the tool and its version.
- Back any "most influential" or "most important" label with two measures that agree. Accept a one-measure claim only when the gap is large (the book accepts 98 against 18, not close values).
- Use in-degree and out-degree on a directed graph. Two nodes with a similar total can play opposite roles (18 in and 80 out against 50 in and 40 out).
- Expect high-degree nodes to have low local clustering. Their neighbours do not link to each other. A downward slope of local clustering against degree is normal, not a data error.
- Normalise scores to 0 to 1 when you compare across networks or across filtered views.

## 5. Tier 3: groups

| Measure | What it gives | Drives |
| --- | --- | --- |
| Modularity communities | A community id per node and a modularity score | Node color |
| Clustering coefficient, local | Cohesion of each node's neighbourhood | Filters, a secondary ramp |
| Triangle count | Closed triples per node | Detail panel |
| Edge communities (link communities) | Groups of edges; a node can belong to several groups | Overlapping group views |
| Embeddedness | Shared-neighbourhood score of an edge | Filter incidental ties (low) from structured ones (high) |

### Run community detection

1. Record the component count and the isolates first. Some algorithms cannot cross component boundaries and leave isolated nodes unassigned.
2. Run the algorithm at three settings or more. On one 1,668-node network, one setting change gave 14, 42, 17 and 7 clusters. Small steps swing results.
3. Log each run: algorithm, parameters, cluster count, smallest and largest cluster size, singleton count, modularity score.
4. Reject over-segmentation: more than one or two singleton clusters, or more than about twice the count of a known grouping.
5. Reject under-segmentation: fewer than about half the count of a known grouping, or one cluster holding most nodes.
6. View each surviving run as colors with edges hidden. Prefer the run whose colors form contiguous regions. When unsure, prefer the lower count.
7. Cross-tabulate the communities against a known attribute (department, grade, country). Agreement explains the communities; disagreement is often the finding.
8. Name the algorithm and its key parameter in the legend title: "Communities: modularity, resolution 1.0".
9. Present the result as one reading of the network, not as a fact about it.

Method notes:

- Modularity optimisation with a resolution parameter: in Gephi tutorials, a lower resolution gives more, smaller communities; a higher one gives fewer, larger ones. Confirm the direction in your tool.
- Default: Louvain or Leiden in a code library (from memory). Leiden avoids badly connected communities. Fix the random seed; results vary between runs.
- Label propagation methods (the book's Chinese Whispers) are fast and cheap to repeat, and they leave isolates unclustered.
- Markov clustering is costly. Test run time on a sample before a graph of more than a few thousand nodes. The book's stated parameter directions look reversed; do not rely on them.

## 6. Partition or cluster: say which

- A partition splits nodes by an attribute you chose (department, type). Its legend names the field.
- A cluster or community comes from an algorithm. Its legend says "detected" and names the method.
- Never mix the two in one legend entry.

## 7. From statistics to filters and views

1. Range-filter one statistic to show the top nodes, for example betweenness above a chosen value.
2. Intersect that range with one group to find the key nodes inside it.
3. Intersect a community with a formal attribute to test whether the attribute explains the community.
4. Recompute statistics on a filtered view when the claim is about the view. Tag each value "full network" or "filtered view".
5. Choose thresholds that keep about the top 5 to 10 percent, and say the cut is a judgment. Example from the book: betweenness above 250 kept 17 of 236 nodes.

## 8. Large graphs

- Default: when betweenness or closeness is too slow on a very large graph, fall back to degree, weighted degree and PageRank, or sample. Say so in the notes.
- Record which statistics completed, with node and edge counts.
- The book reports trouble at about 10,000 nodes and 180,000 edges on default memory in a desktop tool; raise memory or move to code.

## 9. The statistics block

Write this in `network-plan.md`. Every caption claim points to a line here.

```
Scope: <full network | largest component | filtered view: rule>
Tier 1: nodes <n>, edges <e>, density <x>, components <c> (largest <share>),
        average degree <d>, diameter <D> (largest component), average path <L>,
        clustering <C>
Tier 2: size measure <name>, direction <higher = more central>, tool <name version>
        top 10 by <measure>: <ids>; second measure agrees: <yes | no>
        bridges (top betweenness): <ids>
Tier 3: communities <k> by <method, parameters, seed>; modularity <Q>;
        runs tried <list>; cross-tab with <attribute>: <finding>
Claims: "<caption claim>" -> <statistic and value>
```

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Central by position | "X sits in the middle, so X is central" | Cite a centrality value or drop the claim |
| One measure crowned | "Most influential" from degree alone | Compare two measures; report both |
| Diameter of a fragmented graph | One diameter quoted for many components | Report per component; label the scope |
| Default clustering shipped | One run, default settings | Three runs, logged, validated by eye and by attribute |
| Inverted ramp | The darkest nodes are the least central | Write the score direction before mapping |
| Statistics of the whole quoted for a filter | A view of 40 nodes with network-wide numbers | Recompute and tag the scope |
