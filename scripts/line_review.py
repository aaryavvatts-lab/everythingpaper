#!/usr/bin/env python3
"""line_review.py - split a manuscript into numbered sentences and review chunks.

Round 2 of everythingpaper reads EVERY sentence. This tool makes that auditable: each
sentence gets an ID (L0001 ...), chunks of about 40 sentences are written to files, and a
Coverage list in issues.md records which chunks have been reviewed.

Usage:
  python3 -I line_review.py paper.tex --out review/ [--chunk 40]
  python3 -I line_review.py paper.md  --out review/
  python3 -I line_review.py paper.tex --stats

Re-running after edits keeps issues.md and its issue blocks. Chunks whose text changed are
set back to `pending` in the Coverage list so you re-read exactly what changed.
"""
import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

ISSUES_HEADER = """# Issues: {name}

One block per issue, exactly in this shape (see references/checks.md). Real issues go
below this note, outside the code fence:

```
### I-001 | MAJOR | open | L0123-L0124 | claim-support
Quote: "..."
Problem: ...
Fix: ...
```

Severity: FATAL, MAJOR, MINOR, NIT. Status: open, fixed, blocked, wontfix (add a `Reason:` line).

"""


def build_sentences(path):
    sents = []
    n = 0
    for src_line, section, text in C.units_for(path):
        for s in C.split_sentences(text):
            if C.word_count(s) < 2:
                continue
            n += 1
            sents.append({"id": "L%04d" % n, "src": src_line, "section": section, "text": s})
    return sents


def pack_chunks(sents, size):
    """Pack sentences into chunks of at most `size`, never splitting a section across more
    chunks than needed and merging small neighbouring sections. Keeping chunks section-aligned
    means an edit only changes the chunk that holds it, so earlier review work is kept."""
    groups = []
    for s in sents:
        if groups and groups[-1][0] == s["section"]:
            groups[-1][1].append(s)
        else:
            groups.append((s["section"], [s]))
    chunks, cur = [], []
    for _, g in groups:
        pieces = [g[i:i + size] for i in range(0, len(g), size)]
        for piece in pieces:
            if cur and len(cur) + len(piece) > size:
                chunks.append(cur)
                cur = []
            cur = cur + piece
            if len(cur) >= size:
                chunks.append(cur)
                cur = []
    if cur:
        chunks.append(cur)
    return chunks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--out", default="review")
    ap.add_argument("--chunk", type=int, default=40, help="sentences per chunk (default 40)")
    ap.add_argument("--stats", action="store_true", help="print counts and exit")
    a = ap.parse_args()

    if not os.path.isfile(a.file):
        print("no such file:", a.file, file=sys.stderr)
        return 2
    sents = build_sentences(a.file)
    if not sents:
        print("FAIL no sentences found; is the file empty or only a preamble?")
        return 1

    if a.stats:
        by = {}
        for s in sents:
            d = by.setdefault(s["section"], [0, 0])
            d[0] += 1
            d[1] += C.word_count(s["text"])
        print("%-48s %9s %7s" % ("section", "sentences", "words"))
        for k, (n, w) in by.items():
            print("%-48s %9d %7d" % (k[:48], n, w))
        print("total sentences %d, words %d" % (len(sents), sum(C.word_count(s["text"]) for s in sents)))
        return 0

    os.makedirs(a.out, exist_ok=True)
    chunks = pack_chunks(sents, a.chunk)
    state_path = os.path.join(a.out, "chunks.json")
    old = {}
    if os.path.isfile(state_path):
        try:
            old = json.load(open(state_path))
        except Exception:
            old = {}
    ipath = os.path.join(a.out, "issues.md")
    prev_cov = {}
    if os.path.isfile(ipath):
        for mm in re.finditer(r"^- (chunk_\d+): (\w+)", open(ipath, encoding="utf-8").read(), re.M):
            prev_cov[mm.group(1)] = mm.group(2)
    reviewed_hashes = {h for n, h in old.items() if prev_cov.get(n) == "reviewed"}
    new_state = {}
    changed = []
    # remove stale chunk files
    for f in os.listdir(a.out):
        if re.match(r"chunk_\d+\.md$", f):
            os.remove(os.path.join(a.out, f))
    for ci, ch in enumerate(chunks, 1):
        name = "chunk_%02d" % ci
        body = "\n".join(s["text"] for s in ch)
        h = hashlib.sha1(body.encode("utf-8")).hexdigest()
        new_state[name] = h
        if h not in reviewed_hashes:
            changed.append(name)
        lines = ["# %s (sentences %s-%s of %s)" % (name, ch[0]["id"], ch[-1]["id"], sents[-1]["id"]), ""]
        cur = None
        for s in ch:
            if s["section"] != cur:
                cur = s["section"]
                lines.append("## Section: %s" % cur)
            lines.append("%s [src:%s] %s" % (s["id"], s["src"], s["text"]))
        open(os.path.join(a.out, name + ".md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump(new_state, open(state_path, "w"), indent=1)

    # issues.md: keep existing body, rewrite Coverage
    body = ""
    if os.path.isfile(ipath):
        t = open(ipath, encoding="utf-8").read()
        m = re.search(r"^## Coverage\s*$", t, re.M)
        body = t[:m.start()] if m else t
    else:
        body = ISSUES_HEADER.format(name=os.path.basename(a.file))
    cov = ["## Coverage", ""]
    for name in new_state:
        cov.append("- %s: %s" % (name, "pending" if name in changed else "reviewed"))
    open(ipath, "w", encoding="utf-8").write(body.rstrip() + "\n\n" + "\n".join(cov) + "\n")

    print("%d sentences in %d chunks -> %s" % (len(sents), len(chunks), a.out))
    if old:
        print("chunks to (re)read: %s" % (", ".join(changed) or "none; all unchanged chunks keep their reviewed status"))
    else:
        print("first run: every chunk is pending")
    return 0


if __name__ == "__main__":
    sys.exit(main())
