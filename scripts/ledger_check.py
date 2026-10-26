#!/usr/bin/env python3
"""ledger_check.py - grade the Requirements Ledger.

Usage:
  python3 -I ledger_check.py ledger.md [--json out.json]

Reads table rows of the form
  | R1 | Asked | Fit the 9 page limit | PASS | Sec 5 end, compile_check: 9 pages |
Status is OPEN, PASS, FAIL or BLOCKED. Exit 1 while any row is OPEN or FAIL, or a PASS
row has no evidence. BLOCKED rows (need something only the user can supply) are listed
and do not fail the check; they must be named in the final report.
"""
import argparse
import json
import re
import sys

ROW = re.compile(r"^\|\s*(R\d+)\s*\|\s*(Asked|Implied)\s*\|(.*?)\|\s*(OPEN|PASS|FAIL|BLOCKED)\s*\|(.*)\|\s*$", re.I)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ledger")
    ap.add_argument("--json")
    a = ap.parse_args()
    try:
        text = open(a.ledger, encoding="utf-8").read()
    except OSError as e:
        print("cannot read ledger:", e, file=sys.stderr)
        return 2
    rows = []
    for line in text.split("\n"):
        m = ROW.match(line.strip())
        if m:
            rows.append({"id": m.group(1).upper(), "kind": m.group(2).title(), "req": m.group(3).strip(),
                         "status": m.group(4).upper(), "evidence": m.group(5).strip()})
    if not rows:
        print("FAIL no ledger rows found (expected | R1 | Asked | ... | OPEN | |)")
        return 1
    bad = False
    for r in rows:
        flag = ""
        if r["status"] in ("OPEN", "FAIL"):
            flag = "  <- not done"
            bad = True
        elif r["status"] == "PASS" and not r["evidence"]:
            flag = "  <- PASS needs evidence"
            bad = True
        elif r["status"] == "BLOCKED":
            flag = "  <- needs the user"
        print("%-4s %-8s %-8s %s%s" % (r["id"], r["kind"], r["status"], r["req"][:70], flag))
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "BLOCKED", "OPEN")}
    print("\n%d requirements: %d PASS, %d FAIL, %d BLOCKED, %d OPEN" % (
        len(rows), counts["PASS"], counts["FAIL"], counts["BLOCKED"], counts["OPEN"]))
    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1)
    print("LEDGER: FAIL" if bad else "LEDGER: PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
