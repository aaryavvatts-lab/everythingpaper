#!/usr/bin/env bash
# install.sh - install everythingpaper as a Claude Code skill.
#
# Usage:
#   bash install.sh                 install to ~/.claude/skills/everythingpaper
#   bash install.sh --target DIR    install to DIR/everythingpaper
#   bash install.sh --dry-run       show what would be copied, change nothing
#   bash install.sh --companions    also print how to get the helper skills (does not install them)
#
# It copies this skill only. It never deletes anything and never overwrites a folder that
# is not a previous everythingpaper install (it will ask you to move it first).
set -eu

src="$(cd "$(dirname "$0")" && pwd)"
target="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
dry=0; comp=0
while [ $# -gt 0 ]; do
  case "$1" in
    --target) target="$2"; shift 2;;
    --dry-run) dry=1; shift;;
    --companions) comp=1; shift;;
    -h|--help) sed -n '2,12p' "$0"; exit 0;;
    *) echo "unknown option: $1"; exit 2;;
  esac
done

dest="$target/everythingpaper"
items="SKILL.md catalog.md README.md LICENSE references scripts evals"

if [ -e "$dest" ] && ! grep -q '^name: everythingpaper' "$dest/SKILL.md" 2>/dev/null; then
  echo "refusing to overwrite $dest: it exists and is not an everythingpaper install. Move it first."
  exit 1
fi

echo "from: $src"
echo "to:   $dest"
for i in $items; do [ -e "$src/$i" ] && echo "  copy $i"; done
if [ $dry -eq 1 ]; then echo "dry run: nothing changed"; exit 0; fi

mkdir -p "$dest"
for i in $items; do
  [ -e "$src/$i" ] || continue
  rm -rf "$dest/$i"   # only paths this installer owns inside the everythingpaper folder
  cp -R "$src/$i" "$dest/$i"
done
find "$dest/scripts" -type f \( -name '*.sh' -o -name '*.py' \) -exec chmod +x {} +
find "$dest" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true

echo
echo "installed. Start a new Claude Code session and type /everythingpaper"
echo
bash "$dest/scripts/check_skills.sh" --tools | tail -22

if [ $comp -eq 1 ]; then
  cat <<'EOF'

Helper skills (optional but recommended). everythingpaper works without them, using its own
rules in references/craft.md, and gets stronger with each one installed. The catalog lists
the source repo of every skill. Install the repos you trust, for example:

  npx skills add Imbad0202/academic-research-skills
  npx skills add Alexyskoutnev/research-skills
  npx skills add Ar9av/PaperOrchestra
  npx skills add boom5426/nature-paper-skills
  npx skills add Galaxy-Dawn/claude-scholar
  npx skills add lingzhi227/agent-research-skills
  npx skills add K-Dense-AI/scientific-agent-skills
  npx skills add franklee16/academic-research-skills

Read a repo's SKILL.md files before installing; skills run with your permissions.
Then run: bash ~/.claude/skills/everythingpaper/scripts/check_skills.sh --missing
EOF
fi
