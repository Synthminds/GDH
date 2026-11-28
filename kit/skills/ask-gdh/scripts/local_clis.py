#!/usr/bin/env python3
"""local_clis.py: report which local creative programs an agent can drive, and validate their catalog.

The catalog is kit/catalogs/local-clis.json. Each entry is a CLI-Anything harness: a separate
Python package that wraps a desktop program or binary (Inkscape, GIMP, Blender ...) and prints JSON.

Commands:
  probe     Look for each harness and its backend on PATH. Reads only. Runs nothing it finds.
  install   Print the pinned install command for one harness. It prints; it never installs.
  validate  Check the catalog against its schema. Exit 1 on any finding.

Exit codes: 0 pass, 1 findings, 2 usage or an unreadable file.
Standard library only. No network. Writes nothing.
"""
import argparse
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CATALOG = os.path.normpath(os.path.join(HERE, "..", "..", "..", "catalogs", "local-clis.json"))
DEFAULT_CAPS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "catalogs", "capabilities.json"))

NETWORK = ("none", "localhost", "internet")
EVIDENCE = ("VERIFIED", "DOCUMENTED", "UNTESTED")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
BIN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
PATH_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_./-]*/agent-harness$")
REL_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_./-]*$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPO_RE = re.compile(r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STRINGS = ("id", "name", "harness", "installPath", "backendNote", "network", "upstreamSkill", "evidence", "evidenceNote")


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def vocabulary(caps_doc):
    """Return (capability words, discipline names) from capabilities.json, or (None, None)."""
    if not isinstance(caps_doc, dict):
        return None, None
    caps, disciplines = caps_doc.get("capabilities"), caps_doc.get("disciplines")
    if not isinstance(caps, dict) or not isinstance(disciplines, dict):
        return None, None
    return set(caps), set(disciplines)


def entries(doc):
    clis = doc.get("clis") if isinstance(doc, dict) else None
    return [c for c in clis if isinstance(c, dict)] if isinstance(clis, list) else []


def safe_rel(value):
    return isinstance(value, str) and bool(REL_RE.match(value)) and ".." not in value.split("/")


def validate(doc, vocab=None, disciplines=None):
    """Return a list of findings: {"code", "where", "message"}."""
    findings = []

    def add(code, where, message):
        findings.append({"code": code, "where": where, "message": message})

    if not isinstance(doc, dict):
        add("SCHEMA", "-", "the catalog must be a JSON object")
        return findings
    if doc.get("version") != 1:
        add("SCHEMA", "version", "version must be 1")
    up = doc.get("upstream")
    if not isinstance(up, dict):
        add("UPSTREAM", "upstream", "upstream must be an object")
    else:
        if not isinstance(up.get("repo"), str) or not REPO_RE.match(up["repo"]):
            add("UPSTREAM", "upstream.repo", "repo must be an https://github.com/<owner>/<name> URL")
        if not isinstance(up.get("commit"), str) or not SHA_RE.match(up["commit"]):
            add("PIN", "upstream.commit", "commit must be a full 40-character SHA, never a branch or tag")
        if not isinstance(up.get("license"), str) or not up["license"]:
            add("UPSTREAM", "upstream.license", "license must be a non-empty string")
        if not isinstance(up.get("readAt"), str) or not DATE_RE.match(up["readAt"]):
            add("UPSTREAM", "upstream.readAt", "readAt must be YYYY-MM-DD")
    clis = doc.get("clis")
    if not isinstance(clis, list) or not clis:
        add("SCHEMA", "clis", "clis must be a non-empty list")
        return findings
    seen = set()
    for index, entry in enumerate(clis):
        where = "clis[%d]" % index
        if not isinstance(entry, dict):
            add("SCHEMA", where, "entry must be an object")
            continue
        where = "clis[%s]" % entry.get("id", index)
        for key in STRINGS:
            if not isinstance(entry.get(key), str) or not entry.get(key):
                add("FIELD", where, "'%s' must be a non-empty string" % key)
        for key in ("exposes", "spendsCredits"):
            if not isinstance(entry.get(key), bool):
                add("FIELD", where, "'%s' must be true or false" % key)
        cid = entry.get("id")
        if isinstance(cid, str):
            if not ID_RE.match(cid):
                add("ID", where, "id must be lowercase letters, digits and hyphens")
            if cid in seen:
                add("ID", where, "id is not unique")
            seen.add(cid)
        harness = entry.get("harness")
        if isinstance(harness, str) and not ID_RE.match(harness):
            add("HARNESS", where, "harness must be a bare command name")
        path = entry.get("installPath")
        if isinstance(path, str) and (not PATH_RE.match(path) or ".." in path.split("/")):
            add("PATH", where, "installPath must be a relative '<dir>/agent-harness' path with no '..'")
        if not safe_rel(entry.get("upstreamSkill")):
            add("PATH", where, "upstreamSkill must be a relative path with no '..'")
        caps = entry.get("capabilities")
        if not isinstance(caps, list) or not caps or any(not isinstance(c, str) for c in caps):
            add("FIELD", where, "'capabilities' must be a non-empty list of strings")
        elif vocab is not None:
            for cap in caps:
                if cap not in vocab:
                    add("CAPABILITY", where, "capability '%s' is not in the vocabulary" % cap)
        disc = entry.get("disciplines")
        if not isinstance(disc, list) or any(not isinstance(d, str) for d in disc):
            add("FIELD", where, "'disciplines' must be a list of strings")
        elif disciplines is not None:
            for item in disc:
                if item not in disciplines:
                    add("DISCIPLINE", where, "discipline '%s' is not in capabilities.json" % item)
        backend = entry.get("backend")
        if not isinstance(backend, list) or any(
                not isinstance(group, list) or not group or any(not isinstance(b, str) or not BIN_RE.match(b) for b in group)
                for group in backend):
            add("BACKEND", where, "backend must be a list of non-empty lists of binary names")
        network = entry.get("network")
        if isinstance(network, str) and network not in NETWORK:
            add("NETWORK", where, "network must be one of %s" % ", ".join(NETWORK))
        if network == "internet" and entry.get("exposes") is not True:
            add("EXPOSES", where, "a harness that sends data over the internet must set exposes to true")
        if isinstance(entry.get("evidence"), str) and entry["evidence"] not in EVIDENCE:
            add("EVIDENCE", where, "evidence must be one of %s" % ", ".join(EVIDENCE))
    return findings


def install_command(doc, entry):
    """The pinned pip command for one harness. A string; nothing runs it here."""
    up = doc["upstream"]
    return 'python3 -m pip install "git+%s.git@%s#subdirectory=%s"' % (up["repo"], up["commit"], entry["installPath"])


def probe_entry(doc, entry, which=shutil.which):
    harness_ok = which(entry["harness"]) is not None
    missing = [group for group in entry.get("backend", []) if not any(which(b) for b in group)]
    if harness_ok and not missing:
        state = "ready"
    elif harness_ok:
        state = "needs-backend"
    elif not missing:
        state = "needs-harness"
    else:
        state = "needs-both"
    row = {
        "id": entry["id"], "name": entry["name"], "capabilities": entry["capabilities"], "state": state,
        "harness": entry["harness"], "missingBackend": [" or ".join(g) for g in missing],
        "network": entry["network"], "exposes": entry["exposes"], "spendsCredits": entry["spendsCredits"],
        "backendNote": entry["backendNote"], "evidence": entry["evidence"],
    }
    if not harness_ok:
        row["install"] = install_command(doc, entry)
    if entry["network"] == "localhost":
        row["serviceCheck"] = "Confirm the service runs on this machine before the first call."
    return row


def probe(doc, capabilities=None, which=shutil.which):
    wanted = set(capabilities or [])
    rows = []
    for entry in entries(doc):
        if wanted and not wanted.intersection(entry.get("capabilities") or []):
            continue
        rows.append(probe_entry(doc, entry, which))
    return rows


def capability_summary(rows):
    """For each capability: the ids that are ready, in catalog order."""
    out = {}
    for row in rows:
        for cap in row["capabilities"]:
            out.setdefault(cap, [])
            if row["state"] == "ready":
                out[cap].append(row["id"])
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--catalog", default=DEFAULT_CATALOG)
    parser.add_argument("--capabilities-file", default=DEFAULT_CAPS)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="machine output")
    sub = parser.add_subparsers(dest="command")
    p_probe = sub.add_parser("probe", parents=[common], help="report what is installed on PATH")
    p_probe.add_argument("--capability", action="append", help="only harnesses that serve this capability")
    p_install = sub.add_parser("install", parents=[common], help="print the pinned install command for one harness")
    p_install.add_argument("id")
    sub.add_parser("validate", parents=[common], help="check the catalog schema")
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_usage(sys.stderr)
        return 2
    try:
        doc = load_json(args.catalog)
    except (OSError, ValueError) as exc:
        print("cannot read %s: %s" % (args.catalog, exc), file=sys.stderr)
        return 2

    if args.command == "validate":
        try:
            vocab, disciplines = vocabulary(load_json(args.capabilities_file))
        except (OSError, ValueError):
            vocab, disciplines = None, None
        findings = validate(doc, vocab, disciplines)
        if args.json:
            print(json.dumps({"ok": not findings, "findings": findings}, indent=2))
        else:
            for f in findings:
                print("%s  %s  %s" % (f["code"], f["where"], f["message"]))
            print("validate: %d finding(s)" % len(findings))
        return 1 if findings else 0

    findings = validate(doc)
    if findings:
        print("the catalog has %d schema finding(s); run validate" % len(findings), file=sys.stderr)
        return 2

    if args.command == "install":
        entry = next((e for e in entries(doc) if e.get("id") == args.id), None)
        if entry is None:
            print("unknown id '%s'" % args.id, file=sys.stderr)
            return 2
        result = {"id": entry["id"], "install": install_command(doc, entry), "backend": entry["backendNote"],
                  "exposes": entry["exposes"], "network": entry["network"],
                  "note": "Printed only. Run it after the user says yes, in the environment the user names."}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(result["install"])
            print("backend: %s" % result["backend"])
        return 0

    rows = probe(doc, args.capability)
    if args.json:
        print(json.dumps({"upstream": doc["upstream"], "clis": rows, "ready": capability_summary(rows)}, indent=2))
    else:
        for row in rows:
            marks = [m for m, on in (("exposes", row["exposes"]), ("localhost", row["network"] == "localhost")) if on]
            extra = (" missing " + ", ".join(row["missingBackend"])) if row["missingBackend"] else ""
            print("%-12s %-14s %s%s%s" % (row["id"], row["state"], ",".join(row["capabilities"]),
                                          (" [" + ",".join(marks) + "]") if marks else "", extra))
        ready = sum(1 for r in rows if r["state"] == "ready")
        print("local clis: %d ready of %d" % (ready, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
