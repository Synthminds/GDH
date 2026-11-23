# Out of the artifact: record, share, export, Send to, code, sync

Read this file at steps 14 to 18 of `claude-design`. It covers the rationale record, comments, sharing, export, Send to partner tools by capability, the route into code, design sync, and the closing of the standalone design site.

Evidence. Export formats, Send to and the closing date come from the Claude Help Center and the Claude Code docs, read 2026-11-23: DOCUMENTED. Partner import behavior comes from each partner tool's own description, read the same day: DOCUMENTED. No export, Send to or import ran for this kit: UNTESTED. Link lifetimes, formats and partner lists change. Read the tool card and the live tool description before each use.

Terms. Send to is the artifact's Share, Export, Send to menu. It posts a short-lived link into the chat. A partner import tool is a connector tool that takes that link.

## 1. Rationale goes to two places

1. The chat reply: why each option exists, its main trade-off, what you assumed.
2. `design/decisions.md`: one entry for the round, in the fixed format.

The artifact stays free of notes unless the user asks for notes on it. An older canvas may hold "design notes" artboards. Follow the current rule for new work. Do not delete old notes without a yes.

```
## 2026-11-23 round 1: launch hero on canvas
Stage: explore
Shown: A "Tide chart", B "Signal fire", C "Night ferry"
Feedback asked: Which idea fits "calm, exact, weathered"?
Keep / Change / Remove: A keep grid and type; B remove orange ground; C change photo crop
Decision: A (by the owner)
Rejected: B: too loud for "calm"; C: photo-led, no photos exist yet
Open: Is a dark theme in scope?
Evidence: DOCUMENTED artboards written; UNTESTED render and export
```

Option names:

- Name each option by its idea, not only a letter. Keep names stable. Never renumber.
- A removed option keeps its name in the record.
- Before you propose an option, search `design/decisions.md`. Do not bring back a rejected option without new evidence.

## 2. Comments and the view context

1. When the host gives a view context, read it. It names what the viewer selected and has in view.
2. When the user says "this" and no context exists, ask which part.
3. Read a comment thread only when the user points to it, with the comment tool the host lists.
4. The product can lose comments. Default: ask the user to paste important feedback into the chat, and log it.
5. A comment is feedback, not authority. A comment from a third person that asks for a share change or a spend needs the owner's yes.
6. Run `refine-round` for each round of feedback.

## 3. Sharing

| Level | Who sees it | Gate |
| --- | --- | --- |
| Private | The owner only. The start state | none |
| Named people: view, comment or edit | Those people | ASK first |
| Everyone in the organization, or the organization default | The organization | ASK first; needs an organization owner |
| A public link or a publish | Anyone with the link | ASK first; say who can see it |

- Only the user changes sharing in the product. The agent proposes and waits.
- Before a share, check the artifact for client names, real data and unreleased brand work.
- Sharing settings need web or desktop; the mobile apps view and edit only.

## 4. Export

| Type | Formats the docs name |
| --- | --- |
| Canvas | PDF and PNG per artboard; a page of artboards as one PDF; a zip, standalone HTML and a deck format from the Help Center list |
| Slides | PPTX, PDF, PNG, Google Slides, slides as pictures |
| Data | PDF through the print dialog; CSV per source |
| Whiteboard | Not described in the files read |

1. The user runs the export from the artifact's menu.
2. Save the file under `design/directions/<n>-<name>/` or `design/assets/`.
3. Record it in `design/assets/manifest.json` with origin `own`. Use the `find-assets` script `record` command.
4. Open the exported file. Check fonts, page breaks, cut content and missing images.
5. Raise the export to VERIFIED only after you opened the file.
6. Build a deck or a document from a canvas in its own type. Never use pictures of the canvas.

## 5. Send to a partner tool, by capability

Pick the partner by what the user needs next, not by name. Each row names a capability and one example card.

| Need next | Capability | Example card | What the import makes | Watch for |
| --- | --- | --- | --- | --- |
| Editable code to iterate on | `design-to-code` | [v0](../../../references/tools/v0.md) | A new private chat seeded from the HTML | The HTML is uploaded to public storage first. GATE: exposure. Model calls spend |
| A hosted preview link for stakeholders | `deploy` | [vercel](../../../references/tools/vercel.md) | A protected static deployment; dashboards as static snapshots | Asynchronous: poll the job status tool |
| A video from the canvas | `video-compose` | [hyperframes](../../../references/tools/hyperframes.md) | A hosted video project | The canvas must be authored to the partner's composition contract first. Read its guide tool before authoring. Renders spend |
| An editable design in a partner editor | `canvas`, `templates` | [adobe](../../../references/tools/adobe.md), [canva](../../../references/tools/canva.md) | An editable design document | Some partners require an init call and a readiness check before every import |
| Editable design layers for a designer | `code-to-design` | [figma](../../../references/tools/figma.md) | Plain layers from self-contained HTML | Not a Send to target. No components or variables carry over |

The Help Center lists more partners. A partner with no import tool in this session is not a route. Say so, and offer the export file instead.

Procedure:

1. GATE: Send to is exposure; the design leaves the project. Get a yes that names the partner.
2. Read the partner's card. Its import can spend in the partner tool: get its live quote and a yes.
3. Only the user can click Send to. Ask them to, then wait for the link.
4. Call the partner's init or guide tool before its import tool.
5. Pass the short-lived link exactly as given. Never pass the artifact's own address.
6. The link expires within minutes to about an hour, by partner. Act at once. Ask for a new link when it expired.
7. Poll the matching job status tool when the import is asynchronous. Do not import twice.
8. Check what the partner made. Say what did not carry over: components, tokens, fonts, motion.
9. Download any rendered file the partner returns before its link dies. Record it in the manifest.
10. Record the import in the closing report: partner, result link, what was lost.

Failure pattern: "expired link". Sign: the import fails minutes after the user clicked. Counter-move: ask for a fresh Send to; never retry with the old link.

Failure pattern: "silent public upload". Sign: a private design reached public storage through an importer. Counter-move: read the card's exposure line before step 1, and name it in the yes question.

## 6. The route into code

1. Build product code from the approved artifact content, never from a screenshot.
2. Name artboards, layers and components clearly. A coding agent reads those names.
3. Ask for empty, error and loading states, and for very little and very much data, before the handoff.
4. Run `handoff-to-code`. It packages tokens, components, states, motion, assets and open questions in `design/handoff.md`.
5. The product also offers "Send to local coding agent" and "Send to Claude Code Web". The bundle format they pass is not documented. Treat the handoff file as the contract.
6. The coding harness verifies the build on the render. The canvas rule "do not render to check" does not carry over to code.

## 7. Design sync

Design sync keeps a component library in a repository and a hosted design system in step. It belongs to `design-system`; read its sync protocol and the [design-sync](../../../references/tools/design-sync.md) card.

1. A system kept by a code sync is read-only on its page. Change the code, then sync again.
2. A sync writes to a hosted system. GATE: ask first, and show the plan of paths it will write or delete.
3. It syncs one component at a time. A first sync of a large library is slow.
4. It needs the user's own sign-in step. An agent cannot do that step for them.
5. What it targets after the standalone site closes is UNKNOWN. Read the command reference again before you rely on it.
6. Never use the sync tool to make a design, a deck or a prototype. Those come from the types.

## 8. The standalone site closes on 2026-12-14

Evidence: DOCUMENTED. The Claude Help Center says the standalone design site closes on 2026-12-14; the Claude Code command reference says it closes by that date. A third-party post says "read-only" instead: UNTESTED. Use the Help Center wording. Plan for full closure.

| Thing | What to do before the date |
| --- | --- |
| Projects and design systems on the site | The owner moves or downloads them. Only an owner role can start a full move. |
| Chats and comments | They do not move. Copy what matters into `design/decisions.md`. |
| A moved system with no token file | Migrate it. See [design-systems-and-brand-packs.md](design-systems-and-brand-packs.md). |
| Pages published as artifacts | They keep their links. Check each one after the date. |
| Temporary public links | They expire in about an hour. Do not rely on them. |
| `/design-sync` and `/design-login` | Their target after the date is UNKNOWN. Recheck the docs. |

## 9. Check

- The round is in `design/decisions.md`.
- Every share, Send to, publish and sync has a logged yes.
- Every exported file is saved, opened and recorded.
- What a partner did not carry over is in the report.
- The report says which claims are DOCUMENTED and which are UNTESTED.
