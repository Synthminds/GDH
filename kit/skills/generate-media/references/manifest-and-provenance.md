# Recording each output: manifest and prompt log

Read this file at step 18 of `generate-media`. It covers the manifest record for a generated file, the prompt log that holds the full prompt, file naming and storage, derived files, and the checks.

Evidence. The manifest file, its fields and the `record` and `check` commands belong to `find-assets`, read in this kit on 2026-11-23. The origin value `generated` and the use of the source field for the tool and job follow that skill's own example. The prompt log format is this kit's own. Result links expire per the connector cards (some within an hour; lifetimes are often not stated), so files are downloaded before they are recorded.

## 1. What is recorded where

| Item | Where | Why |
| --- | --- | --- |
| The file, its path and hash | `design/assets/manifest.json` | No record, no asset |
| Tool and job id | The record's source field | Trace back to the run |
| Model, prompt reference, generation date, inputs | The record's note | Reproduce and explain the asset |
| Output terms | The record's license field, with the terms URL | Rights for the use |
| The full prompt, negatives, settings, seed, references | The prompt log in `prompt-sheet.md` | Prompts are long; the manifest stays readable |
| Spend | The ledger in `prompt-sheet.md` | Cost control |
| Selection and consent | `design/decisions.md` | The user's choices and permissions |

## 2. File naming and storage

1. Download each result at once. Check that it opens and is the expected type and size, not an error page saved under an image name.
2. Store originals in `design/assets/generated/<kind>/<slug>/source/`.
3. Store finished files in `design/assets/generated/<kind>/<slug>/` or the project's public asset folder.
4. Name by job and version: `empty-tray-v2.png`, `hero-planter-shelf-v1-1440.webp`. Never `image (3).png`.
5. Keep rejected outputs out of the project, or in a `rejected/` folder listed in the manifest's `ignore` patterns. Do not ship them.

## 3. The manifest record

Use `find-assets`'s record command (`A`, as defined in that skill).

```
A record design/assets/manifest.json --id empty-tray-v2 --origin generated \
  --source-url "<tool name>, job <job id>" \
  --license "<tool> output terms, <terms URL>" \
  --attribution "none required" \
  --file design/assets/generated/image/empty-states/source/empty-tray-v2.png \
  --note "model <name and version as read live>; prompt P-03 in prompt-sheet.md; generated 2026-11-23; refs: 2 own sketches" \
  --date 2026-11-23
```

Field rules:

| Field | Rule |
| --- | --- |
| id | Kebab-case, job and version |
| origin | `generated` |
| source | The tool name and the job id. Not a signed result URL; those expire. |
| license | The tool's output terms and their URL, read on the record's date |
| attribution | Usually "none required"; follow the terms when they ask for credit |
| date | The day the terms were read |
| note | Model and version as read live; the prompt id in the log; the generation date; references used; consent or upload approvals by decision round |
| modified | Set on a finished file derived from a generated original |

A finished file derived from the original:

```
A record design/assets/manifest.json --id empty-tray-v2-web --origin generated --modified \
  --source-url "<tool name>, job <job id>" --license "<tool> output terms, <terms URL>" \
  --attribution "none required" --file public/img/empty-states/empty-tray.webp \
  --note "from empty-tray-v2; recolored to tokens, trimmed, WebP; prompt P-03" --date 2026-11-23
```

A paid edit (upscale, expand, background removal) gets its own job id. Add it to the note of the finished file: "upscaled, job <id>".

Then check the manifest, as `find-assets` describes:

```
A check design/assets/manifest.json --root .
```

## 4. The prompt log

One entry per prompt, in `prompt-sheet.md`, under the spend ledger.

```
## Prompt log

Kit: style line S-1; negatives N-1; palette from tokens (ground, ink, accent); model <name> (read 2026-11-23)

### P-03 empty tray
Date: 2026-11-23
Tool: <tool>; job <job id>; outputs 1; aspect 4:3; quality standard; seed <n or not exposed>
Prompt: An empty wire tray with a single paper clip resting in it, waiting. <style line S-1>. 4:3, object in the lower two thirds, generous margin, plain ground. No text, no letters, no logos, no people, one object.
References: sketch-01.png, sketch-02.png (own work)
Result: empty-tray-v1 rejected (gradient shadow); empty-tray-v2 kept (round 3)
Charged: <n> <units>
```

Rules:

1. Record the prompt exactly as sent, including the style line expanded or referenced by id.
2. Record every setting the tool accepted: model, count, aspect, quality, seed, reference ids.
3. Record the result: kept, rejected with reason, and the file names.
4. The prompt log is project data. It holds no account balance, no account id and no private URL when the repository is public.

## 5. Alternative text

1. Write alternative text for each delivered image from what it shows and its job on the page.
2. Mark a purely decorative image as decorative (empty alt).
3. Do not describe the generation process in alt text unless the client asks.

## 6. Checks

- [ ] Each kept file was downloaded and opened; none is an error page.
- [ ] Each kept file has a manifest record with origin `generated`, tool and job id, terms, model, prompt id and date.
- [ ] Each finished derivative is recorded with `modified` and its parent.
- [ ] The prompt log has an entry for every prompt that produced a kept file.
- [ ] The ledger matches the jobs in the log.
- [ ] The manifest check exits clean.
- [ ] Rejected outputs do not ship.

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Signed URL as source | The record points to a link that died | Tool name and job id as the source |
| Prompt lost | Nobody can recreate the asset | Prompt log entry per prompt |
| Unrecorded derivative | The web file has no record | Record with `modified` and its parent |
| Model unknown | "Some model" in the record | Read the model name live and record it |
| Numbered dump | `image (12).png` in the asset folder | Name by job and version |
| Rejects shipped | A rejected variant ends up in the build | Keep rejects out of shipped folders |
| Private data in the log | Account ids or balances in a public repository | Keep them in the chat, out of the files |
