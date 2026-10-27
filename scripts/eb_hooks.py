"""Shared helpers for the Employer Brand OS hooks. Standard library only."""
import json
import os
import sys
from pathlib import Path
from typing import Optional

AGENT_PREFIX = "eb-"


def read_event() -> dict:
    try:
        return json.load(sys.stdin)
    except (ValueError, OSError):
        return {}


def workspace_root(event: dict) -> Optional[Path]:
    """The Employer Brand OS workspace containing cwd, or None outside one."""
    start = Path(event.get("cwd") or os.getcwd()).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / "eb" / "status.md").is_file():
            return candidate
    return None
