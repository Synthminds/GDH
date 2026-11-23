# Interactive pages, libraries by size class, export and deployment

Read this file at step 14 of `network-graph`. It covers the output classes, renderers and libraries by size class (chosen by capability), the interaction set, the content of an interactive page, performance, static export, the file set, deployment and testing.

Evidence. The output classes, the legend content, the about view, search, hover dimming, group selector, detail panel, label tiers, viewer tiers, HTTP testing and versioned export folders come from Cherven (2015), chapter 9. Library facts come from `kit/catalogs/assets.json` (licenses read 2026-11-23). Renderer thresholds are rules of thumb; treat them as defaults and measure on the target device.

## 1. Choose the output class first

| Class | Use for | Formats |
| --- | --- | --- |
| Graph file | Reuse in another tool; the styled master | GEXF (keeps time, color, size, position), GraphML, GML |
| Image | Quick sharing, social previews, slides | PNG at 2x the display size |
| Vector | Print, annotation, further design work | SVG (ungroups into nodes, edges, labels) or PDF |
| Interactive web | Complex networks, exploration | A page with the graph data and a renderer |

Rules:

- Name one primary class and the reason in the plan. Map each audience to a format it can open.
- A graph of thousands of nodes delivered only as an image needs a stated reduction or annotation plan.
- A small embedded raster of a complex graph links to a full-resolution or interactive version.
- Keep the vector master and the styled graph file in every handoff, beside any PNG.

## 2. Viewer tiers

| Tier | Gives | Choose when |
| --- | --- | --- |
| Zoom-only viewer (tiled image) | Pan and zoom over a very large static render | A quick look at a huge graph; no data needed |
| Explorer page | Legend, search, hover, group selector, detail panel | Most interactive deliverables |
| Multi-view site | Several graphs, about pages, zoom-level labels | A project with several questions or periods |

If the brief lists search, filtering or details, reject a zoom-only viewer.

## 3. Renderer and library by size class

Pick by capability first. Libraries below are examples from the asset catalog; read each license through `find-assets` and confirm the current version and API in the library's own documentation.

| Size class | Renderer | Capability needed | Example libraries (catalog id) |
| --- | --- | --- | --- |
| Small (tens) | SVG | Full styling control, accessible DOM, easy print | `d3` force simulation; a `diagram` tool when hand placement is better |
| Medium (hundreds) | SVG or canvas | Force layout, hover, zoom, collision | `d3`, `cytoscape`, `g6` |
| Large (thousands) | WebGL or canvas | GPU rendering, precomputed layout, label density control | `sigma` with graphology, `g6`, `cytoscape` (canvas) |
| Very large (tens of thousands and more) | WebGL | GPU rendering, level of detail, aggregation, offline layout | `sigma`, `deckgl` graph layers |
| Analysis plus layouts in one package | Canvas | Built-in graph algorithms and many layouts | `cytoscape` |
| 3D network view | WebGL | Rotation; only when z encodes an attribute | `react-force-graph` |

Defaults and reasons:

- Default: SVG up to a few hundred nodes; above that, canvas; above a few thousand, WebGL. Measure frame rate on the target device before you decide.
- Default: compute the layout offline or once on load, save positions, and stop the simulation. Live physics on thousands of nodes costs battery and frame rate.
- Default: send the published subset only. Never ship filtered-out data in the page bundle.
- In a sourced data page (the `dataviz` capability, for example the Claude Data type), only the type's bundled chart library runs. A force layout there is written with its `d3`, kept to small and medium graphs. Read the [claude-data](../../../references/tools/claude-data.md) card.

## 4. The content sheet

Fill this with the user before building the page.

```
Title: <...>                      Author or organisation: <...>
Short description (2 sentences or fewer): <...>
Long description (on demand, formatted): <...>
Node = <...>   Edge = <...>   Color = <...>   Size = <...>
Group field for the selector: <field>; display names for each value
Detail panel fields per node type: <list>; fields to hide: <null, zero by design>
Search: <yes | no>; Direction grouping in panel: <yes for directed>
About view: data source with link, objective, how measures were computed, author
Privacy: names <real | pseudonymised>; data shipped <published subset only>
```

## 5. Interaction set

Each item has a check.

| Interaction | Behaviour | Check |
| --- | --- | --- |
| Legend | Node, edge, color, size lines | Four lines present; missing one fails |
| Title and descriptions | Title and author on load; short text visible; long text from an info control | Short text two sentences or fewer |
| Search | Type a label; the node is found and focused | A known label returns its node; duplicates are listed and distinguishable |
| Hover or select | The node and its neighbours keep full strength; all else dims | Leaving restores the view |
| Group selector | Pick a group to highlight or show its members | Readable names and member counts, never "Group 4" |
| Detail panel | Attributes plus neighbours as links; clicking a neighbour selects it | No null or structurally zero rows; in and out neighbours apart on directed graphs |
| Label tiers | Top tier at load; more labels as zoom grows | No overlaps at default zoom |
| Zoom and pan | Zoom in, zoom out, reset, drag to pan, full screen | All work by pointer; reset returns the start view |
| Keyboard | Tab to controls; arrow keys or buttons pan; plus and minus zoom; search reachable | Visible focus on every control |
| Filters | Degree, weight, group and time filters as controls | Active filters always visible with counts |
| Table view | The same nodes as a sortable table | Reachable by keyboard; the accessible form |

Rules:

- The default view must already read as a still image. Interaction deepens a readable picture; it does not rescue an unreadable one.
- Put filter and selection state in the URL when the page is shared, so a link reopens the same view.
- Hover is never the only way to see a value. Selection by click or keyboard shows the same detail.
- Under reduced motion: no animated zoom flights, no autoplay, no settling animation on load.

## 6. Accessibility of the page

- The canvas or SVG has a text alternative: the text summary and a link to the table view.
- Controls are real buttons and inputs with labels.
- Label text 4.5:1 or more on its ground; nodes and story edges 3:1 or more; in every theme.
- Group colors differ for color-vision deficiency; the selector and legend also name each group.
- Focus is visible and never hidden behind the canvas or a sticky header.

## 7. Performance

- Default: hold about 60 frames a second during pan and zoom at the target size on a mid-range device. Measure; do not assume.
- Load the layout positions with the data; do not compute a large layout in the reader's browser.
- Use level of detail: hide labels and thin edges when zoomed out; show them on zoom.
- Pause rendering when the page or tab is hidden.
- Keep the data file small: drop unused attributes; round coordinates.

## 8. Static export

1. Choose a light preset for print; a dark ground is allowed on screen. Check label and edge contrast against whichever ground you use.
2. Export SVG (elements ungroup cleanly) or PDF (may need ungrouping and removal of transparent layers).
3. Open the file in a vector editor or in code. Ungroup.
4. Recolor only the few elements that need emphasis, from tokens.
5. Add a title, a callout on the key node or cluster, and thin pointer lines, in the brand type.
6. Move crowded labels by hand. No label overlaps another label or a key node.
7. Export the final file and keep the editable source.
8. For slides and social images, recompose for the frame. Do not shrink a wide graph into a square; crop to a focus view and state the crop.

## 9. The file set

| File | Purpose |
| --- | --- |
| `<name>.gexf` or `.graphml` | Styled master with positions, colors, sizes |
| `<name>-master.svg` or `.pdf` | Vector master for print and editing |
| `<name>@2x.png` | Quick share and previews |
| `<name>-table.csv` | Ranked node table, the accessible form |
| `site/<version>/` | The interactive page, one folder per export |
| `network-plan.md` | Definitions, statistics, layout record, filters, encoding |

## 10. Deployment and testing

- Export each version to a new, numbered folder. Exporters often overwrite their target folder, and hand edits are lost.
- Keep custom styles and text in a separate tracked file that you re-apply after each export.
- Test the page over HTTP from a local server, not from the file system. Some browsers block scripts or data on a locally opened file.
- Test in two browsers at least: load, search, group select, hover, node click, neighbour links, zoom, reset, keyboard.
- GATE: publishing, deploying or sharing a link is exposure. Get a yes. For a network of people, the privacy answer comes first.
- GATE: a hosted deploy or a paid service is a spend call when it bills. Read the price live, show it, get a yes, call once.

## 11. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Interaction as rescue | The default view is a hairball "but you can zoom" | Fix layout and filters until the still reads |
| Renderer by habit | SVG with five thousand nodes stutters | Choose the renderer by size class; measure |
| Unlabelled legend | Colors with no names | The four legend lines |
| Panel noise | Rows of "null" and zeros | Prune fields by node type |
| Lost hand edits | Custom styles gone after re-export | Versioned folders; tracked patch file |
| Full data shipped | The page bundle holds filtered and private rows | Ship the published subset only |
| File-system testing | Works on the author's machine, blank for others | Test over HTTP in two browsers |
