#!/usr/bin/env python3
"""principles.py: query and validate the GDH principles canon.

The canon is kit/canon/principles.json: {"version": 1, "principles": [...]}.
Each principle has id, title, rule, why, apply, test, check, disciplines,
stages, tags and source {book, part}.

Query:    principles.py --discipline website --stage explore [--tag originality]
          [--check gate] [--id P-EMO-03 | --id P-EMO] [--book designing-for-emotion]
          [--specific] [--full] [--json]
Validate: principles.py --validate [--json]

Filters combine with AND. A flag given twice, or a comma list, matches any of
its values. A principle whose disciplines are ["all"] matches every
discipline; --specific leaves those out.

Python 3.9+, standard library only. No network calls. Writes nothing.
Exit codes: 0 pass, 1 validation findings, 2 usage or input error.
"""

import argparse
import json
import os
import re
import sys

VERSION = "0.2.0"
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CANON = os.path.normpath(os.path.join(HERE, "..", "..", "..", "canon", "principles.json"))
DEFAULT_CAPS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "catalogs", "capabilities.json"))

BOOKS = {
    "design-systems-handbook": "DSH",
    "design-engineering-handbook": "DEH",
    "animation-handbook": "ANI",
    "collaboration-handbook": "COL",
    "principles-of-product-design": "PPD",
    "design-leadership-handbook": "LEAD",
    "designops-handbook": "OPS",
    "design-thinking-handbook": "DT",
    "designing-for-emotion": "EMO",
    "mastering-gephi": "GEPHI",
    "ai-app-5-steps": "AIAPP",
    "mapping-to-mcps": "MCP",
}
STAGES = ("brief", "explore", "refine", "finalize")
TAGS = ("originality", "emotion", "system", "motion", "process", "data", "handoff",
        "accessibility", "collaboration")
CHECKS = ("gate", "default")
TEXT_FIELDS = ("title", "rule", "why", "apply", "test")
ID_RE = re.compile(r"^P-([A-Z]+)-(\d{2,3})$")


class UsageError(Exception):
    """Bad arguments or an unreadable input file."""


def read_json(path, what):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as exc:
        raise UsageError("cannot read %s %s: %s" % (what, path, exc.strerror or exc))
    except ValueError as exc:
        raise UsageError("%s %s is not valid JSON: %s" % (what, path, exc))


def load_disciplines(path):
    data = read_json(path, "capabilities file")
    disc = data.get("disciplines") if isinstance(data, dict) else None
    if not isinstance(disc, dict) or not disc:
        raise UsageError("capabilities file %s has no 'disciplines' object" % path)
    return set(disc)


def principle_list(canon):
    if isinstance(canon, dict) and isinstance(canon.get("principles"), list):
        return canon["principles"]
    return []


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def _str_list(value):
    return isinstance(value, list) and value and all(isinstance(v, str) for v in value)


def validate(canon, disciplines):
    """Return a list of findings: {"code", "id", "message"}."""
    found = []

    def add(code, pid, message):
        found.append({"code": code, "id": pid, "message": message})

    if not isinstance(canon, dict):
        add("SCHEMA", "-", "the canon must be a JSON object")
        return found
    if canon.get("version") != 1:
        add("SCHEMA", "-", "'version' must be 1")
    items = canon.get("principles")
    if not isinstance(items, list):
        add("SCHEMA", "-", "'principles' must be a list")
        return found
    seen = {}
    per_book = {book: 0 for book in BOOKS}
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            add("SCHEMA", "#%d" % index, "a principle must be an object")
            continue
        pid = item.get("id") if isinstance(item.get("id"), str) else "#%d" % index
        match = ID_RE.match(pid)
        if not match:
            add("ID_FORMAT", pid, "id must look like P-ABC-01")
        if pid in seen:
            add("ID_DUPLICATE", pid, "id is used by principles #%d and #%d" % (seen[pid], index))
        else:
            seen[pid] = index
        for key in TEXT_FIELDS:
            value = item.get(key)
            if not isinstance(value, str) or not value.strip():
                add("SCHEMA", pid, "'%s' must be a non-empty string" % key)
            elif any(ord(ch) > 126 for ch in value):
                add("TEXT_ASCII", pid, "'%s' holds a non-ASCII character" % key)
        title = item.get("title")
        if isinstance(title, str) and title.strip() and not 3 <= len(title.split()) <= 7:
            add("TITLE_LENGTH", pid, "title must have 3 to 7 words")
        if item.get("check") not in CHECKS:
            add("CHECK_VALUE", pid, "'check' must be 'gate' or 'default'")
        disc = item.get("disciplines")
        if not _str_list(disc):
            add("SCHEMA", pid, "'disciplines' must be a non-empty list of strings")
        else:
            if "all" in disc and len(disc) > 1:
                add("DISCIPLINE", pid, "'all' must stand alone in 'disciplines'")
            for value in disc:
                if value != "all" and value not in disciplines:
                    add("DISCIPLINE", pid, "unknown discipline '%s'" % value)
        stages = item.get("stages")
        if not _str_list(stages):
            add("SCHEMA", pid, "'stages' must be a non-empty list of strings")
        else:
            for value in stages:
                if value not in STAGES:
                    add("STAGE", pid, "unknown stage '%s'" % value)
        tags = item.get("tags")
        if not _str_list(tags):
            add("SCHEMA", pid, "'tags' must be a non-empty list of strings")
        else:
            for value in tags:
                if value not in TAGS:
                    add("TAG", pid, "unknown tag '%s'" % value)
        for key in ("disciplines", "stages", "tags"):
            value = item.get(key)
            if _str_list(value) and len(set(value)) != len(value):
                add("DUPLICATE_VALUE", pid, "'%s' repeats a value" % key)
        source = item.get("source")
        book = source.get("book") if isinstance(source, dict) else None
        part = source.get("part") if isinstance(source, dict) else None
        if not isinstance(book, str) or book not in BOOKS:
            add("SOURCE_BOOK", pid, "'source.book' must be a known book id")
        else:
            per_book[book] += 1
            if match and match.group(1) != BOOKS[book]:
                add("ID_PREFIX", pid, "id prefix must be P-%s for book '%s'" % (BOOKS[book], book))
        if not isinstance(part, str) or not part.strip():
            add("SCHEMA", pid, "'source.part' must be a non-empty string")
    for book, count in per_book.items():
        if count == 0:
            add("BOOK_EMPTY", book, "book has no principle")
    return found


# --------------------------------------------------------------------------
# Query
# --------------------------------------------------------------------------

def matches(item, args):
    disc = item.get("disciplines") or []
    if args.specific and "all" in disc:
        return False
    if args.discipline and "all" not in disc and not any(d in disc for d in args.discipline):
        return False
    if args.stage and not any(s in (item.get("stages") or []) for s in args.stage):
        return False
    if args.tag and not any(t in (item.get("tags") or []) for t in args.tag):
        return False
    if args.check and item.get("check") not in args.check:
        return False
    if args.book and (item.get("source") or {}).get("book") not in args.book:
        return False
    if args.id:
        pid = item.get("id", "")
        if not any(pid == want or pid.startswith(want + "-") for want in args.id):
            return False
    return True


def query(canon, args):
    return [p for p in principle_list(canon) if isinstance(p, dict) and matches(p, args)]


def format_line(item, full):
    head = "%s [%s] %s: %s" % (item.get("id"), item.get("check"), item.get("title"), item.get("rule"))
    if not full:
        return head + "\n  Test: %s" % item.get("test")
    src = item.get("source") or {}
    return "\n".join([
        head,
        "  Why: %s" % item.get("why"),
        "  Apply: %s" % item.get("apply"),
        "  Test: %s" % item.get("test"),
        "  Scope: %s; stages %s; tags %s" % (", ".join(item.get("disciplines") or []),
                                            ", ".join(item.get("stages") or []),
                                            ", ".join(item.get("tags") or [])),
        "  Source: %s, %s" % (src.get("book"), src.get("part")),
    ])


def split_values(values):
    out = []
    for value in values or []:
        out.extend(v.strip() for v in value.split(",") if v.strip())
    return out


def build_parser():
    p = argparse.ArgumentParser(
        prog="principles.py",
        description="Query or validate the GDH principles canon.")
    p.add_argument("--canon", default=DEFAULT_CANON, help="path to principles.json")
    p.add_argument("--capabilities", default=DEFAULT_CAPS, help="path to capabilities.json")
    p.add_argument("--discipline", action="append", help="discipline key, or several separated by commas")
    p.add_argument("--stage", action="append", help="brief, explore, refine or finalize")
    p.add_argument("--tag", action="append", help="tag such as originality or accessibility")
    p.add_argument("--check", action="append", help="gate or default")
    p.add_argument("--id", action="append", help="exact id, or a prefix such as P-EMO")
    p.add_argument("--book", action="append", help="book id")
    p.add_argument("--specific", action="store_true",
                   help="leave out principles scoped to all disciplines")
    p.add_argument("--full", action="store_true", help="print why, apply, scope and source too")
    p.add_argument("--validate", action="store_true", help="check the canon and exit")
    p.add_argument("--json", action="store_true", help="print one JSON object")
    p.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    return p


def check_filter_values(args, disciplines):
    for name, allowed in (("stage", STAGES), ("tag", TAGS), ("check", CHECKS), ("book", tuple(BOOKS))):
        for value in getattr(args, name) or []:
            if value not in allowed:
                raise UsageError("unknown --%s '%s'; allowed: %s" % (name, value, ", ".join(allowed)))
    for value in args.discipline or []:
        if value != "all" and value not in disciplines:
            raise UsageError("unknown --discipline '%s'; allowed: %s"
                             % (value, ", ".join(sorted(disciplines))))


def main(argv=None):
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    for name in ("discipline", "stage", "tag", "check", "id", "book"):
        setattr(args, name, split_values(getattr(args, name)))
    try:
        disciplines = load_disciplines(args.capabilities)
        check_filter_values(args, disciplines)
        canon = read_json(args.canon, "canon")
    except UsageError as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}))
        else:
            print("principles.py: %s" % exc, file=sys.stderr)
        return 2

    if args.validate:
        findings = validate(canon, disciplines)
        count = len(principle_list(canon))
        if args.json:
            print(json.dumps({"ok": not findings, "principles": count, "findings": findings}, indent=2))
        else:
            for f in findings:
                print("%-16s %-14s %s" % (f["code"], f["id"], f["message"]))
            print("validate: %d principle(s), %d finding(s)" % (count, len(findings)))
        return 1 if findings else 0

    selected = query(canon, args)
    if args.json:
        print(json.dumps({"ok": True, "count": len(selected), "principles": selected}, indent=2))
        return 0
    gates = sum(1 for p in selected if p.get("check") == "gate")
    for item in selected:
        print(format_line(item, args.full))
    print("%d principle(s): %d gate, %d default" % (len(selected), gates, len(selected) - gates))
    return 0


if __name__ == "__main__":
    sys.exit(main())
