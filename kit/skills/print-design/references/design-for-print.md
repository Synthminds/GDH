# Design for print

Read this at step 3, before you model. It holds the rules that decide whether an FDM part prints, fits and lasts. FDM means a nozzle lays plastic in layers.

Evidence. Every number here is a Default from a print-service design guide or a slicer maker's knowledge base, read on 2026-11-27. None is a gate: printers, nozzles and materials differ. A coupon measured on the user's printer replaces any number here; record it in `design/print-profile.md`.

## 1. Orientation first

Choose which face sits on the plate before you draw details. Orientation sets three things at once:

- Strength. A part is weakest across its layers. Put the load along the layers, not across them. A hook printed standing snaps at the bend; printed on its side it holds.
- Overhangs. Every downward face past the overhang limit needs support or a redesign.
- Finish. The top face and the walls look best. The plate face is flat and may show the plate texture. Supported faces are rough.

Rules:

- Give the part one large flat face for the plate.
- Default: put a 45 degree chamfer or a small radius on edges that touch the plate. A sharp edge flares out and lifts. Source: Hubs FDM design guide.
- Turn a feature that would need support so that it does not: a hole across the layers becomes a teardrop or a diamond at the top.

## 2. Walls and features

| Rule | Default | Source |
| --- | --- | --- |
| Thinnest wall | 0.8 mm; prefer at least two perimeters of the nozzle width | Hubs, thin walls |
| Thinnest free-standing wall | 1.2 mm | secondary design guide |
| Smallest feature (pin, rib, text stroke) | 2.0 mm | Hubs, thin walls |
| Space between holes, and from a hole to an edge | 1.5 to 2 times the wall thickness | Hubs, thin walls |
| Smallest round hole that prints round | 2 mm diameter | secondary design guide |

Detail finer than the nozzle width does not print. On a 0.4 mm nozzle, raised text below about 0.8 mm stroke width blurs. Use a 0.2 mm nozzle for fine detail, at a cost in time.

## 3. Overhangs and bridges

| Rule | Default | Source |
| --- | --- | --- |
| Overhang that prints without support | 45 degrees from vertical | Hubs FDM design guide |
| Bridge that prints clean | under 5 mm | Hubs FDM design guide |
| Bridge that prints at all | up to about 10 mm | secondary design guide |

`print_check.py` reports the share of surface past the overhang limit. Faces on the plate are not counted. A part that floats above z = 0 gets a warning.

Ways to remove support:

- Chamfer the underside of a ledge at 45 degrees instead of a flat shelf.
- Split the part at the overhang and join it after printing.
- Use a teardrop hole for a horizontal hole.
- Bridge a short gap instead of spanning a wide one.

## 4. Fits and clearances

A fit is the gap between two parts that touch. FDM parts print slightly larger outside and smaller inside than drawn.

| Fit | Default gap per side | Source |
| --- | --- | --- |
| Snap fit | 0.5 mm | Hubs, snap-fit joints |
| Moving parts (hinge, slider) | 0.3 to 0.6 mm | secondary design guide |
| Print-in-place moving parts | at least 0.5 mm | secondary design guide |
| Press fit and slip fit | no primary number found; print a coupon | none |

Dimensional accuracy on a desktop FDM printer is about plus or minus 0.5 percent, and no better than plus or minus 0.5 mm on small parts. Source: Hubs, dimensional accuracy.

Rules:

- Keep each clearance as a named value in the model.
- Print a coupon for every fit that matters: the pin and the hole alone, or one hinge knuckle. A coupon takes minutes; a failed full part takes hours.
- Vertical holes print undersized. Fix it in the slicer with hole compensation, or draw the hole larger and confirm with a coupon.
- For a screw, model a clearance hole and let the screw cut its thread, or model a hex pocket for a nut. Modeled fine threads print poorly at 0.4 mm.

## 5. Layer height and line width

| Rule | Default | Source |
| --- | --- | --- |
| Layer height | below 80 percent of the nozzle diameter, so 0.32 mm at most on a 0.4 mm nozzle; 70 to 80 percent is the usual top | Prusa knowledge base |
| Line width | about 110 percent of the nozzle diameter | Prusa knowledge base |

Finer layers smooth curved tops and take longer. Coarser layers are stronger between layers and faster.

## 6. Size and splitting

- Run the check with `--printer <id>`. It reports whether the part fits as drawn, fits after a rotation, or does not fit.
- Default: keep 2 mm clear at each edge of the plate.
- A part that does not fit is split. Put the split where a joint hides, and add a joint: dowel holes, a dovetail, a lap or a screw boss. Mark the parts with a small raised letter.
- A tall thin part wobbles and fails. Lay it down, or give it a brim in the slicer.

## 7. Materials

Choose by the job, then check the printer can run it. `printers.json` lists what each printer supports.

| Material | Choose it for | Watch for |
| --- | --- | --- |
| PLA | Most parts, decorative pieces, prototypes | Softens in a hot car or in sun; not for outdoor load |
| PETG | Outdoor parts, planters, wet places, some flex | Strings; sticks too hard to a smooth plate |
| ABS, ASA | Heat, outdoor sun (ASA) | Needs an enclosure; fumes; warps. Not on an open-frame printer |
| TPU | Flexible parts: feet, gaskets, grips | Slow; needs a larger nozzle on some printers |
| Fiber-filled (CF, GF) | Stiff, matte, dimensional parts | Needs a hardened nozzle; abrasive |

For a planter or anything that holds water or soil:

- Use PETG or ASA outdoors. PLA works indoors.
- Default: at least three perimeters and a solid bottom, so it does not seep.
- Add a drainage hole and a saucer seat in the model.
- A printed part is not food-safe by default. Say so when the user asks about food or drink contact.

## 8. Multi-color

- On a printer with a material system, split the model into one body per color and keep them in one 3MF.
- With no material system, a color change at a layer height gives two-color text or bands.
- Purge waste rises with each color change. Fewer, larger color regions print faster and waste less.

## Sources

- Hubs knowledge base: how to design parts for FDM printing; thin walls; snap-fit joints; dimensional accuracy. Read 2026-11-27.
- Prusa knowledge base: layers and perimeters; profiles for different nozzles. Read 2026-11-27.
- A robotics shop's published design guidelines, used only where marked secondary. Read 2026-11-27.
- OrcaSlicer wiki, precision settings (hole compensation). Read 2026-11-27.
