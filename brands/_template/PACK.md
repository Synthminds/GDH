# What a brand pack holds

A brand pack is the portable copy of one brand's design system. Any agent can read it from disk. A Claude Design System artifact is made from it, never the other way round without a check.

Copy this folder to `brands/<slug>/` with `python3 kit/skills/design-system/scripts/ds.py init brands/<slug> --name "<Name>"`. Then run the `design-system` skill.

## Files

| File | Written by | Holds |
| --- | --- | --- |
| `README.md` | a person or an agent | The brand book as usage rules: content fundamentals, visual foundations, iconography, usage rules that name tokens. No title, no history. |
| `tokens.json` | a person or an agent | The tokens in the Claude Design System shape. The single source of every value. |
| `tokens.css` | `ds.py export` | Custom properties for `:root` and each theme. Generated. Do not edit. |
| `DESIGN.md` | `ds.py design-md` | YAML front matter and prose for any coding agent. Generated. Do not edit. |
| `SOURCE.md` | a person or an agent | Where each value came from, the date read, what is INFERRED and what the owner confirmed. |
| `assets/README.md` | a person or an agent | The assets table: file, group, source, license, attribution, date. |
| `assets/<Group>/` | copied files | Logos, icons and imagery as supplied. Never redrawn. |
| `fonts/` | copied files | Font files named in `tokens.json` `type.fonts[].file`, each with a license on record. |
| `components/<Name>/` | a person or an agent | `README.md` and `preview.html` for each component. |
| `PACK.md` | this template | This page. Keep it in the template only. |

## Rules

1. `tokens.json` is the source. Regenerate `tokens.css` and `DESIGN.md` after every change to it.
2. Every token has a usage note. A text color names the grounds it reads on.
3. Every value has a row in `SOURCE.md`. A value with no source is marked INFERRED and waits for the owner.
4. Every asset has a source and a license line before it is used.
5. Keep private facts out of a public pack: no client names, no account ids, no artifact addresses.
6. The starter values in this template are placeholders. They are not a brand.

## Regenerate and check

```
DS="python3 kit/skills/design-system/scripts/ds.py"
$DS validate  brands/<slug>/tokens.json
$DS contrast  brands/<slug>/tokens.json
$DS export    brands/<slug>/tokens.json --css brands/<slug>/tokens.css
$DS design-md brands/<slug>/tokens.json --readme brands/<slug>/README.md -o brands/<slug>/DESIGN.md
$DS specimen  brands/<slug>/tokens.json -o /tmp/<slug>-specimen.html
```

Exit code 0 means pass. Exit code 1 means findings to read.
