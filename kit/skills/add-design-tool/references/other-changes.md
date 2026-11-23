# Other changes: assets, capabilities, brand packs, retiring, review

Read this file when the change is not a new tool: a new asset source, a new capability word, a new brand pack, retiring a tool, re-verifying stale entries, or the quarterly doctor review.

Evidence. The schemas and commands were read and run on 2026-11-23: VERIFIED for the commands. The review interval and the license-before-use rule come from the kit principles and the DesignOps Handbook, chapters 4 and 5: DOCUMENTED as method. The quarterly interval is a default.

## 1. A new asset source

An asset source is a site of free icons, fonts, photos, components, models or similar. It goes into `kit/catalogs/assets.json`, not into the tool catalog.

1. Search `assets.json` for the site and for its group. Stop when it is present.
2. Read the site's license page in this session. Read the terms for generated or trademarked content.
3. ASK: show the license summary. "Add it?"
4. Add one object to `sources`:

| Field | Rule |
| --- | --- |
| `id`, `name`, `url` | Kebab-case unique id; https URL |
| `group` | One of the groups already in the file |
| `holds` | What a person finds there, and one line on when to use it |
| `license` | The license name as the site states it, plus what it requires |
| `attribution` | Whether a credit is required, and its form |
| `commercialUse` | `yes`, `yes-with-limits`, `reference-only`, `varies` or `unknown` |
| `fetch` | How an asset is taken: a download, a package command, a registry |
| `risk` | Known traps: mixed licenses, trademarked content, account-bound terms, a common default look |
| `verifiedOn` | The date you read the license page; `null` when you did not |

5. Set `verifiedOn` only after you read the license page in this session. An unread source keeps `null`, and `find-assets` reads the license before any use.
6. Run `check` and log the change. A catalog-only change is a patch.

## 2. A new capability word

The vocabulary is fixed on purpose. A new word is a design decision.

1. Check that no existing word covers the job, even loosely. Write why each near word fails.
2. ASK the user for a yes. Show the word and its one-line meaning.
3. Add the word and its meaning to `capabilities` in `capabilities.json`.
4. Add it to the list of each discipline whose skill will use it, in preference order.
5. Name it in that skill's Tools section.
6. Add the first tool entry for it. Otherwise `doctor` reports a capability with no tool.
7. Log it. A new word is a minor change.

## 3. A new brand pack

A brand pack is the portable copy of a brand: `brands/<slug>/`.

```
DS="python3 kit/skills/design-system/scripts/ds.py"
$DS init      brands/<slug> --name "<Name>"
$DS validate  brands/<slug>/tokens.json
$DS contrast  brands/<slug>/tokens.json
$DS export    brands/<slug>/tokens.json --css brands/<slug>/tokens.css
$DS design-md brands/<slug>/tokens.json --readme brands/<slug>/README.md -o brands/<slug>/DESIGN.md
$DS specimen  brands/<slug>/tokens.json -o brands/<slug>/specimen.html
```

1. Run `design-system` for the content. This skill only adds the pack to the repository.
2. The public repository holds the fictional example pack and the template only. A real brand's pack lives in a private copy or in the project that uses it.
3. Every token has a usage note. Every value has a source line in `SOURCE.md`, or INFERRED.
4. `check` requires `README.md` and `tokens.json` in each pack folder.
5. To use the pack in Claude artifacts, publish it through `design-system`.

## 4. Retire a tool

Retire when the tool is gone, unmaintained, or replaced by a better tool for every job it served.

1. Find every entry whose `fallback` names it. Point each to the next tool or to `none`. Walk the chains again.
2. Find every card link to it in the skills and their references. Replace each with another example card, or remove the row.
3. Find every mention in `kit/kit.json` moments and wired entries. Change or remove.
4. Delete `kit/catalogs/tools/<id>.json` and `kit/references/tools/<id>.md`.
5. Run `build`, `check`, the tests and `doctor`. `doctor` reports a capability left with no tool.
6. Log the retirement with its reason in the changelog and in each touched skill's refinement log.
7. Tell the user what replaces it, or that the capability now has no tool.

Search for references:

```
grep -rn "<id>" kit/ docs/ evals/
```

## 5. Re-verify a stale entry

`doctor` reports an entry whose `verifiedAt` is more than 180 days old.

1. Read the source page again. Read the live tool list and the guide in a session where the tool is connected.
2. Compare with the card: calls renamed, removed or added; cost model changed; new limits; new exposure.
3. Make the smoke test again. Set the label from what ran today, not from what ran last time.
4. Update the card and the entry. Set `verifiedAt` to today.
5. Check each skill reference that describes the tool's method. Fix drift there too.
6. When the tool is gone, retire it (section 4).

## 6. The quarterly doctor review

Default: once a quarter, and before a release.

```
python3 scripts/gdh.py doctor
python3 scripts/gdh.py doctor --json > /tmp/doctor.json
```

Work the report in this order:

| Warning | Action |
| --- | --- |
| `GDH_DOCTOR_NO_CARD` | Write the card, or retire the entry |
| `GDH_DOCTOR_STALE` | Re-verify (section 5) |
| `GDH_DOCTOR_UNTESTED` | Read the primary source; raise to DOCUMENTED, or keep and note why |
| `GDH_DOCTOR_CAPABILITY_NO_TOOL` | Find a tool for it, or accept the gap and say so in the review |
| `GDH_DOCTOR_NO_EVAL` | Add the triggering cases |
| `GDH_DOCTOR_NO_REFINEMENT_LOG` | Add the log |
| Asset sources with `verifiedOn: null` | Read the license pages of the most used ones first |

Also, by hand:

1. Walk every fallback chain. Each ends in `none` with no loop (see the wiring reference).
2. Read each refinement log for repeated corrections. A correction seen twice becomes a rule or a check.
3. Mark tools nobody used in the quarter. Ask the owner whether to retire them.

Write the result as a dated entry in `CHANGELOG.md` under "Unreleased": what was re-verified, raised, lowered, retired and left open.

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| License by memory | `verifiedOn` set with no page read | Set it back to `null` |
| Orphan fallback | An entry falls back to a retired id | `check` reports it; re-point it |
| Vocabulary creep | A new word for each tool | Section 2: check every near word first |
| Private pack in public | A real brand's tokens in this repository | Remove; keep it private |
| Review skipped | Doctor warnings grow quarter over quarter | Run the review; log it |
