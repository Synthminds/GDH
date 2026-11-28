# Meshy

Catalog entry: [meshy.json](../../catalogs/tools/meshy.json). Source: https://docs.meshy.ai/api/ai.md

Terms in this card. A task is one asynchronous job that the service runs and the agent polls. A preview is geometry with no texture; a refine adds texture to a preview. Printability is the service's own check for watertightness, holes and non-manifold edges.

## What it makes

- A 3D model from text, from one image, or from two to four views of the same object.
- Textures, a remesh to a target face count, a format conversion (STL and 3MF among them), a resize to real dimensions, UVs.
- Print tools: a free printability analysis, a printability repair, an automatic split into parts that print on their own, a multi-color 3MF, and a relief from a photo as a millimetre STL.
- A local command that opens a finished model in an installed slicer.
- It does not design fits. Holes, clips and mounts come from the parametric route in `print-design`.

## Connection and auth

- An official stdio MCP server, started with `npx` from the package `@meshy-ai/meshy-mcp-server`. Name the server `meshy` in `.mcp.json` so its tools start with `mcp__meshy__`.
- The API key sits in `MESHY_API_KEY` on the user's machine. Never ask for the key in chat. In a cloud session, ask for it through the credential tool for the API host.
- The REST API uses a Bearer key on `api.meshy.ai`. The MCP server wraps it; prefer the server.
- Downloads land in `./meshy_output` by default. Point the output inside the project, under `design/print/<part>/source/`.

## Cost model

- Credits are charged when a task is created. A failed task is refunded.
- Free calls: the balance, the printability analysis, the local slicer command. Assume every other call spends until its doc says otherwise.
- GATE: read the balance, quote the call, get a yes, call once.
- Never send the same create call again after a timeout or a server error. There is no idempotency key, so a repeat starts and charges a second task. List the newest tasks first.
- A pending task can be cancelled for a refund. A running one cannot.

## Call order

1. Read the balance.
2. Write the prompt or prepare the views. Three or four views of the real object give the best match.
3. GATE: an image upload is exposure. Ask before you send the user's photos.
4. Create the task. Poll at the interval the service sends back. A task can return to pending; that is not a failure. Wait an hour before you call it stuck.
5. Download every file the moment the task succeeds. Links expire, and API assets are deleted after three days on non-Enterprise plans.
6. Run the free printability analysis, then the GDH mesh check. Repair, solidify and scale as `print-design` says.
7. Record the task id, the prompt or the image source, the plan and the license line in the asset manifest.

## Key tools

| Job | Call |
| --- | --- |
| Credits left | the balance call |
| Model from text | text-to-3D preview, then refine for texture |
| Model from photos | image-to-3D, or multi-image-to-3D with two to four views |
| Make it printable | analyze printability (free), then repair printability |
| Too big or too complex | auto split into printable parts |
| Color print | multi-color print to 3MF |
| Photo to plaque | relief to STL |
| Open in a slicer | send to slicer (local; no API call) |

Read the server's tool list in the session for exact names and parameters. They change between versions.

## Inputs

- Text, or one to four images with the object on a plain background.
- Target real size in millimetres, for the resize step.
- A face count target for the remesh, matched to the nozzle.

## Outputs and how to bring them into a project

- GLB, FBX, OBJ and USDZ from generation; STL, 3MF and others from conversion.
- Save under `design/print/<part>/source/`. Treat each file as a draft until the GDH mesh check passes.
- Record the origin as `generated`, with the tool, the task id and the plan, in `design/assets/manifest.json`.

## Handoffs

- `print-design` repairs, scales, adds functional features and slices.
- `three-d` takes a GLB for the web.
- `find-assets` records the license line.

## Limits and failure modes

- Output license depends on the plan. On the free plan, Meshy owns the output and licenses it under CC BY 4.0, so a printed or shared object needs credit to Meshy. On a paid plan, the customer owns the output. Record which applies.
- On non-Enterprise plans, inputs and outputs may be used to train the service. Do not upload a client's unreleased product or a private photo without the user's yes and that warning.
- A generated mesh often has a skin with no wall, invented back faces from a single photo, and detail finer than a nozzle can print.
- The free plan may not download the newest model versions. Check the plan before a promise.
- The terms page showed a last-updated date after the day it was read. Read the terms again before you quote them.

## Best for

- Organic, decorative forms: figures, sculptural planters, ornaments, plaques, character pieces.
- A first form from photos of a real object.
- Splitting a large model into printable parts.

## Wrong for

- Parts that must fit, clip, screw or carry load. Model those parametrically.
- Exact dimensions. Generated scale is arbitrary until resized.
- Private or client material on a plan that trains on inputs.

## Evidence

DOCUMENTED. On 2026-11-27 the API and MCP documentation, the asset retention page, the 3D printing platform pages and the terms of use were read. The server was not connected in a GDH session. No balance call and no task ran. Credit amounts and plan prices were not recorded; read them live.
