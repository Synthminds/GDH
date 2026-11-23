# From a mesh to a web-ready file

Read this file at steps 10 and 11 of `three-d`. It gives the pipeline in a fixed order with command-level steps for open tools: inspect, normalize, clean, decimate or retopologize, UVs, PBR textures, resize, compress textures, compress geometry, validate, compare.

Evidence. The order (clean, resize textures, compress textures, compress geometry), the codec advice and the warning against mixing compressed outputs come from glTF-Transform guides found by search on 2026-11-23; the official page was not opened. The material and UV conventions come from the Khronos Real-time Asset Creation Guidelines, read 2026-11-23. The command syntax below is from memory of the glTF-Transform CLI, the Blender Python API, ImageMagick and gltfjsx. It is UNTESTED in this kit. Run each tool's `--help` first, work on copies, and confirm each flag before you script it. The tool licenses are in the asset catalog: glTF-Transform and gltfjsx are MIT, Blender's program is GPL (your output is yours).

## 0. Setup

| Tool | Job | Install, with the user's yes |
| --- | --- | --- |
| glTF-Transform CLI | Inspect, clean, simplify, resize, compress, validate | `npx @gltf-transform/cli <command>` (pin a version in a project) |
| KTX-Software | KTX2 texture encoding, called by glTF-Transform | The KTX-Software release for the platform; the CLI reports the binary it needs |
| Blender | Remesh, decimate, UVs, baking, scripted batch work | The Blender installer; headless with `blender -b -P script.py -- args` |
| ImageMagick | Channel packing and image checks | The platform package |
| gltfjsx | A React Three Fiber component from a GLB | `npx gltfjsx` |

Work in `design/assets/3d/<slug>/`. Keep `source/` untouched. Write each step's output to a new file, numbered: `01-normalized.glb`, `02-clean.glb`, and so on. Log each command and its result in the plan's pipeline log.

Below, `gt` stands for `npx @gltf-transform/cli`.

## 1. Inspect

```
gt inspect source/model.glb
```

Read and log:

| Look at | Against |
| --- | --- |
| Scene bounding box | Real dimensions in metres; up axis |
| Mesh count, primitives, vertices | The triangle budget |
| Materials | Metallic-roughness; no unsupported extensions |
| Textures: count, resolution, size, GPU size | The texture budget |
| Animations | Needed or not |
| Extensions used | Supported by the target viewer |

Open the file in a viewer too. Look at the wireframe, the normals and the textures. Note baked shadows, holes and flipped faces.

## 2. Normalize: scale, orientation, origin

1. Scale to real dimensions: one unit is one metre. Measure a known dimension and scale the whole model.
2. Up axis is +Y. The front faces +Z.
3. Origin at the bottom centre of the object.

```
gt center 01-in.glb 01-normalized.glb --pivot below
```

Scale and rotation are easiest in Blender: apply transforms before export (`Ctrl+A`, All Transforms), then export with `export_apply=True` in a script.

## 3. Clean

Remove duplicates, unused data and split vertices.

```
gt dedup 01-normalized.glb 02a.glb
gt prune 02a.glb 02b.glb
gt weld 02b.glb 02-clean.glb
```

Also, by hand or in Blender:

1. Delete hidden, internal and duplicate geometry.
2. Fix flipped normals. Recalculate outside.
3. Close holes that the real object does not have; keep the ones it has.
4. Remove animations the page does not use.
5. Merge meshes that share a material and never move apart, to cut draw calls.

## 4. Reduce: decimate or retopologize

Choose by the state of the mesh:

| Mesh state | Do |
| --- | --- |
| Clean topology, just too dense | Decimate (simplify) |
| Messy, uneven or non-manifold (typical of generated or scanned meshes) | Remesh first, then decimate |
| A product that will be edited later | Retopologize to quads by hand in Blender, then triangulate on export |

Simplify with glTF-Transform:

```
gt simplify 02-clean.glb 03-reduced.glb --ratio 0.5 --error 0.001
```

Lower `--ratio` keeps fewer triangles. A small `--error` protects the silhouette. Run, inspect the count, look at the silhouette, repeat with a new ratio.

Remesh and decimate in headless Blender. Save as `decimate.py`, run on a copy:

```python
import bpy, sys
args = sys.argv[sys.argv.index("--") + 1:]
src, dst, ratio, voxel = args[0], args[1], float(args[2]), float(args[3])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
for obj in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    if voxel > 0:                       # voxel remesh fixes messy topology; it discards UVs
        obj.data.remesh_voxel_size = voxel
        bpy.ops.object.voxel_remesh()
    mod = obj.modifiers.new(name="decimate", type='DECIMATE')
    mod.ratio = ratio
    bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.select_set(False)
bpy.ops.export_scene.gltf(filepath=dst, export_format='GLB', export_apply=True)
```

```
blender -b -P decimate.py -- 02-clean.glb 03-reduced.glb 0.3 0.004
```

A voxel remesh discards UVs and textures. After it, new UVs and a bake from the original are required (sections 5 and 6). Some generation tools offer a remesh call that keeps textures; it spends, so it passes the spend gate.

## 5. UVs

1. Unique textures need non-overlapping UVs inside the 0 to 1 range.
2. Tiling materials may use UVs outside the range.
3. Give the islands a margin so mipmaps do not bleed.

Smart UV project in headless Blender, added to a script after the reduction:

```python
import math
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
bpy.ops.object.mode_set(mode='OBJECT')
```

Check the UV layout by eye. Hand-unwrap seams on visible hero surfaces when automatic seams show.

## 6. PBR textures

Target the metallic-roughness workflow.

| Texture | Holds | Color space |
| --- | --- | --- |
| Base color | Albedo with no lighting or shadows baked in | sRGB |
| Metallic-roughness | Roughness in G, metalness in B | Linear |
| Occlusion | Ambient occlusion in R | Linear |
| Normal | Tangent-space normal | Linear |
| Emissive | Light-emitting areas only | sRGB |

Rules:

1. Metalness is pure black or pure white. Values in between are rare and usually wrong.
2. Pack occlusion, roughness and metalness into one texture (the ORM layout): R occlusion, G roughness, B metalness.
3. Bake fine detail from the dense mesh into the normal map of the reduced mesh, instead of keeping triangles.
4. Bake node or procedural materials to bitmaps before export.
5. Remove baked lighting from a generated albedo, or retexture.

Pack three grayscale maps into one ORM texture with ImageMagick:

```
magick occlusion.png roughness.png metalness.png -combine orm.png
```

Baking a normal map from the dense mesh to the reduced mesh, in Blender: put both meshes in one scene, select the dense mesh then the reduced one, set the render engine to Cycles, give the reduced mesh an image texture node, and bake Normal with "Selected to Active" and a small extrusion. Save the image. Repeat for ambient occlusion.

## 7. Resize textures

```
gt resize 06-textured.glb 07-resized.glb --width 1024 --height 1024
```

Default: 1024 px for phones, up to 2048 px for desktop, power-of-two sizes. Keep a 2048 copy when you serve two tiers.

## 8. Compress textures to KTX2

KTX2 stays compressed on the GPU, so it saves memory as well as download.

| Codec | Use for | Trade-off |
| --- | --- | --- |
| ETC1S | Base color and emissive, where size matters | Smallest; some quality loss |
| UASTC | Normal, occlusion, roughness and metalness; any texture where quality matters | Larger; high quality |

```
gt uastc 07-resized.glb 08a.glb --slots "{normalTexture,occlusionTexture,metallicRoughnessTexture}"
gt etc1s 08a.glb 08-ktx2.glb
```

When KTX2 is not possible, WebP textures cut download but not GPU memory:

```
gt webp 07-resized.glb 08-webp.glb
```

## 9. Compress geometry

| Codec | Strength | Note |
| --- | --- | --- |
| Meshopt | Fast decode | Default for most web scenes |
| Draco | Often the smallest file | Slower decode; needs a Draco decoder |

```
gt meshopt 08-ktx2.glb 09-final.glb
```

Do not mix compressed outputs from different tools on one file. Compress once, at the end.

The single-command route, useful for a first pass. Check every flag with `gt optimize --help`:

```
gt optimize source/model.glb quick.glb --compress meshopt --texture-compress ktx2 --texture-size 1024
```

The step-by-step route gives control over each stage and a log of what changed. Use it for delivery.

## 10. Validate

```
gt validate 09-final.glb
```

Fix every error. Read every warning. Then inspect the final file and log the numbers against the budget:

```
gt inspect 09-final.glb
```

## 11. Compare with the source

1. Render the source and the final side by side, same camera, same light, at the delivered size.
2. Look at the silhouette, the normals at grazing angles, texture detail, color.
3. Look for compression artifacts: banding in gradients, blocky normals, shifted vertices.
4. Fix by raising the quality of the stage that broke it, not by skipping compression.
5. Save the comparison image in `design/reviews/` and note the result in the plan.

## 12. Into the code

For React Three Fiber, generate a component and a transformed copy:

```
npx gltfjsx 09-final.glb --transform --types
```

The loader setup for compressed files is in `web-stack.md`.

## 13. Pipeline log format

```
Pipeline log: chair-oak
01 normalize: scaled x0.01 (cm to m), Y up, origin bottom centre
02 clean: dedup, prune, weld; 2 hidden meshes deleted
03 reduce: voxel 0.004 then decimate 0.3; 412,000 to 41,800 triangles
05 UVs: smart project 66 degrees, margin 0.02
06 textures: normal and AO baked from source; ORM packed
07 resize: 1024
08 KTX2: UASTC for normal and ORM, ETC1S for base color
09 meshopt; validate: 0 errors, 1 warning (unused UV set, removed)
Final: 1.6 MB, 41,800 triangles, 3 textures; compare: pass
```

## 14. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Raw export shipped | 4K textures and millions of triangles | The full pipeline |
| Compress twice | Artifacts and broken files from mixed tools | Compress once, at the end |
| Remesh without rebake | Textures lost after a voxel remesh | New UVs and a bake from the source |
| Baked shadows on albedo | Lighting looks doubled in the scene | Clean albedo; light in the scene |
| Gray metal | Metalness at 0.5 everywhere | Metalness black or white |
| Wrong color space | Normals in sRGB, colors washed out | Base color sRGB; data maps linear |
| Flags from memory | A command fails or does nothing | `--help` first; log what ran |
| Unvalidated file | Breaks in one viewer only | Validate and fix every error |
