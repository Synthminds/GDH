# Checks for slides and print

Read this file at step 2 of `accessibility-gate` when the work is a slide deck, a document, a poster, a one-pager or another piece for paper or for a PDF. Classes and source classes follow the legend in the web and app reference.

A deck or a print piece made with an artifact type follows that type's own rules first. Example cards: [claude-slides](../../../references/tools/claude-slides.md), [claude-design](../../../references/tools/claude-design.md). The floors below come partly from those type rules.

## Part A. Slides

A slide is read at a distance, in a room, often once, and often again later as a file. Check both uses.

### A1. Checks

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| S1 | Text is 4.5:1 or more against its ground; large text 3:1 | Gate | Kernel | Contrast |
| S2 | Text over a photograph passes at its worst point, with one protection method used every time: a card, a scrim or a panel | Gate for the ratio. Default for the method | Kernel. Documented: slides type rule | Worst point |
| S3 | No meaning by color alone: chart series, status, emphasis | Gate | Kernel | Grayscale |
| S4 | Every image, chart and diagram that carries meaning has a text alternative | Gate | Kernel floor | Inspect the export |
| S5 | No slide flashes. No transition strobes | Gate | Kernel floor | Play the deck |
| S6 | Speech in an embedded video or audio clip has captions or a transcript | Gate | GDH gate | Play the clip |
| S7 | Text is 24 px or more on the deck's design canvas | Default | Documented: slides type rule | Measure |
| S8 | Four or five type sizes for the whole deck | Default | Documented: slides type rule | List the sizes |
| S9 | Each slide has a unique title | Default | Memory: common authoring guidance | Outline view |
| S10 | The reading order of each slide's elements matches the visual order | Default | Memory: common authoring guidance | Reading-order pane, screen reader |
| S11 | Text is real text, not a picture of text | Default | Memory | Select the text |
| S12 | A table has a header row and stays simple: no merged cells | Default | Memory | Inspect |
| S13 | A link has text that names its destination | Default | Memory | Inspect |
| S14 | Motion is minimal, starts on a click and has no auto-advance | Default | Rule of thumb | Play the deck |
| S15 | The deck states its language | Default | Memory | File properties |
| S16 | One idea on a slide. The title states the point | Default | Rule of thumb | Read the titles alone |
| S17 | Icons are 32 px or more, with real contrast | Default | Documented: slides type rule | Measure |

### A2. The room test

Rule of thumb, not a measurement: view the slide at a small size on your screen, as it would look from the back of a room. Every word that matters must still read. When text fits only below the size floor, the slide holds too much text. Split the slide; do not shrink the type.

### A3. The file test

A deck that is sent as a file is a document. Check the export, not only the canvas.

1. Export in the format the audience will get.
2. Open the export. Check that text can be selected and searched.
3. Check that images kept their text alternatives. Some exports drop them.
4. Check the reading order with the tool's reading-order view or with a screen reader.
5. Label the export checks UNTESTED when you could not open the exported file.

An export path changes what survives. A text alternative that exists on the canvas and not in the export is a failure of S4 for the people who get the file.

### A4. Common failures

| Name | Sign | Check |
| --- | --- | --- |
| Wall of text | A slide of paragraphs at a small size | S7, S16 |
| Photo with naked text | Light text straight on a busy photograph | S2 |
| Legend by color | A chart that only a color legend explains | S3 |
| Picture of a table | A screenshot of a spreadsheet | S11, S4 |
| Untitled slides | Several slides with no title, or the same title | S9 |
| Strobe transition | A flashing build or a fast zoom on every slide | S5, S14 |
| Lost alt text | Alternatives exist on the canvas and not in the export | S4 |

## Part B. Print and PDF

Paper cannot be zoomed, and its contrast depends on ink, stock and light. A PDF that is read on a screen is also a digital document, with its own checks.

### B1. Checks for anything printed

| # | Check | Class | Source class | Test |
| --- | --- | --- | --- | --- |
| P1 | Text is 4.5:1 or more against its ground; large text 3:1 | Gate | Kernel | Contrast, on the print colors |
| P2 | The piece reads in grayscale | Gate | Kernel: no meaning by color alone | Grayscale |
| P3 | Nothing is under 12 px on a 96 px per inch canvas, which is 9 pt | Default | Documented: design canvas print rule | Measure |
| P4 | Body text is 16 px on that canvas, which is 12 pt, with line height 1.5 to 1.65 | Default | Documented: design canvas print rule | Measure |
| P5 | Body measure is 60 to 75 characters | Default | Documented: design canvas print rule | Count |
| P6 | No gray text lighter than a mid gray that holds 4.5:1 on white | Default | Documented: design canvas print rule, by P1 | Contrast |
| P7 | Rules and table lines are 1 px or more | Default | Documented: design canvas print rule | Measure |
| P8 | Infographic text is about 7 pt or more in print | Default | Rule of thumb | Measure |
| P9 | Text is not set over a busy image without a solid or tinted panel | Default | Rule of thumb, by P1 | Worst point |
| P10 | A code that is scanned, such as a QR code, also has its address in text | Default | Rule of thumb | Look |
| P11 | A phone number, an address and a date are in text, not only in an image | Default | Rule of thumb | Look |
| P12 | Thin, light or condensed faces are not used at small sizes | Default | Rule of thumb | Proof |

P3 and P4 give two floors on purpose. P3 is the smallest text anywhere. P4 is the body size.

### B2. The proof test

A screen is brighter and sharper than paper. Before sign-off of a printed piece:

1. Print one page at real size on an ordinary printer, in grayscale.
2. Read it at arm's length in normal room light.
3. Mark each word that is hard to read.
4. For a large format, print a real-size crop of the smallest text and view it from the real distance.
5. Label the result. "Proofed on an office printer" is VERIFIED for that proof only. Press output is UNTESTED until a press proof exists.

Color on a press differs from color on a screen. A contrast ratio computed from screen values is DOCUMENTED for print, not VERIFIED.

### B3. Checks for a PDF that people read on a screen

These come from memory of PDF accessibility practice. No standard was read for this kit. All are defaults, and most need a PDF tool to test.

| # | Check | Class | Test |
| --- | --- | --- | --- |
| D1 | The PDF is tagged: headings, lists, tables and paragraphs are marked | Default | Tags view in a PDF tool |
| D2 | The reading order is correct | Default | Reading-order view, screen reader |
| D3 | Text is real text. A scan has been through text recognition | Default | Select and search |
| D4 | Images have text alternatives. Decorative ones are marked as artifacts | Default; the alternative itself is gate 8 | Tags view |
| D5 | The document has a title and a language | Default | File properties |
| D6 | A long document has bookmarks that match its headings | Default | Bookmarks pane |
| D7 | Form fields have labels and a tab order | Default | Tab through the form |
| D8 | Links work and name their destination | Default | Click each |
| D9 | Text was not converted to outlines | Default | Select the text |

With no PDF tool in the session, mark D1 to D9 UNTESTED and say which tool can check them. Do not claim a tagged PDF from the export setting alone.

### B4. Offer the alternative

- Default: a printed piece that carries key information also has a digital, accessible version. Name where it lives.
- Default: on request, a large-print version exists. Decide who makes it.

### B5. Common failures

| Name | Sign | Check |
| --- | --- | --- |
| Screen gray on paper | Light gray text that looked fine on a monitor | P1, P6 |
| Hairlines | Rules that vanish in print | P7 |
| Tiny legal text | Terms set far below the floor | P3 |
| Color key only | A map or chart that needs color to be read | P2 |
| Outlined text | A PDF in which no text can be selected | D3, D9 |
| Untagged export | A PDF with no structure | D1 |
| Code without a fallback | A QR code and no address | P10 |

## Worked example

A one-page inspection report, invented for this example, is exported as a PDF and is also printed.

- Contrast: the status band uses white text on the brand mid-tone. `ds.py contrast` reports 3.4:1 for that pair. It fails gate 1 for body text. The band's label is 12 pt regular, so the large-text ratio does not apply.
- Grayscale: "pass" and "fail" rows differ only in green and red. They fail gate 4. An icon and the word were missing.
- Proof: printed on an office printer. The 7 pt footnote is unreadable at arm's length. Default P3 not met.
- PDF: no PDF tool in the session. D1 to D9 are UNTESTED. The report names the tool that can check them.
- Verdict: fail. Two gates failed, one default not met, nine checks untested.
- Hand-off: `refine-round` for the band color and the status marks. The brand color is `brand-required`, so the fix changes the text color or the band role, not the brand hue. The user decides.
