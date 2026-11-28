# Modeling routes

Read this at step 2. It picks how the part is modeled. The route follows the job of the part, not the tool at hand.

## 1. Choose the route

| The part | Route | Why |
| --- | --- | --- |
| Must fit, hold, clip, screw or move | Parametric | Every dimension stays a named number that a coupon result can change |
| Must look right; no mating faces | Generated or sculpted | Organic form is slow to script and fast to generate |
| A decorative form that must also mount, drain or hold | Hybrid | Generate the form, then join parametric features to it |
| A licensed model exists | Adapt | `find-assets` reads the license first; then repair and modify |

Ask one question when the job is unclear: "Does this part touch or hold anything with a size you can measure?" Yes means a parametric core.

## 2. Parametric

Write the part as a script with the key sizes at the top as named values: outer size, wall, clearance, hole diameters, fillet radius. A coupon result then changes one number, not the model.

Tools, in order of preference when present:

- build123d or CadQuery (Python, Apache-2.0). Solid modeling with fillets, shells and booleans, and export to STEP, STL and 3MF. They fit an agent best: the model is plain Python.
- OpenSCAD (GPL-2.0). Constructive solid geometry in its own language. Simple, stable and widely known. Fillets are hard.
- FreeCAD through the `cli-anything-freecad` harness, or `freecadcmd` with a Python script. Full CAD with sketches, constraints and assemblies. See the [cli-anything card](../../../references/tools/cli-anything.md).

Install nothing without the user's yes. Name the package and the environment first.

Rules:

- Model in millimetres. Put the part's base on z = 0 in its print orientation.
- Keep the clearance as a named value. Never bake a fit into a raw number.
- Keep STEP beside the mesh for a part that may go to CNC or to another CAD tool.
- Name each body for its job: `lid`, `base`, `hinge-pin`.

## 3. Generated

A generation tool makes a form from text or from photos. Photos of three sides give a far better result than one photo, which leaves the back invented. Text alone gives the loosest result.

Before the call:

1. GATE: read the balance, quote the call, get a yes, call once. Never repeat a call blind after a timeout; read the task list first.
2. GATE: uploading the user's photos or drawings is exposure. Ask first. Never upload a client's unreleased product.
3. Read the tool's output terms. Record who owns the model and any credit line it requires.

After the call, a generated mesh is a draft, not a print file:

1. Scale it to real size. Generated models come at an arbitrary scale.
2. Run the mesh check. Expect holes, thin shells and non-manifold edges.
3. Repair: close holes, remove inner faces, make it one shell. Use the 3MF harness `repair`, the FreeCAD mesh commands, or Blender.
4. Give it real thickness. A generated surface can be a skin with no wall. Solidify it, or make it solid and hollow it with a set wall.
5. Flatten a base face when the part must stand. Cut it with a plane at z = 0.
6. Decimate to the detail the nozzle can print. Detail below the nozzle width does not print.

Example card: [meshy](../../../references/tools/meshy.md).

### Files from a service the agent may not drive

Some design services have no API and forbid automated use in their terms. An AI hardware-design service that generates part CAD and exports STL, STEP or GLB is one example. With such a service:

1. The user works in the service and exports the file. The agent never signs in, scrapes or clicks through it.
2. The user puts the export in `design/print/<part>/source/`. Record the service, the export date and its output terms.
3. Prefer STEP over STL: STEP keeps exact geometry for edits and fits.
4. Treat the export as a draft. Run the after-steps above and the mesh check. A service's generated CAD can carry unsafe or unprintable choices.

## 4. Sculpted

Blender through the `cli-anything-blender` harness, or a Blender script, for forms the user describes in words and wants to steer step by step. Apply the same after-steps as a generated mesh.

## 5. Hybrid

1. Make the decorative form by the generated or sculpted route and repair it.
2. Model the functional features parametrically: a mount plate, screw bosses, a drainage hole, a cable channel, a lid seat.
3. Join them with booleans in FreeCAD, build123d or Blender. A boolean on a broken mesh fails; repair first.
4. Check the joined mesh. Booleans create the thin slivers and stray faces that the check reports.

## 6. Multi-color and multi-material

- Split the model into one body for each color or material. A 3MF keeps the bodies and their assignment together; STL does not.
- Put a color change at a layer for a cheap two-color part with no material system.
- Record in the profile which material system the printer has and how many slots.

## 7. Failure patterns

| Pattern | What goes wrong | Do this |
| --- | --- | --- |
| Pretty, unprintable | A generated form has no wall thickness and prints as a crumpled skin | Solidify, set the wall, check again |
| Baked fit | The clearance is typed into a dimension; the coupon shows it is wrong and the whole model must change | Keep clearance as a named value |
| Scale drift | A generated model prints at the wrong size | Scale to a measured dimension before the check |
| Detail lost | Fine surface detail below the nozzle width disappears | Exaggerate relief, or use a finer nozzle |
| Boolean on a broken mesh | The join fails or leaves holes | Repair each part first |
