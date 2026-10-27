"""Deterministic tests of the plugin scripts on the demo company materials.

Run: python3 -m unittest discover tests

No model calls. Covers the answer-key traps that scripts handle (demo/answer-key.md):
T3 duplicates, T6 scripted counters in HTML, T9 NFD names, T10 PDF text layer,
T14 the write guard, plus generation, decisions, export and the overview page.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
MATERIALS = ROOT / "demo" / "materials"
PY = sys.executable


def run(script: str, *args, stdin: str = "") -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(SCRIPTS / script), *map(str, args)], input=stdin,
                          capture_output=True, text=True)


class Workspace(unittest.TestCase):
    """A fresh workspace with the demo materials in eb/inbox."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self.tmp.name)
        self.assertEqual(run("init_workspace.py", self.ws).returncode, 0)
        self.inbox = self.ws / "eb" / "inbox"
        for f in MATERIALS.iterdir():
            shutil.copy(f, self.inbox / f.name)

    def tearDown(self):
        self.tmp.cleanup()


class TestInit(Workspace):
    def test_runtime_dirs_and_rules_block(self):
        self.assertTrue((self.ws / ".claude/agents").is_dir(), "agents dir exists before Phase 2")
        self.assertTrue((self.ws / ".claude/skills").is_dir())
        rules = (self.ws / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("employer-brand-os:workspace:start", rules)
        self.assertIn("TARGET", rules)

    def test_rules_block_keeps_user_text_and_is_not_duplicated(self):
        claude = self.ws / "CLAUDE.md"
        claude.write_text("# Мои заметки\n", encoding="utf-8")
        run("init_workspace.py", self.ws)
        run("init_workspace.py", self.ws)
        text = claude.read_text(encoding="utf-8")
        self.assertIn("# Мои заметки", text)
        self.assertEqual(text.count("employer-brand-os:workspace:start"), 1)


class TestIntake(Workspace):
    def test_inventory_duplicates_pdf_and_nfd(self):
        self.assertEqual(run("inventory.py", self.inbox).returncode, 0)
        inv = (self.inbox / "_inventory.md").read_text(encoding="utf-8")
        rows = {line.split("|")[1].strip(): line for line in inv.splitlines() if line.startswith("| ") and "File" not in line}
        copy = next(k for k in rows if "(копия)" in k)
        self.assertIn("EVP_v2_2025_утверждено.docx", rows[copy].split("|")[7], "T3: the copy points to the original")
        original = next(k for k in rows if k == "EVP_v2_2025_утверждено.docx")
        self.assertEqual(rows[original].split("|")[7].strip(), "", "T3: the original is not a duplicate")
        pdf = next(v for k, v in rows.items() if k.endswith(".pdf"))
        self.assertNotIn("scan", pdf, "T10: the PDF has a text layer")
        self.assertTrue(any("NFD or non-breaking space" in k for k in rows), "T9: odd file name flagged")

    def test_extraction_formats(self):
        self.assertEqual(run("extract_text.py", self.inbox).returncode, 0)
        text = self.inbox / "_text"
        html = (text / "Презентация_для_студентов.html.txt").read_text(encoding="utf-8")
        for value in ("1800", "38", "4"):
            self.assertIn(f"data-count={value}", html, "T6: counter value kept")
        self.assertNotIn("animate", html, "scripts dropped")
        self.assertNotIn("base64", html, "inline images dropped")
        pptx = (text / "Стратегия_EB_2026.pptx.txt").read_text(encoding="utf-8")
        self.assertIn("с 18% до 12%", pptx)
        self.assertEqual(pptx.count("--- slide"), 7)
        xlsx = (text / "Итоги_2025.xlsx.txt").read_text(encoding="utf-8")
        self.assertIn("Текучесть операторов кранов, %\t21\t18", xlsx)
        docx = (text / "EVP_v2_2025_утверждено.docx.txt").read_text(encoding="utf-8")
        self.assertIn("Работа, на которой держится Север", docx)

    def test_extraction_refuses_dtd(self):
        bad = self.inbox / "bad.docx"
        with zipfile.ZipFile(bad, "w") as z:
            z.writestr("word/document.xml", '<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "a">]><x>&a;</x>')
        out = run("extract_text.py", self.inbox).stdout
        self.assertIn("failed bad.docx", out)

    def test_nfd_extract_name_is_normalised(self):
        nfd = unicodedata.normalize("NFD", "Отчёт итоги.html")
        (self.inbox / nfd).write_text("<p>текст</p>", encoding="utf-8")
        run("extract_text.py", self.inbox)
        self.assertTrue((self.inbox / "_text" / "Отчёт итоги.html.txt").is_file())


class TestGuard(unittest.TestCase):
    """T14: agents write only their own folder; subagents never write the brand core."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self.tmp.name).resolve()
        (self.ws / "eb").mkdir()
        (self.ws / "eb" / "status.md").write_text("x")

    def tearDown(self):
        self.tmp.cleanup()

    def guard(self, agent, path, cwd=None):
        event = {"cwd": str(cwd or self.ws), "tool_input": {"file_path": str(path)}}
        if agent:
            event["agent_type"] = agent
        return run("guard_write.py", stdin=json.dumps(event)).returncode

    def test_cases(self):
        w = self.ws
        cases = [
            ("eb-stories", w / "eb/work/stories/a.md", 0),
            ("eb-stories", "eb/work/stories/sub/a.md", 0),
            ("eb-stories", w / "eb/work/stories-x/a.md", 2),
            ("eb-stories", w / "eb/work/stories/../reviews/a.md", 2),
            ("eb-stories", w / "eb/brand-core/facts.md", 2),
            ("eb-stories", "/tmp/elsewhere.md", 2),
            ("general-purpose", w / "eb/brand-core/facts.md", 2),
            ("general-purpose", w / "eb/log/decisions/x.md", 2),
            ("general-purpose", w / ".claude/agents/x.md", 2),
            ("general-purpose", w / "eb/inbox/_notes/M01.md", 0),
            (None, w / "eb/brand-core/facts.md", 0),
        ]
        for agent, path, expected in cases:
            with self.subTest(agent=agent, path=str(path)):
                self.assertEqual(self.guard(agent, path), expected)

    def test_inert_outside_workspace(self):
        with tempfile.TemporaryDirectory() as other:
            self.assertEqual(self.guard("eb-stories", Path(other) / "x.md", cwd=other), 0)
        self.assertEqual(run("guard_write.py", stdin="not json").returncode, 0)

    def test_run_log_only_for_team_agents(self):
        run("log_run.py", stdin=json.dumps({"cwd": str(self.ws), "agent_type": "general-purpose"}))
        run("log_run.py", stdin=json.dumps({"cwd": str(self.ws), "agent_type": "eb-stories", "last_assistant_message": "done"}))
        runs = list((self.ws / "eb/log/runs").glob("*.md"))
        self.assertEqual(len(runs), 1)
        self.assertIn("done", runs[0].read_text(encoding="utf-8"))


class TestAssembly(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self.tmp.name)
        run("init_workspace.py", self.ws)
        shutil.copy(ROOT / "templates/team-roster.sample.json", self.ws / "eb/diagnosis/team-roster.json")
        (self.ws / "eb/team/agents").mkdir(parents=True)
        shutil.copy(ROOT / "templates/agent.sample.md", self.ws / "eb/team/agents/employee-stories.md")

    def tearDown(self):
        self.tmp.cleanup()

    def test_render_is_deterministic_and_keeps_user_text(self):
        (self.ws / "CLAUDE.md").write_text("# Our own notes\n\nKeep me.\n", encoding="utf-8")
        self.assertEqual(run("render_team.py", self.ws, "--no-vendor").returncode, 0)
        first = (self.ws / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("Keep me.", first)
        run("render_team.py", self.ws, "--no-vendor")
        self.assertEqual((self.ws / "CLAUDE.md").read_text(encoding="utf-8"), first)
        agent = (self.ws / ".claude/agents/eb-employee-stories.md").read_text(encoding="utf-8")
        self.assertIn("name: eb-employee-stories", agent)
        self.assertNotIn("WebFetch", agent, "no web access unless the description allows it")
        gitignore = (self.ws / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("eb/inbox/**", gitignore)
        self.assertIn("!eb/inbox/_notes/**", gitignore)

    def test_pipeline_waits_for_missing_agent(self):
        out = run("render_team.py", self.ws, "--no-vendor", "--check").stdout
        self.assertIn("waiting pipeline story: needs quality-gate", out)

    def test_rejects_external_agent_at_l2(self):
        f = self.ws / "eb/team/agents/employee-stories.md"
        f.write_text(f.read_text(encoding="utf-8").replace("autonomy: L1", "autonomy: L2"), encoding="utf-8")
        r = run("render_team.py", self.ws, "--no-vendor", "--check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("capped at L1", r.stderr)

    def test_vendor_and_join_script(self):
        self.assertEqual(run("render_team.py", self.ws).returncode, 0)
        market = json.loads((self.ws / "vendor/eb-marketplace/.claude-plugin/marketplace.json").read_text())
        self.assertEqual(market["plugins"][0]["source"], "./employer-brand-os")
        self.assertTrue((self.ws / "vendor/eb-marketplace/employer-brand-os/hooks/hooks.json").is_file())
        self.assertFalse((self.ws / "vendor/eb-marketplace/employer-brand-os/.git").exists())
        self.assertTrue((self.ws / "join_team.sh").is_file())


class TestDecisionsExportOverview(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self.tmp.name)
        run("init_workspace.py", self.ws)

    def tearDown(self):
        self.tmp.cleanup()

    def test_decision_requires_substantive_for_edits(self):
        r = run("record_decision.py", self.ws, "--agent", "x", "--output", "o", "--decision", "EDITED", "--reason", "r", "--by", "b")
        self.assertEqual(r.returncode, 2)

    def test_decision_record(self):
        r = run("record_decision.py", self.ws, "--agent", "eb-stories", "--output", "eb/work/stories/a.md",
                "--decision", "REJECTED", "--reason", "Не про нас", "--by", "Контент-менеджер", "--operator", "Руководитель EB")
        self.assertEqual(r.returncode, 0)
        text = (self.ws / r.stdout.strip()).read_text(encoding="utf-8")
        self.assertIn("- Agent: stories", text, "runtime prefix removed")
        self.assertIn("via operator Руководитель EB", text)

    def test_export_docx_round_trip(self):
        md = self.ws / "d.md"
        md.write_text("# Заголовок\n\nТекст с **жирным** & <угловыми>.\n\n- пункт\n", encoding="utf-8")
        self.assertEqual(run("export_docx.py", md, self.ws / "d.docx").returncode, 0)
        with zipfile.ZipFile(self.ws / "d.docx") as z:
            xml = z.read("word/document.xml").decode("utf-8")
        self.assertIn("&amp; &lt;угловыми&gt;", xml)
        self.assertIn('<w:pStyle w:val="Heading1"/>', xml)

    def test_overview_escapes_hostile_text(self):
        data = json.loads((ROOT / "templates/overview.sample.json").read_text(encoding="utf-8"))
        data["title"] = "</title><script>alert(1)</script>"
        data["agents"][0]["name"] = "</script><img src=x onerror=alert(2)>"
        src = self.ws / "o.json"
        src.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(run("build_overview.py", src, self.ws / "o.html").returncode, 0)
        page = (self.ws / "o.html").read_text(encoding="utf-8")
        self.assertNotIn("<script>alert(1)", page)
        self.assertNotIn("<img src=x", page)
        self.assertEqual(page.count("<script"), 2)


if __name__ == "__main__":
    unittest.main()
