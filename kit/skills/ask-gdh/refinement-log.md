# Refinement log: ask-gdh

Format: `YYYY-MM-DD | observation | change | files`

2026-11-23 | skill authored | first version | SKILL.md, references/
2026-11-23 | align opens every session before routing | named align as step zero; routing waits for its closing report; the pre-flight reads the brief status line; flows start from align | SKILL.md, references/preflight.md, references/routing.md, references/flows.md
2026-11-23 | review: the Skill tool cannot start the 20 user-invoked skills, so every flow stalled after its first such step | step 9 starts a user-invoked skill by reading its SKILL.md in the sibling folder, with the typed command as the last resort | SKILL.md, references/flows.md
2026-11-23 | review: flow 7 ran align twice and flows listed align as step 1 | align left every flow; each flow states the brief it needs; flow 7 step 3 is an in-session escalation | references/flows.md
2026-11-23 | review: "make the hero bolder" matched both the small-change exit and refine-round | feedback rule placed before the exit; worked example and failure pattern added | SKILL.md, references/routing.md
2026-11-23 | review: flows lived in two drifting copies and three extra H2 sections broke the skill shape | flows only in flows.md; routing table and flows as H3 under Procedure; GCH detail moved to the pre-flight | SKILL.md, references/preflight.md
2026-11-23 | review: new-brand flow asked for a direction twice | mood-board chooses the direction once; logo-identity chooses a mark inside it; mark-only requests skip mood-board | references/flows.md
2026-11-23 | review: the align gate used GATE for a precondition; lead-ins drifted | step 0 is a STOP; step 9 names ../<name>/SKILL.md; one Defaults lead-in; short description sentences; preflight accepts the ended-early status | SKILL.md, references/preflight.md
2026-11-26 | GDH 0.2.0 adds concept-forge, originality-gate and design-principles | Routed them in the table; shortened three lines to stay in the word budget | SKILL.md
2026-11-27 | GDH 1.1.0 adds local programs through CLI-Anything harnesses | Pre-flight step 7 probes local-clis.json with scripts/local_clis.py; a ready harness counts as present; a free local harness comes before a spending connector; install offers are gates; trimmed two lines to stay in the word budget | SKILL.md, references/preflight.md, scripts/local_clis.py
