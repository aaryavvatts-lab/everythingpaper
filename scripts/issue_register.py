#!/usr/bin/env python3
"""issue_register.py - summarise review/issues.md and gate on it.

Usage:
  python3 -I issue_register.py review/issues.md            # summary table
  python3 -I issue_register.py review/issues.md --gate     # exit 1 if not clean
  python3 -I issue_register.py review/issues.md --gate --strict   # blocked FATAL/MAJOR also fail
  python3 -I issue_register.py review/issues.md --json out.json

Gate fails while: any FATAL or MAJOR issue is `open`; any chunk in the Coverage list is
not `reviewed`; chunk files exist next to issues.md that Coverage does not list; a
`wontfix` issue has no `Reason:` line. Blocked FATAL/MAJOR issues are reported loudly
(they need the user) and fail only with --strict.
"""
import argparse
import glob
import json
import os
import re
import sys

HEAD = re.compile(r"^###\s+(I-\d+)\s*\|\s*(FATAL|MAJOR|MINOR|NIT)\s*\|\s*(open|fixed|blocked|wontfix)\s*\|\s*([^|]*?)\s*\|\s*(.+?)\s*$",
                  re.I | re.M)
SEV = ["FATAL", "MAJOR", "MINOR", "NIT"]
STA = ["open", "fixed", "blocked", "wontfix"]


def parse(text):
    issues = []
    ms = list(HEAD.finditer(text))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        cov = re.search(r"^## Coverage", text[m.end():end], re.M)
        if cov:
            end = m.end() + cov.start()
        block = text[m.end():end]
        issues.append({
            "id": m.group(1).upper(), "severity": m.group(2).upper(), "status": m.group(3).lower(),
            "where": m.group(4), "category": m.group(5),
            "has_quote": bool(re.search(r"^Quote:", block, re.M | re.I)),
            "has_fix": bool(re.search(r"^Fix:", block, re.M | re.I)),
            "has_reason": bool(re.search(r"^Reason:", block, re.M | re.I)),
        })
    cov = {}
    for m in re.finditer(r"^- (chunk_\d+):\s*(\w+)", text, re.M):
        cov[m.group(1)] = m.group(2).lower()
    return issues, cov


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("issues")
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if not os.path.isfile(a.issues):
        print("no such file:", a.issues, file=sys.stderr)
        return 2
    text = open(a.issues, encoding="utf-8").read()
    # fenced code blocks hold the template example, not real issues
    text = re.sub(r"^```.*?^```[ \t]*$", "", text, flags=re.S | re.M)
    issues, cov = parse(text)
    ids = [i["id"] for i in issues]
    problems = []
    warns = []

    dup = sorted({x for x in ids if ids.count(x) > 1})
    if dup:
        problems.append("duplicate issue IDs: " + ", ".join(dup))
    print("%-8s" % "" + "".join("%9s" % s for s in STA) + "%9s" % "total")
    for s in SEV:
        row = [sum(1 for i in issues if i["severity"] == s and i["status"] == st) for st in STA]
        print("%-8s" % s + "".join("%9d" % r for r in row) + "%9d" % sum(row))
    print()

    for i in issues:
        if i["status"] == "wontfix" and not i["has_reason"]:
            problems.append("%s is wontfix without a Reason: line" % i["id"])
        if not i["has_quote"]:
            warns.append("%s has no Quote: line" % i["id"])
        if i["status"] in ("fixed",) and not i["has_fix"]:
            warns.append("%s is fixed but has no Fix: line" % i["id"])

    open_bad = [i["id"] for i in issues if i["status"] == "open" and i["severity"] in ("FATAL", "MAJOR")]
    if open_bad:
        problems.append("open FATAL/MAJOR: " + ", ".join(open_bad))
    blocked_bad = [i["id"] for i in issues if i["status"] == "blocked" and i["severity"] in ("FATAL", "MAJOR")]
    if blocked_bad:
        msg = "blocked FATAL/MAJOR (need the user): " + ", ".join(blocked_bad)
        (problems if a.strict else warns).append(msg)

    pending = [k for k, v in cov.items() if v != "reviewed"]
    if not cov:
        problems.append("no Coverage list found (run line_review.py first)")
    if pending:
        problems.append("chunks not reviewed: " + ", ".join(sorted(pending)))
    d = os.path.dirname(os.path.abspath(a.issues))
    files = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(d, "chunk_*.md")))
    missing = [f for f in files if f not in cov]
    if missing:
        problems.append("chunk files not in Coverage: " + ", ".join(missing))

    print("chunks reviewed: %d of %d" % (sum(1 for v in cov.values() if v == "reviewed"), len(cov)))
    for w in warns:
        print("WARN", w)
    for p in problems:
        print("FAIL", p)
    if a.json:
        json.dump({"issues": issues, "coverage": cov, "problems": problems, "warnings": warns},
                  open(a.json, "w"), indent=1)
    if a.gate:
        if problems:
            print("GATE: FAIL")
            return 1
        print("GATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
