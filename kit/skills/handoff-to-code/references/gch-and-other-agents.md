# Start lines for GCH and other coding agents

Read this file at steps 16 and 17 of `handoff-to-code`. It covers the start line for each kind of builder, the rules when GCH is loaded, a hosted builder as the target, and how changes flow after the handoff.

Evidence. The GCH side is described from that harness's public contract by name only: DOCUMENTED. No GCH session has consumed a GDH package yet: UNTESTED until one does.

Terms. The builder is the coding harness, agent or team that writes production code. The start line is the short brief the user gives the builder.

## 1. GCH as the builder

When the GCH plugin is installed, give the user this start line and offer to start it.

```
The design is packaged in design/handoff.md.
Start the coding work with the GCH router and give it this brief:
- Goal, scope and out of scope: section 1 of design/handoff.md
- Design system: DESIGN.md and design/tokens.json (tokens only; no raw values)
- Must keep: section 3. Components, states, layout, content: section 4. Motion: section 5.
- Acceptance checks: section 7. Open questions: section 9; start on what they do not block.
- Assets: design/assets/manifest.json. Do not add an asset without a record.
- Sync points: section 2. Show the first rendered screen before building the rest.
```

Rules when GCH is loaded:

1. GCH governs code work: its planning, test rules and review.
2. Its `ux-laws` numbers hold for screens. Where a GDH default differs, the GCH number wins.
3. Its basics rule looks for the design system first. `DESIGN.md` at the project root is what it finds.
4. GDH skills stay available for design questions during the build.
5. Reach a GCH skill by name under its plugin namespace, never by file path.

## 2. Another coding agent

With no GCH, paste the project block from the kit export into `AGENTS.md`, or give the agent these lines:

```
Read design/handoff.md first. It is the design contract.
Use tokens from design/tokens.css only. Add no raw color, size, space, radius or duration.
Build every state listed in section 4. Ask when a state is marked "not designed".
Do not build anything in the out-of-scope list.
Do not add, replace or generate an asset. Ask, then record it in design/assets/manifest.json.
Run the checks in section 7 and report each result as PASS, FAIL or UNTESTED with evidence.
Ask before you change a decision in section 3. Log the change in design/decisions.md.
```

An agent with no question tool gets the open questions as a list at the top of its task.

## 3. A team of people

1. Walk the package with them at kickoff, section by section. Record questions in section 9.
2. Agree the sync points in section 2 with names and dates.
3. GATE: sending files outside the project is exposure. Ask the owner which files leave and where to.

## 4. A hosted builder as the target

1. The user chose the builder. Say once what it is weak at for this design.
2. GATE: an import sends project files out, sometimes to public storage. Ask first and name where they go.
3. GATE: a build there may spend. Read the card, get a live quote and a yes.
4. Call the builder's init or guide tool first.
5. Pass tokens, real copy and the component inventory, not a screenshot.
6. Check what arrived: tokens, components, states. Record what did not carry over.
7. The builder's own flow can lead inside the builder. The gates still hold.
8. Pull the generated source into the repository, then run section 7 on it.

Example card for a hosted builder: [v0](../../../references/tools/v0.md). Example for a preview with pinned comments: [vercel](../../../references/tools/vercel.md).

## 5. Changes after the handoff

| Change | Who decides | Where it is recorded |
| --- | --- | --- |
| A token value | The design owner, through `design-system` | `design/tokens.json`, regenerate; a decision entry |
| A new state, screen or edge case | The design owner, through the discipline skill | A dated subsection in `design/handoff.md` |
| A simplification for build reasons | The user | Section 8 and the decision record |
| A copy change from a code value (a limit, a time) | Builder proposes, design owner confirms | The copy deck and the decision record |
| An asset swap | `find-assets` or `generate-media` | The manifest |
| A component API change | The builder | The inventory row, with the date |

Never edit an old decision entry. Add a new one that replaces it.

## 6. When code already exists and the design is new

1. Read the existing component library first.
2. Map each designed component to an existing one: `reuse`, `extend` or `new`.
3. Pull the current tokens from code with the reverse path. See [reverse-path.md](reverse-path.md).
4. Hand off the difference, not the whole design.

## 7. Check

- The builder has a start line and knows which file is the contract.
- Ownership is stated for tokens, components, states, content, assets and checks.
- A route for changes after the handoff is agreed.
- The first rendered screen has a review date.
