#!/usr/bin/env python3
"""Record a human decision on an agent output (methodology/coordination.md §3).

Usage:
  python3 record_decision.py <workspace> --agent ID --output PATH
      --decision ACCEPTED|EDITED|REJECTED [--substantive yes|no]
      --reason TEXT --by ROLE [--operator ROLE]

Writes one file per decision in eb/log/decisions/. Standard library only.
"""
import argparse
import datetime
import sys
from pathlib import Path

DECISIONS = ("ACCEPTED", "EDITED", "REJECTED")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--agent", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--decision", required=True, choices=DECISIONS)
    ap.add_argument("--substantive", choices=("yes", "no"))
    ap.add_argument("--reason", required=True)
    ap.add_argument("--by", required=True, help="the owner's role")
    ap.add_argument("--operator", help="the operator's role, if an operator recorded it")
    a = ap.parse_args()

    # The roster id, not the runtime name: "eb-employee-stories" -> "employee-stories".
    if a.agent.startswith("eb-"):
        a.agent = a.agent[3:]
    if a.decision == "EDITED" and not a.substantive:
        print("--substantive is required for EDITED (methodology/autonomy.md §3)", file=sys.stderr)
        return 2
    if not a.reason.strip():
        print("--reason must not be empty", file=sys.stderr)
        return 2
    root = Path(a.workspace).expanduser().resolve()
    if not (root / "eb" / "status.md").is_file():
        print(f"{root} is not an Employer Brand OS workspace", file=sys.stderr)
        return 2

    now = datetime.datetime.now()
    folder = root / "eb" / "log" / "decisions"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{now:%Y-%m-%d-%H%M%S}-{a.agent}.md"
    n = 1
    while path.exists():
        n += 1
        path = folder / f"{now:%Y-%m-%d-%H%M%S}-{a.agent}-{n}.md"
    by = a.by + (f" (via operator {a.operator})" if a.operator else "")
    lines = [
        f"# Decision: {a.agent}",
        "",
        f"- Time: {now:%Y-%m-%d %H:%M:%S}",
        f"- Output: {a.output}",
        f"- Agent: {a.agent}",
        f"- Decision: {a.decision}",
    ]
    if a.decision == "EDITED":
        lines.append(f"- Substantive: {a.substantive}")
    lines += [f"- Decided by: {by}", "", "## Reason", "", a.reason.strip(), ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(path.relative_to(root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
