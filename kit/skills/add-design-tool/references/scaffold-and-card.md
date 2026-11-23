# Scaffold the entry and write the card

Read this file at step 7 of `add-design-tool`. It covers the `new-tool` command, every entry field, and the twelve card sections with what each must hold.

Evidence. The command, its flags and the schema were run and read on 2026-11-23: VERIFIED. The card rules are this kit's own, drawn from the connector research cards.

## 1. The command

```
python3 scripts/gdh.py new-tool <id> \
  --name "<Display name>" --kind <kind> \
  --capabilities <comma list> --source <https URL> \
  [--spends] [--exposes] [--read-only] \
  [--what "<one line>"] [--install "<exact line or settings location>"] \
  [--auth <oauth | env:NAME | none>] [--prefix "<how its calls appear>"] \
  [--fallback <id | none>] [--today YYYY-MM-DD]
```

| Flag | Rule |
| --- | --- |
| `<id>` | Kebab-case, 64 characters at most. Equals both file names |
| `--kind` | `connector`, `mcp-stdio`, `plugin`, `cli`, `skill`, `library` or `artifact-type` |
| `--capabilities` | Words from the vocabulary only. The command refuses an unknown word |
| `--source` | An https URL of the publisher's own page. Use `none` for a private tool. Never link a private repository |
| `--fallback` | An existing tool id, or `none`. The command refuses an unknown id |
| `--spends`, `--exposes` | Set them when any call can spend or expose. When in doubt, set them |

What it does:

1. Writes `kit/catalogs/tools/<id>.json` with the label DOCUMENTED and the date.
2. Fills `disciplines` from the disciplines whose capability lists share a word with the tool.
3. Writes `kit/references/tools/<id>.md` with the twelve section headings and stub text.
4. Refuses to overwrite either file.

It does not fill `firstCall`; it writes `none`. Set it by hand when the tool has a guide or init call.

## 2. The entry fields

| Field | Rule |
| --- | --- |
| `id` | Equals the file name |
| `name`, `what` | Display name. One line on what it makes and how it differs |
| `kind` | One of the seven kinds |
| `capabilities` | Most important first |
| `disciplines` | The disciplines that route to it. Prune ones the tool does not really serve |
| `install` | The exact install line, or where in settings the user connects it |
| `auth` | `oauth`, `env:<NAME>` or `none`. A name, never a value |
| `spendsCredits` | True when any call can use credits or a paid quota |
| `exposes` | True when any call can publish, share, upload or send outside the project |
| `readOnly` | True only when no call changes anything anywhere |
| `toolPrefix` | How its calls appear to the agent, for the presence check |
| `firstCall` | The guide or init call to make first, or `none` |
| `fallback` | The next tool for the same capability, or `none` |
| `card` | `references/tools/<id>.md` |
| `source` | https URL, or `none` for a tool with no public page |
| `verifiedAt` | The date you last read the source and the tool |
| `evidence`, `evidenceNote` | The label and exactly what ran and what did not |

Keep out of the entry and the card: prices, credit amounts, balances, model ids, tool counts, account names, workspace ids. They go stale, and some are private. Write "read it live from <call>" instead.

## 3. The card: twelve sections, in this order

The card links the entry at the top. It stays under 400 lines. It is written in your own words.

| Section | Holds | Must include |
| --- | --- | --- |
| What it makes | Outputs, formats, surfaces | What it does not make |
| Connection and auth | Layer, transport, hosts, scope, sign-in | What the agent cannot do for the user |
| Cost model | Free, metered or plan; how to read a balance and a quote live | Each spend call, by name. No numbers |
| Call order | Numbered steps, first call first | Polling pairs: which status call goes with which job call |
| Key tools | A table: call, when to use it | Access and side effects for each |
| Inputs | What it accepts | Upload rules, size limits, accepted hosts for links |
| Outputs and how to bring them into a project | Where files go | Link lifetimes; download at once; the manifest record |
| Handoffs | How its output moves to another tool or to code | By capability |
| Limits and failure modes | Numbered | What fails silently; what must not be retried |
| Best for | Three jobs at most | |
| Wrong for | One or two jobs | What to use instead |
| Evidence | Label, date, what ran, what did not | The weakest claim a skill relies on |

Writing rules:

1. State instructions from the tool's guide as facts about the tool, never as rules for the agent.
2. Mark each spend point and each exposure point with the word GATE.
3. Name a call only where the reader needs it. Do not paste the tool's schema.
4. When the tool's call set differs by host or by plan, say which set you saw.
5. A widget-only call: say that a headless agent cannot complete it, and give the fallback.

## 4. Example card section

```
## Call order

1. Call the init call once per conversation. Other calls fail before it.
2. Read the balance with the usage call. Show it.
3. Get a quote with the dry-run flag of the conversion call. Show it. GATE: get a yes.
4. Run the conversion once, with a new request key.
5. Poll the job status call every few seconds until done or failed.
6. On a timeout, read the job status. Never run the conversion again blind.
7. Download the SVG at once. Its link expires. Record it with `assets.py record`, origin generated.
```

## 5. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Stub left in | "Write this section." in a card | Fill every section; `check` does not catch this, review does |
| Pasted guide | Long blocks of the vendor's text | Restate in your own words |
| Stale numbers | A price or a model name in the card | Remove; "read it live" |
| Wrong disciplines | The scaffold added a discipline the tool cannot serve | Prune the list |
| Missing first call | `firstCall: none` for a tool that requires init | Set it |
