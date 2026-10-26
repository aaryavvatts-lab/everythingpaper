#!/usr/bin/env bash
# check_skills.sh - which catalog skills are installed, and which tools exist.
#
# Usage: check_skills.sh [--tools] [--missing] [--install-hints]
#   --tools          also report programs (python3, LaTeX engine, bibtex, pandoc, git, ...)
#   --missing        print only the missing skills
#   --install-hints  print the install command for the source repos of missing skills
# Reads catalog.md next to this script's folder. Skills live in ~/.claude/skills (override
# with CLAUDE_SKILLS_DIR). Plugin skills (ecc:, anthropic-skills:, Src "plugin") cannot be
# checked from the folder; the Skill tool's list is the authority for those.
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
cat_file="$here/catalog.md"
skills_dir="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
tools=0; only_missing=0; hints=0
for a in "$@"; do case "$a" in --tools) tools=1;; --missing) only_missing=1;; --install-hints) hints=1;; esac; done
[ -f "$cat_file" ] || { echo "catalog.md not found at $cat_file"; exit 2; }

ok=0; miss=0; plug=0; missing_list=""
while IFS=$'\t' read -r src names; do
  for n in $names; do
    if [ "$src" = "plugin" ] || [[ "$n" == *:* ]]; then plug=$((plug+1)); [ $only_missing -eq 0 ] && echo "plugin   $n"; continue; fi
    if [ -f "$skills_dir/$n/SKILL.md" ]; then ok=$((ok+1)); [ $only_missing -eq 0 ] && echo "ok       $n"
    else miss=$((miss+1)); missing_list="$missing_list $n"; echo "MISSING  $n"; fi
  done
done < <(awk -F'|' '/^\| `/{gsub(/ /,"",$3); n=$2; out=""; while (match(n,/`[^`]+`/)) { out=out" "substr(n,RSTART+1,RLENGTH-2); n=substr(n,RSTART+RLENGTH) } print $3 "\t" out }' "$cat_file")

echo
echo "skills: $ok installed, $miss missing, $plug plugin/built-in (not checked)"
if [ $miss -gt 0 ]; then
  echo "A missing skill is not a blocker: use the next best skill in its group or references/craft.md."
  [ $hints -eq 1 ] && echo "Install hints: see the source repo codes in catalog.md; for example: npx skills add <owner>/<repo>"
fi

if [ $tools -eq 1 ]; then
  echo
  echo "tools:"
  for t in python3 tectonic latexmk pdflatex xelatex bibtex biber pandoc pdfinfo pdftotext git gh node curl; do
    if p=$(command -v "$t" 2>/dev/null); then echo "ok       $t ($p)"; else echo "absent   $t"; fi
  done
  if ! command -v tectonic >/dev/null 2>&1 && ! command -v latexmk >/dev/null 2>&1 && ! command -v pdflatex >/dev/null 2>&1; then
    echo "note: no LaTeX engine found; compile_check.sh cannot verify builds. Say so in the report; do not claim a clean build."
  fi
fi
exit 0
