# When a network graph is the right form

Read this file at steps 1, 2 and 4 of `network-graph`. It covers the purpose statement, the form choice table, the size classes and what each class allows.

Evidence. The purpose, delivery and size-class rules come from Cherven, "Mastering Gephi Network Visualization" (2015), chapters 2 and 3. The form choice table is GDH synthesis from that book and the Financial Times Visual Vocabulary. Every number here is a default.

## 1. Write the purpose before you touch data

Write two sentences in `network-plan.md`.

1. Purpose: "This graph will <inform | persuade | educate | entertain> <audience> about <story>."
2. Question: "Who is central", "which groups exist", "what joins group A and group B", "how far is everyone from X", or "how did the network change".

Rules:

- One purpose. A brief with two equal purposes produces two graphs. Ask which one leads.
- Record the delivery before the layout: static or interactive, surface (print, slide, social image, web page, report) and target size in pixels or millimetres.
- Name a domain reviewer: the user or an expert who can say whether the main clusters and hubs make sense.
- Write the edge rule: "A and B are linked when ...". With no edge rule, there is no network. Choose another form.

Why delivery first: an interactive graph may stay dense because the viewer zooms, searches and filters. A static graph carries the whole story in size, color and text.

## 2. Choose the form

A node-link picture is strong at one thing: showing structure that no single row of data holds, such as clusters, bridges, hubs and reach. It is weak at exact comparison. Use the table before you commit.

| The question is mainly about | Best form | Why | A node-link graph is right only when |
| --- | --- | --- | --- |
| Who has the most links, ranked | Ordered bar chart or table (`data-viz`) | Length on a common baseline is read exactly | The ranking must be seen in its structural context |
| Clusters, bridges, overall structure | Node-link graph, force-directed | Position makes groups and gaps visible | Always, within the size limits below |
| Every pairwise link in a dense group | Adjacency matrix | No edge crossings; dense blocks show communities when rows are ordered by community | The group is sparse, or the story is about paths |
| Links in an ordered sequence (chapters, timeline, genome positions) | Arc diagram | Nodes keep their order on one axis; arcs show the links | The order carries no meaning |
| Quantity moving between stages or categories | Sankey or alluvial (`data-viz`) | Width shows volume through stages | The flow has cycles or many-to-many links with no stages |
| Flows between a small set of groups, both ways | Chord diagram, or a matrix of totals | Totals per group pair read directly | The individual entities matter |
| A strict hierarchy with one parent per node | Tree, indented list, icicle or treemap | The hierarchy is the structure; a graph adds noise | Cross-links exist that the story needs |
| One entity and its reach | Ego network, concentric rings by hop distance | The subject sits in the centre | It is |
| Places linked by movement | Flow map (`data-viz` with `maps`) | Geography carries meaning | Location is not part of the story |
| A few boxes and arrows a person arranges | Diagram (`diagram` capability) | Hand placement beats an algorithm under about thirty nodes | Never; draw it as a diagram |
| Exact attributes of each relation | Table with sort and filter | Rows hold detail better than marks | Never alone; pair the graph with the table |

Rules:

- When the table points away from a graph, show the user both a sketch of the better form and the reason. ASK before you switch.
- A graph used as decoration, where a ranked list informs more, is a failure. Route it to `data-viz`.
- Offer a second view for a dense graph: a matrix ordered by community, or a community graph where each node is one community.
- Pair every published graph with a ranked table or a text summary. The table is also the accessible form.

## 3. Bipartite and multipartite data

Test whether any edge joins two nodes of the same type.

- None does: the graph is bipartite (two types) or multipartite (three or more). Examples: person to project, author to paper, professor to department.
- Choose a layered, multipartite or two-column layout, or project the graph (see `data-preparation.md`, section 6).
- Never draw a bipartite graph with one color for both types. Type is the first encoding.

## 4. Size classes

Sort the graph after cleaning. Count nodes and edges in the version you will draw.

| Class | Nodes | What the class allows | What it needs |
| --- | --- | --- | --- |
| Small | Tens, up to about 100 | Any layout family; every node labelled; hand nudges for label room; SVG rendering; a static image carries the story | A legend; a caption |
| Medium | Hundreds | Force-directed or grouped layouts; labels by rank only; SVG or canvas; static works with filtering | Filtering or focus views; tiered labels; overlap removal |
| Large | Thousands | Fast force methods; canvas or WebGL; interaction; static only as an overview plus focused views | Filters, aggregation or interaction; search; level-of-detail labels |
| Very large | Tens of thousands and more | Fast multilevel layouts; WebGL; aggregation to communities; tiled zoom viewers | A reduction step before any static image; a server-side or offline layout |

Defaults and their reasons:

- Default: past a few hundred nodes, a single static node-link view needs filtering, aggregation or interaction. Rule of thumb, not a measured limit.
- Default: at about ten thousand nodes or more, plan an interactive deliverable, or name a reduction step for a static one. The book reports poor results from static images at that scale.
- Default: re-test the layout when the node count grows about five times. A layout that worked at seventy-six nodes may fail at five hundred.

## 5. Read the size and shape together

Size alone does not set the class. Read three more facts in the first look.

| Fact | How to read it | What it changes |
| --- | --- | --- |
| Edges per node (the beta index) | Edges divided by nodes. Below 1: very simple. Near 1 with no hubs: hard to spread. Well above 1: dense | Dense graphs need edge filtering and low edge opacity |
| Components | Count them; find the share in the largest | Many small components need a packed layout or a giant-component view |
| Hubs | Plot the degree distribution | A long tail of low-degree nodes and a few hubs needs size encoding and hub spacing |

Example from the book: a power grid of about 5,000 nodes and 6,500 edges, average degree about 2.7, clustering 0.08, diameter 46. Sparse, hubless and long: expect weak cluster separation in any force layout.

## 6. The first-look record

Write this block in `network-plan.md` before any layout work.

```
Purpose: <one sentence>
Question: <one sentence>
Delivery: <static | interactive | both>; surface <...>; size <...>
Edge rule: A and B are linked when <...>
Node = <...>; Edge = <...>; directed <yes | no>; weighted <yes | no: weight means ...>
Counts: <n> nodes, <e> edges, e/v <ratio>, components <c>, largest <share>
Class: <small | medium | large | very large>
Structure guess: <random | hub and spoke | small world | clustered | layered>
Time: <present and used | present and dropped, because ... | absent>
Form: <node-link | matrix | arc | other>, because <reason>
Reviewer: <name or role>
```

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Graph by reflex | The data has links, so a graph was drawn | Run the form table. Ask what question the picture answers that a table cannot |
| Two purposes | "Show the communities and rank the top influencers" | Split into a graph and a ranked chart |
| Delivery decided last | A dense interactive design ends up as a slide image | Decide delivery in step 1. Plan the static overview and focus views |
| Impressive, unreadable | A striking hairball as a cover image | A cold reader states the finding in thirty seconds, or it fails |
| Bipartite drawn flat | People and projects in one color in one force layout | Encode type first; consider layered or projected views |
