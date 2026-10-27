# Demo: «Полярная гавань»

A complete, fictional Employer Brand function to show and test Employer Brand OS end to end. The company, its people, numbers and documents are invented. Any resemblance to a real employer is accidental.

**ООО «Полярная гавань»** — a port operator in the fictional city of Severogavan: a container terminal and a bulk-cargo terminal, 1,800 employees, an Employer Brand team of six. Its main hiring problem is crane operators.

## What is here

| Path | What |
|---|---|
| `source/` | The materials as reviewable text: strategy deck, two EVP versions, 2025 results, a staff newsletter, team processes, an engagement survey, an exit-interview export, review export, a students' page, an onboarding plan, a voice guide |
| `build_materials.py` | Builds `materials/` from `source/`: pptx, docx, xlsx, pdf, html, csv, md, a byte-identical copy and a file name in NFD. Deterministic. Run: `python3 demo/build_materials.py` |
| `materials/` | The built materials, as a client would drop them into `eb/inbox/` |
| `interview.md` | The EB lead's answers to the six interview blocks, so the diagnosis can run without a live person |
| `answer-key.md` | The 15 traps built into the materials and what the system must do with each |
| `run/` | Snapshots of a full end-to-end run, one per stage, with the system's final message |

## The end-to-end run

Each stage was run headless (`claude -p`) with the plugin installed, as the EB lead who cannot answer live questions:

1. `run/stage-1-brand-core/` — setup, intake of the 13 files, notes, brand core.
2. `run/stage-2-diagnosis/` — interview from `interview.md`, AI map, team proposal with pipelines, roster, validation questionnaire, CHRO summary, overview page.
3. `run/stage-3-assembly/` — team assembly, a trial pipeline run, onboarding.

Each snapshot holds the whole workspace (`workspace/`) and the run's final message (`summary.md`). The stage-3 snapshot leaves out `vendor/` and `join_team.sh` (a copy of this plugin) and the local git history; `scripts/render_team.py` recreates them. The snapshots were made with version 0.2.1, before reference agents: the stage-3 agent descriptions have no Method section, which also shows that such descriptions keep working. The behavioural evals start from these snapshots, so later stages can be tested without repeating earlier ones.

To show the demo, open `run/stage-2-diagnosis/workspace/eb/diagnosis/overview.html` in a browser, then walk through the workspace files of each stage.
