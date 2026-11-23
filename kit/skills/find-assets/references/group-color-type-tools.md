# Group: color and type tools

Catalog group `color-type-tools`: color scales, palette tools, type scale tools and font metric tools. Read this file at step 6 of `find-assets` when the need is a ready scale or a tool that produces values.

How to read this file. An id is a catalog id. An id marked `*` has `verifiedOn` null: read its license before use. Every pick is a default from desk research. Evidence: UNTESTED in a build. License notes are DOCUMENTED on the catalog date, except where marked `*`.

Palette decisions belong to `color`. Scale and pairing decisions belong to `typography`. Token files belong to `design-system`. This group supplies starting values and calculators.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| Ready interface color scales with dark pairs | `radix-colors` | Twelve steps for each hue, with alpha and dark variants | Many products share these hues |
| A simple ready palette | `open-color`, `tailwind-palette` | Readable, well known | An older palette; the default look of a common framework |
| Scales generated to a contrast target | `leonardo` | You state the ratio, it finds the color | None noted |
| A custom scale in a perceptual color space | `huetone`, `oklch-picker` | Tune lightness and chroma step by step | Manual web tools |
| Fast palette exploration | `coolors*`, `realtime-colors*` | Quick ideas; a live page preview | `coolors*`: no resale of palettes, no model training, per the catalog note. `realtime-colors*`: terms unknown. |
| Fluid type and space scales | `utopia` | The usual method for fluid scales | Checked from the registry field only |
| A modular scale preview | `typescale*` | Quick ratio check | Terms unknown |
| Pairing ideas | `fontjoy*` | An idea starter | Terms unknown. A person must review each pair. |
| System font stacks | `modern-font-stacks` | Public domain stacks by classification, no download | Rendering differs by operating system |
| No layout shift when a web font loads | `capsize` | Trims text to the cap height and builds fallback metrics | Needs the font's metrics |

## Decision rules

1. A tool gives values. Values become tokens only through `color`, `typography` or `design-system`.
2. A ready scale is a starting point. Shift hue, chroma or lightness toward the brand before it becomes a token.
3. Check contrast on the final tokens, in every theme. Use the contrast command of the design-system script.
4. A package gets a manifest entry with `--package`. Record it like any dependency.
5. A web tool with unknown terms is for exploration. Do not paste its output files into the project.
6. Default: a color value or a ratio you read off a tool is a number, not an asset. Record the tool and the reason in `design/decisions.md`, not in the manifest.
7. A palette taken whole from a palette site is a different case. Read that site's terms first.
8. A generated pairing is a guess. `typography` tests it on real copy.
9. Use fluid scales only between two stated viewport widths. Take both from the design system.

## License traps

- Palette sites can claim terms over the palettes themselves. One catalog note names a no-resale clause. Unread.
- Web tools with no stated terms are unknown, not free.
- A scale package is permissive code. A brand's published palette is not: it is a reference.
- A font metric tool needs the font file. The font's own license still applies.

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Stock scale | A known scale used unchanged as the brand palette | Tune it to the brand through `color` |
| Tool as decision | "The generator picked it" as the reason for a color | Write the reason from the brief |
| Unchecked contrast | A generated scale that was never tested in the dark theme | Run the contrast check on every pair |
| Ratio worship | A type scale that follows a ratio and ignores the content | Test on real copy. Adjust the steps. |
| Raw values | Colors pasted from a tool into components | Make tokens first |

## Worked choice

The outcomes below are illustrative. They show the reasoning, not verified facts about a source.

Need: status colors for a dashboard that has a brand palette and no semantic colors. Themes: light and dark.

- Tier 1: `design/tokens.json` holds neutrals and one accent. No status colors.
- Catalog: `A search <catalog> --group color-type-tools --query "contrast" --commercial --verified`.
- Chosen: the contrast-target generator. `color` states the targets: text on a status surface meets the contrast floor in both themes.
- The generator returns candidate values. `color` shifts the hues so that none collides with the accent.
- License: permissive package. Verdict `clear`. Recorded with `--package`, because the build uses it.
- The values enter `design/tokens.json` through `design-system`, each with a usage note. The contrast check runs on every pair.
