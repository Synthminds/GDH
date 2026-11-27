# Group: print models

Catalog group `print-models`: 3D-print model repositories and model search. Read this file at step 6 of `find-assets` when the need is a model to print, a part to adapt, or a dimension to model against.

How to read this file. An id is a catalog id. An id marked `*` has `verifiedOn` null: read its license before use. The `access` value and the search link template of each source live in `print-design`'s `references/model-sites.json`, under the same id. That skill's `scripts/model_search.py` builds the search links. Evidence: the terms and license pages were read on 2026-11-27; no download ran in a GDH session.

Modeling, checking and slicing belong to `print-design`. This file covers finding, access and license.

## Access comes before search

Most print-model sites forbid automated access in their terms. The `access` value says what the agent may do:

| Access | The agent may | Sources |
| --- | --- | --- |
| `api` | Query the official API with the user's own key or token | `thingiverse`, `smithsonian-3d`, and `sketchfab*` from group `3d` |
| `fetch` | Fetch the search page and read results | `yeggi`, `nih-3d`, `nasa-3d` |
| `links-only` | Build the search link and hand it to the user. Never fetch, scrape or download | `printables`, `makerworld`, `cults3d`, `myminifactory`, `thangs`, `grabcad`, `mcmaster-cad` |

GATE: a `links-only` site is opened by the user in their own browser. The agent never fetches its pages, even to read a license. The user pastes the license line or a screenshot, or downloads the file into the project.

GATE: an API key or token is the user's. Never ask for it in chat. In a cloud session, ask through the credential tool for the API host.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| Free, commercially usable functional parts | `thingiverse` | The largest sanctioned API; filter to CC0, CC BY and CC BY-SA | NC and ND licenses are common. Read each one. |
| A model for a Bambu printer with a ready print profile | `makerworld` | 3MF with profiles; opens in Bambu Studio | Links only. The common default license forbids selling prints. |
| The widest community catalog | `printables` | Large, well-moderated | Links only. Its own community license limits remixes. |
| Decor, figures, cosplay; commercial print licenses | `cults3d` | Clear commercial-use license options | Links only. Many models are paid. |
| Tabletop miniatures and sculpture | `myminifactory` | Curated, high quality | Mostly paid. Store files forbid selling prints. |
| One search across many sites | `yeggi`, `thangs` | Finds the model wherever it lives | Index only. Apply the source site's access and license. |
| Museum objects and specimens | `smithsonian-3d` | CC0 scans | Rarely STL. Needs repair and a base. |
| Space hardware and planets | `nasa-3d` | Many print-ready models | Insignia are not public domain. |
| Medical and scientific models | `nih-3d` | Specialist catalog | License per entry. Not medical devices. |
| Engineering reference geometry in STEP | `grabcad` | Large engineering catalog | Non-commercial internal use only. |
| Exact sizes of bought hardware | `mcmaster-cad` | Manufacturer dimensions | Reference only. Never print or share this CAD. |

## Decision rules

1. Prefer a license that allows what the user will do. Selling prints needs a commercial license; publishing a remix needs a license without ND.
2. Accept for a product without question: CC0, CC BY, CC BY-SA (keep the share-alike on the file), Cults commercial use. Everything else goes to `license-decision.md`.
3. Record the parent model of every remix: site, URL, author, license, date read. Share-alike and the Open Community License carry over to the remix.
4. A CC license on fan art of a trademarked character does not clear the trademark. Treat fan art as personal use only.
5. A paid model in the results is not free. Name the price and the license before the user buys.
6. A downloaded model is a draft. Run the `print-design` mesh check before slicing.
