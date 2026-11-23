# Font loading and performance

Read this file at step 13 of `typography`. It covers self-hosting, formats, subsets, preloading, `font-display`, fallback metric overrides, budgets, notes for each medium and the checks.

Evidence. Self-hosting, subsetting, preloading the critical files and setting `font-display` come from the Vercel and Rauno Freiberg guidelines, read 2026-11-23. Capsize as the tool for fallback metrics comes from its README, read the same day. The descriptor names and the browser behavior below are written from memory. The layout shift threshold is recalled, not re-read. Treat each mechanic as UNTESTED until you see it in the network panel and in the rendered page.

Terms. A fallback font is the installed font the browser shows until the web font arrives. The swap is the moment the web font replaces the fallback. Layout shift is content that moves after first paint.

## 1. The loading plan

Write the plan as a table before you add any `@font-face` rule.

| Family | Style | File | Subset | Preload | `font-display` | Fallback with overrides |
| --- | --- | --- | --- | --- | --- | --- |
| Text face | 400 to 700 upright | one variable WOFF2 | Latin, Latin extended | yes | swap | system sans, adjusted |
| Text face | italic | one WOFF2 | Latin | no | swap | same |
| Display face | 700 | one WOFF2 | Latin | only when the first view shows it | swap | condensed system face, adjusted |

Then build from the table. A file that is not in the table does not load.

## 2. Self-host

1. Serve font files from the project's own origin. Default: no font CDN in production.
2. A remote font stylesheet in production is a hotlink. It needs a written exception in the manifest.
3. A subscription library that must deliver its own fonts is such an exception. Record the reason.
4. Use WOFF2. Add no older format unless the brief names an old browser.
5. Keep the license file beside the font files.
6. Serve font files with a long cache lifetime and a versioned file name.
7. Take open families from a self-host package and pin its version. `find-assets` records the package.

## 3. Subset

1. Load only the scripts and languages in the brief.
2. Split by script with `unicode-range`. The browser then fetches a file only when the page uses its characters.
3. Self-host packages ship range subsets. Prefer them to a hand-built subset.
4. Read the license before you subset by hand. A changed build can fall under a reserved font name or a consent rule.
5. Keep the features the design uses: tabular numerals, small caps, fractions, local forms. A careless subset removes them.
6. Test the subset with the hardest real strings. A missing glyph falls back and breaks the word.
7. Do not subset to the exact characters of today's copy. Content changes.

## 4. Preload

1. Preload only the files the first view needs. Default: one or two files.
2. Use a link with `rel="preload"`, `as="font"`, the font type and the `crossorigin` attribute.
3. The `crossorigin` attribute is needed even on the same origin. Without it the browser fetches the file twice.
4. Do not preload every weight. Each preload competes with the page's own content.
5. A preloaded file that the first view does not use is waste. Check the network panel.

## 5. Choose font-display

| Value | Behavior | Use when |
| --- | --- | --- |
| `swap` | Fallback at once, then the web font whenever it arrives | Default for text. Pair it with fallback metric overrides. |
| `optional` | Fallback at once; the web font is used only when it is ready almost immediately | No shift is acceptable, and the brand can live with the fallback on a first visit |
| `fallback` | A very short invisible period, then fallback; a late font is not swapped in | A middle path for long reading pages |
| `block` | Invisible text for a few seconds | Avoid for text |

Rules:

1. Text is visible at first paint. Never hide text while a font loads.
2. `swap` with no metric overrides moves lines. Add the overrides.
3. Do not use an icon font. Use SVG icons.

## 6. Fallback metric overrides

The goal: the fallback occupies the same space as the web font, so the swap moves nothing.

1. Pick a fallback that is installed on each major operating system and has a similar width.
2. Declare a second `@font-face` rule that names the local fallback under a new family name.
3. In that rule, set `size-adjust`, `ascent-override`, `descent-override` and `line-gap-override`.
4. Compute the four values from the metrics of both fonts. A font metrics tool from the asset catalog does this.
5. Put the adjusted fallback after the web font in the stack.
6. Compare the fallback render and the final render at three widths. No line may rewrap.

The shape of the rule. The numbers are placeholders. Compute your own.

```css
@font-face {
  font-family: "Text Fallback";
  src: local("Arial");
  size-adjust: 104%;
  ascent-override: 92%;
  descent-override: 24%;
  line-gap-override: 0%;
}
body { font-family: "Text Face", "Text Fallback", sans-serif; }
```

Notes:

- Each web font needs its own adjusted fallback. A display face and a text face differ.
- A condensed display face has no close system match. Reserve the height of the heading block, or use `optional`.
- Some frameworks generate these rules from the font file. Use that feature when the project has it. Then verify the result.
- A system font stack by classification is a good unadjusted last fallback.

## 7. Budgets

These are defaults with no primary source. Replace them with the project's own budget when one exists.

- Default: two families and four font files at most on the first view.
- Default: 150 KB of fonts at most on the first view for a Latin site.
- Default: the font swap moves no line of text. Layout shift stays at 0.1 or under.
- Default: one variable file in place of three or more static weights.

When the design breaks the budget, cut in this order: unused weights, the italic of the display face, the second family.

## 8. Notes by medium

| Medium | Rule |
| --- | --- |
| Web app with a framework | Use the framework's font module when it self-hosts and generates fallbacks. Check its output. |
| Native app | Bundle the files. The license must allow app embedding. Support the system text size setting. |
| Claude Design canvas | One font stylesheet link is the only network access. Brand font files come through an installed design system. |
| Claude Slides deck | The format caps the number of faces. An export may drop a face whose license reserves the name. Test one export. |
| Email | Web fonts are unreliable. Design for the system stack. |
| Print and PDF | Embed or outline the fonts. Check that the license allows embedding. |
| Video | Text is rendered into frames. The license must allow that use. |
| Chart inside an SVG | A web font may not load inside an image. Set chart labels as page text, or outline them. |

Evidence for this table: the artifact rows come from the artifact type rules read 2026-11-23. The other rows are from memory.

## 9. Checks

Run these on the rendered page. Label each result VERIFIED or UNTESTED.

1. The network panel lists only the files in the loading plan.
2. No font request goes to another origin, except a written exception.
3. The computed font of the body and of a heading is the web font, not the fallback. In the browser console, `document.fonts.check` returns true for each style in use.
4. Load the page with a slow network profile. Text is readable before the font arrives.
5. Compare a screenshot before the swap with one after it. No heading rewraps. No block moves.
6. Italic and bold text use real files. Nothing is synthesized.
7. Tabular numerals still work after subsetting.
8. Zoom to 200%. No text is clipped.
9. Each font file has a manifest record and a license file beside it.

## 10. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| CDN left in | A request to a font host in production | Self-host, or write the exception |
| Weight pile | Eight files load, three are used | Load what the scale uses |
| Jumping headline | The heading rewraps when the font arrives | Add an adjusted fallback or reserve the space |
| Invisible text | A blank page region for seconds on a slow network | Set `font-display` |
| Double fetch | The preloaded font downloads twice | Add `crossorigin` to the preload |
| Stripped features | Numbers stop aligning after a subset | Keep the features in the subset |
| Fallback as final | The brand face never loads and nobody notices | Check the computed font |
| Preload everything | Six preload links | Preload the first view only |
