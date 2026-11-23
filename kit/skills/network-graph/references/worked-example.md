# Worked example: from a raw edge list to a published graph

Read this file to see the whole `network-graph` procedure on one dataset. The dataset, names and numbers are invented for illustration. They are internally consistent, but nothing here was rendered. Evidence: UNTESTED.

The case: a research institute wants to show which of its labs work together and who connects them. The output is an interactive page for staff and a static figure for the annual report.

## Step 1. Purpose and question

```
Purpose: This graph will inform institute staff about how labs collaborate.
Question: Which groups of researchers exist, and who joins them?
Delivery: both; web page (1440 px wide) and report figure (A4, 170 mm wide)
Edge rule: two researchers are linked when they co-authored a paper, 2019 to 2025
Reviewer: the institute's research director
```

## Step 2. Form check

- Ranking the most prolific authors: a bar chart (`data-viz`). Not the main question.
- Groups and bridges: structure that no single row holds. A node-link graph fits.
- Second view: a community-by-community matrix of joint papers, for the report.
- Decision logged: node-link graph plus a matrix and a ranked table.

## Step 3. Data preparation

Raw file: `papers.csv` with one row per paper and an author list. 1,190 papers.

1. Split author lists into pairs. 1,190 papers gave 6,842 raw pairs.
2. Normalise names. A mapping table merged 37 spelling variants ("J. Okafor" and "Jo Okafor") into 29 people. Each person gets a stable `id`.
3. Drop external co-authors by the brief's scope: internal staff only. 412 people remain.
4. Merge parallel pairs. Undirected, so A-B and B-A are one edge. Weight = number of joint papers.
5. Self-loops: none after merging. Isolates: 31 staff with no internal co-author. Kept in the table; removed from the drawn view; counted in the caption.
6. Join attributes from the staff file: `lab` (9 values), `role`, `start_year`.

Result: 381 drawn nodes, 1,604 edges, weights 1 to 23.

```
nodes.csv  id,label,lab,role,start_year
           r017,A. Moreau,Climate,PI,2012
edges.csv  source,target,type,weight
           r017,r144,undirected,9
```

Checks: zero orphan references, zero duplicate ids, numeric columns typed.

## Step 4. Size class

381 nodes, 1,604 edges, edges per node 4.2. Medium class: force-directed or grouped layouts, labels by rank, SVG or canvas, filtering for the static figure.

## Step 5. Statistics

```
Scope: drawn network (381 nodes)
Tier 1: edges 1,604; density 2.2 percent of possible edges; components 4
        (largest 368 nodes, 96.6 percent); average degree 8.4;
        diameter 9 and average path 3.6 (largest component only); clustering 0.41
Tier 2: size measure weighted degree; higher = more collaboration; code library, version pinned
        betweenness top 5: r144, r017, r233, r052, r310
        degree top 5: r017, r088, r144, r201, r233; overlap with betweenness: 3 of 5
Tier 3: Leiden, resolution 1.0, seed 7: 11 communities, modularity 0.62
        runs: resolution 0.5 gave 6; 1.0 gave 11; 1.5 gave 19 with 4 singletons
        cross-tab with lab: 8 of 11 communities map mostly to one lab;
        community 4 mixes Climate and Statistics (the finding)
```

Choice: resolution 1.0. Reason: 19 communities over-segment (four singletons); 6 merge three labs that the director says work apart.

## Step 6. Shortlist

Seven questions: relationships and divisions; medium; moderately dense; clusters expected by lab; single-level; time present but dropped for the main view (the network changed slowly); both static and interactive.

Candidates: ForceAtlas2 (force), circular ordered by community (circular), radial axis with one axis per lab (grouped).

## Step 7. Bake-off

All at 1440 by 1000 px, same data.

| Candidate | Tuning steps | Result |
| --- | --- | --- |
| ForceAtlas2 | Scaling 100 to 200 (centre knot); gravity 1.0 to 0.5; weight influence 1; prevent overlap on | Communities form regions; community 4 sits between Climate and Statistics; bridges visible |
| Circular by community | Order by community, then weighted degree | Groups clean, but 1,604 chords form a dense core; bridges unreadable |
| Radial axis by lab | Order on axis by weighted degree | Cross-lab edges visible; within-lab structure lost; the mixed community 4 hidden |

Losers: "Circular: clean groups, but the chords bury the bridges." "Radial: shows cross-lab links, but hides the mixed group, which is the finding."

## Step 8. ASK

Shown side by side: "Which one shows who joins the groups most clearly?" The director chose ForceAtlas2. Logged in `design/decisions.md` with both rejections.

## Step 9. Reduce

- Web page: all 381 nodes; edges with weight 1 drawn at the lowest opacity.
- Report figure: edges with weight 2 or more (1,011 of 1,604). Disclosed.
- Focus view for the report: the ego network of r144 at depth 1 (27 nodes).

## Step 10. Encode

| Channel | Carries | Scale |
| --- | --- | --- |
| Node size | Weighted degree | Area; diameter 6 to 36 px; capped above 120 joint papers (two nodes; noted) |
| Node color | Community (detected, Leiden) | Eight token colors; communities 9 to 11 (sizes 6, 5 and 4) share the neutral "Other" |
| Edge width | Joint papers | 0.5 to 2.5 px |
| Edge color | Neutral gray, low opacity | Constant |
| Highlight | Top 5 betweenness nodes | Accent ring plus label in bold |

The lab attribute goes to the group selector and the detail panel, not to color.

## Step 11. Labels and overlaps

- Labels: the top 20 by weighted degree plus the 5 bridges (25 labels, 3 shared). 22 labels at default zoom.
- Overlap pass: zero node overlaps. Label adjust, then two labels shortened to surname. Zero label overlaps at 1440 px and at 170 mm.

## Step 12. Legend, caption, summary

```
Node = one researcher   Edge = co-authored at least one paper, 2019 to 2025
Size = joint papers (weighted degree), 1 to 120+, larger = more collaboration
Color = communities (detected, Leiden, resolution 1.0); gray = three small communities
Ring = top 5 by betweenness (bridges)
```

Caption: "Co-authorship among 381 institute researchers, 2019 to 2025; 31 staff without internal co-authors not shown. Force-directed layout: distance between nodes is approximate. Report figure shows only pairs with two or more joint papers (1,011 of 1,604 links)."

Summary: "Eleven communities hold 96.6 percent of researchers in one connected network. Eight communities follow lab lines. One community of 41 people joins Climate and Statistics. Five researchers carry most cross-group paths; the top one sits on more shortest paths than the next two together. Average distance between two researchers is 3.6 steps."

## Step 13. Time

Dropped for the main view, with the reason. A second static figure shows the network at the end of 2019, 2022 and 2025 with fixed positions, plus small multiples of node count, edge count and components per year.

## Step 14. Build

- Web page: canvas renderer (medium class), positions precomputed, simulation off. Search, hover dimming, lab selector with names and counts, detail panel with co-authors as links, label tiers, keyboard controls, table view, about view with the data source and method.
- Report figure: SVG master from the same positions; title, two callouts (community 4 and the top bridge), pointer lines; light ground.
- Files: `coauthors.gexf`, `coauthors-master.svg`, `coauthors@2x.png`, `coauthors-table.csv`, `site/001/`.

## Steps 16 to 18. Gates

- Spend: none; the page is static and self-hosted.
- Exposure: the page names staff. ASK: "May staff names appear to all staff?" Director: yes for staff, no for the public report. The public figure labels communities, not people, and the ring marks bridges without names.
- Review: a cold reader said in thirty seconds: "Most labs keep to themselves; one group links climate and statistics people." Matches the finding.

## Closing report

```
Network: institute co-authorship; question: which groups exist and who joins them
Data: 381 nodes, 1,604 edges, undirected, weighted (joint papers); class medium
Structure: components 4, largest 96.6 percent; communities 11 by Leiden, resolution 1.0
Layout: ForceAtlas2, scaling 200, gravity 0.5, seed 7; tested: circular, radial axis
Filters: report edges weight 2 or more, 1,011 of 1,604; isolates 31 not drawn
Encoding: size weighted degree (higher = more); color community; edges weight
Deliverables: page, SVG master, PNG, GEXF, table
Checks: overlaps 0; claims backed 5 of 5; cold reader matched the finding
Evidence: UNTESTED (illustrative example; nothing rendered)
```
