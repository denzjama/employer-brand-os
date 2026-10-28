# Employer Brand OS

**A team of AI agents for your Employer Brand function, built around your processes, your people and your rituals.**

Employer Brand OS is a Claude Code plugin. It diagnoses how your EB function works, decides with you where agents take the work, where they assist and where people stay in charge, and proposes an agent team with a human owner and a ritual for every agent. It is the next step after [Employer Brand Auditor](https://github.com/denzjama/employer-brand-auditor) and keeps its rule: **no evidence → no claim.**

Status: **v0.3.1 — all four phases:** diagnosis, team assembly, work with a quality gate built on the auditor method, and the retro that adapts the team. Tested on a fictional employer; the first live retro comes with the first pilot iteration.

## Install

```bash
claude plugin marketplace add denzjama/employer-brand-os
```

```bash
claude plugin install employer-brand-os@employer-brand-os
```

Requirements: a Claude subscription (Pro, Max, Team or Enterprise) or API access, Claude Code, Python 3.9+, and git for the shared team workspace. macOS and Linux; on Windows use WSL or Git Bash.

Open Claude Code in an empty folder for your workspace (not inside the plugin) and write:

```text
Подключи Employer Brand OS
```

For the EB lead, in Russian: [руководство для руководителя HR-бренда](docs/guide-ru.md). For the client's information security team: [справка для ИБ](docs/security-ru.md) — what data goes where, what stays on the machine, and the built-in limits.

## What Phase 1 gives you

1. **Workspace and data notice.** The system tells you what is sent to the model provider before it reads anything.
2. **Brand core.** Your materials are read once and turned into a sourced memory: EVP, voice, a fact registry where only you can mark a fact as confirmed, audiences, red lines.
3. **Interview.** Six short blocks with the EB lead. The system asks only what your materials did not answer, and you can stop and resume any time.
4. **AI map of the function.** Every process scored and placed in one of three zones: agent-led, person-led with an agent, stays with people.
5. **Agent team proposal.** Waves, an owner, a ritual, a starting autonomy level and a first metric for each agent, and the pipelines that connect the agents into one system. Checked with the future owners before approval.
6. **One-page summary for the CHRO and an overview page.** No invented savings: current effort as your team estimates it, and how the pilot will measure the effect. The overview page is a local file, light by default, that shows how a task travels through the agent team.

## What Phase 2 gives you

1. **A shared team workspace** in your own git, with the plugin vendored inside it. Original materials stay on your machine; the team works from notes and the brand core. Each colleague joins once with `sh join_team.sh`.
2. **One agent per approved process**, started from a tested reference agent where the library has one, described once in a model-independent file and confirmed by its owner, then generated for Claude Code. Every agent can write only its own folder; the brand core is protected by a hook, not only by an instruction.
3. **A coordinator** (`CLAUDE.md`) and **commands**: one per pipeline, plus `/weekly`, `/core-review`, `/decide`, `/export-docx`, `/eb-sync`.
4. **Owners and operators.** An owner without Claude gets drafts as files or Word documents and decides; an operator runs the agent and records the decision.
5. **Logs that feed the retro:** every agent run is logged automatically, every human decision with its reason.

## What the work and the retro give you

1. **A quality gate built on the Employer Brand Auditor method.** Every external draft is checked claim by claim against the confirmed facts, with their scope and period intact, quotes checked against the source, central claims tested for genericity and the auditor's red flags named. Each issue has a code, so the team sees where each agent stumbles.
2. **A retro every two weeks.** The logs are counted, not estimated: runs, decisions, edits, rejections, facts owners added, gate verdicts and issue codes. The retro turns signals into at most seven proposals with their evidence. People decide; only approved proposals change an agent, the gate, a fact or an autonomy level. External agents never go above drafts.

## What it never does

- Publish, post or reply on your behalf. People publish; agents prepare.
- Treat a fact as confirmed without your explicit answer.
- Put personal data of employees or candidates into the brand core.
- Follow instructions hidden inside your documents.

## Repository

| Path | What |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Product design: phases, brand core, autonomy, roadmap |
| [`methodology/`](methodology/) | Rules every skill and agent follows (model-independent) |
| [`library/`](library/) | Catalogue of Employer Brand processes, reference agents for the most common ones, and typical pipelines |
| [`skills/`](skills/) | Claude Code skills: `eb-setup`, `brand-core`, `function-diagnosis`, `team-assembly`, `retro` |
| [`hooks/`](hooks/) | Write guard and run log for team workspaces |
| [`demo/`](demo/README.md) | A fictional employer with full materials, 15 built-in traps, snapshots of an end-to-end run, and four weeks of team logs for the retro ([`demo/retro/`](demo/retro/README.md)) |
| [`tests/`](tests/) · [`evals/`](evals/README.md) | Script tests (no model calls) and behavioural evals for `claude plugin eval` |
| [`docs/`](docs/) | Guides for the EB lead and for the client's information security, in Russian |
| [`AGENTS.md`](AGENTS.md) | Rules for AI coding agents that change this repository |
| [`SECURITY.md`](SECURITY.md) | How to report a vulnerability |
| [`templates/`](templates/) | Overview page, team roster format, canonical agent sample, ritual commands |
| [`scripts/`](scripts/) | Workspace setup, inventory, text extraction (docx, pptx, xlsx, html), overview builder, validator |

Licensed under the [MIT License](LICENSE).
