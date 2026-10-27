# Team assembly (Phase 2)

How the approved, validated team proposal becomes a working agent team in the shared team workspace. Input: `eb/diagnosis/team-roster.json` and the rest of the Phase 1 outputs. Output: agents, coordinator rules, ritual and pipeline commands, a write guard, a run log, and one onboarding page per owner and operator.

## 1. Readiness gate

Assembly starts by reading the "Readiness for Phase 2" part of `eb/status.md` (`workspace.md` §6) and the validation answers (`diagnosis.md` §7a).

| Item | If not ready |
|---|---|
| Security approval | Assembly does not start. Say what is missing. |
| Validation with owners | Only agents whose owner answered "yes" or "rather yes" are assembled. The others wait, listed with the reason. |
| Tool access | An agent whose owner has no access needs an operator (§6). Without one it waits. |
| Shared workspace | Assembly runs in the current folder; moving it into the shared repository is the first onboarding step (§5). |
| Confirmed facts | External-facing agents are assembled; their onboarding page and first run warn which topics have no `CONFIRMED` facts yet. |

Before generating anything, show the EB lead what will be assembled, what waits and why, and get a go-ahead.

## 2. Canonical agent description

Every agent is described once in a model-independent file, `eb/team/agents/<id>.md`. This file is the source of truth; runtime files are generated from it (§3) and never edited by hand.

When the library has a reference agent for the process (`library/agents/<library_id>.md`), the description starts from it: its method, result template, acceptance criteria, checks and limits are kept unless the client's work differs, and its "Client specifics to collect" is the checklist for the client specifics. The reference is adapted, not copied: paths, channels, names of rituals and the result headings follow the client. Without a reference the description starts from the library entry alone.

### 2.1 Header

| Field | Content |
|---|---|
| `id` | kebab-case, unique in the team; equal to the roster `id` |
| `library_id` | The library entry, or `CUSTOM` |
| `name` | Reader-facing name, in the language of the team |
| `owner` | Role (name only if the team uses names in the roster) |
| `operator` | Role of the operator, or `none` |
| `autonomy` | `L0`, `L1` or `L2`; external-facing agents are capped at `L1` (`autonomy.md`) |
| `external_facing` | `true` or `false` |
| `web_access` | `true` only for agents whose library entry reads public web pages (monitoring, competitor watch) |
| `ritual` | Where it lives in the team's week or month |
| `inputs_from` | Roster IDs, or `owner`, `lead`, `coordinator`, `brand-core`, `log` |
| `outputs_to` | The same vocabulary |
| `first_metric` | The metric the owner agreed to |
| `wave` | `WAVE 1`, `WAVE 2` |

### 2.2 Sections, in this order

1. **Purpose** — the library purpose, rewritten for this function in the client's words.
2. **Reads** — the exact brand-core files and workspace paths it reads.
3. **Produces** — the format of its result as a template, and the path: always under `eb/work/<id>/`.
4. **Method** — the steps from the task to the result, then the common failures to avoid. From the reference agent where there is one.
5. **Handoff** — what it expects from the coordinator and what it returns, in the format of `coordination.md` §1, with the acceptance criteria for this agent.
6. **Checks before handing over** — for external-facing agents: only `CONFIRMED` facts, the list of numbers with status and kind (`brand-core.md` §6), then the quality gate. For the quality gate itself: its verdicts and the retry rule (`coordination.md` §2).
7. **Never does** — the library entry's risks and limits, the invariants of `principles.md` that apply, and the client's red lines from `eb/brand-core/red-lines.md`.
8. **Client specifics** — templates, platform and contractor requirements, good examples from the materials and the interview, each with its source. Where a reference agent exists, every item of its "Client specifics to collect" is either filled with a source or listed as missing.

Descriptions written before the Method section existed stay valid; the generator accepts them and reports which ones would gain from a reference.

Every statement in "Client specifics" has a source (material ID or interview date). Nothing is invented to make the agent look complete; a missing template is listed as missing.

### 2.3 Owner confirmation

Before generation, each owner (or the EB lead for agents without a validated owner) sees "Purpose", "Never does" and "Client specifics" of their agent in plain words and confirms or corrects them. The confirmation is recorded in the file's header (`confirmed_by`, `confirmed_on`).

## 3. Generation for the runtime

A converter generates the runtime files from the canonical descriptions and the roster. It is deterministic: the same input gives the same files. The runtime adapter decides the file formats; the rules are the same for every runtime:

1. One runtime agent per canonical description, named with the `eb-` prefix so it cannot collide with other agents.
2. The agent can read the whole workspace and write only under its own `eb/work/<id>/`. Web access only if `web_access` is `true`. No tool that sends anything outside the workspace.
3. The coordinator rules (§4) are written into the runtime's project instruction file between markers, so that the client's own instructions outside the markers are kept.
4. One command per pipeline in the roster, and the ritual commands of §4.2.
5. Where the runtime allows it, the write limit is enforced technically, not only by instruction: a write by an agent outside its own folder, or by any agent into `eb/brand-core/`, is refused.
6. Every finished agent run is recorded automatically (`coordination.md` §4).
7. Regeneration never touches canonical descriptions, work, logs or the brand core.

## 4. Coordinator

The coordinator is the main conversation in the shared workspace: whoever opens the system there acts as coordinator for that session. It is a role of the session, not of a person.

### 4.1 Coordinator rules

Generated from the roster and the canonical descriptions:

- the team: agents, owners, operators, rituals, inputs and outputs;
- the pipelines, step by step;
- the handoff format and the quality-gate loop (`coordination.md` §1–§2);
- recording decisions and runs (`coordination.md` §3–§4);
- the shared repository routine (`coordination.md` §5);
- the invariants: people publish, agents prepare; the brand core is changed only by a person; no unconfirmed fact leaves the workspace.

Agents may technically be able to call other agents; the coordinator still runs the pipeline step by step, so that a person sees each step and every external output is decided in one place.

### 4.2 Commands

| Command | Purpose |
|---|---|
| One per pipeline | Starts the pipeline at its first step and asks only for the missing input |
| Weekly | The pack for the weekly team meeting: new outputs, drafts waiting for a decision, overdue items, the adoption coach's 15 minutes |
| Core review | The monthly brand-core review: the EVP guardian's proposals and a confirmation round |
| Decide | Records an owner's decision on an output (`coordination.md` §3) |
| Export | Exports a draft to a word-processor file for an owner without access to the system |
| Sync | Brings the shared repository up to date (`coordination.md` §5) |

Scheduled runs are not part of the first version: rituals are started by a person at the ritual.

## 5. Shared team workspace

The workspace becomes a shared repository in the client's own version-control system. Rules:

| In the repository | Only on the machine of the person who supplied the materials |
|---|---|
| Brand core, material index and notes | Original materials (`eb/inbox/**` except the index, inventory and notes) |
| Diagnosis, roster, canonical agents, generated runtime files, commands | Text extracts (`eb/inbox/_text/`) |
| Work, logs, retro | Personal runtime settings |
| The plugin itself, at the version the team uses (`vendor/`) | |

- The plugin is vendored: the exact code the security team approved is the code the team uses. An update is a deliberate replacement of `vendor/`.
- Each team member connects once, with the join script shipped in `vendor/` (the runtime adapter documents the command). The connection is recorded in the member's personal settings, not in the shared ones.
- **One writer per file** (`coordination.md` §5): each agent writes only its own folder; the brand core is written only by a person; runs and decisions are one file each, so two people never edit the same log file.

## 6. Owners and operators

Every agent has an owner who decides on its outputs (`principles.md` P6). If the owner has no access to the system:

- an **operator** with access runs the agent's pipelines for the owner;
- the owner receives the draft as a file in the shared workspace or as an exported document;
- the owner decides; the operator records the decision as "decided by the owner, recorded by the operator".

The operator never decides in the owner's place. The adoption coach shows the operators' load at the weekly meeting; a persistent bottleneck is a reason to request access for the owners.

## 7. Trial runs

Each pipeline is run once on a real input chosen during validation (`diagnosis.md` §7a). The result is a draft and a log entry, never a publication. The owner decides on it with the decide command, so the first decision record exists before the team starts.

A trial that fails (the agent cannot produce a usable draft) is fixed in the canonical description and run again; after two failed trials the agent waits and the reason goes to the open questions.

## 8. Onboarding

The adoption coach writes one page per owner and per operator in `eb/team/onboarding/<role>.md`, in plain words: your agents, your rituals, how to start a pipeline, how to record a decision, what the agent never does, who to ask. The page also lists the topics without confirmed facts for external-facing agents.

## 9. Waves and re-runs

The first assembly covers the first wave. Later waves are assembled after the first retro by running the assembly again: it adds new agents and never changes existing ones without an approved proposal (`autonomy.md` §2, `principles.md` P7).

## 10. Outputs and status

| Output | Path |
|---|---|
| Canonical agents | `eb/team/agents/<id>.md` |
| Team roster for people | `eb/team/roster.md` |
| Onboarding pages | `eb/team/onboarding/` |
| Runtime files | generated by the adapter |
| Trial results | `eb/work/<id>/` and `eb/log/` |

`eb/status.md`: Phase 2 complete, the agents assembled and waiting, the date of the first retro.
