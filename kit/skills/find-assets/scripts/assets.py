#!/usr/bin/env python3
"""assets.py: catalog search and asset provenance for the GDH find-assets skill.

Subcommands:
  search  <catalog.json> [--group G] [--query Q] [--commercial] [--no-attribution]
          Filter and rank the entries of kit/catalogs/assets.json.
  record  <manifest.json> --id --source-url --license --attribution --file --date
          Append one provenance entry for each file, with its sha256.
  check   <manifest.json> --root <project>
          Every file in the asset folders has an entry, every entry has a
          license and a source, and every file matches its sha256.
  notices <manifest.json> -o ATTRIBUTION.md
          Write the third-party notices file from the manifest.

The manifest shape is the one in kit/templates/project/design/assets/manifest.json:
  {"version": 1, "fields": {...}, "assets": [{"id", "sourceUrl", "license",
   "attribution", "date", "path", "sha256"}]}
Optional entry fields: licenseUrl, catalogId, origin (outside | own | generated),
modified, package, note. Optional manifest fields: ignore (a list of globs, or of
{"pattern", "reason"} objects) and hotlinkExceptions ([{"prefix", "reason"}]).
An ignore glob may not cover a whole asset folder, and an ignored file is still
compared with the reference files. check reads the catalog (--catalog, default
the catalogs/assets.json beside the skills folder) and tests each catalogId
entry against the catalog terms.

Python 3.9+, standard library only. No network calls. Writes only the manifest
(record) or the -o path (notices). Exit code 0 on pass, 1 on findings, 2 on a
usage error. --json prints one JSON object on stdout.
"""

import argparse
import datetime
import fnmatch
import hashlib
import json
import os
import re
import sys
from collections import OrderedDict

VERSION = "0.1.0"

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WORD_RE = re.compile(r"[a-z0-9]+")
URL_RE = re.compile(r"https?://[^\s\"'()<>\\`]+", re.I)
HOST_RE = re.compile(r"^https?://([^/?#]+)([^?#]*)", re.I)

CATALOG_FIELDS = ("id", "name", "url", "group", "holds", "license", "attribution",
                  "commercialUse", "fetch", "risk", "verifiedOn")
COMMERCIAL_VALUES = ("yes", "yes-with-limits", "varies", "reference-only", "unknown")
COMMERCIAL_OK = ("yes", "yes-with-limits")
ATTRIBUTION_CLASSES = ("none", "notice", "requested", "required", "varies", "unknown", "n/a")
NO_CREDIT_CLASSES = ("none", "notice", "requested")
ORIGINS = ("outside", "own", "generated")

# Default: a catalog check older than this is read again. The research proposes
# 180 days; it is a starting value, not a verified number.
DEFAULT_MAX_AGE_DAYS = 180

DEFAULT_ASSET_DIRS = ("design/assets", "public", "static", "assets", "src/assets")
DEFAULT_REFERENCE_DIRS = ("design/directions",)
ASSET_EXT = {
    ".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg", ".ico", ".bmp", ".tif", ".tiff",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp4", ".webm", ".mov", ".m4v",
    ".mp3", ".wav", ".ogg", ".m4a", ".flac",
    ".glb", ".gltf", ".obj", ".fbx", ".usdz", ".hdr", ".exr", ".ktx2",
    ".lottie", ".riv",
}
SCAN_EXT = {".html", ".htm", ".css", ".scss", ".less", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx",
            ".vue", ".svelte", ".astro", ".mdx"}
WALK_SKIP = {".git", "node_modules", "__pycache__", ".venv"}
SCAN_SKIP = WALK_SKIP | {"dist", "build", "out", ".next", ".astro", ".svelte-kit", "coverage"}
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "fonts.bunny.net", "api.fontshare.com",
              "cdn.fontshare.com", "use.typekit.net", "p.typekit.net")

STOPWORDS = {"a", "an", "the", "for", "of", "and", "or", "with", "to", "in", "on", "free", "some", "my"}
SYNONYMS = {
    "photo": ("photo", "image", "picture"),
    "image": ("image", "photo", "picture"),
    "picture": ("picture", "photo", "image"),
    "font": ("font", "typeface"),
    "typeface": ("typeface", "font"),
    "video": ("video", "clip", "footage"),
    "illustration": ("illustration", "drawing", "vector"),
    "model": ("model", "gltf", "glb"),
    "texture": ("texture", "pbr", "hdri"),
    "logo": ("logo", "brand", "trademark"),
    "chart": ("chart", "plot"),
    "network": ("network", "graph"),
    "map": ("map", "geo"),
    "animation": ("animation", "animated", "motion"),
    "background": ("background", "pattern", "gradient"),
}
FIELD_WEIGHTS = (("id", 6), ("name", 6), ("holds", 3), ("group", 2), ("fetch", 1), ("license", 1), ("risk", 1))
STATUS_ORDER = {"catalog-verified": 0, "read-license": 1, "blocked": 2, "reference-only": 3}

MANIFEST_FIELDS = OrderedDict([
    ("id", "kebab-case id, unique in this file"),
    ("sourceUrl", "the page the asset came from"),
    ("license", "license name and the URL of the license text that was read"),
    ("attribution", "the exact credit line, or \"none required\""),
    ("date", "YYYY-MM-DD the license was read"),
    ("path", "file path inside the project"),
    ("sha256", "hash of the file"),
])

# One code for each rule. tests/test_assets.py holds a test for each code.
CODES = {
    "MANIFEST_INVALID": "The manifest is absent, does not parse, or has no 'assets' list.",
    "MANIFEST_EXCEPTION": "A hotlink exception has no prefix or no reason.",
    "ENTRY_FIELD": "An entry lacks an id, a source, a license, an attribution, a date, or a file and hash.",
    "ENTRY_ID": "An entry id is not kebab-case.",
    "ENTRY_DUPLICATE_ID": "Two entries share one id.",
    "ENTRY_DUPLICATE_PATH": "Two entries record one file.",
    "ENTRY_DATE": "An entry date is not a real YYYY-MM-DD date.",
    "ENTRY_SOURCE": "An outside asset has a source that is not an http or https URL.",
    "ENTRY_ORIGIN": "An entry origin is not outside, own or generated.",
    "ENTRY_PATH": "An entry path is absolute or leaves the project folder.",
    "FILE_MISSING": "An entry names a file that does not exist.",
    "FILE_HASH": "A file differs from the sha256 in its entry.",
    "FILE_UNRECORDED": "A file in an asset folder has no manifest entry.",
    "REFERENCE_SHIPPED": "A file in an asset folder is a copy of a reference file.",
    "HOTLINK": "A source file loads an asset from a remote URL.",
}


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def posix(path):
    return path.replace(os.sep, "/")


def load_json(path):
    """Return (document, error text)."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh, object_pairs_hook=OrderedDict), None
    except OSError as exc:
        return None, "cannot read %s: %s" % (path, exc.strerror or exc)
    except ValueError as exc:
        return None, "%s is not valid JSON: %s" % (path, exc)


def write_text(path, text):
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def parse_date(text):
    """Return a date for a real YYYY-MM-DD string, else None."""
    if not isinstance(text, str) or not DATE_RE.match(text):
        return None
    try:
        return datetime.date(int(text[0:4]), int(text[5:7]), int(text[8:10]))
    except ValueError:
        return None


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def is_http_url(text):
    return isinstance(text, str) and bool(re.match(r"^https?://[^\s/]+", text))


def emit(args, payload, lines):
    """Print the JSON object or the text lines."""
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        for line in lines:
            print(line)


def usage_error(args, message):
    if getattr(args, "json", False):
        print(json.dumps({"ok": False, "error": message}, indent=2))
    else:
        print("error: %s" % message, file=sys.stderr)
    return 2


def finding(code, message, path="", entry_id="", fix=""):
    return OrderedDict([("code", code), ("path", path), ("id", entry_id), ("message", message), ("fix", fix)])


def finding_lines(findings):
    lines = []
    for item in findings:
        where = item["path"] or item["id"] or "-"
        lines.append("%-22s %s  %s" % (item["code"], where, item["message"]))
        if item["fix"]:
            lines.append("%-22s fix: %s" % ("", item["fix"]))
    return lines


# --------------------------------------------------------------------------
# search
# --------------------------------------------------------------------------

def load_catalog(path):
    """Return (sources, problems). Problems make the catalog unusable."""
    doc, error = load_json(path)
    if error:
        return None, [error]
    sources = doc.get("sources") if isinstance(doc, dict) else None
    if not isinstance(sources, list):
        return None, ["%s needs a 'sources' list" % path]
    problems, seen = [], set()
    for index, source in enumerate(sources):
        label = source.get("id", "#%d" % index) if isinstance(source, dict) else "#%d" % index
        if not isinstance(source, dict):
            problems.append("source %s is not an object" % label)
            continue
        missing = [key for key in CATALOG_FIELDS if key not in source]
        if missing:
            problems.append("source %s lacks: %s" % (label, ", ".join(missing)))
            continue
        if not isinstance(source["id"], str) or not ID_RE.match(source["id"]):
            problems.append("source %s: id is not kebab-case" % label)
        if source["id"] in seen:
            problems.append("source %s: id appears more than once" % label)
        seen.add(source["id"])
        if not (isinstance(source["url"], str) and source["url"].startswith("https://")):
            problems.append("source %s: url is not an https URL" % label)
        if source["commercialUse"] not in COMMERCIAL_VALUES:
            problems.append("source %s: commercialUse must be one of %s" % (label, ", ".join(COMMERCIAL_VALUES)))
        if source["verifiedOn"] is not None and parse_date(source["verifiedOn"]) is None:
            problems.append("source %s: verifiedOn must be null or a YYYY-MM-DD date" % label)
        for key in ("name", "group", "holds", "license", "attribution", "fetch", "risk"):
            if not isinstance(source[key], str):
                problems.append("source %s: %s must be a string" % (label, key))
    return sources, problems


def attribution_class(text):
    head = text.split(":", 1)[0].strip().lower() if isinstance(text, str) else ""
    return head if head in ATTRIBUTION_CLASSES else "unknown"


def entry_status(entry, today, max_age_days):
    """Return (status, reasons, duties) for one catalog entry.

    catalog-verified: the catalog terms are current. Confirm the license file
                      that ships with the item, then fetch and record.
    read-license:     open the license text on the source's own domain first.
    blocked:          no known terms. Do not use until the license is read.
    reference-only:   study it. Nothing from it enters a project.
    """
    use = entry["commercialUse"]
    credit = attribution_class(entry["attribution"])
    duties = []
    if credit == "required":
        duties.append("write the credit line; it is a license condition")
    elif credit == "notice":
        duties.append("keep the license or NOTICE file with the files")
    elif credit == "requested":
        duties.append("a credit is asked for; give it where the layout allows")
    elif credit in ("varies", "unknown"):
        duties.append("find the credit rule of the exact item")
    if use == "reference-only":
        return "reference-only", ["reference only: nothing from this source enters a project"], []
    reasons = []
    verified = parse_date(entry["verifiedOn"]) if entry["verifiedOn"] else None
    if verified is None:
        reasons.append("the license was not read for the catalog")
    elif (today - verified).days > max_age_days:
        reasons.append("the catalog check is older than %d days" % max_age_days)
    if use == "yes-with-limits":
        reasons.append("the license has a use limit: test it against this project")
    elif use == "varies":
        reasons.append("each item sets its own license: check the exact item")
    elif use == "unknown":
        reasons.append("no license terms are known")
    if use == "unknown":
        return "blocked", reasons, duties
    return ("read-license" if reasons else "catalog-verified"), reasons, duties


NEXT_STEP = {
    "catalog-verified": "Confirm the license file that ships with the item. Then fetch and record.",
    "read-license": "Open the license text on the source's own domain and run the license procedure before you fetch.",
    "blocked": "Blocked. Read the license first; with no license text, pick another source.",
    "reference-only": "Study only. Record the URL and the lesson in the direction notes. Take no file.",
}


def query_tokens(query):
    tokens = []
    for word in WORD_RE.findall((query or "").lower()):
        if word in STOPWORDS or word in tokens:
            continue
        tokens.append(word)
    return tokens


def token_variants(token):
    """The token, its singular form and its synonyms."""
    singular = token[:-1] if len(token) > 3 and token.endswith("s") else token
    variants = {token, singular}
    for word in SYNONYMS.get(token, ()) + SYNONYMS.get(singular, ()):
        variants.add(word)
    return variants


def score_entry(entry, tokens):
    """Return (tokens matched, score). A token matches a field when a word in
    the field starts with the token or with one of its variants."""
    words = {}
    for field, _weight in FIELD_WEIGHTS:
        found = WORD_RE.findall(str(entry.get(field, "")).lower())
        joined = "".join(found) if field == "id" else ""
        words[field] = (found, joined)
    matched, score = 0, 0
    for token in tokens:
        best = 0
        variants = token_variants(token)
        for field, weight in FIELD_WEIGHTS:
            found, joined = words[field]
            hit = any(word.startswith(variant) for word in found for variant in variants)
            if not hit and joined:
                hit = any(joined.startswith(variant) for variant in variants)
            if hit and weight > best:
                best = weight
        if best:
            matched += 1
            score += best
    return matched, score


def run_search(sources, groups, query, commercial, no_attribution, verified_only, today, max_age_days):
    tokens = query_tokens(query)
    results = []
    for entry in sources:
        if groups and entry["group"] not in groups:
            continue
        if commercial and entry["commercialUse"] not in COMMERCIAL_OK:
            continue
        if no_attribution and attribution_class(entry["attribution"]) not in NO_CREDIT_CLASSES:
            continue
        status, reasons, duties = entry_status(entry, today, max_age_days)
        if verified_only and status != "catalog-verified":
            continue
        matched, score = score_entry(entry, tokens) if tokens else (0, 0)
        if tokens and not matched:
            continue
        item = OrderedDict((key, entry[key]) for key in CATALOG_FIELDS)
        item["status"] = status
        item["reasons"] = reasons
        item["duties"] = duties
        item["next"] = NEXT_STEP[status]
        item["matched"] = matched
        item["score"] = score
        results.append(item)
    results.sort(key=lambda r: (-r["matched"], -r["score"], STATUS_ORDER[r["status"]],
                                0 if r["verifiedOn"] else 1, r["name"].lower()))
    return results, tokens


def cmd_search(args):
    sources, problems = load_catalog(args.catalog)
    if problems:
        return usage_error(args, "catalog is not usable: " + "; ".join(problems[:5]))
    today = parse_date(args.today) if args.today else datetime.date.today()
    if today is None:
        return usage_error(args, "--today must be a YYYY-MM-DD date")
    known = sorted({entry["group"] for entry in sources})
    groups = []
    for value in args.group or []:
        groups.extend(part.strip() for part in value.split(",") if part.strip())
    unknown = [g for g in groups if g not in known]
    if unknown:
        return usage_error(args, "unknown group %s; groups are: %s" % (", ".join(unknown), ", ".join(known)))
    results, tokens = run_search(sources, groups, args.query, args.commercial, args.no_attribution,
                                 args.verified, today, args.max_age_days)
    total = len(results)
    shown = results if args.limit <= 0 else results[:args.limit]
    filters = OrderedDict([("group", groups), ("query", args.query or ""), ("tokens", tokens),
                           ("commercial", bool(args.commercial)), ("noAttribution", bool(args.no_attribution)),
                           ("verified", bool(args.verified))])
    payload = OrderedDict([("ok", total > 0), ("today", today.isoformat()), ("filters", filters),
                           ("count", total), ("shown", len(shown)), ("groups", known), ("results", shown)])
    lines = ["%d result(s), %d shown (today %s)" % (total, len(shown), today.isoformat())]
    for number, item in enumerate(shown, 1):
        lines.append("%d. %s  %s  [%s]" % (number, item["id"], item["name"], item["group"]))
        lines.append("   commercial: %s | attribution: %s | verified: %s | status: %s"
                     % (item["commercialUse"], item["attribution"], item["verifiedOn"] or "no", item["status"]))
        lines.append("   holds: %s" % item["holds"])
        lines.append("   license: %s" % item["license"])
        lines.append("   fetch: %s" % item["fetch"])
        lines.append("   risk: %s" % item["risk"])
        for reason in item["reasons"]:
            lines.append("   why: %s" % reason)
        for duty in item["duties"]:
            lines.append("   duty: %s" % duty)
        lines.append("   next: %s" % item["next"])
    if not total:
        lines.append("No catalog entry matches. Widen the query, drop a filter, or vet a source outside the catalog.")
        lines.append("groups: %s" % ", ".join(known))
    emit(args, payload, lines)
    return 0 if total else 1


# --------------------------------------------------------------------------
# manifest helpers
# --------------------------------------------------------------------------

def new_manifest():
    return OrderedDict([("version", 1), ("fields", OrderedDict(MANIFEST_FIELDS)), ("assets", [])])


def load_manifest(path, create=False):
    """Return (manifest, error text)."""
    if not os.path.exists(path):
        if create:
            return new_manifest(), None
        return None, "%s does not exist" % path
    doc, error = load_json(path)
    if error:
        return None, error
    if not isinstance(doc, dict) or not isinstance(doc.get("assets"), list):
        return None, "%s needs an 'assets' list" % path
    return doc, None


def default_root(manifest_path):
    """<root>/design/assets/manifest.json gives <root>. Any other place gives the manifest folder."""
    folder = os.path.dirname(os.path.abspath(manifest_path))
    parts = posix(folder).split("/")
    if len(parts) >= 2 and parts[-2:] == ["design", "assets"]:
        return os.path.dirname(os.path.dirname(folder))
    return folder


def relative_inside(root, path):
    """Return the POSIX path of 'path' relative to 'root', or None when it is outside."""
    root_real = os.path.realpath(root)
    path_real = os.path.realpath(path)
    try:
        common = os.path.commonpath([root_real, path_real])
    except ValueError:
        return None
    if common != root_real or path_real == root_real:
        return None
    return posix(os.path.relpath(path_real, root_real))


def validate_entries(assets):
    """Return findings that need no file system."""
    out, ids, paths = [], {}, {}
    for index, entry in enumerate(assets):
        if not isinstance(entry, dict):
            out.append(finding("ENTRY_FIELD", "entry %d is not an object" % (index + 1),
                               fix="Remove it and record the asset again."))
            continue
        entry_id = entry.get("id") if isinstance(entry.get("id"), str) else ""
        label = entry_id or "#%d" % (index + 1)
        path = entry.get("path") if isinstance(entry.get("path"), str) else ""
        has_file = bool(path) and isinstance(entry.get("sha256"), str) and bool(entry.get("sha256"))
        has_package = isinstance(entry.get("package"), str) and bool(entry.get("package").strip())
        missing = [key for key in ("id", "sourceUrl", "license", "attribution", "date")
                   if not (isinstance(entry.get(key), str) and entry.get(key).strip())]
        if not has_file and not has_package:
            missing.append("path and sha256 (or package)")
        if missing:
            out.append(finding("ENTRY_FIELD", "lacks: %s" % ", ".join(missing), path, label,
                               "Read the license, then record the asset again with every field."))
        if entry_id and not ID_RE.match(entry_id):
            out.append(finding("ENTRY_ID", "id '%s' is not kebab-case" % entry_id, path, label,
                               "Use lower-case letters, digits and single hyphens."))
        if entry_id:
            if entry_id in ids:
                out.append(finding("ENTRY_DUPLICATE_ID", "id appears more than once", path, label,
                                   "Give each entry its own id."))
            ids[entry_id] = index
        if path:
            if path in paths:
                out.append(finding("ENTRY_DUPLICATE_PATH", "file is recorded by '%s' and '%s'" % (paths[path], label),
                                   path, label, "Keep one entry for each file."))
            else:
                paths[path] = label
        if isinstance(entry.get("date"), str) and entry.get("date").strip() and parse_date(entry["date"]) is None:
            out.append(finding("ENTRY_DATE", "date '%s' is not a real YYYY-MM-DD date" % entry["date"], path, label,
                               "Write the day the license was read."))
        origin = entry.get("origin", "outside")
        if origin not in ORIGINS:
            out.append(finding("ENTRY_ORIGIN", "origin '%s' is not one of %s" % (origin, ", ".join(ORIGINS)),
                               path, label, "Use outside, own or generated."))
        elif origin == "outside" and isinstance(entry.get("sourceUrl"), str) and entry["sourceUrl"].strip() \
                and not is_http_url(entry["sourceUrl"]):
            out.append(finding("ENTRY_SOURCE", "sourceUrl '%s' is not an http or https URL" % entry["sourceUrl"],
                               path, label, "Record the page the asset came from."))
    return out


# --------------------------------------------------------------------------
# record
# --------------------------------------------------------------------------

def cmd_record(args):
    if parse_date(args.date) is None:
        return usage_error(args, "--date must be a real YYYY-MM-DD date")
    if not ID_RE.match(args.id):
        return usage_error(args, "--id must be kebab-case: lower-case letters, digits and single hyphens")
    files = args.file or []
    if not files and not args.package:
        return usage_error(args, "give --file (one or more) or --package")
    if files and args.package:
        return usage_error(args, "give --file or --package, not both")
    for label, value in (("--source-url", args.source_url), ("--license", args.license),
                         ("--attribution", args.attribution)):
        if not value.strip():
            return usage_error(args, "%s must not be empty" % label)
    if args.origin == "outside" and not is_http_url(args.source_url):
        return usage_error(args, "--source-url must be an http or https URL for an outside asset")
    if args.license_url and not is_http_url(args.license_url):
        return usage_error(args, "--license-url must be an http or https URL")
    manifest, error = load_manifest(args.manifest, create=True)
    if error:
        emit(args, {"ok": False, "findings": [finding("MANIFEST_INVALID", error, args.manifest)]},
             ["MANIFEST_INVALID  %s" % error])
        return 1
    root = os.path.abspath(args.root) if args.root else default_root(args.manifest)
    new_entries = []
    for number, name in enumerate(files, 1):
        if not os.path.isfile(name):
            return usage_error(args, "file not found: %s" % name)
        rel = relative_inside(root, name)
        if rel is None:
            return usage_error(args, "%s is outside the project folder %s; copy it in first or pass --root"
                               % (name, root))
        entry_id = args.id if number == 1 else "%s-%d" % (args.id, number)
        new_entries.append(build_entry(args, entry_id, path=rel, sha256=sha256_file(name)))
    if args.package:
        new_entries.append(build_entry(args, args.id, package=args.package.strip()))
    assets = manifest["assets"]
    findings = []
    for entry in new_entries:
        for position, old in enumerate(list(assets)):
            if not isinstance(old, dict):
                continue
            same_id = old.get("id") == entry["id"]
            same_path = "path" in entry and old.get("path") == entry["path"]
            if not (same_id or same_path):
                continue
            if args.replace and same_id:
                assets[position] = None
            elif same_id:
                findings.append(finding("ENTRY_DUPLICATE_ID", "id '%s' is already recorded" % entry["id"],
                                        entry.get("path", ""), entry["id"],
                                        "Pick a new id, or pass --replace to update the entry."))
            else:
                findings.append(finding("ENTRY_DUPLICATE_PATH", "file is already recorded by '%s'" % old.get("id"),
                                        entry["path"], entry["id"],
                                        "Record again under that id with --replace."))
    if findings:
        emit(args, {"ok": False, "findings": findings}, finding_lines(findings) + ["record: nothing written"])
        return 1
    manifest["assets"] = [a for a in assets if a is not None] + new_entries
    if "version" not in manifest:
        manifest["version"] = 1
    write_text(args.manifest, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    lines = []
    for entry in new_entries:
        target = entry.get("path") or entry.get("package")
        digest = (" sha256 %s" % entry["sha256"][:12]) if "sha256" in entry else ""
        lines.append("recorded  %s  %s%s" % (entry["id"], target, digest))
    lines.append("record: %d entr%s written to %s" % (len(new_entries), "y" if len(new_entries) == 1 else "ies",
                                                      args.manifest))
    emit(args, {"ok": True, "manifest": args.manifest, "recorded": new_entries}, lines)
    return 0


def build_entry(args, entry_id, path=None, sha256=None, package=None):
    entry = OrderedDict([("id", entry_id), ("sourceUrl", args.source_url.strip()),
                         ("license", args.license.strip()), ("attribution", args.attribution.strip()),
                         ("date", args.date)])
    if path is not None:
        entry["path"] = path
        entry["sha256"] = sha256
    if package is not None:
        entry["package"] = package
    if args.license_url:
        entry["licenseUrl"] = args.license_url
    if args.catalog_id:
        entry["catalogId"] = args.catalog_id
    if args.origin != "outside":
        entry["origin"] = args.origin
    if args.modified:
        entry["modified"] = True
    if args.note:
        entry["note"] = args.note
    return entry


# --------------------------------------------------------------------------
# check
# --------------------------------------------------------------------------

def walk_files(root, sub, extensions, skip_dirs):
    """Yield POSIX paths, relative to root, of files under root/sub. Symbolic links are not followed."""
    base = os.path.join(root, sub)
    if not os.path.isdir(base):
        return
    for current, dirs, files in os.walk(base, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in skip_dirs and not os.path.islink(os.path.join(current, d)))
        for name in sorted(files):
            full = os.path.join(current, name)
            if name.startswith(".") or os.path.islink(full):
                continue
            if extensions is not None and os.path.splitext(name)[1].lower() not in extensions:
                continue
            yield posix(os.path.relpath(full, root))


def under(path, folder):
    folder = folder.strip("/")
    return path == folder or path.startswith(folder + "/")


def scan_hotlinks(root, scan_dirs, exceptions):
    """Return (findings, exempted count) for remote asset URLs in source files."""
    out, exempted = [], 0
    for sub in scan_dirs:
        for rel in walk_files(root, sub, SCAN_EXT, SCAN_SKIP):
            try:
                with open(os.path.join(root, rel), "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            for number, line in enumerate(text.split("\n"), 1):
                for match in URL_RE.finditer(line):
                    url = match.group(0).rstrip(".,;")
                    parts = HOST_RE.match(url)
                    if not parts:
                        continue
                    host = parts.group(1).lower()
                    extension = os.path.splitext(parts.group(2))[1].lower()
                    if extension not in ASSET_EXT and host not in FONT_HOSTS:
                        continue
                    if any(url.startswith(prefix) for prefix in exceptions):
                        exempted += 1
                        continue
                    out.append(finding("HOTLINK", "line %d loads %s" % (number, url), rel, "",
                                       "Download the file, record it and serve it from the project. "
                                       "Or add a hotlinkExceptions entry with a reason."))
    return out, exempted


PROBE_NAMES = ("gdh-probe.png", "gdh-probe.jpg", "gdh-probe.svg", "gdh-probe.woff2", "gdh-probe.mp4",
               "sub/gdh-probe.png")


def read_ignore(manifest, manifest_path, asset_dirs):
    """Return (patterns, findings). A pattern that covers a whole asset folder is refused: it would let every
    file there skip the license record."""
    raw = manifest.get("ignore", [])
    out, patterns = [], []
    if not isinstance(raw, list):
        return [], [finding("MANIFEST_IGNORE", "ignore must be a list of globs or {pattern, reason} objects",
                            manifest_path, fix="Write a list.")]
    for index, item in enumerate(raw):
        pattern = item.get("pattern") if isinstance(item, dict) else item
        if not isinstance(pattern, str) or not pattern.strip():
            out.append(finding("MANIFEST_IGNORE", "ignore item %d has no glob" % (index + 1), manifest_path,
                               fix="Write a glob such as public/og/*.png."))
            continue
        pattern = posix(os.path.normpath(pattern.strip()))
        folders = list(asset_dirs) + ["design/assets"]
        blanket = [d for d in folders if any(fnmatch.fnmatchcase("%s/%s" % (d.strip("/"), name), pattern)
                                             for name in PROBE_NAMES)]
        if blanket:
            out.append(finding("MANIFEST_IGNORE", "ignore '%s' covers the whole folder %s" % (pattern, blanket[0]),
                               manifest_path, fix="Name a subfolder or a file name pattern, and record the rest."))
            continue
        patterns.append(pattern)
    return patterns, out


def load_terms(catalog_path):
    """Return ({id: source}, error) for the catalog-terms check."""
    sources, problems = load_catalog(catalog_path)
    if sources is None or problems:
        return None, "catalog %s is not usable: %s" % (catalog_path, "; ".join((problems or [])[:3]))
    return dict((s["id"], s) for s in sources if isinstance(s, dict)), None


NO_CREDIT_RE = re.compile(r"^\s*(?:none|no\s+credit|not\s+required|none\s+required|n/?a)\b", re.I)


def catalog_findings(assets, terms):
    """Test each entry that names a catalogId against the catalog terms."""
    out = []
    for entry in assets:
        if not isinstance(entry, dict) or not isinstance(entry.get("catalogId"), str) or not entry["catalogId"]:
            continue
        label, path, cid = entry.get("id") or "?", entry.get("path") or entry.get("package") or "", entry["catalogId"]
        source = terms.get(cid)
        if source is None:
            out.append(finding("CATALOG_UNKNOWN", "catalogId '%s' is not in the catalog" % cid, path, label,
                               "Use the id from catalogs/assets.json, or drop catalogId and vet the source."))
            continue
        use = source.get("commercialUse")
        if use == "reference-only":
            out.append(finding("CATALOG_REFERENCE_ONLY", "the catalog marks '%s' reference-only; nothing from it "
                               "ships" % cid, path, label, "Remove the file. Study the source; take no file."))
        elif use == "unknown":
            out.append(finding("CATALOG_TERMS_UNKNOWN", "the catalog knows no license terms for '%s'" % cid, path,
                               label, "Read the license text of the exact item and record it, or pick another source."))
        credit = attribution_class(source.get("attribution"))
        given = entry.get("attribution") if isinstance(entry.get("attribution"), str) else ""
        if credit == "required" and (not given.strip() or NO_CREDIT_RE.match(given)):
            out.append(finding("CATALOG_CREDIT", "the catalog says '%s' requires a credit, the entry gives none" % cid,
                               path, label, "Write the exact credit line, then run notices."))
    return out


def default_catalog():
    """The catalog beside the skills folder: kit/catalogs or the exported .claude/catalogs."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.normpath(os.path.join(here, "..", "..", "..", "catalogs", "assets.json"))
    return candidate if os.path.isfile(candidate) else None


def run_check(manifest_path, root, asset_dirs, reference_dirs, all_files, scan_dirs, catalog_path=None):
    """Return (findings, info)."""
    info = OrderedDict([("root", root), ("assetDirs", []), ("files", 0), ("recorded", 0), ("entries", 0),
                        ("packages", 0), ("ignored", 0), ("ignoredFiles", []), ("hotlinkExempted", 0),
                        ("catalog", catalog_path)])
    manifest, error = load_manifest(manifest_path)
    if error:
        return [finding("MANIFEST_INVALID", error, manifest_path,
                        fix="Copy the manifest template into design/assets/manifest.json.")], info
    assets = manifest["assets"]
    findings = validate_entries(assets)
    info["entries"] = len(assets)
    ignore, ignore_findings = read_ignore(manifest, manifest_path, asset_dirs)
    findings.extend(ignore_findings)
    if catalog_path:
        terms, terms_error = load_terms(catalog_path)
        if terms_error:
            findings.append(finding("CATALOG_UNREADABLE", terms_error, catalog_path,
                                    fix="Pass --catalog with the kit catalog, or fix the file."))
        else:
            findings.extend(catalog_findings(assets, terms))
    exceptions = []
    for item in manifest.get("hotlinkExceptions", []) if isinstance(manifest.get("hotlinkExceptions", []), list) else []:
        prefix = item.get("prefix") if isinstance(item, dict) else None
        reason = item.get("reason") if isinstance(item, dict) else None
        if not (is_http_url(prefix) and isinstance(reason, str) and reason.strip()):
            findings.append(finding("MANIFEST_EXCEPTION", "a hotlink exception needs an http(s) prefix and a reason",
                                    manifest_path, fix="State the vendor rule that forbids self-hosting."))
        else:
            exceptions.append(prefix)

    recorded = {}
    hashes = {}
    for entry in assets:
        if not isinstance(entry, dict):
            continue
        label = entry.get("id") if isinstance(entry.get("id"), str) and entry.get("id") else "?"
        path = entry.get("path")
        if not isinstance(path, str) or not path:
            if isinstance(entry.get("package"), str) and entry.get("package"):
                info["packages"] += 1
            continue
        clean = posix(os.path.normpath(path))
        if os.path.isabs(path) or re.match(r"^[A-Za-z]:", path) or clean == ".." or clean.startswith("../"):
            findings.append(finding("ENTRY_PATH", "path must be relative and stay inside the project", path, label,
                                    "Copy the file into the project and record it again."))
            continue
        full = os.path.join(root, clean)
        if relative_inside(root, full) is None:
            findings.append(finding("ENTRY_PATH", "path resolves outside the project", path, label,
                                    "Copy the file into the project and record it again."))
            continue
        recorded.setdefault(clean, label)
        if not os.path.isfile(full):
            findings.append(finding("FILE_MISSING", "the recorded file does not exist", path, label,
                                    "Restore the file, or remove the entry when the asset left the project."))
            continue
        actual = sha256_file(full)
        hashes[clean] = actual
        expected = entry.get("sha256")
        if isinstance(expected, str) and expected and actual != expected.lower():
            findings.append(finding("FILE_HASH", "sha256 is %s, the entry says %s" % (actual[:12], expected[:12]),
                                    path, label,
                                    "The file changed. Confirm the source and license still hold. "
                                    "Then record again with --replace; add --modified when you edited it."))

    present_dirs = [d.strip("/") for d in asset_dirs if os.path.isdir(os.path.join(root, d))]
    info["assetDirs"] = present_dirs
    manifest_rel = relative_inside(root, manifest_path)
    seen, seen_set, ignored = [], set(), []
    for sub in present_dirs:
        for rel in walk_files(root, sub, None if all_files else ASSET_EXT, WALK_SKIP):
            if rel in seen_set or rel == manifest_rel:
                continue
            seen_set.add(rel)
            if any(fnmatch.fnmatchcase(rel, pattern) for pattern in ignore):
                info["ignored"] += 1
                ignored.append(rel)
                continue
            seen.append(rel)
            info["files"] += 1
            if rel in recorded:
                info["recorded"] += 1
            else:
                findings.append(finding("FILE_UNRECORDED", "no manifest entry", rel, "",
                                        "Read its license and run record. For a file the project made, "
                                        "record it with --origin own or --origin generated."))

    reference_hashes = {}
    for sub in reference_dirs:
        sub = sub.strip("/")
        if any(under(sub, d) or under(d, sub) for d in present_dirs):
            continue
        for rel in walk_files(root, sub, ASSET_EXT, WALK_SKIP):
            reference_hashes.setdefault(sha256_file(os.path.join(root, rel)), rel)
    info["ignoredFiles"] = ignored
    if reference_hashes:
        # An ignored file is still compared: ignore skips the license record, never the reference check.
        for rel in seen + ignored:
            digest = hashes.get(rel) or sha256_file(os.path.join(root, rel))
            if digest in reference_hashes:
                findings.append(finding("REFERENCE_SHIPPED", "identical to the reference file %s" % reference_hashes[digest],
                                        rel, recorded.get(rel, ""),
                                        "A reference never ships. Remove the copy, then source or make an asset "
                                        "with a license that allows the use."))
    if scan_dirs:
        hot, exempted = scan_hotlinks(root, scan_dirs, exceptions)
        findings.extend(hot)
        info["hotlinkExempted"] = exempted
    return findings, info


def cmd_check(args):
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        return usage_error(args, "--root is not a folder: %s" % args.root)
    asset_dirs = args.asset_dir if args.asset_dir else list(DEFAULT_ASSET_DIRS)
    reference_dirs = args.reference_dir if args.reference_dir else list(DEFAULT_REFERENCE_DIRS)
    catalog = args.catalog if args.catalog else (None if args.no_catalog else default_catalog())
    if args.catalog and not os.path.isfile(args.catalog):
        return usage_error(args, "--catalog is not a file: %s" % args.catalog)
    findings, info = run_check(args.manifest, root, asset_dirs, reference_dirs, args.all_files, args.scan or [],
                               catalog)
    lines = finding_lines(findings)
    lines.append("check: %d file(s) in %s; %d recorded; %d entr%s (%d package); %d ignored; %d finding(s)"
                 % (info["files"], ", ".join(info["assetDirs"]) or "no asset folder", info["recorded"],
                    info["entries"], "y" if info["entries"] == 1 else "ies", info["packages"], info["ignored"],
                    len(findings)))
    emit(args, OrderedDict([("ok", not findings), ("findings", findings), ("info", info)]), lines)
    return 1 if findings else 0


# --------------------------------------------------------------------------
# notices
# --------------------------------------------------------------------------

NO_CREDIT_TEXT = ("none required", "none", "no credit required", "not required")


def cell(text):
    return str(text).replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip()


def render_notices(manifest, manifest_label, title):
    entries = sorted((e for e in manifest["assets"] if isinstance(e, dict)), key=lambda e: str(e.get("id", "")))
    credited, quiet, own = [], [], []
    for entry in entries:
        origin = entry.get("origin", "outside")
        needs_credit = entry.get("attribution", "").strip().lower().rstrip(".") not in NO_CREDIT_TEXT
        if origin == "own":
            own.append(entry)
        elif needs_credit:
            credited.append(entry)
        else:
            quiet.append(entry)
    lines = ["# %s" % title, "",
             "Generated from `%s` by `assets.py notices`. Do not edit this file by hand." % manifest_label,
             "To change it, record the asset and run the command again.", ""]
    lines += ["## Credits", ""]
    if credited:
        lines.append("Each credit below is a license condition or a credit that the author asked for.")
        lines.append("")
        for entry in credited:
            target = entry.get("path") or entry.get("package") or ""
            lines.append("### %s" % cell(entry.get("id", "")))
            lines.append("")
            lines.append("- Credit: %s" % cell(entry.get("attribution", "")))
            lines.append("- Source: %s" % cell(entry.get("sourceUrl", "")))
            lines.append("- License: %s" % cell(entry.get("license", "")))
            if entry.get("licenseUrl"):
                lines.append("- License text: %s" % cell(entry["licenseUrl"]))
            lines.append("- %s: `%s`" % ("Package" if entry.get("package") and not entry.get("path") else "File",
                                         cell(target)))
            lines.append("- Changed by this project: %s" % ("yes" if entry.get("modified") else "no"))
            lines.append("- License read on: %s" % cell(entry.get("date", "")))
            lines.append("")
    else:
        lines += ["No asset in this project needs a credit line.", ""]
    lines += ["## Other outside and generated assets", ""]
    if quiet:
        lines += ["These assets need no credit line. Their licenses still apply.", "",
                  "| Asset | File or package | Source | License | Changed | License read on |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for entry in quiet:
            lines.append("| %s | `%s` | %s | %s | %s | %s |" % (
                cell(entry.get("id", "")), cell(entry.get("path") or entry.get("package") or ""),
                cell(entry.get("sourceUrl", "")), cell(entry.get("license", "")),
                "yes" if entry.get("modified") else "no", cell(entry.get("date", ""))))
        lines.append("")
    else:
        lines += ["None.", ""]
    if own:
        lines += ["## Assets made by this project", "",
                  "| Asset | File | Made by | Terms |", "| --- | --- | --- | --- |"]
        for entry in own:
            lines.append("| %s | `%s` | %s | %s |" % (cell(entry.get("id", "")), cell(entry.get("path", "")),
                                                     cell(entry.get("sourceUrl", "")), cell(entry.get("license", ""))))
        lines.append("")
    counts = OrderedDict([("credited", len(credited)), ("noCredit", len(quiet)), ("own", len(own))])
    return "\n".join(lines).rstrip("\n") + "\n", counts


def cmd_notices(args):
    manifest, error = load_manifest(args.manifest)
    if error:
        emit(args, {"ok": False, "findings": [finding("MANIFEST_INVALID", error, args.manifest)]},
             ["MANIFEST_INVALID  %s" % error, "notices: nothing written"])
        return 1
    findings = validate_entries(manifest["assets"])
    if findings:
        emit(args, {"ok": False, "findings": findings}, finding_lines(findings) + ["notices: nothing written"])
        return 1
    text, counts = render_notices(manifest, args.label or posix(args.manifest), args.title)
    write_text(args.output, text)
    emit(args, OrderedDict([("ok", True), ("output", args.output), ("counts", counts)]),
         ["wrote  %s" % args.output,
          "notices: %d with a credit, %d without, %d made by the project"
          % (counts["credited"], counts["noCredit"], counts["own"])])
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(prog="assets.py", description="Asset catalog search and provenance records.")
    parser.add_argument("--version", action="version", version="assets.py %s" % VERSION)
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("search", help="filter and rank catalog entries")
    p.add_argument("catalog", help="path to kit/catalogs/assets.json")
    p.add_argument("--group", action="append", help="group id; repeat it or use commas")
    p.add_argument("--query", help="words that describe the need")
    p.add_argument("--commercial", action="store_true", help="keep entries whose commercial use is yes or yes-with-limits")
    p.add_argument("--no-attribution", action="store_true",
                   help="keep entries that need no visible credit (classes none, notice, requested)")
    p.add_argument("--verified", action="store_true", help="keep entries whose status is catalog-verified")
    p.add_argument("--limit", type=int, default=10, help="results to show; 0 shows all (default 10)")
    p.add_argument("--today", help="YYYY-MM-DD; default is the system date")
    p.add_argument("--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS,
                   help="age after which a catalog check is read again (default %d)" % DEFAULT_MAX_AGE_DAYS)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("record", help="append a provenance entry to the manifest")
    p.add_argument("manifest", help="path to design/assets/manifest.json")
    p.add_argument("--id", required=True, help="kebab-case id; more files get -2, -3")
    p.add_argument("--source-url", required=True, help="the page the asset came from")
    p.add_argument("--license", required=True, help="license name and the URL of the text that was read")
    p.add_argument("--attribution", required=True, help="the exact credit line, or \"none required\"")
    p.add_argument("--file", action="append", help="a file inside the project; repeat for more files")
    p.add_argument("--date", required=True, help="YYYY-MM-DD the license was read")
    p.add_argument("--package", help="name@version of a dependency, in place of --file")
    p.add_argument("--root", help="project folder; default is the folder above design/assets")
    p.add_argument("--license-url", help="URL of the license text")
    p.add_argument("--catalog-id", help="id of the catalog entry the asset came from")
    p.add_argument("--origin", choices=ORIGINS, default="outside")
    p.add_argument("--modified", action="store_true", help="the project changed the file")
    p.add_argument("--note", help="a use limit or a duty to remember")
    p.add_argument("--replace", action="store_true", help="replace the entry that has the same id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_record)

    p = sub.add_parser("check", help="verify the manifest against the project files")
    p.add_argument("manifest", help="path to design/assets/manifest.json")
    p.add_argument("--root", required=True, help="project folder")
    p.add_argument("--asset-dir", action="append",
                   help="asset folder, relative to the root; repeat it (default: %s)" % ", ".join(DEFAULT_ASSET_DIRS))
    p.add_argument("--reference-dir", action="append",
                   help="reference folder (default: %s)" % ", ".join(DEFAULT_REFERENCE_DIRS))
    p.add_argument("--all-files", action="store_true", help="check every file, not only asset file types")
    p.add_argument("--scan", action="append", help="source folder to scan for remote asset URLs; repeat it")
    p.add_argument("--catalog", help="catalog for the catalogId terms check (default: catalogs/assets.json beside "
                                     "the skills folder, when present)")
    p.add_argument("--no-catalog", action="store_true", help="skip the catalogId terms check")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("notices", help="write the third-party notices file")
    p.add_argument("manifest", help="path to design/assets/manifest.json")
    p.add_argument("-o", "--output", required=True, help="file to write, for example ATTRIBUTION.md")
    p.add_argument("--title", default="Third-party notices")
    p.add_argument("--label", help="manifest path to print in the file (default: the path as given)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_notices)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
