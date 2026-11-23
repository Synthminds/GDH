# Data preparation: nodes, edges, weights and attributes

Read this file at step 3 of `network-graph`. It covers the two-table shape, identifiers, direction, weight, attributes, de-duplication, self-loops and isolates, projection of bipartite data, derived fields, time fields and privacy.

Evidence. The table shape, the clean-before-import rule, derived fields by word-boundary match and the node-before-edge order come from Cherven (2015), chapters 1, 2, 8 and 10. Projection and weight-merging rules are standard graph practice written by GDH; treat them as defaults.

## 1. The two-table shape

Every graph tool reads two tables. Build them in the project, in code or a spreadsheet, before any graph tool opens them.

Node table:

| Column | Required | Content |
| --- | --- | --- |
| `id` | Yes | A stable, unique key. Never a display name that can change or repeat. |
| `label` | Yes | The display name. Short form here; the full name goes in another column. |
| `type` | For multipartite data | The node type, from a controlled list. |
| Grouping columns | When used for color or filters | Categorical values from a controlled list. |
| Ranking columns | When used for size or filters | Numbers, typed as numbers. |
| `start`, `end` | For time-based networks | Typed as number, date or timestamp. |
| Coordinates | For geographic layouts | Latitude and longitude, or a region key. |

Edge table:

| Column | Required | Content |
| --- | --- | --- |
| `source` | Yes | A node `id`. |
| `target` | Yes | A node `id`. Include both columns even for an undirected graph. |
| `type` | Yes | `directed` or `undirected`. One value for the whole graph unless the story needs mixed edges. |
| `weight` | When strength matters | A number. State what it means: count of co-authored papers, messages sent, money moved. |
| `label` | Optional | Relation name, when relations differ in kind. |
| `start`, `end` | For time-based networks | As for nodes. |

Gate checks on the tables:

- Every `source` and `target` exists in the node `id` column. Zero orphan references.
- Every `id` is unique. Zero duplicates.
- Every numeric column parses as a number. A number stored as text cannot be ranked or filtered.

## 2. Define the units

Write one sentence each in `network-plan.md`:

- "One node is <entity>." Choose the unit on purpose when an entity plays several roles. A musician who plays two instruments can be two nodes (musician-instrument pairs) when grouping by instrument matters, or one node when the person matters.
- "One edge means <relation>." Name the event or fact that creates it, and its time window.
- "The weight is <measure>." Or "Edges are unweighted."

## 3. Direction and weight

| Decision | Choose directed when | Choose undirected when |
| --- | --- | --- |
| Direction | The relation has a sender and a receiver: follows, cites, pays, depends on, reports to | The relation is mutual by nature: co-authored, met, shares a border |

Rules:

- Direction changes the statistics. A directed graph uses in-degree and out-degree, not degree.
- Draw direction only when it is part of the question. An arrow on every edge adds clutter.
- Weight changes the layout when the layout uses it. If edge width shows weight, let weight also pull the layout, unless you write a reason.
- Choose a weight scale on purpose: raw counts, normalised shares, or a log transform when a few edges carry most of the weight.

## 4. De-duplication and merging

Run these steps in order. Record each rule and its count in the plan.

1. Normalise node keys: trim spaces, fix case, unify spellings and transliterations. Keep a mapping table from raw value to `id`.
2. Merge duplicate nodes. Two raw names that mean one entity get one `id`. Record the merges.
3. Merge parallel edges. For an undirected graph, A-B and B-A are one pair. Sum their weights, or count them as the weight. For a directed graph, keep A-to-B and B-to-A apart.
4. Decide self-loops. Remove them when they carry no meaning (a person co-authoring with themselves). Keep them, with a note, when they do (a module that calls itself).
5. Decide isolated nodes. Keep them when "who is unconnected" is part of the story. Otherwise remove them from the drawn view and state the count in the caption.
6. Check the counts against the source after import. A drop in rows means a parse or key problem.

## 5. Put styling fields in the data

- Every color, size and filter rule refers to a column. Manual styling is limited to a short, named highlight list with a reason.
- Add sort keys and ranking fields before import. A graph tool is a weak editor; row-level fixes inside it are slow and lost on re-import.
- Keep one group-to-color mapping across every graph in the project. Store it as a token table, not inside one tool's project file.

## 6. Project bipartite data only on purpose

A bipartite graph (people to projects) can be projected to one node type: two people are linked when they share a project.

| Choice | Use when | Cost |
| --- | --- | --- |
| Keep bipartite | Both types matter to the reader | Needs a layered or two-type layout and two shapes or colors |
| Project to one type | The story is about one type only | Creates dense cliques: a project of 40 people adds 780 edges |
| Project with a weight | Shared-membership count matters | Filter weak edges (weight 1) to avoid a hairball |

State the projection in the caption: "Two people are linked when they worked on at least two projects together."

## 7. Derive fields when the data has none

A dense graph with no categorical field cannot be colored by meaning. Derive fields before the first color pass.

From labels, by text pattern:

1. Write the pattern with word boundaries. A plain search for "man" also hits "woman" and "Norman".
2. Set the letter case on purpose.
3. Review a sample of at least 20 matches and 20 non-matches for false hits and misses.
4. Write the definition of the field in the plan.

From structure:

- Degree band (low, middle, high), community id, component id.
- Hop distance from a focus node (0 for the focus, 1 for its neighbours, and so on). Unreachable nodes get their own value.

From outside sources: join an attribute table by `id`. Record its source and license.

## 8. Time fields

- Every element in a time-based network has a start. An end is needed when elements leave.
- Type time fields as number, date or timestamp. Never as text.
- Carry every time field the source offers: birth, entry, exit, event time. Choose the one that tells the story later; trying a field is cheaper than a new data pull.
- When the data arrives as period snapshots, keep one schema across all files, the same `id` for the same entity, and a strictly later timestamp for each file.

Read `dynamic-networks.md` for the design rules.

## 9. Privacy and sharing

- A network of people exposes relations that no single row shows: who knows whom, who left, who bridges two groups.
- Ask the user, before any render leaves the project: may real names appear, may the data file ship with the page, who may see the page.
- Use mock or pseudonymised data in prototypes that are shared. Swap in real data only for the approved audience.
- An interactive page that ships the full graph file ships every edge, including filtered ones. Ship only the published subset.

## 10. Preparation checklist

- [ ] Node table: unique `id`, `label`, typed attribute columns.
- [ ] Edge table: `source`, `target`, `type`, `weight` with a stated meaning.
- [ ] Zero orphan references; zero duplicate ids.
- [ ] One-sentence definitions of node, edge and weight.
- [ ] Merge, self-loop and isolate rules recorded with counts.
- [ ] Bipartite structure tested; projection decided and stated.
- [ ] Derived fields defined; text matches spot-checked.
- [ ] Time fields typed; snapshot files share one schema.
- [ ] Privacy answer recorded for people networks.
- [ ] Source and license of each dataset recorded through `find-assets`.
