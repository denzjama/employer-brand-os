#!/bin/sh
# Connect this computer to the team's Employer Brand OS (methodology/assembly.md §5).
# Run once from the root of the shared workspace:  sh join_team.sh
# It registers the plugin vendored in vendor/eb-marketplace for this folder only
# (personal settings, never committed). Nothing is downloaded from the internet.
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if ! command -v claude >/dev/null 2>&1; then
  echo "Claude Code is not installed on this computer. Ask the team's operator for help." >&2
  exit 1
fi
if [ ! -f "vendor/eb-marketplace/.claude-plugin/marketplace.json" ]; then
  echo "vendor/eb-marketplace is missing: run this script from the root of the shared workspace." >&2
  exit 1
fi

# Another copy of the plugin enabled for this user (for example a developer copy)
# would run every hook twice. Switch it off for this folder only.
claude plugin list 2>/dev/null | grep -o 'employer-brand-os@[A-Za-z0-9_.-]*' | sort -u | while read -r other; do
  if [ "$other" != "employer-brand-os@eb-team" ]; then
    claude plugin disable "$other" --scope local >/dev/null 2>&1 && echo "Switched off $other in this folder."
  fi
done

claude plugin marketplace add "$ROOT/vendor/eb-marketplace" --scope local
claude plugin install employer-brand-os@eb-team --scope local

echo
echo "Done. Open Claude Code in this folder. Start with /eb-sync, then /weekly or your pipeline command."
