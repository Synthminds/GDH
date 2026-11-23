# The tell list

List version: 2026-11-23. Read this file at step 8 of `design-critique`.

A tell is a visual habit that marks work as generic AI output. This file lists each tell, why it reads as generic, and the counter-move. Part 2 holds the tells that `scripts/tells.py` detects. Part 3 holds the tells that only a reviewer can see.

## 1. How to use the list

- The list is a GDH default. The user, the design system and the brief rank above it.
- A tell that the user or the design system requires is `brand-required`. Report it under that label, with its source. It is not a finding.
- A brand-required choice still passes the gates. A required palette that fails contrast is an accessibility finding.
- The list is not a design method. A page that avoids every tell can still be generic. The method is: derive each choice from this subject and this brief.
- The list moves. Looks that were once the cure are now tells. Keep the version date. Default: review the list every 90 days.
- A tell is a lead. Confirm it on the render before you report it.

The swap test is the real check: would this page fit any other product in the category? Each part that would fit is a finding, with or without a listed tell.

When a tell is confirmed, the counter-move is to rebuild the element from the brief. Do not soften it. A gradient at half strength is still the default gradient.

## 2. Tells the script detects

Severity is the script's default. Raise or lower it in the review when the context calls for it, and say why.

### Color and surface

| Code | Severity | What the script matches | Why it reads as generic | Counter-move |
| --- | --- | --- | --- | --- |
| `TELL_PURPLE_GRADIENT` | high | A CSS gradient, or Tailwind gradient classes, whose stops include indigo, violet or purple and all sit between blue and pink | It is the most repeated brand statement in generated pages. It says "software" and nothing about this subject | Take the palette from the subject's world. Use one flat color with a role. A gradient needs a reason and token stops |
| `TELL_GRADIENT_TEXT` | high | `background-clip: text`, or `bg-clip-text` with `text-transparent` | It puts emphasis in an effect, not in the words. It also fails contrast at one end of the gradient | Solid token color. Carry emphasis with size, weight or position |
| `TELL_GLASS_EVERYWHERE` | medium | Three or more backdrop-blur uses in the scan | Blur is used as a costume. No layer needs to separate from moving content | Keep blur for one layer over moving content. Give other surfaces a solid token color |
| `TELL_GLOW_SHADOW` | medium | A shadow layer with no offset, a blur of 8 px or more and a saturated color; a Tailwind colored shadow | A glow has no light source. It decorates and adds no depth | An elevation token with an offset and a blur, or no shadow |
| `TELL_UNIFORM_RADIUS` | low | Six or more radius uses, of which 80 percent share one value of 12 px or more. In an HTML style block, a class or tag selector counts each element it matches | One radius for every role shows that no role was decided | Radius tokens by role: control, card, sheet. A nested radius is smaller than its parent |
| `TELL_COLOR_SPRAWL` | low | More than 12 distinct literal colors outside tokens | Colors were picked one at a time. No palette exists | Map each color to a semantic token. Remove the rest. For depth run `design-system` audit |
| `TELL_SECOND_WAVE_PALETTE` | medium | With stock type only: a cream ground with a terracotta or orange accent, or a near-black ground with one vermilion, orange or acid-green accent. Default: the hue bands are a dated rule of thumb | These looks became the next default once agents learned to avoid the purple gradient | Take the ground and the accent from the subject's world. Decide light or dark from the use scene |

### Type

| Code | Severity | What the script matches | Why it reads as generic | Counter-move |
| --- | --- | --- | --- | --- |
| `TELL_DEFAULT_FONT_ONLY` | medium | Every declared family starts with Inter, Roboto, Arial, Helvetica, Open Sans or a system stack; or a styled document declares no family | The typeface is the voice. A default voice is nobody's voice | Choose a text face for this subject. Test it with real copy. Load it and record its license. Then run `typography` |
| `TELL_FONT_SIZE_SPRAWL` | low | More than 8 distinct literal font sizes | Sizes picked one at a time. No scale exists | One scale from one ratio. Name each step by role |
| `TELL_SECOND_WAVE_FONT` | low | Every declared family is a first-wave default or a second-wave face, and one second-wave face is present. The second-wave list of 2026-11-23: Geist, Space Grotesk, DM Sans, Poppins, Manrope, Plus Jakarta Sans, Instrument Serif, Fraunces, Playfair Display | These faces replaced Inter as the reflex choice. They carry no reason of their own | Find the reason in the brief. With none, choose a face for this subject and run `typography` |
| `TELL_ACCENT_WORD` | low | An `em`, `i`, `span` or `strong` inside an h1 or h2 that sets one word apart with italic, a second face or a second color | One styled word is the only typographic idea on the page | Let the whole headline carry the weight. Drop the styled word |
| `TELL_MONO_LABELS` | low | A monospace family on small or tracked uppercase labels, two or more times, with no code selector | A "technical" costume on labels that hold no code | Set labels in the text face. Keep monospace for code, data and measurement |
| `TELL_EYEBROW_EVERY_HEADING` | medium | A small uppercase, tracked label directly above two or more headings, and above at least half of the h1 and h2 headings | The label repeats what the heading says. It is template chrome | Delete each label that carries no information. Keep one only where it names a real category |
| `TELL_FAKE_SEQUENCE` | low | Three or more markers from 01 to 09, starting at 01, outside an ordered list | Numbers imply an order the items do not have | Number only real steps, in an ordered list |
| `TELL_ARROW_EVERY_LINK` | low | An arrow glyph or arrow icon in three or more link or button texts, or an arrow in `::after` content on a link selector | The arrow repeats the affordance on every link | Keep an arrow only where direction is the message. Let the link text name the action |
| `TELL_REVEAL_EVERY_SECTION` | medium | `opacity: 0` with a translate on a section or reveal selector, or reveal classes, `data-aos` or motion `initial` props, three or more times | Motion as a reflex. Content waits for a scroll | Remove the reveal. Keep one authored motion that answers user input or explains a change |
| `TELL_MIDDOT_META` | low | Two or more short text runs of 16 words or fewer joined with middle dots | Template chrome copied from showcase sites | Write the meta line as a sentence, or drop the parts that carry no information |

### Structure

| Code | Severity | What the script matches | Why it reads as generic | Counter-move |
| --- | --- | --- | --- | --- |
| `TELL_HERO_THREE_CARDS` | medium | A centered h1 followed by a three-column grid | It is the default page skeleton. It appears whether or not the content has three equal parts | Start from the content. Open with the most characteristic thing in the subject's world. Give unequal content unequal space |
| `TELL_LEFT_BORDER_CARD` | medium | A one-sided border of 2 px or more on a rounded box or a card-like selector | A side bar on a rounded box is the stock "callout". It marks status by color alone | Mark the state with an icon and a label, a full border or a tinted ground |
| `TELL_GRADIENT_STAT_ROW` | medium | Three or more big numbers in one file, with a gradient fill | The hero-metric template. The numbers are often filler | Show a figure only with a source and a comparison. Solid token color |
| `TELL_STAT_ROW` | low | Three or more big numbers in one file | Same template without the gradient | Keep it only when each figure has a source and helps a decision |
| `TELL_EMOJI_ICON` | medium | An emoji at the edge of an element or a string, or in CSS `content` | Emoji render differently on each platform and carry no brand. They stand in for an icon set nobody chose | One icon set with one stroke weight, or authored SVG. Record the source through `find-assets` |

### Content

These three are never `brand-required`. Invented content breaks kernel rule 11. `--allow` refuses them.

| Code | Severity | What the script matches | Why it matters | Counter-move |
| --- | --- | --- | --- | --- |
| `TELL_LOREM` | high | Placeholder Latin text | Placeholder text hides real length and real hierarchy problems | Real copy from the brief. A missing fact becomes a bracketed label such as `[PRICE]` |
| `TELL_PLACEHOLDER_COPY` | medium | "Feature One", "Your headline here", "Card title", stock names such as John Doe | The page was designed around nothing | Specific copy. Ask the user for the missing name or fact |
| `TELL_INVENTED_STAT` | high | Figures in the forms of "10,000+ customers", "99.9% uptime", "10x faster", "4.9/5", with no source on the line | A figure with no source is an invented fact until proven | Confirm the figure and its source. Otherwise use a labelled placeholder |

The script skips a figure when its line holds a `data-source` attribute, a `cite` element, the word "source:" or a bracketed placeholder.

### How the script decides brand-required

| Input | The script treats a pattern as required when |
| --- | --- |
| `--tokens tokens.json` | Value matches only, for patterns with a value. A gradient token holds the exact observed stops; Tailwind palette steps resolve against token names first. A shadow token holds the exact shadow layer. A blur token holds every observed blur radius. Every color of a second-wave palette is a token color. The radius family holds one value. A type family or font token names the face. A token name alone counts only for patterns with no single value: gradient text, a side bar, an eyebrow label, a stat block |
| `--design DESIGN.md` | A sentence names the pattern and holds no negation word, and it does not sit under a heading such as "Do not" or "Avoid" |
| `--allow CODE` | The user said so in this session. The source reads "user" |

Limits of this logic. Check them in the review:

- A sentence that allows a pattern in one place ("glass on the nav only") makes the script accept it everywhere. Check the scope yourself.
- A gradient with stops outside the tokens stays a finding, even when the design system has a gradient. That is drift from the system.
- A heading such as "Do and do not" marks every line under it as a ban. A required pattern listed there shows up as a finding. Relabel it by hand.
- The script reads the files you pass. A token defined elsewhere is unknown to it.
- A token name alone still marks an eyebrow, a side bar, gradient text or a stat block required across the whole scan. Confirm the scope of that token on the render.
- A gradient whose stops equal plain ramp steps (for example `indigo-500`, `purple-500`, `pink-500`) is not a brand gradient. The script reports it unless a gradient token holds those stops. A sentence in `DESIGN.md` can still mark it required; check that sentence.

### What the scan misses

The scan reads one file at a time as text. Check these by eye on every review:

- A figure built at run time, or split in a form the figure check does not read. The check reads sibling elements and value and label pairs in one data literal. Read every stat block by eye all the same.
- A file the scan skipped for size, a folder whose name starts with a dot, and a path that holds no matching file. The summary lists skipped files. Zero files scanned is no result.
- An emoji inside a user message, a comment or chat text is content, not an icon. Drop a `TELL_EMOJI_ICON` finding on such text.
- A figure with a real prose attribution, such as "in the 2025 member survey" or "according to", may still be flagged. Keep the figure when the source exists, and say so in the review.

## 3. Tells only a reviewer can see

Check these on the render. Each needs judgement. Where a row names a code, the script catches only the forms that section 2 lists; check the other forms by eye.

| Tell | How to see it | Counter-move |
| --- | --- | --- |
| Cream ground, high-contrast serif, terracotta accent (`TELL_SECOND_WAVE_PALETTE` with stock type) | The page could be any "warm editorial" brand | Ask which object in the subject's world the palette comes from |
| Near-black ground with one acid or vermilion accent (`TELL_SECOND_WAVE_PALETTE` with stock type) | The reaction to the purple gradient, now a default of its own | Decide light or dark from the use scene, not from the category |
| Broadsheet layout: hairline rules, zero radius, dense columns | A newspaper costume on content that is not news | Structure must carry information. Remove rules that divide nothing |
| The card kit: identical rounded cards, one radius, one gray shadow | Every section has the same container | Vary structure where content differs. No card inside a card |
| An icon tile above every heading | Rounded square, icon, heading, text, repeated | Remove icons that say nothing. Use a real picture or no picture |
| Numbered markers 01, 02, 03 on items that are not a sequence (`TELL_FAKE_SEQUENCE`) | Numbers imply order where none exists | Number only real steps |
| Meta strings joined with middle dots (`TELL_MIDDOT_META`); labels as "WORD, dash, fragment" | Template chrome copied from showcase sites | Write the meta line as a sentence, or drop it |
| An arrow on every link and button (`TELL_ARROW_EVERY_LINK`) | Decoration that repeats the affordance | Keep an arrow only where direction is the message |
| One headline word in italic, bold or a second color (`TELL_ACCENT_WORD`) | The only typographic idea on the page | Make the whole headline carry the weight |
| Fade and slide up on every section (`TELL_REVEAL_EVERY_SECTION`); hover lift on every card | Motion as a reflex | One authored moment. Motion that answers user input |
| Monospace for labels and small data with no code in sight (`TELL_MONO_LABELS`) | A "technical" costume | Monospace for code, data and measurement only |
| Gray text on a colored ground | Fails contrast and looks washed out | Tint the text from the ground hue or from the foreground |
| Tinted near-black and tinted near-white by habit | Listed as a current tell by one source and as good practice by others | Do not hard-code either way. Decide from the design system, then the brief |
| Decorative sparklines, progress rings and badges | Shapes that stand in for content | Every chart mark shows real data, or goes |
| Filler copy: "Submit", "Learn more", "Unlock the power of" | Words that fit any product | Buttons name their action. Claims name a fact |
| A generic geometric mark beside a default sans wordmark | A logo that is not an idea | Send to `logo-identity` |
| Three "directions" that are one layout in three colors | Options with no idea | Send to `mood-board` |

## 4. Positive signs

Absence of tells is not the goal. Look for these, and name them under "working well":

- One memorable element, and quiet everywhere else.
- A palette and a typeface that a person can trace to the subject's world.
- Structure that differs where content differs.
- Copy that could belong to no other product.
- Borders, numbers and labels that each encode something.
- A page that fails the swap test: it would look wrong under a competitor's name.

## 5. Keeping the list current

- Change the list through `add-design-tool` or a refinement of this skill. Log each change in `refinement-log.md`.
- When you add a rule to `tells.py`, add its row here and a test in `tests/test_tells.py`. Update `LIST_VERSION`.
- Retire a rule when the habit fades or the rule misfires often. A stale ban list becomes the next template.
- A second detector can run beside this one. See the tool cards for `impeccable` and `design-taste-frontend`. Their rule sets differ from this list, and they change often.

## Sources

- Anthropic frontend-design skill: the five default clusters and the type tells.
- Impeccable README and craft floor, read 2026-11-23: nested cards, side bars, gradient text, glass as decoration, hero-metric block, emoji as icons.
- Claude Design System type reference, craft rule on AI tropes.
- design-taste-frontend, "Never" list.
- The rules are scored against a small labelled corpus in `evals/cases/quality/` (10 pages, one reviewer). Run `python3 evals/quality.py` for precision and recall per rule. Ten pages prove little; the thresholds (3 blurs, 80 percent, 8 sizes, 12 colors) stay defaults.
- Known gaps on 2026-11-23: no rule covers the second-wave templates (cream and terracotta, tinted near-black with one orange accent, bento grids). Recall is 0 for invented figures with no currency or plus sign, glass on four surfaces, an invented testimonial name, a plain stat row in a serif face and one radius on pastel surfaces. Emoji inside chat messages are a false positive for `TELL_EMOJI_ICON`.
