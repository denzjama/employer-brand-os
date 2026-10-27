#!/usr/bin/env python3
"""PreToolUse hook: keep every agent inside its own folder (methodology/assembly.md §3).

- Outside an Employer Brand OS workspace: does nothing.
- Main session (no agent_type): allowed; a person is present.
- Team agents (`eb-<id>`): may write only under eb/work/<id>/.
- Any other subagent: may not write into eb/brand-core/, eb/team/,
  eb/log/decisions/, .claude/ or vendor/.
Exit code 2 refuses the write and shows the reason to the agent.
"""
import sys
from pathlib import Path

from eb_hooks import AGENT_PREFIX, read_event, workspace_root

PROTECTED = ("eb/brand-core", "eb/team", "eb/log/decisions", ".claude", "vendor")


def refuse(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    event = read_event()
    agent = event.get("agent_type")
    root = workspace_root(event)
    if not agent or root is None:
        return
    target = (event.get("tool_input") or {}).get("file_path") or (event.get("tool_input") or {}).get("notebook_path")
    if not target:
        return
    path = Path(target)
    if not path.is_absolute():
        path = Path(event.get("cwd") or root) / path
    path = path.resolve()
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = None

    if agent.startswith(AGENT_PREFIX):
        own = f"eb/work/{agent[len(AGENT_PREFIX):]}"
        if rel is None or not (rel == own or rel.startswith(own + "/")):
            refuse(f"Employer Brand OS: agent {agent} may write only under {own}/. Return the content to the coordinator instead.")
        return

    if rel is not None and any(rel == p or rel.startswith(p + "/") for p in PROTECTED):
        refuse(f"Employer Brand OS: subagents may not write to {rel}. Only a person changes the brand core, the team and the decision log.")


if __name__ == "__main__":
    main()
