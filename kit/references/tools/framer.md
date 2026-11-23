# Framer

Catalog entry: [framer.json](../../catalogs/tools/framer.json). Source: https://www.framer.com

Terms in this card. A session is the handle that `open_project` returns. A program is the JavaScript that one `exec` call runs inside Framer. A replica is the copy of a node inside a breakpoint or a variant. A branch is a working copy of the project with its own preview URL.

## What it makes

- Marketing sites and landing pages on a canvas, with responsive breakpoints and hosted publishing.
- App-style prototypes on the canvas.
- Color tokens and text style presets inside the project.
- Motion: appear, scroll, hover, loop, ticker, page transitions and text effects.
- CSS-style 3D transforms and catalog shader backgrounds, without WebGL code.
- CMS collections, forms, A/B tests and analytics.
- Screenshots of project nodes and of an outside URL.
- Stock image search, icon sets and a component catalog for use inside the project.
- It makes no code repository. A Framer site stays on Framer hosting.

## Connection and auth

- The connector signs in with the user's Framer account.
- These tools replace the `@framer/agent` CLI and the local `framer` skills. Do not use either beside this server.
- `open_project` returns the session handle, the complete project instructions and the project context.
- The context lists enabled add-ons, project fonts, custom fonts and the catalog shaders.
- Reuse one session across turns. Open the project again only when a tool says the session is unknown or expired.
- `list_workspaces` shows the role, the plan and the permissions for each workspace. Read the plan there. Do not assume it.
- Preflight: call `list_workspaces`. It is a free read and proves the sign-in.

## Cost model

- No tool description names credits or a cost for one call.
- Not stated: whether `exec` calls are metered. Report a quota error to the user. Do not retry it.
- Plan limits apply to the site, not to the call. One stated limit: a form email destination allows 1 recipient on a free site and 3 on other sites.
- Not shown in anything that was read: plan limits for pages, CMS items, custom domains and bandwidth.
- The instructions describe the "Framer Convert" trigger features as paid.
- Live quote: no tool returns a price or a balance. `list_workspaces` returns the plan. `api.publishing.status()` returns the publish state.
- Account writes: `create_project`, any mutating `exec` program, `create_upload_url`, `submit_feedback`.
- GATE: publishing runs inside `exec` through `api.publishing.publish()`. Get an explicit request before you publish.

## Call order

1. Find the target. Call `list_projects`, or call `list_workspaces` with the filter `permissions: ["create_project"]`.
2. Call `open_project` with the project id or URL. Do this once for each project.
3. Call `read_docs` for `README.md`, then for `context.md`.
4. Read only the reference docs whose stated condition matches the task. A doc is split into `part-N.md` files. Read every part.
5. Read the matching skills before the first mutating program. The catalog includes `create-from-scratch`, `recreate-from-reference`, `style`, `breakpoint`, `component`, `cms` and `shaders`.
6. Aim for about three programs for one request. First read. Then build in one long program that ends with screenshots. Then fix and summarize.
7. Call `view_image` on the screenshots when the result depends on visual judgment.
8. Report `branchChange` and link `activeBranch.url` in the final summary.

## Key tools

| Tool | Use it when |
|---|---|
| `list_workspaces` | You need a place where a project can be created. |
| `list_projects` | You look for an existing site by title. Results are paged. |
| `create_project` | You start empty, or you remix a template from a `framer.com/remix/...` or `framer.link/...` link. |
| `open_project` | You start a session and get the rules. It also accepts a branch link. |
| `read_docs` | You need a reference, a guide or a skill for the task. |
| `exec` | Everything else: read the tree, insert and patch nodes, CMS, components, styles, code files, screenshots, publishing. |
| `view_image` | You must look at screenshots or asset references. Up to 10 in one call. |
| `create_upload_url` | A local image or file (up to 20 MB) must enter the project. PUT the bytes, then pass the returned `url` to `api.tree.assetReference`. |
| `submit_feedback` | Only after the user approves the exact report. |

Useful calls inside an `exec` program:

- `api.images.search({query, orientation, width})` for stock images.
- `api.fonts.list()` and `api.fonts.get(name)` for the font catalog with weights, variable axes and OpenType features.
- `api.icons.list()`, `api.icons.listIcons(setId)` and `tree.installIconSet()`.
- `api.components.list()`, `api.controls.components()` and `tree.installComponent()`.
- `api.controls.shaders()` and `tree.installShader()`. The catalog includes `liquid-gradient`, `mesh`, `particles`, `fluted-glass`, `logo-glass` and `logo-crystal`.
- `api.tree.screenshot(node, {theme})` and `api.screenshot(url, {viewport})`.
- `api.tree.toSVG(node)` for the SVG source of a canvas vector.
- `api.files.create`, `write` and `applyPatch` for React code components, overrides and shader modules.
- `api.publishing.status()`, `.publish()` and `.deployToProduction(versionId)`.
- `fetch()` for public Markdown, HTML, JSON or text.

## Inputs

- A target project, or permission to create one.
- For new work: a brand direction, fonts and a palette.
- Images as reachable URLs, or local files that the agent uploads through `create_upload_url`.
- Framer programs cannot see chat attachments.
- A remix link when the work starts from a template.
- An explicit request before a publish, a production deploy, a branch merge or a branch delete.

## Outputs and how to bring them into a project

- The main output is a hosted Framer project with an editor URL and a branch preview URL.
- After a publish: a staging URL or a production URL.
- Screenshots as image URLs. SVG source through `tree.toSVG`. Code file source through `api.files.read`. Component share URLs through `api.components.url(id)`.
- Default: assume no export of a page as HTML or React exists. The research found no export API.
- A Framer site does not land in a repository. Link to it or embed it.
- Save any SVG or screenshot that the project keeps as a file. Write a provenance record in `design/assets/manifest.json`.

## Handoffs

- From a reference: a screenshot or an outside page, through the skill `recreate-from-reference` and `api.screenshot`.
- From a design system: brand tokens become color tokens and text style presets.
- From an image generator: any image that has a URL. From a logo file: SVG through `SVGNode`.
- Default: this server has no import tool for a Claude Design canvas. Rebuild from a screenshot or from the design tokens.
- Out: the published URL for review, and SVG and screenshots into other tools.
- Framer hosts its own sites. It is an alternative to a separate deploy host, not a feeder for one.
- To a code builder: no direct tool. Attach a screenshot as a reference.

## Limits and failure modes

1. Programs run inside Framer. They cannot read local files or chat attachments.
2. A thrown error or a timeout does not roll back earlier writes. Read the affected nodes again before a retry. Never rerun the whole program.
3. The first edit creates a branch automatically.
4. A publish from a branch updates only the branch preview.
5. On main with staging on, `publish()` updates staging. Only `deployToProduction()` goes live.
6. Work on the canvas first. Use a code component only for runtime logic: fetch, timers, browser storage.
7. Never insert into, duplicate or remove replica descendants. Add to the primary variant and override.
8. Default breakpoints: Desktop 1200 px, Tablet 810 px, Phone 390 px.
9. Overlays do not appear in screenshots. Gesture variants cannot be captured.
10. These tools cannot set localization, proxies, custom response headers or static files.
11. The `shader` attribute is fixed at insert. To change it, remove the node and insert a new one.
12. Every `RichTextNode` link needs a `linkStylePreset`.
13. A link to a draft page breaks after publish.
14. The built-in design rules warn against invented gold, amber or purple palettes. They also require one committed visual direction. The project design system still leads.
15. The source and the license of `api.images.search` results are unknown. Read the license before a stock image ships.
16. `api.publishing.status()` was not run in research. Publish rights for an editor role are unknown. Check before you promise a publish.

## Best for

1. A polished marketing or launch site with a CMS-backed blog or case studies, responsive breakpoints and scroll or appear motion.
2. Fast visual exploration on a freeform design page: several hero directions side by side, a screenshot of each, then the user chooses.
3. A hero with a catalog shader background, or a glass or crystal logo treatment, without WebGL code.

## Wrong for

A data dashboard or an authenticated app that must live in the project's own repository and call its own backend. Use a code builder or local code, then a deploy tool.

## Evidence

DOCUMENTED on 2026-11-23.

- VERIFIED by live calls: `list_workspaces`, `list_projects`, `open_project` (session handle, instruction set and project context returned) and `read_docs` for `README.md`. No edit was made.
- DOCUMENTED from the `open_project` instructions and `README.md`: the call order, the `exec` API names, every limit above.
- UNTESTED: every `exec` program, so no insert, screenshot, image search, upload or publish ran. `create_project`, `create_upload_url` and `submit_feedback` did not run.
- Read by name and description only: the guides and the skills.
- Unverified: plan limits; whether `exec` is metered; the stock image source and license; publish rights by role; the absence of a page export.
