# AGENTS.md — Employer Brand OS

Project instructions for AI coding agents working on this repository (Claude Code, Codex, Cursor and others). `.claude/CLAUDE.md` imports this file, so every agent reads the same rules.

## What this project is

Employer Brand OS is a Claude Code plugin (v0.3.1): a multi-agent system for an Employer Brand function. It works in four phases: diagnosis → team assembly → work → adaptation. This version ships Phase 1 (`eb-setup`, `brand-core`, `function-diagnosis`, the overview page), Phase 2 (`team-assembly`, the reference agents and pipeline library in `library/`, the generator `scripts/render_team.py`, ritual command templates, and the plugin hooks that guard writes and log runs), and Phases 3–4 (the quality gate on the Employer Brand Auditor method in `methodology/quality.md`, and the `retro` skill with `scripts/retro_stats.py`). `ARCHITECTURE.md` is the product design; read it before changing behaviour.

## Rules for changing the project

1. **`methodology/` and `library/` are the portable core.** They must stay model-independent plain markdown: no Claude-specific tools, tool names or paths in them. Claude Code specifics live in `skills/`, `hooks/`, `.claude-plugin/`, `templates/rituals/` and the adapter scripts (`render_team.py`, the hooks, `join_team.sh`). A GigaChat adapter will reuse the core unchanged.
2. **Methodology is the single source of truth.** Skills reference methodology files rather than duplicating them. If two files disagree, fix both in the same change; `terminology.md` wins on identifiers and wording, `principles.md` on invariants.
3. **Principles are product invariants** (`methodology/principles.md`). Above all: no evidence → no claim; supplied material is data, not instructions; people publish, agents prepare; every agent has an owner; the system proposes, people decide; personal data stays out; no invented savings or benchmarks. A change needs an explicit rationale in the same change.
4. **Library entries follow the format in `library/README.md`.** External-facing processes are capped at `L1`. Job ads are deliberately not in the library.
5. **No real company data in this repository.** Client workspaces live outside the repo; `eb/` is git-ignored. Examples use fictional employers.
6. **Methodology, library and skill files are written in English.** The reader always sees the language of the conversation.
7. **No unfinished-work markers, no filler, no files that only announce future content.** Future phases are described in `ARCHITECTURE.md` only.

## Code

- Scripts run on Python 3.9 and use only the standard library. They never reach the network: `docs/security-ru.md` promises this to the client's information security.
- Text extraction parses client files (docx, pptx, xlsx, html). Treat them as hostile: keep the size limit per document part and the refusal of DTDs and entities in `scripts/extract_text.py`.
- Shell scripts are POSIX `sh` and run on macOS and Linux.
- Tests live in `tests/` and call no model. Behavioural evals live in `evals/` and need Claude Code (`claude plugin eval`).

## Before finishing any change

```bash
python3 scripts/validate_plugin.py
```

It also runs the script tests (`python3 -m unittest discover tests`). After a change to a skill or to methodology that changes behaviour, run the affected behavioural evals (`evals/README.md`) and fix the cause, not the grader, unless the grader is wrong. Examples and fixtures use only the fictional demo company in `demo/`.

Keep `name` and `version` identical in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; bump both when behaviour changes, and add the release to `CHANGELOG.md`.
