# Extend and version a system

Use this to add a token, a component or a theme, and to release the change. A system is a product with versions. Every change gets a version, a note and a record.

`DS` means `python3 <skill folder>/scripts/ds.py`.

## First: is the change needed?

1. Check that no existing token or component already does the job.
2. Default: add a token only when the need appears in two or more real places.
3. Hold a candidate in a waiting list in `design/decisions.md` until it earns its place.
4. Check where the change must be made: a code-synced system changes in code. See [sync.md](sync.md).

## Add a token

1. Name it by role. Follow the system's existing pattern. The name must be new across all families.
2. Enter the exact value. For a color, fill every theme, or alias a raw color.
3. Write the usage note. A text color names its grounds.
4. Run `DS validate` and `DS contrast`.
5. Regenerate `tokens.css` and `DESIGN.md`. Add a rule to the README when the token changes how people build.
6. Add a row to `SOURCE.md`: who decided, when and why.

## Add a theme

1. ASK what the theme is for: dark, high contrast, a sub-brand or a season.
2. Add `{"id", "name"}` to `color.themes`. The cap is in [../references/tokens-format.md](../references/tokens-format.md).
3. Give every color a value for the new theme. A color with one string value keeps it in all themes.
4. A dark theme is its own mapping. Lower the chroma. Do not invert.
5. A high-contrast theme holds 7:1 for text pairs.
6. Run `DS contrast`. Every pair must pass in the new theme.
7. Run `DS specimen` and show the new theme beside the old ones.
8. Components must not change between themes. Two themes differ only in token values.

## Add a component

1. Confirm the component is on the inventory or the owner asks for it.
2. Create `components/<Name>/README.md` and `preview.html`. Follow [../references/components.md](../references/components.md).
3. Use tokens only. Run `DS audit components/<Name>`; the target is zero raw literals.
4. Show every state that applies.
5. Product code for the component belongs to the coding harness. Hand it over through `design/handoff.md`.

## Version

Use semantic versioning in `tokens.json` `version`.

| Change | Bump |
| --- | --- |
| Remove or rename a token, a style, a theme or a component prop | major |
| Change a value so that existing screens look different in a way a user would notice | major, unless the owner calls it a fix |
| Add a token, a style, a theme or a component | minor |
| Fix a value that was wrong against its source; edit a usage note | patch |

Write the breaking-change rule above into the README once, so adopters know it.

## Deprecate before you remove

Never keep two versions alive by renaming. No `button2`, no `new-accent`.

1. Keep the old token. Change its usage note to this form:
   `DEPRECATED since <version>. Use <replacement>. Removal: <YYYY-MM-DD>.`
2. A deprecation needs all three: the replacement, the reason and the date.
3. Where a value can alias, point the old token at the new one so both stay equal.
4. Release that as a minor version.
5. On or after the date, remove the token in a major version.
6. Before removal, run `DS audit <folders> --tokens <tokens.json>` and search for the old name. Report what still uses it.

## Release

1. Run `DS validate`, `DS contrast` and `DS specimen`.
2. Regenerate `tokens.css`, `DESIGN.md` and any Tailwind or DTCG export the project uses.
3. Write release notes in `SOURCE.md` or the project change log: added, changed, deprecated, removed, and the action each adopter must take.
4. Record the round in `design/decisions.md`.
5. GATE: publishing the new version to Claude or to a package registry exposes it. Get a yes first.
6. Check that the list of components in code equals the list in `components/`.

## Sources

- Design Systems Handbook (InVision DesignBetter), chapter 3 "Handling change", "The right way: versioning", "The wrong way: duplication"; chapter 4 "Releases, branches, and version numbers".
- Claude Design System artifact type, craft reference on accessibility themes, read 2026-11-23.
