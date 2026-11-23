# Source, generate or model

Read this file at steps 5 to 9 of `three-d`. It covers the route choice, sourcing a licensed model, generating one from photos or text, modeling one, the spend and exposure gates, and what a generated mesh needs before web use.

Evidence. The source list and license classes come from the GDH asset catalog research, where license status was checked per source on 2026-11-23 (some sources are verified, others are not; `find-assets` holds the status). The generation facts (photo-to-3D beats text-to-3D, one photo invents the back, provider parameter names differ, a wrong parameter name runs with no polygon limit, started 3D jobs may not be cancellable) come from the 3D connector cards, read 2026-11-23. No model was generated in research. The Khronos asset conventions were read 2026-11-23.

## 1. Choose the route

| Situation | Route |
| --- | --- |
| A generic object, prop, material or environment | Source a licensed asset |
| The client's real product, with photos or CAD | Generate from photos, or convert the CAD file, then repair |
| A precise product with exact dimensions and CAD available | Convert CAD; never generate |
| A stylized or abstract shape | Model it: procedural geometry in code, or a simple model in Blender |
| A scene of many objects | Build in a scene tool or in code from sourced and modeled parts |

Rules:

1. Source first. It costs nothing and its license is known.
2. A real product must look like the real product. Use the client's photos or CAD, never a look-alike.
3. Procedural geometry in code (a torus, a terrain from data, extruded SVG) is often the lightest and most original route.

## 2. Source a licensed model

Run `find-assets` with the 3D group. It searches the catalog, reads the license and writes the record.

| Source class | License pattern | Note |
| --- | --- | --- |
| CC0 libraries of models, materials and environment maps | No attribution, commercial use allowed | The lowest-risk pulls. Some require a credit only for live API use. |
| Low-poly kits | CC0 or a pack-specific license | Read the license file inside each pack; some forbid redistributing the assets as assets |
| Community model sites | Per model: CC BY common, CC0, NC and ND variants | Filter for downloadable and license. NC is unusable for client work. Uploads may infringe. |
| Museum open-access collections | CC0 on marked items only | Other items are non-commercial |
| Reference sample models | Per model, many CC BY | Meant for renderer tests, not brand visuals |
| Research-scale object indexes | Per-object licenses, many non-commercial | Not a clean asset source |

Rules:

1. Read the license on the model's own page. A site-level license is not enough when items differ.
2. Record the author, the license, the source page and the date before the file enters the project.
3. Self-host environment maps. Do not rely on a helper library's CDN presets in production.
4. A third-party product, vehicle or character model can carry trademark or design rights even under CC0. Do not use one as the client's product.

## 3. Generate from photos or text

### Inputs

1. Photos beat text. Ask for photos of the object: default three views, front, side and back. Four views when the tool takes them.
2. Shoot on a plain background, even light, no harsh reflections, the whole object in frame, the same distance each time.
3. One photo gives one side. The tool invents the back. Say so in the result and in the record.
4. Text-to-3D takes one object per prompt. Expect less faithful geometry.
5. Ask where the model goes: web viewer, game, print or render. The use sets the triangle target.

### The calls

1. Call the tool's guide or workflow first. Read the card.
2. Read the model list and parameters live. Parameter names for polygon count differ between providers. A wrong name may be dropped silently and the job runs with no limit.
3. Set the polygon target for the use, with the parameter name the live schema shows.
4. Ask for web delivery options when the tool has them: a reduced texture size, compressed geometry, KTX2 or WebP textures.
5. GATE: quote the job. Show the model, the quoted cost, the balance and what the user gets. Get a yes. Call once with a new request key. Keep the job id.
6. A started 3D job may not be cancellable. Say so before the yes.
7. Poll at the interval the card gives. Download the result link at once; signed links can expire within an hour.
8. A failed job: read the reason. Retry only with the user's yes, with the same request key when the tool says a retry with the same key is free.

GATE before any upload: the client's photos, CAD files or unreleased product images leave the project. Ask first. Name the tool and what it keeps. Upload only what the job needs.

### What a generated mesh needs

Generated meshes arrive dense and uneven, with poor UVs and baked lighting. Never ship one as delivered.

| Problem | Check | Fix |
| --- | --- | --- |
| Too many triangles | Inspect the count | Decimate or remesh to the budget |
| Uneven, messy topology | Wireframe view | Remesh (the tool's remesh, or voxel remesh in Blender), then decimate |
| Baked lighting in the color texture | Shadows painted on the albedo | Retexture, or relight the texture by hand; ask for an unlit albedo |
| Wrong scale and orientation | Bounding box size and up axis | Scale to real dimensions; Y up; facing +Z |
| Origin off | Pivot not at the bottom centre | Move the origin |
| Back invented from one photo | Compare with the real object | More photos, or hide the back with the camera limits, and say so |
| Text or logos melted | Labels on the product are garbled | Rebuild labels as a texture from the real artwork |

The fixes are in `mesh-to-web-pipeline.md`.

## 4. Model it

1. Procedural in code: build simple geometry from primitives, extrusions of SVG paths, or data. No download; perfect for abstract heroes and data scenes.
2. Blender: model, UV, texture and export a GLB. Headless Blender runs scripts for batch work; see the pipeline reference.
3. A hosted scene builder: some tools build scenes in a hosted Blender from Python, with catalog assets only. Read the card; an uploaded mesh may not enter a hosted scene.
4. CAD conversion: export from CAD to glTF or an interchange format, then run the pipeline. CAD meshes are often very dense and need decimation and new UVs.

Asset conventions to follow for every route, from the Khronos guidelines:

1. Real scale: one unit is one metre.
2. Upright, facing forward, origin at the bottom centre.
3. Triangles only in the delivered file.
4. Instances for repeated parts.
5. Metallic-roughness PBR. Metal maps are pure black or pure white.
6. Occlusion, roughness and metalness packed in one texture.
7. Node or procedural materials baked to bitmaps.
8. Unique-texture UVs inside the 0 to 1 range.
9. glTF 2.0 binary (`.glb`), unused animation and data removed.

## 5. Worked example: a planter from three photos

| Step | Decision |
| --- | --- |
| Route | Generate from photos; no CAD exists |
| Photos | Front, side, back on a grey card, daylight, same distance |
| Upload gate | The user said yes to sending the three photos to the generation tool |
| Target | Web viewer, 30,000 to 50,000 triangles, from the use table |
| Quote | Shown with the balance; user said yes; one call; job id kept |
| Result | Dense mesh; drainage hole closed; baked shadow on the albedo |
| Repair | Remesh, decimate to 38,000 triangles, reopen the hole by hand, retexture with an unlit albedo |
| Record | Origin `generated`; tool and job id in the source field; note "back modeled from photo 3; drainage hole rebuilt by hand" |

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Generate first | Credits spent on a chair any library has | Source first |
| Look-alike product | A generated model that is not the client's product | Photos or CAD of the real product |
| One photo | The back is invented and wrong | Three views, or limit the camera and say so |
| Unlimited polygons | A 2 million triangle result | Polygon target with the live parameter name |
| Shipped as delivered | Dense, uneven mesh with baked shadows on the web | Repair through the pipeline |
| Silent upload | Client CAD sent to a tool without asking | Exposure gate |
| Expired link | The GLB link returns an error page | Download at once; check the file |
