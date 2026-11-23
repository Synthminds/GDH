# Contrast gates and color-blind safety

Read this file at steps 10 and 11 of `color`. It covers the contrast gate, how to run the script, the pairs file, how to fix a failing pair, the special cases, APCA as advice, the color-blind procedure and the failure patterns.

Evidence. The ratios 4.5:1 and 3:1 are the GDH kernel floor. They also appear in the Impeccable craft floor and the Claude Design craft rules, read 2026-11-23. The large-text definition follows WCAG. The script behavior was exercised on 2026-11-23: usage-note pairs, a pairs file, alpha foregrounds and `oklch()` values. The APCA targets come from "APCA in a Nutshell", read the same day. "Prefer blue against orange" and "meaning colors also differ in lightness" come from the Claude Design craft rules. The share of people with a color vision deficiency and the Okabe-Ito values are recalled from memory. The Okabe-Ito ratios in this file were computed.

Terms. A pair is one foreground on one ground. A ground is the color under a text or a control. Normal text is text under 24px, or under 18.66px when bold. Large text is that size or more.

## 1. The gate

| What | Ratio | Kind in the script |
| --- | --- | --- |
| Normal text on its ground | 4.5:1 | `text` |
| Large text on its ground | 3:1 | `large` |
| Control outlines, focus rings, icons that carry meaning, chart marks that must be told apart | 3:1 against what is beside them | `ui` |

The gate holds in every theme. It holds for every state: hover, pressed, focus, selected.

Not held to a ratio: decoration, a disabled control, a logo. These exemptions are recalled from WCAG and not re-read. Such an element still must not carry meaning alone.

## 2. Run the script

`DS` means `python3 ../design-system/scripts/ds.py` from the skill folder.

```
DS validate design/tokens.json
DS contrast design/tokens.json
DS contrast design/tokens.json --pairs design/reviews/pairs.txt
DS contrast design/tokens.json --json
```

1. Run `validate` first. A token that does not parse cannot be checked.
2. `contrast` with no pairs file reads pairs from usage notes. "Text on bg and surface." makes two pairs.
3. Each pair is checked in each theme.
4. Exit code 0 means every pair passes. Exit code 1 means a pair fails or no pair was found.
5. "No pairs found" is not a pass. Write the usage notes or pass a pairs file.
6. Save the output in `design/reviews/<date>-color.md`. That is the evidence.

Read one output line:

```
PASS  dark     accent-text on bg  9.87:1  needs 4.5:1 (text)  normal text pass, large text pass
```

Theme, pair, measured ratio, required ratio, kind, and what the pair could carry.

## 3. The pairs file

Use a pairs file for pairs that usage notes cannot express.

One pair on each line: `<foreground> on <ground> [text|large|ui]`. The kind is `text` when left out. A name is a token name or a color literal. Write a literal with no spaces.

```
text on accent-subtle
on-accent on accent-hover
#ffffff on #0b5f5f large
focus on surface ui
```

A JSON file may limit a pair to themes:

```json
[{"fg": "danger-text", "bg": "danger-subtle", "kind": "text", "themes": ["dark"]}]
```

Put these in the file every time:

- every label on every state of a fill
- every text role on every tinted ground
- the weakest point of a gradient or an image under text, as a literal
- chart marks against the chart ground

## 4. Fix a failing pair

Work in this order. Stop at the first step that passes.

1. Move the lightness of the foreground. Hold hue and chroma.
2. Move the lightness of the ground, when the foreground is fixed.
3. Reduce chroma when the color leaves sRGB at the new lightness.
4. Change the pairing: use dark text on a light fill in place of white.
5. Add a role: keep the brand color as a fill and add a darker role for text.
6. Add a backing: a solid chip or a scrim under text on an image.

Never fix a pair by changing a fixed brand color. Never fix it by making the text larger only to reach the 3:1 class, unless the design wants large text there.

A fixed pair that fails:

1. Keep the value exact.
2. Flag it in the usage note: "Fails 4.5:1 on bg (2.6:1). Use only for large display text."
3. List it in the report under "Kept exact and flagged".
4. Give the builder a passing role for the same job.
5. ASK when the brand requires the failing pair for body text. The gate does not yield in silence.

Planning shortcuts, computed 2026-11-23:

- White text needs a fill at OKLCH lightness 0.55 or lower.
- A control outline on white needs lightness 0.67 or lower.
- On a dark ground near lightness 0.19, text needs lightness 0.60 or higher for 4.5:1.

## 5. Special cases

| Case | Rule |
| --- | --- |
| Semi-transparent foreground | The script composites it over the ground. Check it on each ground it meets. |
| Semi-transparent ground | The script refuses it. The ratio depends on what lies under it. Check the composited literal. |
| Text on a gradient | Check against the stop with the least contrast. Add both ends to the pairs file as literals. |
| Text on a photo | Add a scrim or a solid backing. Check the text against the backing. |
| Placeholder text | It is text. It meets 4.5:1. |
| Link inside body text | It meets 4.5:1 on the ground. It also has an underline, or another cue that is not color. |
| Focus ring | 3:1 against the ground beside it. On a filled button, check it against the page ground. |
| Icon with a text label | The label carries the meaning. The icon needs no ratio. |
| Icon alone | 3:1, and an accessible name. |
| Selected item | The selection has a second cue. The text on the selected ground meets 4.5:1. |
| Print | Ratios are a screen measure. For print, also check a grayscale proof. |

## 6. APCA as advice

APCA is a newer contrast method. It is not part of WCAG 2.2. Treat it as advice. Never report it as conformance.

Its published targets, in Lc units: 90 preferred and 75 minimum for body text; 60 for other content text; 45 for headlines and fine icons; 30 for placeholder and disabled text; 15 for dividers.

Use it in two places:

1. A dark theme. A pair can pass the ratio and still read poorly. Check dark body text with an APCA tool and aim for Lc 75 or more.
2. Thin or small text. APCA accounts for weight and size.

`ds.py` does not compute APCA. Use a tool from the asset catalog. Label the result as advice in the report.

## 7. Color-blind procedure

Default: assume that some users cannot tell red from green. The share recalled from memory is about 1 in 12 men.

1. List every place where color carries meaning: status, chart series, links in text, required fields, selected states, map legends, diff views, form errors.
2. Give each meaning a second cue. Use an icon, a label, a shape, a pattern, a position or an underline.
3. Make meaning colors differ in lightness. Default: a difference of 0.15 in OKLCH lightness or more between two colors that must be told apart.
4. Prefer blue against orange to red against green for an opposing pair.
5. Simulate three deficiencies on a real screen: deuteranopia, protanopia and tritanopia. Use the agent route below, a simulator in the browser's developer tools, or a design tool.
6. Convert the screen to grayscale. Every meaning is still readable.
7. Fix what merges. Change lightness first, then hue.
8. Write the result in the review file. VERIFIED means you viewed the simulation. Otherwise write UNTESTED.

Agent route, through the `capture` capability (example card: `headless-browser`). Chromium can emulate a vision deficiency through its DevTools protocol command `Emulation.setEmulatedVisionDeficiency`. Its types include `deuteranopia`, `protanopia`, `tritanopia` and `achromatopsia`. Evidence: DOCUMENTED from the protocol reference; this kit has not run it.

1. Open the page in a small Playwright script with Chromium.
2. Open a DevTools session on the page. Send the command with one type.
3. Capture the full page at one width. Save it as `design/reviews/<date>-cvd/<type>.png`.
4. Repeat for each type, and once with `achromatopsia` for the grayscale check.
5. View each capture. Compare each meaning from step 1 across the captures.
6. Write one line for each meaning: the pair, each type, merged or distinct, and the second cue.

With no capture route, ask the user for screenshots from the browser's own emulation. Until then the result is UNTESTED.

Starting set with no brand hues to keep: the Okabe-Ito set. The Claude Design System craft rules name it for color-blind-safe status colors. The hex values below are recalled from memory.

| Color | Hex | On white | On a dark ground `#0b1110` |
| --- | --- | --- | --- |
| Orange | `#E69F00` | 2.25:1 | 8.46:1 |
| Sky blue | `#56B4E9` | 2.31:1 | 8.26:1 |
| Bluish green | `#009E73` | 3.42:1 | 5.57:1 |
| Yellow | `#F0E442` | 1.32:1 | 14.41:1 |
| Blue | `#0072B2` | 5.19:1 | 3.68:1 |
| Vermilion | `#D55E00` | 3.87:1 | 4.93:1 |
| Reddish purple | `#CC79A7` | 3.06:1 | 6.23:1 |

Read the computed ratios before you use the set:

- On white, orange, sky blue and yellow fall under 3:1. As status marks they need an outline, a label or a darker step.
- On a dark ground, every color except blue passes 4.5:1.
- The set separates hues. It does not make them pass contrast. Run the script on the roles you derive.

## 8. Checks

1. The script output is saved and shows zero failures.
2. The pairs file covers states, tinted grounds and gradient ends.
3. Every flagged brand pair is in the report.
4. Every meaning has a second cue. List each meaning and its cue.
5. The simulation was viewed, or the report says UNTESTED.
6. The grayscale view keeps every meaning.

## 9. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| No pairs | The script found nothing and the result was read as a pass | Write usage notes or a pairs file |
| Happy path only | Only text on the page ground was checked | Add states, tinted grounds and gradient ends |
| Light theme only | Dark pairs never checked | The script checks every theme; fill every theme |
| Gray on color | Muted gray text on a colored fill | Tint the text from the fill's ramp; check the pair |
| White on yellow | White label on a light fill | Dark label |
| Hue fix | A failing brand color shifted in hue to pass | Restore it. Add a role for text. |
| Red means error | A red outline with no icon or message | Add the second cue |
| Simulation claimed | "Color-blind safe" with no simulation viewed | Run it, or write UNTESTED |
| APCA as law | An Lc value reported as conformance | Report the WCAG ratio. Add APCA as advice. |
| Tooltip-only meaning | The legend lives in a hover state | Label directly |
