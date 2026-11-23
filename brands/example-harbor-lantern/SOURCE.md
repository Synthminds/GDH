# Sources for Harbor Lantern

This file records where each value in the pack came from. A value with no source is not a brand fact.

Harbor Lantern is fictional. No brand book, client or owner exists behind it. Every value was chosen by the kit authors to show a complete pack.

| Part | Source | Date read | Status |
| --- | --- | --- | --- |
| Color tokens | Traced to objects of the subject's world (table below) | 2026-11-23 | Authored for the example; contrast measured with `ds.py contrast` |
| Type families | Traced to chart legends and tide tables (table below) | 2026-11-23 | Authored for the example; font files not shipped yet |
| Type styles | `ds.py init` starter scale | 2026-11-23 | Authored for the example |
| Spacing, radius, shadow, motion | `ds.py init` starter values, radius and shadow tightened | 2026-11-23 | Authored for the example |
| README brand book | Written for the example | 2026-11-23 | Authored for the example |
| Logo and other assets | None | 2026-11-23 | The pack ships no asset |

## Why each choice

Brand words: calm, exact, weathered. Subject: a shop on a tidal harbor for people who sail small boats.

| Choice | Traced to | Brand word |
| --- | --- | --- |
| `bg` chart white | The white of deep water on a nautical chart | calm |
| `surface` shallows tint | The pale blue that a chart gives to shallow water | exact: raised ground reads like a warning of shallows |
| `text` wet slate | Slate harbor steps after rain | weathered |
| `accent` starboard green | The green navigation light: the safe side | exact: green means go |
| `danger` port red | The red navigation light | exact: red means stop |
| `lamp` lantern amber | The harbor lantern of the brand name; fills only | calm: one warm point in a cool page |
| Dark theme | Night water under the same lights | calm |
| IBM Plex Sans Condensed for headings | The narrow capitals and figures of chart legends | exact |
| IBM Plex Sans for text | A grotesque with open shapes that holds up at small sizes outdoors | weathered, not nostalgic |
| IBM Plex Mono for figures | Tide tables align their columns | exact |
| Tight radius, matte surfaces | Printed charts and enamel signs have no gloss | weathered |

Swap test: a generic bank or software page would not take green and red from navigation lights, a chart-white ground or condensed legend type. Each choice above fails to transfer without a reason.

Rejected: a cream ground with one orange accent. It was the first version of this pack. It is a common template, and nothing in the subject asked for it.

Font files: copied on 2026-11-23 from IBM's own npm packages of the Plex release (repository https://github.com/IBM/plex): `@ibm/plex-sans` 2.0.0, `@ibm/plex-sans-condensed` 3.0.0 and `@ibm/plex-mono` 2.5.0. Each file is the package's `fonts/split/woff2/<name>-Latin1.woff2`. `fonts/OFL.txt` is the package `LICENSE.txt`, which is the same in all three packages: SIL Open Font License 1.1, copyright IBM Corp., Reserved Font Name "Plex". The license allows use, bundling and redistribution with the license; a modified version may not use the reserved name. Evidence: VERIFIED on 2026-11-23. Each file starts with the WOFF2 signature. A headless Chrome render of `specimen.html` and `sample.html` reported every used face as loaded through `document.fonts`.

| File | sha256 |
| --- | --- |
| `fonts/IBMPlexSans-Regular-Latin1.woff2` | `bdb53f2af84b15e0a742428f5e199dacc3e6fd60776f0aebd9f700e2c97c960f` |
| `fonts/IBMPlexSans-Medium-Latin1.woff2` | `668a0d9eabbfac0925f431988f56222b8b989ad66a0a78e91bc5889f73fe274a` |
| `fonts/IBMPlexSans-Bold-Latin1.woff2` | `098277f28ccff8b6128068edc357d59cb9cb3d4e3d15d77e7757c85ba1162c73` |
| `fonts/IBMPlexSansCondensed-SemiBold-Latin1.woff2` | `f21ec2af242f62f72790e9a9ba16ef3f56e65a3d85b91195b47e8ea6865fce1b` |
| `fonts/IBMPlexSansCondensed-Bold-Latin1.woff2` | `9009342802429edfa891d1d2079dbbc7268a21f6adf6ed2a94fcdcce7cd1a37f` |
| `fonts/IBMPlexMono-Regular-Latin1.woff2` | `e8993d946649b9d01abb1ed06d574b19d8ea3e66b5c3948602db335c44c18e56` |

## INFERRED values

In a real pack, this list holds every value that was estimated or sampled by eye, and the owner confirms each one.

- None. This pack has no outside source to infer from.

## Confirmed by the owner

- Not applicable. A fictional brand has no owner to confirm it.

## Checks run on 2026-11-23

- `ds.py validate tokens.json`: 0 errors, 0 warnings.
- `ds.py contrast tokens.json`: 11 pairs, 22 checks in two themes, 0 failed.
- `tells.py specimen.html sample.html` with the pack tokens and `DESIGN.md`: 0 findings.
- `tokens.css`, `DESIGN.md` and `specimen.html` were generated from `tokens.json`. `sample.html` was written by hand from `tokens.css`.
