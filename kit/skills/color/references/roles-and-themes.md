# Semantic roles, themes and dark mode

Read this file at steps 7 to 9 of `color`. It covers the role set, how roles map to ramp steps, how to write usage notes that the contrast script can read, themes, the dark mode rules and the failure patterns.

Evidence. Semantic tokens over raw colors, "dark mode is its own mapping", "contrast rises on a state change", `color-scheme`, the theme color and the native select rule come from the Vercel Web Interface Guidelines. The jobs of ramp steps come from Radix Colors. Role-based naming, one interactive color and theming by swapping values come from the Design Systems Handbook, chapters 2 and 3. A high-contrast theme at 7:1 and theme-exact failing pairs come from the Claude Design System craft rules. All were read 2026-11-23. The chroma and lightness adjustments for dark mode are defaults from practice.

Terms. A role is a semantic token. A ground is the color under a text or a control. A pair is one foreground role on one ground role. A theme is one full set of values for the same roles.

## 1. The role set

Components use roles. They never use a ramp step or a raw value.

Start with the smallest set that the first real screen needs. Add a role when a real need repeats.

| Group | Role | Job | Contrast it must meet |
| --- | --- | --- | --- |
| Surface | `bg` | Page ground | None; it is a ground |
| Surface | `surface` | Cards and panels | None |
| Surface | `surface-raised` | Menus, popovers, dialogs | None |
| Surface | `surface-sunken` | Wells, table stripes, code blocks | None |
| Text | `text` | Body copy and headings | 4.5:1 on every surface it sits on |
| Text | `text-muted` | Captions, meta, placeholders | 4.5:1 on every surface it sits on |
| Text | `text-disabled` | Disabled labels | None; pair it with a disabled state that is not color alone |
| Border | `border` | Dividers and card edges | None; decoration only |
| Border | `border-control` | Edges of inputs, checkboxes, outline buttons | 3:1 on every surface it sits on |
| Border | `focus` | Focus ring | 3:1 against the ground beside it |
| Accent | `accent` | Primary action fill | 3:1 on surfaces when it is the only edge of the control |
| Accent | `accent-hover`, `accent-pressed` | States of the fill | Same as `accent`; contrast never falls |
| Accent | `on-accent` | Label on the fill | 4.5:1 on `accent` and on its states |
| Accent | `accent-text` | Links and colored text | 4.5:1 on every surface it sits on |
| Accent | `accent-subtle` | Tinted ground for a selected item | None; `text` on it still needs 4.5:1 |
| Status | `danger`, `on-danger` | Destructive fill and its label | As accent and on-accent |
| Status | `danger-text`, `danger-subtle` | Error message; error ground | 4.5:1 for the text on its grounds |
| Status | `success-*`, `warning-*`, `info-*` | Same four parts, only for statuses the product has | Same |

Rules:

1. Name by role, never by value. `accent`, not `teal-500`.
2. One interactive color. Links and the primary button fill come from the same hue.
3. A decorative border is not a control outline. Give each its own role.
4. Add a status only when the product shows that status. A status needs an icon or a label as well.
5. `warning` is usually a light fill. Its label is dark text, not white.
6. A disabled state uses lower contrast and one more cue: a cursor, an icon, a pattern or a text.
7. Default: start with 8 to 14 roles. More is a sign of one-off needs.

## 2. Map ramp steps to roles

| Role | Light theme | Dark theme |
| --- | --- | --- |
| `bg` | Neutral 1 | Neutral 1 of the dark ramp |
| `surface` | Neutral 2, or white | Neutral 2 |
| `surface-raised` | White or neutral 1 with a shadow | Neutral 3 |
| `surface-sunken` | Neutral 3 | A step darker than `bg`, or neutral 2 |
| `text` | Neutral 12 | Neutral 12 |
| `text-muted` | Neutral 11 | Neutral 11 |
| `border` | Neutral 6 | Neutral 6 |
| `border-control` | Neutral 8 | Neutral 8 |
| `focus` | Brand 8 or 9 | Brand 8 or a lighter brand step |
| `accent` | Brand 9 | Brand 9 |
| `accent-hover` | Brand 10 | Brand 10 of the dark ramp, which is lighter |
| `on-accent` | White, or brand 12 on a light fill | White, or brand 12 on a light fill |
| `accent-text` | Brand 11 | Brand 11 of the dark ramp |
| `accent-subtle` | Brand 3 | Brand 3 of the dark ramp |
| `danger-text` | Red 11 | Red 11 of the dark ramp |
| `danger-subtle` | Red 3 | Red 3 of the dark ramp |

This map is a default. The script decides. When a pair fails, move the role one step and run the script again.

## 3. Write the tokens and the usage notes

The color family holds a flat list. A value is one string, or one string for each theme. The grammar belongs to `design-system`.

The contrast script reads pairs from the usage notes. Write each note so that it can.

| Note pattern | The script checks |
| --- | --- |
| `Text on bg and surface.` | This token as normal text on `bg` and on `surface`, at 4.5:1 |
| `Large text on accent.` | This token as large text on `accent`, at 3:1 |
| `Outline on bg and surface.` | This token as a control outline, at 3:1 |
| `Border on bg.`, `Focus ring on bg.`, `Icon on surface.`, `Control on bg.` | This token as a non-text element, at 3:1 |

Rules:

1. Use the exact token names after "on". Join names with commas, "and" or "or".
2. A decorative border must not say "Border on". Write "Dividers. Decoration only." Then the script does not hold it to 3:1.
3. A text token with no "Text on" phrase is not checked. That is a gap, not a pass.
4. Put the job first, then the pair phrase: "Links. Text on bg and surface."
5. Raw ramp steps that live in the token file take the note "Raw. Do not use in components."

Example:

```json
{"name": "text-muted", "value": {"light": "#4f5b5a", "dark": "#a9b4b3"},
 "usage": "Captions and meta. Text on bg and surface."}
```

Then run `DS validate <tokens.json>` and `DS contrast <tokens.json>`.

## 4. Themes

1. A theme is a full set of values for the same roles. Component code does not change between themes.
2. List the themes in `color.themes`. Each role gives one value for each theme id.
3. A role with one value for all themes writes one string. Check that it works on every theme's grounds.
4. Default: ship light and dark. Follow the system preference unless the brief names a default.
5. A high-contrast theme is an added theme. Its text pairs reach 7:1. It does not replace the normal themes.
6. A sub-brand or a section theme swaps values only. It adds no new role.
7. The token file caps the number of themes. Read the cap in the token format reference of `design-system`.

Check: put two themes side by side on the same screen. Only colors differ. Every role is filled in both.

## 5. Dark mode rules

1. Build dark as its own mapping. An inverted light theme leaves strong colors glowing and shadows useless.
2. Choose the dark ground from the design system, then the brief. Do not hard-code true black or near black.
3. Raise the surface lightness with elevation. A menu is lighter than a card. A card is lighter than the page.
4. Shadows carry little on a dark ground. Use the lighter surface and a border to show elevation.
5. Default: lower the chroma of large fills and tinted grounds. Keep the hue.
6. Default: body text is an off-white near L 0.93 to 0.95. Muted text sits near L 0.76.
7. Colored text needs a light step of the ramp. The light-theme link color fails on a dark ground.
8. A solid fill can keep its light-theme value when white text still passes on it. Check its edge against the dark ground as a control.
9. Status colors need new values. A tinted status ground on dark is a dark tint, not a pastel.
10. Hover and pressed states move toward more contrast, which on dark means lighter.
11. Re-run the script. Every pair is checked in every theme. That is the gate.
12. Default: aim above the floor for dark body text, at 7:1 or more. The authors of APCA state that the WCAG 2 ratio overstates contrast for dark colors.
13. Check gradients on dark grounds for banding.
14. Give images, illustrations and the logo a dark variant. Do not invert a photo.

For code deliverables, also set these. They come from the Vercel guidelines.

- `color-scheme: dark` on the root in the dark theme, so native controls and scrollbars follow.
- The browser theme color matches the page ground in each theme.
- A native `select` gets explicit ground and text colors.

## 6. States

| State | Rule |
| --- | --- |
| Hover | One ramp step toward more contrast with the ground |
| Pressed | Two steps toward more contrast |
| Focus | The `focus` ring, 3:1 against the ground beside it; never removed without a replacement |
| Selected | `accent-subtle` ground, plus a second cue: a check mark, a bar that encodes selection, or weight |
| Disabled | Lower contrast, plus a second cue |
| Error | `danger-text` with an icon and a message; a red outline alone is not enough |

Contrast never falls on a state change. Check the label on the hover and pressed fills as pairs.

## 7. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Primitives only | Components use ramp steps; dark mode means editing every component | Add roles. Map steps to roles. |
| Value names | Tokens named `blue-600` in components | Rename by role |
| Inverted dark | Dark theme made by flipping lightness | Build the dark mapping |
| Glowing dark | Full-chroma fills on a dark ground | Lower the chroma of large areas |
| One link color | The same link value in both themes; it fails in one | A value for each theme |
| Border as outline | A pale divider color used as an input edge | `border-control` at 3:1 |
| Unchecked role | A text role with no "Text on" note | Write the note. Run the script. |
| Half theme | A role with no value in one theme | Fill every role in every theme |
| Role sprawl | Forty roles after one screen | Merge. Add a role only when a need repeats. |
| Status by hue | Red and green badges with no icon or label | Add the second cue |
