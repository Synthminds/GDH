# Vercel

Catalog entry: [vercel.json](../../catalogs/tools/vercel.json). Source: https://vercel.com/docs

This card covers only the tools that serve design work. The server holds many more tools for infrastructure: domains, firewall, flags, storage, sandboxes and billing. A design skill does not call those.

Terms in this card. A deployment is one build with its own URL. A preview is a deployment that is not production. A protected deployment needs sign-in or a share link. A Toolbar thread is a review comment pinned to an element of a preview page. An import is a Claude artifact hosted as a static deployment.

## What it makes

- Preview and production deployments of a site or an app.
- A protected static page from a Claude Design canvas.
- A protected static snapshot of a Claude dashboard, and a playback page for a Claude motion MP4.
- Share access to a protected preview.
- A review loop: pinned comments on a preview that the agent reads, answers and resolves.
- It makes no design content. It hosts and reviews what other tools build.

## Connection and auth

- The connector signs in with the user's Vercel account. Calls run at team scope or at project scope.
- A project-scoped connection changes import behavior. See limit 3.
- `get_auth_user` returned 404 "User not found" in research while team-scoped calls worked. Treat the user endpoint as optional.
- On an access or not-found error, verify the scope first. Then follow the sign-in or SSO steps that the error reports.
- When a tool returns `requires_user_action`, pass the dashboard URL to the user. Leave the action pending.
- The Vercel CLI is the fallback: `vercel deploy`, `vercel inspect`, `vercel curl`, `vercel api`. Error payloads name the matching command.
- CLI credentials and defaults are separate from the connector's. Keep the same team id when you switch.
- Preflight: call `list_teams`. It is a free read and proves the sign-in.

## Cost model

- No tool description states a price for one call.
- Default: deployments, builds and bandwidth count against the Vercel plan. Research did not read the plan tier.
- Calls that create billable or public things: `create_deployment`, the three `import-claude-*` tools, `create_project`, `create_git_project`, `request_promote`, `assign_alias`.
- Real money, and outside design work: `buy_domain`. Never call it from a design skill.
- Not free of side effects: `get_access_to_vercel_url` and `web_fetch_vercel_url`. Each can create a share link on the deployment. Anyone with that URL can view it for up to 23 hours.
- Free reads: `list_teams`, `list_projects`, `get_project`, `list_deployments`, `get_deployment`, `list_deployment_events`, `open_deployments`, `list_toolbar_threads`, `get_toolbar_thread`, the three import status tools, `search_vercel_documentation`, `get_git_deployment_context`.
- Live quote: no tool quotes a deployment. Default: read the account charges with `list_billing_charges`. Default: for a domain, `get_purchase_quote` returns the quote.
- GATE: get a yes before a production promotion, a new project, an alias or a share link.

## Call order

1. Resolve the scope once. Read `.vercel/project.json` (`orgId`, `projectId`) when the repository has one.
2. Otherwise call `list_teams`, then `list_projects`. Reuse the ids. Never guess an id. Ask when the target stays unclear.
3. Deploy: call `create_deployment` with inline files or through the project's Git connection. Omit `target` for a preview.
4. The build is asynchronous. Poll `get_deployment` until the state is `READY`, `ERROR` or `CANCELED`.
5. On a failure, read `list_deployment_events` with `builds: 1`.
6. Claude import: call `import-claude-design-from-url`, `import-claude-dashboard-from-url` or `import-claude-motion-from-url`.
7. Poll the matching status tool with the `job_id` until `done` or `failed`. `done` returns the protected deployment URL.
8. Share: call `get_access_to_vercel_url` to give the user a link to a protected preview.
9. Review: call `list_toolbar_threads` with team, project, branch and page. Then call `get_toolbar_thread`.
10. After the fix: call `reply_to_toolbar_thread` once, then `change_toolbar_thread_resolve_status` with `resolved: true`.
11. GATE: call `request_promote` only on request. It moves a preview to production without a rebuild.
12. Verify every write before you report it done. Check an uncertain write before any retry.

## Key tools

| Tool | Use it when |
|---|---|
| `open_deployments` | The user asks "is it deployed?" or wants to watch a build. It shows status, preview URL and logs. |
| `create_deployment` | You publish a small static design or redeploy from Git. |
| `get_deployment`, `list_deployments` | You poll the build state, or you look for the preview of a branch or a commit. |
| `list_deployment_events` | A deployment failed and you need the build log. |
| `import-claude-design-from-url` | A Claude Design canvas must become a protected static page. Self-contained HTML up to 30 MiB. |
| `import-claude-dashboard-from-url` | A Claude dashboard must become a styled static snapshot. Version 1 JSON manifest up to 16 MiB. |
| `import-claude-motion-from-url` | A Claude motion piece must become a playback page. A complete MP4 up to 100 MiB. |
| `get-design-import-job-status` and its dashboard and motion siblings | You poll an import to `done` and read the URL. |
| `get_access_to_vercel_url` | A reviewer needs access to a protected preview. |
| `web_fetch_vercel_url` | The agent must read its own protected preview to verify the result. |
| `list_toolbar_threads`, `get_toolbar_thread` | You pull pinned review comments with page path, CSS selector, selected text, device and attachments. |
| `reply_to_toolbar_thread`, `change_toolbar_thread_resolve_status` | You close the loop after a fix. |

Also useful: `request_promote`, `assign_alias` (a stable review URL), `create_project` with `enablePreviewFeedback` and `ssoProtection`, `edit_toolbar_message`, `add_toolbar_reaction`, `search_vercel_documentation`.

## Inputs

- The team and the project, or a repository with `.vercel/project.json`.
- For a Claude import: the artifact URL on `claudeusercontent.com` plus a `download_token`. Claude supplies both.
- Never extract the token from the URL. The URL expires in about 10 minutes.
- A stable `claude_design_project_id`, so that a second send updates the earlier import.
- An explicit request before a production promotion.
- An explicit request before a reply in a comment thread on the user's behalf.

## Outputs and how to bring them into a project

- A deployment URL on `*.vercel.app`. An import is protected by default. No source code comes back.
- Toolbar threads return structured feedback: page path, CSS selector, selected text, device, messages, attachments, linked issues and a web URL.
- Map each thread to a file and an element in the repository. Write the change list into the decision record.
- `web_fetch_vercel_url` returns the rendered response for checks.
- Record each deployment URL and its protection state in `design/handoff.md`.

## Handoffs

- From Claude Design: three import tools, one each for a design (HTML), a dashboard (JSON manifest) and a motion piece (MP4).
- Other connectors expose import tools with the same names. Each target has its own contract. Vercel is the "host it as is" choice.
- From a code builder: its deploy call creates the Vercel project and the deployment. Inspect both here.
- From local code or the coding harness: a Git-linked project, `create_deployment` or the CLI.
- To the agent: Toolbar threads feed the scoped refinement round.
- A hosted site builder with its own hosting does not feed Vercel.

## Limits and failure modes

1. A dashboard import is a static snapshot. It has no live data, no query execution and no working filters. Executable content and outside resources are removed.
2. Imports need write access and deployment protection on generated URLs. New imports reuse one project for each user across title changes.
3. A project-scoped connection creates the deployment in that project, not in the import project.
4. An older "legacy" design import needs the original title and the stable id on every later send.
5. `reply_to_toolbar_thread` is not idempotent. A repeated call posts a duplicate that everyone on the thread sees.
6. Only your own Toolbar messages can be edited.
7. `list_toolbar_threads` returns unresolved threads only, unless `status` is set.
8. An incomplete upload shows a null deployment URL.
9. The docs describe `deploy_to_vercel` (300 files, 3 MiB for one file, 4 MiB total) for root connections only. The researched session exposed `create_deployment` and `create_git_project` in its place.
10. Not verified: whether those size limits apply to `create_deployment`. Its schema states no limit.
11. Do not rebuild a medium or large project, or a binary asset, inside tool arguments. Use Git or the CLI.
12. Follow pagination for complete results. Report partial data as partial.
13. Never print or request a secret. Never decrypt an environment value unless the user asks.
14. A share link exposes the preview to anyone who holds the URL. Treat it as an exposure, not as a read.
15. How Claude Design hands the artifact URL and token to an agent in a coding host is unverified.

## Best for

1. Turning a finished design build into a shareable preview URL, then promoting it when approved.
2. The feedback loop: the user pins comments on the preview, the agent reads them by page and selector, fixes, replies and resolves.
3. Hosting a Claude Design canvas, a dashboard snapshot or a motion MP4 as a protected link for stakeholders, with no rebuild.

## Wrong for

Creating or changing a design. Vercel hosts and reviews. Use a code builder, a site builder, a design canvas or local code for the build.

## Evidence

DOCUMENTED on 2026-11-23.

- VERIFIED by live calls: `list_teams`, `list_projects`, `list_toolbar_threads` and `search_vercel_documentation`. `get_auth_user` failed with 404.
- DOCUMENTED from schemas, server instructions and documentation search results: every other tool and limit in this card.
- UNTESTED: `create_deployment`, the three import tools, `get_access_to_vercel_url`, `web_fetch_vercel_url`, `request_promote` and every thread reply or resolve.
- Unverified: the plan tier and build limits; Toolbar availability by plan; the size and file-count limits of `create_deployment`; the import flow from a coding host.
- The tools `list_billing_charges` and `get_purchase_quote` are named from the session tool list. Research did not read their schemas.
