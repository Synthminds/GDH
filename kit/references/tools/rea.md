# REA (Reverse Engineer Anything)

Catalog entry: [rea.json](../../catalogs/tools/rea.json). Source: https://www.npmjs.com/package/rea-agents

REA is an MIT-licensed analysis tool by a third-party author. The owner keeps a fork and names REA as a GDH tool. GDH uses it for one purpose: to learn structure and technique from software and sites. The output of that study is an original design. GDH never uses it to copy proprietary design, code or assets.

Terms in this card. Evidence is REA's name for a tool result with provenance. A target is one browser page that REA attaches to. A passive tool reads a target and does not act on it.

## What it makes

- It makes no design output. It returns evidence about software that already exists.
- Page structure: DOM node names, accessibility roles, scripts, resources and network metadata of a live page.
- Bundle analysis: chunks, route candidates, endpoint candidates and vendor fingerprints (which animation, 3D or chart library a site ships).
- The code behind one effect: listeners on a CSS selector, and the functions that ran during one interaction.
- Viewport screenshots as PNG, and a local pixel diff of two screenshots.
- A route and module map of an Electron app directory or an ASAR file, without running the app.
- It has no CSS tool, no computed-style tool and no design-token tool. It makes no brand, logo, 3D, video or audio output.

## Connection and auth

- No account and no key. Analysis runs on the local machine.
- MCP registry name `io.github.morluto/rea`. npm package `rea-agents`. Version read: 6.7.0. Transport: stdio.
- Setup: run `npx rea-agents setup`. It registers the server and installs the matching skill. It shows the planned changes and asks for approval.
- Restart the agent after setup. The server start command is `npx rea-agents mcp` or `rea mcp`.
- The tool prefix depends on the registered server name. The usual prefix is `mcp__rea__`.
- Every MCP tool has a CLI twin with hyphens: `inspect_web_page` is `rea inspect-web-page`.
- Needs Node.js 22.19 or later, 24.11 or later, or 26 or later. Website work needs a Chrome-family browser.
- Static JavaScript analysis on Linux needs a procps-compatible `ps`.
- Run `rea doctor` or setup only when the tools are missing. Do not run them before every task.

## Cost model

- Free. No call spends credits. No quote tool exists and none is needed.
- The cost is context and local CPU time. Evidence results can be large.
- Tool schemas are compact by default. `REA_MCP_INPUT_SCHEMA_PROFILE=full` expands them and costs more context.
- Some native providers are paid third-party programs that the user must own. Design work does not need them.

## Call order

GATE: before any call, confirm that the user may analyze the target. See the license and ethics limits below.

Website work:
1. The user or the agent starts a separate browser profile with a debugging port on loopback.
2. Example: `google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/rea-browser-profile <url>`.
3. Call `list_browser_targets` with the endpoint to get a `target_id`.
4. Call `inspect_web_page` or another passive tool on that target.
5. For static analysis, capture with `include_script_sources: true`. Then call `export_web_scripts` with a new empty directory.
6. Call `analyze_javascript_application` on the returned `analysis_input`.
7. For `observe_web_execution` or `observe_web_session`, wait for the "armed" progress event. Then perform the action.

REA does not launch, own or close that browser. The exception is `capture_browser_scenario`: it can launch its own Playwright browser and drive declared actions.

## Key tools

| Tool | Use it when |
|---|---|
| `list_browser_targets` | First call for website work. It lists the page targets at a debugging endpoint. |
| `inspect_web_page` | You need structure, roles, scripts, resources and network metadata. Add `include_script_sources: true` to keep script text. |
| `capture_web_screenshot` | You need a visible-viewport PNG of the reference or of your own build. |
| `compare_web_screenshots` | You check a rebuild against a reference, or one iteration against the previous one. |
| `analyze_web_bundle` | You need chunks, routes, endpoints and vendor fingerprints without running the scripts. |
| `export_web_scripts` | You write captured scripts to disk for static analysis. |
| `analyze_javascript_application` | You analyze an exported script folder, an Electron app directory or an ASAR. |
| `inspect_web_event_listeners` | You need the handler code on one element (the first match of a CSS selector). |
| `observe_web_execution` | You need the functions that run during one interaction window. |
| `observe_web_session` | You record navigation and lifecycle events while the user walks a flow. |
| `capture_browser_scenario` | You need a repeatable action list with a snapshot at each step. |
| `compare_web_captures` | You diff two captures or two scenario runs: DOM, accessibility, URL, storage, screenshots. |

REA also ships MCP prompts. `investigate_feature` is the one for design study. `export_evidence_bundle` saves the session evidence.

## Inputs

- The target: a URL that the user may inspect, or a local app directory or ASAR.
- The user's confirmation that they hold the right to analyze the target.
- The feature or effect of interest in plain words. A CSS selector when known.
- For passive tools: a running browser with a debugging port.

## Outputs and how to bring them into a project

- Evidence JSON, returned inline with an Evidence ID. Each result separates observations, inferences and unknowns.
- Write the findings as notes on structure and technique: library names, the route map, how an interaction works.
- PNG screenshots. Save them in the project's reference folder or mood board folder. They never ship in the product.
- Exported script files with a manifest, in a directory that the caller chooses. Keep that directory out of the product source.
- REA returns no component code to paste. Write original code that the findings inform.
- Save an evidence bundle next to the entry in `design/decisions.md` when a finding drives a design decision.

## Handoffs

- To DAM: DAM ships a framework builder that opens a disposable browser, attaches REA read-only and drafts a `tokens.json` and a `DESIGN.md`.
- The token math in that builder is DAM code, not REA. The draft is marked derived and unreviewed. See [dam.md](dam.md).
- The builder fills only an item whose framework status is `needed`. The capture must come from the item's own source origin.
- To a mood board or a Claude Design canvas: attach REA screenshots as reference images. No "Send to" route ends in REA.
- To the build step: pass library names, the route map and the interaction technique. Build with project components or original code.
- With a page fetcher: REA drops page text by default. Use a page fetch tool for copy and Markdown.
- To a refinement round: screenshot each iteration and diff it against the approved reference.

## Limits and failure modes

License and ethics limits. These bind every use in GDH.
1. REA is MIT and comes as is. The license covers REA. It grants nothing over a target.
2. Analyze only public pages, or properties that the user owns or is authorized to examine.
3. Never go behind a login, a bot wall or another access control without authorization.
4. Never use REA to defeat DRM, license checks or anti-cheat. The project refuses that work.
5. Record structure and technique. Do not keep, copy or ship a target's code, images, fonts, logo or look.
6. Build an original. A design that reproduces the reference wholesale fails the GDH rule "reference, credit, re-implement".
7. The user carries the legal duty: laws, contracts, IP rights, privacy duties and terms of service.
8. A public site or a reachable debugging port is not permission for every operation.
9. Source-like output grants no rights to the original program or its data. Check the target's rights before you publish or reuse a result.
10. Observing or driving a target can change its state. Permission to inspect does not cover execution or interception.
11. Label every derived token set "unreviewed" until a person checks it.

Technical limits.
12. Passive tools do not click, navigate or evaluate page code. Only `capture_browser_scenario` drives actions.
13. DOM evidence keeps node names, value lengths and attribute names. It drops text and attribute values.
14. Accessibility names need `include_accessibility_text: true`.
15. Screenshots cover the visible viewport only.
16. `observe_web_execution` changes JIT timing. It excludes child frames, workers and WebAssembly.
17. Listener inspection misses delegated listeners on ancestors and listeners in framework registries.
18. Static route lists and endpoint lists are candidates. They are not proof that a route is reachable.
19. Attaching can clear another client's emulation settings. Use a disposable browser profile.
20. A headless Linux container may never open the debugging port without GLES, EGL and Mesa libraries.
21. A locked keyring can stall Chrome. Add `--password-store=basic`.
22. The runtime workflows are verified upstream only on Linux x64 with Chrome 153 and Node 24.
23. Results can be incomplete or wrong. Treat an inference as a lead, not a fact.
24. The REA skill says to skip REA for ordinary source-repository analysis. Read the repository instead.
25. The tool set is large (more than 200 tools on 2026-10-19, not confirmed since). Read the live tool list.
26. DAM builder: its accuracy gate failed. The accent color matched in 8 of 10 cases and the gate needs 9.
27. DAM builder: it samples one static desktop render. It sees no hover state, no motion and no responsive state.
28. DAM builder: it names fonts and does not capture them. It refuses to run as root (`REA_ROOT_REFUSED`).
29. DAM builder: a cloud network policy can block the target. It ran end to end with REA only on local fixtures.

## Best for

1. "How did they build that?": find the libraries, the bundle structure and the handler code behind an effect, then write an original version.
2. A first-draft token set and `DESIGN.md` from the user's own live site, through the DAM builder, as a measured start for a redesign.
3. Visual regression in a refinement loop: screenshot each iteration and pixel-diff it against the previous one.

## Wrong for

Cloning a competitor's site, downloading its assets or reading content behind a login. Also wrong for page copy (use a page fetch tool) and for any generation task.

## Evidence

DOCUMENTED on 2026-11-23. The card comes from a read of a repository checkout, not from a running server.

- DOCUMENTED: tool names and behavior (from the docs), the setup and start commands, the runtime requirements, the license and the disclaimer.
- UNTESTED: every tool call, setup, the browser attach, script export, screenshot diff and the DAM builder with a live site.
- Not read: the tool input schemas, the full generated tool catalog and several docs pages.
- Ownership note: the license names a third-party copyright holder. The owner's checkout is a fork. REA is not owner-written code.
- Sources read: the REA README, `LICENSE`, `DISCLAIMER.md`, `server.json`, and docs on browser observation, web runtime, script export, route inventory and MCP prompts.
