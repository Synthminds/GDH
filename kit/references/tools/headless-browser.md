# Local headless browser

Catalog entry: [headless-browser.json](../../catalogs/tools/headless-browser.json). Source: https://playwright.dev/docs/cli

Terms in this card. A capture is one screenshot file of one page at one width and one theme. The view matrix is the list of widths and themes that a skill names for its rendered review. A full-page capture records the whole scroll height, not only the window.

## What it makes

- PNG captures of a local HTML file or a local dev server, at any width, in light and dark color schemes.
- Full-page captures for a design review, a critique report and a before-and-after pair.
- It does not judge the design. `design-critique` and `accessibility-gate` read the captures.

## Connection and auth

- No account and no connector. It runs on the user's machine.
- Route one: Playwright through `npx`. Install the browser once with `npx playwright install chromium`.
- Route two: a Chrome or Chromium binary that is already installed. It needs no download.
- Confirm a route before the review: `npx playwright --version` or `google-chrome --version`.

## Cost model

Free. It makes no spend call. A first Playwright install downloads a browser build; ask the user before that download.

## Call order

1. Confirm a browser is present.
2. Serve the page from a file URL or a local server. Never capture a page on a public host without the user's yes.
3. Capture each width and each theme of the view matrix.
4. Save the files under `design/reviews/<date>-<scope>/`.
5. Open each capture and review it. A capture that nobody looked at proves nothing.

## Key tools

Full page, one width, one color scheme, with Playwright:

```
npx playwright screenshot --browser chromium --full-page --viewport-size "390,844" --color-scheme dark "file:///abs/path/index.html" design/reviews/2026-11-23-home/390-dark.png
```

The same for each width of the matrix. Default widths: 390, 768, 1024 and 1440 px. Repeat with `--color-scheme light`.

Window-height capture with Chrome:

```
google-chrome --headless=new --hide-scrollbars --window-size=1440,2400 --screenshot=design/reviews/2026-11-23-home/1440-light.png "file:///abs/path/index.html"
```

Set the window height to the page height for a full capture. Chrome has no full-page flag.

A page that sets its theme with `data-theme` on the root ignores the color-scheme flag. Give the page a query parameter that sets the attribute, or capture through a small Playwright script that sets it before the shot.

## Inputs

- A local file path or a local server address.
- The view matrix from the skill: widths and themes.
- Fonts present on the machine or loaded by the page. A missing font changes the capture.

## Outputs and how to bring them into a project

- PNG files. Keep them under `design/reviews/` beside the report that cites them.
- Name each file `<width>-<theme>.png`.
- Captures of the user's own work need no provenance record. A capture of an outside site is a reference: it stays in the mood board and never ships.

## Handoffs

- In: any HTML that the project builds.
- Out: files for `design-critique`, `accessibility-gate`, `refine-round` and the handoff report.

## Limits and failure modes

1. A sandboxed container may need `--no-sandbox` for Chrome. Use it only on a local, trusted page.
2. Web fonts from a remote host do not load offline. Ship the font files or accept a fallback face and label it.
3. Animations captured mid-run show a half state. Set reduced motion or wait for the end state.
4. A capture shows layout and color. It does not test keyboard use, focus order or a screen reader.
5. A page that needs sign-in shows the sign-in screen. Serve a local build with sample data instead.

## Best for

1. The rendered review that kernel rule 14 asks for on a coded deliverable.
2. Before-and-after pairs in a refinement round.
3. Specimen captures for a design system.

## Wrong for

An artifact type with its own check rule. Follow that type's rule instead. A hosted design canvas shows its own preview.

## Evidence

VERIFIED on 2026-11-23: Playwright 1.63 wrote a full-page dark capture at 390 px of the example brand specimen. Chrome wrote 390 px and 1440 px captures of the same file. All runs were local, with no network. UNTESTED: a local dev server, a page with remote fonts, and the `data-theme` script route.
