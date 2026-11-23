# Fetch and record

Read this file at step 13 of `find-assets`. It covers how an asset enters the project, what the manifest holds, how `assets.py` checks it and how credits are written. Fetch only after the license verdict is `clear` or `clear with duties`.

`A` means `python3 <skill folder>/scripts/assets.py`. The script makes no network call. It never downloads. You fetch with the host's tools.

## Fetch routes

| Route | Use it for | What lands in the project | Record |
| --- | --- | --- | --- |
| Registry add | A copy-in component from a component registry | Source files, and often new dependencies | Each file, plus each new design dependency as a package |
| Package install | An icon set, a font package, an animation or chart library | A dependency at one version | `--package <name>@<version>` |
| Direct download | A photo, a video, an illustration, a font file, a model, an HDRI | One file or one archive | Each file that ships |
| Connector fetch | An item from a connected library | Text or a file that the tool returns | Each file you save |
| User download | An asset whose license binds the account that downloads it | A file the user or the client places | The file, with a note on who holds the license |

### Registry add

1. Read the item's source and its license before you run the command. A registry item is third-party code.
2. Run the registry's add command from the catalog `fetch` line or from the tool card. The usual form is the component CLI with the registry name and the item name.
3. Read the diff: new files, changed files, new dependencies.
4. Keep any copyright header in the files.
5. Record the files with one `record` call. Pass `--file` for each file.
6. Record each new dependency that carries design material with `--package`.
7. Restyle the component with project tokens before the first review.

A command that embeds an account key reads the key from an environment variable. Never write a key into a file.

### Package install

1. Install one exact version. Do not use a range or a `latest` tag in the manifest.
2. Read the license file inside the installed package. Compare it with what you read on the source.
3. Record with `--package <name>@<version>`. No file hash exists for a package: the lockfile holds it.
4. Record again with `--replace` when the version changes, after you read the license of the new version.

### Direct download

1. Download from the item's own page, into a scratch folder first.
2. Confirm the file type and size. A file that is not what the page describes stops the fetch.
3. Optimize: compress images, clean SVG, compress models, convert fonts to a web format when the license allows changes.
4. Move the result into the project asset folder.
5. Record the file that ships, not the file you downloaded. The hash must match what is on disk.
6. Keep a license file beside the asset when one ships with it. Fonts under an open font license need it.

### Connector fetch

1. Confirm the item's license in the tool's item record before you fetch the file.
2. GATE: a metered fetch needs the quote and a yes. Call once.
3. Save returned text as a file. Keep its license header.
4. A signed download link expires. Download at once.
5. Record the source as the item's page URL, not the tool name alone.

### User download

Some licenses bind the person who downloads: a foundry's free font license, a subscription font library, paid stock. The agent does not download these on the user's behalf.

1. Tell the user what to download and from which page.
2. The user places the file or activates the service.
3. Record the file with a note: `License held by <client>; downloaded by the client on <date>.`
4. In a public repository, keep such a file out of version control when its license forbids redistribution.

## Never hotlink

Download the asset and serve it from the project. Do not load it from someone else's URL.

- The remote file can change or disappear.
- A remote load tells a third party about every visitor.
- Several source terms forbid embedding or re-hosting without consent.

Exceptions need a written reason in the manifest. Two cases are known: a vendor whose terms require its own delivery, and a map tile service with its own terms.

```json
"hotlinkExceptions": [
  {"prefix": "https://use.typekit.net/", "reason": "The font vendor's terms forbid self-hosting. The client holds the subscription."}
]
```

`A check <manifest> --root . --scan src` reports each remote asset URL and each font host URL in source files. A URL that starts with an exception prefix passes. An exception with no reason is itself a finding.

## Where files go

Follow the project's own structure first. Default, when the project has none:

| Kind | Folder |
| --- | --- |
| Fonts | `public/fonts/<family>/`, with the license file |
| Images and video | `public/img/`, `public/video/` |
| 3D models and HDRIs | `public/models/`, `public/hdri/` |
| Icons kept as files | `src/assets/icons/` |
| Design-side sources: vector masters, layered files | `design/assets/` |
| References and captures | `design/directions/` only. Never an asset folder. |

`check` looks in `design/assets`, `public`, `static`, `assets` and `src/assets` when they exist. Pass `--asset-dir` for each folder when the project differs.

## The manifest

The file is `design/assets/manifest.json`. `record` creates it in the template shape when it is absent.

| Field | Required | Holds |
| --- | --- | --- |
| `id` | yes | Kebab-case, unique. Use `<source>-<asset>`, for example `polyhaven-studio-small-09`. |
| `sourceUrl` | yes | The page of that exact item. For an asset the project made: a short origin text. |
| `license` | yes | License name and the URL of the text you read |
| `attribution` | yes | The exact credit line, or `none required` |
| `date` | yes | The day you read the license, `YYYY-MM-DD` |
| `path` and `sha256` | for a file | Path inside the project, and the hash of the file |
| `package` | for a dependency | `name@version`, in place of `path` and `sha256` |
| `licenseUrl` | no | The license URL alone |
| `catalogId` | no | The catalog entry the asset came from |
| `origin` | no | `outside` (the default), `own` or `generated` |
| `modified` | no | `true` when the project changed the file |
| `note` | no | Duties and limits that still apply |

Two optional lists sit beside `assets`: `ignore` (glob patterns that `check` skips) and `hotlinkExceptions`.

### Commands

One file from outside:

```
A record design/assets/manifest.json --id polyhaven-studio-small-09 \
  --source-url https://polyhaven.com/a/studio_small_09 \
  --license "CC0-1.0, https://polyhaven.com/license" \
  --attribution "none required" --catalog-id poly-haven \
  --file public/hdri/studio_small_09_2k.hdr --date 2026-11-23
```

Several files of one asset. The ids become `brand-serif`, `brand-serif-2`, `brand-serif-3`:

```
A record design/assets/manifest.json --id brand-serif --source-url <family page> \
  --license "OFL-1.1, <license URL>" --attribution "none required" \
  --file public/fonts/serif/regular.woff2 --file public/fonts/serif/italic.woff2 \
  --file public/fonts/serif/bold.woff2 --date 2026-11-23
```

A dependency:

```
A record design/assets/manifest.json --id icons-package --source-url <repository URL> \
  --license "<name>, <license file URL>" --attribution "none required" \
  --package <name>@<exact version> --date 2026-11-23
```

A file the project made, and a file a generator made:

```
A record design/assets/manifest.json --id empty-state-diagram --origin own \
  --source-url "project: drawn in code from tokens, round 3" \
  --license "owned by the client" --attribution "none required" \
  --file src/assets/empty-state.svg --date 2026-11-23

A record design/assets/manifest.json --id hero-render --origin generated \
  --source-url "<tool name>, job <reference>" --license "<output terms>, <terms URL>" \
  --attribution "none required" --file public/img/hero.webp --date 2026-11-23
```

An asset you changed after the first record:

```
A record design/assets/manifest.json --id polyhaven-studio-small-09 ... --replace --modified \
  --note "Tone-mapped and resized to 2k."
```

Rules:

- `record` refuses a second entry with the same id or the same file. Use `--replace` to update an entry.
- `record` refuses a file outside the project folder. Copy it in first.
- `--date` is the day the license was read, not the day of the commit.
- The project folder is the folder above `design/assets`. Pass `--root` when the manifest sits elsewhere.

## Check codes

`A check design/assets/manifest.json --root .` exits 0 only with zero findings.

| Code | Meaning | Fix |
| --- | --- | --- |
| `MANIFEST_INVALID` | The manifest is absent, does not parse, or has no `assets` list | Copy the template, then record again |
| `MANIFEST_EXCEPTION` | A hotlink exception has no prefix or no reason | State the vendor rule that forbids self-hosting |
| `ENTRY_FIELD` | An entry lacks an id, a source, a license, an attribution, a date, or a file and hash | Read the license. Record the asset with every field. |
| `ENTRY_ID` | An id is not kebab-case | Rename it |
| `ENTRY_DUPLICATE_ID` | Two entries share one id | Give each entry its own id |
| `ENTRY_DUPLICATE_PATH` | Two entries record one file | Keep one |
| `ENTRY_DATE` | The date is not a real date | Write the day the license was read |
| `ENTRY_SOURCE` | An outside asset has a source that is not a URL | Record the item page |
| `ENTRY_ORIGIN` | The origin is not `outside`, `own` or `generated` | Correct it |
| `ENTRY_PATH` | A path is absolute or leaves the project | Copy the file in and record it again |
| `FILE_MISSING` | An entry names a file that is gone | Restore the file or remove the entry |
| `FILE_HASH` | The file differs from its recorded hash | Confirm the source and the license still hold. Record with `--replace`. |
| `FILE_UNRECORDED` | A file in an asset folder has no entry | Find its origin and record it. With no origin, replace it. |
| `REFERENCE_SHIPPED` | A file in an asset folder is a copy of a file under `design/directions/` | Remove the copy. Source the asset through the license decision. |
| `HOTLINK` | A source file loads an asset from a remote URL (only with `--scan`) | Self-host it, or add an exception with a reason |

`check` reads file types that carry design material: images, fonts, video, audio, 3D, animation files. Pass `--all-files` to check every file in the asset folders.

A `FILE_UNRECORDED` file with no known origin is the hard case. Do not invent a record. Ask the user where it came from. When nobody knows, treat it as unlicensed and replace it.

## Credits

`A notices design/assets/manifest.json -o ATTRIBUTION.md` writes three sections: credits that are due, other outside and generated assets, and assets the project made. Do not edit the file by hand. Record, then run the command again.

A notices file is often not enough:

- When a license asks for a visible credit, place it where the license says: a footer, a credits page, a caption.
- Keep the license file beside each font.
- Default: give a credit line in `ATTRIBUTION.md` even when none is required. It costs nothing and keeps the origin findable.
- Say in the credit when the project changed the asset.

## Reference versus ship

| Test | Reference | Ship asset |
| --- | --- | --- |
| Where is the file? | Under `design/directions/` | In an asset folder |
| Was its license read? | Not needed to look at it | Yes, before the fetch |
| Is there a manifest entry? | No. A URL and a lesson in the direction notes. | Yes, with a hash |
| Can the product load it? | Never | Yes |

Rules:

1. A reference is never copied, moved or re-exported into an asset folder.
2. To ship something first seen as a reference, find its maker's page and run the license decision from the start.
3. A screenshot of someone's product is a reference for ever. It has no license route.
4. Keep reference images out of a public repository. Add the capture folders to the ignore file.
5. `check` compares file hashes. It catches an exact copy. It does not catch a redrawn or resized copy: that is the originality check in `reverse-engineer-reference`.

## Worked run

Need: a studio HDRI for a product viewer and an icon set, in a client product.

1. `A search <catalog> --group 3d --query "hdri" --commercial --no-attribution`. First result: a public domain library, status `catalog-verified`.
2. The catalog note says that the live API needs a visible credit and downloads do not. Choose the download.
3. Open the license page. Confirm the public domain dedication. Verdict `clear`.
4. Download the 2k file to a scratch folder. Move it to `public/hdri/`.
5. Record it with `--catalog-id poly-haven` and today's date.
6. `A search <catalog> --group icons --query "stroke weights" --commercial`. Choose a set with several weights so that the stroke can match the text weight.
7. Install one exact version. Read the license file inside the package. Verdict `clear`.
8. Record it with `--package`.
9. `A check design/assets/manifest.json --root . --scan src` exits 0.
10. `A notices design/assets/manifest.json -o ATTRIBUTION.md`.
