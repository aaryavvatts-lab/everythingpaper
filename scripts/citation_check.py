#!/usr/bin/env python3
"""citation_check.py - check a BibTeX file, optionally against the public Crossref and arXiv APIs.

Usage:
  python3 -I citation_check.py refs.bib [--tex paper.tex] [--online] [--max-online 60] [--json out.json]

Offline (default, no network): duplicate keys and titles, missing required fields, malformed
DOIs, implausible years, "and others" author lists, URL-form DOIs, cited-but-missing and
uncited keys when --tex is given.

--online (sends titles and DOIs from the bib to api.crossref.org and export.arxiv.org; skip
it for a confidential manuscript): confirms each DOI resolves, compares the registered title
with the bib title, flags retractions Crossref records, suggests a DOI for entries without
one, and checks arXiv ids. A match is evidence the reference EXISTS. It does not prove the
reference supports the claim it is cited for; read the source for that.
"""
import argparse
import difflib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

REQUIRED = {
    "article": [("author",), ("title",), ("journal", "journaltitle"), ("year", "date")],
    "inproceedings": [("author",), ("title",), ("booktitle",), ("year", "date")],
    "conference": [("author",), ("title",), ("booktitle",), ("year", "date")],
    "book": [("author", "editor"), ("title",), ("publisher",), ("year", "date")],
    "incollection": [("author",), ("title",), ("booktitle",), ("publisher",), ("year", "date")],
    "phdthesis": [("author",), ("title",), ("school", "institution"), ("year", "date")],
    "mastersthesis": [("author",), ("title",), ("school", "institution"), ("year", "date")],
    "techreport": [("author",), ("title",), ("institution",), ("year", "date")],
    "misc": [("title",), ("year", "date")],
    "online": [("title",), ("url",)],
    "unpublished": [("author",), ("title",), ("note",)],
}
UA = "everythingpaper-citation-check/1.0 (research manuscript QA)"


def parse_bib(text):
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        etype = m.group(1).lower()
        if etype in ("comment", "string", "preamble"):
            continue
        i = m.end()
        depth = 1
        j = i
        while j < len(text) and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        body = text[i:j - 1]
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            name = fm.group(1).lower()
            k = fm.end()
            if k >= len(body):
                continue
            if body[k] == "{":
                d = 1
                e = k + 1
                while e < len(body) and d:
                    if body[e] == "{":
                        d += 1
                    elif body[e] == "}":
                        d -= 1
                    e += 1
                val = body[k + 1:e - 1]
            elif body[k] == '"':
                e = body.find('"', k + 1)
                val = body[k + 1:e] if e > 0 else ""
            else:
                mm = re.match(r"[^,\n]+", body[k:])
                val = mm.group(0).strip() if mm else ""
            fields.setdefault(name, re.sub(r"\s+", " ", val).strip())
        entries.append({"key": m.group(2), "type": etype, "fields": fields, "line": text.count("\n", 0, m.start()) + 1})
    return entries


def norm(s):
    s = re.sub(r"\\[a-zA-Z]+\s*", " ", s or "")
    s = re.sub(r"[{}\\$]", "", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def get_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bib")
    ap.add_argument("--tex")
    ap.add_argument("--online", action="store_true")
    ap.add_argument("--max-online", type=int, default=60)
    ap.add_argument("--json")
    a = ap.parse_args()
    if not os.path.isfile(a.bib):
        print("no such file:", a.bib, file=sys.stderr)
        return 2
    entries = parse_bib(open(a.bib, encoding="utf-8", errors="replace").read())
    if not entries:
        print("FAIL no BibTeX entries found in", a.bib)
        return 1
    out = []

    def add(level, key, msg):
        out.append((level, key, msg))

    keys = [e["key"] for e in entries]
    for k in sorted({k for k in keys if keys.count(k) > 1}):
        add("FAIL", k, "duplicate key")
    titles = {}
    this_year = date.today().year
    for e in entries:
        f, k = e["fields"], e["key"]
        for group in REQUIRED.get(e["type"], [("title",), ("year", "date")]):
            if not any(f.get(g) for g in group):
                add("FAIL" if group[0] in ("title", "author") else "WARN", k,
                    "missing %s (entry type @%s)" % ("/".join(group), e["type"]))
        t = norm(f.get("title", ""))
        if t:
            if t in titles:
                add("WARN", k, "same title as %s (duplicate reference?)" % titles[t])
            titles[t] = k
        y = re.search(r"\d{4}", f.get("year", "") or f.get("date", ""))
        if (f.get("year") or f.get("date")) and not y:
            add("WARN", k, "year not a four-digit number: %r" % (f.get("year") or f.get("date")))
        elif y and not (1600 <= int(y.group(0)) <= this_year + 1):
            add("WARN", k, "implausible year %s" % y.group(0))
        d = f.get("doi", "")
        if d:
            if re.match(r"https?://", d, re.I) or d.lower().startswith("doi:"):
                add("WARN", k, "doi field should hold the bare DOI, not a URL or 'doi:' prefix: %s" % d[:60])
            bare = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", d, flags=re.I)
            if not re.match(r"^10\.\d{4,9}/\S+$", bare):
                add("FAIL", k, "malformed DOI: %s" % d[:60])
        if re.search(r"\band others\b|\bet al\b", f.get("author", ""), re.I):
            add("WARN", k, "author list is truncated ('others'/'et al.'); some venues require full lists")
        if e["type"] == "misc" and (f.get("journal") or f.get("booktitle")):
            add("WARN", k, "@misc entry has a journal or booktitle; use @article or @inproceedings")
        if e["type"] in ("article", "inproceedings") and not (f.get("doi") or f.get("url") or f.get("eprint")):
            add("WARN", k, "no DOI, URL or eprint; hard to verify")
        if re.search(r"\b(placeholder|todo|tbd|xxx|lorem)\b", " ".join(f.values()), re.I):
            add("FAIL", k, "placeholder text in entry")

    if a.tex and os.path.isfile(a.tex):
        txt = open(a.tex, encoding="utf-8", errors="replace").read()
        used = set()
        for m in re.finditer(r"\\(?:cite[a-zA-Z]*|parencite|textcite|autocite|nocite)\*?(?:\[[^\]]*\])*\{([^}]*)\}", txt):
            for kk in m.group(1).split(","):
                used.add(kk.strip())
        for kk in sorted(used - set(keys) - {"*"}):
            add("FAIL", kk, "cited in the paper but missing from the bib")
        for kk in sorted(set(keys) - used):
            add("WARN", kk, "in the bib but never cited")

    if a.online:
        n = 0
        for e in entries:
            if n >= a.max_online:
                add("WARN", "-", "stopped online checks after %d entries (--max-online)" % a.max_online)
                break
            f, k = e["fields"], e["key"]
            title = f.get("title", "")
            doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", f.get("doi", ""), flags=re.I)
            eprint = f.get("eprint", "")
            try:
                if doi:
                    n += 1
                    try:
                        msg = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
                    except urllib.error.HTTPError as ex:
                        if ex.code == 404:
                            add("FAIL", k, "DOI not found at Crossref: %s (may be a DataCite or other registry DOI; check by hand)" % doi)
                            continue
                        raise
                    reg = (msg.get("title") or [""])[0]
                    r = difflib.SequenceMatcher(None, norm(title), norm(reg)).ratio()
                    if r < 0.85:
                        add("WARN", k, "bib title differs from the registered title (match %.2f): bib=%r registered=%r" % (r, title[:60], reg[:60]))
                    else:
                        add("OK", k, "DOI resolves, title matches (%.2f)" % r)
                    ub = msg.get("updated-by") or []
                    if any("retract" in (u.get("type", "") + u.get("label", "")).lower() for u in ub):
                        add("FAIL", k, "Crossref records a retraction for this work")
                elif eprint:
                    n += 1
                    xml = get_text("http://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(eprint))
                    m = re.search(r"<entry>.*?<title>(.*?)</title>", xml, re.S)
                    if not m:
                        add("FAIL", k, "arXiv id %s not found" % eprint)
                    else:
                        reg = re.sub(r"\s+", " ", m.group(1)).strip()
                        r = difflib.SequenceMatcher(None, norm(title), norm(reg)).ratio()
                        add("OK" if r >= 0.85 else "WARN", k, "arXiv %s title match %.2f" % (eprint, r) if r >= 0.85
                            else "arXiv title differs (match %.2f): bib=%r arxiv=%r" % (r, title[:60], reg[:60]))
                elif title:
                    n += 1
                    q = urllib.parse.quote(title + " " + (f.get("author", "").split(" and ")[0]))
                    items = get_json("https://api.crossref.org/works?rows=1&query.bibliographic=" + q)["message"]["items"]
                    if items:
                        reg = (items[0].get("title") or [""])[0]
                        r = difflib.SequenceMatcher(None, norm(title), norm(reg)).ratio()
                        if r >= 0.9:
                            add("INFO", k, "no DOI in bib; Crossref match %.2f suggests doi = {%s}" % (r, items[0].get("DOI")))
                        else:
                            add("WARN", k, "no DOI and no confident Crossref match (best %.2f: %r); verify this reference exists by hand" % (r, reg[:60]))
                    else:
                        add("WARN", k, "no Crossref match; verify this reference exists by hand")
            except Exception as ex:  # network problems are not paper problems
                add("WARN", k, "online check failed (%s); verify by hand" % ex.__class__.__name__)
            time.sleep(0.25)

    order = {"FAIL": 0, "WARN": 1, "INFO": 2, "OK": 3}
    out.sort(key=lambda x: (order[x[0]], x[1]))
    for level, key, msg in out:
        if level == "OK" and not a.online:
            continue
        print("%-4s %-28s %s" % (level, key[:28], msg))
    nf = sum(1 for o in out if o[0] == "FAIL")
    nw = sum(1 for o in out if o[0] == "WARN")
    print("\n%d entries: %d FAIL, %d WARN%s" % (len(entries), nf, nw, "" if a.online else " (offline; add --online to check existence)"))
    if a.json:
        json.dump([{"level": l, "key": k, "message": m} for l, k, m in out], open(a.json, "w"), indent=1)
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
