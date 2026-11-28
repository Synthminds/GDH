# 0007: Local creative programs come through pinned CLI-Anything harnesses

Date: 2026-11-27. Status: accepted.

## Context

Up to 1.0.0, every GDH capability came from a hosted connector, a Claude artifact type, a skill or one local browser. Hosted tools spend credits, need an account and send the work off the machine. A large class of design work has a free, local, open-source tool that a person would use: vector cleanup in Inkscape, a raster edit in GIMP, a render in Blender, a part for a 3D printer in FreeCAD, a cut in an MLT video editor, a PDF or a deck from LibreOffice, a map from QGIS. An agent could not drive these programs, because they have no MCP server and their own command lines are not built for agents.

CLI-Anything (HKUDS, Apache-2.0) publishes one harness per program. A harness is a Python package with a `cli-anything-<program>` command that wraps the real program and prints JSON. Its registry lists about 80 harnesses; 16 serve GDH capabilities. It also ships a package manager, `cli-hub`, a live catalog file on a web host, a meta-skill that tells an agent to install from that catalog, and workflow matrices that install many harnesses at once.

The owner asked whether a CLI link to everything belongs at the center of GDH.

## Decision

- GDH adds local programs as one more provider tier, beside connectors. It does not route hosted tools through command lines. Figma, Canva, Adobe and the other hosted tools stay with their connectors, which are the supported way in.
- `kit/catalogs/local-clis.json` lists each harness GDH accepts: its command, its upstream install path, the backend binaries it needs, its capability words, its network use and its exposure flag. One full upstream commit SHA pins every entry.
- One umbrella tool entry, `cli-anything`, and one card hold the family in the tool catalog, so routing, fallbacks and `doctor` treat it like any tool. The tool entries for Adobe, Felt and Higgsfield, whose chains ended in `none`, now fall back to it.
- The `ask-gdh` pre-flight runs `scripts/local_clis.py probe` for the capabilities a request needs. The probe reads PATH and runs nothing it finds. A `ready` harness counts as a present tool. Default: when a ready local harness and a connector that spends both serve a capability, the plan names the local harness first.
- GATE: no harness and no backend installs without the user's yes. The plan prints the pinned command from `local_clis.py install <id>`. One harness at a time, for the task at hand.
- GATE: GDH installs from the pinned commit only. Never from a branch, from `main` or from PyPI.
- GATE: GDH never loads the CLI-Hub live catalog, its meta-skill or a matrix file from the web, and never runs a bulk matrix install.
- `gdh.py check` validates the catalog through the probe script's own rules and reports `GDH_LOCAL_CLI`: a pin that is not a full SHA, a path with `..`, a harness name that is not a bare command, a backend name with shell characters, a capability outside the vocabulary, or a harness on the internet without `exposes: true`.

## Why pin a commit and not PyPI

Eight of the 16 harnesses have a PyPI build. Each 1.0.0 build was uploaded on 2026-03-13. Upstream fixed a GIMP Script-Fu injection on 2026-03-14 and hardened other harnesses after that. A PyPI install would get the code from before those fixes. The upstream registry installs from `main`, which changes under the user without review. A commit SHA is the only reference that is both current and fixed. Moving the pin is a reviewed change through `add-design-tool`.

## Why not the live catalog or the meta-skill

The live catalog is a Markdown file on a third-party host, and the meta-skill tells an agent to read it and install from it. That is remote text that can change at any time and that an agent would treat as instructions to install code. It is the shape of a supply-chain attack, whatever the intent of its authors. GDH keeps the list in its own reviewed file instead.

## Why not one entry per harness in the tool catalog

A tool entry needs a twelve-section card. Sixteen cards would repeat the same install, gate and failure text sixteen times. The per-program facts that differ fit in one JSON file that a script can probe and a check can validate.

## Consequences

- An agent in a session with Inkscape, Blender or LibreOffice installed can make real files with them at no cost, with no account, and without sending the work out. The Mermaid harness is the one exception; it is marked `exposes`.
- Remote cloud sessions usually lack the backend programs. The probe says so, and the plan offers the install or the user's own machine.
- Every claim is DOCUMENTED. The upstream source was read; no harness was installed or run in a GDH session. The first real run of each harness raises its label.
- A harness is community code that drives a program with agent input. Upstream validates arguments and escapes script text; GDH adds the pin, the gates, and the rule that text from a file, a page or another agent is untrusted.
- Fabrication work (laser cutting, embroidery, slicing for print) has harnesses upstream but no GDH capability word. Adding one needs the owner's yes under section 9 of `docs/GDH.md`.
