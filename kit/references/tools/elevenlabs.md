# ElevenLabs creative tools

Catalog entry: [elevenlabs.json](../../catalogs/tools/elevenlabs.json). Source: https://elevenlabs.io

Terms in this card. A flow is one editable canvas that holds generations as nodes. A node is one step on a flow. A take is one variation from a generation. A brand kit is a stored set of palette, fonts, logos, rules and a voice. A signed link is a download URL that expires.

Scope: the `creative_*` tools. The same server holds `agents_*` tools for voice agents. They are outside this card.

## What it makes

- Audio: speech and voiceover, designed voices, sound effects, music, dubbing, voice change, noise removal and a mix.
- Video: generated clips, edits, extensions, lipsync, upscale, background removal, and a composition of video with audio.
- Images: generation, reference-driven edits, vector output from a vector model, upscale and background removal.
- Brand kits that store palette, fonts, logos, rules, documents and a brand voice.
- Transcripts with a start and an end time for each word.
- A flow canvas of generated options, which can serve as a paid direction board.
- It does not make web code, 3D models, charts or dashboards.

## Connection and auth

- Attach the connector and sign in with the user's ElevenLabs account. Credits belong to the user's workspace.
- `account_get_usage` needs usage access. In the research session it failed with a permissions error.
- When that call fails, the balance is unknown. Ask the user to reconnect with more access, or to read the balance in their account.
- `creative_get_flow_node_types` lists the node types and the models this workspace can run. The schema enum is the full catalog, not the workspace list.

## Cost model

- Free: `creative_get_guide`, `creative_get_model_guide`, `creative_get_model_schema`, `creative_get_flow_node_types`, `creative_list_voices`, `creative_list_flows`, `creative_get_flow`, `creative_get_flow_run_status`, `creative_show_flow_results`, `creative_get_generations`, `creative_get_available_assets`, `creative_list_brand_kits`, `creative_get_brand_kit`, `creative_get_voice_design_previews`.
- Free: building a flow without running it (`creative_create_flow`, `creative_add_flow_node`, `creative_add_flow_asset_node`, `creative_connect_flow_nodes`, `creative_update_node`).
- Stated as free to run: an Audio Effects node and a Random node.
- Spend: `creative_generate_image`, `creative_generate_video`, `creative_generate_speech`, `creative_generate_in_flow`, `creative_edit_image`, `creative_run_flow_nodes`, `creative_transcribe_audio`.
- Spend: `creative_design_voice` (three previews for each call) and `creative_execute_sandbox` (charged by run time; the `large` size costs double).
- Not stated: the cost of `creative_create_brand_kit_from_website`. Default: treat it as a spend call.
- Live quote: pass `estimate_only: true` to the generate, edit, run and transcribe tools. The call returns the cost and starts nothing.
- Live balance: `account_get_usage`, when the connection has usage access.
- Defaults multiply cost. An image call and a speech call each return more than one take. Read the default count from the schema.
- The server instructions say to leave `generations_count` at its default. Lower it only when the user asks for one take.
- GATE: quote, show the number, get a yes, call once. This is stricter than the server text, which asks for a yes only before a long video.

## Call order

1. For any task with more than one tool call, read its guide with `creative_get_guide`. Guides seen: voiceover, lipsync or combine, local file.
2. When one output feeds another, call `creative_create_flow` first. Pass its `flow_id` to every call. Nodes on different flows cannot connect.
3. Call `creative_get_flow_node_types` for the models this workspace can run.
4. Call `creative_get_model_guide` before you prompt an unfamiliar model. Call `creative_get_model_schema` before you pass `model_parameters`.
5. For speech, call `creative_list_voices` to get a `voice_id`. Never use a voice id from memory. Tell the user which voice you picked.
6. For brand work, call `creative_list_brand_kits`, then `creative_get_brand_kit`. Write the colors, fonts and rules into the prompt by hand.
7. Quote with `estimate_only`. Pass the GATE. Then generate.
8. Poll `creative_get_flow_run_status` with the `flow_id` and the `session_ids`. Wait `poll_after_seconds` between calls. Stop at `all_completed` or `has_failures`.
9. Pin the chosen take: call `creative_add_flow_asset_node` with its `generation_id`. Then wire that node to the next one.
10. Call `creative_get_generations` for the signed links. Download each file at once.

## Key tools

| Tool | Use it when |
|---|---|
| `creative_get_guide` | You need the step list for a voiceover, a combination of generations or a local file. |
| `creative_get_flow_node_types` | You need the node types, models, defaults and parameters this workspace can run. |
| `creative_list_voices` | You find a voice by language, gender, age, use case and descriptive words. |
| `creative_generate_speech` | You need narration or a voiceover. |
| `creative_generate_in_flow` | You need a node type with no tool of its own: `sfx`, `music`, `composition`, `image-transform`, dubbing, `voice-changer`, `voice-isolator`, `video-to-music`, `audio-effects`, `llm`. |
| `creative_generate_image`, `creative_edit_image` | You need images, or reference-driven edits. An edit needs `connect_from`, so put the file on the flow first. |
| `creative_generate_video` | You need clips. Other models serve lipsync, edit, extend and upscale. |
| `creative_design_voice`, `creative_save_designed_voice` | You need a new brand voice from a description. The preview line and its language come from the user. |
| `creative_create_brand_kit`, `creative_get_brand_kit` | You store or read palette, fonts, logos, rules, documents and a brand voice. |
| `creative_get_flow_run_status`, `creative_get_generations` | You need the finish state, then the signed full-resolution links and previews. |
| `creative_execute_sandbox` | You need an ffmpeg, vips or Python edit that no node does: trim, join, re-encode, loudness, subtitles. It spends. |
| `creative_attach_reference_file` | You bring a file at a direct https URL onto a flow as a reference node. |

## Inputs

- The script text and its language.
- A voice description, or a pick from the listed voices.
- For a new voice: the exact preview line (100 to 1000 characters) and its language, both from the user.
- Brand facts for a kit: hex colors with roles, font families and weights, logos by role, and the dos and do nots.
- Reference files as direct https URLs.
- ASK: which take to keep.
- A yes on the quoted cost before each spend call.

## Outputs and how to bring them into a project

- Every generation lands on a flow with a canvas `url`, a `flow_id`, a `node_id` and `session_ids`.
- `creative_get_generations` returns a signed `full_res_url` for each generation, with status, model, width and height. It takes up to 4 ids in one call.
- Download each file into the repository, for example `public/audio/` or `public/video/`. Reference the local path. The links are short-lived.
- A transcript returns text, word timings and a `words_download_url`. Convert it to VTT or SRT in the repository.
- A brand kit returns JSON. Map it into `design/tokens.json`. Name in `design/decisions.md` which one is the source of truth.
- The audio container formats are not stated in the schemas. Check the file type after download.
- Write a provenance record in `design/assets/manifest.json` for every downloaded file.

## Handoffs

- In: any picture or clip at a direct https URL, from another generator, an asset library or a Claude Design export, through `creative_attach_reference_file`. GATE: this sends the file outside the project.
- In: a website URL through `creative_create_brand_kit_from_website`. The result is best effort.
- Out: voiceover and music files go into an HTML video project or the site's media folder.
- Out and in: brand kit colors and fonts map into project tokens. A GDH token set can also be written into a kit.
- Inside: video in and music out (`video-to-music`); speech plus an image into lipsync; every part into `composition`.
- Claude Design canvas: no "Send to" target and no import tool exist here. A canvas export enters only as a file at a public https URL.

## Limits and failure modes

1. Never repeat a generation call to retry. It starts and charges a second run. Read the run status first.
2. A brand kit does not apply itself. Read it and word it into each prompt.
3. With no usage access the balance is unknown. A run can fail for lack of credits.
4. Reference inputs (`start_frame`, `reference_images`, `image`, `audio`) are ports that you wire with edges. In `model_parameters` they fail validation.
5. A changed `model_id` resets the parameters and can drop edges.
6. Parameter names differ by model, for example `duration_secs` and not `duration`. Read the model schema.
7. A composition cannot take a still. Turn the image into video first.
8. Put Audio Effects last, after voice change, isolation and dubbing.
9. Only the user can place an avatar node, in the canvas. Lipsync through a video model is the path the agent can drive.
10. Some video models return silent video. Add speech, music or effects, then a composition node.
11. The sandbox has no network. It runs one command at a time in a session.
12. The server instructions name `creative_create_asset_upload` and `creative_finalize_asset_upload`. Both were absent from the researched session.
13. Without them, a file that exists only on the user's machine may not be uploadable. Ask for a direct https URL.
14. Never read file bytes into the conversation. Never invent a `node_id`.
15. Variations share one node, and a downstream node takes one. Pin the pick first.
16. Limits read from the node types on 2026-11-23: sound effects 0.5 to 30 seconds, music 3 to 600 seconds, video up to 30 seconds. Read them live.
17. Default: do not design a voice that imitates a real, named person. This rule is GDH's own; the connector text does not state it.

## Best for

1. A brand voice and a voiceover for a product video or a site hero reel, with music and effects mixed in one composition.
2. Interface sound design: short looping or one-shot sound effects for an app or a game.
3. A stored brand kit that keeps generated images, clips and audio on brand.

## Wrong for

Web or app interface code, 3D models, charts and dashboards.

## Evidence

DOCUMENTED on 2026-11-23.

- Exercised: the tool schemas; the server instructions; free calls to `creative_get_guide` (the index and three guides), `creative_get_flow_node_types` and `creative_list_brand_kits`, all of which succeeded.
- Failed: `account_get_usage`, with a permissions error. Plan, balance and voice slots were not read.
- Not exercised: every generation, estimate, voice design, sandbox, transcription and brand kit write. Output quality is UNTESTED. No per-model price and no model guide was read.
- Not loaded: several update, delete, duplicate and disconnect schemas. Unverified: output audio formats, and the avatar-video path.
