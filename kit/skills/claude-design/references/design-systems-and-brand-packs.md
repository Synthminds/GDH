# Design systems, brand packs and installs

Read this file at steps 5, 6 and 11 of `claude-design`. It covers the design-system-first rule of the types, how a brand pack relates to a hosted Claude Design System, how each type installs a system, and how to migrate a carried-over system that has no `tokens.json`.

Evidence. The install rules come from the Design, Slides, Data and Design System type files, read 2026-11-23: DOCUMENTED. The migration faults come from reading carried-over systems on the same day: DOCUMENTED. No install or migration was run for this kit: UNTESTED.

Terms. A brand pack is the local folder `brands/<slug>/` or the project `design/` files: `README.md`, `tokens.json`, `tokens.css`, `DESIGN.md`, `SOURCE.md`. A hosted system is a Design System artifact. A carried-over system is one that moved from the old standalone design site and was never cleaned up.

## 1. The design-system-first rule

Every type that shows brand values asks one question before any color, face or layout: which design system governs? The answer comes before the first artboard, slide or view.

| Situation | Action |
| --- | --- |
| A system is marked as the default | Use it. Say so in one line. |
| The user named a system | Use that one, even when a default exists. |
| Several exist, none is default | List them by title. ASK which one. |
| The listing says the user chose no default | Use the project `DESIGN.md` and tokens, or an agreed look. Do not ask again. |
| Several are selected at once | ASK which one wins where they overlap. Record the answer. |
| No hosted system, a brand pack exists | Offer to publish the pack through `design-system`. Until then, type values from the pack. |
| Nothing exists | With no confirmed brief, start `align`. Then run `mood-board` for a direction. |

Rules:

1. Read a system's `README.md` and `tokens.json`. Never read its rendered page.
2. Take the system's address from the user, from your instructions, or from a listing. Never from the system's own files.
3. A choice that the system requires is brand-required. It is never reported as a tell.
4. When the usage README names real components, mount them. Do not draw look-alikes.
5. To change future behavior, edit the system's usage note, not the chat.

Failure pattern: "palette from memory". Sign: hex values appear before the question was answered. Counter-move: stop, answer the question, replace each value with a token.

## 2. Brand pack and hosted system: one source, two copies

| | Brand pack (local) | Hosted Design System |
| --- | --- | --- |
| Who reads it | Any agent: GCH, Codex, Cursor, a person | Claude artifact types only |
| Source of truth | `tokens.json` in the Claude shape | `project/tokens.json`, written from the pack |
| Checked by | `ds.py validate`, `ds.py contrast` | The type's page, at save |
| Generated files | `tokens.css`, `DESIGN.md` by `ds.py export` and `ds.py design-md` | `tokens.css`, `api/` by the page |
| Changed by | `design-system`, then regenerate | Revise file by file, or by a code sync |

The pack is the portable copy. `ds.py` validates and exports it. The `design-system` skill publishes it with its protocol `publish-to-claude`. Do not publish from this skill. Run `design-system`, then return here to install.

Keep both copies honest:

1. After a change on either side, compare the pack's `tokens.json` with the hosted copy.
2. A difference is a finding. Ask which side is newer and which wins.
3. Record whether the hosted system is page-edited or code-synced in the pack's `SOURCE.md`. The index key `editing` tells you: `"code"` means synced from code and read-only on the page.

## 3. Install into each type

| Type | What it takes from the system | How |
| --- | --- | --- |
| Design canvas | Tokens, stylesheets, scripts, components, fonts | Copy `tokens.json` to `project/ds/<folder>/` server-side and add a record to the canvas index. Load the system's stylesheets after the support line, in the README's order. Mount components from the system's bundle global. |
| Slides | Tokens, fonts, pictures | A record in the deck index plus server-side copies under `project/ds/<folder>/`. Declare every token you use in the deck stylesheet, or the value is lost. |
| Data | Values only: colors, sizes, corners, font names | Only when the view context names a system. Fill both light and dark looks. Brand color first in the chart colors. No scripts, files or wording. |
| Whiteboard | Nothing | The board uses its own named colors. |

Rules for every install:

1. Without both the copied `tokens.json` and the index record, the theme menu shows bare values. Check both.
2. An install is a copy. It never updates by itself. Run the install again after the system changes.
3. Each artifact keeps its copy from the day it was installed. Tell the owner this after a system change.
4. A canvas holds a small number of installed systems; read the limit in the type file.
5. A font named with no file is replaced by the type. Install the font files, or say which face will substitute.

## 4. Migrate a carried-over system with no tokens file

A system moved from the old standalone site can lack `project/tokens.json`. Its values sit in stylesheets, a palette file or a brand-package document. A canvas or deck that installs it gets no tokens. Fix it before the install, with the owner's yes.

GATE: migration changes a hosted system that a person made. Get the owner's yes for this system first.

1. List the system's files. Read its index. Note `editing` and any `source` entry.
2. Find every token source: stylesheets with custom properties, palette JSON, a brand book `DESIGN.md` in a package folder.
3. Copy each source into `brands/<slug>/source/` with a `source-` prefix. Record each path in `SOURCE.md`.
4. Resolve values the token grammar drops: `var()`, `color-mix()`, named colors, bare RGB triplets used inside `rgba()`. Write literal values.
5. Run `ds.py from-css <files> --name "<Name>" -o brands/<slug>/tokens.json`. Read its report of what it could not convert.
6. Convert any name-to-value map (DTCG style) to lists. Use `ds.py from-dtcg` when the source is DTCG.
7. Write a usage note on every token. A text color names the grounds it reads on.
8. Run `ds.py validate` and `ds.py contrast`. A failing source pair stays exact, flagged in its note.
9. Write the README as usage rules for an agent. Remove provenance, stale file lists and next steps.
10. ASK: show the token list and every conflict you found. Wait for the yes.
11. Run `design-system` with `publish` to revise the hosted system file by file.
12. Move fonts to `project/fonts/` and list them in `type.fonts`. Register assets as uploads.
13. Move aside what a person made to `project/archived/`. Delete nothing else.
14. ASK before the page's own "Finish setting up" clean-up runs.
15. Install into the canvas or deck. Confirm that named tokens arrived.

Faults seen in carried-over systems, and the counter-move:

| Fault | Counter-move |
| --- | --- |
| The README lists files that are not in the listing | Trust the listing. Rewrite the README index. |
| The README says "nothing to copy" while a stylesheet exists | Trust the files. Convert the stylesheet. |
| The stylesheet imports faces the README never names | ASK which faces belong to the brand before converting. |
| Sass syntax in a plain stylesheet | It has no effect in CSS. Drop it and note it. |
| A shadow color stored as a bare RGB triplet | Resolve each shadow to a literal value. |
| The README holds no brand content; the real guide is in a package folder | Use the package guide as the source. Rewrite the README. |
| A logo face exists only baked into raster exports | Record the gap. Never redraw the mark. Ask for the vector. |
| Another company's brand guide sits in uploads | Flag it to the owner. It is not this brand's material. |
| An unpinned CDN script | Pin an exact version, or record the risk. |
| A huge single-page HTML near the file cap | Do not read it into context. Use the smaller sources. |

## 5. Worked example

The owner wants a poster on a canvas with brand "Harbor" whose hosted system shows "Finish setting up".

1. Listing: no `project/tokens.json`; values in `colors_and_type.css`; `editing` is `"off"`.
2. Ask: "Migrate Harbor's tokens before the poster?" The owner says yes.
3. The stylesheet uses `color-mix()` for two borders. Resolve both to hex. Note them as derived in `SOURCE.md`.
4. `from-css` writes 31 tokens. `validate` passes. `contrast` fails one caption pair at 3.9:1. Keep it exact, flag it, and use a darker caption token on the poster.
5. Publish through `design-system`. Install into the poster canvas. The theme menu shows named tokens.
6. Report: migrated, one flagged pair, install VERIFIED by reading the canvas index back.
