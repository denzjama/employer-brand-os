#!/usr/bin/env python3
"""Create the Employer Brand OS workspace layout (methodology/workspace.md).

Usage: python3 init_workspace.py <workspace-dir> [--lang ru|en]

Never overwrites an existing file. Refuses to run inside a plugin directory.
"""
import argparse
import datetime
import sys
from pathlib import Path

DIRS = [
    "eb/inbox/_text",
    "eb/inbox/_notes",
    "eb/brand-core",
    "eb/diagnosis",
    "eb/team",
    "eb/work/adhoc",
    "eb/log",
    "eb/retro/proposals",
]

TEXT = {
    "ru": {
        "draft": "Черновик: ещё не утверждён руководителем EB.",
        "status": (
            "# Статус Employer Brand OS\n\n"
            "Фаза: 1 — диагноз функции\n\n"
            "## Шаги\n\n"
            "- [x] {today} Рабочая папка создана\n"
            "- [ ] Материалы положены в eb/inbox/ и проиндексированы\n"
            "- [ ] Бренд-ядро собрано\n"
            "- [ ] Факты бренд-ядра подтверждены\n"
            "- [ ] Интервью: блок A — мандат и ожидания\n"
            "- [ ] Интервью: блок B — команда\n"
            "- [ ] Интервью: блок C — процессы\n"
            "- [ ] Интервью: блок D — данные и системы\n"
            "- [ ] Интервью: блок E — цели и планы\n"
            "- [ ] Интервью: блок F — готовность к изменениям и ритуалы\n"
            "- [ ] Карта функции и AI-карта\n"
            "- [ ] Предложение по команде агентов и конвейеры\n"
            "- [ ] Проверка с будущими владельцами агентов\n"
            "- [ ] Сводка для CHRO\n"
            "- [ ] Разбор и утверждение с руководителем EB\n"
            "- [ ] Страница обзора\n\n"
            "Отметки: [ ] не начато, [~] частично (чего ждём — ниже), [x] готово.\n\n"
            "## Ждём\n\n"
            "Пока ничего.\n\n"
            "## Готовность к фазе 2\n\n"
            "- Согласование безопасности: не готово\n"
            "- Доступ к инструменту у владельцев: не готово\n"
            "- Общая папка команды: не готово\n"
            "- Проверка с будущими владельцами: не готово\n"
            "- Подтверждённые факты для внешних агентов: не готово\n\n"
            "Следующий шаг: положить материалы в eb/inbox/ и попросить собрать бренд-ядро.\n"
        ),
        "titles": {
            "evp.md": "EVP",
            "voice.md": "Голос бренда",
            "facts.md": "Реестр фактов",
            "audiences.md": "Аудитории",
            "red-lines.md": "Красные линии",
            "decisions.md": "Журнал решений",
        },
        "index": "Индекс материалов",
        "interview": "Журнал интервью",
    },
    "en": {
        "draft": "DRAFT — not yet approved by the EB lead.",
        "status": (
            "# Employer Brand OS status\n\n"
            "Phase: 1 — function diagnosis\n\n"
            "## Steps\n\n"
            "- [x] {today} Workspace created\n"
            "- [ ] Materials placed in eb/inbox/ and indexed\n"
            "- [ ] Brand core built\n"
            "- [ ] Brand-core facts confirmed\n"
            "- [ ] Interview: block A — mandate and expectations\n"
            "- [ ] Interview: block B — team\n"
            "- [ ] Interview: block C — processes\n"
            "- [ ] Interview: block D — data and systems\n"
            "- [ ] Interview: block E — goals and plans\n"
            "- [ ] Interview: block F — change readiness and rituals\n"
            "- [ ] Function map and AI map\n"
            "- [ ] Agent team proposal and pipelines\n"
            "- [ ] Validation with the future owners\n"
            "- [ ] CHRO summary\n"
            "- [ ] Review and approval with the EB lead\n"
            "- [ ] Overview page\n\n"
            "Marks: [ ] not started, [~] partly done (see Waiting for), [x] done.\n\n"
            "## Waiting for\n\n"
            "Nothing yet.\n\n"
            "## Readiness for Phase 2\n\n"
            "- Security approval: not ready\n"
            "- Tool access for owners: not ready\n"
            "- Shared team workspace: not ready\n"
            "- Validation with future owners: not ready\n"
            "- Confirmed facts for external-facing agents: not ready\n\n"
            "Next step: put materials into eb/inbox/ and ask to build the brand core.\n"
        ),
        "titles": {
            "evp.md": "EVP",
            "voice.md": "Tone of voice",
            "facts.md": "Fact registry",
            "audiences.md": "Audiences",
            "red-lines.md": "Red lines",
            "decisions.md": "Decision log",
        },
        "index": "Material index",
        "interview": "Interview log",
    },
}

FACTS_TABLE = "| ID | Fact | Kind | Pillar | Source | Period | Status | Confirmed | Notes |\n|---|---|---|---|---|---|---|---|---|\n"
INDEX_TABLE = (
    "| ID | File | Type | Format | Pages | Period | Same as | Summary | Personal data | Used for |\n"
    "|---|---|---|---|---|---|---|---|---|---|\n\n"
    "## Decisions\n\n| Date | Material | Decision | Who decided |\n|---|---|---|---|\n"
)


def write_new(path: Path, content: str, created: list) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")
    created.append(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--lang", choices=sorted(TEXT), default="ru")
    args = parser.parse_args()

    root = Path(args.workspace).expanduser().resolve()
    for candidate in [root, *root.parents]:
        if (candidate / ".claude-plugin").is_dir():
            print(f"Refusing: {candidate} is a plugin directory. Choose a separate workspace folder.", file=sys.stderr)
            return 2

    t = TEXT[args.lang]
    today = datetime.date.today().isoformat()
    created: list = []
    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    write_new(root / "eb/status.md", t["status"].format(today=today), created)
    write_new(root / "eb/inbox/_index.md", f"# {t['index']}\n\n{INDEX_TABLE}", created)
    write_new(root / "eb/diagnosis/interview-log.md", f"# {t['interview']}\n", created)
    write_new(root / "eb/log/adhoc.md", "# One-off requests\n\n| Date | Request | Similar library process | Time |\n|---|---|---|---|\n", created)
    for name, title in t["titles"].items():
        body = f"# {title}\n\n{t['draft']}\n\n"
        if name == "facts.md":
            body += FACTS_TABLE
        write_new(root / "eb/brand-core" / name, body, created)

    print(f"Workspace: {root}")
    for p in created:
        print(f"created {p.relative_to(root)}")
    if not created:
        print("Nothing created: the workspace already exists.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
