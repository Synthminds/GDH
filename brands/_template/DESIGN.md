---
name: "Template"
description: "Template design system."
version: "0.1.0"
colors:
  bg: "#ffffff"
  surface: "#f3f4f6"
  border: "#7c828d"
  text: "#17191e"
  text-muted: "#565c68"
  accent: "#1d55b0"
  on-accent: "#ffffff"
  danger: "#b3261e"
typography:
  display:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif"
    fontSize: "40px"
    fontWeight: 700
    lineHeight: 1.1
  heading:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif"
    fontSize: "28px"
    fontWeight: 700
    lineHeight: 1.2
  title:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif"
    fontSize: "20px"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  small:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.45
  caption:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.4
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, \"Liberation Mono\", monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
spacing:
  space-1: "4px"
  space-2: "8px"
  space-3: "16px"
  space-4: "32px"
rounded:
  radius-sm: "4px"
  radius-md: "8px"
  radius-full: "999px"
---

# Template

## Overview

Template is a design system. TODO: Replace this paragraph. Say in two or three sentences what the brand is, who it serves, and the one feeling every surface must carry.

### Content fundamentals

- TODO: Name the voice in three adjectives. Give one sentence of proof for each.
- TODO: State the casing for headings, buttons and labels.
- TODO: State the person (we, you) and the emoji policy.
- TODO: Paste three real lines of copy: a headline, a button label and an error message.

## Colors

Themes: `light`, `dark`. The front matter lists the `light` theme.

| Token | light | dark | Use |
| --- | --- | --- | --- |
| `bg` | `#ffffff` | `#111318` | Page ground. |
| `surface` | `#f3f4f6` | `#1c1f26` | Raised ground for cards, panels and inputs. |
| `border` | `#7c828d` | `#7b8290` | Control outlines and dividers. Border on bg and surface. |
| `text` | `#17191e` | `#eceef2` | Headings and body copy. Text on bg and surface. |
| `text-muted` | `#565c68` | `#a8aeb9` | Secondary copy and captions. Text on bg and surface. |
| `accent` | `#1d55b0` | `#8fb4ff` | The one primary action in a view, links and the focus ring. Text on bg and surface. |
| `on-accent` | `#ffffff` | `#0c1a33` | Label of a filled accent control. Text on accent. |
| `danger` | `#b3261e` | `#ffb4ab` | Error text and destructive actions. Always pair it with a word or an icon. Text on bg and surface. |

Contrast of the pairs named in the usage notes (WCAG 2.x ratio):

| Pair | Theme | Ratio | Required | Result |
| --- | --- | --- | --- | --- |
| `border` on `bg` | light | 3.86:1 | 3:1 (ui) | pass |
| `border` on `bg` | dark | 4.81:1 | 3:1 (ui) | pass |
| `border` on `surface` | light | 3.51:1 | 3:1 (ui) | pass |
| `border` on `surface` | dark | 4.27:1 | 3:1 (ui) | pass |
| `text` on `bg` | light | 17.58:1 | 4.5:1 (text) | pass |
| `text` on `bg` | dark | 15.99:1 | 4.5:1 (text) | pass |
| `text` on `surface` | light | 15.97:1 | 4.5:1 (text) | pass |
| `text` on `surface` | dark | 14.19:1 | 4.5:1 (text) | pass |
| `text-muted` on `bg` | light | 6.71:1 | 4.5:1 (text) | pass |
| `text-muted` on `bg` | dark | 8.33:1 | 4.5:1 (text) | pass |
| `text-muted` on `surface` | light | 6.10:1 | 4.5:1 (text) | pass |
| `text-muted` on `surface` | dark | 7.39:1 | 4.5:1 (text) | pass |
| `accent` on `bg` | light | 7.05:1 | 4.5:1 (text) | pass |
| `accent` on `bg` | dark | 8.97:1 | 4.5:1 (text) | pass |
| `accent` on `surface` | light | 6.40:1 | 4.5:1 (text) | pass |
| `accent` on `surface` | dark | 7.96:1 | 4.5:1 (text) | pass |
| `on-accent` on `accent` | light | 7.05:1 | 4.5:1 (text) | pass |
| `on-accent` on `accent` | dark | 8.37:1 | 4.5:1 (text) | pass |
| `danger` on `bg` | light | 6.53:1 | 4.5:1 (text) | pass |
| `danger` on `bg` | dark | 10.94:1 | 4.5:1 (text) | pass |
| `danger` on `surface` | light | 5.93:1 | 4.5:1 (text) | pass |
| `danger` on `surface` | dark | 9.71:1 | 4.5:1 (text) | pass |

## Typography

| Family | Stack |
| --- | --- |
| `sans` | system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif |
| `mono` | ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace |

| Style | Group | Size | Line height | Weight | Use |
| --- | --- | --- | --- | --- | --- |
| `display` | Headings | 40px | 1.1 | 700 | One hero headline in a view. |
| `heading` | Headings | 28px | 1.2 | 700 | Page and section titles. |
| `title` | Headings | 20px | 1.3 | 600 | Card titles and dialog titles. |
| `body` | Text | 16px | 1.5 | 400 | All running text. The base size. |
| `small` | Text | 14px | 1.45 | 400 | Secondary text, table cells and form help. |
| `caption` | Text | 12px | 1.4 | 500 | Labels, captions and metadata. Never for running text. |
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
| `shadow-sm` | `0 1px 2px rgba(23, 25, 30, 0.08)` | Inputs and resting cards. |
| `shadow-md` | `0 4px 12px rgba(23, 25, 30, 0.12)` | Menus, popovers and raised cards. |

## Shapes

| Token | Value | Use |
| --- | --- | --- |
| `radius-sm` | `4px` | Tags, chips and small controls. |
| `radius-md` | `8px` | Buttons, inputs and cards. |
| `radius-full` | `999px` | Pills and avatars. |

## Motion

| Token | Value | Use |
| --- | --- | --- |
| `duration-fast` | `120ms` | Hover and press feedback on controls. |
| `duration-base` | `200ms` | Menus, dialogs and panels that enter or leave. |
| `ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` | Default easing for every transition. No springs. |

## Visual foundations

#### Color

- Use `bg` for the page ground and `surface` for raised ground.
- Set headings and body copy in `text`. Set secondary copy in `text-muted`.
- Use `accent` for the one primary action in a view, for links and for the focus ring.
- Set the label of a filled `accent` control in `on-accent`.
- Use `danger` for errors and destructive actions. Pair it with a word or an icon.
- Draw control outlines and dividers in `border`.
- Switch theme with `data-theme="light"` or `data-theme="dark"` on the root element.

#### Type

- Set running text in `body`. Use `small` for secondary text and `caption` for labels.
- Use `display` once in a view. Use `heading` for page and section titles and `title` for cards.
- Set code and aligned numbers in `code`.
- TODO: Name the brand typefaces and add their files under `fonts/`. The starter uses system fonts.

#### Spacing, shape and depth

- Space with `space-1` to `space-4` only. Use `space-3` inside cards and `space-4` between sections.
- Round controls and cards with `radius-md`. Use `radius-sm` for tags and `radius-full` for pills.
- Keep surfaces flat. Use `shadow-sm` for resting cards and `shadow-md` for menus and popovers.

#### Motion

- Use `duration-fast` for hover and press feedback and `duration-base` for panels that enter or leave.
- Ease every transition with `ease-standard`. Do not use springs or bounces.
- Remove motion when the user asks for reduced motion.

## Iconography

- TODO: Name the icon set, the stroke weight and the sizes. State the license and where the files live.
- Do not redraw a logo. Use the supplied files under `assets/`.

## Components

No component rules are recorded in the brand book. Build components from the tokens above.

## Do's and Don'ts

- Take every color, size, space, radius and duration from a token in `tokens.json`.
- Add a token before you use a new value. Give it a usage note.
- Keep each text and ground pair at 4.5:1 or more in every theme. Large text and outlines need 3:1.
- Do not show a status by color alone.
- TODO: Add the brand's own do and do not rules.

## Source

This file is generated from `tokens.json` and `README.md` by `ds.py design-md`. Edit those files, then generate it again.
