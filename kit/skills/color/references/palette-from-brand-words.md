# A palette from the brand words and the subject

Read this file at steps 1 to 5 of `color`. It covers the color brief, the category default, the translation from words to hue, chroma and lightness, the named colors, the options round, the failure patterns and two worked palettes, one for a physical subject and one for an abstract subject.

Evidence. "Decide light or dark from the use scene" comes from the Impeccable craft floor. "Write four to six named colors before you build" and the three template palettes come from the Anthropic frontend-design skill. "Prefer the brand's colors and derive from them" comes from the Claude Design craft rules. "Soften a saturated palette when playful must also be trusted" and "differ from the category" come from Designing for Emotion, chapters 2 and 3. All were read 2026-11-23. The word table below is practice written from memory: a default, UNTESTED until the palette is seen on a real screen. Both worked palettes at the end were checked with `ds.py contrast` on 2026-11-23.

Terms. Hue is the color family, as an angle. Chroma is the strength of the color. Lightness is how light it is. A named color is one color with a role and a reason.

## 1. Write the color brief

| Line | Write | Example |
| --- | --- | --- |
| Brand words | Three words, each with its "not" | steady, not stiff; coastal, not nautical-themed; exact, not cold |
| Subject colors | Five colors seen in the subject's own world, each with its object | Wet slate quay, weathered teal hull paint, buoy orange, chart paper, tide-gauge white |
| Fixed colors | Colors the user or the design system fixes, with their source | None |
| Use scene | Who, where, in what light, on what device | A skipper on deck at dawn, phone in hand, glare and low light both occur |
| Media | Screen, print, signage, video | Mobile web; one printed poster |
| Meanings | Every meaning color must carry | Late, cancelled, on time, selected |

Rules:

1. Take subject colors from photos the user supplies, from the brief's references, or from a question to the user.
2. A subject color is evidence. Note its hue family, its strength and its lightness. Do not sample a pixel and call it the brand.
3. A fixed color is exact. Record its value and its source. Never round it.
4. List the meanings now. They decide how many status hues the palette needs.

## 2. Write the category default

Write the palette that most products in the category share. One line is enough.

- "Marine apps: navy ground, white text, a cyan accent, red and green lights."
- "Finance apps: deep blue, a green for gains, a gray card grid."

Then decide per attribute: keep the convention or break it. Keep a convention that carries meaning for the user. Break a convention that only signals "we are in this category".

Check: place the candidate palette beside five competitor screens. A reviewer can pick it out. The notes name two conventions it breaks on purpose.

Three template palettes to treat as defaults to move away from, unless the brief asks for one:

- a cream ground with a high-contrast serif and a terracotta accent
- a near-black ground with one acid-green or vermilion accent
- gradient washes over a kit of identical cards

A purple-to-blue gradient as the brand statement is the fourth. A design system that prescribes any of these wins. Report it as `brand-required`.

## 3. Turn each word into a color intent

Translate each brand word into intents for hue, chroma and lightness. Write the intent before you pick a value.

| The word points to | Hue | Chroma | Lightness and contrast |
| --- | --- | --- | --- |
| calm, quiet | Few hues; neighbors on the wheel | Low to moderate | Soft steps between surfaces; text contrast still passes |
| energetic, loud | One hue with a far accent | High in the accent, low in the ground | Strong light and dark contrast |
| warm, human | Reds through yellows; a warm-tinted neutral | Moderate | Off-white grounds, not blue-white |
| cool, exact, technical | Blues through teals; a cool-tinted neutral | Low in surfaces, clear in accents | Crisp steps; clear control outlines |
| trusted, serious | One restrained hue | Low to moderate | Dark text on light ground; few tints |
| playful and trusted | Several hues | Reduced from pure primaries | Mid lightness; avoid a toy look |
| premium | One deep hue or near-neutral | Low | Wide lightness range, much empty ground |
| natural | Hues seen in the subject's materials | Low to moderate, uneven | Earth and plant lightness, not neon |
| urgent | Used only for the urgent state | High | High contrast to the ground |

Rules:

1. Write one row for each brand word. A word that changes no row is not a color word. Leave it to type or layout.
2. Use the "not" to cut. "Coastal, not nautical-themed" cuts navy with red and white stripes.
3. Take the hue from a subject color when one fits the intent. That ties the palette to the subject.
4. One brand hue and at most one accent hue carry emphasis. More hues need a meaning each.
5. Pick the accent for its job. An accent that marks the primary action must stand apart from every status hue.

## 4. Name four to six colors

Write the named colors as a table. This is the palette plan. Build nothing before it exists.

| Name | Role | Intent | Reason |
| --- | --- | --- | --- |
| Hull teal | Brand and primary action | Hue near 195, moderate chroma, dark enough for white text | The hull paint; "steady" asks for a deep, quiet color |
| Slate | Text and dark surfaces | The neutral, tinted to the teal hue | The wet quay |
| Chart paper | Light ground | Near white, tinted to the teal hue | The paper chart; "exact" asks for a clean ground |
| Buoy orange | The one live-state marker | Far from teal, high chroma | The buoy: the thing you look for |
| Signal red | Danger only | A red apart from the orange | Cancelled sailings |

Tests on the plan:

- The no-template test. The plan matches none of the template palettes, or the brief asks for one.
- The swap test. Would this plan fit a competitor? If yes, change the row that is generic.
- The reason test. Every row cites a brand word or a subject color.
- The job test. No two colors share a job. No job has two colors.

## 5. Decide the first theme from the use scene

| Use scene | First theme |
| --- | --- |
| Bright surroundings, outdoor use, long reading | Light |
| Dark rooms, media viewing, night use, long monitoring sessions | Dark |
| Both occur | Build both; ship the system preference as the default |

The product category does not decide. A developer tool is not dark by rule. A wellness app is not pastel by rule.

## 6. Show options

1. No direction chosen yet: show two or three palettes that differ in idea. Each takes its hue logic from a different subject color.
2. A direction is chosen: show two variants that differ in one attribute. Change the accent, or the neutral tint, or the chroma level.
3. Show each palette on the same real sample: one screen or one card with real copy. A row of swatches decides nothing.
4. Show each palette with its text pairs already passing contrast.
5. Keep option names stable across rounds.
6. ASK: "For each palette: keep, change or remove the ground, the brand color, the accent?"

## 7. When colors are fixed

1. Load the fixed colors exactly as given. Record the source of each.
2. List the roles the fixed set does not cover: muted text, control outlines, status, dark theme.
3. Derive each missing role from the fixed hues. Hold the hue. Move lightness and chroma.
4. ASK before you add a derived color to the tokens. Mark it INFERRED until the owner approves.
5. A fixed pair that fails contrast stays exact. Flag it. Add a passing role beside it for text.
6. Do not invent an unrelated hue to fill a gap. A status hue is the only exception, and it needs a yes.

## 8. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Template palette | The plan matches a known template with no reason | Return to the subject colors |
| Swatch row | Options shown as swatches with no screen | Show each on the same real sample |
| Stock scale | A public scale used unchanged as the brand palette | Shift hue, chroma and lightness toward the plan |
| Five accents | Many strong colors with no ranking | One brand hue, one accent, the rest neutral |
| Hue as status and brand | The brand red also means error | Move the brand hue or the status hue apart |
| Tool as reason | "The generator picked it" | Write the reason from the brief |
| Category echo | The palette cannot be told from competitors | Break two conventions on purpose |
| Toy palette | Pure primaries on a product that must be trusted | Reduce chroma; keep the hues |
| Gray on color | Plain gray text on a colored surface | Tint the secondary text from the surface hue |
| Avoidance palette | All color removed to avoid a gradient; near-black with one acid accent | Derive from the subject, not from a ban list |

## 9. Worked palette

The values below passed `ds.py validate` and `ds.py contrast` on 2026-11-23: 19 pairs, 38 checks in two themes, 0 failed. The project is fictional.

Tide table app. Brand words: steady, coastal, exact. Scene: on deck, glare and low light. Both themes ship.

| Role | Light | Dark | Reason |
| --- | --- | --- | --- |
| `bg` | `#fafcfc` | `#0b1110` | Chart paper; night deck. Neutral tinted to hue 195. |
| `surface` | `#f3f8f8` | `#111717` | One step from the ground |
| `text` | `#121d1d` | `#e7ecec` | Slate. 16.72:1 and 15.97:1 on `bg`. |
| `text-muted` | `#4f5b5a` | `#a9b4b3` | 6.85:1 and 8.95:1 on `bg` |
| `border-control` | `#848f8e` | `#616b6b` | 3.23:1 and 3.47:1 on `bg` |
| `accent` | `#117878` | `#117878` | Hull teal. White text on it: 5.27:1. |
| `accent-text` | `#0b5f5f` | `#5ecbcb` | Links. 7.24:1 and 9.87:1 on `bg`. |
| `signal` | `#d8732b` | `#f59740` | Buoy orange, icon only. 3.18:1 and 8.51:1 on `bg`. |
| `danger-text` | `#ac1a1c` | `#f98f87` | 6.98:1 and 8.44:1 on `bg`, always with an icon |

What the checks changed:

- The first buoy orange was lighter. It reached only 2.73:1 on the light ground and failed as an icon. Its lightness went down until it passed 3:1.
- The orange never carries white text: 3.27:1. A signal chip uses the dark text token on orange: 5.25:1.
- The teal fill is the same in both themes. Its link color is not: the dark theme needs a light teal.
- Teal at this hue has a low sRGB chroma limit. The brand color is quieter than the hull paint. The orange carries the energy.

## 10. Second worked palette: an abstract subject

The subject is the one in `mood-board`, directions reference, section 8: an AI assistant that turns recorded customer interviews into findings for a product team. Brand words: traceable, candid, collegial. The user chose direction A, Marked Transcript. The project is fictional.

Scene: a researcher at a desk between calls, office light, long reading of transcripts. First theme: light. Dark waits until a night-use scene appears in the brief.

Category default: a white ground, a violet to indigo gradient on every AI action, a sparkle icon, gray cards. Two conventions break on purpose: no gradient, and no hue that says "AI". One convention stays: a plain light ground, because people read long text on it.

Where each color comes from:

| Name | Role | Subject source | Brand word |
| --- | --- | --- | --- |
| Printout white | Ground | A transcript printed for the debrief | candid: plain paper, nothing staged |
| Ink | Text | The pen notes in the margin | traceable |
| Highlighter yellow | Fill behind a quoted span; the primary button | The highlighter on the printout | traceable: the quote is marked, not paraphrased |
| Reviewer green | Links and comments | The green pen a colleague uses for notes, not the red pen of a grader | collegial, not cosy |
| Error red | Errors only | None; a plain status color | none |

Values, checked with `ds.py contrast` on 2026-11-23: 11 pairs, 0 failed.

| Role | Light | Check |
| --- | --- | --- |
| `bg` | `#f8f9fa` | Cool neutral, not cream: OKLCH chroma 0.002 |
| `surface` | `#eef1f4` | One step from the ground |
| `text` | `#18202b` | 15.56:1 on `bg`; 12.67:1 on `highlight` |
| `text-muted` | `#4b5563` | 7.16:1 on `bg`; speaker labels and time codes |
| `border` | `#7b8594` | 3.54:1 on `bg`; 3.29:1 on `surface` |
| `highlight` | `#f7e463` | A fill only. 1.23:1 on `bg`, so the primary button also carries a 1 px ink outline |
| `accent-text` | `#0e6656` | 6.52:1 on `bg`; always underlined |
| `danger` | `#9f1d24` | 7.44:1 on `bg`; always with an icon |

What the plan avoids:

- The violet tech look: no color has an OKLCH hue between 270 and 320, and nothing uses a gradient. The neutrals sit near hue 250 with chroma under 0.03, so they read as gray.
- The warm editorial look: the ground is cool printout white, not cream, and the accent is yellow, not terracotta.
- Color as the only cue: a highlighted quote also has a time-code tab, and a link is underlined.

Swap test: put a competitor's name on the transcript view. The yellow mark on a quoted span and the green comment pen still point at this product's job, which is evidence from interviews. A generic "insights" app has no transcript to mark.
