# Vet a source outside the catalog

Read this file at step 7 of `find-assets`. Use it when tiers 1 to 4 give no fit and you search the web. It has two parts: how to search, and how to vet a source nobody in this kit has read.

A source found on the web is unknown. Unknown means blocked until the vetting passes. The vetting takes five checks and produces one note.

## Part 1. Search the web

Use the host's web search tool. A search call can be billed: apply the spend gate when the tool says so.

Query patterns that find primary sources:

| Goal | Pattern | Why |
| --- | --- | --- |
| A public domain asset | `<subject> <kind> CC0` or `<subject> public domain open access` | Finds museum, agency and curated public domain libraries |
| An open-source library | `<need> library license site:github.com` | Lands on the repository, where the license file is |
| An author's own release | `<subject> <kind> free commercial use license` plus the format | Finds a maker's own site more often than an aggregator |
| A government or institution source | `<subject> open data` or `<subject> open access images` | Institutions publish terms on their own domain |
| A named item's origin | The item's exact title in quotes, plus `license` | Finds the first publisher of a file that aggregators copy |

Search rules:

1. Prefer the maker's own domain or repository over any list, mirror or aggregator.
2. Treat an image search result as a lead to a page. The result grid states no license.
3. Skip sites that hold other people's work with no named author: wallpaper sites, "free PNG" sites, logo dump sites.
4. Skip a preview with a watermark. A watermark means that the file is for sale.
5. A list of "free" resources is a lead. It is not a source and it is not a license statement.
6. Stop after three candidate sources. Vet them before you search more.
7. Search for single items. Never crawl a site, never bulk-download and never build a set from one source.

## Part 2. The five checks

Run them in order. One failed check ends the vetting with verdict `blocked`.

### Check 1. Who publishes it

Find the name behind the source: a person, a studio, a company or an institution.

- Read the about page, the footer, the repository owner and the contact page.
- Decide which one it is: the author, a curator who names each author, or an aggregator.
- For a repository: confirm that it is the original, not a fork or a mirror. Look at the owner, the history and the link from the project's site.
- For a package: confirm that the registry page links to that repository.

Pass: a named publisher who is the author, or a curator who names the author of each item.
Fail: no named publisher, or an aggregator that cannot say who made the item.

### Check 2. License text on its own domain

Find a license or terms text that you can open and cite by URL.

- Look for `/license`, `/terms`, a `LICENSE` file, or a license block on the item page.
- The text must sit on the source's own domain or in its own repository.
- A license claimed for the source by another site does not count.
- Read the whole text. Note its version or its date when it has one.

Pass: you opened the text today and can state its URL.
Fail: no text, a broken link, or a text you could not open. An unopened text is unread.

### Check 3. Per-asset license variation

Find out whether every item carries the same terms.

- Look at three item pages. Compare their license lines.
- Look for a free tier beside a paid tier. Paid items follow other terms.
- Look inside a bundle. A component can ship someone else's font, photo or icon set.
- For code, read the license of each dependency the item adds.

Pass: uniform terms, or each item shows its own license and you read the one for your item.
Fail: mixed terms with no license line on the item.

### Check 4. Trademark and likeness risk

Look at the asset itself, not at the license.

- Does it show a logo, a product with a known shape, a character, an artwork or a known building?
- Does it show a person who can be identified?
- Is the asset itself a brand mark, or a copy of one?

Pass: none of these, or the use stays inside the limits in `license-decision.md`, "Marks, people and logos".
Fail: the use needs a permission that the license cannot give.

### Check 5. Model training and resale clauses

Search the license text for these words. Read every sentence that holds one.

```
AI   machine learning   dataset   scrape   automated   sublicense   resell   redistribute
template   compete   competing   merchandise   print on demand   endorse   trademark
non-commercial   attribution   terminate   revoke   employees   revenue
```

- A training or dataset clause limits what an agent may do with the asset. See "Model training and bulk clauses" in `license-decision.md`.
- A resale or competing-product clause decides the P3 and P4 profiles.
- A headcount or revenue clause needs a fact about the client. ASK for it.
- A terminate or revoke clause means that the terms can end. Record the date and the version.

Pass: no clause blocks this project's use profile.
Fail: a clause blocks it, or a clause is unclear. An unclear clause is `needs a human`.

## A further check for code

A registry item or a package is third-party code that runs in the user's project.

1. Read the source before you install it. Look for an install script, a network call and obfuscated code.
2. Count the dependencies it adds. Each one is another license and another risk.
3. Prefer a copy-in item that you can read in full over a package you cannot.
4. Hand a new dependency to the coding harness for its own review when one is loaded.
5. A registry index lists many registries. Each registry sets its own license. Vet the registry, then the item.

## The vetting note

Write the note in the closing report. Keep it with the manifest entry when the asset enters: put the deciding clauses in `note`.

```
Source: <name>, <URL>
Publisher: <who> (author | curator | aggregator | unknown)
License text: <URL>, read <YYYY-MM-DD>, version <v or none>
Per-asset terms: <uniform | varies: shown on each item | varies: not shown>
Marks and likeness: <none seen | list>
Training and resale clauses: <own-words summary with clause location | none found>
Code review: <not code | read: <n> files, <n> dependencies, no install script>
Verdict: usable | usable with duties: <list> | needs a human: <clause> | blocked: <reason>
Evidence: VERIFIED license text read today | UNTESTED <what was not checked>
```

A vetted source still needs the license decision for the exact item. The note covers the source. The nine questions cover the item and the use.

## Add a good source to the catalog

When a source passes and is likely to serve again, propose it for the catalog.

- Hand it to `add-design-tool`. That skill owns catalog changes.
- Give it the vetting note and the fields: id, name, url, group, holds, license, attribution, commercialUse, fetch, risk.
- Set `verifiedOn` to the day you read the text. Leave it null when you did not read it.

## Failure patterns

| Name | What happens | The test that catches it |
| --- | --- | --- |
| License by reputation | "It is on a code host, so it is open source." | Check 2: state the URL of the text you read |
| Badge trust | A badge or a registry field is taken as the license | Compare the field with the license file in the repository |
| Aggregator laundering | A file is taken from a site that copied it from its maker | Check 1: name the author. Search the title for the first publisher. |
| Whole-site assumption | One license page is applied to every item | Check 3: open three item pages |
| Preview copying | Code or art is copied from the preview of a paid product | Look for a price or a paid tier. A preview grants nothing. |
| Fork drift | An old fork or an old package still shows the old license | Read the license at the version you install, in the original repository |
| Free means free | "Free" is read as "free to redistribute" | Check 5: search for `redistribute` and `resell` |
| Credit as permission | A credit line is added to an asset with no license | A credit repairs nothing. Verdict `blocked`. |
| Search result as source | An image is saved from a result grid | Rule 2 of the search rules: open the page |

## Worked example

The outcomes in this example are illustrative. They show the order of work, not the terms of any real source.

Need: a satellite-style texture of sea ice for a climate report cover. Tiers 1 to 4 give no fit: the catalog's space-agency entry is unread.

1. Query: `sea ice satellite image open access`. The first results are an agency image library and two wallpaper sites.
2. Skip the wallpaper sites: no named author.
3. Check 1: the agency is the publisher and names the instrument and the date for each image. Pass.
4. Check 2: the agency's media guidelines page opens. It is on the agency's own domain. Pass.
5. Check 3: the guidelines say that some images belong to third parties and are marked. The chosen image carries no such mark. Pass.
6. Check 4: the image shows no person and no mark. The guidelines protect the agency's insignia. The cover will not show it. Pass.
7. Check 5: the text asks for a credit and forbids any suggestion of endorsement. No training clause. Pass with a duty.
8. Verdict: `usable with duties: credit line; no insignia; no endorsement wording`.
9. Then run the nine questions for this image and the P1 profile, fetch the file from the item page, and record it.

The note says VERIFIED for the license text and UNTESTED for the third-party mark check on any other image.
