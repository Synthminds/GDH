# Group: components

Catalog group `components`: HTML, CSS, Tailwind and React components, primitives, templates and registries. Read this file at step 6 of `find-assets` when the need is interface code.

How to read this file. An id is a catalog id: `A search <catalog> --group components --query "<id>"` prints its entry. An id marked `*` has `verifiedOn` null: its license was not read for the catalog, so read it before use. Every pick is a default from desk research. Evidence: UNTESTED in a build. License notes are DOCUMENTED on the catalog date, except where marked `*`.

Design decisions belong to `website-design`, `app-design` and `dashboard-design`. This file covers sourcing and license.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| Accessible behavior with your own styling | `radix-primitives`, `base-ui`, `ark-ui`, `headless-ui` | Unstyled: the look comes from project tokens | You design every state yourself |
| A copy-in styled baseline for React and Tailwind | `shadcn-ui` | You own the code after the copy | The default look is common. Restyle before the first review. |
| Animated marketing sections | `magicui`, `motion-primitives`, `cult-ui`, `kokonut-ui` | Plain permissive licenses | Overused effects read as a template. Paid tiers exist. |
| Animated effects with a resale limit | `react-bits`, `animate-ui`, `aceternity-ui*` | Large, polished sets | Not plain MIT. Blocked in a resale kit until the user approves. |
| Static HTML with no framework | `hyperui`, `daisyui`, `flowbite`, `uiverse` | Works without React. Good for static pages and email. | Community pieces vary. Check keyboard use and contrast. |
| Restrained forms and inputs | `origin-ui` | Clean input patterns | It is moving to a successor (`coss-ui*`, license unknown: blocked) |
| Vue, Solid or Svelte | `ark-ui`, `park-ui`, `headless-ui`, `daisyui` | Multi-framework | Smaller sets |
| Tokens and utilities with no component layer | `open-props`, `tw-animate-css` | Small, framework-free | None noted |
| A full site template | `html5up*`, `astro-themes*` | Fast start for a static site | Credit duty or per-theme terms. A template is the least unique start. |
| Discovery across many registries | `shadcn-registry-directory`, `21st-dev*` | Wide reach | Each registry and each author sets a license. Review code before install. |
| A wide plugin-based kit | `preline` | Broad coverage | A second fair-use license adds limits. Read both. |

Not asset sources: `tailwind-plus*` is a paid catalog; never copy from its previews. `impeccable` is an agent design skill; see its tool card.

## Decision rules

1. Design system first. When `DESIGN.md` names a component library, stay inside it.
2. Choose headless primitives when the brand words ask for a distinct look. A styled kit brings its own look with it.
3. Choose a styled baseline when the brief asks for speed and the look is set by tokens anyway.
4. Default: one animated effect component for each view. A second one needs a reason from the brief.
5. A component with motion must honor reduced motion. Test it before you record it.
6. A registry install is a third-party code pull. Read the code, the dependencies and the license of that registry.
7. A marketplace component with no stated license is a credited reference. Re-implement the idea with project primitives.
8. In a resale kit or a builder tool, every `yes-with-limits` entry here needs the user's recorded approval.
9. Prefer a source you can read in full over one that hides source behind a paid or metered call.

## License traps

- A resale clause on top of a permissive license (`react-bits`, `animate-ui`). The registry field for one of them states only the permissive license.
- Two licenses at once (`preline`): the stricter one decides.
- A custom license (`aceternity-ui*`): unread. Read every clause.
- Per-registry and per-author terms (`shadcn-registry-directory`, `21st-dev*`): the index license says nothing about an item.
- A component can bundle a font, an icon set or an image with its own license. Open the files.
- Paid previews: a preview grants nothing.

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Kit look | Default radius, default neutral palette, default shadow, unchanged spacing | Map every value to a project token before review |
| Effect pile | Three or more animated backgrounds, borders or text effects in one view | Keep the one that serves the primary job. Remove the rest. |
| Registry trust | An install ran before anyone read the item | Read first. Check the diff after. |
| Preview copy | Markup that matches a paid product's preview | Remove it. Build from primitives. |
| Marketplace default | The top search result, unchanged | Judge by fit to the need form. Change layout or motion. |
| Second kit | Two styled kits in one product | Pick one. Record the reason. |

## Worked choice

The outcomes below are illustrative. They show the reasoning, not verified facts about a source.

Need: a pricing section for a B2B data tool. Brand words: exact, calm, plain. Ships in a client product. The project uses React and has tokens.

- Tier 1: no pricing component. A headless primitives package is installed.
- Tier 3: a marketplace search returns several pricing tables with previews. Their structure is useful: three plans, one highlighted, a feature matrix under the fold.
- Rejected: an animated border effect from an effects library. It conflicts with "calm", and its license adds a resale clause the project does not need to carry.
- Chosen: build the section from the installed primitives and project tokens. Use the marketplace previews as a reference for structure only, with a credit in the direction notes.
- Record: nothing new enters. The closing report says so.
