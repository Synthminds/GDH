# Group: illustration

Catalog group `illustration`: illustration sets, vector libraries, pattern and background generators. Read this file at step 6 of `find-assets` when the need is an illustration, a pattern or a texture.

How to read this file. An id is a catalog id. An id marked `*` has `verifiedOn` null: read its license before use. In this group every id is marked `*`. No illustration source was read for the catalog. `svg-noise-method*` is a coding method: it has no license to read. Every pick is a default from desk research. Evidence: UNTESTED.

## The order of preference

Stock illustration is the asset kind that people recognise fastest. Prefer in this order:

1. No illustration. Ask whether type, a real screenshot, a photo or data does the job better.
2. An illustration made for this product: drawn in code from tokens, or drawn by the user's illustrator.
3. A generated illustration in a style set by the direction. That is `generate-media`, with the spend gate.
4. A stock illustration, changed to fit the tokens.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| Grain, noise or a paper texture | `svg-noise-method*` | You write a filter in code: no file, no license | Paint cost on large areas. Test on a slow device. |
| A background shape, wave or blob | `haikei*` | A generator: each output differs | Web app only. Terms unread. |
| A repeating pattern | `hero-patterns*` | Subtle, clean patterns | The catalog note says credit is required. Unread. |
| Hand-drawn people | `open-peeps*`, `open-doodles*` | The catalog note says public domain | A recognisable style. Unread. |
| Flat spot illustrations | `undraw*` | One consistent style with a recolor control | Widely recognised. No bulk download, no model training, per the catalog note. Unread. |
| Themed concept sets | `storyset*`, `blush*` | Large sets, several styles | `storyset*`: credit required. `blush*`: vector export is paid, per the catalog note. |
| One specific vector | `svg-repo*` | Wide search coverage | Each asset has its own license. Uploads have no guaranteed origin. |
| Modular people | `humaaans*` | Mix-and-match figures | Terms unknown: blocked until read |

## Decision rules

1. Read the license of the exact set and the exact item first. Nothing in this group is cleared by the catalog.
2. One illustration style for each product. Two sets side by side look like two products.
3. Recolor to project color tokens. This is the minimum change, and it is not enough alone.
4. Match the line weight of the illustration to the icon stroke and the type weight.
5. Run the naming test: "Would a designer name the source set at a glance?" When the answer is yes, it is a tell unless the brief accepts it.
6. For figures of people, check the audience in the brief. The set must be able to show the people the product serves.
7. For a per-asset library, answer question 9 of the license decision: who made this file?
8. Prefer a pattern or a texture you generate in code over a downloaded one. It has no license and it matches the tokens exactly.
9. An illustration never carries information that text does not also carry.
10. Never trace, redraw or recolor someone's illustration from a reference. That is copying.

## License traps

- "Free without credit" sets often forbid redistribution in packs, competing services and model training. Read for those words.
- A customizable set can be free as an image and paid as a vector.
- A credit-required set needs the credit where the license says, not only in a notices file.
- A community vector library mixes public domain, permissive and attribution licenses. The license line is on each item page.
- A generator's terms can cover its output. Read them once and record the URL.

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Known set | Anyone in the field can name the source | Replace it, or change it past recognition with the brief's agreement |
| Filler figures | Smiling figures that say nothing about the product | Remove them. Show the product or the result. |
| Two hands | Two illustration styles in one flow | Keep one |
| Palette clash | Set colors beside brand colors | Recolor from tokens |
| Unknown maker | A vector from an upload site with no author | Verdict `blocked`. Pick a file with a named author. |
| Meaning in the picture only | A step explained only by its drawing | Add the text |

## Worked choice

The outcomes below are illustrative. They show the reasoning, not verified facts about a source.

Need: a first-run illustration for a budgeting app. Brand words: plain, steady, kind. Ships in a client product.

- Preference 1: can the first run show the user's own first budget in place of a drawing? Yes. A live preview with sample numbers marked as sample does the job.
- A small accent is still wanted behind the preview.
- Chosen: a soft grain made with the code method, tinted from one surface token. Recorded with `--origin own`.
- Rejected: a flat people set. The naming test fails, and its license is unread.
- Result: no outside asset. The report lists the rejected set and the reason.
