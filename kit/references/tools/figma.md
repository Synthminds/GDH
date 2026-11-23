# Figma

Catalog entry: [figma.json](../../catalogs/tools/figma.json). Source: https://www.figma.com

Terms in this card. A file key is the id in a Figma file URL. A session is the id that `create_session` returns for one task. A shader is a WebGPU effect or fill. A generative plugin is a reusable canvas tool with a panel. A code layer is a runnable code project placed inside a Figma file. Weave is a separate paid service that runs named image and video models.

## What it makes

- Editable design layers from self-contained HTML: a brand sheet, a mood board, a screen or a component set.
- A code layer or a Figma Make file from a local code project.
- Shaders: a static or animated effect or fill. The source also runs in a React project.
- Generative plugins: a canvas tool with a panel that a designer reuses.
- Raster images placed into a frame, and editable vector icons and illustrations.
- A change list from reviewer comments on a file.
- Images and video from a named model through Weave, when the account is linked.
- It makes no hosted site and no working app. Output stays inside Figma, except shader source and image files.

## Connection and auth

- The connector signs in with the user's Figma account.
- The tool set differs by session. Check the tool list before you choose a path.
- The researched session exposed only these groups: session, branch, shader, plugin, generation, comments, the two import tools and three Weave tools.
- Documented but absent in that session: `use_figma`, `get_design_context`, `get_screenshot`, `get_metadata`, `get_variable_defs`, `get_motion_context`, `get_figjam`, `download_assets`, `upload_assets`, `export_video`, `create_new_file`, `generate_figma_design`, `generate_diagram`, `search_design_system`, `get_libraries`, the Code Connect tools, `whoami`, `get_figma_skill`, `weave_list_tools`, `weave_run_tool`, `weave_upload_asset`.
- The cause of the gap is unknown: a connector setting, a plan limit or a staged rollout.
- Name the fallback for each absent tool. Example: without `create_new_file`, ask the user for a file URL.
- The server also serves MCP resources: docs, skills with reference files and a React shader runtime.
- Weave needs its own link, made in the Weave profile settings. `weave_find_model` says so when the link is absent.
- Preflight: call `list_shaders`. It is a free read and proves the sign-in.

## Cost model

- No credits, per the server's rate-limit document: list and read tools, `create_session`, `html_to_figma`, shader and plugin create and update, and the first `send_code_to_figma` import.
- Spend, Figma AI credits from the destination file's plan: `generate_image` and `generate_vector_illustration`. Each call is one charge. The image cost varies by model.
- Spend, Weave credits from a separate paid Weave account: `weave_run_model`.
- Live quote for Weave: call `weave_run_model` without `acknowledgedCost`. That call only quotes.
- No tool returns a quote or a balance for Figma AI credits. Ask the user to read it in Figma.
- Read tools are rate limited by seat. Write tools are exempt.
- On the read date: a View or Collab seat got about 20 read calls a month. A Full or Dev seat got 200 a day, or 600 a day on Enterprise.
- Read the current limits in `file://figma/docs/rate-limits-access.md`. The seat type comes from `whoami`; when it is absent, ask the user.
- GATE: before each generation call, name the tool and the credit pool. Get a yes. Call once.

## Call order

1. Get the file key from a Figma URL that the user supplies: `figma.com/design/<fileKey>/...`.
2. For a branch URL, use the branch key as the file key. Convert `node-id=1-2` to `1:2`.
3. Call `create_session` with the file key and a short task description. Do this once, before any file tool, also for read-only work.
4. Pass the returned id as `sessionId` on every later file call for that task.
5. For imports, make one fresh UUID for each user prompt. Pass it as `promptId` on every `html_to_figma` and `send_code_to_figma` call for that prompt.
6. Load the matching skill first from `skill://figma/<name>/SKILL.md`: `figma-shaders` before a shader write, `figma-generative-plugins` before a plugin write, `figma-code-workflows` before `send_code_to_figma`.
7. A shader or plugin create needs a `planKey` in the form `team::<id>` or `organization::<id>`. Its documented source is `whoami`. When that tool is absent, ask the user.
8. Create is two steps. Create a starter, read its source, then call the update tool with complete replacement files. Never stop after create.
9. Weave: call `weave_find_model`, then `weave_run_model` for the quote, get approval, run, then `weave_get_model_run_output`.

## Key tools

| Tool | Use it when |
|---|---|
| `create_session` | Always first, once the file key is known. |
| `html_to_figma` | You hold self-contained HTML and want editable layers. `cssSelector` makes each matching element its own frame, up to 20 in one call. |
| `send_code_to_figma` | The user explicitly asks for a runnable code layer or a Make file from a local project. |
| `list_shaders`, `get_shader` | You pick or read a first-party effect or fill: halftone, dither, CRT, bloom, mesh gradient, nebula, caustics, moire and more. |
| `list_file_shaders` | You read the shaders that one file uses, also ones the user does not own. |
| `create_shader`, `update_shader` | You author a new effect or fill. The source is one `main.ts` file. |
| `create_generative_plugin`, `update_generative_plugin` | You build a reusable canvas tool with a panel (`code.ts` and `ui.html`). |
| `generate_vector_illustration` | A mark, an icon or a spot illustration must be an editable vector. Set `kind` to `icon` or `illustration`. Spend call. |
| `generate_image` | A raster image must land in a frame. Read the model list and the default from the schema. Spend call. |
| `get_comments` | A refinement round needs the reviewer feedback. Filter by node, page, unread or resolved. It does not mark comments read. |
| `weave_find_model`, `weave_run_model`, `weave_get_model_run_output` | The user names a specific image or video model. |
| `create_branch` | Only when the user explicitly asks for a branch. Organization and Enterprise plans only. |

## Inputs

- A Figma Design file URL with edit access. Without `create_new_file`, the agent cannot create a file.
- A `planKey` for shader or plugin authoring.
- Brand tokens, fonts and images embedded in the HTML. The import fetches no external URL. Inline every image as a data URI.
- The user's answer to "editable design layers or a code layer?" when the request does not say.
- Approval of the cost before any generation call.

## Outputs and how to bring them into a project

- `html_to_figma`: the tool returns a single-use URL. POST the HTML to it with `Content-Type: text/html`. The response gives the file URL and the new node ids. The result stays in Figma.
- `generate_image`: the result holds `image.url` and curl instructions. Download the file into the project's asset folder.
- `generate_vector_illustration`: the result is a node id only. SVG export needs `download_assets`. When that tool is absent, the user exports the SVG in Figma.
- Shaders: `get_shader` returns file URIs for `main.ts`, the compiled `.build/main.js` and `features.json`.
- Shader in React: copy the served runtime (`ShaderEffect.tsx`, `ShaderFill.tsx`, `useShaderRuntime.ts`) and the source into the project. The docs say correct display needs HTML-in-Canvas.
- Shader or plugin authoring: return the try link `https://www.figma.com/file/new?try-tool-resource-content-id=<id>&try-tool-resource-type=<gen_effect|gen_fill|gen_tool>&type=design&mode=design`.
- Weave runs: output URLs with curl instructions. Prefer the URL download over inline media.
- Write a provenance record in `design/assets/manifest.json` for every file that enters the project.

## Handoffs

- From a Claude Design canvas or any local HTML: export one self-contained HTML document, then call `html_to_figma`. This server has no "Send to" import tool.
- From a code project: `send_code_to_figma` takes a git source, a GitHub source or an archive upload.
- From a code builder: take a static HTML render of the generated app and call `html_to_figma`.
- To Picsart scenes: `picsart_scene_import_figma_paint` accepts CSS paint copied from a Figma layer.
- To GetLayers: `getlayers_figma_match` expects a frame read through this server. That route fails when the design read tools are absent.
- To code: shader source and runtime. Full design-to-code needs `get_design_context`. Load the `figma-design-to-code` skill before you call it.
- To a refinement round: `get_comments` feeds the change list.

## Limits and failure modes

1. `html_to_figma` makes plain layers. It does not use the file's components, variables or libraries.
2. `html_to_figma` works on Design files only. The cap is 50 MB with images.
3. `html_to_figma` does not run an app and does not capture a live site. For an outside site, the docs point to the Figma Chrome extension.
4. `send_code_to_figma` creates no design shapes. Do not offer it as a way to get editable layers.
5. A successful or changed code import cannot be replaced.
6. Never resume a failed upload. Never retry an ambiguous import failure. Continue within one hour of the upload.
7. When the user does not say where the code goes, ask "editable design layers or a code layer?" and stop.
8. A shader update replaces the whole `main.ts`. The `kind` cannot change. No new file can be added.
9. On a shader build error, fix once and retry once. Then report.
10. Set `metadata.isAnimated` when the shader reads frame time. Set `metadata.usesMouse` when it reads the pointer.
11. When the tool reports that animation is unavailable, treat that as final.
12. Others with access can read plugin and shader source. Never embed a secret.
13. Image size is approximate. Width and height only pick an aspect ratio. The maximum is 2048 px.
14. The generation tools reject nested instance node ids such as `I1:2;3:4`.
15. Without `whoami`, the plan, the seat, the rate tier and the `planKey` are unknown. Ask the user.
16. A low seat tier can exhaust its read calls in one task. Plan reads and batch them.
17. The Figma skills in a host plugin take precedence over the skills that the server serves.

## Best for

1. Pushing an HTML brand sheet (palette, type scale, logo lockups) or a mood board into a file that a designer refines.
2. Authoring a custom animated shader fill or effect for a hero background, then reusing the source in React.
3. Pulling unresolved comments on a frame and turning them into the change list for the next round.

## Wrong for

A deployed, working web app or dashboard. Figma output is layers, shaders and code layers inside Figma, not a hosted site. Use a code builder and a deploy tool.

## Evidence

DOCUMENTED on 2026-11-23.

- VERIFIED by live calls: `list_shaders` and `list_generative_plugins` succeeded. `weave_find_model` answered that the account is not linked to Weave. The MCP resources were readable.
- DOCUMENTED from schemas, server instructions and served files: every tool in this card; the docs `tools-and-prompts.md`, `rate-limits-access.md` and `generative-plugins-and-shaders.md`; the skills `figma-shaders`, `figma-generative-plugins` and `figma-code-workflows`.
- UNTESTED: `create_session`, `get_comments` and `list_file_shaders` (no file key was available); `html_to_figma` and `send_code_to_figma` (writes); every generation call; shader and plugin authoring; every Weave run.
- Absent in the researched session, so UNTESTED: the design read and write core listed under Connection and auth.
- Unverified: credit prices for image and vector generation; the Weave model list and prices; the content of eleven other Figma skills, read by description only.
