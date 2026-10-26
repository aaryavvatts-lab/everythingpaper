"""Shared helpers for everythingpaper scripts: read a manuscript (.tex, .md or .txt),
turn it into clean paragraphs and numbered sentences, and keep source line numbers.

Standard library only. Scripts import this with a sys.path insert so they also work
under `python3 -I`.
"""
import os
import re

ABBREV = ["e.g.", "i.e.", "et al.", "Fig.", "Figs.", "Eq.", "Eqs.", "Sec.", "Secs.", "Tab.",
          "vs.", "cf.", "etc.", "approx.", "No.", "Dr.", "Prof.", "resp.", "Ref.", "Refs.",
          "Alg.", "Thm.", "Lem.", "Prop.", "Cor.", "Def.", "St.", "Inc.", "Ltd.", "w.r.t.",
          "s.t.", "a.k.a."]


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def is_tex(path):
    return path.lower().endswith((".tex", ".ltx"))


def strip_comment(line):
    """Remove an unescaped LaTeX % comment from one line."""
    out = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            out.append(line[i:i + 2])
            i += 2
            continue
        if c == "%":
            break
        out.append(c)
        i += 1
    return "".join(out)


def tex_body_lines(text):
    """Return [(lineno, line)] for the document body with comments removed.
    Lines before \\begin{document} (the preamble) are dropped when present."""
    lines = text.split("\n")
    start = 0
    end = len(lines)
    for i, l in enumerate(lines):
        if "\\begin{document}" in strip_comment(l):
            start = i + 1
            break
    for i in range(len(lines) - 1, -1, -1):
        if "\\end{document}" in strip_comment(lines[i]):
            end = i
            break
    return [(i + 1, strip_comment(lines[i])) for i in range(start, end)]


MATH_ENVS = r"equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|displaymath|math|split|array"


def clean_tex_inline(s):
    """Make a LaTeX fragment readable: citations, refs, math, formatting commands."""
    s = re.sub(r"\\begin\{(%s)\}.*?\\end\{\1\}" % MATH_ENVS, " MATH ", s, flags=re.S)
    s = re.sub(r"\$\$.*?\$\$", " MATH ", s, flags=re.S)
    s = re.sub(r"\\\[.*?\\\]", " MATH ", s, flags=re.S)
    s = re.sub(r"\$[^$\n]+\$", "MATH", s)
    s = re.sub(r"\\(?:cite[a-zA-Z]*|parencite|textcite|autocite)\*?(?:\[[^\]]*\])*\{([^}]*)\}", r"[cite:\1]", s)
    s = re.sub(r"\\(?:ref|eqref|autoref|cref|Cref|pageref)\*?\{([^}]*)\}", r"(ref:\1)", s)
    s = re.sub(r"\\(?:bibliography|bibliographystyle|addbibresource|maketitle|tableofcontents|printbibliography)\b(\[[^\]]*\])?(\{[^}]*\})?", " ", s)
    s = re.sub(r"\\(?:label|centering|noindent|clearpage|newpage|vspace\*?\{[^}]*\}|hspace\*?\{[^}]*\}|bigskip|medskip|smallskip)\b(\{[^}]*\})?", " ", s)
    s = re.sub(r"\\(?:includegraphics)(\[[^\]]*\])?\{[^}]*\}", " ", s)
    s = re.sub(r"\\(?:textbf|textit|emph|textsc|texttt|underline|mathrm|mathbf|text|textrm)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\footnote\{([^{}]*)\}", r" (footnote: \1)", s)
    s = re.sub(r"\\begin\{[^}]*\}(\[[^\]]*\])?(\{[^}]*\})?", " ", s)
    s = re.sub(r"\\end\{[^}]*\}", " ", s)
    s = re.sub(r"\\item\b", " - ", s)
    s = re.sub(r"~", " ", s)
    s = s.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_").replace("\\#", "#")
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


SECTION_RE = re.compile(r"\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\{([^}]*)\}")
CAPTION_RE = re.compile(r"\\caption(?:\[[^\]]*\])?\{")


def tex_units(path):
    """Yield (src_line, section, text) paragraph units from a .tex file.
    Captions become their own units with section 'caption: <section>'."""
    text = read_text(path)
    lines = tex_body_lines(text)
    section = "(front matter)"
    units = []
    buf = []
    buf_line = None
    in_abs = False
    in_math = 0

    def flush():
        nonlocal buf, buf_line
        if buf:
            raw = "\n".join(buf)
            # pull captions out as separate units
            while True:
                m = CAPTION_RE.search(raw)
                if not m:
                    break
                depth = 1
                j = m.end()
                while j < len(raw) and depth:
                    if raw[j] == "{":
                        depth += 1
                    elif raw[j] == "}":
                        depth -= 1
                    j += 1
                cap = raw[m.end():j - 1]
                c = clean_tex_inline(cap)
                if c:
                    units.append((buf_line, "caption: " + section, c))
                raw = raw[:m.start()] + " " + raw[j:]
            c = clean_tex_inline(raw)
            if c and re.search(r"[A-Za-z]{3}", c):
                units.append((buf_line, section, c))
        buf = []
        buf_line = None

    for ln, line in lines:
        if re.search(r"\\begin\{abstract\}", line):
            flush()
            section = "Abstract"
            line = re.sub(r"\\begin\{abstract\}", "", line)
        if re.search(r"\\end\{abstract\}", line):
            line = re.sub(r"\\end\{abstract\}", "", line)
            buf.append(line)
            if buf_line is None:
                buf_line = ln
            flush()
            section = "(after abstract)"
            continue
        tm = re.search(r"\\title(?:\[[^\]]*\])?\{(.*)\}\s*$", line)
        if tm and not buf:
            units.append((ln, "Title", clean_tex_inline(tm.group(1))))
            continue
        sm = SECTION_RE.search(line)
        if sm:
            flush()
            section = clean_tex_inline(sm.group(2))
            continue
        if re.search(r"\\begin\{(%s)\}" % MATH_ENVS, line):
            in_math += 1
        if in_math:
            buf.append(line)
            if buf_line is None:
                buf_line = ln
            if re.search(r"\\end\{(%s)\}" % MATH_ENVS, line):
                in_math -= 1
            continue
        if not line.strip():
            flush()
            continue
        if buf_line is None:
            buf_line = ln
        buf.append(line)
    flush()
    return units


def md_units(path):
    text = read_text(path)
    section = "(front matter)"
    units = []
    buf = []
    buf_line = None
    in_code = False

    def flush():
        nonlocal buf, buf_line
        if buf:
            t = " ".join(x.strip() for x in buf).strip()
            if t and re.search(r"[A-Za-z]{3}", t):
                units.append((buf_line, section, t))
        buf = []
        buf_line = None

    for i, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("```"):
            flush()
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush()
            section = m.group(2).strip()
            continue
        if not line.strip():
            flush()
            continue
        if line.strip().startswith("|") or re.match(r"^\s*[-*_]{3,}\s*$", line):
            flush()
            continue
        if buf_line is None:
            buf_line = i
        buf.append(line)
    flush()
    return units


def units_for(path):
    return tex_units(path) if is_tex(path) else md_units(path)


def split_sentences(text):
    t = text
    for a in ABBREV:
        t = t.replace(a, a.replace(".", "\u2024"))
    t = re.sub(r"(\d)\.(\d)", "\\1\u2024\\2", t)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\[\(\"'\\-])", t)
    out = []
    for p in parts:
        p = p.replace("\u2024", ".").strip()
        if p:
            out.append(p)
    return out


def word_count(s):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", s))
