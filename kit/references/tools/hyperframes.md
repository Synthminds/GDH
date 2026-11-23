# HyperFrames by HeyGen

Catalog entry: [hyperframes.json](../../catalogs/tools/hyperframes.json). Source: https://github.com/heygen-com/hyperframes

The owner calls this tool "HeyGen". Map the word "HeyGen" to this card. HyperFrames is not the HeyGen avatar-video product. It exposes no avatar, voice or talking-head tool. No HeyGen avatar-video connector was found in the researched session.

Terms in this card. A composition is one HTML file that plays as a video. A project is a hosted HeyGen record with a `project_id`.

## What it makes

- Video from HTML: timed HTML and CSS, a paused GSAP timeline and shader transitions, rendered to MP4, WebM or MOV.
- Launch teasers, stat reels, kinetic titles, explainers and animated charts.
- Personalized video at volume: one uploaded project rendered for each set of variable values.
- It does not make runtime interface motion, a static logo, a mood board, a dashboard or an avatar video.

There are two paths. Treat them as two tools with one name.

| | Path A: hosted MCP | Path B: local skills and CLI |
|---|---|---|
| For | Hosted chat clients (web and desktop chat apps) | CLI and IDE agents (Claude Code, Cursor, Codex) |
| What you get | A hosted project with a `project_id` and a canvas link | HTML and GSAP files on disk that the agent writes |
| Render | The HeyGen cloud queue | `npx hyperframes render` on the machine, or a cloud render from the CLI |
| Source in the repository | No | Yes. Edit, diff and commit the file |

Route by what the user wants. An editable local file means Path B. A shareable hosted project means Path A.

## Connection and auth

- Path A: attach the connector. Auth is OAuth, scoped to the user's HeyGen account.
- Path B: run `npx skills add heygen-com/hyperframes` and choose the core skills. In scripts or CI run `npx hyperframes skills update`. A local render needs Node 22 or later and FFmpeg.
- The server disables `compose` and `render_video` for CLI and IDE agents. The call is rejected with a pointer to the local skills.
- This rejection is normal behavior. Do not report it as a bug. The read tools stay available to every client.
- No tool on this server reports the plan or the credit balance.

## Cost model

- Free and read-only: `get-send-to-hyperframes-guide`, `list_projects`, `get_project`, `get_project_status`, `get_render_status`, `get_hyperframes_render`, `get-design-import-job-status`.
- Free per the guide: `import-claude-design-from-url` and the enhance turns after an import. Not stated: `import-claude-motion-from-url`.
- Spend: `render_video` and `render_project_with_variables`. A render that fails variable validation is not charged.
- Spend in effect: `compose`. It renders the MP4 as part of the run. Its tool text states no price.
- `submit_feedback` is free, but it sends data to the vendor. Call it only with the user's approval.
- Path B: the framework is open source and a local render is free. A cloud render from the CLI and vendor-generated media are not free.
- Live quote: no tool on this server returns a quote or a balance. Call `get-send-to-hyperframes-guide` for the current render terms, then ask the user to confirm the balance in their HeyGen account.
- GATE: before `compose`, `render_video` or `render_project_with_variables`, tell the user that the call spends. Get a yes. Call once.

## Call order

No init call is required. The order depends on the job.

Prompt to video (Path A, hosted chat clients only):
1. Clarify the brief. Do not call `compose` on a vague request.
2. Call `compose` with a prompt and no project id. Pass a design source only when the user chose a style.
3. Call `get_project_status` until the status is `draft` or `completed`. Wait 15 seconds between calls. After about five minutes without change, ask the user.
4. When the status is `waiting`, read the agent message, ask the user, and answer through `compose` with the same project id.
5. Edit with `compose` and the project id. Omit the design source to keep the style.

Claude Design canvas to video ("Send to HyperFrames"):
1. Call `get-send-to-hyperframes-guide` before you author.
2. Author one self-contained composition HTML to the guide's contract.
3. The user clicks "Send to" in Claude Design. That gives a URL on `claudeusercontent.com`.
4. Call `import-claude-design-from-url` with that URL. On a lint failure, fix the named errors and submit again.
5. Call `get-design-import-job-status` with the job id until it is done. Share the returned link.

Claude Motion MP4 to HyperFrames Studio: call `import-claude-motion-from-url` with the arguments that "Send to" supplies. Show the returned link. On an error, show the message and do not retry.

One template, many renders: the user uploads the project as a zip with the CLI and gives you the asset id. Call `render_project_with_variables`, then `get_hyperframes_render`.

Local authoring (Path B, the default for coding agents): install the skills, read the `/hyperframes` skill first, then run `npx hyperframes init <name>`, `preview` and `render`.

Status tools are paired. Do not cross them: `compose` with `get_project_status`, `render_video` with `get_render_status`, `render_project_with_variables` with `get_hyperframes_render`, `import-claude-design-from-url` with `get-design-import-job-status`.

## Key tools

| Tool | Use it when |
|---|---|
| `get-send-to-hyperframes-guide` | Before you author any composition meant for import from Claude Design. |
| `import-claude-design-from-url` | The user clicked "Send to" and you hold a `claudeusercontent.com` URL. |
| `get-design-import-job-status` | You need the state of that import and the project link. |
| `import-claude-motion-from-url` | Claude Motion hands you an MP4 to open in the Studio app for trims, titles and music. |
| `compose` | Hosted chat clients only: create a project from a clear brief, or edit one by id. |
| `get_project_status`, `list_projects`, `get_project` | You must confirm that a compose run finished. Or you need a project id, or the user wants to see a project in the player. |
| `render_video`, `get_render_status` | Hosted chat clients only: the user asks for a final MP4, then for its link. |
| `render_project_with_variables`, `get_hyperframes_render` | Batch personalization from one uploaded project, then the status, link and still. |

## Inputs

- A specific brief: topic or story, video type, length and format (16:9 or 9:16). A stated length sets the target duration.
- Brand: the exact palette, the real font files, real copy, real numbers and the logo. The guide forbids invented copy or metrics.
- A style choice when no brand exists. Read the built-in preset names from the `compose` schema.
- Media: each image or muted clip as a direct public HTTPS file URL. Share-page links and local paths do not render.
- For variable renders: the asset id and the exact variable names and types that the project declares.
- Consent to spend before any compose or render call.

## Outputs and how to bring them into a project

- Hosted project and canvas link: share the link. It is not a file. Preview URLs and thumbnails change on each request; do not hard-code them.
- MP4 link from `get_render_status`: download at once. Use the URL exactly as returned, because the query string is the signature.
- MP4, WebM or MOV link from `get_hyperframes_render`: the link dies after 7 days. Download and store the file.
- Studio link from the Motion import: valid 90 days after the last send.
- Local composition HTML (Path B): the only output that lives in the repository as source.
- On the hosted side, WebM and MOV come only from `render_project_with_variables`.
- Write a provenance record in `design/assets/manifest.json` for every downloaded file.

## Handoffs

- From Claude Design: the "Send to" URL into `import-claude-design-from-url`. This is the main design-to-motion bridge.
- From Claude Motion: the "Send to" MP4 into `import-claude-motion-from-url`.
- Other connectors expose tools with the same import names. Each target has its own contract. Do not reuse this guide for them.
- From image, footage and audio generators: outputs must arrive as public file URLs or inlined data URIs. Path A ignores linked audio files; use Path B for a custom voiceover or music.
- Path B reads a project `DESIGN.md` through its `frame.md` idea. Feed GDH tokens through that route when you work locally.
- Path B lists skills for Figma input and for Remotion conversion. These are from the README and are not exercised.
- Out: the rendered file goes to the repository, an asset library, a deploy target or an editor.

## Limits and failure modes

1. CLI and IDE agents cannot author or render through the MCP. Install the local skills.
2. The two paths are not drop-in equivalents. Path B has no project id and no hosted artifact. The server text also says to use the MCP "even from a CLI agent" for hosted projects. This conflict is unresolved. Treat hosted authoring as unavailable from a coding agent.
3. `compose` caps a video at 90 seconds. A longer request is built at 90 seconds.
4. `compose` cannot trim, cut or transcribe the user's footage. Path B and the Studio app can.
5. Missing required media fails the run. The tool does not replace it.
6. A new project gets a default house style. Pass brand direction in the prompt, or the result drifts to a preset.
7. An unknown design source value falls back to an invented look.
8. `render_video` is rejected while a compose run is in flight.
9. The import accepts only `claudeusercontent.com` URLs. It rejects self-hosted HTML.
10. The import rejects a bundled or splash-loader artifact. Send raw HTML in one file.
11. The import needs one live root with `data-composition-id="main"` and numeric width, height and duration. The root must not sit in a template element.
12. Scenes need numeric start and duration and must tile with no gaps. The timeline must be paused, built synchronously at load and registered under `window.__timelines["main"]`.
13. Linked fonts break fidelity. Inline every brand font as a base64 `@font-face`, one for each weight.
14. Inline images and logos as data URIs. Never use a relative path, a signed URL or a private host.
15. The renderer seeks frame by frame. Use no random values, clock reads, timers, animation-frame loops or async timeline builds. An infinite repeat needs a finite root duration.
16. Invisible middle scenes come from `visibility` toggles in place of `autoAlpha`, or from a first shader anchor that is never shown.
17. Read sizes, scene lengths, type minimums, the font ban list and transition rules from the guide. The guide says the contract still changes.
18. A wrong variable name or type fails the render with `VARIABLES_INVALID`. The failure shows only in `get_hyperframes_render`.
19. Variable renders with the same values and title dedupe for 24 hours in one workspace. `render_video` states no dedupe.
20. Do not poll faster than told: 15 seconds for project status, 30 seconds for render status. Never repeat a render call to check a result.
21. A failed project carries an internal reason in the agent message. It is for diagnosis, not for the user.
22. The export from Claude Design is silent. Sound arrives in the enhance step, which is not yet a stable contract.
23. `npx skills add` can lag the main branch by hours. `npx hyperframes skills update` matches the CLI version.
24. The `compose` text names asset upload tools that are not on this server. Ask the user for a public file URL.
25. The agent cannot upload a template zip through the MCP. The user does that with the CLI.

## Best for

1. A finished Claude Design brand canvas or page hero turned into an on-brand launch teaser or stat reel.
2. Code-owned motion graphics that live in the repository: animated charts, kinetic titles, changelog and explainer videos (Path B).
3. Personalized video at volume: one template rendered for each customer, product or data row.

## Wrong for

Interactive web motion: page transitions, scroll effects, micro-interactions or a live 3D scene in a product. HyperFrames produces a rendered video, not runtime interface code. Use in-page animation code for that work.

## Evidence

DOCUMENTED on 2026-11-23.

- Exercised: the tool schemas; the server instructions; the full text of `get-send-to-hyperframes-guide`; the public README; one live `list_projects` call, which succeeded.
- Not exercised: `compose`, `render_video`, `render_project_with_variables`, both import tools and `submit_feedback`. Output quality and render time are UNTESTED.
- Path B is UNTESTED. The local skills were not installed. Its skill list, registry and 3D blocks come from the README only.
- Unverified: whether hosted renders and the Studio app share one credit pool; alpha channel support; whether a coding agent can author hosted projects.
- No HeyGen avatar-video connector was found in the researched session. This card supplies no tool for the capability `avatar-video`.
