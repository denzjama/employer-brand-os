#!/bin/sh
# Shared scaffold for the behavioural evals. Runs in the eval run's working folder.
#   setup.sh materials            fresh workspace with all demo materials in eb/inbox
#   setup.sh reviews-only         fresh workspace with only the review export (prompt injection)
#   setup.sh snapshot <stage>     a copy of demo/run/<stage>/workspace
#   setup.sh quality-gate         stage 3 with five facts confirmed and a story draft to check
#   setup.sh retro                stage 3 with four weeks of team logs (demo/retro/)
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
  quality-gate)
    # The assembled team, the current runtime files, five facts confirmed, a story draft with planted problems.
    cp -R "$ROOT/demo/run/stage-3-assembly/workspace/." .
    python3 "$ROOT/scripts/init_workspace.py" . --lang ru >/dev/null
    python3 "$ROOT/scripts/render_team.py" . --no-vendor >/dev/null
    python3 - <<'PY'
import re
from pathlib import Path
p = Path("eb/brand-core/facts.md")
t = p.read_text(encoding="utf-8")
for fid in ("F005", "F007", "F008", "F017", "F028"):
    t = re.sub(rf"^(\| {fid} \|.*?\| )TO CONFIRM \|  \|", r"\1CONFIRMED | Руководитель HR-бренда, 2026-11-01 |", t, flags=re.M)
p.write_text(t, encoding="utf-8")
PY
    mkdir -p eb/inbox/stories eb/work/employee-stories
    cp "$LIB/../quality-gate-traps/files/transcript.md" eb/inbox/stories/2026-10-30-kran.md
    cp "$LIB/../quality-gate-traps/files/draft.md" eb/work/employee-stories/2026-11-02-kran.md
    ;;
  retro)
    # The assembled team plus four weeks of fictional logs (demo/retro/README.md).
    cp -R "$ROOT/demo/run/stage-3-assembly/workspace/." .
    python3 "$ROOT/scripts/init_workspace.py" . --lang ru >/dev/null
    cp -R "$ROOT/demo/retro/overlay/." .
    ;;
  *)
    echo "unknown mode $1" >&2
    exit 2
    ;;
esac
cp "$ROOT/demo/interview.md" interview-answers.md
