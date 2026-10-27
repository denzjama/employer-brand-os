# Employer Brand OS

**A team of AI agents for your Employer Brand function, built around your processes, your people and your rituals.**

Employer Brand OS is a Claude Code plugin. It diagnoses how your EB function works, decides with you where agents take the work, where they assist and where people stay in charge, and proposes an agent team with a human owner and a ritual for every agent. It is the next step after [Employer Brand Auditor](https://github.com/denzjama/employer-brand-auditor) and keeps its rule: **no evidence → no claim.**

Status: **v0.2.1 — Phase 1 (diagnosis) and Phase 2 (team assembly).** The adaptation loop (retro) is designed in [`ARCHITECTURE.md`](ARCHITECTURE.md) and comes next.

## Install

```bash
claude plugin marketplace add denzjama/employer-brand-os
```

```bash
claude plugin install employer-brand-os@employer-brand-os
```

Open Claude Code in an empty folder for your workspace (not inside the plugin) and write:

```text
Подключи Employer Brand OS
```

## What Phase 1 gives you

1. **Workspace and data notice.** The system tells you what is sent to the model provider before it reads anything.
2. **Brand core.** Your materials are read once and turned into a sourced memory: EVP, voice, a fact registry where only you can mark a fact as confirmed, audiences, red lines.
3. **Interview.** Six short blocks with the EB lead. The system asks only what your materials did not answer, and you can stop and resume any time.
4. **AI map of the function.** Every process scored and placed in one of three zones: agent-led, person-led with an agent, stays with people.
5. **Agent team proposal.** Waves, an owner, a ritual, a starting autonomy level and a first metric for each agent, and the pipelines that connect the agents into one system. Checked with the future owners before approval.
6. **One-page summary for the CHRO and an overview page.** No invented savings: current effort as your team estimates it, and how the pilot will measure the effect. The overview page is a local file, light by default, that shows how a task travels through the agent team.

## What Phase 2 gives you

1. **A shared team workspace** in your own git, with the plugin vendored inside it. Original materials stay on your machine; the team works from notes and the brand core. Each colleague joins once with `sh join_team.sh`.
2. **One agent per approved process**, each described once in a model-independent file and confirmed by its owner, then generated for Claude Code. Every agent can write only its own folder; the brand core is protected by a hook, not only by an instruction.
3. **A coordinator** (`CLAUDE.md`) and **commands**: one per pipeline, plus `/weekly`, `/core-review`, `/decide`, `/export-docx`, `/eb-sync`.
4. **Owners and operators.** An owner without Claude gets drafts as files or Word documents and decides; an operator runs the agent and records the decision.
5. **Logs that feed the retro:** every agent run is logged automatically, every human decision with its reason.

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
| [`library/`](library/) | Catalogue of Employer Brand processes that agents are built from |
| [`skills/`](skills/) | Claude Code skills: `eb-setup`, `brand-core`, `function-diagnosis`, `team-assembly` |
| [`hooks/`](hooks/) | Write guard and run log for team workspaces |
| [`demo/`](demo/README.md) | A fictional employer with full materials, 15 built-in traps, and snapshots of an end-to-end run |
| [`tests/`](tests/) · [`evals/`](evals/README.md) | Script tests (no model calls) and behavioural evals for `claude plugin eval` |
| [`templates/`](templates/) | Overview page, team roster format, canonical agent sample, ritual commands |
| [`scripts/`](scripts/) | Workspace setup, inventory, text extraction (docx, pptx, xlsx, html), overview builder, validator |

Licensed under the [MIT License](LICENSE).
