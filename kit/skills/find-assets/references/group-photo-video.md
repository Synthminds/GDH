# Group: photo and video

Catalog group `photo-video`: stock photos, stock video and open-access museum and agency media. Read this file at step 6 of `find-assets` when the need is a photograph, an artwork image or footage.

How to read this file. An id is a catalog id. An id marked `*` has `verifiedOn` null: read its license before use. Only two sources in this group were read for the catalog. Every pick is a default from desk research. Evidence: UNTESTED.

## The order of preference

1. The client's own photographs and footage. Ask for them first.
2. Open-access imagery that few products use: museum collections, archives, agency libraries.
3. Generated imagery in the chosen direction. That is `generate-media`, with the spend gate.
4. Stock photographs and stock video, with a treatment that ties them to the brand.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| Museum art as texture, editorial image or period detail | `met-open-access`, `art-institute-chicago` | Read for the catalog. The first flags public domain objects. The second states a license for each record. | Only flagged or licensed records are covered. An image can differ from its record. Check each object. |
| More museum and archive imagery | `rijksmuseum*`, `smithsonian-open-access*` | Very high resolution; one holds 3D scans | Each item has its own notice. Unread. |
| Space and earth imagery | `nasa-media*` | Unique subject matter | The agency's insignia is protected. No suggestion of endorsement. Unread. |
| Contemporary photographs | `unsplash*`, `pexels*` | High quality, wide subjects | People, logos and property are not cleared. A paid tier uses another license. No bulk or model use. Unread. |
| Stock video for backgrounds and b-roll | `pexels*`, `mixkit*`, `coverr*` | Short clips | Some items carry a non-commercial license. Clips are not screened. Unread. |
| Mixed media in one place | `pixabay*` | Photos, vectors, video, music | Mixed quality. Generated items are present and labelled. Unread. |
| A search across openly licensed media | `openverse*` | One search over many sources | It does not verify licenses. Confirm on the source page. |
| Historic or factual images | `wikimedia-commons*` | Wide coverage of real things | Each file has its own license. Share-alike can reach a derivative. |

## Decision rules

1. Ask the user for real photographs before any search. One real photo of the real product outweighs ten stock photos.
2. Read the license on the item's own page. A stock site has more than one license in use.
3. Record the item page URL and the maker's name. Do not record a file-delivery URL.
4. Answer question 8 of the license decision for every photo: who and what is in the frame?
5. Do not use an identifiable person in a testimonial, a health, a money or a legal context. A stock license clears no likeness.
6. Reject a photo that shows a logo, a product with a known shape, a screen with someone's interface, or an artwork.
7. A non-commercial or no-derivatives item is blocked for client work. Filter for it in a media search.
8. A share-alike item that you merge into a composite is `needs a human`.
9. Download, optimize and self-host. Set real pixel sizes for each breakpoint.
10. Give the maker a credit line in `ATTRIBUTION.md` even when none is required. Default.
11. Pull single items by hand or through one item call. Never bulk-download, never scrape, never build a set.
12. An API key is a credential. Ask the user for it. Never write it into a file.

Treatment rules that tie stock to a brand:

- Crop for a point of view. A centered subject at the original crop is the stock look.
- Use one treatment across the product: a duotone from two brand tokens, one grade, or one grain.
- Keep text off busy areas. Text on a photo must still meet the contrast floor. Check the real pixels.
- Run the swap question: "Could this photo sit on a competitor's page?" When yes, replace it or reduce its role.

## Video rules

- A background clip needs a poster frame, a muted track and a pause control.
- Honor reduced motion: show the poster frame, not the clip.
- Budget the file weight with `website-design`. Footage is the heaviest asset on most pages.
- Read the license for the music inside a clip too. Music terms differ from footage terms.
- Editing, captions and export belong to `motion-video`.

## License traps

- "Free to use" on stock sites comes with no-resale, no-competing-service and no-model-training clauses.
- A stock site's paid tier and its free tier are different licenses on similar pages.
- Museum open access covers only the objects flagged as public domain. The museum's name and logo are not covered.
- A media search engine reports a license. It does not confirm it.
- Images of art can carry rights of the photographer in some places. Use the institution's own open-access file.

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Handshake stock | A staged scene that fits any company | Use a real photo, or remove the image |
| Unchecked frame | A logo, a face or a screen that nobody looked at | Run question 8. Replace the photo. |
| Saved from search | A file saved from a results grid, origin unknown | `FILE_UNRECORDED`. Find the item page or replace it. |
| Remote hero | The hero image loads from a stock host | Self-host. `check --scan` reports it. |
| Autoplay with no way out | Moving footage with no pause control and no reduced-motion path | Add both |
| Mixed grades | Warm, cool and black-and-white photos on one page | Apply one treatment |

## Worked choice

The outcomes below are illustrative. They show the reasoning, not verified facts about a source.

Need: a hero image for a private bank's wealth-planning page. Brand words: patient, exact, discreet. Ships in a client product.

- The client has no photography that fits.
- Stock people in an office fail the swap question, and a face beside money claims breaks rule 5.
- Catalog: `A search <catalog> --group photo-video --query "public domain artwork" --commercial --verified`.
- Chosen: a still-life painting from a museum's open-access collection. The object record carries the public domain flag.
- Verdict `clear`. Question 8: no person, no mark. A citation is requested: it goes in `ATTRIBUTION.md` and on the credits page.
- Treatment: a tight crop on one detail and a duotone from two brand tokens. Recorded with `--modified`.
