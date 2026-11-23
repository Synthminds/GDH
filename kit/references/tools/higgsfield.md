# Higgsfield

Catalog entry: [higgsfield.json](../../catalogs/tools/higgsfield.json). Source: https://higgsfield.ai

Terms in this card. A job is one generation request with a `job_id`. A media id names one uploaded or imported input file. A workflow is a bundled method that `get_workflow_instructions` returns. A preset is a named recipe or slash command. The sandbox is the remote Linux box behind `sandbox_exec`.

## What it makes

- Raster images: stills, mood board tiles, mockups, product shots, text in an image, GIF.
- Vector marks and icons as SVG, through a vector-capable image model.
- Video: text to video, image to video, edit, extend, reframe, upscale, lipsync, motion transfer.
- Audio: speech, music, dubbing, voice change, stem separation.
- 3D models as GLB from a photo or text, with optional rigging and stock animations.
- 3D scenes in a hosted Blender, driven by Python, exported as GLB and .blend.
- Brand asset kits through the `brand-asset-creation` workflow: palette options, logo candidates, type, mockups, a brandbook as PPTX and PDF.
- Hosted websites, generation apps and browser games on its own stack and its own host.
- It has no chart tool, no dashboard tool, no font files, no web or stock search and no free-form board canvas.

## Connection and auth

- The connector signs in with the user's Higgsfield account. The agent handles no API key.
- TikTok and Meta Ads need their own link step (`tiktok_connect`, `meta_ads_connect`).
- Many tools render a widget in clients that support MCP Apps. A text-only client must relay links and poll.
- Load tool schemas by name for the surface in use. The full tool set is very large and each description is long.

## Cost model

- Every generation spends credits from one account balance. Read calls are free.
- Free: workflow, bundle and preset reads, `models_explore`, `balance`, `transactions`, list and show tools, the three `estimate_*_cost` tools, `ads_studio_quote`, `ai_influencer_prepare`, `apps_search`, `apps_describe`.
- Free: every hosted 3D scene build, edit, render and export call.
- Free quote mode: `generate_3d`, `reframe`, `outpaint_image` and `upscale_image` with `get_cost: true`.
- Spend: `generate_image`, `generate_video`, `generate_audio` and their batch forms, `generate_3d`, `execute_preset`, `motion_control`, `reframe`, `remove_background`, `outpaint_image`, `upscale_image`, `upscale_video`, `voice_change`, voice creation, `ads_studio_generate`, `ai_influencer_generate`, `video_analysis_create`, `virality_predictor`, `scene_builder_3d_generate_angles`, `scene_builder_3d_generate_video`, `gpu_generate`, `gpu_job_start`.
- `gpu_rent` bills for each second until the rental stops. `apps_invoke` can bill for each action.
- `meta_ads_write` can spend real advertising money.
- Live quote: call the matching `estimate_*_cost` tool. It returns the credit cost and a `quote_ref`. Call `balance` for the live balance.
- Generate with `params: {"ref": "<quote_ref>"}`. The generated request then equals the quoted request.
- A full website build or brand kit spends on many jobs. No tool returns one total. Quote each job.
- The flags `use_unlim` and `use_free_gens` are the user's choice only. When a call returns `unlim_choice`, ask the user, then repeat the call.

## Call order

There is no single init call. Follow these routing rules.

1. Call `get_workflow_instructions` with no argument to list the workflows. Call it again with the workflow name before any multi-step job.
2. A workflow is required before website tools, the first `ads_studio_*` call, any branding work, thumbnails and photo to GLB. A one-color logo recolor counts as branding work.
3. Resolve a slash command with `get_preset_instructions` before you pick tools. Load the preset `/3d-jutsu` once before any 3D scene work.
4. Call `models_explore` before a generation. Read the parameters, the aspect ratios and `medias[].roles` for the chosen model.
5. Bring inputs in. Local file: `media_upload`, then HTTP PUT the bytes, then `media_confirm`. Web URL: `media_import_url`.
6. Call `get_preferences` before the first generation that has no destination. Create a project only on request or when `auto_create_project` is true.
7. GATE: quote with `estimate_*_cost`, show the number, get a yes, then generate once.
8. Wait and show. One job: `job_display`. Many jobs: a batch call, then `jobs_wait`, then one `show_generation_by_ids`.
9. Website: load `website-builder-flow`, ask type, animation mode and publish choice, then `list_website_categories`, `create_website`, `website_repo_access` (checkout), edit through `sandbox_exec`, `website_repo_access` (push), `deploy_website`, `website_status`.
10. 3D scene: create or list a project, `scene_builder_3d_get_project`, `_query_python`, `_run_python` with the exact guards, `_get_operation` until it ends, render, inspect, `_get_glb` or `_get_blend`.

## Key tools

| Tool | Use it when |
|---|---|
| `get_workflow_instructions` | You start a brand, website, product photo, thumbnail, photo to 3D or video production job. |
| `models_explore` | You must pick a model or read its exact parameters, roles, durations and sizes. |
| `estimate_image_cost`, `estimate_video_cost`, `estimate_audio_cost` | Before every paid generation. |
| `generate_image`, `generate_image_batch` | You need stills, tiles, textures, icons, SVG marks or mockups. Use the batch form for 2 to 12 different prompts. |
| `generate_video` | You need a hero loop, product motion, image to video, a video edit or motion transfer. |
| `generate_3d` | You need one object as a GLB from a photo or text. |
| `scene_builder_3d_query_python`, `_run_python`, `_get_glb` | You need a multi-object scene, set or turntable. |
| `media_upload`, `media_confirm`, `media_import_url` | You bring brand files, references or earlier renders in as media ids. |
| `jobs_wait`, `show_generation_by_ids` | You collect the results of batch jobs. |
| `sandbox_exec` | You need ffmpeg, ImageMagick, a Playwright capture, the brand scripts or a website repo edit. |
| `create_website`, `deploy_website` | The user wants a live site that Higgsfield hosts. |
| `get_presets`, `get_preset_instructions` | You browse or load a named recipe. Browsing never approves `execute_preset`. |

Second tier: `remove_background`, `upscale_image`, `outpaint_image`, `reframe`, `upscale_video`, `manage_reference_elements`, `animation_actions`, `list_voices`.

## Inputs

- Brand: the official logo file, palette hex values, font names, brandbook pages or a homepage URL. The brand workflow treats supplied official assets as fixed.
- Website: the type (website, app or game), animated or not, an existing brand or free rein, and the publish choice.
- References: images, video or audio as files or HTTPS URLs.
- 3D: 2 to 4 photos of one object from different sides, and the intended use (game, web viewer, print, render).
- Aspect ratio for mockups and video. State vertical explicitly when the target is vertical.
- An explicit yes on each quoted cost, on publishing, on sharing and on a GPU rental.

## Outputs and how to bring them into a project

- Image: a job with a result URL (PNG, JPEG, WebP, GIF or SVG). Download it into the project. Do not hotlink.
- Logo: an SVG result is a concept candidate, never the master. Hand it to `logo-identity`, which redraws the mark by construction and checks the paths by hand before any file becomes the master.
- Official logo: the rule "never redraw" applies only to an official logo that the user supplied. The brand workflow treats that file as fixed. Recolor it with the workflow's export script.
- Video: an MP4 URL. Download, transcode to the delivery formats and add a poster frame.
- Audio: WAV, MP3, PCM or OGG. Download into the project.
- 3D model: a GLB URL. One provider can return FBX. Load a GLB with a glTF loader.
- 3D scene: short-lived links for GLB and .blend. Download at once.
- Brandbook: PPTX and PDF. Lift hex values and font names into project tokens by hand.
- Website: a git repository and a live URL on a Higgsfield subdomain. The code stays in Higgsfield's repository and sandbox. Read files out through `sandbox_exec` to reuse code elsewhere.
- Write a provenance record in `design/assets/manifest.json` for every downloaded file.
- Default: 30,000 to 50,000 triangles for a web viewer model. This number is the workflow's rule of thumb.

## Handoffs

- No tool here imports from or exports to another connector. Every handoff is a file or a URL.
- In: any public HTTPS image or video URL enters through `media_import_url`.
- In: a Claude Design canvas has no "Send to" target here. Render it to PNG first, then upload the PNG.
- Out: download image, video, GLB and SVG results, then place them in the repository or an asset library.
- Out: MP4 clips can feed a video composition tool as source footage.
- Out: an SVG goes to a vector editor by file import. The workflow promises no native Figma, Canva, PSD, AI or EPS file.
- Voice ids from `list_voices` work only inside Higgsfield.
- TikTok publishing accepts only Higgsfield-hosted media, and JPEG or WebP for photos. Convert PNG results first.

## Limits and failure modes

1. A wrong parameter name is dropped without an error. 3D providers name the polygon limit differently. A wrong name runs with no limit.
2. Never retry after a timeout. The job may exist, and a retry can pay twice. Read the job state first.
3. For 3D scene and GPU calls, reuse the same `requestId` or `idempotency_key` on a repeat.
4. `medias[].value` takes a media id or a job id. It rejects a raw URL.
5. The server cannot read chat attachments. Upload the bytes yourself, or call `media_upload_widget` as the only tool in that turn.
6. The website flow leads its own design. Its text forbids other design skills, bans palette families and requires a generated cover.
7. Use the website builder only when the user chooses it. Then let its flow lead. By default use Higgsfield for assets only.
8. A build of type website may hold no AI generation feature. A generation feature forces type app, the Higgsfield UI kit and Higgsfield sign-in.
9. Every `deploy_website` is live production. There is no preview stage. Migrations run on live data.
10. `publish_website` does not deploy. It lists nothing useful when the title or the cover is empty.
11. Website repo access is brokered: a 15-minute edit lease, a transfer cap, a file-size cap, a clean worktree and a fast-forward push.
12. Sandbox: 60 seconds by default and 120 seconds at most for a foreground command. Background jobs get 15 minutes.
13. The sandbox home folder persists 24 hours after last use. It is shared for each user, not for each chat.
14. The brand workflow keeps its state in a sandbox file. Publish that file after each change, because the sandbox is not durable.
15. Hosted 3D scenes: about five minutes for each operation, no network, catalog assets only, one mutation at a time.
16. A generated or uploaded mesh cannot enter a hosted scene.
17. Area lights, procedural shaders and world lighting do not survive GLB export. Use Sun, Spot or Point lights.
18. A succeeded scene operation proves that the code ran. It does not prove the look. Render from the delivery camera and inspect the image.
19. On a stale-state conflict, query again and write a new edit under a new operation id.
20. A trained character model works only with a short list of image models, one per generation.
21. Reference elements work only on a listed set of models. The SVG output mode accepts no references and no elements.
22. Logo candidates need three distinct prompts in one batch call. Do not set a count of three on one prompt.
23. Some audio models are for games only. Do not use them for standalone audio. One model's tag is unresolved.
24. A job can end as `nsfw` or `ip_detected`. One 3D provider can flag non-human creatures.
25. The workflow authors report failed runs on one 3D provider family. Use it only on request.
26. One photo shows one side. The model invents the back. Say so in the result.
27. Model ids change often. Never store a model id in a skill. Read `models_explore` each time.
28. `jobs_wait` waits 15 seconds at most. Video and 3D jobs take minutes. Poll at the returned `poll_after_seconds`.
29. Result URL lifetime is not documented. Download every result in the same session.
30. `media_import_url` accepts 50 MB at most.
31. Send feedback to the vendor only after the user approves the exact report.

## Best for

1. A brand asset kit from a brief: palette options, vector logo concepts for `logo-identity`, type, mockups and a brandbook, with approval for each slot.
2. Generated assets for a site or app built elsewhere: hero stills, a loop video, product shots, a web viewer model, a voiceover or music bed.
3. A 3D scene or product turntable built in hosted Blender, exported as GLB and .blend.

## Wrong for

A data dashboard or chart system in an existing codebase. Higgsfield has no chart or table tool, and its website builder keeps the code in its own repository and stack. Build in the project's own stack and call Higgsfield only for illustration assets.

## Evidence

DOCUMENTED on 2026-11-23.

- Exercised: live tool schemas; the workflow catalog; the workflows `website-builder-flow`, `brand-asset-creation` and `photo-to-3d-model`; one bundle file; the preset catalog and the 3D scene preset; model lists for image, video, audio and 3D; website categories; app search; five cost estimates.
- Not exercised: any generation, upload, deploy, publish or share call. Output quality, real job time and widget behavior in a text-only client are UNTESTED.
- Not read: most workflows and most bundle reference files, including the design recipe, the review rubric and the logo, type and palette references.
- Unverified: result URL lifetime; whether direct repository clone access exists; the total cost of a full website or brand kit.
