#!/usr/bin/env bash
# compile_check.sh - build a LaTeX paper in a scratch folder and report what a reviewer would see.
#
# Usage: compile_check.sh paper.tex [--out DIR] [--page-limit N]
#
# Picks the first available engine: latexmk, tectonic, pdflatex (+bibtex or biber).
# Builds in DIR (default $TMPDIR/everythingpaper-qc/<name>, outside your paper folder). Reports: engine,
# build status, pages, undefined references and citations, overfull boxes, missing files.
# Exit: 0 clean, 1 problems (failed build, undefined refs, over the page limit), 2 no compiler.
set -u

tex=""; out=""; limit=""
while [ $# -gt 0 ]; do
  case "$1" in
    --out) out="$2"; shift 2;;
    --page-limit) limit="$2"; shift 2;;
    -h|--help) sed -n '2,10p' "$0"; exit 0;;
    *) tex="$1"; shift;;
  esac
done
if [ -z "$tex" ] || [ ! -f "$tex" ]; then echo "usage: compile_check.sh paper.tex [--out DIR] [--page-limit N]"; exit 2; fi

dir="$(cd "$(dirname "$tex")" && pwd)"; base="$(basename "$tex" .tex)"
# default build folder is outside the paper folder so QC files never land in the delivery folder
[ -z "$out" ] && out="${TMPDIR:-/tmp}/everythingpaper-qc/$base"
mkdir -p "$out"; out="$(cd "$out" && pwd)"
log="$out/$base.build.log"; : > "$log"
engine=""; status=1

if command -v latexmk >/dev/null 2>&1; then
  engine="latexmk"
  (cd "$dir" && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir="$out" "$base.tex" >>"$log" 2>&1); status=$?
elif command -v tectonic >/dev/null 2>&1; then
  engine="tectonic"
  (cd "$dir" && tectonic --keep-logs --outdir "$out" "$base.tex" >>"$log" 2>&1); status=$?
elif command -v pdflatex >/dev/null 2>&1; then
  engine="pdflatex"
  (cd "$dir" && pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$out" "$base.tex" >>"$log" 2>&1
   if grep -q '\\bibdata\|\\citation' "$out/$base.aux" 2>/dev/null; then
     if command -v bibtex >/dev/null 2>&1; then (cd "$out" && BIBINPUTS="$dir:" bibtex "$base" >>"$log" 2>&1); fi
   fi
   pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$out" "$base.tex" >>"$log" 2>&1
   pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$out" "$base.tex" >>"$log" 2>&1); status=$?
else
  echo "NO COMPILER: install tectonic, latexmk or pdflatex to verify the build. Skipped (this is not a pass)."
  exit 2
fi

pdf="$out/$base.pdf"
# paths may contain spaces: read the logs through a function, never an unquoted variable
alllogs() { cat "$log"; [ -f "$out/$base.log" ] && cat "$out/$base.log"; true; }
count() { alllogs 2>/dev/null | grep -c -E "$1" || true; }
undef_refs=$(count "(LaTeX Warning: (Reference|Citation) .* undefined|There were undefined (references|citations)|undefined control sequence|Undefined control sequence)")
overfull=$(count "Overfull \\\\hbox")
missing=$(count "(File .* not found|not found\\.|No file .*\\.(bbl|aux))")

pages="?"
if [ -f "$pdf" ]; then
  if command -v pdfinfo >/dev/null 2>&1; then pages=$(pdfinfo "$pdf" 2>/dev/null | awk '/^Pages:/{print $2}');
  else pages=$(python3 -I - "$pdf" <<'PY'
import re,sys,zlib
d=open(sys.argv[1],'rb').read()
parts=[d]
for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream',d,re.S):
    try: parts.append(zlib.decompress(m.group(1)))
    except Exception: pass
allb=b'\n'.join(parts)
n=[int(x) for x in re.findall(rb'/Type\s*/Pages[^>]{0,200}?/Count\s+(\d+)',allb)]
if not n: n=[len(re.findall(rb'/Type\s*/Page\b(?!s)',allb))] if re.search(rb'/Type\s*/Page\b(?!s)',allb) else []
print(max(n) if n else '?')
PY
); fi
fi

echo "engine: $engine"
if [ -f "$pdf" ] && [ "$status" -eq 0 ]; then echo "build: OK ($pdf)"; else echo "build: FAILED (see $log)"; fi
echo "pages: $pages${limit:+ (limit $limit, counts everything including references)}"
echo "undefined references/citations/commands: $undef_refs"
echo "overfull boxes: $overfull"
echo "missing files: $missing"
rc=0
[ "$status" -ne 0 ] && rc=1
[ ! -f "$pdf" ] && rc=1
[ "$undef_refs" -gt 0 ] && rc=1
if [ -n "$limit" ] && [ "$pages" != "?" ] && [ "$pages" -gt "$limit" ]; then echo "FAIL over the page limit: $pages > $limit"; rc=1; fi
if [ "$status" -ne 0 ]; then echo "--- last log lines ---"; tail -n 15 "$log"; fi
[ "$rc" -eq 0 ] && echo "COMPILE: PASS" || echo "COMPILE: FAIL"
exit $rc
