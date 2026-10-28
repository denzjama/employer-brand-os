#!/usr/bin/env python3
"""Iteration statistics and signals for the retro (methodology/retro.md §2–§3).

Usage: python3 retro_stats.py <workspace> [--until YYYY-MM-DD] [--days 14] [--print]

Reads eb/log/runs/, eb/log/decisions/, eb/work/quality-gate/, eb/log/adhoc.md and
the canonical agents in eb/team/agents/, and writes eb/retro/<until>-stats.md:
per-agent counts for the iteration, gate verdicts and issue codes, and the
signals that can be counted (S2–S9). Signals that need reading the reasons
(S1, S10) are listed as candidates with the reasons verbatim. Deterministic:
the same records give the same file. --print writes to stdout instead.
Standard library only.
"""
import argparse
import datetime
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_team  # noqa: E402

CODES = {"FACT", "KIND", "ANCHOR", "LINK", "QUOTE", "PERSONAL", "RED LINE", "INSTRUCTION",
         "GENERIC", "VOICE", "CRITERIA"}
MISSABLE = {"FACT", "KIND", "ANCHOR", "LINK", "QUOTE", "PERSONAL", "RED LINE", "INSTRUCTION"}
NO_REASON = "(no reason given)"
STREAK_FOR_L2 = 10
MANUAL_RUNS_FOR_L1 = 4
REPEAT = 3


def field(text: str, name: str) -> str:
    m = re.search(rf"^-?\s*{re.escape(name)}:\s*(.+?)\s*$", text, re.M)
    return m.group(1) if m else ""


def section(text: str, title: str) -> str:
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def day(value: str):
    m = re.match(r"(\d{4}-\d{2}-\d{2})", value or "")
    return datetime.date.fromisoformat(m.group(1)) if m else None


def read_decisions(ws: Path) -> list:
    out = []
    for p in sorted((ws / "eb/log/decisions").glob("*.md")):
        t = p.read_text(encoding="utf-8")
        d = day(field(t, "Time")) or day(p.name)
        if not d:
            continue
        out.append({
            "file": p.relative_to(ws).as_posix(), "date": d, "time": field(t, "Time") or p.name,
            "agent": field(t, "Agent").removeprefix("eb-"),
            "decision": field(t, "Decision"), "substantive": field(t, "Substantive"),
            "check": field(t, "Check"), "reason": section(t, "Reason"), "facts": section(t, "Facts added"),
        })
    return sorted(out, key=lambda d: (d["time"], d["file"]))


def read_runs(ws: Path) -> list:
    out = []
    for p in sorted((ws / "eb/log/runs").glob("*.md")):
        t = p.read_text(encoding="utf-8")
        d = day(field(t, "Time")) or day(p.name)
        agent = field(t, "Agent") or field(t, "Agent type")
        if d and agent:
            out.append({"file": p.relative_to(ws).as_posix(), "date": d, "agent": agent.removeprefix("eb-")})
    return out


def read_checks(ws: Path, ids: set) -> list:
    out = []
    for p in sorted((ws / "eb/work/quality-gate").glob("*.md")):
        t = p.read_text(encoding="utf-8")
        # Tolerates checks written before the fixed header: "- **Вердикт: `PASS`**".
        m = re.search(r"(?:Verdict|Вердикт)[\s:*`]*(PASS WITH FIXES|BLOCKED|PASS)", t)
        verdict = m.group(1) if m else ""
        attempt = re.search(r"(?:Attempt|Попытка)[\s:*`]*(\d+)", t)
        codes = []
        for row in re.findall(r"^\|([^\n]+)\|\s*$", t, re.M):
            cells = [c.strip().strip("`") for c in row.split("|")]
            for c in cells[:3]:
                if c in CODES or re.fullmatch(r"RF\d\d", c):
                    codes.append(c)
                    break
        agent = field(t, "Agent").removeprefix("eb-")
        if not agent:
            # Checks written before the header existed: <date>-<agent>-<draft>.md
            rest = p.stem[11:]
            agent = max((i for i in ids if rest == i or rest.startswith(i + "-")), key=len, default="")
        out.append({
            "file": p.relative_to(ws).as_posix(), "date": day(p.name), "agent": agent,
            "draft": field(t, "Draft"), "verdict": verdict,
            "attempt": int(attempt.group(1)) if attempt else 1, "codes": codes,
        })
    return out


def read_adhoc(ws: Path) -> list:
    path = ws / "eb/log/adhoc.md"
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and day(cells[0]):
            rows.append({"date": day(cells[0]), "request": cells[1], "process": cells[2] or "none"})
    return rows


def read_agents(ws: Path) -> dict:
    agents = {}
    for p in sorted((ws / "eb/team/agents").glob("*.md")):
        try:
            a = render_team.parse_agent(p)
        except render_team.InputError:
            continue
        agents[a["id"]] = a
    return agents


def streak(decisions: list) -> int:
    n = 0
    for d in reversed(decisions):
        if d["decision"] == "ACCEPTED" or (d["decision"] == "EDITED" and d["substantive"] == "no"):
            n += 1
        else:
            break
    return n


def collect(ws: Path, until: datetime.date, days: int) -> dict:
    since = until - datetime.timedelta(days=days - 1)
    inside = lambda d: d is not None and since <= d <= until  # noqa: E731
    agents = read_agents(ws)
    decisions, runs, adhoc = read_decisions(ws), read_runs(ws), read_adhoc(ws)
    checks = read_checks(ws, set(agents) | {d["agent"] for d in decisions})
    ids = sorted(set(agents) | {d["agent"] for d in decisions} | {r["agent"] for r in runs} | {c["agent"] for c in checks if c["agent"]})
    check_by_path = {c["file"]: c for c in checks}
    rows, signals = [], []

    notes = []

    def signal(code, target, text, evidence):
        signals.append({"signal": code, "target": target, "text": text.rstrip("."), "evidence": sorted(evidence)})

    for aid in ids:
        a = agents.get(aid, {})
        dec_all = [d for d in decisions if d["agent"] == aid]
        dec = [d for d in dec_all if inside(d["date"])]
        run_all = [r for r in runs if r["agent"] == aid]
        run = [r for r in run_all if inside(r["date"])]
        chk = [c for c in checks if c["agent"] == aid and inside(c["date"])]
        codes = Counter(code for c in chk for code in c["codes"])
        kinds = Counter(d["decision"] for d in dec)
        substantive = [d for d in dec if d["decision"] == "EDITED" and d["substantive"] == "yes"]
        rejected = [d for d in dec if d["decision"] == "REJECTED"]
        no_reason = [d for d in dec if d["reason"] == NO_REASON]
        facts = [d for d in dec if d["facts"]]
        first = [c for c in chk if c["attempt"] == 1]
        first_pass = [c for c in first if c["verdict"] in ("PASS", "PASS WITH FIXES")]
        not_passed = [c for c in chk if c["attempt"] >= 3 and c["verdict"] == "BLOCKED"]
        last_run = max((r["date"] for r in run_all), default=None)
        row = {
            "agent": aid, "name": a.get("name", aid), "autonomy": a.get("autonomy", "?"),
            "external": a.get("external_facing", "?"), "runs": len(run), "last_run": last_run,
            "accepted": kinds["ACCEPTED"], "edited": kinds["EDITED"], "substantive": len(substantive),
            "rejected": len(rejected), "no_reason": len(no_reason), "facts_added": len(facts),
            "streak": streak(dec_all), "checks": len(chk), "first": len(first), "first_pass": len(first_pass),
            "not_passed": len(not_passed), "codes": codes,
        }
        rows.append(row)

        hard = substantive + rejected
        if len(hard) >= REPEAT:
            signal("S1", aid, f"{len(hard)} substantive edits or rejections: read the reasons for a common cause",
                   [d["file"] for d in hard])
        for d in facts:
            signal("S2", "brand-core", f"facts added by the owner of {aid}: {d['facts']}", [d["file"]])
        if row["external"] == "true" and row["streak"] >= STREAK_FOR_L2:
            notes.append(f"`{aid}`: {row['streak']} outputs in a row without a substantive edit, but it is external-facing "
                         "and capped at L1: no autonomy proposal (autonomy.md §2)")
        if row["autonomy"] == "L1" and row["external"] == "false" and row["streak"] >= STREAK_FOR_L2:
            signal("S4", aid, f"{row['streak']} outputs in a row without a substantive edit: L1 to L2 may be proposed",
                   [d["file"] for d in dec_all[-row["streak"]:]])
        if row["autonomy"] == "L0":
            recent = [r for r in run_all if r["date"] and r["date"] > until - datetime.timedelta(days=2 * days)]
            if len(recent) >= MANUAL_RUNS_FOR_L1:
                signal("S4", aid, f"{len(recent)} runs in two iterations: L0 to L1 may be proposed", [r["file"] for r in recent])
        if len(rejected) >= 2:
            signal("S5", aid, f"{len(rejected)} rejections in the iteration: lowering the level may be proposed",
                   [d["file"] for d in rejected])
        two_iterations_ago = until - datetime.timedelta(days=2 * days - 1)
        assembled = day(a.get("confirmed_on", ""))
        if (aid in agents and assembled and assembled < two_iterations_ago
                and (last_run is None or last_run < two_iterations_ago)):
            signal("S6", aid, "no run in two iterations: ask the owner why", [])
        for code, n in sorted(codes.items()):
            if n >= REPEAT:
                signal("S7", aid, f"issue {code} found {n} times", [c["file"] for c in chk if code in c["codes"]])
        if not_passed:
            signal("S7", aid, f"{len(not_passed)} draft(s) not passed after three attempts", [c["file"] for c in not_passed])
        for d in hard:
            c = check_by_path.get(d["check"])
            if c and c["verdict"] in ("PASS", "PASS WITH FIXES"):
                signal("S8", "quality-gate", f"{aid}: draft passed the gate ({c['verdict']}) but was "
                       f"{'rejected' if d['decision'] == 'REJECTED' else 'substantively edited'}; reason: {d['reason']}",
                       [d["file"], c["file"]])
        for d in no_reason:
            signal("S9", aid, "rejected or edited without a reason: ask the owner", [d["file"]])

    by_process = defaultdict(list)
    for r in adhoc:
        by_process[r["process"]].append(r)
    for process, items in sorted(by_process.items()):
        if len(items) >= REPEAT:
            signal("S3", process, f"{len(items)} one-off requests resembling {process}", [])
    adhoc_in = [r for r in adhoc if inside(r["date"])]
    return {"since": since, "until": until, "rows": rows, "signals": signals, "notes": notes,
            "adhoc": len(adhoc_in), "adhoc_total": len(adhoc),
            "decisions": len([d for d in decisions if inside(d["date"])])}


def render(s: dict) -> str:
    out = [
        f"# Retro statistics {s['since']} – {s['until']}",
        "",
        "Generated by scripts/retro_stats.py from eb/log/ and eb/work/quality-gate/. Counts only; reasons are read by the retro.",
        "",
        "## Agents",
        "",
        "| Agent | Level | External | Runs | Last run | Accepted | Edited (substantive) | Rejected | No reason | Facts added | In a row without substantive edit | Gate checks | First-attempt pass | Not passed | Issue codes |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in s["rows"]:
        codes = ", ".join(f"{c} {n}" for c, n in sorted(r["codes"].items())) or "—"
        first = f"{r['first_pass']} of {r['first']}" if r["first"] else "—"
        out.append(
            f"| {r['agent']} | {r['autonomy']} | {'yes' if r['external'] == 'true' else 'no' if r['external'] == 'false' else '?'} "
            f"| {r['runs']} | {r['last_run'] or 'never'} | {r['accepted']} | {r['edited']} ({r['substantive']}) | {r['rejected']} "
            f"| {r['no_reason']} | {r['facts_added']} | {r['streak']} | {r['checks']} | {first} | {r['not_passed']} | {codes} |")
    out += ["", f"Decisions in the iteration: {s['decisions']}. One-off requests: {s['adhoc']} in the iteration, {s['adhoc_total']} in total.", ""]
    if s["decisions"] < 5:
        out += ["Few decisions in this iteration: the evidence is thin, and silence is not acceptance.", ""]
    out += ["## Signals", ""]
    if not s["signals"]:
        out.append("None.")
    for g in s["signals"]:
        ev = "; ".join(g["evidence"]) if g["evidence"] else "—"
        out.append(f"- **{g['signal']}** `{g['target']}`: {g['text']}. Evidence: {ev}")
    if s["notes"]:
        out += ["", "## Not a signal", ""] + [f"- {n}" for n in s["notes"]]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--until", help="last day of the iteration, YYYY-MM-DD (default: today)")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--print", action="store_true", help="print instead of writing eb/retro/<until>-stats.md")
    a = ap.parse_args()
    ws = Path(a.workspace).expanduser().resolve()
    if not (ws / "eb" / "status.md").is_file():
        print(f"{ws} is not an Employer Brand OS workspace", file=sys.stderr)
        return 2
    until = datetime.date.fromisoformat(a.until) if a.until else datetime.date.today()
    text = render(collect(ws, until, a.days))
    if a.print:
        print(text, end="")
        return 0
    out = ws / "eb" / "retro" / f"{until}-stats.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(out.relative_to(ws))
    return 0


if __name__ == "__main__":
    sys.exit(main())
