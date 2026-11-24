# GDH moments

This file is generated from `kit.json`. Run `python3 scripts/gdh.py build` to change it.

A moment grants no authority. The kernel and the user rank higher.
In the Claude Code plugin, each skill name carries the prefix `gdh:`.

## Start

Start the skill before the work. Say so in one line.

- The first design-led request of a session arrives: a brand or logo, a mood board, the look of a site or app, a dashboard or chart design, an infographic, 3D, animation or motion graphics, or a design system. Start `align`.
- `align` has closed in this session and the design work needs a plan, or the user asks what GDH can do. Start `ask-gdh`.
- You are about to choose a look, a palette or a typeface and no confirmed brief exists, or the audience, job or brand changed. Start `align`.
- A confirmed brief must change, or another skill needs to read or check the brief. Start `design-brief`.
- You are about to build a full design and no direction is chosen. Start `mood-board`.
- You need an outside image, icon, font, component, model or template. Start `find-assets`.
- You are about to tell the user a design is done. Start `design-critique`.

## Offer

- You are about to tell the user a design is done. Offer `accessibility-gate`.
- The user gives feedback on a design. Offer `refine-round`.
- The user names a tool, connector or asset source that the catalog does not hold. Offer `add-design-tool`.
- A design is approved and code work starts. Offer `handoff-to-code`.

## How to offer

Ask one question with the host question tool. Put the recommended option first. Put Skip last. Offer once in a session. On a yes, `ask-gdh` loads a user-invoked GDH skill by reading its `SKILL.md`; the user may also type the command, such as `/gdh:refine-round`. With no question tool, write one closing line: `Option: <skill>: <what it does>.`

## Wired skills

These skills are not in this kit. Name one only with its install line.

- `impeccable`: design critique and polish for a screen. Install: `/plugin marketplace add pbakaus/impeccable`. Source: https://github.com/pbakaus/impeccable
- `dashboard-design-skill`: dashboard playbooks, layouts, component patterns and a screenshot QA pass. Install: `/plugin marketplace add abdiraimov-otabek/dashboard-design-skill`, then `/plugin install dashboard-design@dashboard-design-skill`. Source: https://github.com/abdiraimov-otabek/dashboard-design-skill
- `design-taste-frontend`: layout and visual taste for a landing page or a company site. Install: `npx skills@1.8.1 add Leonxlnx/taste-skill@f6b76575f949707b4e3c37cd86cb44b0b98643e8 --skill design-taste-frontend`. Source: https://github.com/Leonxlnx/taste-skill
- `deslop`: a scan for AI-writing tells in marketing copy and brand voice. Install: `/plugin marketplace add ProfSynapse/synaptic-labs-plugins`, then `/plugin install deslop@synaptic-labs`. Source: https://github.com/ProfSynapse/synaptic-labs-plugins
