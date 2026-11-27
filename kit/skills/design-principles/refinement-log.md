# Refinement log: design-principles

Format: `YYYY-MM-DD | observation | change | files`

2026-11-26 | skill scaffolded | new skill | SKILL.md
2026-11-26 | the twelve design books had no shared, queryable canon | wrote 325 principles with tests, gates and sources, one readable list per book, the coverage audit, and a router body that queries the canon by discipline and stage | SKILL.md, scripts/principles.py, ../../canon/principles.json, ../../canon/principles/, ../../../docs/PRINCIPLES-COVERAGE.md, ../../../tests/test_principles.py
2026-11-27 | review: four gates were judgment calls; P-DT-03 sat near a well-known quote; the coverage link left the plugin | P-GEPHI-10, P-GEPHI-12, P-EMO-20 and P-ANI-04 became defaults; P-EMO-07 and P-COL-27 tests made yes or no; P-DT-03 reworded; the coverage file named as a repository path; tests/test_canon_sync.py keeps the lists and the JSON in step | SKILL.md, ../../canon/principles.json, ../../canon/principles/
