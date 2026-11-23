# License decision

Read this file at step 9 of `find-assets`. Run it for each candidate, before the fetch. Stop at the first failed step and tell the user. This file is working practice. It is not legal advice. When the answer carries real legal weight, the verdict is `needs a human`.

## The one rule

Read the license text itself, today, in one of two places:

- the source's own domain (its license page or terms page), or
- the source's own repository (its license file).

These are not the license text: a badge, a registry `license` field, a search result summary, a blog post, a model's memory, the GDH catalog.

Evidence for the rule (DOCUMENTED, files read on 2026-11-23): two cataloged packages declared one license in their registry field while their repository carried a different one. One carries an added clause that forbids resale. One replaced its license and now forbids logo use.

For a result with status `catalog-verified`, read the license file that ships with the exact item or version you fetch. For every other status, read the text on the source before you fetch.

## Step 1. Classify the pull

| Class | Examples | Read this | Then |
| --- | --- | --- | --- |
| Code dependency | A package, a registry item | The license file in the repository, at the version you install | Record the package and its exact version |
| Copied source | A component pasted from a site, an HTML template | The license of the site or repository, and any header in the file | Keep the copyright header in the file |
| Media asset | Photo, video, illustration, icon, font, 3D model, HDRI, animation file | The license on the page of that exact item | Record the item page, not the home page |
| Reference | A gallery shot, a competitor site, a logo archive | Nothing to clear, because nothing is taken | Record the URL and the lesson only |

Sources where each item sets its own terms need the check for each item: community vector libraries, model libraries, open media search engines, media commons, icon aggregators, font libraries.

## Step 2. Name the use profile

Take it from `design/brief.md`. Ask when it is absent. One project can match several profiles.

| Profile | What it means | Effect |
| --- | --- | --- |
| P1 Client or own product | The asset is part of a product or a site that earns money | Needs commercial use |
| P2 Internal | A prototype or an internal tool that is never sold | The widest choice. Still record it. |
| P3 Resale kit | A template, a UI kit, a design system or an asset pack for sale | Every `yes-with-limits` source is blocked until the user approves in writing |
| P4 Builder tool | A product that lets others build sites, animations or designs | Check every "no competing product" clause |
| P5 Public repository | The files sit in a repository that anyone can clone | That is redistribution. Check it for fonts and media. |
| P6 Logo or trademark | The asset becomes part of a mark | Most stock and icon licenses forbid it. Draw the mark. |
| P7 Model input | The asset trains a model or feeds a dataset | Many free media licenses forbid it. Treat as blocked. |

## Step 3. Answer the nine questions

Answer from the text. For each answer, note the clause in a few of your own words and its URL. "Unknown" is an answer, and it blocks.

| # | Question | Blocks when |
| --- | --- | --- |
| 1 | Is commercial use allowed? | The license is non-commercial and the profile is P1, P3 or P4 |
| 2 | Is modification allowed? | The license forbids derivatives and you will crop, recolor or edit. Some font licenses need consent to modify. |
| 3 | Is attribution required? In what form and where? | You cannot place the credit where the license asks for it |
| 4 | May the file be redistributed: in this repository, in the bundle, to the client? | Profile P5 and the license forbids redistribution. Or the license forbids handing files to a third party. |
| 5 | Is there a field-of-use limit? | The project matches the limit: resale of the asset itself, competing product, entity size, logo use, merchandise |
| 6 | Does a share-alike or copyleft term reach our work? | The term would force the project's own work open and the user has not agreed |
| 7 | Does this exact item differ from the source's default terms? | The item is premium, carries its own license, or bundles someone else's work |
| 8 | What can the license not grant? | A person's likeness, a trademark, a product design, an artwork or a building in the frame |
| 9 | Is the uploader the author? | The source accepts uploads and nothing ties this item to its maker |

Questions 8 and 9 are not license terms. A license from the wrong person, or a license that covers only the photographer's rights, clears nothing else.

## Step 4. Give the verdict

| Verdict | When | What you do |
| --- | --- | --- |
| `clear` | All nine answers are known and none blocks | Fetch and record |
| `clear with duties` | Use is allowed with a duty: a credit, a notice file, a version pin, a headcount limit | Fetch, record, and write each duty in the manifest `note` |
| `needs a human` | An answer depends on a reading of law or contract: share-alike reach, resale of a kit, a likeness, a competing-product clause | Show the clause to the user. Do not fetch. Record the decision in `design/decisions.md`. |
| `blocked` | An answer is unknown, the text cannot be opened, or a term forbids the use | Pick another candidate |

Rules:

- "Probably fine" is not a verdict. An unread or unclear term is `blocked`.
- A user instruction outranks a GDH default. It does not waive this gate. When the user wants a blocked asset, state the clause, ask, and record the user's decision.
- A credit you give by choice never repairs a missing permission.
- The verdict belongs to one item, one use profile and one date. A new profile needs a new verdict.

## License families

Default: the rows below are a general reading to speed up step 3. They are UNTESTED against any one text. The text of the item governs.

| Family | Usual reading | Usual duty |
| --- | --- | --- |
| Public domain dedication (CC0) | Any use, no credit | None. Marks and people in the content are still not cleared. |
| Permissive code (MIT, ISC, BSD, Apache-2.0) | Use, change and ship | Keep the copyright and license notice with redistributed source. Apache-2.0 also has a NOTICE file. |
| Open font (SIL OFL) | Bundle, embed and self-host | Keep the license file with the font. Do not sell the font alone. A reserved font name limits the name of a changed build. |
| Attribution (CC BY) | Any use with credit | Credit with title, author, source and license. Say when you changed it. |
| Share-alike (CC BY-SA) | Any use with credit | A derivative carries the same license. `needs a human` when the asset is merged into owned work. |
| Non-commercial (any NC) | No commercial use | Blocked for P1, P3 and P4 |
| No derivatives (any ND) | Use only unchanged | Blocked when you will edit it |
| Copyleft program (GPL, AGPL) | The program's license reaches code that links to it | Output files you make with the program are yours. Keep an AGPL editor out of a production bundle. |
| Custom "free" license | Free of charge, with limits the publisher chose | Read every clause. Search for the words in `vet-a-source.md`. |
| All rights reserved, or no license | No permission | Reference only |

A credit line in the usual attribution form:

```
"<Title>" by <Author>, <source URL>, licensed under <license name> (<license URL>). <Changes: cropped and recolored.>
```

## Known limits in the catalog

This table is a pointer, not the terms. Read the text. "Read" means that the license file was read for the catalog on 2026-11-23 (DOCUMENTED). "Unread" means that the catalog note comes from a search summary (UNTESTED): treat it as a lead.

| Limit | Catalog ids | State |
| --- | --- | --- |
| No resale of the components themselves; a resale clause added to MIT | `react-bits`, `animate-ui` | Read |
| A second fair-use license: no competing product; a derivative template needs credit and a link | `preline` | Read |
| Custom license, no resale or redistribution as a library or a template | `aceternity-ui` | Unread |
| No use as a logo or a brand mark; no competing icon library | `remix-icon` | Read |
| The collection is public domain, each mark is still a trademark | `simple-icons` | Read |
| Free only for individuals and very small entities; larger entities need a paid license | `remotion` | Read |
| Free and not open source; not for a no-code animation builder that competes with the owner | `gsap` | README read, full text unread |
| The runtime is permissive; the visual editor is AGPL | `theatre` | Read (README and registry) |
| No handing of font files to a third party; changes need consent | `fontshare` | Unread |
| No self-hosting; a client site needs the client's own subscription | `adobe-fonts` | Unread |
| No model training, no scraping, no bulk collection | `unsplash`, `pexels`, `pixabay`, `undraw`, `coolors`, `mobbin` | Unread |
| Two license statements that disagree | `quaternius` | Unread |
| A visible credit when you build on the live API; none for downloaded files | `poly-haven` | Read (README) |
| Attribution required | `html5up`, `hero-patterns`, `storyset`, `rive-community` | Unread |
| Each item sets its own license | `svg-repo`, `sketchfab`, `poly-pizza`, `openverse`, `wikimedia-commons`, `iconify`, `google-fonts`, `shadcn-registry-directory`, `21st-dev` | Mixed |

Licenses change. Two cataloged sources changed terms in the two years before the catalog date. A third states that its terms change at its next major version. Default: read an entry again when its check is older than 180 days, and before first use in a P3 or P4 project.

## Marks, people and logos

- Never build a logo from a stock icon or a stock illustration. Others hold the same file, and several licenses forbid it.
- Use a third-party mark only unchanged, only in a "works with" or a social link context, and only as that brand's guidelines allow.
- Never place a mark in a way that suggests an endorsement.
- A government insignia or seal needs explicit permission.
- A stock photo license does not clear the people, the logos, the products or the artworks in the frame.
- Do not use an identifiable person in a context that suggests they use, endorse or suffer from something.
- A name or a mark the user wants to adopt needs a knockout search. That belongs to `logo-identity`. The search services are in `group-logo-aids.md`.

## Model training and bulk clauses

- You may pull single assets for one project from a source that forbids scraping.
- You may not crawl it, bulk-download it or build a dataset from it.
- Default: when a license forbids machine-learning use, do not pass its assets to a generation tool as a style or content reference. Verdict `needs a human`.
- Some model libraries mark single items as closed to machine-learning use. Read the item page.

## Worked examples

The license outcomes in these examples are illustrative. They show the reasoning, not the terms of a real source.

**1. An icon package for a client product (P1).** Candidate: a stroke icon set from the catalog with status `catalog-verified`. The license file in the installed package is a permissive code license. Q1 yes. Q2 yes. Q3 no credit in the product. Q4 the notice travels inside the package. Q5 none. Q6 none. Q7 uniform. Q8 the set holds no brand marks. Q9 the publisher is the author. Verdict `clear`. Record it with `--package <name>@<version>`.

**2. A free display typeface for a client site in a public repository (P1, P5).** Candidate: a family from a foundry's free library, status `read-license`. The catalog note says: no handing of files to third parties. Read the license page. When the text confirms the note, Q4 blocks: a public repository redistributes the file, and the client is a third party. Verdict `blocked` for this route. Two ways forward: the client downloads its own copy and the repository ignores the font folder, or `typography` picks an open-font-license family of similar character.

**3. A community 3D model for a product hero (P1).** Candidate: one model on a community library, status `read-license`. Read the item page, not the site terms. The item is attribution-licensed. Q3: the credit goes in `ATTRIBUTION.md` and on a credits page. Q7: the item shows no notice against machine-learning use, and none is planned. Q9: the uploader's profile shows the build files and other original work. Verdict `clear with duties`. When Q9 cannot be answered, prefer a public domain model from a curated library.

**4. An animated background in a template the user will sell (P3).** Candidate: a component from a library with a resale clause added to a permissive license. The clause forbids selling the component itself. Whether a paid template that contains it counts is a reading of the clause. Verdict `needs a human`. Offer two alternatives: a library under a plain permissive license, or an effect written from scratch and recorded with `--origin own`.

## What to write down

For each asset that enters, the manifest entry holds:

- `license`: the license name and the URL of the text you read. Example: `CC BY 4.0, https://creativecommons.org/licenses/by/4.0/`.
- `attribution`: the exact credit line, or `none required`.
- `date`: the day you read the text.
- `note`: each duty and each limit that still applies. Example: `Free only for entities up to the size in the license; client confirmed headcount on 2026-11-23.`

For each `needs a human` verdict, and each time the user chooses among candidates, add an entry to `design/decisions.md` in the fixed format:

```
## 2026-11-23 round 4: hero image source
Stage: refine
Shown: A museum still life (public domain); B stock office photo (stock license); C generated image (quote shown)
Feedback asked: Which source fits "patient, exact, discreet", given the license duties of each?
Keep / Change / Remove: Keep A with a tight crop. Remove B. Hold C.
Decision: A (by <who>)
Rejected: B: fails the swap question; shows a face beside money claims
Rejected: C: not needed; no spend approved
Open: where the credits page lives
Evidence: VERIFIED license text of A read 2026-11-23; UNTESTED contrast of text over the crop
```

Before you propose a source, search `design/decisions.md`. Do not propose a rejected source again without new evidence.
