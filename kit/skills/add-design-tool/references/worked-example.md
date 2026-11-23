# Worked example: one fictional tool, end to end

Read this file to see the whole procedure of `add-design-tool` run once. The tool is fictional: "Example Vector Forge", a hosted connector that turns a sketch or a rough raster mark into clean SVG paths. Its pages live on the reserved domain `example.com`. Do not add it to the real catalog.

Evidence. The `new-tool`, `check` and `doctor` commands below were run in a scratch copy of this repository on 2026-11-23. Their output is pasted as it appeared: VERIFIED. The tool calls in steps 8 and 9 are invented for the example; nothing was called.

## Step 1. Name the job

"The harness needs to turn a photographed pencil sketch into a clean SVG at `logo-identity` step 9."

Capability: `vector`. Second capability: `image-edit` (it also removes a paper background).

## Step 2. Search the catalog

```
grep -l '"vector"' kit/catalogs/tools/*.json
```

The present `vector` tools: a creative suite connector with a vectorize call, a design-tool connector with a paid vector illustration call, and two generators. The gap: none of them accepts a node budget, and the logo route needs a small, clean path set for small sizes. That sentence becomes `what`.

## Step 3. Map

| Workflow step | Capability | Tool | Call | Access | Side effects |
| --- | --- | --- | --- | --- | --- |
| `logo-identity` 9, before conversion | `vector` | Example Vector Forge | init | read | none |
| same | `vector` | Example Vector Forge | quote with a dry-run flag | read | none |
| same | `vector` | Example Vector Forge | convert with a node budget | write | spends; uploads the image |
| same | `vector` | Example Vector Forge | job status | read | none |

## Step 4. Vet

The table from the vet reference, filled for the fictional tool, is in [vet.md](vet.md), section 5. Verdict: add as DOCUMENTED. The user says yes.

## Step 5. Scaffold

Command:

```
python3 scripts/gdh.py new-tool example-vector-forge --name "Example Vector Forge" \
  --kind connector --capabilities vector,image-edit \
  --source https://example.com/vector-forge --spends --exposes \
  --what "Turns a black-and-white sketch or a rough raster mark into clean SVG paths with a node budget." \
  --install "Attach the Example Vector Forge connector in the host's connector settings." \
  --auth oauth --prefix mcp__Example_Vector_Forge__ --fallback adobe --today 2026-11-23
```

Output:

```
wrote  kit/catalogs/tools/example-vector-forge.json
wrote  kit/references/tools/example-vector-forge.md
next: fill the card, make one free or approved call, then run 'gdh.py check'
```

The entry it wrote:

```
{
  "id": "example-vector-forge",
  "name": "Example Vector Forge",
  "what": "Turns a black-and-white sketch or a rough raster mark into clean SVG paths with a node budget.",
  "kind": "connector",
  "capabilities": ["vector", "image-edit"],
  "disciplines": ["brand", "logo", "infographic"],
  "install": "Attach the Example Vector Forge connector in the host's connector settings.",
  "auth": "oauth",
  "spendsCredits": true,
  "exposes": true,
  "readOnly": false,
  "toolPrefix": "mcp__Example_Vector_Forge__",
  "firstCall": "none",
  "fallback": "adobe",
  "card": "references/tools/example-vector-forge.md",
  "source": "https://example.com/vector-forge",
  "verifiedAt": "2026-11-23",
  "evidence": "DOCUMENTED",
  "evidenceNote": "Entry written from the source page. No call was exercised."
}
```

The scaffold printed the arrays on several lines; they are joined here to save space.

## Step 6. Fill the entry and the card

Entry diff after reading the guide page:

```
-  "disciplines": ["brand", "logo", "infographic"],
+  "disciplines": ["brand", "logo"],
-  "firstCall": "none",
+  "firstCall": "init, once per conversation",
```

The infographic discipline was pruned: the tool makes marks, not charts.

Card, first sections filled (the stub said "Write this section."):

```
## What it makes

- Clean SVG paths from a photographed sketch, a scan or a rough raster mark.
- A node budget per conversion. Background removal for paper scans.
- It does not draw new marks from text. It does not export PDF or EPS.

## Connection and auth

- Layer: a directory connector. Transport: http. Sign-in: OAuth in the host.
- Claude apps: Settings, Connectors, add, sign in, then turn it on in the chat.
- Claude Code: add it with local scope first; promote after the first call passes.
- The agent cannot sign in for the user.

## Cost model

- Metered per conversion. Read the balance with the usage call and a quote with the dry-run flag. Never write the numbers.
- GATE: convert is a spend call.
```

Fill the remaining nine sections the same way. Mark GATE at the convert call and at the upload it makes.

## Step 7. Connect

The user attaches the connector and signs in. They start a fresh session. The tool appears under its prefix.

## Step 8. Exercise

1. Init: answered with a session handle.
2. Usage: answered with a balance. The number is not written anywhere.
3. Quote with the dry-run flag on a harmless test sketch the user supplied: answered with a price.
4. The user declines the spend today. Convert is not run.

Entry diff:

```
-  "evidence": "DOCUMENTED",
-  "evidenceNote": "Entry written from the source page. No call was exercised."
+  "evidence": "VERIFIED",
+  "evidenceNote": "Init, usage and a dry-run quote ran on 2026-11-23 and answered. Convert was not run (spend declined). Upload retention read from the privacy page only."
```

The label is VERIFIED because a skill relies only on the presence check and the quote at this point. The convert path is named as not exercised.

## Step 9. Wire

1. Fallback chain: Example Vector Forge falls back to `adobe`. The walk ends at `none`. No loop.
2. The adobe entry keeps `fallback: none`. The new tool is better for the logo job, so it goes first in the logo route by example, not by a chain change.
3. `capabilities.json`: no change. The logo discipline already lists `vector` first.
4. Card link in `logo-identity`, Tools section:

```
-- `vector`: hand-written SVG is the first route and needs no tool. A vector tool converts or cleans. Example cards: [adobe](../../references/tools/adobe.md), [figma](../../references/tools/figma.md).
+- `vector`: hand-written SVG is the first route and needs no tool. A vector tool converts or cleans. Example cards: [example-vector-forge](../../references/tools/example-vector-forge.md), [adobe](../../references/tools/adobe.md), [figma](../../references/tools/figma.md).
```

5. Method: the node budget needs one paragraph in `logo-identity`'s vector route reference: "Ask for a budget that keeps the smallest lockup clean; check the paths by hand after." No new skill.
6. Moment: none. The tool does not change when the agent should act.
7. Eval case: none needed, because routing did not change. To prove the router still sends this job, a case like this one would do:

```
{
  "id": "trigger-ask-gdh-vectorize",
  "kind": "triggering",
  "skill": "ask-gdh",
  "prompt": "I drew our logo on paper and photographed it. Can you turn it into a clean SVG we can print?",
  "expect": {"skills_fired": ["ask-gdh"]}
}
```

## Step 10. Version, build, check, tests, doctor

Raise `version` in `kit/kit.json` from `0.1.0` to `0.1.1`. A tool entry is a patch.

```
python3 scripts/gdh.py build
python3 scripts/gdh.py check
python3 -m unittest discover -s tests
python3 scripts/gdh.py doctor --today 2026-11-23
```

In a fresh scratch copy with the new entry, `build` printed `build: 0 file(s) written, 7 unchanged`: a tool entry changes no generated file. With the version raised, `build` printed `build: 3 file(s) written, 4 unchanged`: the two plugin manifests and the Claude marketplace now carry `0.1.1` (scratch copy, 2026-11-23). `check` printed `check: 0 finding(s), 0 accepted`. The unit tests printed `OK`. `doctor` printed `doctor: 0 warning(s) on 2026-11-23`. The same `doctor` run with `--today 2027-06-01` reported every entry as stale, for example:

```
GDH_DOCTOR_STALE  kit/catalogs/tools/vercel.json  verified 190 days ago; verify the entry again
```

## Step 11. Log

`kit/skills/logo-identity/refinement-log.md`:

```
+2026-11-23 | the owner connected a vector tool with a node budget | cataloged it; added its card link to the vector route | kit/catalogs/tools/example-vector-forge.json, kit/references/tools/example-vector-forge.md, kit/skills/logo-identity/SKILL.md
```

`CHANGELOG.md`:

```
 ## Unreleased

-Nothing yet.
+### Added
+
+- Tool `example-vector-forge` (capability `vector`), VERIFIED for init, usage and quote; convert not exercised.
```

## Step 12. Report

```
Tool: Example Vector Forge (example-vector-forge), kind connector, capabilities vector, image-edit
Job: logo-identity step 9 -> vector -> init, quote, convert, job status
Vetting: publisher Example Org, license proprietary service terms, maintained yes, data kept per privacy page, cost metered, exposes yes
Catalog: entry kit/catalogs/tools/example-vector-forge.json, card kit/references/tools/example-vector-forge.md, fallback adobe, chain checked yes
Exercised: init, usage, dry-run quote on 2026-11-23; evidence VERIFIED (convert not exercised)
Wiring: disciplines brand, logo; card linked from logo-identity; moment unchanged; eval none
Checks: version 0.1.0 -> 0.1.1, build ok, check 0, tests passed, doctor 0 warnings
Reach: branch add-example-vector-forge; merge and push by the user; then marketplace update and `/reload-plugins`
Not done: a convert run, when the user approves a spend
```

After the owner merges and pushes, users update the GDH marketplace and run `/reload-plugins`. A restart alone keeps the old version.

## A new skill, for contrast

When a tool needs a whole workflow no skill owns, the scaffold looks like this. Output from the scratch copy:

```
python3 scripts/gdh.py new-skill pattern-library --invocation user --discipline brand \
  --description "Builds repeat patterns from brand marks. Use it for a surface pattern, a wrapping paper or a background tile." \
  --today 2026-11-23

wrote  kit/skills/pattern-library/SKILL.md
wrote  kit/skills/pattern-library/refinement-log.md
wrote  kit/kit.json
wrote  README.md
wrote  kit/.codex-plugin/plugin.json
wrote  kit/README.md
next: write the skill body, name the skill in ask-gdh, then run 'gdh.py check'
```

`check` then reported `GDH_ROUTER_INCOMPLETE kit/skills/ask-gdh/SKILL.md does not name the skill 'pattern-library'` until the router named it.
