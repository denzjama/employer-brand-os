#!/usr/bin/env python3
"""SubagentStop hook: record every team-agent run (methodology/coordination.md §4).

Writes eb/log/runs/<date>-<time>-<agent>.md for agents named `eb-<id>`.
Does nothing outside an Employer Brand OS workspace or for other subagents.
"""
import datetime

from eb_hooks import AGENT_PREFIX, read_event, workspace_root

MAX_MESSAGE = 4000


def main() -> None:
    event = read_event()
    agent = event.get("agent_type") or ""
    root = workspace_root(event)
    if root is None or not agent.startswith(AGENT_PREFIX):
        return
    now = datetime.datetime.now()
    agent_id = agent[len(AGENT_PREFIX):]
    runs = root / "eb" / "log" / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    path = runs / f"{now:%Y-%m-%d-%H%M%S}-{agent_id}.md"
    message = (event.get("last_assistant_message") or "").strip()
    if len(message) > MAX_MESSAGE:
        message = message[:MAX_MESSAGE] + "\n\n[truncated]"
    path.write_text(
        f"# Run: {agent_id}\n\n"
        f"- Time: {now:%Y-%m-%d %H:%M:%S}\n"
        f"- Agent: {agent_id}\n"
        f"- Session: {event.get('session_id', '')}\n\n"
        f"## Final message\n\n{message}\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
