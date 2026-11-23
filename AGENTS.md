# Working on the GDH repository

This file is for a person or an agent who changes GDH itself. To use GDH in a design project, read [README.md](README.md).

## What this repository is

GDH is a kit of design skills, rules and catalogs. The plugin is the `kit/` folder. The engine is `scripts/gdh.py`. Architecture and maintenance notes are in [docs/GDH.md](docs/GDH.md).

The front door: every design session starts with the `align` skill. Without a confirmed `design/brief.md` it runs the full interview. With one it re-aligns in a few questions. `--full` forces the full interview. Keep the kernel, the moments, the README files and the export block in step with this rule.

## Commands

Run each command from the repository root. Each needs Python 3.9 or later and nothing else.

| Command | Does |
| --- | --- |
| `python3 scripts/gdh.py build` | Writes the generated files from `kit/kit.json`: both plugin manifests, both marketplace files, `kit/canon/MOMENTS.md` and the catalog blocks in the two README files. |
| `python3 scripts/gdh.py check` | Runs every rule. Exits 1 on any finding. `--json` gives machine output. `--codes` lists the rule codes. |
| `python3 -m unittest discover -s tests` | Runs the unit tests. |
| `python3 scripts/gdh.py doctor` | Lists stale catalog entries, untested tools, capabilities with no tool and skills with no eval case. Advice, not a gate. |
| `python3 scripts/gdh.py export --repo <dir> --dry-run` | Shows what an export into a project would write. |
| `python3 scripts/gdh.py new-tool <id> ...` | Scaffolds a tool entry and a card. |
| `python3 scripts/gdh.py new-skill <name> ...` | Scaffolds a skill, registers it and rebuilds. |

Before you say a change is done: run `build`, then `check`, then the tests. All three must pass.

## Rules

1. `kit/kit.json` is the registry. Register a skill there, or remove its folder. Never leave a stray.
2. Never edit a generated file by hand. Change the source, then run `build`.
3. Fix a finding at its cause. Do not weaken a rule to pass it. `kit/scan.accepted.json` is for a true false positive only, with a written reason. Some codes need an exact path and the finding's `match` value; see `docs/GDH.md`, section 3.
4. Keep `SKILL.md` a router: 150 lines and 1,500 words at most, with the eight sections in the fixed order. Depth goes in `references/`, 400 lines at most for each file.
5. Link every file in a skill folder from its `SKILL.md`, and say when to read it.
6. A skill routes by capability. It names a tool only as an example, with a link to the tool card.
7. Write no price, credit amount, balance, model id or tool count into a skill body. The agent reads these live.
8. A number is a gate only when a primary source was read, or the rule has no number. Otherwise write "Default:" before it.
9. Label each claim about a tool or a result VERIFIED, DOCUMENTED or UNTESTED. Raise a label only after a real call or a real render.
10. Use the fixed terms in one sense: direction, brief, decision record, gate, default, spend call, tell.
11. Prose is plain technical English: one instruction in a sentence, active voice, present tense, no emoji, no em dash, no HTML comment, ASCII punctuation.
12. Write in your own words. Do not copy sentences from a book, a vendor guide or another skill. Name the source in a short list.
13. Scripts use the Python standard library only, make no network call, write only to paths given as arguments, exit 0 on a pass and 1 on findings, and take `--json`. Each script has tests under `tests/`.
14. Log each skill change in that skill's `refinement-log.md`: `YYYY-MM-DD | observation | change | files`. Add a line to [CHANGELOG.md](CHANGELOG.md).
15. Record a decision that changes the architecture as a short file in `docs/adr/`.

## The public-repository rule

This repository is public. Treat every file as published.

- Write no email address, account id, workspace or team id, credit balance, private link or client name anywhere.
- Write no artifact address of a real account. Use a placeholder such as `<artifact link>`.
- The only brand pack in the public tree is the fictional example under `brands/example-harbor-lantern/`, plus `brands/_template/`.
- The owner's private packs may sit under `brands/` in a local working copy. `.gitignore` ignores every folder under `brands/` except the template and the example, so a new pack needs no edit. Never write a pack's folder name in a tracked file. Put an extra local rule in `.git/info/exclude`. See [brands/README.md](brands/README.md).
- A tool card may name a tool, its public documentation and its public tool names. It holds no quote, no balance and no private project name.
- `check` scans for keys, tokens, email addresses and id-like strings. It cannot find a client name. Read your diff before you commit.

## Relations to other harnesses

- GDH does not depend on GCH. It names a GCH skill only as an option when GCH is installed.
- Do not copy code or prose from GCH or from any wired skill. Wired skills are named in `kit/kit.json` with their install lines and are not vendored.
- The text that GCH uses to offer GDH is kept in [docs/HANDOFF-GCH.md](docs/HANDOFF-GCH.md). Change both sides together.

## Where things are

| Need | Path |
| --- | --- |
| The always-on rules | `kit/canon/KERNEL.md` |
| Why the rules are what they are | `kit/canon/PRINCIPLES.md` |
| The capability words | `kit/catalogs/capabilities.json` |
| Tool entries and cards | `kit/catalogs/tools/`, `kit/references/tools/` |
| Free asset sources | `kit/catalogs/assets.json` |
| Triggering eval cases | `evals/cases/triggering/` |
| Open work | `docs/GDH.md`, section "Open work" |
