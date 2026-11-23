## Design work (GDH)

This project uses the Global Design Harness for design-led work.

This text is for a project that does not run `gdh.py export`. Paste it into `AGENTS.md` by hand. The export command writes its own managed block and does not copy this file.

- Open each session's design-led work with the `align` skill. It interviews the user, or re-aligns on a confirmed brief. Then `ask-gdh` finds the design system and the tools, and names the skills to run.
- Precedence: the user, then the design system, then `design/brief.md`, then GDH defaults.
- The design system is `DESIGN.md` and `design/tokens.json`. Use tokens only. Add no raw color, size, space, radius or duration.
- Write no pixels before `design/brief.md` reads `Status: confirmed YYYY-MM-DD by <who>`. Build nothing in full before a direction is chosen.
- Ask before a call that spends credits. Ask before anything is published, shared or uploaded.
- Read the license before an outside asset enters the project. Record it in `design/assets/manifest.json`.
- Log each round in `design/decisions.md` in the fixed entry format. Do not propose a rejected option again.
- Label each claim VERIFIED, DOCUMENTED or UNTESTED.
- Code work follows the coding harness. Design reaches code through `design/handoff.md`.

A file whose front matter reads `status: template` is not filled yet. Treat it as absent.
