#!/usr/bin/env python3
"""model_search.py: plan a search for a printable model across print-model sites.

For one query it prints, for each site, the search link and what the agent may do there:
  api         query the official API with the user's own key or token
  fetch       fetch the search page and read the results
  links-only  hand the link to the user; never fetch, scrape or download

It joins references/model-sites.json (access and link templates) with the license facts in
kit/catalogs/assets.json under the same id. It makes no network call and fetches nothing.

Commands:
  plan      Print the search plan for a query.
  validate  Check that model-sites.json and assets.json agree. Exit 1 on any finding.

Exit codes: 0 pass, 1 findings, 2 usage or an unreadable file.
"""
import argparse
import json
import os
import re
import sys
from urllib.parse import quote, quote_plus

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SITES = os.path.normpath(os.path.join(HERE, "..", "references", "model-sites.json"))
DEFAULT_ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "catalogs", "assets.json"))
ACCESS = ("api", "fetch", "links-only")
ORDER = {"api": 0, "fetch": 1, "links-only": 2}
COMMERCIAL_OK = ("yes", "yes-with-limits")
MAX_QUERY = 200
DO = {
    "api": "Query the official API with the user's key. Never put the key in chat or a file.",
    "fetch": "Fetch this search page and read the results. Open each result's source site and apply its rule.",
    "links-only": "Give the link to the user. Do not fetch, scrape or download. The user reports the license.",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def clean_query(text):
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        raise ValueError("the query is empty")
    if len(text) > MAX_QUERY:
        raise ValueError("the query is longer than %d characters" % MAX_QUERY)
    return text


def build_link(template, query):
    """Fill {q} in a template. Path-style templates get %20; query-style get +."""
    head = template.split("{q}", 1)[0]
    plus = head.endswith("=") or "yeggi.com/q/" in head  # Yeggi joins words with + in its path
    encoded = quote_plus(query) if plus else quote(query, safe="")
    return template.replace("{q}", encoded)


def validate(sites_doc, assets_doc):
    findings = []

    def add(code, where, message):
        findings.append({"code": code, "where": where, "message": message})

    if not isinstance(sites_doc, dict) or sites_doc.get("version") != 1 or not isinstance(sites_doc.get("sites"), list):
        add("SCHEMA", "model-sites.json", "needs version 1 and a 'sites' list")
        return findings
    sources = {s.get("id"): s for s in (assets_doc or {}).get("sources", []) if isinstance(s, dict)}
    seen = set()
    for index, site in enumerate(sites_doc["sites"]):
        where = "sites[%s]" % (site.get("id", index) if isinstance(site, dict) else index)
        if not isinstance(site, dict):
            add("SCHEMA", where, "entry must be an object")
            continue
        sid = site.get("id")
        if sid in seen:
            add("ID", where, "id appears more than once")
        seen.add(sid)
        if sid not in sources:
            add("ID", where, "id is not a source in assets.json")
        if not isinstance(site.get("linkChecked"), bool):
            add("SCHEMA", where, "linkChecked must be true or false")
        if site.get("access") not in ACCESS:
            add("ACCESS", where, "access must be one of %s" % ", ".join(ACCESS))
        url = site.get("searchUrl")
        if not isinstance(url, str) or not url.startswith("https://") or url.count("{q}") != 1:
            add("URL", where, "searchUrl must be an https URL with exactly one {q}")
        elif sid in sources:
            host = url.split("/")[2]
            base = sources[sid].get("url", "").split("/")[2] if "//" in sources[sid].get("url", "") else ""
            if host.replace("www.", "") != base.replace("www.", ""):
                add("URL", where, "search host %s differs from the catalog host %s" % (host, base))
    for sid, source in sources.items():
        if source.get("group") == "print-models" and sid not in seen:
            add("MISSING", sid, "a print-models source has no entry in model-sites.json")
    return findings


def plan(sites_doc, assets_doc, query, access=None, commercial=False):
    sources = {s["id"]: s for s in assets_doc.get("sources", []) if isinstance(s, dict) and "id" in s}
    rows = []
    for site in sites_doc["sites"]:
        if access and site["access"] not in access:
            continue
        source = sources[site["id"]]
        if commercial and source["commercialUse"] not in COMMERCIAL_OK + ("varies",):
            continue
        rows.append({
            "id": site["id"], "name": source["name"], "access": site["access"],
            "link": build_link(site["searchUrl"], query), "do": DO[site["access"]],
            "license": source["license"], "commercialUse": source["commercialUse"],
            "risk": source["risk"], "verifiedOn": source["verifiedOn"],
            "linkChecked": site.get("linkChecked") is True,
        })
    rows.sort(key=lambda r: ORDER[r["access"]])
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sites", default=DEFAULT_SITES)
    parser.add_argument("--assets", default=DEFAULT_ASSETS)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="machine output")
    sub = parser.add_subparsers(dest="command")
    p_plan = sub.add_parser("plan", parents=[common], help="print the search plan for a query")
    p_plan.add_argument("query", nargs="+")
    p_plan.add_argument("--access", action="append", choices=ACCESS, help="only sites with this access")
    p_plan.add_argument("--commercial", action="store_true",
                        help="drop sources whose catalog entry rules out commercial use")
    sub.add_parser("validate", parents=[common], help="check model-sites.json against assets.json")
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_usage(sys.stderr)
        return 2
    try:
        sites_doc, assets_doc = load_json(args.sites), load_json(args.assets)
    except (OSError, ValueError) as exc:
        print("cannot read a catalog: %s" % exc, file=sys.stderr)
        return 2
    findings = validate(sites_doc, assets_doc)
    if args.command == "validate":
        if args.json:
            print(json.dumps({"ok": not findings, "findings": findings}, indent=2))
        else:
            for f in findings:
                print("%s  %s  %s" % (f["code"], f["where"], f["message"]))
            print("validate: %d finding(s)" % len(findings))
        return 1 if findings else 0
    if findings:
        print("model-sites.json has %d finding(s); run validate" % len(findings), file=sys.stderr)
        return 2
    try:
        query = clean_query(" ".join(args.query))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    rows = plan(sites_doc, assets_doc, query, args.access, args.commercial)
    if args.json:
        print(json.dumps({"query": query, "sites": rows}, indent=2))
    else:
        for r in rows:
            print("%-14s %-11s %s%s" % (r["id"], r["access"], r["link"], "" if r["linkChecked"] else "  (link pattern unchecked)"))
        print("plan: %d site(s) for '%s'. links-only sites: hand the link to the user." % (len(rows), query))
    return 0


if __name__ == "__main__":
    sys.exit(main())
