# Mapping to MCPs in Claude Cowork and Claude Code (field guide, v1.0, 2026)

Book id `mapping-to-mcps`, id prefix `P-MCP`. 7 principles, 2 of them gates. The machine-readable copy is in [principles.json](../principles.json); this file matches it word for word.

Gates: P-MCP-02, P-MCP-06.
Every other principle is a default. Query them with the `design-principles` skill.

## Section 01: The basics

**P-MCP-01 Record tools, layer and transport.** Record each connector's layer, its transport and the tools it exposes, not only its name. Test: Each catalog entry lists layer, transport and exposed tools.

## Section 02: What ships inside

**P-MCP-02 Read the live connector list.** Read the host's live list of connectors before planning a workflow, and never assume a connector is present. Test: The plan cites a live check of each connector it relies on.

**P-MCP-03 Check write access first.** Check whether a connector can write before designing a workflow that needs it to write. Test: Every workflow step that writes uses a connector recorded as write-capable.

## Section 03: On your machine

**P-MCP-04 Try local, then promote.** Add a new connector at the narrowest scope first and promote it to project or user scope only after it passes verification. Test: Newly added connectors start at local scope with a recorded verification before promotion.

## Section 04: Connecting

**P-MCP-05 Connected means a real call.** Mark a connector connected only after a real tool call succeeds, not when it appears in a list. Test: Each connector marked connected has a recorded successful call.

## Section 05: Adding your own

**P-MCP-06 Secrets live outside config.** Pass secrets to a local server as environment variables and never write a secret into a command, a committed config or the catalog. Test: No command, committed config or catalog entry contains a secret value.

**P-MCP-07 Build only when none exists.** Build a new connector only when no existing one covers the capability, and hand the build to the coding side while design registers the result. Test: A proposed connector build cites the search of existing options that found none.

Sources: Mapping to MCPs in Claude Cowork and Claude Code (field guide, v1.0, 2026); Section 01: The basics, Section 02: What ships inside, Section 03: On your machine, Section 04: Connecting, Section 05: Adding your own. Paraphrased in the kit's own words; no sentence is quoted.
