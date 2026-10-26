#!/usr/bin/env bash
# run_tests.sh - regression tests for the everythingpaper scripts.
# Usage: bash tests/run_tests.sh
# Runs each script on tests/sample/ fixtures (a paper with seeded defects and a clean twin) and
# checks it catches what it should and stays quiet where it should. No network is used.
set -u
root="$(cd "$(dirname "$0")/.." && pwd)"
S="$root/scripts"; F="$root/tests/sample"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
pass=0; fail=0
ok()   { pass=$((pass+1)); echo "ok   $1"; }
bad()  { fail=$((fail+1)); echo "FAIL $1"; }
has()  { printf '%s' "$2" | grep -q -- "$3" && ok "$1" || bad "$1 (missing: $3)"; }
hasno(){ printf '%s' "$2" | grep -q -- "$3" && bad "$1 (unexpected: $3)" || ok "$1"; }
py() { python3 -I "$@"; }

# paper_lint
out=$(py "$S/paper_lint.py" "$F/paper_defects.tex" --bib "$F/refs.bib" --no-dashes); rc=$?
[ $rc -eq 1 ] && ok "paper_lint exits 1 on defects" || bad "paper_lint exit code ($rc)"
for k in todo-evidence undefined-ref missing-bib "banned dash" abstract-number repeated-word significant-no-test undefined-acronym ai-tell mixed-spelling unused-label; do
  has "paper_lint finds $k" "$out" "$k"
done
hasno "paper_lint does not double count TODO-EVIDENCE" "$out" "FAIL todo  "
out=$(py "$S/paper_lint.py" "$F/paper_clean.tex" --bib "$F/refs.bib" --no-dashes); rc=$?
[ $rc -eq 0 ] && ok "paper_lint exits 0 on clean paper" || bad "paper_lint clean exit ($rc)"
hasno "paper_lint clean has no FAIL lines" "$out" "^FAIL"

# citation_check (offline)
out=$(py "$S/citation_check.py" "$F/refs.bib" --tex "$F/paper_defects.tex"); rc=$?
[ $rc -eq 1 ] && ok "citation_check exits 1 on bad bib" || bad "citation_check exit ($rc)"
has "citation_check finds cited-but-missing key" "$out" "missing2020"
has "citation_check finds malformed DOI" "$out" "malformed DOI"
has "citation_check finds duplicate title" "$out" "same title"

# outline_lint
out=$(py "$S/outline_lint.py" "$F/outline_bad.md"); rc=$?
[ $rc -eq 1 ] && ok "outline_lint exits 1 on bad outline" || bad "outline_lint bad exit ($rc)"
has "outline_lint: undefined claim" "$out" "undefined claim C3"
has "outline_lint: claim without evidence" "$out" "claim C2 has no evidence"
has "outline_lint: word budget" "$out" "word budget"
out=$(py "$S/outline_lint.py" "$F/outline_good.md"); rc=$?
[ $rc -eq 0 ] && ok "outline_lint exits 0 on good outline" || bad "outline_lint good exit ($rc)"

# ledger_check
out=$(py "$S/ledger_check.py" "$F/ledger_mixed.md"); rc=$?
[ $rc -eq 1 ] && ok "ledger_check exits 1 while OPEN or PASS-without-evidence" || bad "ledger exit ($rc)"
has "ledger_check flags BLOCKED" "$out" "needs the user"
cat > "$tmp/ledger_ok.md" <<'EOF'
| ID | Kind | Requirement | Status | Evidence |
|----|------|-------------|--------|----------|
| R1 | Asked | Find errors | PASS | issues.md |
| R2 | Implied | No fabricated numbers | PASS | EVIDENCE.md |
| R3 | Asked | Needs data | BLOCKED | user |
EOF
py "$S/ledger_check.py" "$tmp/ledger_ok.md" >/dev/null; [ $? -eq 0 ] && ok "ledger_check exits 0 when all PASS or BLOCKED" || bad "ledger_check all-pass exit"

# line_review + issue_register
py "$S/line_review.py" "$F/paper_defects.tex" --out "$tmp/review" --chunk 6 >/dev/null
nch=$(ls "$tmp/review"/chunk_*.md | wc -l | tr -d ' ')
[ "$nch" -eq 2 ] && ok "line_review makes 2 chunks of 6 sentences" || bad "line_review chunk count ($nch)"
has "line_review numbers sentences" "$(cat "$tmp/review/chunk_01.md")" "L0001"
has "line_review reviews the title" "$(cat "$tmp/review/chunk_01.md")" "Section: Title"
hasno "line_review keeps bibliography commands out" "$(cat "$tmp/review"/chunk_*.md)" "plain"
out=$(py "$S/issue_register.py" "$tmp/review/issues.md" --gate); rc=$?
[ $rc -eq 1 ] && ok "gate fails while chunks are unread" || bad "gate unread exit ($rc)"
has "gate names unread chunks" "$out" "chunks not reviewed"
hasno "template example is not counted as a real issue" "$out" "open FATAL/MAJOR"
sed -i.bak 's/: pending/: reviewed/' "$tmp/review/issues.md"
out=$(py "$S/issue_register.py" "$tmp/review/issues.md" --gate); rc=$?
[ $rc -eq 0 ] && ok "gate passes when all chunks read and no open MAJOR" || bad "gate pass exit ($rc)"
python3 -I - "$tmp/review/issues.md" <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
t=t.replace("## Coverage","### I-001 | MAJOR | open | L0003 | claim-support\nQuote: \"x\"\nProblem: y\nFix: z\n\n## Coverage")
open(p,"w").write(t)
PY
py "$S/issue_register.py" "$tmp/review/issues.md" --gate >/dev/null; [ $? -eq 1 ] && ok "gate fails on open MAJOR" || bad "gate open MAJOR"
sed 's/the the/the/' "$F/paper_defects.tex" > "$tmp/p2.tex"
out=$(py "$S/line_review.py" "$tmp/p2.tex" --out "$tmp/review" --chunk 6)
has "re-run flags the changed chunk" "$out" "chunk_01"
has "re-run keeps the open issue" "$(cat "$tmp/review/issues.md")" "I-001 | MAJOR | open"

# compile_check (skips cleanly with no compiler)
out=$(bash "$S/compile_check.sh" "$F/paper_clean.tex" --out "$tmp/build" --page-limit 4); rc=$?
if [ $rc -eq 2 ]; then ok "compile_check reports no compiler (rc 2)"; else
  [ $rc -eq 0 ] && ok "compile_check passes the clean paper" || bad "compile_check clean exit ($rc)"
  has "compile_check counts pages" "$out" "pages: 1"
  bash "$S/compile_check.sh" "$F/paper_defects.tex" --out "$tmp/build2" >/dev/null; [ $? -eq 1 ] && ok "compile_check fails undefined refs" || bad "compile_check defects exit"
fi

# check_skills
bash "$S/check_skills.sh" --tools >/dev/null && ok "check_skills runs" || bad "check_skills failed"

echo; echo "$pass passed, $fail failed"
[ $fail -eq 0 ]
