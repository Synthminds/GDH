Template is a design system. TODO: Replace this paragraph. Say in two or three sentences what the brand is, who it serves, and the one feeling every surface must carry.

## Content fundamentals

- TODO: Name the voice in three adjectives. Give one sentence of proof for each.
- TODO: State the casing for headings, buttons and labels.
- TODO: State the person (we, you) and the emoji policy.
- TODO: Paste three real lines of copy: a headline, a button label and an error message.

## Visual foundations

### Color

- Use `bg` for the page ground and `surface` for raised ground.
- Set headings and body copy in `text`. Set secondary copy in `text-muted`.
- Use `accent` for the one primary action in a view, for links and for the focus ring.
- Set the label of a filled `accent` control in `on-accent`.
- Use `danger` for errors and destructive actions. Pair it with a word or an icon.
- Draw control outlines and dividers in `border`.
- Switch theme with `data-theme="light"` or `data-theme="dark"` on the root element.

### Type

- Set running text in `body`. Use `small` for secondary text and `caption` for labels.
- Use `display` once in a view. Use `heading` for page and section titles and `title` for cards.
- Set code and aligned numbers in `code`.
- TODO: Name the brand typefaces and add their files under `fonts/`. The starter uses system fonts.

### Spacing, shape and depth

- Space with `space-1` to `space-4` only. Use `space-3` inside cards and `space-4` between sections.
- Round controls and cards with `radius-md`. Use `radius-sm` for tags and `radius-full` for pills.
- Keep surfaces flat. Use `shadow-sm` for resting cards and `shadow-md` for menus and popovers.

### Motion

- Use `duration-fast` for hover and press feedback and `duration-base` for panels that enter or leave.
- Ease every transition with `ease-standard`. Do not use springs or bounces.
- Remove motion when the user asks for reduced motion.

## Iconography

- TODO: Name the icon set, the stroke weight and the sizes. State the license and where the files live.
- Do not redraw a logo. Use the supplied files under `assets/`.

## Usage rules

- Take every color, size, space, radius and duration from a token in `tokens.json`.
- Add a token before you use a new value. Give it a usage note.
- Keep each text and ground pair at 4.5:1 or more in every theme. Large text and outlines need 3:1.
- Do not show a status by color alone.
- TODO: Add the brand's own do and do not rules.
