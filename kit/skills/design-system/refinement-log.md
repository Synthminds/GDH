# Refinement log: design-system

Format: `YYYY-MM-DD | observation | change | files`

2026-11-23 | skill authored | first version | SKILL.md, protocols/, references/, scripts/ds.py
2026-11-23 | align now opens every session and owns the interview | the no-brief line sends the user to align instead of design-brief | SKILL.md
2026-11-23 | ds.py audit counted @font-face descriptors and the CSS-wide keyword inherit as raw font literals; the generated specimens of two packs failed their own audit | audit skips @font-face blocks and CSS-wide keywords; two regression tests | scripts/ds.py, tests/test_ds.py
2026-11-23 | review: step 8 wrote `design-md` output over the hand-written project DESIGN.md | step 8 targets DESIGN.md only when absent, a template or generated; otherwise DESIGN.generated.md and a hand merge; gate 5 separates generated and hand-written DESIGN.md | SKILL.md
2026-11-23 | review: tokens-format.md stated as fact that a motion family survives on the hosted page; the research says the page has no motion family and drops unread entries at the first edit | labelled it UNTESTED; motion stays in tokens.css and DESIGN.md; publish protocol reads the tokens back and checks the motion family after each page edit; open item: confirm with an owner-approved artifact write | references/tokens-format.md, protocols/publish-to-claude.md
2026-11-23 | review: --force and the design-md refusal were not in the command table; a pointer named design-brief | command rows name --force; refusal sentence; create-from-brief starts align; one tool-pick and Defaults lead-in; short description sentences | SKILL.md, protocols/create-from-brief.md
