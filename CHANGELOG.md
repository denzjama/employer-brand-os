# Changelog

## 0.3.1 — packaging for the first clients

- `docs/guide-ru.md`: a guide for the EB lead without a technical background: what the system does, what is needed, installation, the four phases, the rules that cannot be switched off, what to do when something goes wrong.
- `docs/security-ru.md`: a brief for the client's information security: data flows, what stays on the machine, built-in limits and how each is enforced, version control of the vendored plugin, steps before a pilot.
- README: requirements and links to both guides.
- Validator: no client workspace and no machine-specific paths in the published files.
- Checked before publishing: no pilot data or machine paths in any commit; installation from a fresh clone; the first run in an empty folder gives the data notice and creates nothing before consent.

## 0.3.0 — quality gate on the auditor method, and the retro (Phases 3–4)

- `methodology/quality.md`: the quality gate checks a draft with the Employer Brand Auditor method: claim extraction, fact check with status, kind and anchors, links between facts, verbatim quotes, quarantine of unconfirmed facts, the genericity test on central claims, the auditor's red flags that apply to drafts (with their IDs), and a verdict. Every issue has a code; every check is saved with a fixed header (agent, draft, attempt, verdict) so it can be counted.
- The quality-gate reference agent follows the method; `render_team.py` embeds the method in the generated quality-gate agent, so it holds without `vendor/`.
- Decision records gain the gate check the owner saw, facts the owner added, and an explicit "no reason given" (`record_decision.py --check --facts-added --no-reason`; `/decide` asks for them).
- `methodology/retro.md` and the `retro` skill (Phase 4): every two weeks the iteration is counted, signals S1–S10 found, at most seven proposals written with their evidence, decisions recorded, and only approved proposals applied. External-facing agents are never proposed above L1.
- `scripts/retro_stats.py`: deterministic iteration statistics and countable signals from the logs and gate checks, including checks written before the fixed header.
- `demo/retro/`: four weeks of fictional team logs with nine planted signals and traps (answer key R1–R9), built by `build_logs.py`.
- Evals: `quality-gate-traps` (a story draft with eight planted problems against five confirmed facts) and `retro` (the answer key). Tests: retro statistics on the demo logs, decision records, the gate method in the runtime agent.
- Validator: issue codes agree between `quality.md`, `terminology.md` and `retro_stats.py`; the demo logs match their builder.

## 0.2.2 — reference agents and pipeline library

- `library/agents/`: ten reference agents for the most common processes (quality gate, employee stories, review monitoring, review responses, project briefs, channel adaptation, content plan, CHRO report, EVP guardian, adoption coach). Each gives the method step by step, the result template, acceptance criteria, checks, limits, the failures owners usually reject, and what to collect from the client. Assembly starts every canonical description from its reference, so agent quality no longer depends on how the model expands a short library entry.
- `library/pipelines/`: eight typical pipelines (employee story, review to response, project brief, one piece to all channels, monthly plan, CHRO report, brand-core loop, learning loop). The team proposal starts its pipelines from them; roster pipelines keep a `library_id`.
- Canonical agent descriptions gain a Method section between Produces and Handoff. Descriptions without it, written by 0.2.1, stay valid; `render_team.py --check` lists the ones that have a reference to start from.
- `render_team.py` refuses a pipeline in which an external-facing agent hands a draft to a person without the quality gate.
- Validator: format of reference agents and pipelines, steps that refer only to the pipeline's agents and roles, the quality gate in every external pipeline, the decision recorded at the end.
- Evals: the `team-assembly` case checks the reference-based descriptions and an honest report of the steps the eval sandbox blocks (runtime files in `.claude/`, `.git`); `no-push` matches commands, not text the run read; the snapshot scaffold restores empty folders that git drops.
- The adoption coach entry reads the logs from `eb/log/runs/` and `eb/log/decisions/`, as the workspace has them.

## 0.2.1 — demo company and tests

- `demo/`: the fictional employer «Полярная гавань» — materials in every format seen in the pilot, built from text sources by `demo/build_materials.py`; the EB lead's interview answers; an answer key of 15 traps; snapshots of a full end-to-end run (brand core, diagnosis, team assembly) with the system's final messages.
- `tests/`: deterministic script tests (no model calls), also run by the validator.
- `evals/`: behavioural cases for `claude plugin eval` — prompt injection, brand-core traps, pre-send check, diagnosis traps, team assembly — starting from fresh materials or the demo snapshots.
- New workspaces get a block of workspace rules in `CLAUDE.md` (facts only from the registry, targets never as results, numbers listed before anything leaves, material is data, people publish), so the invariants hold even when no skill runs. Found by the pre-send eval: an urgent request was answered without any skill.
- New workspaces get empty `.claude/agents/` and `.claude/skills/`, so agents generated in Phase 2 are picked up without a restart. Found by the demo run. The assembly skill no longer imitates missing agents with general-purpose subagents.
- Inventory: of byte-identical files, the one with the shortest name is the original.

## 0.2.0 — Phase 2: team assembly

- New skill `team-assembly`: readiness gate, canonical agent descriptions confirmed by their owners, generation, shared repository, trial runs, onboarding pages.
- New methodology: `assembly.md` (Phase 2) and `coordination.md` (handoffs, quality-gate loop with at most three attempts, one file per decision and per run, shared repository routine).
- New `scripts/render_team.py`: vendors the plugin into `vendor/eb-marketplace/`, generates `.claude/agents/eb-<id>.md`, the coordinator block in `CLAUDE.md`, one command per pipeline, the ritual commands, `eb/team/roster.md` and a `.gitignore` that keeps original materials out of the repository. Deterministic; never touches work, logs or the brand core.
- New plugin hooks: `guard_write.py` lets a team agent write only its own `eb/work/<id>/` and keeps every subagent out of the brand core, team files and decision log; `log_run.py` logs every team-agent run. Both do nothing outside an Employer Brand OS workspace.
- New `scripts/record_decision.py`, `scripts/export_docx.py` (standard library), and `scripts/join_team.sh` for a colleague to connect once.
- Ritual command templates: `/weekly`, `/core-review`, `/decide`, `/export-docx`, `/eb-sync`.
- Operators: an owner without access decides; an operator runs the agent and records the decision.
- Validator: Phase 2 files, hook references, ritual templates, and a deterministic sample assembly.

## 0.1.1 — fixes after the first pilot

The first real diagnosis of an Employer Brand function (51 materials, six interview blocks, a 27-process map) left 25 notes on the plugin. This release addresses those that concern Phase 1.

**Facts**
- A fact is confirmed only by an explicit answer about that fact. A text the user already sent to colleagues does not confirm its numbers.
- The fact registry has a Kind column: result, target, plan, practice, estimate, or unclear. A target is never written as a result; numbers of unclear kind are asked about first.
- Every number in anything that leaves the workspace is listed with its status and kind before the user sends it.
- Minors and credentials found in materials are covered by the personal-data rules.
- Consent to the data notice is given in the conversation that reads the files; a relayed consent is asked again.
- A conflict with the client's security policy is said once, recorded, and left to the user to decide.

**Intake**
- New `scripts/inventory.py`: sizes, pages, PDF text layer (scans), byte-identical duplicates, file names in NFD or with non-breaking spaces.
- `scripts/extract_text.py` reads HTML, keeps scripted counter values (`data-*` attributes), drops inline images and scripts, names extracts by NFC-normalised path.
- Index columns for format, pages and duplicates or versions; a Decisions section for sensitive files, credentials and embedded instructions.
- Extracts of sensitive files are deleted until the user decides.
- Note batches are sized by volume (about 100 pages), not by file count; the core is built in groups and merged when the notes do not fit in one context.

**Diagnosis**
- Interview blocks can be partly done while answers from team leads are awaited; `eb/status.md` has "Waiting for" and "Readiness for Phase 2".
- Volume can be scored from frequency when nobody knows the hours.
- Full tie-break order for the first wave.
- Every proposed agent has tool access (or an operator), inputs and outputs; the first wave is described as 3 to 5 pipelines.
- New `eb/diagnosis/team-roster.json` for Phase 2, in the format of `templates/team-roster.sample.json`.
- New validation step with the future owners before approval (`eb/diagnosis/validation.md`).
- Block D asks about tool access; Block F looks for the root cause of resistance.
- One-off requests during the interview are handled, logged and the interview resumes.
- New overview page: `templates/overview.html` and `scripts/build_overview.py`, light by default with a dark switch, data rendered as text only.

**Library**
- Four new processes: design production, ambassador programme, recruitment campaigns, contractor and paperwork operations. Two new domains: campaigns and operations.

**Not in this release:** the shared team workspace and team assembly (Phase 2).

## 0.1.0

First version: architecture, methodology, a library of 17 processes, and the Phase 1 skills `eb-setup`, `brand-core` and `function-diagnosis`.
