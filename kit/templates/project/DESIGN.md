---
status: template
name: "<product or brand name>"
version: 0.1.0
updated: YYYY-MM-DD
tokens: design/tokens.json
colors: {}
typography: {}
---

# DESIGN.md

This file is the design system in prose. `design/tokens.json` holds the values. This file holds the rules.
While `status` reads `template`, this file is not a design system. Agents treat it as absent.
The `design-system` skill fills it. Set `status: active` when the user approves the first version.

## Overview

State the idea of the look in two or three sentences. Name the three brand words from `design/brief.md`.
Say what this system is not.

## Colors

List each color token with its role and its reason. Do not list a hex value without a token name.

| Token | Role | Used for | Never used for | Because |
| --- | --- | --- | --- | --- |
| `<color.name>` | `<surface, text, accent, status>` | | | `<brand word or persona trait>` |

Contrast pairs that passed, with the measured ratio:

| Text token | Background token | Ratio | Theme |
| --- | --- | --- | --- |

## Typography

| Role | Family | Weight | Size token | Line height | Because |
| --- | --- | --- | --- | --- | --- |
| Display | | | | | |
| Body | | | | | |
| Data or code | | | | | |

Font licenses are recorded in `design/assets/manifest.json`.

## Layout

State the grid, the spacing scale token names, the breakpoints and the density rule.

## Shapes

State the radius tokens, the border rule and the icon style.

## Elevation

State the shadow or layer tokens and when each applies. Write "none" when the system is flat.

## Motion

Map each duration and easing token to one role: control, surface, page or flourish.
State the reduced-motion behavior.

## Imagery

State the image style, the illustration style, and what a generated image may and may not show.

## Voice

Link the design persona in `design/brief.md`. State three copy rules with one real example each.

## Components

List each component with its states and the tokens it uses. Link the code or the design file.

## Do and do not

| Do | Do not | Why |
| --- | --- | --- |

## Brand-required choices

List each choice that a tell scan would flag and that this brand requires. A reviewer reports these as `brand-required`.

| Choice | Where it applies | Source |
| --- | --- | --- |

## Change log

| Date | Change | Decision record entry |
| --- | --- | --- |
