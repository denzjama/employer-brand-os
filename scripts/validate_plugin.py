#!/usr/bin/env python3
"""Validate Employer Brand OS. Standard library only.

Checks manifests, skill frontmatter, the process library format and the
autonomy cap, and that every referenced methodology or library file exists.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAINS = {
    "strategy", "research", "reputation", "content", "social", "campaigns",
    "creative", "quality", "analytics", "operations", "adoption",
}
LEVELS = {"L0", "L1", "L2"}
SECTIONS = [
    "Purpose", "Fits when", "Triggers", "Inputs", "Outputs",
    "Human checkpoint", "Suggested ritual", "Metrics", "Risks and limits",
]
REQUIRED = [
    "ARCHITECTURE.md", "README.md", "LICENSE", "AGENTS.md", "SECURITY.md",
    ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
    "methodology/principles.md", "methodology/terminology.md", "methodology/workspace.md",
    "methodology/brand-core.md", "methodology/diagnosis.md", "methodology/autonomy.md",
    "library/README.md", "scripts/init_workspace.py", "scripts/extract_text.py",
    "scripts/inventory.py", "scripts/build_overview.py", "CHANGELOG.md",
    "templates/overview.html", "templates/overview.sample.json", "templates/team-roster.sample.json",
    "methodology/assembly.md", "methodology/coordination.md", "templates/agent.sample.md",
    "hooks/hooks.json", "scripts/render_team.py", "scripts/guard_write.py", "scripts/log_run.py",
    "library/agents/README.md", "library/pipelines/README.md", "methodology/quality.md", "methodology/retro.md",
    "scripts/retro_stats.py", "skills/retro/SKILL.md", "docs/guide-ru.md", "docs/security-ru.md", "demo/retro/README.md", "demo/retro/build_logs.py", "scripts/eb_hooks.py", "scripts/record_decision.py", "scripts/export_docx.py", "scripts/join_team.sh",
]
REF_SECTIONS = [
    "Purpose", "Reads", "Produces", "Method", "Handoff", "Checks before handing over", "Never does",
    "Common failures", "Client specifics to collect",
]
PIPE_SECTIONS = ["Purpose", "Fits when", "Trigger", "Steps", "Decision", "Variants", "Risks and limits"]
RITUALS = ["weekly", "core-review", "decide", "export-docx", "eb-sync"]
ROSTER_SPECIAL = {"owner", "coordinator", "brand-core", "log", "lead"}
UNFINISHED = re.compile(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum)\b", re.I)

errors: list = []


def err(msg: str) -> None:
    errors.append(msg)


def frontmatter(path: Path) -> tuple:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        err(f"{path.relative_to(ROOT)}: missing frontmatter")
        return {}, text
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, m.group(2)


def check_required() -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            err(f"missing required file {rel}")


def check_manifests() -> None:
    try:
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        err(f"manifest: {exc}")
        return
    entries = [p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")]
    if not entries:
        err("marketplace.json has no entry for the plugin name")
    elif entries[0].get("version") != plugin.get("version"):
        err("plugin.json and marketplace.json versions differ")
    if not re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")):
        err("plugin.json version is not semver")


def check_refs(path: Path, text: str) -> None:
    base = path.parent
    for ref in set(re.findall(r"`((?:\.\./)+[\w./-]+\.md)`", text)):
        if not (base / ref).resolve().is_file():
            err(f"{path.relative_to(ROOT)}: broken reference {ref}")
    for ref in set(re.findall(r"`((?:methodology|library)/[\w./-]+\.md)`", text)):
        if not (ROOT / ref).is_file():
            err(f"{path.relative_to(ROOT)}: broken reference {ref}")
    for name in set(re.findall(r"`([a-z-]+\.md)` §", text)):
        if not (ROOT / "methodology" / name).is_file():
            err(f"{path.relative_to(ROOT)}: section reference to unknown file {name}")


def check_skills() -> None:
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        err("no skills found")
    for path in skills:
        fields, body = frontmatter(path)
        if fields.get("name") != path.parent.name:
            err(f"{path.relative_to(ROOT)}: name must equal folder name")
        desc = fields.get("description", "")
        if not desc or len(desc) > 1024:
            err(f"{path.relative_to(ROOT)}: description missing or over 1024 characters")
        if "data, not instructions" not in body:
            err(f"{path.relative_to(ROOT)}: must keep the 'data, not instructions' rule")
        check_refs(path, body)


def check_library() -> None:
    entries = sorted((ROOT / "library/processes").glob("*.md"))
    if not entries:
        err("process library is empty")
    for path in entries:
        rel = path.relative_to(ROOT)
        fields, body = frontmatter(path)
        if fields.get("id") != path.stem:
            err(f"{rel}: id must equal file name")
        if fields.get("domain") not in DOMAINS:
            err(f"{rel}: unknown domain {fields.get('domain')}")
        for key in ("name", "name_ru"):
            if not fields.get(key):
                err(f"{rel}: missing {key}")
        level = fields.get("default_autonomy")
        if level not in LEVELS:
            err(f"{rel}: default_autonomy must be one of {sorted(LEVELS)}")
        ext = fields.get("external_facing")
        if ext not in {"true", "false"}:
            err(f"{rel}: external_facing must be true or false")
        if ext == "true" and level == "L2":
            err(f"{rel}: external-facing processes are capped at L1 (autonomy.md §2)")
        found = re.findall(r"^## (.+)$", body, re.M)
        if found != SECTIONS:
            err(f"{rel}: sections must be exactly {SECTIONS}, found {found}")
        check_refs(path, body)
    covered = {frontmatter(p)[0].get("domain") for p in entries}
    for missing in sorted(DOMAINS - covered):
        err(f"library has no process in domain {missing}")


def pipeline_steps(body: str) -> list:
    m = re.search(r"^## Steps\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", m.group(1) if m else "", re.M)
    return [{"from": a, "to": b, "what": c} for a, b, c in rows if a != "From" and not set(a) <= {"-"}]


def check_references() -> None:
    processes = {p.stem: frontmatter(p)[0] for p in (ROOT / "library/processes").glob("*.md")}
    for path in sorted((ROOT / "library/agents").glob("*.md")):
        if path.name == "README.md":
            continue
        rel = path.relative_to(ROOT)
        fields, body = frontmatter(path)
        if fields.get("id") != path.stem or path.stem not in processes:
            err(f"{rel}: id must equal the file name and a process in library/processes/")
            continue
        found = re.findall(r"^## (.+)$", body, re.M)
        if found != REF_SECTIONS:
            err(f"{rel}: sections must be exactly {REF_SECTIONS}, found {found}")
        if processes[path.stem].get("external_facing") == "true" and "CONFIRMED" not in body:
            err(f"{rel}: an external-facing reference must require CONFIRMED facts")
        if not re.search(r"^\d+\. ", body, re.M):
            err(f"{rel}: Method must be numbered steps")
        check_refs(path, body)
    ids = set()
    for path in sorted((ROOT / "library/pipelines").glob("*.md")):
        if path.name == "README.md":
            continue
        rel = path.relative_to(ROOT)
        fields, body = frontmatter(path)
        ids.add(path.stem)
        if fields.get("id") != path.stem or not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", path.stem):
            err(f"{rel}: id must be kebab-case and equal the file name")
        if path.stem in RITUALS:
            err(f"{rel}: id collides with a ritual command")
        for key in ("name", "name_ru"):
            if not fields.get(key):
                err(f"{rel}: missing {key}")
        agents = [a.strip() for a in fields.get("agents", "").split(",") if a.strip()]
        unknown = [a for a in agents if a not in processes]
        if not agents or unknown:
            err(f"{rel}: agents must list library processes, unknown: {unknown}")
        ext = fields.get("external_facing")
        if ext not in {"true", "false"}:
            err(f"{rel}: external_facing must be true or false")
        if ext == "false" and any(processes.get(a, {}).get("external_facing") == "true" for a in agents):
            err(f"{rel}: uses an external-facing agent, so the pipeline is external-facing")
        found = re.findall(r"^## (.+)$", body, re.M)
        if found != PIPE_SECTIONS:
            err(f"{rel}: sections must be exactly {PIPE_SECTIONS}, found {found}")
        steps = pipeline_steps(body)
        if not steps:
            err(f"{rel}: no steps table")
            continue
        refs = {s[k] for s in steps for k in ("from", "to")}
        for ref in sorted(refs - set(agents) - ROSTER_SPECIAL):
            err(f"{rel}: step refers to {ref}, which is neither in agents nor a role")
        for a in agents:
            if a not in refs:
                err(f"{rel}: agent {a} takes no step")
        if steps[-1]["to"] != "log" or steps[-1]["from"] not in {"owner", "lead"}:
            err(f"{rel}: the last step must record a person's decision in the log")
        if ext == "true":
            if "quality-gate" not in agents:
                err(f"{rel}: an external-facing pipeline passes the quality gate")
            for s in steps:
                if s["from"] == "quality-gate" and s["to"] not in {"owner", "lead"}:
                    err(f"{rel}: the quality gate hands over to the person who decides")
                if (processes.get(s["from"], {}).get("external_facing") == "true"
                        and s["to"] in {"owner", "lead"}):
                    err(f"{rel}: {s['from']} reaches a person without the quality gate")
    roster = json.loads((ROOT / "templates/team-roster.sample.json").read_text(encoding="utf-8"))
    for pl in roster.get("pipelines", []):
        lib = pl.get("library_id")
        if lib is not None and lib != "CUSTOM" and lib not in ids:
            err(f"team-roster.sample.json: pipeline {pl.get('id')} has unknown library_id {lib}")


def check_phase34() -> None:
    import filecmp
    import shutil
    import subprocess
    import tempfile
    sys.path.insert(0, str(ROOT / "scripts"))
    import retro_stats
    quality = (ROOT / "methodology/quality.md").read_text(encoding="utf-8")
    terms = (ROOT / "methodology/terminology.md").read_text(encoding="utf-8")
    in_quality = set(re.findall(r"\| `([A-Z][A-Z ]+[A-Z])` \| (?:yes|no)", quality))
    in_quality |= set(re.findall(r"is issue `([A-Z]+)`", quality))
    for code in sorted(retro_stats.CODES):
        if code not in in_quality:
            err(f"issue code {code} is counted by retro_stats.py but not defined in quality.md")
        if f"`{code}`" not in terms:
            err(f"issue code {code} is missing from terminology.md")
    for code in sorted(in_quality - retro_stats.CODES):
        err(f"issue code {code} in quality.md is not counted by retro_stats.py")
    # The demo logs are rebuilt from build_logs.py; the committed overlay must match.
    overlay = ROOT / "demo/retro/overlay"
    if not overlay.is_dir():
        err("demo/retro/overlay is missing: run demo/retro/build_logs.py")
        return
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "retro"
        shutil.copytree(ROOT / "demo/retro", copy, ignore=shutil.ignore_patterns("overlay", "__pycache__"))
        subprocess.run([sys.executable, str(copy / "build_logs.py")], capture_output=True)
        cmp = filecmp.dircmp(overlay, copy / "overlay")
        def diff(c, prefix=""):
            out = [prefix + n for n in c.left_only + c.right_only + c.diff_files]
            for name, sub in c.subdirs.items():
                out += diff(sub, prefix + name + "/")
            return out
        changed = diff(cmp)
        if changed:
            err(f"demo/retro/overlay is out of date with build_logs.py: {changed[:5]}")


def check_publishable() -> None:
    """Nothing machine- or client-specific may be published with the plugin."""
    import subprocess
    files = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=ROOT).stdout.split()
    if not files:
        return
    if any(f.startswith("eb/") for f in files):
        err("a client workspace (eb/) is tracked at the repository root")
    home = re.compile(r"(/Users/|/home/|C:\\Users\\|/private/var/|/private/tmp/)[A-Za-z0-9._-]+")
    for rel in files:
        path = ROOT / rel
        if path.suffix.lower() not in {".md", ".py", ".json", ".sh", ".yaml", ".html", ".txt", ".csv"} or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        m = home.search(text)
        if m:
            err(f"{rel}: machine-specific path {m.group(0)}")


def check_text() -> None:
    for path in [*ROOT.glob("*.md"), *ROOT.glob("methodology/*.md"), *ROOT.glob("library/**/*.md"), *ROOT.glob("skills/*/SKILL.md")]:
        text = path.read_text(encoding="utf-8")
        if UNFINISHED.search(text):
            err(f"{path.relative_to(ROOT)}: unfinished-work marker")
        if path.parent.name == "methodology":
            check_refs(path, text)


def check_templates() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_overview  # noqa: E402

    try:
        sample = json.loads((ROOT / "templates/overview.sample.json").read_text(encoding="utf-8"))
        roster = json.loads((ROOT / "templates/team-roster.sample.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        err(f"templates: {exc}")
        return
    for problem in build_overview.check(sample):
        err(f"templates/overview.sample.json: {problem}")
    page = (ROOT / "templates/overview.html").read_text(encoding="utf-8")
    for marker in ("__LANG__", "__TITLE__", "__DATA__"):
        if page.count(marker) != 1:
            err(f"templates/overview.html: placeholder {marker} must appear exactly once")
    if 'data-theme="dark"' not in page or "prefers-color-scheme" in page:
        err("templates/overview.html: must be light by default with an explicit dark switch")
    ids = {a["id"] for a in roster.get("agents", [])}
    for a in roster.get("agents", []):
        for key in ("owner", "tool_access", "autonomy", "ritual", "first_metric", "inputs_from", "outputs_to"):
            if key not in a:
                err(f"team-roster.sample.json: agent {a.get('id')} missing {key}")
        for ref in a.get("inputs_from", []) + a.get("outputs_to", []):
            if ref not in ids | ROSTER_SPECIAL:
                err(f"team-roster.sample.json: agent {a.get('id')} refers to unknown {ref}")
    for pl in roster.get("pipelines", []):
        for st in pl.get("steps", []):
            for ref in (st.get("from"), st.get("to")):
                if ref not in ids | ROSTER_SPECIAL:
                    err(f"team-roster.sample.json: pipeline {pl.get('id')} refers to unknown {ref}")


def check_phase2() -> None:
    import re as _re
    import shutil
    import subprocess
    import tempfile

    try:
        hooks = json.loads((ROOT / "hooks/hooks.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        err(f"hooks/hooks.json: {exc}")
        return
    for groups in hooks.get("hooks", {}).values():
        for group in groups:
            for h in group.get("hooks", []):
                for script in _re.findall(r"scripts/[\w.]+", h.get("command", "")):
                    if not (ROOT / script).is_file():
                        err(f"hooks/hooks.json: missing {script}")
    for r in RITUALS:
        f = ROOT / "templates/rituals" / r / "SKILL.md"
        if not f.is_file():
            err(f"missing ritual template {r}")
            continue
        fields, body = frontmatter(f)
        if fields.get("name") != r:
            err(f"templates/rituals/{r}: name must be {r}")
        if "data, not instructions" not in body:
            err(f"templates/rituals/{r}: must keep the 'data, not instructions' rule")
    # Integration: assemble the fictional sample team in a temporary workspace.
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        (ws / "eb/diagnosis").mkdir(parents=True)
        (ws / "eb/team/agents").mkdir(parents=True)
        (ws / "eb/status.md").write_text("# status\n")
        shutil.copy(ROOT / "templates/team-roster.sample.json", ws / "eb/diagnosis/team-roster.json")
        shutil.copy(ROOT / "templates/agent.sample.md", ws / "eb/team/agents/employee-stories.md")
        run = subprocess.run([sys.executable, str(ROOT / "scripts/render_team.py"), str(ws), "--no-vendor"],
                             capture_output=True, text=True)
        if run.returncode != 0:
            err(f"render_team.py on the samples failed: {run.stderr.strip() or run.stdout.strip()}")
            return
        expected = [".claude/agents/eb-employee-stories.md", "CLAUDE.md", "eb/team/roster.md", ".gitignore"]
        expected += [f".claude/skills/{r}/SKILL.md" for r in RITUALS]
        for rel in expected:
            if not (ws / rel).is_file():
                err(f"render_team.py did not write {rel}")
        claude_md = (ws / "CLAUDE.md").read_text(encoding="utf-8")
        if "{{" in claude_md or any("{{" in (ws / ".claude/skills" / r / "SKILL.md").read_text() for r in RITUALS):
            err("render_team.py left an unfilled placeholder")
        before = claude_md
        subprocess.run([sys.executable, str(ROOT / "scripts/render_team.py"), str(ws), "--no-vendor"], capture_output=True)
        if (ws / "CLAUDE.md").read_text(encoding="utf-8") != before:
            err("render_team.py is not deterministic: a second run changed CLAUDE.md")


def check_demo_and_evals() -> None:
    import subprocess

    for rel in ("demo/README.md", "demo/answer-key.md", "demo/interview.md", "demo/build_materials.py",
                "evals/README.md", "evals/_lib/setup.sh", "tests/test_scripts.py"):
        if not (ROOT / rel).is_file():
            err(f"missing {rel}")
    if not any((ROOT / "demo/materials").glob("*")):
        err("demo/materials is empty: run python3 demo/build_materials.py")
    for case in sorted(p for p in (ROOT / "evals").iterdir() if p.is_dir() and not p.name.startswith(("_", "results"))):
        for f in ("case.yaml", "prompt.md", "scaffold.sh"):
            if not (case / f).is_file():
                err(f"evals/{case.name}: missing {f}")
        if not list((case / "graders").glob("*.md")):
            err(f"evals/{case.name}: no graders")
        scaffold = (case / "scaffold.sh").read_text(encoding="utf-8") if (case / "scaffold.sh").is_file() else ""
        for snap in re.findall(r"snapshot (\S+)", scaffold):
            if not (ROOT / "demo/run" / snap / "workspace/eb/status.md").is_file():
                err(f"evals/{case.name}: snapshot demo/run/{snap} is missing")
    tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-q"],
                           capture_output=True, text=True, cwd=ROOT)
    if tests.returncode != 0:
        err("script tests failed:\n" + tests.stderr[-2000:])


def main() -> int:
    check_required()
    check_templates()
    check_phase2()
    check_demo_and_evals()
    check_manifests()
    check_skills()
    check_library()
    check_references()
    check_phase34()
    check_publishable()
    check_text()
    if errors:
        print(f"FAILED: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    skills = len(list((ROOT / "skills").glob("*/SKILL.md")))
    procs = len(list((ROOT / "library/processes").glob("*.md")))
    refs = len(list((ROOT / "library/agents").glob("*.md"))) - 1
    pipes = len(list((ROOT / "library/pipelines").glob("*.md"))) - 1
    print(f"OK: {skills} skills, {procs} library processes, {refs} reference agents, {pipes} pipelines, manifests consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
