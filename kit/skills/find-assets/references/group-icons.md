# Group: icons

Catalog group `icons`: interface icon sets, brand marks and icon tooling. Read this file at step 6 of `find-assets` when the need is an icon.

How to read this file. An id is a catalog id. An id marked `*` has `verifiedOn` null: read its license before use. This group has no such id on the catalog date. Every pick is a default from desk research. Evidence: UNTESTED in a build. License notes are DOCUMENTED on the catalog date.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| A default stroke set for product UI | `lucide`, `tabler-icons`, `heroicons` | Consistent grids, permissive licenses | `lucide` holds no brand marks. `heroicons` is small. `tabler-icons` holds brand marks: trademark rules apply. |
| Several weights, or duotone | `phosphor` | Six weights for each icon, so the stroke can match the text weight | A larger bundle when it is not tree-shaken |
| Variable axes: fill, weight, grade, optical size | `material-symbols` | One icon font with axes | A strong platform look |
| Regular and filled pairs | `fluent-icons`, `bootstrap-icons`, `remix-icon` | Broad sets with both styles | `fluent-icons` has a platform look. `remix-icon` forbids logo use. |
| A large free rounded set | `hugeicons-free` | Large free tier | Checked from the registry field only. Paid styles may not be redistributed. |
| Existing brand marks | `simple-icons` | The usual source for single-path brand marks | Each mark is a trademark. Use it unchanged, by that brand's guidelines. |
| Many sets behind one interface | `iconify` | One API across sets | Each set keeps its own license. Some need credit. |
| Icons with hover motion | `animated-lucide` | Quick micro-motion | Use it sparingly. Honor reduced motion. |

A connected `logo-search` tool can also return existing marks. An empty result from it can be an outage, not an answer.

## Decision rules

1. One icon set for each product. Two sets differ in grid, stroke, corner and optical weight, and the difference shows.
2. Match the stroke to the text. Set the icon stroke so that it reads as heavy as the body text beside it.
3. Take icon sizes from tokens. Do not size icons by hand in each place.
4. When the set lacks an icon, draw it on the same grid with the same stroke and corner. Record it with `--origin own`.
5. Never import one icon from a second set to fill a gap.
6. An icon is never a logo. A stock icon cannot be protected, and at least one license here forbids the use.
7. A brand mark is not an icon. Do not recolor, crop or restyle it unless that brand's guidelines allow it.
8. Use a brand mark only for "works with", "sign in with" and social links. Never in a way that suggests an endorsement.
9. Record an icon package once, with `--package`. Record a single downloaded SVG as a file.
10. An icon-only control needs an accessible name. `accessibility-gate` checks it.

## The consistency test

Run this before you accept a set.

1. Pick the twelve icons the product uses most.
2. Set them in a row at the body text size, beside a line of body text.
3. Look for the odd one: a different stroke, a different corner, a heavier fill, a different visual size.
4. Repeat at the smallest size the product uses.
5. A set that fails at the smallest size is the wrong set, or the size is too small.

## License traps

- `remix-icon`: the repository license changed and now forbids logo and brand-mark use. Its registry field still names the old license.
- `simple-icons`: public domain as a collection. The marks stay trademarks. The data file lists a license and guidelines for single marks.
- `iconify`: the tooling license says nothing about a set. Read the set's own license.
- `tabler-icons`: brand marks inside a permissive set are still trademarks.
- `hugeicons-free`: only the free pack is permissive.

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Mixed sets | Two stroke widths or two corner styles in one view | Return to one set. Draw the gaps. |
| Default everything | The set's default size and stroke in every place | Set size and stroke from tokens to match the type |
| Icon as logo | A stock icon beside the product name as the mark | Hand off to `logo-identity` |
| Restyled brand mark | A partner logo recolored to the product palette | Restore the official mark. Read that brand's guidelines. |
| Decoration icons | An icon on every heading and every card | Keep icons where they speed recognition. Remove the rest. |
| Unnamed control | An icon-only button with no accessible name | Add the name |

## Worked choice

The outcomes below are illustrative. They show the reasoning, not verified facts about a source.

Need: interface icons for a reading app. Brand words: quiet, literary, warm. Body text is a serif at a light weight. Ships in a client product.

- Tier 1: no icon set installed.
- Catalog: `A search <catalog> --group icons --query "stroke weights" --commercial`.
- A default 2 px stroke set looks heavy beside the light serif. The weight range of `phosphor` lets the stroke match the text: its light weight sits closest.
- License: a permissive code license in the package. Verdict `clear`. No credit in the product.
- Change planned: icon size from the type scale tokens; stroke weight fixed at one weight product-wide.
- Record: one package entry. The two icons the set lacks are drawn on its grid and recorded with `--origin own`.
