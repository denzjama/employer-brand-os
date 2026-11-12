#!/usr/bin/env python3
"""Build the team map and the morning status of an assembled team (methodology/assembly.md §10a).

Usage: python3 build_team_map.py <workspace> [--date YYYY-MM-DD] [--days 14] [--out PATH]

Reads eb/diagnosis/team-roster.json, the canonical agents in eb/team/agents/,
the brand core, the material inventory and the logs (through retro_stats), and
writes eb/team/team-map.html: the sources, the brand core and the log, the
coordinator, the agents grouped by the domain of their library process, the
pipelines, where people decide and what stops a pipeline, and the status for
the date: counts for the last --days days, what waits for a person, what
happened that day. The page shows counts and names of agents and roles only:
no text from decisions, materials or facts. Deterministic for a given date.
Standard library only.
"""
import argparse
import datetime
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_team  # noqa: E402
import retro_stats  # noqa: E402

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = PLUGIN_ROOT / "templates" / "team-map.html"
PROCESSES = PLUGIN_ROOT / "library" / "processes"

GROUPS = [
    ("research", ("research", "strategy")),
    ("reputation", ("reputation",)),
    ("content", ("content", "social", "campaigns")),
    ("projects", ("creative", "operations")),
    ("analytics", ("analytics",)),
    ("quality", ("quality", "adoption")),
    ("other", ()),
]
NO_DRAFTS = {"quality-gate", "adoption-coach"}
STATUSES = ["CONFIRMED", "TO CONFIRM", "EVIDENCE NEEDED", "OUTDATED"]

UI = {
    "ru": {
        "kicker": "Employer Brand OS · команда агентов", "title": "Команда агентов",
        "lede": "Кто работает, с какими знаниями, через какие конвейеры и где решают люди. Рядом статус: что ждёт решения сегодня.",
        "stamp": "Статус на {date} · журналы за {since} – {until}",
        "tiles": ["Агенты в работе", "Владельцы", "Решения людей", "Опубликовали агенты"],
        "tileNotes": ["ждут следующих волн: {n}", "у каждого агента свой", "за период, с причиной", "публикуют только люди"],
        "people": "{n} чел.",
        "sources": "Материалы функции · {n} в eb/inbox", "more": "ещё {n}",
        "lead": "Руководитель · правила один раз",
        "leadItems": ["интервью по блокам", "подтверждает факты по одному", "красных линий: {n}", "утверждает состав команды"],
        "core": "Бренд-ядро · файлов: {n}", "coreNote": "пишет только человек, агентам запись закрыта",
        "facts": "фактов: {n}",
        "log": "Журнал · eb/log",
        "logItems": ["запусков агентов: {n}", "решений людей с причиной: {n}", "проверок контроля качества: {n}", "пишется сам, читает ретро"],
        "coord": "Координатор", "coordTitle": "Основная сессия в общей папке",
        "coordNote": "Разбирает задачу, собирает конвейер, чужой шаг сам не делает",
        "coordPill": "конвейеров: {n} · 3 попытки на контроль",
        "groups": {"research": "Исследования и стратегия", "reputation": "Отзывы и репутация", "content": "Контент и каналы",
                   "projects": "Проекты и подрядчики", "analytics": "Аналитика и отчёты", "quality": "Качество и обучение",
                   "other": "Другие процессы"},
        "waves": {"WAVE 1": "первая волна", "WAVE 2": "вторая волна", "DATA FIRST": "сначала данные"},
        "groupCount": "в работе {a}", "groupWait": "ждут {w}",
        "external": "наружу", "operator": "оператор {name}",
        "notPassed": "не прошли контроль за три попытки: {n}",
        "neverRun": "ещё не запускался", "idle": "не запускался {n} дн.", "runs": "запусков за период: {n}",
        "pipelines": "Конвейеры", "pipeWait": "ждёт агентов: {names}",
        "nodes": {"owner": "владелец", "lead": "руководитель", "brand-core": "бренд-ядро", "log": "журнал"},
        "decideTitle": "Где решают люди",
        "decide": [["Руководитель", "подтверждает факты, утверждает команду и предложения ретро"],
                   ["Владельцы", "принимают, правят или отклоняют черновик и пишут причину"],
                   ["Люди", "публикуют и отвечают на площадках"]],
        "stopsTitle": "Что останавливает конвейер",
        "stops": [["Факт не подтверждён", "в карантин, вопрос руководителю"], ["Красная линия", "черновик остановлен"],
                  ["Цитата не дословная", "назад агенту"], ["Спрятанная инструкция", "показать, не выполнять"],
                  ["Персональные данные", "убрать до черновика"], ["Три попытки без прохода", "владельцу с пометкой"]],
        "statusCmd": "статус", "statusRows": ["запусков агентов", "решений людей", "принято без правок по существу",
                                              "правки по существу · отказы", "контроль с первой попытки",
                                              "частое замечание контроля", "опубликовали агенты"],
        "of": "{a} из {b}", "none": "—",
        "inbox": "Ждёт вас", "inboxEmpty": "Ничего не ждёт решения.",
        "items": {
            "draft": ["{agent}: черновики ждут решения", "у владельца: {n}, самый старый от {date}"],
            "S1": ["{agent}: повторяются правки", "правок по существу или отказов: {n}. Найти общую причину на ретро"],
            "S2": ["Новые факты от владельцев", "записаны в решениях: {n}. Подтвердить или нет"],
            "S3": ["Повторяются разовые запросы", "похожих на процесс «{agent}»: {n}. Ритуал или задача агенту"],
            "S4": ["{agent}: можно поднять уровень", "черновики принимают без правок: решить на ретро"],
            "S5": ["{agent}: много отказов", "за период: {n}. Решить на ретро, не снизить ли уровень"],
            "S6": ["{agent}: не запускался", "две итерации без запуска: спросить владельца"],
            "S7code": ["{agent}: замечание «{code}» ({n})", "разобрать на ретро"],
            "S7fail": ["{agent}: черновики не прошли контроль ({n})", "за три попытки, у владельца с пометкой"],
            "S8": ["Контроль пропустил ошибку", "владелец нашёл то, что контроль пропустил ({agent}): поправить контроль"],
            "S9": ["{agent}: решение без причины", "спросить владельца, выводов не делать"],
            "facts": ["Факты ждут подтверждения", "в реестре со статусом «уточнить»: {n}"],
        },
        "today": "Сегодня", "todayEmpty": "Сегодня запусков и решений нет.",
        "run": "{agent}: запуск", "decision": "{agent}: {decision}",
        "decisions": {"ACCEPTED": "принято", "EDITED": "принято с правками", "REJECTED": "отклонено"},
        "neverTitle": "Чего агенты не делают",
        "never": ["не публикуют и не отвечают на площадках", "не пишут в бренд-ядро",
                  "не поднимают себе уровень самостоятельности", "не оценивают людей по данным использования"],
        "foot": "Страница собрана скриптом build_team_map.py из папки команды. Обновляется при сборке команды и перед планёркой.",
        "themeDark": "Тёмная тема", "themeLight": "Светлая тема",
    },
    "en": {
        "kicker": "Employer Brand OS · agent team", "title": "Agent team",
        "lede": "Who works, with what knowledge, through which pipelines, and where people decide. Next to it, the status: what waits for a decision today.",
        "stamp": "Status on {date} · logs for {since} – {until}",
        "tiles": ["Agents at work", "Owners", "People's decisions", "Published by agents"],
        "tileNotes": ["{n} more wait for later waves", "every agent has one", "in the period, with a reason", "only people publish"],
        "people": "{n} people",
        "sources": "Function materials · {n} in eb/inbox", "more": "{n} more",
        "lead": "EB lead · rules once",
        "leadItems": ["interview by blocks", "confirms facts one by one", "{n} red lines", "approves the team"],
        "core": "Brand core · {n} files", "coreNote": "only a person writes here; agents cannot",
        "facts": "{n} facts",
        "log": "Log · eb/log",
        "logItems": ["{n} agent runs", "{n} decisions with a reason", "{n} quality-gate checks", "written automatically, read by the retro"],
        "coord": "Coordinator", "coordTitle": "The main session in the shared folder",
        "coordNote": "Breaks down the task, runs the pipeline, never does another agent's step",
        "coordPill": "{n} pipelines · 3 attempts at the gate",
        "groups": {"research": "Research and strategy", "reputation": "Reviews and reputation", "content": "Content and channels",
                   "projects": "Projects and agencies", "analytics": "Analytics and reports", "quality": "Quality and learning",
                   "other": "Other processes"},
        "waves": {"WAVE 1": "first wave", "WAVE 2": "second wave", "DATA FIRST": "data first"},
        "groupCount": "{a} at work", "groupWait": "{w} waiting",
        "external": "external", "operator": "operator {name}",
        "notPassed": "{n} drafts did not pass the gate in three attempts",
        "neverRun": "not run yet", "idle": "no run for {n} days", "runs": "runs in the period: {n}",
        "pipelines": "Pipelines", "pipeWait": "waits for: {names}",
        "nodes": {"owner": "owner", "lead": "EB lead", "brand-core": "brand core", "log": "log"},
        "decideTitle": "Where people decide",
        "decide": [["EB lead", "confirms facts, approves the team and retro proposals"],
                   ["Owners", "accept, edit or reject a draft and give the reason"],
                   ["People", "publish and reply on platforms"]],
        "stopsTitle": "What stops a pipeline",
        "stops": [["Unconfirmed fact", "quarantined, question to the EB lead"], ["Red line", "draft stopped"],
                  ["Quote not verbatim", "back to the agent"], ["Hidden instruction", "reported, not followed"],
                  ["Personal data", "removed before the draft"], ["Three failed attempts", "to the owner, marked"]],
        "statusCmd": "status", "statusRows": ["agent runs", "people's decisions", "accepted without substantive edits",
                                              "substantive edits · rejections", "gate pass at first attempt",
                                              "most frequent gate issue", "published by agents"],
        "of": "{a} of {b}", "none": "—",
        "inbox": "Waiting for you", "inboxEmpty": "Nothing waits for a decision.",
        "items": {
            "draft": ["{agent}: draft waits for a decision", "{n} with the owner, the oldest from {date}"],
            "S1": ["{agent}: repeated edits", "{n} substantive edits or rejections: find the common cause at the retro"],
            "S2": ["New facts from owners", "{n} recorded in decisions: confirm or not"],
            "S3": ["Repeated one-off requests", "{n} resemble the process “{agent}”: a ritual or a task for an agent"],
            "S4": ["{agent}: level could go up", "drafts accepted without edits: decide at the retro"],
            "S5": ["{agent}: many rejections", "{n} in the period: decide at the retro whether to lower the level"],
            "S6": ["{agent}: not run", "no run in two iterations: ask the owner"],
            "S7code": ["{agent}: issue “{code}” ({n})", "discuss at the retro"],
            "S7fail": ["{agent}: drafts did not pass the gate ({n})", "after three attempts, with the owner, marked"],
            "S8": ["The gate missed a mistake", "the owner caught what the gate missed ({agent}): fix the gate"],
            "S9": ["{agent}: decision without a reason", "ask the owner, draw no conclusion"],
            "facts": ["Facts wait for confirmation", "{n} in the registry marked “to confirm”"],
        },
        "today": "Today", "todayEmpty": "No runs or decisions today.",
        "run": "{agent}: run", "decision": "{agent}: {decision}",
        "decisions": {"ACCEPTED": "accepted", "EDITED": "edited", "REJECTED": "rejected"},
        "neverTitle": "What agents never do",
        "never": ["publish or reply on platforms", "write to the brand core", "raise their own autonomy level",
                  "rate people by usage data"],
        "foot": "Built by build_team_map.py from the team folder. Updated at assembly and before the weekly meeting.",
        "themeDark": "Dark theme", "themeLight": "Light theme",
    },
}
SEVERITY = {"S7fail": "hi", "S1": "hi", "S8": "hi", "draft": "hi", "S2": "md", "S7code": "md", "S4": "md", "S5": "md",
            "facts": "md", "S3": "lo", "S6": "lo", "S9": "lo"}


def fmt(template: str, **kw) -> str:
    return template.format(**{k: v for k, v in kw.items()})


def library_domains() -> dict:
    out = {}
    for p in PROCESSES.glob("*.md"):
        m = re.search(r"^domain:\s*(\S+)", p.read_text(encoding="utf-8"), re.M)
        if m:
            out[p.stem] = m.group(1)
    return out


def group_of(library_id: str, domains: dict) -> str:
    d = domains.get(library_id or "")
    for key, members in GROUPS:
        if d in members:
            return key
    return "other"


def fact_counts(ws: Path) -> Counter:
    path = ws / "eb/brand-core/facts.md"
    counts = Counter()
    if not path.is_file():
        return counts
    col = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if col is None and ("Status" in cells or "Статус" in cells):
            col = cells.index("Status") if "Status" in cells else cells.index("Статус")
        elif col is not None and len(cells) > col and cells[col] in STATUSES:
            counts[cells[col]] += 1
    return counts


def table_rows(path: Path) -> int:
    if not path.is_file():
        return 0
    rows = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.startswith("|")]
    return max(len(rows) - 2, 0)


def sources(ws: Path) -> list:
    inbox = ws / "eb/inbox"
    if not inbox.is_dir():
        return []
    out = []
    for p in sorted(inbox.rglob("*"), key=lambda p: p.as_posix()):
        rel = p.relative_to(inbox)
        if p.is_file() and not any(part.startswith(("_", ".")) for part in rel.parts):
            name = re.sub(r"\s*\(копия\)|\s*\(copy\)", "", p.stem).replace("_", " ").strip()
            item = {"name": name, "ext": p.suffix.lstrip(".").lower() or "file"}
            if item not in out:
                out.append(item)
    return out


def clock(value: str) -> str:
    m = re.search(r"\d{4}-\d{2}-\d{2}[ T-](\d{2}):?(\d{2})", value or "")
    return f"{m.group(1)}:{m.group(2)}" if m else ""


def drafts(ws: Path, ids: list, decisions: list, since, until) -> dict:
    decided = {d["output"] for d in decisions if d.get("output")}
    out = {}
    for aid in ids:
        if aid in NO_DRAFTS:
            continue
        waiting = []
        for p in sorted((ws / "eb/work" / aid).glob("*.md")):
            day = retro_stats.day(p.name)
            rel = p.relative_to(ws).as_posix()
            if day and since <= day <= until and rel not in decided:
                waiting.append(day)
        if waiting:
            out[aid] = waiting
    return out


def read_outputs(ws: Path) -> dict:
    out = {}
    for p in (ws / "eb/log/decisions").glob("*.md"):
        out[p.relative_to(ws).as_posix()] = retro_stats.field(p.read_text(encoding="utf-8"), "Output")
    return out


def chain(p: dict, names: dict, ui: dict, agents: dict) -> list:
    # The main path: reads from the brand core are side inputs, not steps.
    seq = []
    steps = p.get("steps", [])
    refs = [steps[0].get("from")] if steps else []
    refs += [s.get("to") for s in steps if s.get("from") != "brand-core"]
    for ref in refs:
        if ref and ref != "coordinator" and (not seq or seq[-1]["ref"] != ref):
            seq.append({"ref": ref})
    out = []
    for n in seq:
        ref = n["ref"]
        if ref in ("owner", "lead"):
            kind = "person"
        elif ref in ("brand-core", "log"):
            kind = "store"
        elif agents.get(ref, {}).get("library_id") == "quality-gate" or ref == "quality-gate":
            kind = "gate"
        else:
            kind = "agent"
        out.append({"label": ui["nodes"].get(ref) or names.get(ref, ref), "kind": kind})
    return out


def collect(ws: Path, date: datetime.date, days: int) -> dict:
    roster, agents = render_team.load(ws)
    lang = "en" if roster.get("language") == "en" else "ru"
    ui = UI[lang]
    ready, waiting_pipes = render_team.pipelines_ready(roster, agents)
    stats = retro_stats.collect(ws, date, days)
    rows = {r["agent"]: r for r in stats["rows"]}
    decisions = retro_stats.read_decisions(ws)
    outputs = read_outputs(ws)
    for d in decisions:
        d["output"] = outputs.get(d["file"], "")
    runs = retro_stats.read_runs(ws)
    checks = list((ws / "eb/work/quality-gate").glob("*.md"))
    domains = library_domains()
    names = {a["id"]: a["name"] for a in roster.get("agents", [])}
    names.update({i: a["name"] for i, a in agents.items()})

    groups = {key: {"key": key, "label": ui["groups"][key], "agents": []} for key, _ in GROUPS}
    for ra in roster.get("agents", []):
        aid = ra["id"]
        a = agents.get(aid)
        entry = {"name": names.get(aid, aid), "owner": (a or ra).get("owner", ""), "wave": ui["waves"].get(ra.get("wave", ""), ra.get("wave", ""))}
        if a is None:
            entry.update({"assembled": False})
        else:
            op = a.get("operator", "none")
            r = rows.get(aid, {})
            if r.get("not_passed"):
                state, note = "alert", fmt(ui["notPassed"], n=r["not_passed"])
            elif not r.get("last_run"):
                state, note = "idle", ui["neverRun"]
            elif (date - r["last_run"]).days > days:
                state, note = "idle", fmt(ui["idle"], n=(date - r["last_run"]).days)
            else:
                state, note = "ok", fmt(ui["runs"], n=r.get("runs", 0))
            entry.update({"assembled": True, "autonomy": a["autonomy"], "external": a["external_facing"] == "true",
                          "operator": fmt(ui["operator"], name=op) if op and op != "none" else "",
                          "ritual": a.get("ritual", ""), "state": state, "note": note})
        groups[group_of((a or ra).get("library_id", ""), domains)]["agents"].append(entry)
    group_list = [g for g in groups.values() if g["agents"]]
    for g in group_list:
        a_n = sum(1 for x in g["agents"] if x["assembled"])
        w_n = len(g["agents"]) - a_n
        g["count"] = fmt(ui["groupCount"], a=a_n) + (" · " + fmt(ui["groupWait"], w=w_n) if w_n else "")

    pipes = []
    for p in ready:
        pipes.append({"title": p.get("title") or p["id"], "trigger": p.get("trigger", ""), "chain": chain(p, names, ui, agents)})
    for p, missing in waiting_pipes:
        pipes.append({"title": p.get("title") or p["id"], "trigger": fmt(ui["pipeWait"], names=", ".join(names.get(m, m) for m in missing)),
                      "chain": chain(p, names, ui, agents), "waiting": True})

    since = stats["since"]
    in_period = [d for d in decisions if since <= d["date"] <= date]
    clean = [d for d in in_period if d["decision"] == "ACCEPTED" or (d["decision"] == "EDITED" and d["substantive"] == "no")]
    subst = [d for d in in_period if d["decision"] == "EDITED" and d["substantive"] == "yes"]
    rej = [d for d in in_period if d["decision"] == "REJECTED"]
    first = sum(r["first"] for r in stats["rows"])
    first_pass = sum(r["first_pass"] for r in stats["rows"])
    codes = Counter()
    for r in stats["rows"]:
        codes.update(r["codes"])
    top = codes.most_common(1)
    status_rows = [
        str(sum(r["runs"] for r in stats["rows"])), str(len(in_period)),
        fmt(ui["of"], a=len(clean), b=len(in_period)) if in_period else ui["none"],
        f"{len(subst)} · {len(rej)}",
        fmt(ui["of"], a=first_pass, b=first) if first else ui["none"],
        f"{top[0][0]} · {top[0][1]}" if top else ui["none"],
        "0",
    ]

    items = []
    for aid, days_list in sorted(drafts(ws, list(agents), decisions, since, date).items()):
        items.append(("draft", {"agent": names.get(aid, aid), "n": len(days_list), "date": min(days_list).isoformat()}))
    s2 = 0
    for s in stats["signals"]:
        code, target = s["signal"], s["target"]
        agent = names.get(target, target)
        n = re.match(r"(\d+)", s["text"])
        n = int(n.group(1)) if n else 0
        if code == "S2":
            s2 += 1
        elif code == "S7":
            m = re.match(r"issue (\S+(?: LINE)?) found (\d+) times", s["text"])
            if m:
                items.append(("S7code", {"agent": agent, "code": m.group(1), "n": int(m.group(2))}))
            else:
                items.append(("S7fail", {"agent": agent, "n": n}))
        elif code == "S8":
            items.append(("S8", {"agent": names.get(s["text"].split(":")[0], s["text"].split(":")[0])}))
        elif code in ui["items"]:
            items.append((code, {"agent": agent, "n": n}))
    if s2:
        items.append(("S2", {"n": s2}))
    to_confirm = fact_counts(ws)["TO CONFIRM"]
    if to_confirm:
        items.append(("facts", {"n": to_confirm}))
    order = {"hi": 0, "md": 1, "lo": 2}
    items.sort(key=lambda it: order[SEVERITY[it[0]]])
    inbox = [{"sev": SEVERITY[k], "title": fmt(ui["items"][k][0], **v), "text": fmt(ui["items"][k][1], **v)} for k, v in items]

    today = []
    for r in runs:
        if r["date"] == date:
            t = retro_stats.field((ws / r["file"]).read_text(encoding="utf-8"), "Time")
            today.append((clock(t) or clock(Path(r["file"]).name), fmt(ui["run"], agent=names.get(r["agent"], r["agent"]))))
    for d in decisions:
        if d["date"] == date:
            today.append((clock(d["time"]) or clock(Path(d["file"]).name),
                          fmt(ui["decision"], agent=names.get(d["agent"], d["agent"]),
                              decision=ui["decisions"].get(d["decision"], d["decision"].lower()))))
    today.sort()

    facts = fact_counts(ws)
    core_files = sorted(p.stem for p in (ws / "eb/brand-core").glob("*.md"))
    src = sources(ws)
    owners = sorted({a["owner"] for a in agents.values()})
    waiting_agents = [a for a in roster.get("agents", []) if a["id"] not in agents]
    terms = {"ru": {"CONFIRMED": "подтверждено", "TO CONFIRM": "уточнить", "EVIDENCE NEEDED": "нужно доказательство", "OUTDATED": "устарело"},
             "en": {"CONFIRMED": "confirmed", "TO CONFIRM": "to confirm", "EVIDENCE NEEDED": "evidence needed", "OUTDATED": "outdated"}}[lang]
    return {
        "lang": lang,
        "title": ui["title"],
        "ui": {k: ui[k] for k in ("kicker", "lede", "lead", "coord", "coordTitle", "coordNote", "pipelines", "external",
                                  "decideTitle", "decide", "stopsTitle", "stops", "statusCmd", "statusRows", "inbox",
                                  "inboxEmpty", "today", "todayEmpty", "neverTitle", "never", "foot", "log", "themeDark", "themeLight")},
        "stamp": fmt(ui["stamp"], date=date.isoformat(), since=since.isoformat(), until=date.isoformat()),
        "tiles": [
            {"label": ui["tiles"][0], "value": str(len(agents)), "note": fmt(ui["tileNotes"][0], n=len(waiting_agents)) if waiting_agents else "", "dot": "green"},
            {"label": ui["tiles"][1], "value": fmt(ui["people"], n=len(owners)), "note": ui["tileNotes"][1], "dot": "sun"},
            {"label": ui["tiles"][2], "value": str(len(in_period)), "note": ui["tileNotes"][2], "dot": "violet"},
            {"label": ui["tiles"][3], "value": "0", "note": ui["tileNotes"][3], "dot": "coral"},
        ],
        "sources": {"label": fmt(ui["sources"], n=len(src)), "items": src[:12],
                    "more": fmt(ui["more"], n=len(src) - 12) if len(src) > 12 else ""},
        "leadItems": [fmt(x, n=table_rows(ws / "eb/brand-core/red-lines.md")) for x in ui["leadItems"]],
        "core": {"label": fmt(ui["core"], n=len(core_files)), "files": core_files,
                 "facts": fmt(ui["facts"], n=sum(facts.values())),
                 "factsBy": [f"{n} {terms[s]}" for s in STATUSES for n in [facts[s]] if n],
                 "note": ui["coreNote"]},
        "logItems": [fmt(ui["logItems"][0], n=len(runs)), fmt(ui["logItems"][1], n=len(decisions)),
                     fmt(ui["logItems"][2], n=len(checks)), ui["logItems"][3]],
        "coordPill": fmt(ui["coordPill"], n=len(ready)),
        "groups": group_list,
        "pipes": pipes,
        "status": {"date": date.isoformat(), "since": since.isoformat(), "rows": list(zip(ui["statusRows"], status_rows))},
        "inbox": inbox,
        "todayItems": [{"time": t, "text": x} for t, x in today],
    }


def build(data: dict) -> str:
    # Escape "<" so no string in the data can close the script element.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    page = TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("__LANG__", html.escape(data["lang"]), 1)
    page = page.replace("__TITLE__", html.escape(data["title"]), 1)
    return page.replace("__DATA__", payload, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--date", help="status date, YYYY-MM-DD (default: today)")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--out", help="output path (default: eb/team/team-map.html)")
    args = ap.parse_args()
    ws = Path(args.workspace).expanduser().resolve()
    if not (ws / "eb" / "status.md").is_file():
        print(f"{ws} is not an Employer Brand OS workspace", file=sys.stderr)
        return 2
    date = datetime.date.fromisoformat(args.date) if args.date else datetime.date.today()
    try:
        data = collect(ws, date, args.days)
    except (render_team.InputError, ValueError, KeyError) as exc:
        print(f"Input problem: {exc}", file=sys.stderr)
        return 1
    out = Path(args.out) if args.out else ws / "eb" / "team" / "team-map.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(data), encoding="utf-8")
    print(f"written {out.relative_to(ws) if out.is_relative_to(ws) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
