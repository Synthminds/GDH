# Deliverables

Read this file at step 15 of `logo-identity`. It covers the file set, the naming pattern, SVG cleaning, the favicon and the app icon, and the manifest records.

Evidence. The file set and the icon sizes are common practice, written from memory. Each size is a default. Confirm the icon sizes against the current platform guidance before release.

## 1. The folder

```
design/assets/logo/
  source/      the master vector file and the working file
  svg/         one SVG for each lockup and color version
  png/         raster exports at fixed widths
  favicon/     the browser icon set
  app-icon/    the app icon masters and exports
```

The master is one vector file. Every other file is an export from it. Never edit an export by hand.

## 2. Naming pattern

```
<brand>-<lockup>-<color>[-<width>].<ext>
```

| Part | Values |
| --- | --- |
| `brand` | The brand slug in kebab-case. |
| `lockup` | `primary`, `stacked`, `mark`, `wordmark`. |
| `color` | `color`, `black`, `white`, `mono-<token>`. |
| `width` | The pixel width of a raster export, for example `512`. |

Examples: `harbor-lantern-primary-color.svg`, `harbor-lantern-mark-white-512.png`.

Use lowercase and hyphens only. Do not put a version number in the name. The decision record holds the history.

## 3. The file set

| Lockup | SVG | PNG widths (default) | Versions |
| --- | --- | --- | --- |
| primary | yes | 512, 1024, 2048 | color, black, white |
| stacked | yes | 512, 1024, 2048 | color, black, white |
| mark | yes | 64, 256, 512, 1024 | color, black, white |
| wordmark | yes | 512, 1024 | black, white |

- Export each PNG with a transparent ground.
- Export print files only on request. Ask the printer for the color profile and the format first.
- Deliver the white version on a dark preview, so that a person can see it.

## 4. SVG cleaning

Do each step on a copy of the export, then compare the render with the master.

1. Convert all text to outlines. A wordmark must not depend on an installed font.
2. Expand strokes to fills when the stroke weight is part of the shape.
3. Merge overlapping shapes of one color. Remove hidden layers and empty groups.
4. Remove editor metadata, comments and unused definitions.
5. Set a `viewBox`. Remove fixed `width` and `height`, so that the file scales.
6. Fit the artboard to the lockup plus its clear space, or to the shape alone. State which in the usage sheet.
7. Use plain fills. Reference a gradient only in the color version, never in the black or white version.
8. Add a `title` element with the brand name for a standalone file.
9. Round coordinates to two decimals. Check that curves did not change.
10. Open the file in a browser at 16 px and at 1024 px. Compare both with the master.

Check: the file holds no raster image, no font reference, no script and no outside link.

## 5. Favicon set

Default set. Build it from the mark, not from the full lockup.

| File | Size | Note |
| --- | --- | --- |
| `icon.svg` | vector | May adapt to light and dark with a media query inside the file. |
| `favicon.ico` | 32 px | For older browsers. |
| `apple-touch-icon.png` | 180 px | Opaque ground. Some platforms round the corners. |
| `icon-192.png`, `icon-512.png` | 192 px, 512 px | For a web app manifest. |
| `icon-maskable-512.png` | 512 px | Keep the mark inside the central safe zone. Default: the inner 80 percent. |

- Redraw the mark for 16 px when detail closes up. Simplify, do not shrink.
- Test the icon on a light tab bar and on a dark one.

## 6. App icon

1. Read the current platform guidance for sizes, shapes and layers. Do not rely on memory for these.
2. Build one master at the largest size the platform asks for. Default: 1024 px, square, opaque.
3. Do not draw the corner radius. The platform applies its own mask.
4. Keep the mark inside the safe zone the platform states.
5. Do not put the wordmark in an app icon, unless the brand is a wordmark only.
6. Check the icon at the smallest size the platform shows, beside real icons from the category.

## 7. Manifest records

Write one record in `design/assets/manifest.json` for each delivered file.

| Field | Value for a logo file |
| --- | --- |
| `id` | The file name without the extension. |
| `sourceUrl` | `own` for work drawn in the project. The tool name for a generated concept that was redrawn. |
| `license` | `owned by <client>` when the mark is original. The typeface license id for a wordmark face. |
| `attribution` | `none`, or the text a license requires. |
| `date`, `path`, `sha256` | The export date, the path and the hash of the file. |

Set the origin to `own`. The record script accepts `outside`, `own` and `generated`. For a concept that a generator made and a person redrew, the delivered vector is `own`, and the note says "redrawn from a generated concept (<tool>)". A generated raster never ships as a logo file.

## 8. Closing check

- Every lockup in the usage sheet has its files.
- Every file opens, and its name follows the pattern.
- The black version holds one fill color.
- The manifest holds one record for each file, and each hash matches.
