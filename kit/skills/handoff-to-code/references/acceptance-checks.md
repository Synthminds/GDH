# Acceptance checks a coding agent can run

Read this file at step 12 of `handoff-to-code`. It turns the design gates into checks with a pass condition and a way to run each, so the builder can prove the build without asking the designer.

Evidence. The script commands were run on 2026-11-23: VERIFIED for the scripts. The browser methods are standard practice and were not run for this kit: UNTESTED. The contrast floors are the WCAG 2.2 AA values the kernel uses: DOCUMENTED. Every other number is a default.

Terms. A check is one test with a pass condition. A method is how to run it: a command, or a short manual walk with a recorded result. A check with no method is a wish.

## 1. How to write a check

| Field | Rule |
| --- | --- |
| Check | A short name |
| Pass condition | Observable and exact: a count, a ratio, a yes for every item |
| How to run | A command, or numbered manual steps |
| Evidence | What the builder records: output file, captures, a list |
| Gate or default | Gate blocks release; default can be changed by the owner |

Turn each gate of the discipline skills into one row. Remove a check you cannot give a method, or give it one.

## 2. The standard set

`DS`, `A` and `T` are the scripts named in [package.md](package.md), section 2. `<src>` is the built source folder.

| # | Check | Pass condition | How to run | Class |
| --- | --- | --- | --- | --- |
| 1 | Tokens only | No raw color, size or duration in the built source | `$DS audit <src> --tokens design/tokens.json`; exit 0 | Gate |
| 2 | Tokens current | `tokens.css` equals the export of `tokens.json` | Re-run `$DS export design/tokens.json --css /tmp/t.css`; diff with `design/tokens.css` | Gate |
| 3 | Contrast | Every pair passes in every theme | `$DS contrast design/tokens.json`; exit 0 | Gate |
| 4 | Assets recorded | Every shipped file has a record and a matching hash; no reference file ships; no unrecorded remote asset URL | `$A check design/assets/manifest.json --root . --scan <src>`; exit 0 | Gate |
| 5 | No generic tells outside the brand | Zero high findings that are not brand-required | `$T <src> --tokens design/tokens.json --design DESIGN.md` | Default |
| 6 | No placeholder copy | Zero lorem ipsum; every bracketed placeholder is listed in section 9 | Search `<src>` for "lorem" and for `[` placeholders; compare with section 9 | Gate |
| 7 | Copy matches the deck | Each key in section 4.4 renders its text | Search `<src>` for each key or text; list misses | Gate |
| 8 | States reachable | Each `designed` cell of the state matrix can be reached and matches its reference | A state page, a story per state, or a test fixture per state; capture each | Gate |
| 9 | Keyboard | The primary flow completes by keyboard alone; focus is visible at every step; order matches reading order | Walk the flow with Tab, Shift+Tab, Enter, Space, Escape; record the tab order | Gate |
| 10 | Focus outline | Focus indicators reach 3:1 against their ground | Measure the focus color pair with `$DS contrast --pairs` | Gate |
| 11 | Layout at widths | No sideways page scroll; each region follows its rule | Capture at 320, 390, 768, 1024, 1440 px | Gate for the scroll; default for the widths |
| 12 | Zoom | Nothing clips or overlaps at 200% text zoom | Zoom the browser to 200%; capture | Gate |
| 13 | Reduced motion | No movement beyond the variant in section 5 | Turn on the reduced-motion setting, or emulate it in the test browser; walk the flow | Gate |
| 14 | Motion tokens | Every duration and easing in code names a token | Covered by check 1; list exceptions with their reason | Gate |
| 15 | Non-visual signal | Each motion row's equivalent exists in markup | Inspect the element after the trigger: state attribute or live region present | Gate |
| 16 | Targets | Each target meets the size for its input | Measure in the rendered page | Default: 24 px pointer, 44 px touch |
| 17 | Color not alone | Status reads in greyscale | Capture with a greyscale filter; each status has a word or an icon | Gate |
| 18 | Images and names | Every meaningful image has alternative text; every control has a name | Inspect the accessibility tree or run an automated checker | Gate |
| 19 | Charts with real data | Each chart reads with real, flat, empty and extreme data | Feed four fixtures; capture each | Gate for dashboards |
| 20 | AI states | Waiting, fast, slow, limited and failed exist for each AI entry point | A throttled mock and a fast mock; a limit fixture; a failure fixture | Gate when in scope |

When GCH is loaded, its `ux-laws` numbers replace the defaults in rows 11 and 16. Its screen-state rule sets the minimum for row 8.

## 3. Captures

1. Capture with any `capture` tool from the catalog, or with GCH's `browser-lane` skill when installed.
2. Name captures `<screen>-<state>-<width>-<theme>.png`.
3. Store them where the coding harness keeps evidence. Link the folder in section 10.
4. With no capture tool, ask the user for screenshots. Mark what nobody saw UNTESTED.

## 4. Reporting

The builder reports each check as one line:

```
#3 Contrast: PASS. ds.py contrast, 11 pairs, 22 checks, 0 failed. Output: design/reviews/2026-12-02-checks.md
#9 Keyboard: FAIL. Focus lost after the sheet closes. Capture: calendar-sheet-close-390-light.png
#13 Reduced motion: UNTESTED. Emulation not available in the test browser.
```

A FAIL on a gate stops release until fixed or accepted as a recorded exception by the owner.

## 5. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Wish list | "Looks right on mobile" | A width, a capture and a pass condition |
| Script without exit | Output pasted with no pass or fail | Read the exit code; state PASS or FAIL |
| Checks after release | Checks written once the build ships | Write them in the package, before the build |
| Silent waiver | A failed gate marked "fine" | Owner's recorded exception, or fix |
