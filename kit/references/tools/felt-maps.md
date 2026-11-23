# Felt Maps

Catalog entry: [felt-maps.json](../../catalogs/tools/felt-maps.json). Source: https://felt.com

Terms in this card. A map is one Felt map with a `map_id`. A layer is one data set on a map. A component is a chart, a stat card or a filter beside the map. A print page is a designed sheet that holds maps, legends and text.

Read this first. In the research session every map tool was blocked: the workspace plan did not include MCP access. This card is written from tool schemas alone. Treat every step below as UNTESTED until one call succeeds.

## What it makes

- Web maps with data layers: location maps, coverage maps and choropleths.
- Charts and filters linked to a map: stat card, bar chart, histogram, line chart, time series.
- Map images for a page or a report: PNG, JPG, PDF or SVG.
- Print-ready map sheets with a legend, a locator map, text, images and sections.
- Numbers from raster layers, for example elevation or land cover, to drive a legend or a callout.
- Map visualization only. It does not make any non-geographic chart or diagram.

## Connection and auth

- Attach the connector and sign in with the user's Felt account.
- MCP access depends on the workspace plan. The refusal text named the Business plan or higher, as read on 2026-11-23. A workspace admin changes the plan in workspace settings.
- Without that access, the server says only `who_am_i`, `help_center` and `developer_docs` work. It also says: do not try the other tools.
- Of those three, only `developer_docs` had a schema in the researched session.
- ASK: before any map work, ask whether the workspace plan includes MCP access. A plan change is the admin's decision.

## Cost model

- No schema holds a price for a call. Access is gated by plan, not by credits.
- No spend call was found. No tool returns a quote or a balance, and none is needed.
- The risk is data change, not money. Several tools write or delete with no undo.
- GATE: `set_map_sharing` changes who can open a map. Call it only on request, and call `get_map_sharing` first.
- GATE: `add_url_to_map` sends a data URL to Felt. Get a yes before you add client data.

## Call order

From the tool descriptions. None of these steps ran.

1. Get a `map_id`. Almost every tool needs one. No create-map tool was in the researched session, so the user supplies a map or its URL.
2. Call `list_map_layers`. Then inspect a layer for its column names before you style, chart or edit.
3. For places: call `get_geocoding_guidance` before `search_places`. Call `resolve_places` to get coordinates. Never estimate coordinates.
4. For a print page: call `get_print_item_guidance` before `create_print_page` or `upsert_print_items`. Call `list_print_layouts` for a starting layout.
5. For a data edit: call `get_sql_editing_guidance` before `edit_features`.
6. For sharing: call `get_map_sharing` before `set_map_sharing`.
7. Export with `export_map_image` or `export_print_page`. Download the file at once.

## Key tools

| Tool | Use it when |
|---|---|
| `developer_docs` | You have a question on the Felt JavaScript SDK, the REST API, embedding or the Felt Style Language. It works without plan MCP access. |
| `add_url_to_map` | You import GeoJSON, CSV, Shapefile, ArcGIS or WMS data from a URL as a layer. Processing is asynchronous. |
| `list_map_layers` | You need to see what a map holds, in legend order. |
| `create_layer_component` | You add a stat card, a chart, a time series or a filter beside the map. |
| `update_map_properties` | You set the title, the description, the basemap, the initial view, or the pan and zoom limits. |
| `export_map_image` | You need a PNG, JPG, PDF or SVG of one view, with a legend and a scale bar. |
| `create_print_page`, `upsert_print_items` | You design a sheet: a standard or custom paper size, with maps, locator maps, legends, text and images. |
| `export_print_page` | You print a designed page to PDF, PNG, JPG or SVG. Several pages become one PDF. |
| `get_raster_stats`, `get_raster_histogram`, `sample_raster_value` | You need numbers from a raster layer. |
| `search_places`, `resolve_places` | You geocode names or addresses. One call takes up to 24. |
| `set_map_sharing` | The user asks to change link or workspace access. |

## Inputs

- A Felt map: its id or its URL.
- The data source: a public URL to a file or a service, or a workspace table.
- The column that drives color or size.
- The area to frame.
- The brand basemap color. The basemap takes a preset (default, light, dark, satellite), a hex color or a tile URL.
- The output size and format. Paper sizes include Letter, A4, A3, tabloid and custom, in inches, centimeters, millimeters or pixels.
- An admin decision on the plan, when access is blocked.

## Outputs and how to bring them into a project

- A Felt map URL for embedding. Read the SDK and iframe details through `developer_docs`.
- `export_map_image` and `export_print_page` return a `download_url` that expires. Download the PNG, SVG or PDF into the repository.
- An image export goes up to 16384 px on a side, per the schema.
- SVG keeps data layers, legends and text as vectors over a raster basemap. That suits further editing in a design tool.
- The agent cannot view the image it exports. Ask the user to check the downloaded file.
- Write a provenance record in `design/assets/manifest.json` for every exported file. Record the data source and its license.

## Handoffs

- Out: an exported SVG or PNG goes into a page, a deck or an infographic as a placed image.
- To a Claude Design canvas: place the exported image by hand. No "Send to" target and no import tool exist here.
- In: a brand hex color into the basemap, for a quiet branded ground.
- In: data prepared in a spreadsheet or a warehouse reaches Felt as a URL.
- In: a brand logo goes on a print page as an `image` item.
- To a dashboard page: embed the map URL. The linked charts and filters stay inside Felt.

## Limits and failure modes

1. Blocked by plan in the research session. Do not call map tools until the plan includes MCP access. The server asks for this.
2. Descriptions name tools that were absent from the session: `inspect_layer`, `generate_fsl`, `help_center`, `who_am_i`, `upsert_annotations`, `poll_layer_processing_status` and any create-map tool.
3. Because of item 2, styling a layer and creating a map may not be possible through the connector.
4. The agent cannot view the image it exports.
5. `edit_features`, `remove_layer` and the delete tools have no undo. Get a yes first.
6. Layer components bind by a column's `storage_name`. SQL edits use the `display_name`. A mix of the two fails.
7. `search_places` does not do category searches.
8. A component's type cannot change after creation. Default: delete it and create a new one, with the user's yes.
9. `add_url_to_map` processes data asynchronously. The tool that polls the status was absent from the session.
10. Never estimate coordinates. Resolve each place with the geocoding tools.
11. A wrong number on a map is a factual error. Use only data the user supplied, and name its source on the map.

## Best for

These jobs hold once access exists.

1. A branded location or coverage map, exported as SVG for a website or a report.
2. An interactive choropleth with linked charts and filters, embedded in a dashboard page.
3. A print-ready map sheet with a legend, a locator map and a logo.

## Wrong for

Any non-geographic chart or diagram. While the workspace plan lacks MCP access, the tool serves no job at all.

## Evidence

DOCUMENTED on 2026-11-23. The basis is tool schemas only.

- Exercised: the tool schemas in the session. One data call, `get_print_item_guidance`, was made and refused for lack of plan access.
- Not exercised: every map tool. No map was read, changed or exported. The print, geocoding and SQL guidance texts were not read. `developer_docs` was not called.
- Every capability in this card is UNTESTED in practice. Do not make this tool a required step until one call succeeds.
- Absent from the session: the tools listed in limit 2.
