# 21st.dev

Catalog entry: [21st-dev.json](../../catalogs/tools/21st-dev.json). Source: https://21st.dev

Terms in this card. A component is a React and shadcn interface component; its search id is a numeric demo id. A theme is a set of CSS custom properties; its id is a uuid. A template is a full site or page listing with a price and a URL. A video block is a Remotion component. A take is one variant of a design the user generated on 21st. A retrieval is one `get_component` call that returns source code.

## What it makes

- Candidates for interface sections: components with a preview image, a preview clip, an author and an install command.
- Themes: complete light and dark token CSS for a Tailwind and shadcn app, with chart colors and font variables.
- Template listings: a price and a URL. No tool returns template code.
- Short videos from brand-bound Remotion blocks in a hosted editor, exported as MP4.
- Existing third-party brand marks as SVG through `search_logo`. It does not design logos.
- Reference material for mood boards: preview images, clips, posters and loops.
- It makes no 3D model, no capture and no site deployment. It publishes only to its own marketplace.

## Connection and auth

- The connector signs in with the user's 21st account.
- A coding host can register the remote server with a bearer token from the environment variable `API_KEY_21ST`.
- Install commands embed `$API_KEY_21ST`. The variable must exist in the shell. Never write the key into a file.
- The hosted generation tools (`generate`, `iterate_generation`) appear only when the account has that entitlement.
- Call `get_usage` to read `aiGenerationEnabled`. When it is false, search, retrieve and adapt locally.
- Team libraries need team membership on 21st.

## Cost model

- Free: `search`, `search_picker`, `get_inspiration`, `search_logo`, `get_theme`, `get_usage`, bookmark and team list tools, `video_list_blocks`, `video_search_blocks`.
- Free: `get_take`, `get_generation`, `get_generation_job`, `get_notes`, `get_changes`, `edit_take`, `update_note`.
- Metered: `get_component`. Each call uses one retrieval from a small daily quota. It can return a paywall in place of code.
- Metered: `video_export` uses the plan's export quota and can return `blocked`. A cached export is free.
- Limited: `video_snapshot` has a small hourly preview budget.
- Paid: hosted generation needs its own entitlement and credits. Paid component access does not grant it.
- Paid templates: the price is in the search result. Purchase happens on the site, not through a tool.
- Not stated: whether video project creation, operations, variants or uploads use a quota. Treat each as an account write that needs consent.
- Live quote: call `get_usage`. It returns the tier, the retrievals left, the credit state and the reset date. `get_component` also returns `structuredContent.quota`.
- GATE: get the user's yes before each `get_component` and each `video_export`.

## Call order

No init call exists. Call `get_usage` once at the start of a session.

Component into a project:
1. Call `search` for an agent lookup. Call `search_picker` when the user should choose visually.
2. Call `get_inspiration` when the project's design context should rank the results.
3. Shortlist from metadata only: name, description, preview image, preview clip, URL.
4. GATE: call `get_component` with the demo id only for the chosen item and only with consent.
5. Check `structuredContent.locked` and `found` before you treat the text as source.
6. Re-implement the idea with the project's own primitives and tokens.

Theme into a project: call `search` with `type: "theme"`, then `get_theme` with the uuid. Both are free.

Template: call `search` with `type: "template"`. Add `free: true` to filter. Open the URL.

Video:
1. Call `video_search_blocks` or `video_list_blocks`. Read each block's `fields` and `propsSchema`.
2. Call `video_create_project` with a block sequence and a size.
3. Call `video_get_doc` to verify the draft and read the current `rev`.
4. Call `video_apply_ops` with `baseRev`. On a conflict, read again and plan again. Do not resend old operations.
5. Call `video_snapshot` to review a frame.
6. Upload assets: `video_upload_asset`, PUT the bytes, then `video_finalize_asset`.
7. GATE: call `video_export`, then poll `video_export_status` for the download URL.

Take handoff: call `get_generation` with the project id, confirm the take with the user, call `get_take`, then read `get_notes` and `get_changes`.

## Key tools

| Tool | Use it when |
|---|---|
| `get_usage` | A session starts. You need the retrieval quota and the hosted generation state. |
| `search` | You need candidates across components, themes and templates. |
| `search_picker` | The user should see the candidates and choose. |
| `get_inspiration` | Ranking should respect project context. It returns a confidence and a rationale for each result. |
| `get_component` | One chosen component needs its source, demo, install command and dependencies. |
| `get_theme` | A project needs a starting token set. |
| `search_logo` | A page needs an existing third-party mark, for example in an integration row. |
| `video_search_blocks`, `video_list_blocks` | You plan a motion piece and filter by job, energy, kind and size. |
| `video_create_project`, `video_apply_ops` | You build or edit a hosted video with typed operations. |
| `video_snapshot` | You review one frame before export. |
| `get_take` | The user sketched a design on 21st and wants it rebuilt in the codebase. |
| `list_bookmarks`, `get_bookmark_list` | The user keeps a saved reference set on 21st. |

## Inputs

- A plain-language need, for example "pricing table" or "dark theme".
- For `get_inspiration`: the project's `.21st/design.json` object, only when the user asks for project-aware search.
- For video: aspect ratio, real on-screen copy, brand colors, fonts, light and dark logo files and motion energy.
- For video blocks marked `requiresScreenshot`: the screenshots.
- For a take handoff: the project id and the take number.
- Consent before each retrieval and before any account write: bookmarks, lists, video projects, uploads, exports, profile, publishing.

## Outputs and how to bring them into a project

- Search result: type, id, name, description, preview image URL, preview clip URL, author, install command, page URL.
- Theme CSS: a `:root` block, a `.dark` block and an `@theme inline` block in Tailwind v4 syntax.
- Theme into Tailwind v4: paste the CSS into the global stylesheet, then tune it to the brand.
- Theme into Tailwind v3: drop the `@theme inline` block and map the tokens in the Tailwind config.
- Component: default to reference, credit and re-implement. Keep the author and the page URL as a credit line.
- Component install is a per-component decision by the user. The install command runs the shadcn registry installer.
- Logo: fetch the SVG URL and the dark variant when present. Save each as a file.
- Preview images and clips: link them in a mood board. Do not ship them as product assets.
- Video: download the exported MP4 at once and store it in the project. Or install the block into a Remotion project.
- Write a provenance record in `design/assets/manifest.json` for every file that enters the project.

## Handoffs

- From a brand kit or a Claude Design system: pass colors, fonts and logos into the video `brand` operation or into theme search.
- This server has no import tool for a Claude Design canvas.
- Theme out: the CSS variables are plain shadcn tokens. Use them as a token source for any builder or design file.
- Component to a design file: build it locally, then push the rendered page with a code-to-design tool.
- Take to code: the `copyPrompt` text is written for a coding agent. Hand it to the coding harness.
- Generated media in: an image, clip or voice track from another tool enters through the video asset upload tools.
- Video out: the MP4 or the installed block goes to the repository, an asset library or a host.
- References out: preview and poster URLs feed any board tool.

## Limits and failure modes

1. The free retrieval quota is tiny. Plan for metadata-only work.
2. `get_component` can succeed without code. Check `locked` and `found` first.
3. `search_logo` returned an empty list for three well-known brands. Treat an empty result as a possible outage. Use another SVG source.
4. Theme search is literal. A three-word query returned nothing and a one-word query returned results. Use short queries and the `color` filter.
5. Theme results carry no preview image and no description. Fetch the CSS and render a swatch locally to judge it.
6. `limit` defaults to 8 and stops at 30. A request can return fewer items than asked.
7. The filters `author`, `mine` and `liked` bypass ranking and ignore `query`, `sort`, `tag` and `color`.
8. `mine` and `author` show public components only. Private and team components come from `list_team_components`.
9. A bare "video" query stays in the interface catalog. Pass `runtime: "remotion"` for video blocks.
10. Ids differ by type: a numeric demo id for a component, a uuid for a theme, a numeric id with no code tool for a template.
11. Results carry no license field. Treat catalog code as a credited reference unless the component page states a license.
12. Remotion blocks carry their own Remotion license line. Read it before use.
13. Catalog quality varies. It is a community marketplace. Judge by the preview, not by rank.
14. A popular component used unchanged makes the work generic. Restyle with project tokens and change layout or motion.
15. Video edits use optimistic concurrency. Always send the latest `baseRev`. The user may edit in the browser at the same time.
16. Hand-set fields in a video survive an edit unless `force` names them.
17. Export URLs are short-lived. Upload URLs are presigned and need the exact returned content type.
18. Video block text limits are strict. Write copy to the field limits in `fields`.
19. `video_create_project` accepts 40 operations at most.
20. `delete_template` is a hard delete. `edit_profile` replaces the whole board. A `tags` argument replaces the full set.
21. Use no destructive or publishing tool without an explicit user request.
22. `send_feedback`, `record_take_outcome` and `record_inspiration_feedback` must never carry source code, paths, prompts or project details.
23. `latest: true` on `get_take` only suggests a take. Confirm the take with the user before you fetch it.
24. Report real typecheck and build results in `record_take_outcome`, and only with the user's approval.

## Best for

1. A starting point for a web or dashboard section in a React, Tailwind and shadcn project, with a preview for each candidate.
2. A complete light and dark token set at no retrieval cost, tuned to the brand afterward.
3. A short product or launch video from brand-bound Remotion blocks, with frame snapshots for review.

## Wrong for

An original logo or brand identity. `search_logo` only looks up existing third-party marks, and no tool here draws a new one. Use a vector generation tool and the logo skill.

## Evidence

VERIFIED on 2026-11-23 for catalog search and theme retrieval. Other surfaces carry the labels below.

- VERIFIED by live calls: `search` for components, themes and templates; `get_inspiration`; `get_theme` (full CSS returned); `get_usage`; `video_list_blocks`; `list_teams`; `list_bookmark_lists`.
- DOCUMENTED from schemas only: `get_component`, every video project, snapshot and export tool, the take handoff tools, `search_picker`, the logo response shape.
- UNTESTED: source retrieval, video export, hosted generation (absent from the tool list), team libraries.
- Unverified: paid tier limits; the schema of `.21st/design.json`; component license terms on the site; the cause of the empty logo results.
