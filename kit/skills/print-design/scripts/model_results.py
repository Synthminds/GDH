#!/usr/bin/env python3
"""model_results.py: turn model-site API responses into one result list and an image gallery.

The agent calls each site's official API and saves the raw JSON response. This script reads those
files, maps them to one record shape, reads each license into plain terms, and writes a gallery
page with a thumbnail, the title, the author, the license verdict and the links for each model.

Commands:
  normalize  Map one saved API response to records. Sources: thingiverse-search, thingiverse-thing,
             sketchfab-search, sketchfab-model, smithsonian, records (records already in GDH shape).
  merge      Join record files, drop duplicates, apply details from thing or model responses.
  license    Read one license string into plain terms.
  gallery    Write a self-contained HTML gallery from a record file.

Exit codes: 0 pass, 1 findings, 2 usage or an unreadable file.
Standard library only. No network: it never fetches a response, an image or a model file.
"""
import argparse
import html
import json
import os
import re
import sys
from urllib.parse import urlparse

RECORD_FIELDS = ("id", "site", "title", "author", "pageUrl", "thumbnail", "license", "downloadable", "files")
MAX_RECORDS = 500

# ---------------------------------------------------------------- licenses

# Each rule: (pattern, label, sell prints, remix, credit, note). Order matters: first match wins.
LICENSE_RULES = [
    (r"\bnc\b|non[- ]?commercial", "Non-commercial", "no", None, "required", "No selling prints or files."),
    (r"\bcc0\b|public domain|\bpd\b", "Public domain (CC0)", "yes", "yes", "none", ""),
    (r"\bby[- ]?sa\b|share[- ]?alike", "CC BY-SA", "yes", "yes-share-alike", "required",
     "A published remix keeps the same license."),
    (r"\bby[- ]?nd\b|no[- ]?deriv", "CC BY-ND", "yes", "no", "required", "Print as is; publish no modified file."),
    (r"cc[- ]?by\b|creative commons[- ]?attribution\b|\bcc-by\b|attribution", "CC BY", "yes", "yes", "required", ""),
    (r"cults.*\bcu[- ]?nd\b|commercial use.*no deriv", "Cults commercial, no derivatives", "yes", "no", "varies",
     "Sell prints; no remix; no file resale."),
    (r"cults.*\bcu\b|commercial use", "Commercial use", "yes", "yes", "varies", "Sell prints; no file resale."),
    (r"cults.*\bpu\b|private use|personal use", "Private use", "no", "no", "varies", "Personal prints only."),
    (r"standard digital file|\bsdfl\b", "Standard Digital File License", "no", "no", "varies",
     "No sharing or selling files or prints."),
    (r"open community license|\bocl\b", "Open Community License", "check", "yes-share-alike", "required",
     "Commercial limits apply; read it. A remix keeps the license."),
    (r"\bl?gpl\b|gnu", "GNU GPL family", "yes", "yes-share-alike", "notice", "Keep the license with shared files."),
    (r"cern[- ]?ohl", "CERN OHL", "yes", "yes-share-alike", "notice", "Read the variant: S and W are copyleft."),
    (r"\bmit\b|\bbsd\b|apache", "Permissive (MIT, BSD, Apache)", "yes", "yes", "notice", "Keep the notice."),
    (r"sketchfab (standard|license)|editorial", "Sketchfab Standard or Editorial", "check", "check", "varies",
     "Read the license page."),
]


def read_license(text):
    """Plain terms for a license string. Unknown text gives 'unknown', never a guess of yes."""
    raw = (text or "").strip()
    low = raw.lower()
    result = {"raw": raw, "label": "Unknown", "sellPrints": "unknown", "remix": "unknown",
              "credit": "unknown", "note": "Read the license on the model page."}
    if not raw:
        return result
    for pattern, label, sell, remix, credit, note in LICENSE_RULES:
        if re.search(pattern, low):
            remix_value = remix
            if remix is None:  # NC: remix depends on ND and SA in the same string
                remix_value = "no" if re.search(r"\bnd\b|no[- ]?deriv", low) else (
                    "yes-share-alike" if re.search(r"\bsa\b|share", low) else "yes")
            result.update({"label": label, "sellPrints": sell, "remix": remix_value, "credit": credit,
                           "note": note})
            return result
    return result


def verdict(lic, use):
    """'ok', 'no' or 'check' for an intended use: personal, sell, remix."""
    if use == "personal":
        return "check" if lic["sellPrints"] == "unknown" else "ok"
    key = "sellPrints" if use == "sell" else "remix"
    value = lic[key]
    if value in ("yes", "yes-share-alike"):
        return "ok"
    if value == "no":
        return "no"
    return "check"


# ---------------------------------------------------------------- normalizers

def g(obj, *path, default=None):
    """Safe nested get over dicts and list indexes."""
    for key in path:
        if isinstance(obj, dict):
            obj = obj.get(key)
        elif isinstance(obj, list) and isinstance(key, int) and -len(obj) <= key < len(obj):
            obj = obj[key]
        else:
            return default
        if obj is None:
            return default
    return obj


def https_or_none(value):
    if isinstance(value, str) and value.startswith("https://") and urlparse(value).netloc:
        return value
    return None


def record(site, rid, title, author, page, thumb, license_text, downloadable, files=None):
    return {"id": "%s:%s" % (site, rid), "site": site, "title": str(title or "Untitled")[:200],
            "author": str(author or "unknown")[:120], "pageUrl": https_or_none(page),
            "thumbnail": https_or_none(thumb), "license": read_license(license_text),
            "downloadable": bool(downloadable), "files": files or []}


def thingiverse_hits(doc):
    if isinstance(doc, dict):
        doc = doc.get("hits") or doc.get("results") or []
    return doc if isinstance(doc, list) else []


def norm_thingiverse_search(doc):
    out = []
    for hit in thingiverse_hits(doc):
        if not isinstance(hit, dict) or hit.get("id") is None:
            continue
        out.append(record("thingiverse", hit["id"], hit.get("name"), g(hit, "creator", "name"),
                          hit.get("public_url") or hit.get("url"),
                          hit.get("preview_image") or hit.get("thumbnail"), hit.get("license"), True))
    return out


def norm_thingiverse_thing(doc):
    if not isinstance(doc, dict) or doc.get("id") is None:
        return []
    files = []
    for f in doc.get("files") or doc.get("zip_data", {}).get("files", []) or []:
        if isinstance(f, dict) and f.get("name"):
            files.append({"name": str(f["name"])[:200], "size": f.get("size"),
                          "url": https_or_none(f.get("download_url") or f.get("url"))})
    return [record("thingiverse", doc["id"], doc.get("name"), g(doc, "creator", "name"),
                   doc.get("public_url"), doc.get("thumbnail") or doc.get("preview_image"),
                   doc.get("license"), True, files)]


def sketchfab_thumb(item):
    images = g(item, "thumbnails", "images", default=[]) or []
    images = [i for i in images if isinstance(i, dict) and i.get("url")]
    if not images:
        return None
    # Pick the image closest to 640 px wide.
    best = min(images, key=lambda i: abs((i.get("width") or 0) - 640))
    return best["url"]


def sketchfab_license(item):
    lic = item.get("license")
    if isinstance(lic, dict):
        return lic.get("label") or lic.get("slug") or lic.get("fullName")
    return lic


def norm_sketchfab_one(item):
    if not isinstance(item, dict) or not item.get("uid"):
        return None
    return record("sketchfab", item["uid"], item.get("name"),
                  g(item, "user", "displayName") or g(item, "user", "username"),
                  item.get("viewerUrl"), sketchfab_thumb(item), sketchfab_license(item),
                  item.get("isDownloadable", False))


def norm_sketchfab_search(doc):
    items = doc.get("results", []) if isinstance(doc, dict) else []
    return [r for r in (norm_sketchfab_one(i) for i in items) if r]


def norm_sketchfab_model(doc):
    r = norm_sketchfab_one(doc)
    return [r] if r else []


def norm_smithsonian(doc):
    rows = g(doc, "response", "rows", default=[]) or []
    out = []
    for row in rows:
        content = row.get("content", {}) if isinstance(row, dict) else {}
        media = g(content, "descriptiveNonRepeating", "online_media", "media", default=[]) or []
        has_3d = any("3d" in str(m.get("type", "")).lower() for m in media if isinstance(m, dict))
        if not has_3d:
            continue
        thumb = next((m.get("thumbnail") for m in media if isinstance(m, dict) and m.get("thumbnail")), None)
        cc0 = any(g(m, "usage", "access") == "CC0" for m in media if isinstance(m, dict))
        files = [{"name": str(m.get("idsId") or m.get("type"))[:200], "size": None,
                  "url": https_or_none(m.get("content"))}
                 for m in media if isinstance(m, dict) and "3d" in str(m.get("type", "")).lower()]
        out.append(record("smithsonian-3d", row.get("id") or row.get("url"), row.get("title"),
                          g(content, "freetext", "dataSource", 0, "content") or "Smithsonian",
                          g(content, "descriptiveNonRepeating", "record_link"), thumb,
                          "CC0" if cc0 else "", cc0, files))
    return out


def norm_records(doc):
    items = doc.get("records", doc) if isinstance(doc, dict) else doc
    out = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict) or not item.get("site") or not item.get("title"):
            continue
        lic = item.get("license")
        lic_text = lic.get("raw") if isinstance(lic, dict) else lic
        rid = item.get("id", "").split(":", 1)[-1] or item.get("pageUrl") or item["title"]
        r = record(item["site"], rid, item["title"], item.get("author"), item.get("pageUrl"),
                   item.get("thumbnail"), lic_text, item.get("downloadable", False), item.get("files"))
        out.append(r)
    return out


NORMALIZERS = {
    "thingiverse-search": norm_thingiverse_search,
    "thingiverse-thing": norm_thingiverse_thing,
    "sketchfab-search": norm_sketchfab_search,
    "sketchfab-model": norm_sketchfab_model,
    "smithsonian": norm_smithsonian,
    "records": norm_records,
}


def merge(lists):
    """Join record lists in order. A later record with the same id fills fields the earlier one lacks."""
    by_id, order = {}, []
    for records in lists:
        for r in records:
            if r["id"] not in by_id:
                by_id[r["id"]] = dict(r)
                order.append(r["id"])
                continue
            base = by_id[r["id"]]
            for key in ("pageUrl", "thumbnail"):
                base[key] = base[key] or r[key]
            if base["license"]["label"] == "Unknown" and r["license"]["label"] != "Unknown":
                base["license"] = r["license"]
            if r["files"]:
                base["files"] = r["files"]
            base["downloadable"] = base["downloadable"] or r["downloadable"]
    return [by_id[i] for i in order][:MAX_RECORDS]


# ---------------------------------------------------------------- gallery

CSS = """
:root { --bg: #f6f5f2; --card: #ffffff; --ink: #1d1d1b; --muted: #5e5c57; --line: #dedbd3;
  --ok: #1e6b3a; --ok-bg: #e3f1e7; --no: #8a1c1c; --no-bg: #f6e1e1; --check: #7a5a00; --check-bg: #f7efd5;
  --accent: #2a4d8f; }
@media (prefers-color-scheme: dark) { :root { --bg: #151514; --card: #201f1d; --ink: #ecebe6; --muted: #a8a59d;
  --line: #34322e; --ok: #8fd3a5; --ok-bg: #1c3324; --no: #f0a3a3; --no-bg: #3a1d1d; --check: #e8cc7a;
  --check-bg: #362d12; --accent: #9db8ef; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 15px/1.45 system-ui, sans-serif; }
header, main, section.more { max-width: 1180px; margin: 0 auto; padding: 20px 16px; }
h1 { font-size: 22px; margin: 0 0 4px; }
p.sub { color: var(--muted); margin: 0; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 10px; overflow: hidden;
  display: flex; flex-direction: column; }
.thumb { aspect-ratio: 4 / 3; background: var(--line); display: grid; place-items: center; color: var(--muted); }
.thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.body { padding: 12px; display: flex; flex-direction: column; gap: 6px; flex: 1; }
.num { font-weight: 700; color: var(--muted); font-variant-numeric: tabular-nums; }
.title { font-weight: 600; }
.meta { color: var(--muted); font-size: 13px; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { font-size: 12px; padding: 2px 8px; border-radius: 999px; border: 1px solid var(--line); }
.ok { color: var(--ok); background: var(--ok-bg); border-color: transparent; }
.no { color: var(--no); background: var(--no-bg); border-color: transparent; }
.check { color: var(--check); background: var(--check-bg); border-color: transparent; }
.actions { margin-top: auto; display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 14px; }
.actions > * { white-space: nowrap; }
.actions span { color: var(--muted); }
a { color: var(--accent); }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
ul.links { columns: 2 220px; padding-left: 18px; }
"""

WORDS = {"ok": "yes", "no": "no", "check": "check"}


def esc(value):
    return html.escape(str(value), quote=True)


def card(index, r, use):
    lic = r["license"]
    sell, remix = verdict(lic, "sell"), verdict(lic, "remix")
    thumb = ('<img src="%s" alt="%s" loading="lazy" referrerpolicy="no-referrer">' % (esc(r["thumbnail"]), esc(r["title"]))
             if r["thumbnail"] else "no image")
    actions = []
    if r["pageUrl"]:
        actions.append('<a href="%s" rel="noopener noreferrer" target="_blank">Open on %s</a>' % (esc(r["pageUrl"]), esc(r["site"])))
    direct = [f for f in r["files"] if f.get("url")]
    if direct:
        actions.append("<span>%d file%s via API</span>" % (len(direct), "" if len(direct) == 1 else "s"))
    elif r["downloadable"]:
        actions.append("<span>download via API</span>")
    focus = verdict(lic, use)
    return """<article class="card" id="m%d">
<div class="thumb">%s</div>
<div class="body">
<div><span class="num">#%d</span> <span class="title">%s</span></div>
<div class="meta">%s on %s</div>
<div class="chips"><span class="chip %s">%s</span><span class="chip %s">sell prints: %s</span><span class="chip %s">remix: %s</span></div>
<div class="meta">%s%s</div>
<div class="actions">%s</div>
</div></article>""" % (index, thumb, index, esc(r["title"]), esc(r["author"]), esc(r["site"]),
                       focus, esc(lic["label"]), sell, WORDS[sell], remix, WORDS[remix],
                       esc(("credit: %s. " % lic["credit"]) if lic["credit"] not in ("none", "unknown") else ""),
                       esc(lic["note"]), "".join(actions))


def gallery(records, query, use, more_links):
    cards = "\n".join(card(i + 1, r, use) for i, r in enumerate(records))
    more = ""
    if more_links:
        items = "".join('<li><a href="%s" rel="noopener noreferrer" target="_blank">Search %s</a></li>'
                        % (esc(link["link"]), esc(link["name"])) for link in more_links
                        if https_or_none(link.get("link")))
        more = ('<section class="more"><h2>Browse on other sites</h2><p class="sub">These sites are browsed by you. '
                'Download a file you like into the part\'s source folder and tell the agent its number or name.</p>'
                '<ul class="links">%s</ul></section>' % items)
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer"><title>Model finds: %s</title><style>%s</style></head>
<body><header><h1>Model finds: %s</h1>
<p class="sub">%d results. Licence chips read each licence for: %s. Tell the agent the numbers you want, for example "use #3, adapt #7".</p>
</header><main><div class="grid">
%s
</div></main>%s</body></html>
""" % (esc(query), CSS, esc(query), len(records), esc(use), cards, more)


# ---------------------------------------------------------------- command line

def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command")
    p_norm = sub.add_parser("normalize", help="map one saved API response to records")
    p_norm.add_argument("--source", required=True, choices=sorted(NORMALIZERS))
    p_norm.add_argument("path")
    p_norm.add_argument("--out", help="write records here; default prints them")
    p_merge = sub.add_parser("merge", help="join record files")
    p_merge.add_argument("paths", nargs="+")
    p_merge.add_argument("--out", required=True)
    p_lic = sub.add_parser("license", help="read one license string")
    p_lic.add_argument("text", nargs="+")
    p_gal = sub.add_parser("gallery", help="write an HTML gallery")
    p_gal.add_argument("path", help="a record file")
    p_gal.add_argument("--out", required=True)
    p_gal.add_argument("--query", default="models")
    p_gal.add_argument("--use", choices=("personal", "sell", "remix"), default="personal")
    p_gal.add_argument("--plan", help="model_search.py plan --json output, for the browse-yourself links")
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_usage(sys.stderr)
        return 2
    try:
        if args.command == "license":
            print(json.dumps(read_license(" ".join(args.text)), indent=2))
            return 0
        if args.command == "normalize":
            records = NORMALIZERS[args.source](load_json(args.path))
            payload = {"version": 1, "records": records}
            if args.out:
                write_json(args.out, payload)
                print("normalize: %d record(s) to %s" % (len(records), args.out))
            else:
                print(json.dumps(payload, indent=2))
            return 0
        if args.command == "merge":
            lists = [norm_records(load_json(p)) for p in args.paths]
            records = merge(lists)
            write_json(args.out, {"version": 1, "records": records})
            print("merge: %d record(s) to %s" % (len(records), args.out))
            return 0
        records = merge([norm_records(load_json(args.path))])
        more = []
        if args.plan:
            plan = load_json(args.plan)
            more = [s for s in plan.get("sites", []) if s.get("access") == "links-only"]
        page = gallery(records, args.query, args.use, more)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(page)
        print("gallery: %d card(s) to %s" % (len(records), args.out))
        return 0
    except (OSError, ValueError) as exc:
        print("cannot read or write: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
