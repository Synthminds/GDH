# design-taste-frontend (tasteskill)

Catalog entry: [design-taste-frontend.json](../../catalogs/tools/design-taste-frontend.json). Source: https://github.com/Leonxlnx/taste-skill

This is an agent skill by Leonxlnx, not an MCP connector. License: MIT. Release read: 2.5.1. GDH offers it and does not copy it, because it declares a Stop hook and runs scripts.

Terms in this card. The gate is the skill's finish check, run by `scripts/gate.mjs`. To deal is to let a script pick a layout, a palette or a font pairing. The kit is the skill's `assets` folder. A page kind is one of `software`, `gaming`, `tech`, `product`, `service`, `place`.

## What it makes

- Websites only: company, product, shop, cafe, hotel, studio, SaaS, AI, developer-tool and game sites.
- A page built from written copy, a screen plan, a dealt hero layout, a dealt palette and a dealt Google Fonts pairing.
- Licensed stand-in photographs, real brand marks and interface icons as local files.
- A browser-checked finish: the build is not done until the gate passes or the fix rounds run out.
- It makes no app screen, no dashboard and no data visualization. Release 2.5.0 removed the earlier app-screen pipeline.

## Connection and auth

- No account and no API key. Check the skill list for `design-taste-frontend` before you route to it.
- ASK before any install. Name the Stop hook in the question.
- Pinned install line: see the `install` field in the catalog entry. It pins the skills CLI version and a commit.
- The pinned commit is the merge commit of release 2.5.1. Upstream has moved since and still carries the label 2.5.1.
- The pin uses skills CLI 1.8.1. The npm registry served 1.9.0 on the research date.
- Needs Node 22 or later and Chrome, Edge or Chromium. ffmpeg is optional.

## Cost model

- Free. No call spends credits. No quote tool exists and none is needed.
- Live photo search calls Wikimedia Commons, which is free.
- The Stop hook adds turns: it blocks the stop while a build fails the gate.

## Call order

1. Pick the stack. Empty folder: copy the kit and start from `assets/starter.html`. Existing project: build in its own stack with the kit in the public folder. Next.js: use a static export.
2. Read the brief. Write down the page kind, what is sold, the buyer, the one main action and the real material.
3. Arm the gate before any page exists: `node <skill>/scripts/gate.mjs --start index.html --kind <kind> --category "<what is sold>" --primary "<main action>"`.
4. Write all copy first. The skill has a copy layer: a fact sheet, a voice card and a register.
5. Plan the page as screens. Write one line for each section: its idea, its picture and its height (1 or 2 screens).
6. Deal. Do not choose by taste. `assets/layout/deal.mjs` deals the hero layout. `scripts/start.mjs deal --page <kind> --trade <trade>` deals the palette and the fonts.
7. Build. Run `node <skill>/scripts/gate.mjs index.html` until it prints `GATE: PASS`.
8. Stop after three fix rounds at most. The gate then prints `GATE: OPEN`. Report the open findings to the user.

## Key tools

| Script | Use it when |
|---|---|
| `scripts/gate.mjs` | You start and finish every build. It runs the checker at 1440 and 390, a 320 walk, and the copy lint. |
| `scripts/start.mjs deal` | You need a palette and a Google Fonts pairing for the page kind and trade. It emits the head links and the root tokens. |
| `assets/layout/deal.mjs` | You need the hero layout: split, centred, product, photo, place, collage, editorial, word, film, statement or triptych. |
| `scripts/consistency.mjs` | You need the browser checker alone: contrast, alignment, section rhythm, empty areas, placeholder text, reduced motion, tap size, collisions. |
| `scripts/copy-lint.mjs` | You count the tells of model-written copy. It needs no browser. |
| `scripts/photos.mjs` | You search, fetch and credit photographs (CC0, CC BY, CC BY-SA or public domain). |
| `scripts/icons.mjs` | You resolve real brand marks, file-type icons and interface icons to local SVG. |
| `scripts/effects.mjs`, `scripts/moments.mjs` | You deal a shader ground or a scroll or pointer moment. Tech, software and gaming pages only. |
| `scripts/shoot.mjs`, `scripts/perf.mjs` | You need screenshots or the performance budget. |

The gate ends on one line: `PASS`, `FAIL`, `OPEN`, `SETUP`, `ERROR` or `OFF`. The checker runs at 1440, 1024, 768 and 390.

## Inputs

- What is sold, who buys it and the one main action.
- Real material: logo, product screens, photographs, prices, address, opening hours.
- Without client photographs the skill uses licensed stand-ins. It lists each one in its report.
- The page kind and the trade. The dials of older releases (variance, motion intensity, density) do not exist in 2.5.1.

## Outputs and how to bring them into a project

- Static HTML and CSS: `index.html` plus the `assets/` kit.
- Or components in the project's own stack (React, Next.js, Vue, Svelte, Astro) with the kit served from `public/assets`.
- `.taste-skill/`: gate state, deal history, waivers, and `names.json` for a coined brand name. The history makes later pages differ.
- Optional `credits.html`. Photo credits go in one footer line.
- Write a provenance record in `design/assets/manifest.json` for each fetched photograph and icon.
- Default: read the license line of each stand-in photograph before the page ships. Research did not verify the photo library's terms.
- Copy the dealt palette and font pairing into `DESIGN.md` and `design/tokens.json` when the user keeps them.

## Handoffs

- To a design system: the dealt palette and pairing can seed a `DESIGN.md`.
- To an audit: after `GATE: PASS`, run a deeper accessibility and performance audit. See [impeccable.md](impeccable.md) and [vercel-web-design-guidelines.md](vercel-web-design-guidelines.md).
- To an asset library: fetched photographs are files in the repository. A library can take them in with their license lines.
- From a Claude Design canvas or a hosted builder: neither is an input format, and no "Send to" route ends here.
- Bring such a page into a local folder first (standalone HTML export or "Send to local coding agent"). Then arm the gate on it.
- The skill audits an existing page in a browser before it changes anything.
- From a direction plan: see [anthropic-frontend-design.md](anthropic-frontend-design.md) when the user wants free choice of palette and type.

## Limits and failure modes

What the skill enforces, in summary:
- No caption under any image or render. Credits go in one footer line.
- Every visual renders at all four widths. No empty ground.
- One section for each screen at 1440x900. The hero stands alone on the first screen.
- Equal left and right content edges.
- A fixed set of quiet hover and press interactions, one hero entrance, and one dealt moment for each page (two on a long page).
- No tilt, no carousels, no timed tabs, no fade-in on every section, no parallax on text, no scroll-jacking.
- Shaders, WebGL scenes and 3D only on software, tech and gaming pages, with four live WebGL contexts at most.
- No stock photograph passed off as the client's. No drawn look-alike of a real logo. No invented review, customer or figure.
- No copied code or signature effect from a reference site.
- Addresses carry street and district only. Contacts use `.example` domains.

Gotchas:
1. It declares a Stop hook in the skill frontmatter with a 600 s timeout. The hook blocks the stop while a build fails the gate.
2. The hook counts its blocks and stops at a limit, so it should not trap the agent. It still adds turns.
3. It bans violet and lavender anywhere in the page's own design. A brand whose color is purple needs a waiver or another tool.
4. Waivers live in `.taste-skill/waivers.json`. The file takes five waivers at most.
5. GDH precedence differs. The user and the project design system outrank the skill's bans. Record each brand-required exception as a waiver.
6. It deals layout, palette and type. Do not use it when the user has fixed a palette and a typeface, unless the brief overrides the deal.
7. "One section for each screen" conflicts with dense content briefs. Check the brief before you route here.
8. No browser on the host means the gate cannot run. It prints `GATE: ERROR`.
9. Never edit the kit's own files to clear a check. The skill forbids it.
10. The release pace is fast, and 2.5.0 was a full rebuild. Keep the commit pin. Read the changelog before you move it.
11. Companion skills by the same author exist in other repositories. Unverified: research saw them in a search result only.
12. The gate checks its own rules. It does not replace the GDH accessibility gate or the design critique.

## Best for

1. A landing page or company site from an empty folder for a real small business, with licensed stand-in photographs.
2. A SaaS or developer-tool marketing site with real product fragments, diagrams and one restrained shader moment.
3. An audit and rebuild of a page that "looks AI-made", with an objective browser gate as the stop condition.

## Wrong for

An application dashboard, an admin interface or a data visualization. It also does not fit a brand system with a fixed violet palette.

## Evidence

DOCUMENTED on 2026-11-23. Research read a shallow clone of the public repository (commit `6c0b5c7`). The pinned commit is `f6b7657`.

- DOCUMENTED: the run order, the script set, the house rules, the "never" list, the Stop hook and the waiver file.
- UNTESTED: the install line, every script, the gate, the Stop hook behavior and the photo search. The skill was not installed.
- Not confirmed: that the pinned commit and the commit read behave the same; the license terms of the photo library.
- Sources read: `skills/taste-skill/SKILL.md`; `CHANGELOG.md`; `references/photos.md`; the npm registry record of the skills CLI.
