# The tokens.json format

This file describes the token file that a Claude Design System page can read. `scripts/ds.py validate` enforces it. Evidence: DOCUMENTED. The grammar was read from the Design System type's format reference on 2026-11-23. One real system in this shape validates with zero findings. No artifact write was run to confirm each rejection on the live page.

## Shape

```json
{
  "name": "Acme",
  "version": "0.1.0",
  "color": {
    "themes": [{"id": "light", "name": "Light"}, {"id": "dark", "name": "Dark"}],
    "tokens": [
      {"name": "bg", "value": {"light": "#ffffff", "dark": "#111318"}, "usage": "Page ground."},
      {"name": "ink", "value": "#17191e", "usage": "Raw dark. Do not use it in components."},
      {"name": "text", "value": {"light": "{ink}", "dark": "#eceef2"}, "usage": "Body copy. Text on bg."}
    ]
  },
  "type": {
    "fonts": [{"family": "Inter", "file": "fonts/Inter-Variable.woff2", "weight": "400 700", "style": "normal"}],
    "families": {"sans": "Inter, system-ui, sans-serif"},
    "groups": [
      {"name": "Text", "family": "sans", "styles": [
        {"name": "body", "fontSize": "16px", "lineHeight": 1.5, "fontWeight": 400, "usage": "Running text."}
      ]}
    ]
  },
  "spacing": {"tokens": [{"name": "space-1", "value": "4px", "usage": "Icon to label gap."}]},
  "radius": {"tokens": [{"name": "radius-md", "value": "8px", "usage": "Buttons and cards."}]},
  "shadow": {"tokens": [{"name": "shadow-sm", "value": "0 1px 2px rgba(23, 25, 30, 0.08)", "usage": "Resting cards."}]},
  "motion": {"tokens": [{"name": "duration-fast", "value": "120ms", "usage": "Hover feedback."}]}
}
```

## Rules

1. Every family except `type` is `{"tokens": [{"name", "value", "usage"}]}`. The list order is the display order.
2. `color` also holds `themes`: a list of `{"id", "name"}`. The token list is flat. There are no nested groups.
3. A color value is one string for all themes, or an object with one string for each theme id.
4. A color string is one of these:
   - hex with 3, 4, 6 or 8 digits;
   - `rgb()`, `rgba()`, `hsl()` or `oklch()` with plain numbers and no nested function;
   - an alias `"{other-token}"` that names an existing color token.
5. These color values drop on the page: a named color such as `red`, `var()`, `color-mix()`, an alias of a missing token, an alias of itself.
6. A name matches `[A-Za-z0-9][A-Za-z0-9_.-]{0,63}`. Names are unique across all families except `type`.
7. A length in `spacing`, `radius` and in type sizes is a number, or a value in `px`, `rem`, `em` or `%`.
8. `type` has `fonts`, `families` and `groups`. A group names a key of `families`. A style has `name`, `fontSize`, `lineHeight` and `fontWeight`. `letterSpacing`, `sample` and `usage` are optional.
9. A font needs a file. A font that is named with no file gets replaced.
10. Every token has a usage note. A missing note is a warning, not an error.
11. A family may carry a `note` string. Other top-level keys such as `name`, `version` and `meta` are not families.
12. Per-theme values are documented for `color` only. For a shadow that differs by theme, write two tokens.

## The DTCG trap

A W3C Design Tokens (DTCG) file is a name-to-value map:

```json
{"spacing": {"sm": {"$type": "dimension", "$value": {"value": 8, "unit": "px"}}}}
```

It is valid JSON and the page cannot read it. The family shows empty. Its entries are lost at the first token edit on the page. `validate` reports it as `DTCG_MAP`. Convert it first:

```
python3 <skill folder>/scripts/ds.py from-dtcg brand.tokens.json -o tokens.json
```

## Motion

The page has no motion family. Name each motion token by role: control, surface, page or flourish.

UNTESTED: whether a hosted Design System page keeps a `motion` family through a token edit. The page drops entries it cannot read at the first token edit, so motion tokens may vanish without a warning. Kernel rule 13 needs duration tokens, so guard them:

- Keep the motion tokens in `tokens.json`, in the generated `tokens.css` and in the motion section of `DESIGN.md`.
- After any edit on a hosted Design System page, read the page's token file fresh and run `ds.py validate` on it.
- Confirm the `motion` family is still there. When it is gone, restore it from the local `tokens.json` and record the loss.
- Raise this label only after an owner-approved artifact write shows the result. Log it in `refinement-log.md`.

## Caps

Read from the same format reference. `validate` reports each as an error.

| Limit | Cap |
| --- | --- |
| Themes | 8 |
| Colors | 600 |
| Families | 12 |
| Type groups | 12 |
| Type styles | 80 |
| Tokens in any other family | 60 |

Default: stay far below these. A small system is easier to follow.

## Validator codes

Errors block. Warnings do not, unless you pass `--strict`.

| Code | Level | Meaning |
| --- | --- | --- |
| `DTCG_MAP` | error | The family is a name-to-value map. Run `from-dtcg`. |
| `FAMILY_SHAPE`, `TOKEN_SHAPE` | error | The family has no `tokens` list, or a token is not an object. |
| `NAME_INVALID`, `NAME_DUPLICATE` | error | The name breaks the pattern or repeats in another family. |
| `VALUE_MISSING` | error | The token has no value. |
| `COLOR_NAMED` | error | A named color. Write hex. |
| `COLOR_VAR`, `VALUE_VAR` | error | `var()` in a value. Use an alias or the literal. |
| `COLOR_MIX`, `VALUE_COLOR_MIX` | error | `color-mix()` in a value. Write the result. |
| `COLOR_ALIAS_MISSING`, `COLOR_ALIAS_SELF`, `COLOR_ALIAS_CYCLE`, `COLOR_ALIAS_SYNTAX` | error | The alias has no target, points at itself, loops, or is not a whole alias. |
| `COLOR_NESTED_FUNCTION`, `COLOR_SYNTAX`, `COLOR_HEX`, `COLOR_VALUE` | error | The color does not parse. |
| `COLOR_THEME_UNKNOWN` | error | A per-theme key is not a theme id. |
| `THEMES_MISSING`, `THEME_SHAPE`, `THEME_DUPLICATE` | error | The themes list is absent or broken. |
| `LENGTH_INVALID` | error | A spacing or radius value is not a length. |
| `TYPE_SHAPE`, `TYPE_FAMILIES_MISSING`, `TYPE_GROUPS_MISSING`, `TYPE_GROUP_FAMILY`, `TYPE_STYLES_MISSING`, `TYPE_STYLE_DUPLICATE` | error | The type family is not in the fonts, families, groups shape. |
| `TYPE_FONT_SIZE_MISSING`, `TYPE_FONT_SIZE`, `TYPE_LINE_HEIGHT`, `TYPE_FONT_WEIGHT`, `TYPE_LETTER_SPACING` | error | A style field is absent or malformed. |
| `CAP_*` | error | A cap from the table above is exceeded. |
| `USAGE_MISSING` | warning | No usage note. |
| `COLOR_FUNCTION_UNLISTED` | warning | A color function outside the documented list, such as `lab()`. Convert it. |
| `COLOR_THEME_VALUE_MISSING` | warning | A per-theme value skips a theme. |
| `TYPE_FONT_FILE_MISSING` | warning | A font names no file. |
| `TYPE_LINE_HEIGHT_MISSING`, `TYPE_FONT_WEIGHT_MISSING` | warning | A style lacks a field. `from-css` never invents one. |
| `VALUE_PER_THEME_OUTSIDE_COLOR`, `THEMES_OUTSIDE_COLOR` | warning | Theme data outside `color`. |

## What the generated files look like

- `tokens.css`: line 1 is a generated-from comment. `:root` holds every token with the first theme's colors. One `[data-theme="<id>"]` block for each theme redeclares every color. A `prefers-color-scheme: dark` block follows when a `dark` theme exists. An alias becomes `var(--target)`. A dot in a name becomes a dash.
- Type variables: `--font-<family>`, `--type-<style>-size`, `--type-<style>-line-height`, `--type-<style>-weight`, `--type-<style>-letter-spacing`.
- Tailwind v4 file: `@theme inline` maps `--color-<name>` to the variables in `tokens.css`, so themes keep working. `@theme` holds fonts, text sizes, spacing, radius, shadow and easing. Import `tokens.css` first. Default: clear a default namespace you replace with `--color-*: initial` in your own entry file.
- Flat JSON: one name-to-literal map for each theme, with aliases resolved.
- DTCG file: the 2025.10 object forms for color, dimension and duration. Themes and exact source strings sit under `$extensions.gdh`, so `to-dtcg` then `from-dtcg` returns the same file. A `$value` you edit in a DTCG tool wins over the stored string.
- Do not upload this `tokens.css` to a Claude Design System artifact. The page generates its own.

## from-css in detail

- Scopes it reads: `:root`, `html`, `body`, `:host`, a Tailwind `@theme` block, theme selectors such as `[data-theme="dark"]`, `.dark`, `.theme-<id>`, and `@media (prefers-color-scheme: dark)`.
- Scopes it skips and reports: any other selector, and any other media query.
- It resolves `var()` chains with fallbacks, `color-mix()` in `srgb`, `srgb-linear`, `oklab` and `oklch`, and `calc()` with one unit.
- It reads a bare triplet such as `0 59 79` as a color only when a wrapper such as `rgb(var(--x) / 0.5)` exists in the files, or the name ends in `-rgb`, or the triplet has percent signs.
- It keeps a literal as written. It lists every computed literal under COMPUTED.
- It converts only the basic named colors. It reports any other keyword.
- A usage note comes only from a comment on the same line as the declaration. Nothing else is guessed.
- A `var(--x)` that points at another color becomes an alias. Pass `--no-alias` for literals.
- Exit code 1 means at least one property was not converted. The file is still written. Read the report.
