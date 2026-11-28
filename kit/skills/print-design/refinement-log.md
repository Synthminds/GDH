# Refinement log: print-design

Format: `YYYY-MM-DD | observation | change | files`

2026-11-27 | skill scaffolded | new skill | SKILL.md
2026-11-27 | new skill: FDM print design with a stdlib mesh check, printer profiles and a send gate | created | SKILL.md, references/, scripts/print_check.py
2026-11-27 | the owner asked for model search across print sites; most sites forbid automated access | find-a-model.md and model_search.py plan searches under api, fetch and links-only rules; step 2 searches first | SKILL.md, references/find-a-model.md, references/model-sites.json, scripts/model_search.py
2026-11-28 | the owner wants to find models, see images, download and modify them | model_results.py normalizes API responses, reads licenses and builds an image gallery; model-apis.md; find-a-model sections 3 and 6 | SKILL.md, references/model-apis.md, references/find-a-model.md, scripts/model_results.py
