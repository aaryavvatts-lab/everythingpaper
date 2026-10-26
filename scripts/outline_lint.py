#!/usr/bin/env python3
"""outline_lint.py - check a paper outline BEFORE drafting anything.

Fixing a weak argument costs one line here and a rewrite later.

Outline format (plain Markdown):

  # Paper title
  venue: NeurIPS 2026
  page_limit: 9               pages of main text (optional)
  words_per_page: 600         optional, default 600
  claim: the one central claim, a sentence a skeptic could disprove
  C1: first supporting claim
  C2: second supporting claim

  ## 1. Introduction
  words: 900
  purpose: state the problem, the gap and the contribution
  claims: C1, C2
  - bullet notes

  ## 4. Experiments
  words: 2000
  purpose: show C1 and C2 hold against strong baselines
  claims: C1, C2
  evidence: C1 -> Table 2, Fig 3; C2 -> Table 4 (ablation)

Usage:
  python3 -I outline_lint.py outline.md [--relaxed] [--allow-missing] [--json out.json]

FAIL: no title or central claim, no claims C1..., a claim with no evidence (or evidence
'none'/'missing'/'TBD') unless --allow-missing, a section citing an undefined claim, words
over 110 percent of the page budget. WARN: missing standard sections (skipped with
--relaxed for surveys, theory and other formats), missing purpose or words, a central claim
over 40 words or a title under 4 words, words under 50 percent of budget.
"""
import argparse
import json
import re
import sys

STANDARD = [("abstract", r"abstract"), ("introduction", r"introduction|motivation"),
            ("related work or background", r"related|background|prior work|literature"),
            ("method", r"method|approach|model|framework|design|theory|preliminar"),
            ("experiments or results", r"experiment|result|evaluation|analysis|finding"),
            ("limitations or discussion", r"limitation|discussion|threats"),
            ("conclusion", r"conclusion|summary|outlook")]


def parse(text):
    head = {}
    claims = {}
    sections = []
    cur = None
    title = None
    for raw in text.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
            continue
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            cur = {"name": m.group(1).strip(), "words": None, "purpose": "", "claims": [], "evidence": {}, "bullets": 0}
            sections.append(cur)
            continue
        m = re.match(r"^(C\d+)\s*:\s*(.+)$", line.strip(), re.I)
        if m and cur is None:
            claims[m.group(1).upper()] = m.group(2).strip()
            continue
        m = re.match(r"^([A-Za-z_ ]+?)\s*:\s*(.*)$", line.strip())
        if m:
            k, v = m.group(1).strip().lower().replace(" ", "_"), m.group(2).strip()
            if cur is None:
                head[k] = v
            else:
                if k == "words":
                    mm = re.search(r"\d+", v)
                    cur["words"] = int(mm.group(0)) if mm else None
                elif k == "purpose":
                    cur["purpose"] = v
                elif k == "claims":
                    cur["claims"] = [c.strip().upper() for c in re.split(r"[,\s]+", v) if c.strip()]
                elif k == "evidence":
                    for part in v.split(";"):
                        pm = re.match(r"\s*(C\d+)\s*(?:->|=>|:)\s*(.*)$", part, re.I)
                        if pm:
                            cur["evidence"][pm.group(1).upper()] = pm.group(2).strip()
                continue
        if cur is not None and line.lstrip().startswith(("-", "*")):
            cur["bullets"] += 1
    return title, head, claims, sections


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outline")
    ap.add_argument("--relaxed", action="store_true")
    ap.add_argument("--allow-missing", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    try:
        text = open(a.outline, encoding="utf-8").read()
    except OSError as e:
        print("cannot read outline:", e, file=sys.stderr)
        return 2
    title, head, claims, sections = parse(text)
    res = []

    def add(level, msg):
        res.append((level, msg))

    if not title:
        add("FAIL", "no '# Title' line")
    elif len(title.split()) < 4:
        add("WARN", "title is only %d words; a title should say what the paper shows" % len(title.split()))
    cc = head.get("claim", "")
    if not cc:
        add("FAIL", "no 'claim:' line (the one central claim)")
    elif len(cc.split()) > 40:
        add("WARN", "central claim is %d words; make it one sentence a skeptic could disprove" % len(cc.split()))
    if not claims:
        add("FAIL", "no supporting claims (lines like 'C1: ...' before the first section)")
    if not sections:
        add("FAIL", "no '## Section' blocks")

    if not a.relaxed:
        names = " | ".join(s["name"].lower() for s in sections)
        for label, pat in STANDARD:
            if not re.search(pat, names):
                add("WARN", "no section for %s (use --relaxed for surveys or theory papers)" % label)

    evidenced = {}
    total_words = 0
    for s in sections:
        if not s["purpose"]:
            add("WARN", "section '%s' has no purpose: line" % s["name"])
        if s["words"] is None:
            add("WARN", "section '%s' has no words: budget" % s["name"])
        else:
            total_words += s["words"]
        for c in s["claims"]:
            if c not in claims:
                add("FAIL", "section '%s' cites undefined claim %s" % (s["name"], c))
        for c, ev in s["evidence"].items():
            if c not in claims:
                add("FAIL", "section '%s' gives evidence for undefined claim %s" % (s["name"], c))
            evidenced.setdefault(c, []).append(ev)

    for c in claims:
        evs = evidenced.get(c, [])
        if not evs:
            lvl = "WARN" if a.allow_missing else "FAIL"
            add(lvl, "claim %s has no evidence mapped; cut it, soften it, or mark it [TODO-EVIDENCE]" % c)
        elif all(re.fullmatch(r"\s*(none|missing|tbd|todo|n/?a)?\W*", e, re.I) or re.search(r"\b(none|missing|tbd|todo)\b", e, re.I)
                 for e in evs):
            lvl = "WARN" if a.allow_missing else "FAIL"
            add(lvl, "claim %s evidence is %r; resolve before drafting" % (c, "; ".join(evs)[:50]))

    for c, evs in evidenced.items():
        if any(re.search(r"\b(planned|pending|will|expected|to be (run|added)|not yet)\b", e, re.I) for e in evs):
            add("WARN", "claim %s evidence is planned, not in hand; keep it a hypothesis and mark it [TODO-EVIDENCE] in the draft" % c)

    pl = re.search(r"\d+(?:\.\d+)?", head.get("page_limit", ""))
    if pl:
        wpp = re.search(r"\d+", head.get("words_per_page", "600"))
        budget = float(pl.group(0)) * int(wpp.group(0) if wpp else 600)
        if total_words > budget * 1.10:
            add("FAIL", "word budget %d exceeds %.0f (page limit x words per page) by more than 10 percent" % (total_words, budget))
        elif total_words and total_words < budget * 0.5:
            add("WARN", "word budget %d is under half of %.0f; is the paper thin?" % (total_words, budget))

    order = {"FAIL": 0, "WARN": 1}
    res.sort(key=lambda r: order[r[0]])
    for lvl, msg in res:
        print("%-4s %s" % (lvl, msg))
    nf = sum(1 for r in res if r[0] == "FAIL")
    nw = sum(1 for r in res if r[0] == "WARN")
    print("\n%d sections, %d claims, %d words budgeted: %d FAIL, %d WARN" % (len(sections), len(claims), total_words, nf, nw))
    if a.json:
        json.dump([{"level": l, "message": m} for l, m in res], open(a.json, "w"), indent=1)
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
