Harbor Lantern is a fictional brand, made as the example pack for the Global Design Harness. It is an invented shop on a tidal harbor that serves people who sail small boats. Every surface must feel like a calm voice on the radio: watchful, exact and weathered.

This pack is an example. It names no real company, person or product. Copy it to learn the shape of a pack, not to reuse the brand.

## Content fundamentals

- Voice: calm, exact, weathered. Calm: it states the one thing that matters first. Exact: it gives the number and the unit. Weathered: it uses plain words and no hype.
- Limits: calm, but not sleepy. Exact, but not technical. Weathered, but not nostalgic.
- Casing: sentence case for headings, buttons and labels. No all-caps words.
- Person: "we" for the shop, "you" for the reader. No emoji.
- Headline: "Know the window before you leave the dock."
- Button label: "Check today's tide"
- Error message: "No tide data since 09:15. Showing the last forecast."

## Visual foundations

### Color

- Use `bg` for the page ground and `surface` for raised ground.
- Set headings and body copy in `text`. Set secondary copy in `text-muted`.
- Use `accent` for the one primary action in a view, for links and for the focus ring. It is the only strong color.
- Set the label of a filled `accent` control in `on-accent`.
- Use `danger` for errors and destructive actions. Pair it with a word or an icon.
- Draw control outlines, dividers and hairlines in `border`.
- Switch theme with `data-theme="light"` or `data-theme="dark"` on the root element.
- Use `lamp` only as a fill behind the next-tide marker. It is never text and never a second accent.
- Keep the page mostly chart white and wet slate. One green element in a view is the target.
- Green for go and red for stop come from a boat's navigation lights. Use them as the lights do: green for the safe action, red for danger.

### Type

- Set running text in `body`, in the `text` family. Use `small` for secondary text and `caption` for labels.
- Use `display` once in a view. Use `heading` for page and section titles and `title` for cards. All three use the `condensed` family, like the legends on a chart.
- Set code and aligned numbers in `code`. Tide times and depths use tabular figures.
- Faces: IBM Plex Sans for text, IBM Plex Sans Condensed for headings, IBM Plex Mono for figures. All three are under the SIL Open Font License. The reason is in `SOURCE.md`.
- The pack ships six Latin-1 WOFF2 files under `fonts/` with the license in `fonts/OFL.txt`: Plex Sans 400, 500 and 700 (for strong text), Plex Sans Condensed 600 and 700, Plex Mono 400. `tokens.css` declares each with `@font-face`. A project that needs another script or weight adds that file from the same release and records it.

### Spacing, shape and depth

- Space with `space-1` to `space-4` only. Use `space-3` inside cards and `space-4` between sections.
- Round controls and cards with `radius-md`. Use `radius-sm` for tags and `radius-full` for pills.
- Keep surfaces matte and flat. Use `shadow-sm` for resting cards and `shadow-md` for menus and popovers.
- Use thin `border` hairlines to divide, like the lines of a chart. Do not use gloss, glass or glow.

### Motion

- Use `duration-fast` for hover and press feedback and `duration-base` for panels that enter or leave.
- Ease every transition with `ease-standard`. Do not use springs or bounces.
- Remove motion when the user asks for reduced motion.

## Iconography

- The pack ships no icon set. A project that uses this pack picks one outline set with one stroke weight and records its license.
- The pack ships no logo. A missing logo is a labelled placeholder. Never draw or generate one to fill the gap.
- No mascot. The brand is a voice, never a picture of a person.

## Usage rules

- Take every color, size, space, radius and duration from a token in `tokens.json`.
- Add a token before you use a new value. Give it a usage note.
- Keep each text and ground pair at 4.5:1 or more in every theme. Large text and outlines need 3:1.
- Do not show a status by color alone.
- Do: lead with the answer, then the detail. Do: show the age of data before the data.
- Do not: use a gradient, a second accent color, a stock photo of people, or an exclamation mark.
