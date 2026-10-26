#!/usr/bin/env python3
"""paper_lint.py - mechanical checks on a manuscript (.tex, .md, .txt).

Usage:
  python3 -I paper_lint.py paper.tex [--bib refs.bib] [--no-dashes] [--max-sentence 45] [--json out.json]

FAIL (blocks delivery): [TODO-EVIDENCE] markers, TODO/TBD/FIXME/XXX/lorem ipsum, unresolved
  citation placeholders ([CITE], \\cite{?}, ??), \\ref to a label that does not exist,
  \\cite key missing from the bib, duplicate labels, banned dashes with --no-dashes.
WARN: unused labels and bib entries, repeated words, acronyms used twice and never
  defined, over-long sentences, overclaim phrases, unsupported "significant", AI-tell phrases,
  abstract numbers that never appear in the body, mixed US/UK spelling.

These are mechanics. They do not know whether a claim is true; Round 2 does.
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

AI_TELLS = [r"\bdelve[sd]?\b", r"\btapestry\b", r"it is worth noting", r"it is important to note",
            r"in the realm of", r"plays? a (crucial|pivotal|vital) role", r"\bunderscores?\b",
            r"\bpivotal\b", r"landscape of", r"ever-evolving", r"a testament to", r"\bseamlessly\b",
            r"\bleverag(e|es|ed|ing)\b", r"\bmeticulous(ly)?\b", r"in today'?s (fast-paced|digital)",
            r"\bshed light on\b", r"paves? the way"]
OVERCLAIM = [r"\bobvious(ly)?\b", r"\bclearly\b", r"\btrivial(ly)?\b", r"\bundoubtedly\b", r"it is well[- ]known",
             r"\bwithout (a )?doubt\b", r"\bproves? that\b(?! (the|a|an|every|for)\b)", r"\bfirst to\b",
             r"\bno prior work\b", r"\bstate[- ]of[- ]the[- ]art\b", r"\bbreakthrough\b", r"\brevolutionary\b",
             r"\bperfect(ly)?\b", r"\balways\b", r"\bnever\b"]
STAT_NEAR = re.compile(r"(p\s*[<=>]|\bp-?value|confidence interval|\bCI\b|t-test|Wilcoxon|ANOVA|bootstrap|std|\\pm|±|"
                       r"standard (deviation|error)|permutation|Mann|significance test)", re.I)
ACR_OK = {"AI", "ML", "US", "UK", "EU", "PDF", "URL", "HTML", "GPU", "CPU", "API", "IEEE", "ACM", "OK", "ID", "IID",
          "MATH", "II", "III", "IV", "TODO", "RGB", "LSTM", "CNN", "SGD", "KL", "MSE", "MAE", "LLM", "NLP", "SOTA",
          "AUC", "ROC", "FAQ", "AM", "PM", "NASA", "DNA", "RNA", "MRI", "CT", "BERT", "GPT"}
SPELL = [("color", "colour"), ("analyze", "analyse"), ("behavior", "behaviour"), ("modeling", "modelling"),
         ("optimize", "optimise"), ("generalize", "generalise"), ("center", "centre"), ("labeled", "labelled"),
         ("organization", "organisation"), ("normalize", "normalise")]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--bib")
    ap.add_argument("--no-dashes", action="store_true", help="FAIL on em dashes, en dashes and LaTeX ---")
    ap.add_argument("--max-sentence", type=int, default=45)
    ap.add_argument("--json")
    a = ap.parse_args()
    if not os.path.isfile(a.file):
        print("no such file:", a.file, file=sys.stderr)
        return 2
    tex = C.is_tex(a.file)
    raw = C.read_text(a.file)
    body_lines = C.tex_body_lines(raw) if tex else [(i + 1, l) for i, l in enumerate(raw.split("\n"))]
    findings = []  # (level, code, line, message)

    def add(level, code, line, msg):
        findings.append((level, code, line, msg))

    # --- placeholders --------------------------------------------------------------------
    ph = [(r"\[TODO-EVIDENCE[^\]]*\]?", "todo-evidence"), (r"\b(TODO|TBD|FIXME|XXX)\b(?!-EVIDENCE)", "todo"),
          (r"lorem ipsum", "lorem"), (r"\[CITE\]|\[\?\]|\\cite\{\?+\}|\(\?\?\)", "cite-placeholder"),
          (r"\?\?", "unresolved-ref"), (r"\\(?:cite|ref)\{\s*\}", "empty-ref"), (r"\bcitation needed\b", "cite-needed")]
    for ln, line in body_lines:
        for pat, code in ph:
            for m in re.finditer(pat, line, re.I if code != "todo" else 0):
                add("FAIL", code, ln, "unresolved: %s" % m.group(0)[:70])

    # --- labels, refs, cites ---------------------------------------------------------------
    labels = collections.defaultdict(list)
    refs = collections.defaultdict(list)
    cites = collections.defaultdict(list)
    if tex:
        for ln, line in body_lines:
            for m in re.finditer(r"\\label\{([^}]*)\}", line):
                labels[m.group(1)].append(ln)
            for m in re.finditer(r"\\(?:ref|eqref|autoref|cref|Cref|pageref|vref)\*?\{([^}]*)\}", line):
                for k in m.group(1).split(","):
                    refs[k.strip()].append(ln)
            for m in re.finditer(r"\\(?:cite[a-zA-Z]*|parencite|textcite|autocite|nocite)\*?(?:\[[^\]]*\])*\{([^}]*)\}", line):
                for k in m.group(1).split(","):
                    if k.strip():
                        cites[k.strip()].append(ln)
        for k, ls in labels.items():
            if len(ls) > 1:
                add("FAIL", "dup-label", ls[1], "label %s defined %d times (lines %s)" % (k, len(ls), ",".join(map(str, ls))))
        for k, ls in refs.items():
            if k not in labels and k != "*":
                add("FAIL", "undefined-ref", ls[0], "\\ref to undefined label %s" % k)
        for k, ls in labels.items():
            if k not in refs and re.match(r"(fig|tab|sec|thm|lem|prop|cor|alg|app)[:_-]", k, re.I):
                add("WARN", "unused-label", ls[0], "label %s is never referenced" % k)
        bibkeys = None
        if a.bib and os.path.isfile(a.bib):
            btxt = C.read_text(a.bib)
            bibkeys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", btxt))
        else:
            inline = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", raw)
            if inline:
                bibkeys = set(inline)
        if bibkeys is not None:
            for k, ls in cites.items():
                if k not in bibkeys:
                    add("FAIL", "missing-bib", ls[0], "cited key %s is not in the bibliography" % k)
            for k in sorted(bibkeys - set(cites)):
                add("WARN", "unused-bib", 0, "bib entry %s is never cited" % k)
        elif cites:
            add("WARN", "no-bib", 0, "no --bib given and no \\bibitem entries; cited keys were not checked")

    # --- dashes ----------------------------------------------------------------------------
    if a.no_dashes:
        for ln, line in body_lines:
            for m in re.finditer("\u2014|\u2013|---", line):
                add("FAIL", "dash", ln, "banned dash %r" % m.group(0))

    # --- prose checks on cleaned units -------------------------------------------------------
    units = C.units_for(a.file)
    sentences = []
    for src, sec, text in units:
        for s in C.split_sentences(text):
            sentences.append((src, sec, s))
    full_text = " ".join(t for _, _, t in units)

    for src, sec, s in sentences:
        wc = C.word_count(s)
        if wc > a.max_sentence:
            add("WARN", "long-sentence", src, "%d words in [%s]: %s..." % (wc, sec[:30], s[:80]))
        for m in re.finditer(r"\b(\w+)\s+\1\b", s, re.I):
            w = m.group(1)
            if w.lower() not in ("that", "had") and not w.isdigit() and len(w) > 1:
                add("WARN", "repeated-word", src, "repeated word '%s %s' in: %s..." % (w, w, s[:70]))
        low = s.lower()
        for pat in AI_TELLS:
            m = re.search(pat, low)
            if m:
                add("WARN", "ai-tell", src, "AI-tell phrase '%s': %s..." % (m.group(0), s[:70]))
        for pat in OVERCLAIM:
            m = re.search(pat, low)
            if m:
                add("WARN", "overclaim", src, "check strength of '%s': %s..." % (m.group(0), s[:70]))
        for m in re.finditer(r"\bsignifican(t|tly)\b", low):
            ctx = s[max(0, m.start() - 160): m.end() + 160]
            if not STAT_NEAR.search(ctx):
                add("WARN", "significant-no-test", src, "'significant' without a test or interval nearby: %s..." % s[:70])
                break

    # acronyms
    def_ac = set(re.findall(r"\(\s*([A-Z][A-Za-z]{1,7}s?)\s*\)", full_text))
    def_ac |= set(re.findall(r"\\newacronym\{[^}]*\}\{([^}]*)\}", raw))
    counts = collections.Counter(re.findall(r"\b[A-Z]{2,7}s?\b", re.sub(r"\[cite:[^\]]*\]|\(ref:[^)]*\)", " ", full_text)))
    for ac, n in counts.items():
        base = ac.rstrip("s") if ac.endswith("s") and len(ac) > 3 else ac
        if n >= 2 and base not in ACR_OK and ac not in ACR_OK and base not in def_ac and ac not in def_ac:
            add("WARN", "undefined-acronym", 0, "acronym %s used %d times, no '(%s)' definition found" % (ac, n, base))

    # abstract numbers vs body
    abs_text = " ".join(t for _, sec, t in units if sec.lower().startswith("abstract"))
    body_text = " ".join(t for _, sec, t in units if not sec.lower().startswith("abstract"))
    if abs_text and body_text:
        for num in sorted(set(re.findall(r"\d+(?:\.\d+)?%?", abs_text))):
            core = num.rstrip("%")
            if len(core.replace(".", "")) < 2:
                continue
            if re.fullmatch(r"(19|20)\d\d", core):
                continue
            if not re.search(r"(?<![\d.])" + re.escape(core) + r"(?![\d])", body_text):
                add("WARN", "abstract-number", 0, "number %s in the abstract never appears in the body" % num)
    elif not abs_text:
        add("WARN", "no-abstract", 0, "no abstract found (\\begin{abstract} or a heading named Abstract)")

    # spelling variants
    low_all = full_text.lower()
    for us, uk in SPELL:
        if re.search(r"\b" + us, low_all) and re.search(r"\b" + uk, low_all):
            add("WARN", "mixed-spelling", 0, "both US '%s' and UK '%s' spellings appear" % (us, uk))

    # --- report ------------------------------------------------------------------------------
    order = {"FAIL": 0, "WARN": 1}
    findings.sort(key=lambda f: (order[f[0]], f[1], f[2]))
    nfail = sum(1 for f in findings if f[0] == "FAIL")
    nwarn = sum(1 for f in findings if f[0] == "WARN")
    for level, code, line, msg in findings:
        print("%-4s %-20s %s%s" % (level, code, ("line %d: " % line) if line else "", msg))
    print("\n%s: %d FAIL, %d WARN, %d sentences, ~%d words" % (
        os.path.basename(a.file), nfail, nwarn, len(sentences), C.word_count(full_text)))
    if a.json:
        json.dump([{"level": l, "code": c, "line": ln, "message": m} for l, c, ln, m in findings],
                  open(a.json, "w"), indent=1)
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
