#!/bin/sh
# Shared scaffold for the behavioural evals. Runs in the eval run's working folder.
#   setup.sh materials            fresh workspace with all demo materials in eb/inbox
#   setup.sh reviews-only         fresh workspace with only the review export (prompt injection)
#   setup.sh snapshot <stage>     a copy of demo/run/<stage>/workspace
# The plugin root is found from this script's own path.
set -e
LIB="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$LIB/../.." && pwd)"
case "$1" in
  materials)
    python3 "$ROOT/scripts/init_workspace.py" . --lang ru >/dev/null
    cp "$ROOT"/demo/materials/* eb/inbox/
    ;;
  reviews-only)
    python3 "$ROOT/scripts/init_workspace.py" . --lang ru >/dev/null
    cp "$ROOT/demo/materials/Отзывы_hh_выгрузка.md" eb/inbox/
    ;;
  snapshot)
    cp -R "$ROOT/demo/run/$2/workspace/." .
    # git keeps no empty folders: restore the layout (init never overwrites a file)
    python3 "$ROOT/scripts/init_workspace.py" . --lang ru >/dev/null
    ;;
  *)
    echo "unknown mode $1" >&2
    exit 2
    ;;
esac
cp "$ROOT/demo/interview.md" interview-answers.md
