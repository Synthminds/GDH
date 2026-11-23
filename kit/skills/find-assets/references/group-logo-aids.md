# Group: logo aids

Catalog group `logo-aids`: vector tools, favicon tools and trademark search services. Read this file at step 6 of `find-assets` when a mark needs cleaning, exporting or a first conflict search.

How to read this file. An id is a catalog id. An id marked `*` has `verifiedOn` null. Every pick is a default from desk research. Evidence: UNTESTED in a build. License notes are DOCUMENTED on the catalog date, except where marked `*`.

The design of a mark belongs to `logo-identity`. This group holds tools, not marks. No source in any catalog group supplies a logo.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| Edit and export vectors from a script | `inkscape` | A vector editor with a command line for SVG, PNG and PDF export | The program license reaches its extensions, not your artwork |
| An open design tool with vector-native files | `penpot` | Open file format, self-host possible | The hosted service has its own terms |
| Shrink an SVG | `svgo`, `svgomg` | The usual optimizer; a visual version of it | Default settings can remove the view box or ids. Review the settings. |
| A full favicon and app icon set | `favicons`, `realfavicongenerator` | One master in, every platform size out | Review the generated manifest file |
| Vectorize your own sketch | `vtracer` | Color tracing of a raster drawing | The result needs manual cleanup. Never trace someone else's mark. |
| A first conflict search for a name or a mark | `uspto-trademark-search*`, `tmview*`, `wipo-brand-db*` | Public search services for one country, for many offices, and for international marks | A clear search is not legal clearance. Unread. |

## Decision rules

1. Never build a mark from a stock icon, a stock illustration or a traced third-party mark.
2. Never deliver a raster logo. The master is a vector file with clean paths.
3. A tool leaves no manifest entry. The file it produces is the project's own: record it with `--origin own`.
4. A mark from a generator is `--origin generated`. Record the tool and its output terms.
5. After a trace or a generation, check the paths by hand: point count, closed shapes, no stray points, no hidden layers.
6. Optimize a copy. Keep the master untouched under `design/assets/`.
7. After optimizing, open the file and compare it with the master at a large size and a small size.
8. Generate the favicon set from the simplest version of the mark, not from the full lockup.

## The knockout search

Run it before the user adopts a name or a mark. It finds obvious conflicts. It clears nothing.

1. GATE: an image search sends the unreleased mark to a third party. Ask before any upload.
2. Search the exact name.
3. Search phonetic variants and common misspellings.
4. Search inside the main classes of goods and services for the product.
5. Search the web and the app stores for the same name in the same field.
6. Save what you searched and what you found in the project.
7. Report in one of two forms: "no obvious conflict found", or "possible conflict: mark, owner, class".
8. Say in the report that this is not legal clearance. A trademark attorney clears a mark before launch.

Limits to state with every result:

- A register search does not cover unregistered marks in use.
- One office's register does not cover another country.
- Similarity is a legal judgment. You report what you saw. You do not judge it.

## Third-party marks

- A partner's logo comes from that partner's own brand page, or from the brand-mark set in the `icons` group.
- Use it unchanged, at the clear space and the minimum size its guidelines state.
- Record each mark in the manifest, with the guidelines URL in `note`.
- A connected `logo-search` tool returns existing marks. It designs nothing.

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Icon as mark | The logo is an icon from a public set | Return to `logo-identity` |
| Raster master | The only logo file is a PNG | Redraw as vector. Check the paths. |
| Trace and ship | A traced file with hundreds of points and uneven curves | Clean the paths by hand |
| Over-optimized | A mark that lost its view box, or changed shape after optimizing | Review the optimizer settings. Compare with the master. |
| Clearance claim | "The name is free" after a register search | State the limits. Send the user to an attorney. |
| Leaked mark | An unreleased logo uploaded to a web tool with no question | Exposure gate. Ask first, every time. |

## Worked choice

The outcomes below are illustrative. They show the reasoning, not verified facts about a source.

Need: turn an approved hand sketch of a monogram into a production mark, with a favicon set. A name search is wanted too.

- The sketch is the user's own. Tracing it is allowed.
- Trace it with the tracer. Clean the paths in the vector editor: fewer points, true curves, closed shapes.
- Save the master under `design/assets/`. Record it with `--origin own`.
- Optimize a copy. Compare it with the master at two sizes.
- Generate the favicon set from the simplified monogram. Record each generated file with `--origin own`.
- Knockout search: text search only. The user has not agreed to an image upload.
- Report: "no obvious conflict found in two registers for the exact name and three variants. This is not legal clearance."
