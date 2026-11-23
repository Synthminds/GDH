---
name: "Harbor Lantern"
description: "Harbor Lantern is a fictional brand, made as the example pack for the Global Design Harness. It is an invented shop on a tidal harbor that serves people who sail small boats. Every surface must feel like a calm voice on the radio: watchful, exact and weathered."
version: "0.1.0"
colors:
  bg: "#f3f5f2"
  surface: "#dfe9ea"
  border: "#5f7178"
  text: "#17242b"
  text-muted: "#44555d"
  accent: "#1d6b45"
  on-accent: "#ffffff"
  danger: "#a52a1c"
  lamp: "#e3a72f"
typography:
  display:
    fontFamily: "\"IBM Plex Sans Condensed\", \"IBM Plex Sans\", \"Arial Narrow\", \"Liberation Sans Narrow\", sans-serif"
    fontSize: "44px"
    fontWeight: 700
    lineHeight: 1.05
  heading:
    fontFamily: "\"IBM Plex Sans Condensed\", \"IBM Plex Sans\", \"Arial Narrow\", \"Liberation Sans Narrow\", sans-serif"
    fontSize: "28px"
    fontWeight: 700
    lineHeight: 1.2
  title:
    fontFamily: "\"IBM Plex Sans Condensed\", \"IBM Plex Sans\", \"Arial Narrow\", \"Liberation Sans Narrow\", sans-serif"
    fontSize: "20px"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "\"IBM Plex Sans\", \"Helvetica Neue\", Arial, \"Liberation Sans\", sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  small:
    fontFamily: "\"IBM Plex Sans\", \"Helvetica Neue\", Arial, \"Liberation Sans\", sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.45
  caption:
    fontFamily: "\"IBM Plex Sans\", \"Helvetica Neue\", Arial, \"Liberation Sans\", sans-serif"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.4
  code:
    fontFamily: "\"IBM Plex Mono\", ui-monospace, Menlo, Consolas, \"Liberation Mono\", monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
spacing:
  space-1: "4px"
  space-2: "8px"
  space-3: "16px"
  space-4: "32px"
rounded:
  radius-sm: "2px"
  radius-md: "4px"
  radius-full: "999px"
---

# Harbor Lantern

## Overview

Harbor Lantern is a fictional brand, made as the example pack for the Global Design Harness. It is an invented shop on a tidal harbor that serves people who sail small boats. Every surface must feel like a calm voice on the radio: watchful, exact and weathered.

This pack is an example. It names no real company, person or product. Copy it to learn the shape of a pack, not to reuse the brand.

### Content fundamentals

- Voice: calm, exact, weathered. Calm: it states the one thing that matters first. Exact: it gives the number and the unit. Weathered: it uses plain words and no hype.
- Limits: calm, but not sleepy. Exact, but not technical. Weathered, but not nostalgic.
- Casing: sentence case for headings, buttons and labels. No all-caps words.
- Person: "we" for the shop, "you" for the reader. No emoji.
- Headline: "Know the window before you leave the dock."
- Button label: "Check today's tide"
- Error message: "No tide data since 09:15. Showing the last forecast."

## Colors

Themes: `light`, `dark`. The front matter lists the `light` theme.

| Token | light | dark | Use |
| --- | --- | --- | --- |
| `bg` | `#f3f5f2` | `#0d171c` | Page ground. Deep-water white of a nautical chart in light; night water in dark. |
| `surface` | `#dfe9ea` | `#15232a` | Raised ground for cards, panels and inputs. The shallow-water tint of a chart. |
| `border` | `#5f7178` | `#70868e` | Control outlines, dividers and chart hairlines. Border on bg and surface. |
| `text` | `#17242b` | `#e4ebe8` | Wet slate. Headings and body copy. Text on bg and surface. |
| `text-muted` | `#44555d` | `#a3b4b8` | Secondary copy and captions. Text on bg and surface. |
| `accent` | `#1d6b45` | `#5fc58f` | Starboard green, from the navigation light. The one primary action in a view, links and the focus ring. Text on bg and surface. |
| `on-accent` | `#ffffff` | `#06140c` | Label of a filled accent control. Text on accent. |
| `danger` | `#a52a1c` | `#ff8b7b` | Port red, from the navigation light. Error text and destructive actions. Always pair it with a word or an icon. Text on bg and surface. |
| `lamp` | `#e3a72f` | `#f0b847` | Lantern amber. A fill behind the next-tide marker only. Never a text color and never a second accent. |

Contrast of the pairs named in the usage notes (WCAG 2.x ratio):

| Pair | Theme | Ratio | Required | Result |
| --- | --- | --- | --- | --- |
| `border` on `bg` | light | 4.64:1 | 3:1 (ui) | pass |
| `border` on `bg` | dark | 4.74:1 | 3:1 (ui) | pass |
| `border` on `surface` | light | 4.12:1 | 3:1 (ui) | pass |
| `border` on `surface` | dark | 4.20:1 | 3:1 (ui) | pass |
| `text` on `bg` | light | 14.47:1 | 4.5:1 (text) | pass |
| `text` on `bg` | dark | 15.00:1 | 4.5:1 (text) | pass |
| `text` on `surface` | light | 12.82:1 | 4.5:1 (text) | pass |
| `text` on `surface` | dark | 13.28:1 | 4.5:1 (text) | pass |
| `text-muted` on `bg` | light | 7.08:1 | 4.5:1 (text) | pass |
| `text-muted` on `bg` | dark | 8.45:1 | 4.5:1 (text) | pass |
| `text-muted` on `surface` | light | 6.28:1 | 4.5:1 (text) | pass |
| `text-muted` on `surface` | dark | 7.48:1 | 4.5:1 (text) | pass |
| `accent` on `bg` | light | 5.90:1 | 4.5:1 (text) | pass |
| `accent` on `bg` | dark | 8.53:1 | 4.5:1 (text) | pass |
| `accent` on `surface` | light | 5.23:1 | 4.5:1 (text) | pass |
| `accent` on `surface` | dark | 7.55:1 | 4.5:1 (text) | pass |
| `on-accent` on `accent` | light | 6.47:1 | 4.5:1 (text) | pass |
| `on-accent` on `accent` | dark | 8.86:1 | 4.5:1 (text) | pass |
| `danger` on `bg` | light | 6.49:1 | 4.5:1 (text) | pass |
| `danger` on `bg` | dark | 7.98:1 | 4.5:1 (text) | pass |
| `danger` on `surface` | light | 5.76:1 | 4.5:1 (text) | pass |
| `danger` on `surface` | dark | 7.06:1 | 4.5:1 (text) | pass |

## Typography

| Family | Stack |
| --- | --- |
| `text` | "IBM Plex Sans", "Helvetica Neue", Arial, "Liberation Sans", sans-serif |
| `condensed` | "IBM Plex Sans Condensed", "IBM Plex Sans", "Arial Narrow", "Liberation Sans Narrow", sans-serif |
| `mono` | "IBM Plex Mono", ui-monospace, Menlo, Consolas, "Liberation Mono", monospace |

Font files: IBM Plex Sans (fonts/IBMPlexSans-Regular-Latin1.woff2); IBM Plex Sans (fonts/IBMPlexSans-Medium-Latin1.woff2); IBM Plex Sans (fonts/IBMPlexSans-Bold-Latin1.woff2); IBM Plex Sans Condensed (fonts/IBMPlexSansCondensed-SemiBold-Latin1.woff2); IBM Plex Sans Condensed (fonts/IBMPlexSansCondensed-Bold-Latin1.woff2); IBM Plex Mono (fonts/IBMPlexMono-Regular-Latin1.woff2).

| Style | Group | Size | Line height | Weight | Use |
| --- | --- | --- | --- | --- | --- |
| `display` | Headings | 44px | 1.05 | 700 | One hero headline in a view. Short lines, sentence case. |
| `heading` | Headings | 28px | 1.2 | 700 | Page and section titles. |
| `title` | Headings | 20px | 1.3 | 600 | Card titles and dialog titles. |
| `body` | Text | 16px | 1.5 | 400 | All running text. The base size. |
| `small` | Text | 14px | 1.45 | 400 | Secondary text, table cells and form help. |
| `caption` | Text | 12px | 1.4 | 500 | Labels, captions and metadata, set in sentence case. Never for running text. |
| `code` | Code | 14px | 1.5 | 400 | Code, identifiers and numbers that must align. |

## Layout

| Token | Value | Use |
| --- | --- | --- |
| `space-1` | `4px` | Gap between an icon and its label. |
| `space-2` | `8px` | Gap inside a control; gap between related items. |
| `space-3` | `16px` | Padding of cards and inputs; gap between form fields. |
| `space-4` | `32px` | Gap between sections; page gutter on wide screens. |

## Elevation

| Token | Value | Use |
| --- | --- | --- |
| `shadow-sm` | `0 1px 0 rgba(23, 36, 43, 0.10)` | A hairline lift under resting cards. Surfaces stay matte. |
| `shadow-md` | `0 4px 10px rgba(23, 36, 43, 0.14)` | Menus, popovers and raised cards. |

## Shapes

| Token | Value | Use |
| --- | --- | --- |
| `radius-sm` | `2px` | Tags, chips and small controls. |
| `radius-md` | `4px` | Buttons, inputs and cards. Corners stay tight: the brand is exact, not soft. |
| `radius-full` | `999px` | Pills and avatars. |

## Motion

| Token | Value | Use |
| --- | --- | --- |
| `duration-fast` | `120ms` | Hover and press feedback on controls. |
| `duration-base` | `180ms` | Menus, dialogs and panels that enter or leave. |
| `ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` | Default easing for every transition. No springs. |

## Visual foundations

#### Color

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

#### Type

- Set running text in `body`, in the `text` family. Use `small` for secondary text and `caption` for labels.
- Use `display` once in a view. Use `heading` for page and section titles and `title` for cards. All three use the `condensed` family, like the legends on a chart.
- Set code and aligned numbers in `code`. Tide times and depths use tabular figures.
- Faces: IBM Plex Sans for text, IBM Plex Sans Condensed for headings, IBM Plex Mono for figures. All three are under the SIL Open Font License. The reason is in `SOURCE.md`.
- The pack ships six Latin-1 WOFF2 files under `fonts/` with the license in `fonts/OFL.txt`: Plex Sans 400, 500 and 700 (for strong text), Plex Sans Condensed 600 and 700, Plex Mono 400. `tokens.css` declares each with `@font-face`. A project that needs another script or weight adds that file from the same release and records it.

#### Spacing, shape and depth

- Space with `space-1` to `space-4` only. Use `space-3` inside cards and `space-4` between sections.
- Round controls and cards with `radius-md`. Use `radius-sm` for tags and `radius-full` for pills.
- Keep surfaces matte and flat. Use `shadow-sm` for resting cards and `shadow-md` for menus and popovers.
- Use thin `border` hairlines to divide, like the lines of a chart. Do not use gloss, glass or glow.

#### Motion

- Use `duration-fast` for hover and press feedback and `duration-base` for panels that enter or leave.
- Ease every transition with `ease-standard`. Do not use springs or bounces.
- Remove motion when the user asks for reduced motion.

## Iconography

- The pack ships no icon set. A project that uses this pack picks one outline set with one stroke weight and records its license.
- The pack ships no logo. A missing logo is a labelled placeholder. Never draw or generate one to fill the gap.
- No mascot. The brand is a voice, never a picture of a person.

## Components

No component rules are recorded in the brand book. Build components from the tokens above.

## Do's and Don'ts

- Take every color, size, space, radius and duration from a token in `tokens.json`.
- Add a token before you use a new value. Give it a usage note.
- Keep each text and ground pair at 4.5:1 or more in every theme. Large text and outlines need 3:1.
- Do not show a status by color alone.
- Do: lead with the answer, then the detail. Do: show the age of data before the data.
- Do not: use a gradient, a second accent color, a stock photo of people, or an exclamation mark.

## Source

This file is generated from `tokens.json` and `README.md` by `ds.py design-md`. Edit those files, then generate it again.
