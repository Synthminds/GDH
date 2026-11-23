# Publish the pack as a Claude Design System artifact

Use this to create or revise a Design System artifact from a brand pack. Other Claude artifact types (Design, Slides, Data) then read the brand from it.

Evidence: DOCUMENTED, UNTESTED. The layout and order below were read from the Design System type's own files on 2026-11-23. No artifact was written while this skill was made. Read the type's current skill file before each publish; it wins over this page.

GATE: this is an exposure gate. Publishing puts the brand, its fonts and its assets in a Claude artifact that can be shared. Do nothing in this protocol until the owner says yes to this pack, this artifact and this audience.

## Before the gate

1. The pack passes every gate in `SKILL.md`.
2. The README holds no TODO, no title, no provenance and no next steps.
3. Every asset has a license line that covers this use.
4. ASK: "New system or revise an existing one? Who may see it? Is this the default system?"
5. Show the owner the file list you will write. Wait for the yes.

## Find the tool and the type

1. Use a tool with the `design-system` capability. Check it is present in this session. Read its card.
2. List the artifact types the account can start from. Pick the type named "Design System".
3. Read the type's skill file and its format, craft and cover references through the tool.
4. To revise, get the artifact address from the owner or from a listing of their Design System artifacts.
5. Read the artifact's index and file list before any write.
6. An index with `"editing": "code"` means the system is synced from code. Do not write to it here. Go to [sync.md](sync.md).

## File layout under project/

| Path | What | From the pack |
| --- | --- | --- |
| `project/tokens.json` | The tokens, written whole | `tokens.json` |
| `project/README.md` | The brand book | `README.md` |
| `project/<Section>.md` | More brand-book sections, 24 at most | optional |
| `project/components/<Name>/README.md`, `preview.html` | Guidelines and a live preview | `components/` |
| `project/components/bundle.js`, `bundle.css`, `index.d.ts`, `lib/*.js` | Built components, optional | a build, with a yes |
| `project/fonts/<file>` | Font files named in `type.fonts[].file` | `fonts/` |
| `project/assets/<Group>/<file>` | Images, SVG, video, PDF, sent as uploads | `assets/` |
| `project/components/Cover/preview.html` | The cover | made in this protocol |
| `project/design-system.json` | The index | written last |

Do not write `project/tokens.css`, `project/manifest.json` or anything under `project/api/`. The page generates them. The pack's `tokens.css`, `DESIGN.md`, `SOURCE.md` and `PACK.md` stay local.

## Order for a new system

1. Create the artifact with one publish call: the type link, a title and no files. Never send the type link twice; a second call makes a second artifact.
2. Run `ds.py validate` on the exact `tokens.json` you will send. Zero errors.
3. Write `project/tokens.json` whole.
4. Write `project/README.md`.
5. Send fonts to `project/fonts/`. The paths must equal `type.fonts[].file`.
6. Send assets as uploads to `project/assets/<Group>/`. Give each asset a usage note. Read the upload limits live.
7. Write each component folder. Build two or three first, save, then build the rest.
8. Write the cover.
9. Write `project/design-system.json` last, once. It names the title, the namespace, the libraries, the groups and the asset groups.

Why the index is last: it lists what exists. Writing it first describes files that are not there yet.

## Order for a revision

1. Revise file by file. Never rebuild the whole system.
2. A person may have edited the page. Read the current file before you replace it.
3. Keep usage notes and README prose that a person wrote.
4. Move a file aside to `project/archived/` instead of deleting it. Follow the type's clean-up rules for the three record files it may delete.
5. Close with three lists: DELETED, MOVED ASIDE, SAFE TO DELETE.
6. A system migrated from the standalone site may show "Finish setting up". ASK before you run that clean-up.

## The cover

- File: `project/components/Cover/preview.html`. Width 960 px. Height 240 to 360 px. Keep the folder bare.
- Three parts: 3 to 5 large blocks in identity colors at full value; one pattern drawn from what the system says about itself; the name in the display face at bottom left with one tagline line.
- The blocks fill a quarter to a half of the cover.
- Take sides from spacing tokens and corners from radius tokens.
- Tests. Squint: the name reads first, then color, then pattern. Cover the name: blocks and pattern still identify the brand.
- Avoid a row of equal squares, a barcode of thin rules, confetti, words on blocks and any motion.
- Keep a four-line derivation comment at the top of the SVG.

## Checklist before you report

- [ ] The owner said yes to this publish.
- [ ] `tokens.json` validates; every theme is filled; contrast passes or failures are flagged.
- [ ] No DTCG map, no `var()`, no `color-mix()`, no named color in the tokens.
- [ ] Every font in `type.fonts` has a file at the stated path.
- [ ] Assets went up as uploads, each with a usage note and a license on record.
- [ ] Each component has a README and a preview whose first line holds `@dsCard`.
- [ ] The cover exists and uses tokens for its geometry.
- [ ] The index was written last and once.
- [ ] Nothing a person made was deleted.
- [ ] `SOURCE.md` records the artifact, the date and page-edited or code-synced. Keep the address out of public files.

## After publishing

1. Tell the owner the artifact is private until they share it.
2. Each design or deck keeps its own copy of the system from the day it was made. Reinstall to update one.
3. Read `project/tokens.json` back from the artifact. Run `ds.py validate` on that copy.
4. Confirm the `motion` family survived. Whether the page keeps it is UNTESTED; see [../references/tokens-format.md](../references/tokens-format.md#motion).
5. Repeat steps 3 and 4 after any token edit on the page. Restore a lost family from the pack.
6. Record the publish in `design/decisions.md` with the evidence label VERIFIED once the page shows the tokens.

## Sources

- Claude Design System artifact type: skill, format, craft and cover references, read 2026-11-23.
- Claude Academy tutorial on design systems: file package, reading order, sharing levels.
