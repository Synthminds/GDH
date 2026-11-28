# Model site APIs

Read this at step 2 when a search uses a site with access `api` in `model-sites.json`. The agent makes the calls; `scripts/model_results.py` turns the saved responses into records and a gallery. GDH scripts make no network calls.

Evidence. Hosts, auth and endpoints come from each site's developer pages, read on 2026-11-27. The response field names in the normalizers follow the public documentation and were tested on fixtures only: UNTESTED against a live response. When a field is missing, the record shows "unknown" or "no image"; fix the normalizer after the first live run.

## Keys

Each API needs the user's own free key or token. Never ask for it in chat, print it, or write it in a file.

| Site | Get the key | Where it goes |
| --- | --- | --- |
| Thingiverse | Create an app on the Thingiverse developer pages; copy its app token | `THINGIVERSE_TOKEN` on the user's machine; in a cloud session, the credential tool for `api.thingiverse.com` |
| Sketchfab | Account settings, API token | `SKETCHFAB_TOKEN`; in a cloud session, the credential tool for `api.sketchfab.com` |
| Smithsonian Open Access | A free api.data.gov key | `SI_API_KEY`; in a cloud session, the credential tool for `api.si.edu` |

A cloud session blocks these hosts until a credential is saved for them. On the user's machine they work at once.

## Calls

Save every raw response under `design/print/<part>/finds/raw/`, one file per call, before you normalize it.

Thingiverse: search, then details and files for the picks.

```
curl -s -H "Authorization: Bearer $THINGIVERSE_TOKEN" \
  "https://api.thingiverse.com/search/<words>?type=things&per_page=24" > raw/thingiverse-search.json
curl -s -H "Authorization: Bearer $THINGIVERSE_TOKEN" \
  "https://api.thingiverse.com/things/<id>" > raw/thingiverse-<id>.json
curl -s -H "Authorization: Bearer $THINGIVERSE_TOKEN" \
  "https://api.thingiverse.com/things/<id>/files" > raw/thingiverse-<id>-files.json
```

The search hits carry no license. Fetch the thing details for every model the user may pick, so its license chip is read and not "unknown". Merge the files list into the thing details before you normalize, under the key `files`.

Sketchfab: search downloadable models only, with a license filter when the use needs one.

```
curl -s "https://api.sketchfab.com/v3/search?type=models&q=<words>&downloadable=true&count=24" \
  > raw/sketchfab-search.json
curl -s -H "Authorization: Token $SKETCHFAB_TOKEN" \
  "https://api.sketchfab.com/v3/models/<uid>/download" > raw/sketchfab-<uid>-download.json
```

Search may work without a token; download needs one. The download response gives short-lived links. Download at once. Sketchfab models are often made for screens: check the mesh closely.

Smithsonian: search, keep CC0 3D items.

```
curl -s "https://api.si.edu/openaccess/api/v1.0/search?q=<words>&api_key=$SI_API_KEY" > raw/smithsonian.json
```

Pass the key in the query only through the environment variable. Never paste it into a command you show.

Fetch sites (`yeggi`, `nih-3d`, `nasa-3d`): read the search page with the session's fetch tool. Write each result into a records file by hand: site, title, author, pageUrl, thumbnail, license. Normalize it with `--source records`.

Links-only sites: build their links with `model_search.py plan` and pass the plan to the gallery, so they appear as browse buttons.

## Make the gallery

```
python3 scripts/model_results.py normalize --source thingiverse-search raw/thingiverse-search.json --out finds/thingiverse.json
python3 scripts/model_results.py normalize --source thingiverse-thing raw/thingiverse-101.json --out finds/thingiverse-101.json
python3 scripts/model_results.py normalize --source sketchfab-search raw/sketchfab-search.json --out finds/sketchfab.json
python3 scripts/model_results.py merge finds/thingiverse.json finds/thingiverse-101.json finds/sketchfab.json --out finds/results.json
python3 scripts/model_search.py plan <words> --json > finds/plan.json
python3 scripts/model_results.py gallery finds/results.json --query "<words>" --use sell \
  --plan finds/plan.json --out finds/index.html
```

`--use` sets the licence verdict on each card: `personal`, `sell` or `remix`. Show the gallery to the user: send the file, or publish it as a private page. Thumbnails load from the sites' image hosts when the page opens; the script downloads nothing.

## Download a pick

1. The user names the cards: "use #3, adapt #7".
2. Read the license again on the record. A card marked "check" needs the model page read first.
3. Download the files through the API into `design/print/<part>/source/`. Thingiverse file links need the token header. Sketchfab links expire; download at once.
4. Record each file in `design/assets/manifest.json`: origin `outside`, site, page URL, author, license, the date, and the parent model of a remix.
5. Run the mesh check before anything else.
