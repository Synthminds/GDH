# License and provenance for 3D

Read this file at step 17 of `three-d`. It covers license classes for models, materials and environment maps, the risks particular to 3D, the manifest records for sourced, generated, modeled and optimized files, and consent for scanned objects and people.

Evidence. The license findings come from the GDH asset research, which checked licenses per source on 2026-11-23: CC0 libraries confirmed in their own files, a low-poly source with two conflicting license statements, community model sites with per-model licenses and some no-AI notices, museum collections with CC0 on marked items only, and a live-API credit duty on one CC0 library. Sources marked unverified there stay unverified; `find-assets` holds the current status. The manifest fields and the `record` command belong to `find-assets`. Nothing here is legal advice.

## 1. License classes for 3D assets

| Class | Typical sources | Can ship in client work | Duties |
| --- | --- | --- | --- |
| CC0 | Main HDRI, material and model libraries; museum items marked CC0 | Yes | None for the asset; a credit when a library's live API is used |
| CC BY | Many community models; many reference sample models | Yes | Credit in the form the license asks |
| CC BY-SA | Some community models | Only when share-alike on the derivative is acceptable | Credit; derivative under the same license |
| NC or ND | Many community models; non-CC0 museum items | No for client work; ND blocks the pipeline's changes | Not applicable |
| Pack license | Low-poly kits | Usually yes; read the license file inside the pack | Often no redistribution of the assets as assets |
| Vendor output terms | Generated models | As the tool's terms say | Read the terms; record them |
| Own work | Modeled or procedural | Yes | Record as own |

Rules:

1. Read the license on the model's own page, and the license file inside a downloaded pack. A site-level statement is not enough when items differ.
2. Reject NC for client work. Reject ND when the pipeline will decimate, retexture or compress, because those are modifications.
3. A no-AI notice on a model forbids using it to train or prompt a generator. Do not upload such a model as a generation reference.
4. CC0 does not clear trademarks or design rights. A model of a branded car, phone or chair can still infringe when used as the client's product or in an ad.
5. Unverified license entries in the catalog need a direct read of the license page before use.

## 2. Records for each file

Record every file that ships: the model, each external texture, the environment map, the poster render. Use `find-assets`'s record command (`A` below, as in that skill).

A sourced model:

```
A record design/assets/manifest.json --id chair-oak-source \
  --source-url <model page> --license "CC-BY-4.0, <license URL>" \
  --attribution "<title> by <author>, CC BY 4.0" \
  --file design/assets/3d/chair-oak/source/chair.glb --date 2026-11-23
```

An environment map:

```
A record design/assets/manifest.json --id studio-hdri-1k \
  --source-url <asset page> --license "CC0-1.0, <license URL>" \
  --attribution "none required" --file public/3d/hdri/studio-1k.hdr --date 2026-11-23
```

A generated model. Name the tool and the job in the source field; put the model, the reference inputs and the generation date in the note:

```
A record design/assets/manifest.json --id planter-generated-source --origin generated \
  --source-url "<tool>, job <job id>" --license "<output terms>, <terms URL>" \
  --attribution "none required" --file design/assets/3d/planter/source/planter.glb \
  --note "model <name read live>; inputs: 3 client photos (upload approved, see decisions round 2); generated 2026-11-23" \
  --date 2026-11-23
```

The optimized file is a modification of the source. Record it with the pipeline summary:

```
A record design/assets/manifest.json --id chair-oak-web --modified \
  --source-url <model page> --license "CC-BY-4.0, <license URL>" \
  --attribution "<title> by <author>, CC BY 4.0, modified" \
  --file public/3d/chair-oak/chair.glb \
  --note "decimated, retextured, KTX2 and meshopt; pipeline log in three-d-plan.md" \
  --date 2026-11-23
```

A procedural or modeled asset:

```
A record design/assets/manifest.json --id hero-torus --origin own \
  --source-url "project: procedural geometry in src/three/hero.ts, round 2" \
  --license "owned by the client" --attribution "none required" \
  --file public/3d/hero/poster.webp --date 2026-11-23
```

Then run the manifest check and regenerate the notices file, as `find-assets` describes.

## 3. Credits

1. A CC BY model needs a credit where the license asks: a credits page or the page footer is common. Write the credit line in the record exactly.
2. Mark modified works as modified.
3. A live API credit duty (for example a "powered by" line) applies only when the page calls the library's API at run time. Downloading the asset into the project avoids it.
4. Keep the credit when the model is decimated or retextured. A modification does not remove the duty.

## 4. Consent for scans and photos

1. A model made from photos of a client's product needs the client's permission to upload those photos to a tool. That is the exposure gate.
2. A scan or a generated model of a real person needs that person's written consent on record.
3. A model of a private interior or an identifiable property needs the owner's permission.
4. Record the consent as a consent entry in `design/decisions.md`. Use the fixed entry format of the project template, with a scope that starts `consent,`. The shape and an example are in `generate-media`, rights reference, section 2. Reference the entry in the manifest note.
5. Keep the signed document out of the repository. The entry records only where it lives.
6. A revocation is a new consent entry with `Decision: consent revoked (by <who>)`. Delete the scan or model and its generated files. Never edit the old entry.

## 5. Hosting and delivery

1. Self-host every model, texture, environment map and decoder file. Do not hotlink a tool's signed link or a library's CDN.
2. A signed result link can expire within an hour. Download at once and check the file is a real GLB, not an error page.
3. Keep the source, the intermediate files and the final file in `design/assets/3d/<slug>/`. Ship only the final file from `public/` or the project's asset folder.

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Site license assumed | A model from a community site shipped as if CC0 | Read the model's own license |
| ND modified | A no-derivatives model decimated and compressed | Reject ND for the pipeline |
| Credit lost in the pipeline | The optimized file ships with no credit | The credit follows the modified file |
| Branded model as product | A CC0 model of a known product used in an ad | Trademark and design rights still apply |
| Generated with no record | A GLB in the project with no origin | Record origin `generated`, tool, job, terms |
| Upload without consent | Client product photos sent to a generator | Exposure gate, with the yes in the record |
| Hotlinked GLB | The scene loads from a tool's signed URL | Self-host |
