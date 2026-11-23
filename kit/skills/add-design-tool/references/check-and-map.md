# Check the catalog, then map the job

Read this file at steps 1 to 4 of `add-design-tool`. It covers how to name the job and its capability, how to search the catalog and the live session, and how to map a workflow step to a capability and to the tool's own calls with the registration template.

Evidence. The layer, transport, scope, connect and verify vocabulary comes from the owner's field guide on mapping MCP servers, read through the GDH research: DOCUMENTED for the steps it states; the registry fields it implies are proposals. The "capability before tool" rule is this kit's design. The catalog schema is the one `gdh.py check` enforces: VERIFIED on 2026-11-23.

Terms. A capability is a design job from the fixed vocabulary. A tool is one catalog entry: a connector, a local server, a plugin, a CLI, a skill, a library or an artifact type. A call is one function the tool exposes. A workflow step is one step of a discipline skill's procedure.

## 1. Name the job first

The first question is not "what is this tool" but "which step of which workflow needs it".

1. Write one line: "The harness needs to <verb> <object> at <workflow step>."
2. Pick the capability word from `kit/catalogs/capabilities.json` that names that job.
3. When two words fit, pick the narrower one. `vector` beats `image-edit` for "make an SVG".
4. When no word fits even loosely, stop here. A new word is a design decision; see [other-changes.md](other-changes.md).

| Group | Capability words |
| --- | --- |
| Images | `image-gen`, `image-edit`, `vector` |
| Video and sound | `video-gen`, `video-compose`, `avatar-video`, `audio` |
| 3D and motion | `3d-gen`, `3d-scene`, `motion` |
| Interface parts | `ui-components`, `templates`, `fonts`, `logo-search` |
| Surfaces | `canvas`, `whiteboard`, `diagram`, `moodboard`, `slides` |
| Systems and brand | `design-system`, `brand-kit` |
| Data | `dataviz`, `maps` |
| Libraries and study | `asset-library`, `reverse-engineer`, `capture` |
| Code bridge | `deploy`, `design-to-code`, `code-to-design` |
| Review | `critique` |

The live list in `capabilities.json` wins over this table.

## 2. Search before you add

1. List catalog entries with the capability. One way: search `kit/catalogs/tools/*.json` for the word.
2. Read the live tool list of this session. A connector may already be attached under a name you did not expect.
3. Check the host's connector list when the user can open it: built-in first, then the directory, then custom.
4. For each match, read its card's "Best for" and "Wrong for".
5. Ask what the new tool does that those cannot. Look for a format, a quality, a cost model, a library or a familiar editor.
6. No real difference: stop. Tell the user which present tool to use, and why.
7. A real difference: write it in one sentence. It becomes the entry's `what` field.

Decision rules:

| Finding | Action |
| --- | --- |
| A present tool covers the job equally | Do not add. Name the present tool |
| The new tool is better for this job | Add it; it becomes first in the chain for this discipline |
| The new tool is worse but works where the first is absent | Add it as a fallback |
| The new tool covers a capability no tool has | Add it; `doctor` stops reporting that gap |
| The tool is a design method, not a tool (a skill pack, a guideline set) | Add with kind `skill` or `library`, or offer it as wired, not vendored |

## 3. The mapping sheet

Fill one row for each call of the tool that a workflow will use. This sheet goes into the card under "Key tools" and "Call order".

| Workflow step | Capability | Tool | Call | Access | Side effects |
| --- | --- | --- | --- | --- | --- |
| `logo-identity` step 9, redraw as vector | `vector` | the new tool | its vectorize call | write | spends; uploads the image |
| same step, before the call | `vector` | the new tool | its quote or balance call | read | none |

Fields:

- Access: `read`, `write` or `read+write`. A step that writes must map to a call that can write. Never design around a write the tool cannot do.
- Side effects: `none`, `spends`, `uploads`, `publishes`, `sends`, `deletes`. Any value but `none` is a gate point in the card.

When two present tools share a capability, the skill text names the capability and the catalog's fallback chain picks the tool. Never hard-code a tool into a procedure step.

## 4. The registration template

The field guide proposes a registration record. The GDH catalog holds part of it in the entry and part in the card. Fill each line from a page you read or a call you made.

| Template field | Where it goes in GDH | Rule |
| --- | --- | --- |
| name | entry `id`, `name` | Unique, stable, kebab-case id |
| layer: built-in, directory, custom | card, "Connection and auth" | Custom connectors may need a paid host plan; say so |
| transport: http or stdio | entry `kind`; card, "Connection and auth" | Prefer http over the legacy streaming transport when both exist |
| url or command and args | entry `install` | A local server pins `package@version` |
| env vars | entry `auth` as `env:<NAME>` | Names only, never values |
| auth method | entry `auth` | The user completes sign-in |
| scope: local, project, user | card, "Connection and auth" | Start local; promote after the first call passes |
| config location | card, "Connection and auth" | Per host; never a file inside a settings folder by guess |
| tools | card, "Key tools" | Each call the harness uses |
| access, side effects | card, "Key tools"; entry `readOnly`, `spendsCredits`, `exposes` | True when in doubt |
| capabilities | entry `capabilities` | From the vocabulary, most important first |
| safety: inputs validated, secrets in env, tested | card, "Limits and failure modes" | For a local or third-party server |
| smoke test | entry `evidenceNote`; card, "Evidence" | The free call used, date, result |
| known limits | card, "Limits and failure modes" | Include what fails silently |
| last verified, review by | entry `verifiedAt`; `doctor` flags after 180 days | |
| status: trial, active, retired | the label and the changelog | A new entry is DOCUMENTED until a call runs |

## 5. Hosts

A tool can need different steps per host. Record each host the owner uses in the card, under "Connection and auth".

| Host | How the user connects | How to verify |
| --- | --- | --- |
| Claude apps and Cowork | Settings, Connectors, add, sign in, then turn it on in the chat | The tool appears in the session list |
| Claude Code | The add command with a scope, then a fresh session | The list and get commands show it connected |
| Other hosts | Their own config file | Mark "not covered by source" until read |

A config change needs a host restart before the tool appears. Tell the user. The agent never edits a credential file.

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Tool first | "Add X" with no job named | Write the one-line job first |
| Shiny duplicate | A second tool for a covered job with no stated gap | Name the present tool; stop |
| Vocabulary stretch | `image-gen` used for a font tool | Pick the right word, or propose a new one |
| Write on a read tool | A workflow step writes through a read-only connector | Map a write-capable call, or change the step |
| Hidden side effect | An import that uploads to public storage | Side effects column; gate point in the card |
