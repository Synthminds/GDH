# Routing a video to a tool

Read this file at step 12 of `motion-video`. It covers the routing table by need, the two HyperFrames paths, presenter and avatar requests, hand-offs from a design canvas, and what to deliver when no tool fits.

Evidence. This table applies the GDH resolution of conflict 22: route by need, and label every route UNTESTED until an exercised job confirms it. No research session ran a render or a generation with any video tool. Tool facts come from connector cards built from tool schemas, server instructions and guides read on 2026-11-23. Prices, model names and limits change; read them live from each tool.

## 1. The routing table by need

Every row is UNTESTED. Confirm a row with one small owner-approved job before you treat it as a rule, and log the result in the skill's refinement log.

| Need | Capability | Route | Example card | Why this route |
| --- | --- | --- | --- | --- |
| Code-owned or brand-exact video that lives in the repository | `video-compose` | A local HTML video composer: compositions as HTML files, previewed and rendered on the machine | [hyperframes](../../../references/tools/hyperframes.md) (local path) | Exact fonts, tokens and copy; the source can be edited, diffed and re-rendered |
| Generated footage: real-looking scenes, product shots in motion, b-roll | `video-gen` | A video generator, through `generate-media` | [higgsfield](../../../references/tools/higgsfield.md), [elevenlabs](../../../references/tools/elevenlabs.md) | Footage that does not exist; quote before each clip |
| Scene work with templates and free export: animate a static design, a UI demo, captions on a screen recording | `video-compose` | A scene engine | [picsart](../../../references/tools/picsart.md) | Template scenes, frame checks before export |
| A shared hosted project the user wants to open and share in the vendor's app | `video-compose` | The hosted HTML video composer, from a hosted chat client only | [hyperframes](../../../references/tools/hyperframes.md) (hosted path) | A project link and a cloud render |
| React video from parameterized blocks | `video-compose` | Remotion blocks from a component catalog, in a hosted editor or a local Remotion project | [21st-dev](../../../references/tools/21st-dev.md) | Typed blocks bound to brand fields; check the Remotion license size limit |
| On-brand collateral video in a design app the user already uses | `video-compose`, `video-gen` | The design app's own video tools | [canva](../../../references/tools/canva.md), [adobe](../../../references/tools/adobe.md) | The user edits there afterwards |
| Voice, music, effects, transcription | `audio` | An audio tool | [elevenlabs](../../../references/tools/elevenlabs.md) | One flow can mix voice and music |
| Storyboard, look kit, styleframes | `canvas` | A design canvas, through `claude-design` | [claude-design](../../../references/tools/claude-design.md) | Comparable frames on one board |

Choose by the first question the user answers yes to:

1. Must the video's source live in the project and be re-rendered by the team? Use the local HTML composer.
2. Does the video need footage that does not exist? Use a video generator for those shots, then compose.
3. Is the job a quick animation of an existing design or screen recording, with templates? Use a scene engine.
4. Does the user want a hosted project link in the vendor's app? Use the hosted composer, from a hosted chat client.
5. Is the project already a React video project? Use parameterized blocks.

Many videos mix routes: generated clips as footage inside a code-owned composition, voice from an audio tool. Keep one route as the master timeline.

## 2. The two HyperFrames paths

The owner calls this tool "HeyGen". It is HeyGen's HTML video framework. It is not HeyGen's avatar product.

| | Hosted path (MCP) | Local path (skills and CLI) |
| --- | --- | --- |
| Who can author | Hosted chat clients: web and desktop chat apps | Command-line and IDE agents: Claude Code, Cursor, Codex |
| What you get | A hosted project with an id and a link | HTML compositions on disk |
| Authoring | A vendor agent composes from a clear prompt | The coding agent writes the composition |
| Render | Cloud queue; spends | Local render; free. A cloud render from the CLI spends. |
| Edit later | In the vendor's app | In the repository |
| Read tools | Available to every client | Not needed |

Rules:

1. From a command-line agent, the hosted compose and render calls are refused by design. The refusal points to the local skills. It is not a bug.
2. Install the local skills only with the user's yes. The card has the install line. A local render needs Node and FFmpeg.
3. Read the installed core skill first. It holds the composition contract and the work loop.
4. On the hosted path, do not call compose on a vague request. Confirm the video plan first.
5. A hosted project with no design source drifts to a house preset. Pass the brand direction in the prompt.
6. Never poll status faster than the card says.
7. Render links expire. The card states seven days for one kind of render link. Download at once.

## 3. From a design canvas to video

| Start | Hand-off | Card |
| --- | --- | --- |
| A Claude Design canvas authored to the composition contract | The user clicks "Send to"; the import tool takes the short-lived URL | [hyperframes](../../../references/tools/hyperframes.md) |
| A Claude Motion MP4 | "Send to" an editor that accepts motion imports | [hyperframes](../../../references/tools/hyperframes.md), [canva](../../../references/tools/canva.md), [adobe](../../../references/tools/adobe.md) |
| An HTML styleframe built locally | It becomes scene one of a local composition | [hyperframes](../../../references/tools/hyperframes.md) |
| A Figma frame | A scene engine or the local composer can import it, per its card | [picsart](../../../references/tools/picsart.md), [figma](../../../references/tools/figma.md) |

Rules:

1. Call the target's guide tool before you author for it. Each target has its own contract; do not reuse one target's guide for another.
2. Send-to URLs live for minutes. Use them at once.
3. Fonts must be embedded the way the contract asks. A linked web font often falls back to a system face in a renderer.

## 4. Presenter and avatar requests

No tested presenter or avatar-video tool is in the catalog. HyperFrames exposes no avatar, voice or talking-head tool. One audio tool lists an avatar step that only the user can place in its own canvas; that path is UNTESTED.

When the user asks for a presenter:

1. Say plainly that no tested avatar route exists in this kit.
2. Offer the alternatives:
   - A real presenter filmed by the user, then composed with captions and graphics.
   - Voice-over with kinetic type and product footage, no face.
   - A lipsync or avatar step in a tool the user operates in its own app, with the result brought back as footage.
3. GATE: any likeness of a real person, cloned or animated, needs that person's written consent on record.
4. When a presenter tool is added to the catalog through `add-design-tool`, exercise it once and update this file.

## 5. Licenses that shape the route

1. Remotion is free only for individuals, non-profits and companies up to a stated headcount. Check the client's size before choosing a Remotion route. Read the license through `find-assets`.
2. GSAP is free for commercial use but not open source, with a limit on competing no-code builders. Read the current terms.
3. The HTML video framework itself is open source. Its cloud render and vendor media are not free.
4. Fonts used in a render need a license that allows embedding in video.

## 6. With no video tool

Deliver what can be finished, and say what is not:

1. The video plan, the script with timings, the storyboard and the chosen styleframes.
2. An HTML animatic with the guide read.
3. The sound plan, the caption file drafted from the script, and the export spec list.
4. A plain statement: "The render is not done. No video tool was available in this session."

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| One tool for everything | Generated footage used for kinetic type and logo | Compose type and logo in code; generate only footage |
| Rule from a guess | "Always use tool X" written after one look at its card | Label UNTESTED; confirm with one job |
| Hosted call from the command line | Compose refused; retried in a loop | Use the local path; the refusal is normal |
| Avatar promised | A presenter video promised with no tool | State the gap; offer the alternatives |
| Expired hand-off | A send-to or render link used hours later | Use it at once; download at once |
| License surprise | A Remotion build for a large company | Check the license before the route |
