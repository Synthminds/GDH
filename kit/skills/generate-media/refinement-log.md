# Refinement log: generate-media

Format: `YYYY-MM-DD | observation | change | files`

2026-11-23 | skill authored by the integrator; the builder output for this skill was absent | first version | SKILL.md, references/
2026-11-23 | the first version was thin: two references; the spend gate, consistency, rights and per-medium guidance were short | rewrote to full depth; eight references; full spend gate with test-before-batch, ledger and retry rules; prompt log tied to the manifest record | SKILL.md, references/
2026-11-23 | review: the consent record used its own header and fields, so readers of the last entry's stage found none | consent is now a decision entry in the fixed format with scope consent, and revocation is a new entry; tool pick points to kernel rule 8; Defaults lead-in shortened | SKILL.md, references/rights-consent-exposure.md
2026-11-23 | review: 'media brief' overloaded the term brief; consent used GATE | renamed to prompt sheet (references/prompt-sheet.md, prompt-sheet.md in the project); consent step is a STOP; one Defaults lead-in; short description sentences | SKILL.md, references/*.md
