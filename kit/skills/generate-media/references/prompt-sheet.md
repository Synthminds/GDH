# The prompt sheet

Read this file at step 4 of `generate-media`. It covers the prompt sheet, how to turn the chosen direction and the tokens into words a model can use, the prompt structure, the negative list, composition for text, and worked examples.

Evidence. The derive-from-the-subject method and the generic-output habits come from the Anthropic frontend-design skill and the Impeccable craft floor, read 2026-11-23. Tool facts (some vector models accept a list of hex colors, a vector output mode may accept no reference images, a text field copied exactly as the user wrote it, names of living designers and brands kept out of prompts in brand workflows) come from the connector cards and workflow text, read 2026-11-23. No prompt was run; the quality of any phrasing here is UNTESTED.

## 1. The prompt sheet

Write it in `prompt-sheet.md` before the first prompt. One sheet per set.

| Field | Holds | Example |
| --- | --- | --- |
| Asset | What it is and how many | 6 spot illustrations for empty states |
| Job | What it must do for the person | Make an empty screen feel calm and show the next step |
| Placement and size | Where it sits; delivered pixel size; aspect ratio | 320 x 240 on screen, 2x density; 4:3 |
| Direction | The chosen direction's name and idea sentence | "Paper trail: the work is real paper that sorts itself" |
| Subject vocabulary | Concrete things from the subject's world | Index cards, paper clips, carbon copies, rubber stamps |
| Style line | One sentence fixed for the whole set | See section 3 |
| Palette | Token names and values, with roles | Ground `color.paper` #F5EFE6; ink `color.ink` #1B1A17; accent `color.stamp` #C2410C |
| Composition | Where the subject sits; where text or UI goes | Subject in the lower right two thirds; calm space top left |
| Must not | The negative list | See section 5 |
| References | Images that show the style, with their license status | Two own sketches; one licensed reference for texture only |
| Tool and medium | Capability; output format; vector or raster | `image-gen`, PNG with transparency |
| Spend limit | In the tool's units | Set by the user |

## 2. From direction and tokens to words

Models read words, and some read color values. Translate the design system into both.

| Token family | Into the prompt |
| --- | --- |
| Color | Name each color in plain words with its role ("warm off-white paper ground, near-black ink, one burnt-orange accent"). Pass hex values too when the tool takes a color list. |
| Type | Never ask the model to render text. State "no text, no letters, no numbers". Type is added later in the design. |
| Radius and shape | "Soft rounded corners" or "hard square corners", only when shapes appear |
| Shadow and depth | "Flat, no shadows" or "soft paper shadow, short offset" |
| Texture | "Fine paper grain" or "smooth vector fills" |
| Motion (for video) | The brand's motion character: "slow, settling moves" or "crisp, snappy cuts" |
| Imagery rules | Copy the design system's do and do-not list into the sheet |

Derive the subject vocabulary from the subject's own world: its materials, tools, places and history. Five to ten concrete nouns. These make a set specific to the brand instead of generic.

## 3. The style line

One sentence that fixes medium, technique, light, palette and texture. Reuse it word for word in every prompt of the set.

Template:

```
<medium and technique>, <light>, <palette in words>, <texture>, <framing>
```

Examples:

```
flat cut-paper illustration with soft paper shadows, even daylight, warm off-white ground with near-black ink and one burnt-orange accent, fine paper grain, centered object on plain ground

editorial product photograph, soft window light from the left, muted warm neutrals with a deep green accent, shallow depth of field, eye-level three-quarter view

isometric line illustration, no lighting, two-color: deep navy lines on pale blue ground, smooth vector fills, object isolated with margin
```

## 4. The prompt structure

One prompt per idea. Write it in this order:

1. Subject: the one thing, concretely, with its action. "A stack of index cards sorting itself into three trays."
2. Context: where it is, only as much as the composition needs.
3. Style line, word for word.
4. Composition: framing, camera or view, where empty space goes, aspect ratio.
5. Constraints: the must-not list in short form.

Rules:

1. One idea per prompt. Different ideas go in different prompts in one batch, not as variations of one prompt.
2. Concrete nouns over adjectives. "Brass paper clip" beats "premium detail".
3. Name no living artist, no designer and no brand in a prompt.
4. Never ask for text, logos, interface screens or numbers in the image.
5. Use the tool's own parameter for aspect ratio, output count and format. Do not rely on words in the prompt for them.
6. When the tool asks for the user's prompt copied exactly (some tools do for their own reasons), copy it exactly and add the sheet's constraints only through the fields the tool offers. Read the card.
7. Read the model's own prompting guide when the tool has one. Model guides differ.

## 5. The negative list

Write it once per project. Put the short form in each prompt, or in the tool's negative field when it has one.

Always:

- No text, letters, numbers, watermarks or signatures.
- No logos, brand marks or recognizable products of other brands.
- No real or recognizable people unless consent is on record.

From the direction and the tell list, as relevant:

- No purple-to-blue gradient wash, no glow on dark, no glassy blobs, unless the brand requires them.
- No generic stock poses: handshake, pointing at a screen, laughing at a salad.
- No floating 3D abstract shapes with no link to the subject.
- No cluttered scene; one subject.

A choice that the design system requires is never on the negative list. Report it as `brand-required`.

## 6. Composition for text and interface

1. A hero image leaves calm space where the headline will sit. State where: "empty calm area in the upper left third".
2. Keep the subject away from the edges that crops will cut on other ratios. Generate at the widest ratio needed, or generate per ratio.
3. Spot illustrations sit on a plain or transparent ground at a known margin, so they scale and align.
4. Check the busiest area behind future text. Text will need a scrim if contrast is uncertain.

## 7. Worked examples

Empty-state illustration, one of six:

```
Subject: an empty wire tray with a single paper clip resting in it, waiting.
Style: flat cut-paper illustration with soft paper shadows, even daylight, warm off-white ground with near-black ink and one burnt-orange accent, fine paper grain, centered object on plain ground.
Composition: 4:3, object in the lower two thirds, generous margin, transparent or plain ground.
Constraints: no text, no letters, no logos, no people, one object.
Tool fields: aspect 4:3; outputs 2; format PNG.
```

Hero photograph for a staged product scene:

```
Subject: the client's ceramic planter (reference images 1 to 3) on a pale oak shelf with a trailing pothos.
Style: editorial product photograph, soft window light from the left, muted warm neutrals with a deep green accent, shallow depth of field, eye-level three-quarter view.
Composition: 16:9, planter in the right third, calm empty wall in the left half for a headline.
Constraints: no text, no logos, keep the planter's shape, glaze color and drainage hole exactly as in the references.
Tool fields: aspect 16:9; outputs 2; references: product photos 1 to 3 (upload approved, decisions round 2).
```

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Adjective soup | "Stunning, premium, modern, sleek" | Concrete nouns from the subject's world |
| Style drift | Each prompt describes the style differently | One style line, word for word |
| Text in image | Garbled words in the picture | "No text"; add type in the design |
| Variations of one idea | Four near-identical outputs | One prompt per idea in a batch |
| Category default | The output looks like every competitor's hero | Subject vocabulary and the direction, not the category |
| Named artist | "In the style of" a living artist | Describe the technique in words |
| No room for text | The subject fills the frame behind the headline | State the calm area in the composition |
