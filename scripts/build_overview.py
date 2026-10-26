#!/usr/bin/env python3
"""Build the Phase 1 overview page (methodology/diagnosis.md §8a).

Usage: python3 build_overview.py <data.json> <out.html>

Checks the data against the template's needs, then embeds it as JSON in
templates/overview.html. All text is rendered as text by the page, never as
HTML. Standard library only.
"""
import html
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "overview.html"
UI_KEYS = [
    "lede", "scenariosLabel", "schemeLabel", "play", "showAll", "themeDark", "themeLight", "rules",
    "deckTitle", "deckNote", "flipHint", "flipLabel", "cardWith", "cardOwner", "cardWhen", "cardGoal",
    "cardNot", "cardRuleTitle", "cardRule", "functionTitle", "pressureTitle", "mapTitle", "legend",
    "whyHint", "priorityNote", "zone", "wave1", "priority", "readyTitle", "status",
]
KINDS = {"person", "coord", "agent", "store"}


def check(d: dict) -> list:
    problems = []
    for key in ("lang", "title", "ui", "nodes", "scenarios", "agents", "function", "processes", "readiness"):
        if key not in d:
            problems.append(f"missing top-level key: {key}")
    if problems:
        return problems
    problems += [f"missing ui.{k}" for k in UI_KEYS if k not in d["ui"]]
    nodes = d["nodes"]
    for nid, n in nodes.items():
        if n.get("kind") not in KINDS:
            problems.append(f"node {nid}: kind must be one of {sorted(KINDS)}")
        if not n.get("label"):
            problems.append(f"node {nid}: missing label")
    for s in d["scenarios"]:
        for st in s.get("steps", []):
            for edge in st.get("edges", []):
                for nid in edge:
                    if nid not in nodes:
                        problems.append(f"scenario '{s.get('title')}': unknown node {nid}")
    for a in d["agents"]:
        if a.get("node") and a["node"] not in nodes:
            problems.append(f"agent '{a.get('name')}': unknown node {a['node']}")
    for p in d["processes"]:
        if p.get("zone") not in {"A", "B", "C"}:
            problems.append(f"process '{p.get('name')}': zone must be A, B or C")
    for r in d["readiness"]:
        if r.get("status") not in {"ok", "todo", "rule"}:
            problems.append(f"readiness '{r.get('title')}': status must be ok, todo or rule")
    return problems


def build(data: dict) -> str:
    # Escape "<" so no string in the data can close the script element.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    page = TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("__LANG__", html.escape(data["lang"]), 1)
    page = page.replace("__TITLE__", html.escape(data["title"]), 1)
    return page.replace("__DATA__", payload, 1)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    problems = check(data)
    if problems:
        print("Data problems:")
        for p in problems:
            print(f"  - {p}")
        return 1
    Path(sys.argv[2]).write_text(build(data), encoding="utf-8")
    print(f"written {sys.argv[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
