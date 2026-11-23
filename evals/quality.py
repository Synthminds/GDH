#!/usr/bin/env python3
"""Score the tell scan against the labelled quality corpus.

Reads evals/cases/quality/labels.json, runs tells.py on each page, and reports
precision and recall for each rule and for whole pages. Exit 0 when every
measure meets the recorded baseline, 1 when one falls below it.
Standard library only. No network. Writes nothing.
"""

import argparse
import importlib.util
import io
import json
import os
import sys
from collections import OrderedDict
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(HERE, "cases", "quality")
TELLS = os.path.join(ROOT, "kit", "skills", "design-critique", "scripts", "tells.py")
MOODBOARD = os.path.join(ROOT, "kit", "skills", "mood-board", "scripts", "moodboard.py")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_tells():
    return load_module("gdh_tells", TELLS)


def score_boards(corpus, labels):
    """Run the mood-board diff on each labelled board. Return (rows, problems)."""
    moodboard = load_module("gdh_moodboard", MOODBOARD)
    rows, problems = [], []
    for case in labels.get("boards", []):
        with open(os.path.join(corpus, case["board"]), encoding="utf-8") as handle:
            board = json.load(handle)
        _metrics, pairs, _defaults, findings = moodboard.analyse(board)
        verdicts = [pair["verdict"] for pair in pairs]
        errors = sorted(set(f["code"] for f in findings if f["level"] == "error"))
        passed = not errors
        ok = verdicts == case["verdicts"] and errors == sorted(case["errors"]) and passed == case["pass"]
        if not ok:
            problems.append("board %s: verdicts %s, errors %s" % (case["id"], verdicts, errors))
        rows.append(OrderedDict([("id", case["id"]), ("verdicts", verdicts), ("errors", errors),
                                 ("asLabelled", ok)]))
    return rows, problems


def scan(tells, page, tokens=None):
    argv = ["--json"]
    if tokens:
        argv += ["--tokens", tokens]
    out = io.StringIO()
    with redirect_stdout(out):
        tells.main(argv + [page])
    data = json.loads(out.getvalue())
    found = set(item["code"] for item in data.get("findings", []))
    required = set(item["code"] for item in data.get("brandRequired", []))
    return found, required


def ratio(numerator, denominator):
    return None if denominator == 0 else round(float(numerator) / denominator, 2)


def score(corpus=CORPUS):
    with open(os.path.join(corpus, "labels.json"), encoding="utf-8") as handle:
        labels = json.load(handle)
    tells = load_tells()
    rules = OrderedDict((code, {"tp": 0, "fp": 0, "fn": 0}) for code in sorted(tells.RULES))
    cases, page_tp, page_fp, page_fn, brand_ok = [], 0, 0, 0, True
    for case in labels["cases"]:
        page = os.path.join(corpus, case["page"])
        tokens = os.path.join(corpus, case["tokens"]) if case.get("tokens") else None
        found, required = scan(tells, page, tokens)
        expect = set(case.get("expect", []))
        for code in rules:
            if code in found and code in expect:
                rules[code]["tp"] += 1
            elif code in found:
                rules[code]["fp"] += 1
            elif code in expect:
                rules[code]["fn"] += 1
        generic = case["class"].startswith("generic")
        if generic and found:
            page_tp += 1
        elif generic:
            page_fn += 1
        elif found:
            page_fp += 1
        if "expectBrandRequired" in case and required != set(case["expectBrandRequired"]):
            brand_ok = False
        cases.append(OrderedDict([("id", case["id"]), ("class", case["class"]),
                                  ("missed", sorted(expect - found)), ("extra", sorted(found - expect)),
                                  ("brandRequired", sorted(required))]))
    for counts in rules.values():
        counts["precision"] = ratio(counts["tp"], counts["tp"] + counts["fp"])
        counts["recall"] = ratio(counts["tp"], counts["tp"] + counts["fn"])
    pages = OrderedDict([("recall", ratio(page_tp, page_tp + page_fn)),
                         ("precision", ratio(page_tp, page_tp + page_fp))])
    base = labels["baseline"]
    below = []
    if pages["recall"] is not None and pages["recall"] < base["pageRecall"]:
        below.append("page recall %.2f < %.2f" % (pages["recall"], base["pageRecall"]))
    if pages["precision"] is not None and pages["precision"] < base["pagePrecision"]:
        below.append("page precision %.2f < %.2f" % (pages["precision"], base["pagePrecision"]))
    for code, floor in sorted(base.get("ruleRecall", {}).items()):
        value = rules.get(code, {}).get("recall")
        if value is not None and value < floor:
            below.append("%s recall %.2f < %.2f" % (code, value, floor))
    for code, floor in sorted(base.get("rulePrecision", {}).items()):
        value = rules.get(code, {}).get("precision")
        if value is not None and value < floor:
            below.append("%s precision %.2f < %.2f" % (code, value, floor))
    if base.get("brandRequiredExact") and not brand_ok:
        below.append("a brand-required case reported the wrong codes")
    boards, board_problems = score_boards(corpus, labels)
    below += board_problems
    return OrderedDict([("tool", "quality.py"), ("cases", cases), ("rules", rules), ("pages", pages),
                        ("boards", boards), ("belowBaseline", below), ("pass", not below)])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Score tells.py against the labelled quality corpus.")
    parser.add_argument("--corpus", default=CORPUS, help="folder that holds labels.json")
    parser.add_argument("--json", action="store_true", help="print one JSON object on stdout")
    args = parser.parse_args(argv)
    result = score(args.corpus)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("%-30s %4s %4s %4s %9s %6s" % ("rule", "tp", "fp", "fn", "precision", "recall"))
        for code, c in result["rules"].items():
            if c["tp"] or c["fp"] or c["fn"]:
                print("%-30s %4d %4d %4d %9s %6s" % (code, c["tp"], c["fp"], c["fn"],
                                                    c["precision"], c["recall"]))
        print("pages: recall %s, precision %s" % (result["pages"]["recall"], result["pages"]["precision"]))
        for case in result["cases"]:
            if case["missed"] or case["extra"]:
                print("%s: missed %s; extra %s" % (case["id"], case["missed"] or "none", case["extra"] or "none"))
        for board in result["boards"]:
            print("board %s: %s; errors %s; %s" % (board["id"], ", ".join(board["verdicts"]),
                                                   board["errors"] or "none",
                                                   "as labelled" if board["asLabelled"] else "NOT as labelled"))
        for line in result["belowBaseline"]:
            print("BELOW BASELINE: %s" % line)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
