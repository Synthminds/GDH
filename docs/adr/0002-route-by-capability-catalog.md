# 0002: Skills route by capability through a data catalog

Date: 2026-11-23. Status: accepted.

## Context

The owner connects many design tools and adds more over time. Tools change their models, prices and tool names often. A skill that names a tool in its procedure goes stale, and a new tool would force a rewrite of every skill that could use it. Not every session has every tool.

## Decision

1. A fixed vocabulary of capability words lives in `kit/catalogs/capabilities.json`, with the owning skill and the allowed capabilities for each discipline.
2. Each tool is one JSON entry in `kit/catalogs/tools/` and one card in `kit/references/tools/`. The entry states kind, capabilities, auth, whether it spends credits, whether it exposes content, the first call, a fallback and an evidence label.
3. A skill names capabilities. It names a tool only as an example, with a link to its card.
4. At run time the agent lists the tools for a capability, confirms one is present in the session, reads its card, calls its first call, and falls back by the catalog when it is absent.
5. No price, credit amount, model id or tool count is written into a skill body. The agent reads them live.
6. The vocabulary changes only through `add-design-tool`, with the owner's yes.

## Consequences

- Adding a tool is a data change: one entry, one card, a build and a check.
- A missing tool degrades to its fallback, or to a stated local route, without a skill change.
- The catalog can go stale. `doctor` reports entries older than 180 days and entries labelled UNTESTED.
- The agent pays a small cost at run time to read the catalog and a card.
- A routing choice between several tools for one capability is a proposal until someone exercises the tools. The open-work list says which.
- Free asset sources follow the same idea in `kit/catalogs/assets.json`, with a license field and a date the license page was read.

## Alternatives considered

- One skill for each tool: rejected. It multiplies descriptions in context and breaks when a tool is absent.
- One large tools file: rejected. One file for each tool keeps a change small and reviewable.
