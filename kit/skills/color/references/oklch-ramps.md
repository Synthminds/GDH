# OKLCH ramps and the tinted neutral

Read this file at step 6 of `color`. It covers the OKLCH model, the computed lightness thresholds, the ramp recipe, the tinted neutral, the dark ramp, gamut limits, a worked ramp and the failure patterns.

Evidence. Working in OKLCH and the OKLCH default palette come from the Tailwind CSS documentation. The twelve steps with fixed jobs come from Radix Colors, "Understanding the scale". Tinting neutrals, borders and shadows toward the ground hue comes from the Vercel Web Interface Guidelines. All were read 2026-11-23. The thresholds, chroma limits and hex values in this file were computed on 2026-11-23 with the color conversion of `ds.py`. The lightness and chroma targets of the recipe are GDH defaults. The gate is the contrast script, not this recipe.

Terms. A ramp is one hue in ordered lightness steps. A step is one color of a ramp. A ground is the color under a text or a control. In gamut means the color can be shown in sRGB.

## 1. OKLCH in three numbers

`oklch(L C H)`:

- L is lightness, from 0 (black) to 1 (white). Equal steps in L look like equal steps in lightness.
- C is chroma, from 0 (gray) upward. The largest value a screen can show depends on hue and lightness.
- H is hue, an angle from 0 to 360.

Hue anchors, computed from the sRGB primaries:

| Color | H | Note |
| --- | --- | --- |
| Red | 29 | |
| Orange | 53 | |
| Yellow | 110 | Strong only at high lightness |
| Green | 142 | |
| Cyan and teal | 195 | Low chroma limit at mid lightness |
| Blue | 264 | Strong only at low lightness |
| Magenta | 328 | |

Why OKLCH for ramps: you can hold hue and chroma and move only lightness. Contrast depends mostly on lightness. So one lightness plan serves every hue.

## 2. Computed thresholds

Use these to plan a ramp. Then let the script decide.

| Question | Answer | Computed for |
| --- | --- | --- |
| How dark must a fill be to take white text at 4.5:1? | L 0.55 or lower is safe. The limit runs from 0.55 to 0.59 by hue. | Eight hues, chroma 0.15 or the sRGB limit |
| How dark must a gray be to reach 3:1 on white? | L 0.67 or lower | Chroma 0 |
| On a dark ground of L 0.17 to 0.21, how light must a foreground be for 3:1? | L 0.49 to 0.50 or higher | Neutral foreground |
| The same, for 4.5:1? | L 0.58 to 0.60 or higher | Neutral foreground |
| The same, for 7:1? | L 0.70 to 0.72 or higher | Neutral foreground |

Consequences:

1. A light, strong fill, such as yellow, amber, lime or light orange, takes dark text, not white.
2. A control outline on a white ground sits at L 0.67 or lower. A pale gray outline fails.
3. One mid-lightness color cannot serve as text in both themes. Plan a light-theme text step and a dark-theme text step.

## 3. sRGB chroma limits

The largest in-gamut chroma, by lightness and hue. Computed.

| L | Red 25 | Orange 55 | Yellow 100 | Green 145 | Teal 195 | Blue 255 | Violet 300 | Magenta 330 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.30 | 0.12 | 0.07 | 0.06 | 0.09 | 0.05 | 0.10 | 0.16 | 0.14 |
| 0.45 | 0.18 | 0.11 | 0.09 | 0.14 | 0.08 | 0.15 | 0.24 | 0.21 |
| 0.60 | 0.24 | 0.15 | 0.13 | 0.19 | 0.10 | 0.20 | 0.26 | 0.27 |
| 0.75 | 0.15 | 0.17 | 0.16 | 0.24 | 0.13 | 0.13 | 0.15 | 0.25 |
| 0.90 | 0.05 | 0.06 | 0.19 | 0.20 | 0.15 | 0.05 | 0.06 | 0.09 |

Read it this way:

- Yellow and green are strong when light. Blue, violet and red are strong when dark.
- Teal is never very strong in sRGB. A teal brand looks quieter than its paint chip. Say so to the user early.
- A status set with equal chroma across hues must use the lowest limit among them.

## 4. The ramp recipe

Build each hue as twelve steps with fixed jobs. Then put only the steps you use into tokens.

| Step | Job | Light theme L | Chroma, as a share of the peak |
| --- | --- | --- | --- |
| 1 | Page ground | 0.99 | 5 to 10% |
| 2 | Subtle ground | 0.975 | 10 to 15% |
| 3 | Component ground | 0.95 | 25% |
| 4 | Component ground, hover | 0.925 | 40% |
| 5 | Component ground, pressed or selected | 0.895 | 50% |
| 6 | Subtle border, decoration only | 0.86 | 65% |
| 7 | Border, decoration only | 0.80 | 80% |
| 8 | Control outline and focus ring | 0.64 | 100% |
| 9 | Solid fill: the named color | 0.50 to 0.56 for white text | 100% |
| 10 | Solid fill, hover | Step 9 minus 0.04 | 95% |
| 11 | Colored text | 0.44 to 0.48 | 85% |
| 12 | High-contrast text | 0.22 to 0.26 | 45% |

Procedure:

1. Fix the hue from the palette plan.
2. Set step 9 first. It is the named color. Pick its L for the text it must carry.
3. Read the chroma limit for that hue and L from the table. Set the peak chroma at or under it.
4. Fill the other steps from the L column and the chroma shares.
5. Convert each step to sRGB. A step that is out of gamut loses chroma until it fits. Hold L and H.
6. Look at the twelve steps side by side. No step may change hue family. Shift the hue of a step a few degrees toward its neighbor when it does.
7. Check the pairs the jobs promise. The table below lists them.
8. Write each used step as a token value. Use hex, or `oklch()` with plain numbers. Both are valid in the token file.

Pairs the jobs promise. Check each with `DS contrast` and a pairs file.

| Pair | Needs |
| --- | --- |
| Step 11 on steps 1, 2 and 3 | 4.5:1 |
| Step 12 on steps 1 to 5 | 4.5:1 |
| White, or step 1, on steps 9 and 10 | 4.5:1 |
| Step 8 on steps 1 and 2 | 3:1 |
| Steps 6 and 7 on any ground | No requirement; they are decoration |

A light named color. When the brand color is light, such as a yellow at L 0.86, step 9 keeps that lightness. Its label uses step 12, not white. Computed example: dark slate on `#f4ce23` gives 11.28:1; white gives 1.53:1.

Hue drift. A yellow darkened at one hue turns olive. Move its dark steps toward orange. This follows the Design Systems Handbook rule: mix toward a neighboring hue when black makes a color muddy.

## 5. The tinted neutral

A neutral with a trace of the brand hue ties the surfaces to the brand. Pure gray beside a brand color looks cold and unrelated.

1. Use the brand hue, or the ground hue when the ground is colored.
2. Default: chroma 0.003 to 0.008 for light steps, 0.010 to 0.015 for dark steps.
3. Use the same L plan as the ramp recipe. Set step 9 to 0.55, step 11 to 0.46, step 12 to 0.22.
4. Test: place the neutral beside a pure gray of the same lightness. The tint shows in the pair. It does not show alone.
5. A neutral that reads as "a blue page" or "a beige page" has too much chroma. Halve it.
6. Tint borders and shadow colors from the same neutral. Do not use pure black with alpha for shadows on a tinted ground.
7. Secondary text on a colored surface comes from that surface's ramp, never from the neutral ramp.
8. A warm brand word can ask for a warm neutral beside a cool brand hue. That is a decision. Record its reason.

## 6. The dark ramp

Do not reverse the light ramp. Build a second L plan.

| Step | Job | Dark theme L |
| --- | --- | --- |
| 1 | Page ground | 0.17 |
| 2 | Raised surface | 0.20 |
| 3 | Component ground | 0.24 |
| 4 | Hover | 0.27 |
| 5 | Pressed or selected | 0.30 |
| 6 | Subtle border, decoration only | 0.34 |
| 7 | Border, decoration only | 0.40 |
| 8 | Control outline and focus ring | 0.52 |
| 9 | Solid fill | Keep the light-theme value when it still reads as the brand |
| 10 | Solid fill, hover | Step 9 plus 0.04 |
| 11 | Colored text | 0.76 to 0.80 |
| 12 | High-contrast text | 0.93 to 0.95 |

Rules:

1. Default: reduce the chroma of large dark surfaces. Strong color in a dark ground glows.
2. A higher surface is lighter. Each level adds about 0.03 to L.
3. Whether the ground is true black, near black or tinted comes from the design system, then the brief. Do not hard-code it.
4. Step 9 needs 3:1 against the dark ground when it is the only edge of a button. Check it as a control.
5. Hover on a dark theme goes lighter, not darker. Contrast must not fall on a state change.

## 7. Worked ramp

Hull teal, hue 195, peak chroma 0.085. Computed 2026-11-23. All steps are in gamut.

| Step | L | C | Hex |
| --- | --- | --- | --- |
| 1 | 0.99 | 0.006 | `#f7fdfd` |
| 2 | 0.975 | 0.012 | `#eef9f9` |
| 3 | 0.95 | 0.024 | `#ddf4f3` |
| 4 | 0.925 | 0.034 | `#cdeeed` |
| 5 | 0.895 | 0.044 | `#bce6e5` |
| 6 | 0.86 | 0.055 | `#a7dddc` |
| 7 | 0.80 | 0.068 | `#89cccb` |
| 8 | 0.64 | 0.085 | `#429c9c` |
| 9 | 0.52 | 0.085 | `#117878` |
| 10 | 0.48 | 0.080 | `#086b6c` |
| 11 | 0.44 | 0.072 | `#0b5f5f` |
| 12 | 0.24 | 0.040 | `#012525` |

Measured: white on step 9 is 5.28:1. Step 11 on step 1 is 7.29:1. Step 8 on step 1 is 3.15:1, and on step 2 it is 3.02:1. Step 7 on step 1 is 1.77:1, so it is decoration only.

The matching neutral, hue 195:

| Step | Light | Dark |
| --- | --- | --- |
| 1 | `#fafcfc` | `#0b1110` |
| 2 | `#f3f8f8` | `#111717` |
| 3 | `#ebf2f1` | `#1a2121` |
| 6 | `#cdd6d6` | `#313a3a` |
| 8 | `#848f8e` | `#616b6b` |
| 11 | `#4f5b5a` | `#a9b4b3` |
| 12 | `#121d1d` | `#e7ecec` |

Dark colored text for the same hue: `#5ecbcb` at L 0.78. It reaches 9.87:1 on the dark ground.

## 8. Ready scales as a start

A ready scale from the asset catalog can replace steps 1 to 4 of the recipe. Reach it through `find-assets`.

1. A ready scale is a start. Shift its hue, chroma or lightness toward the palette plan.
2. A scale used unchanged is the look of every product that uses it.
3. A scale generated to a contrast target still needs the script on the final tokens.
4. Record the tool and the reason in `design/decisions.md`.

## 9. Wide gamut

1. Default: every token value is in sRGB. That is the value every screen shows.
2. A wider color is an enhancement inside a media query for wide-gamut screens.
3. The sRGB value comes first in the stylesheet. The wide value overrides it.
4. Check contrast on the sRGB value. `ds.py` computes in sRGB.
5. Never rely on a wide-gamut color for a meaning.

## 10. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| HSL ramp | Steps made by changing HSL lightness; yellow looks far lighter than blue at one step | Rebuild in OKLCH |
| Flat chroma | One chroma for all twelve steps; light steps look neon, dark steps look muddy | Follow the chroma shares |
| Clipped chroma | A value outside sRGB, silently clipped; the hue shifts | Reduce chroma until in gamut |
| Mid-gray outline | A control outline lighter than L 0.67 on white | Use step 8 |
| White on light fill | White text on yellow, amber or light orange | Dark text on a light fill |
| Pure gray beside color | Neutral with zero chroma on a tinted brand | Tint the neutral |
| Colored page | A neutral with chroma above 0.02 | Halve the chroma |
| Reversed ramp | The dark theme uses the light ramp upside down | Build the dark L plan |
| Whole ramp in tokens | Twelve steps of five hues as tokens, most unused | Tokens hold used steps only |
