# Group: fonts

Catalog group `fonts`: typeface libraries, single families and self-host packages. Read this file at step 6 of `find-assets` when the need is a font file or a font package.

How to read this file. An id is a catalog id. An id marked `*` has `verifiedOn` null: read its license before use. Every pick is a default from desk research. Evidence: UNTESTED in a build. License notes are DOCUMENTED on the catalog date, except where marked `*`.

The choice of typeface, the pairing and the scale belong to `typography`. This file covers where a chosen kind of face can come from and what its license asks.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| The widest open catalog | `google-fonts` | Many families, many variable | Each family has its own license. Read the family's license file. |
| Self-hosting an open family | `fontsource` | One package for each family, with subsets and variable axes | Pin the version. The font's own license travels in the package. |
| A dependable interface text face | `ibm-plex`; the families in the shortlist below; `inter`, `geist` only with a reason | Open font license, well drawn, wide weights | `inter` and `geist` are on the overused list below. They carry no brand on their own. |
| Monospace | `ibm-plex`; the monospace row of the shortlist; `jetbrains-mono`, `geist` for code only | Open font license | A monospace face as brand voice is on the overused list. |
| A distinctive free display face | The display rows of the shortlist; `league-moveable-type`, `fontshare*`, `velvetyne*` | Faces that fewer products use | `fontshare*`: files may not pass to a third party. `velvetyne*`: limited language coverage. |
| Curated or contemporary free faces | `open-foundry*`, `uncut-wtf*` | Unusual choices | Terms unknown for each font: blocked until read |
| A professional subscription library | `adobe-fonts*` | Large catalog through a connected `fonts` tool | Licensed, not owned. No self-hosting. The client needs its own subscription. |
| A privacy-first font CDN | `bunny-fonts*` | Drop-in replacement for a font CDN | Still a third-party host. Self-hosting is the default. |
| No download at all | `modern-font-stacks` (group `color-type-tools`) | System font stacks by classification | Rendering differs by operating system |

## Shortlist by classification

`typography` names a classification (its choosing-a-face reference, section 3). This table turns that classification into named candidates. Start the shortlist here, then add or swap faces for a reason from the brief.

Evidence: UNTESTED. The faces, licenses, coverage, weights, italics and figure notes come from memory, not from a license page read in this build. `verifiedOn` is `not read` for every row. Before a face enters the project, read its license file in the family's repository or on its catalog page, check coverage and figures in the specimen, and record the date. "Check" means the figure set is not known; test `font-variant-numeric: tabular-nums` in the specimen.

Fetch route for every row: catalog id `google-fonts` or `fontsource`, except where the row names `league-moveable-type`. Each row is a Default.

| Classification | Face | License | Coverage | Weights | Italic | Tabular figures | verifiedOn |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Old-style and humanist serif | EB Garamond | OFL-1.1 | Latin, Greek, Cyrillic | 400 to 800, variable | Yes | Yes | not read |
| Old-style and humanist serif | Alegreya | OFL-1.1 | Latin, Greek, Cyrillic, Vietnamese | 400 to 900 | Yes | Yes | not read |
| Old-style and humanist serif | Literata | OFL-1.1 | Latin, Greek, Cyrillic, Vietnamese | 200 to 900, variable, optical size | Yes | Yes | not read |
| Old-style and humanist serif | Crimson Pro | OFL-1.1 | Latin, Vietnamese | 200 to 900, variable | Yes | Check | not read |
| Transitional serif | Source Serif 4 | OFL-1.1 | Latin, Greek, Cyrillic, Vietnamese | 200 to 900, variable, optical size | Yes | Yes | not read |
| Transitional serif | Newsreader | OFL-1.1 | Latin, Vietnamese | 200 to 800, variable, optical size | Yes | Check | not read |
| Transitional serif | Libre Baskerville | OFL-1.1 | Latin | 400, 700 | 400 only | Check | not read |
| Transitional serif | PT Serif | OFL-1.1 | Latin, Cyrillic | 400, 700 | Yes | Check | not read |
| High-contrast serif (didone) | Bodoni Moda | OFL-1.1 | Latin | 400 to 900, variable, optical size | Yes | Check | not read |
| High-contrast serif (didone) | Prata | OFL-1.1 | Latin, Cyrillic, Vietnamese | 400 | No | Check | not read |
| High-contrast serif (didone) | Gloock | OFL-1.1 | Latin, Cyrillic | 400 | No | Check | not read |
| Slab serif | Zilla Slab | OFL-1.1 | Latin | 300 to 700 | Yes | Check | not read |
| Slab serif | Bitter | OFL-1.1 | Latin, Cyrillic, Vietnamese | 100 to 900, variable | Yes | Check | not read |
| Slab serif | Roboto Slab | Apache-2.0 | Latin, Greek, Cyrillic, Vietnamese | 100 to 900, variable | No | Yes | not read |
| Humanist sans | Source Sans 3 | OFL-1.1 | Latin, Greek, Cyrillic, Vietnamese | 200 to 900, variable | Yes | Yes | not read |
| Humanist sans | Fira Sans | OFL-1.1 | Latin, Greek, Cyrillic, Vietnamese | 100 to 900 | Yes | Yes | not read |
| Humanist sans | Alegreya Sans | OFL-1.1 | Latin, Greek, Cyrillic, Vietnamese | 100 to 900 | Yes | Yes | not read |
| Humanist sans | Atkinson Hyperlegible | OFL-1.1 | Latin | 400, 700 | Yes | Check | not read |
| Grotesque and neo-grotesque sans | Public Sans | OFL-1.1 | Latin, Vietnamese | 100 to 900, variable | Yes | Yes | not read |
| Grotesque and neo-grotesque sans | Archivo | OFL-1.1 | Latin, Vietnamese | 100 to 900, variable, width axis | Yes | Check | not read |
| Grotesque and neo-grotesque sans | Schibsted Grotesk | OFL-1.1 | Latin | 400 to 900, variable | Yes | Check | not read |
| Grotesque and neo-grotesque sans | Hanken Grotesk | OFL-1.1 | Latin | 100 to 900, variable | Yes | Check | not read |
| Geometric sans | Jost | OFL-1.1 | Latin, Cyrillic | 100 to 900, variable | Yes | Check | not read |
| Geometric sans | Red Hat Display | OFL-1.1 | Latin | 300 to 900, variable | Yes | Check | not read |
| Geometric sans | League Spartan (`league-moveable-type`) | OFL-1.1 | Latin | 100 to 900, variable | No | Check | not read |
| Geometric sans | Lexend | OFL-1.1 | Latin, Vietnamese | 100 to 900, variable | No | Check | not read |
| Monospace | IBM Plex Mono (`ibm-plex`) | OFL-1.1, reserved font name | Latin, Cyrillic | 100 to 700 | Yes | Fixed width | 2026-11-23 for the family license |
| Monospace | Source Code Pro | OFL-1.1 | Latin, Greek, Cyrillic, Vietnamese | 200 to 900, variable | Yes | Fixed width | not read |
| Monospace | Fira Mono | OFL-1.1 | Latin, Greek, Cyrillic | 400, 500, 700 | No | Fixed width | not read |
| Monospace | Martian Mono | OFL-1.1 | Latin, Cyrillic | 100 to 800, variable, width axis | No | Fixed width | not read |
| Script and display | League Gothic (`league-moveable-type`) | OFL-1.1 | Latin | 400, variable width | No | Check | not read |
| Script and display | Big Shoulders Display | OFL-1.1 | Latin, Vietnamese | 100 to 900, variable | No | Check | not read |
| Script and display | Caveat | OFL-1.1 | Latin, Cyrillic | 400 to 700, variable | No | Check | not read |

Rules for the shortlist:

1. Take three candidates from the rows for the classification. Reject by coverage, license, weights and figures, in that order.
2. A row is a starting point, not a pick. `typography` tests each candidate with real copy before it commits.
3. When a row fails the brief, search the catalog and the web by the same filters. Record why the row failed.
4. After you read a license page, keep the date in the manifest entry. Report a wrong row so the table can be corrected.

## Overused in generated work

These faces appear in a large share of generated interfaces. Default: do not pick one of them for a brand voice or a headline unless the brief gives a written reason. Evidence: UNTESTED. The list comes from tell lists in the research and from observation, not from a measured count.

| Face | Typical generated use |
| --- | --- |
| Inter | Every text role, by default |
| Geist | Interface text and headlines |
| Space Grotesk | Headlines over an interface sans |
| DM Sans | Interface text |
| Manrope | Interface text and headlines |
| Plus Jakarta Sans | Interface text and headlines |
| Poppins | Headlines and buttons |
| Instrument Serif | An italic serif headline over a sans |
| Fraunces | A soft serif headline |
| Playfair Display | A high-contrast serif headline |
| JetBrains Mono | Monospace used as brand voice, labels and headings |

Rules for the list:

1. Precedence holds. When the user or the design system names one of these faces, use it and report it as `brand-required`. It is not a finding.
2. Otherwise, a face from the list needs one sentence in `design/decisions.md` that cites the brief: a brand word, a use context or a constraint. "Clean" and "modern" are not reasons.
3. A built-in face default of an artifact type or a tool is not a reason. Replace it with a face chosen for the brief.
4. A monospace face from the list stays valid for code, data and measurement.
5. The tell scan in `design-critique` checks font families. Inter is in its first-wave set (`TELL_DEFAULT_FONT_ONLY`). The other proportional faces here are its second-wave set of 2026-11-23 (`TELL_SECOND_WAVE_FONT`). A monospace face on labels is `TELL_MONO_LABELS`. Keep the scan and this list the same; report a difference as a kit defect.

## Decision rules

1. `typography` decides the face. Come here with a classification and a role, not with "a nice font".
2. Default: self-host. Use a package, or font files in the project with their license file.
3. Record every family. A package gets one `--package` entry. Font files get one entry for each file.
4. Keep the license file beside the font files. An open font license asks for it.
5. Check language coverage against the content languages in the brief before you commit to a face.
6. A changed build of an open font can be limited by a reserved font name. Read the license before you subset by hand or rename.
7. Use the variable package when the design uses three weights or more of one family.
8. A font whose license forbids redistribution never enters a public repository. The client downloads its own copy.
9. A subscription font is delivered by its vendor. That is a hotlink exception with a written reason in the manifest.
10. A font CDN left in production is a hotlink. `check --scan` reports it.
11. Load at most the weights and styles the design uses.

Default (general reading, UNTESTED against any one family): subsetting counts as a change to the font. A family with a reserved font name may limit what a changed build can be called. Package builds from the self-host source already handle this for their own subsets.

## License traps

- `google-fonts`: most families use the open font license, some use other licenses. The catalog is not one license.
- `fontshare*`: the catalog note says free for commercial use and self-hosting on your own sites, no transfer of files, changes need consent. Unread. An agency cannot hand the files to a client under that note.
- `adobe-fonts*`: the catalog note says web use only through the vendor's embed, and a client site needs the client's subscription. Unread.
- `velvetyne*`: the foundry asks for a credit. Give it.
- `ibm-plex`: a reserved font name applies.
- No open font may be sold on its own.
- A font inside a component or a template has its own license. Find it.

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Default face | The most common interface face in every role, chosen with no reason | Go back to `typography`. A face needs a reason from the brief. |
| Orphan font | A font file with no license file and no manifest entry | Find the family and its license. Record it or replace it. |
| CDN left in | A remote font stylesheet in production | Self-host, or write the exception |
| Foundry font in public | A no-redistribution font committed to a public repository | Remove it from history with the user. The client downloads its own copy. |
| Weight pile | Eight font files loaded, three used | Load what the scale uses |
| Missing glyphs | Fallback letters inside words in a second language | Check coverage first. Pick a family that covers the languages. |
| Activation by habit | A subscription font activated with no question | An activation is a spend and exposure call. Ask first. |

## Worked choice

The outcomes below are illustrative. They show the reasoning, not verified facts about a source.

`typography` asks for: a humanist serif for long reading, a quiet sans for interface text, both open, Latin and Greek coverage. Brand words: warm, editorial, exact. Ships in a client product in a public repository.

- Public repository: redistribution matters. A no-transfer foundry license is out before the search starts.
- Catalog: `A search <catalog> --group fonts --query "serif" --commercial --verified`.
- Candidates: a superfamily with serif and sans under the open font license; two families from the widest open catalog.
- Coverage: the superfamily covers Greek. One of the two others does not: rejected.
- License: read the license file in the family's repository. A reserved font name applies. No renaming is planned. Verdict `clear with duties: keep the license file`.
- Fetch: the variable packages from the self-host source, pinned.
- Record: one package entry for each family. Duty in `note`: "Reserved font name. Do not rename a changed build."
