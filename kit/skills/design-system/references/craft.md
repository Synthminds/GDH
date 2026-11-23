# What makes a design system good

Read this before you call a system finished. Rules marked "Default:" yield to the source and the owner. The other rules restate the craft reference of the Claude Design System type and the gates of this skill.

## 1. The brand book is a set of usage rules

- Write the README for an agent that must build with the system. Use imperative sentences.
- Name tokens, styles and assets in each rule: "Set body copy in `body` with color `text` on `bg`."
- Do not write a title, a history, a provenance note or next steps in the README. Put provenance in `SOURCE.md`.
- Let the length follow the source. A thin source gives a short README.
- Sections for a rich source: content fundamentals, visual foundations, iconography, usage rules.
- Content fundamentals: tone, casing, person, emoji policy, and real copy examples.
- Visual foundations: color, type, spacing, imagery, motion, states, borders, shadows, radii and layout.
- Keep the overview short. Claude reads the overview every time and the rest on demand.

## 2. Exact values

- The source defines the inventory. Use its token names, its values and its order.
- A value of 5px stays 5px. Do not round to a scale you prefer.
- The source beats any library it resembles.
- Code is truth. A screenshot is lossy. Sample from a screenshot only when no code exists, and mark it INFERRED.
- Keep one home for each value. A value in `tokens.json` does not also live in a hand-written stylesheet.

## 3. Usage notes

- Every token and every asset has a usage note.
- A note says where the token is used and where it is not.
- A text color names its grounds in this form: "Text on bg and surface." The contrast check reads that sentence.
- Use "Large text on <token>." for display type. Use "Border on <token>." for outlines and rings.
- Put a measured ratio or a warning in the note when a pair is close to the limit.

## 4. Real fonts

- Wire the type scale to real font files. List each file in `type.fonts`.
- A font with no file gets replaced on the page. Ask the owner for the files.
- Record the license of each font in the assets table.
- A system stack is honest when the brand has no typeface. Say so in the README.

## 5. Legible in every theme

- Gate: each text and ground pair holds 4.5:1. Large text, borders, focus rings and icons hold 3:1.
- Check every theme. A dark theme is its own mapping, not an inversion.
- A failing pair from a real source stays exact. Flag it in the usage note and name a safe substitute.
- A high-contrast request means an added theme at 7:1.
- A color-blind-safe request means each status carries a word or an icon and does not rely on red against green.
- Default: with no brand hues to keep, start status colors from the Okabe-Ito set. Read the values from a primary source.
- Default: report APCA values as advice. They are not the gate.

## 6. Assets

- Copy a supplied asset. Never approximate one.
- No logo in the sources means the name in plain type, plus a note. Never redraw a mark from memory.
- Record the source, the license and the date for each file.

## 7. Substance

- Fill every theme.
- Give each component a README and a preview.
- Say what the consumer provides: props, children, container and data.
- Build only the component families the source has.
- List the full inventory first. Track against it. Report what remains.

## 8. No tells

A tell is a generic choice that marks work as machine-made. Avoid these unless the source has them:

- a blue to purple gradient as the brand statement;
- decorative emoji;
- a card with a colored left border;
- filler statistics and invented numbers;
- an overused typeface chosen without a reason;
- gray text on a colored ground.

Precedence: a choice that the brand's own system prescribes is never a tell. Report it as brand-required.

## 9. Structure

- Default: use two tiers. Raw colors hold values. Role colors alias them and carry the usage rules.
- Default: components use role tokens only.
- Default: name by role. `text-muted` survives a rebrand; `gray-500-text` does not.
- Default: keep each scale at 12 values or fewer.
- Default: add a token only when a real need repeats.

## 10. Proof

A system is done when all of these hold:

1. `ds.py validate` reports zero errors and zero warnings, or each warning has a reason in the report.
2. `ds.py contrast` reports zero failures, or each failure is a flagged source value.
3. The specimen page renders every theme and the owner has seen it.
4. `SOURCE.md` has a line for each family and a list of INFERRED values.
5. The decision record holds the round in which the owner accepted the system.

## Sources

- Claude Design System artifact type, craft reference, read 2026-11-23.
- Claude Academy tutorial on design systems: reading order and fonts.
- Design Systems Handbook (InVision DesignBetter), chapter 2 "Design tokens" and "Creating a visual inventory".
