# Wire the tool into the kit

Read this file at steps 12 to 19 of `add-design-tool`. It covers how a cataloged tool becomes reachable: disciplines, the fallback chain, capability order, card links, moments, reference files, new skills, eval cases, the version bump, the build, the logs and how the change reaches installs.

Evidence. The engine commands and rules were run and read on 2026-11-23: VERIFIED. The "extend a reference before adding a skill" rule and the moment limits come from the GCH kit design, read through the GDH research: DOCUMENTED as method.

Terms. The fallback chain is the path from one tool's `fallback` to the next. A moment is an always-loaded line that tells the agent when to start or offer a skill. The owning skill is the skill named for a discipline in `capabilities.json`.

## 1. How a skill finds a tool

A skill never names a tool as the only way to do a step. At run time it:

1. Reads its discipline's capability list in `capabilities.json`, in preference order.
2. Reads `kit/catalogs/tools/` for entries with that capability.
3. Checks which ones are present in this session.
4. Reads the card of the chosen tool, then follows `fallback` when the tool is absent.

So most tools need no skill change. The entry is enough.

## 2. Disciplines

1. Read the `disciplines` the scaffold filled. Keep only those the tool really serves.
2. A discipline must exist in `capabilities.json`; `check` reports an unknown one.
3. A tool that serves a discipline through a capability not in that discipline's list does not reach it. Either add the capability to the list (section 4) or drop the discipline.

## 3. The fallback chain

Each entry has one `fallback`. Together they form chains.

1. Set the new tool's `fallback` to the next best present tool for its main capability, or `none`.
2. Is the new tool a better second choice for an existing tool? Then re-point that tool's `fallback` to it.
3. Walk the chain from each changed entry. An agent stops at a tool it has already tried.
4. Every chain ends in `none`. A loop is not allowed, even among free tools that do the same job: a missing tool can send the agent round it. When two tools back each other up, point the second one at `none`, and say in its card that the chain ends there.
5. Prefer a last link that needs no spend and no sign-in.
6. A fallback must share the capability that the step needs. A chain that jumps capability is broken.

List every loop. The output must be empty:

```
python3 - <<'PY'
import json, glob
fb = {json.load(open(f))["id"]: json.load(open(f))["fallback"] for f in glob.glob("kit/catalogs/tools/*.json")}
for start in fb:
    seen, cur = [], start
    while cur != "none" and cur not in seen:
        seen.append(cur); cur = fb.get(cur, "none")
    if cur != "none":
        print("loop:", " -> ".join(seen + [cur]))
PY
```

## 4. Capability order in a discipline

`capabilities.json` lists, for each discipline, the capabilities its skill may use, in preference order.

1. Change the order only when the new tool changes which capability should be tried first for that discipline.
2. Add a capability to a discipline only when its skill's procedure has a step that needs it.
3. Mention a newly added capability in that skill's Tools section, or the skill will not use it.
4. Every change to `capabilities.json` is a design decision. Log it.

## 5. Card links in a skill

1. Add a card link to a skill's Tools table only when the tool is a good example for that capability.
2. Keep the row a capability row: "`vector`: ... Example card: [name](../../references/tools/<id>.md)".
3. From a reference file inside a skill, the path is `../../../references/tools/<id>.md`.
4. Never write "call X" in a procedure step.

## 6. Moments

A moment says when to start or offer a skill. Tools are not offered by moments; skills are.

1. Change a moment only when the new tool makes a skill worth offering at a new point in the work.
2. A moment offers three skills at most. It may start only a model-invoked skill.
3. Keep the rendered moments text inside its budget. `check` measures it.
4. Earned means: without the moment, the agent would miss the skill at that point. A hunch is not earned.

## 7. Method: extend a reference before adding a skill

| Situation | Change |
| --- | --- |
| The tool does a known capability the usual way | None. Entry and card only |
| The tool needs a workflow across several steps of a discipline | Extend one reference file of the owning skill; link it at the step |
| The tool is a good example for a capability | Add its card link to the Tools table |
| No skill owns the behavior at all | A new skill, section 8 |

Keep the reference file under 400 lines. When it would pass that, split it and link both from `SKILL.md`.

## 8. A new skill

Add one only when the catalog and a reference file cannot carry the behavior.

```
python3 scripts/gdh.py new-skill <name> --invocation user \
  --discipline <discipline> --description "<what it does and when to use it>"
```

1. The command scaffolds the folder and a refinement log, registers the skill in `kit/kit.json`, and rebuilds the generated files.
2. Write the body in the eight fixed sections. Keep `SKILL.md` a router: 150 lines and 1,500 words at most.
3. Prefer `user` invocation. A model-invoked skill spends the shared description budget.
4. Name the new skill in `ask-gdh`. `check` reports `GDH_ROUTER_INCOMPLETE` until you do.
5. A new discipline goes into `capabilities.json` with the skill as its owner.
6. With GCH installed, `gch:skill-crafter` and `gch:writing-for-agents` help with the body.

## 9. Eval cases

`evals/cases/triggering/` holds triggering cases for model-invoked skills and negative cases.

| Change | Case to add |
| --- | --- |
| A new model-invoked skill | Two cases: a plain user prompt that should start it. The scaffold writes a stub; replace its prompt |
| A new user-invoked skill | A case for `ask-gdh` with a prompt that needs the new skill, expecting `ask-gdh` to fire |
| A new moment or trigger phrase | A case with a prompt at that point in the work |
| A tool that changes no routing | None |

Case shape:

```
{
  "id": "trigger-ask-gdh-vectorize",
  "kind": "triggering",
  "skill": "ask-gdh",
  "prompt": "I drew our logo on paper and photographed it. Can you turn it into a clean SVG we can print?",
  "expect": {"skills_fired": ["ask-gdh"]}
}
```

Write the prompt as a user would. Do not reuse the words of the skill's description. The `id` equals the file name.

## 10. Version, build, check, tests, doctor

Raise `version` in `kit/kit.json` first. Use the release class in section 11: a tool entry or card is a patch, `0.1.0` to `0.1.1`. `build` copies the version into the plugin manifests.

Why: a Claude Code plugin that sets `version` keeps users on that version until it changes. Evidence: DOCUMENTED (Claude Code plugin reference, read through the GDH research). Not exercised in this build. A catalog change without a version bump never reaches an installed copy.

```
python3 scripts/gdh.py build
python3 scripts/gdh.py check
python3 -m unittest discover -s tests
python3 scripts/gdh.py doctor
```

- `build` regenerates the plugin manifests, the marketplaces, the moments text and the catalog blocks of the README files.
- `check` must exit 0. Fix a finding at its cause. Never weaken a rule.
- `kit/scan.accepted.json` is for a true false positive only, with a written reason.
- `doctor` is advice: stale entries, UNTESTED entries, capabilities with no tool, skills with no eval case.

## 11. Log the change

One line in the owning skill's `refinement-log.md`:

```
YYYY-MM-DD | observation | change | files
```

One line in `CHANGELOG.md` under "Unreleased", in the right group:

| Change | Release class |
| --- | --- |
| A tool entry, a card, an asset source, a fallback | patch |
| A new skill or a new capability word | minor |
| A kernel or registry schema change | major |

Move the changelog lines from "Unreleased" under a heading with the new version and the date.

## 12. How the change reaches installs

1. The work sits on a branch in a scratch checkout. Committing, pushing and opening a pull request are the user's steps, or need the user's yes.
2. After the owner merges and pushes, a user updates the GDH marketplace in Claude Code and runs `/reload-plugins`. Evidence: DOCUMENTED, not exercised.
3. A project export made with `gdh.py export` does not update itself. Run the export again in that project.
4. Restarting a session without a marketplace update loads the old version. Do not tell the user that a restart alone is enough.
