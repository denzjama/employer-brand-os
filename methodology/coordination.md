# Coordination

How work moves through the agent team: handoffs, the quality-gate loop, decision and run records, and the shared repository routine. Used by the coordinator from Phase 2 on.

## 1. Handoff

The coordinator passes a task to an agent, and the agent returns its result, in one format:

| Field | Content |
|---|---|
| Pipeline | The pipeline and the step |
| From → To | Roster IDs, or `owner`, `lead`, `coordinator` |
| Task | What is needed, in one or two sentences |
| Done so far | Results of earlier steps, with paths |
| Use | Brand-core files and fact IDs to rely on |
| Acceptance criteria | From the agent's canonical description, plus anything the owner added |
| Goes next to | Who receives the result |

The agent returns the same fields plus: the result path, which criteria are met, and what it could not do and why.

## 2. Quality-gate loop

Every external-facing draft goes to the quality gate before its owner sees it.

1. The gate checks the draft with the method of `quality.md` and returns `PASS`, `PASS WITH FIXES` or `BLOCKED` with the issues, their codes and the unmet criteria. Every check is saved in its own file, so that the retro can count verdicts, attempts and issue codes per agent.
2. On `BLOCKED`, the draft goes back to the agent with the issues only. The agent fixes those issues and adds nothing new.
3. At most three attempts. After the third, the draft goes to the owner with the history of attempts, marked as not passed. Such cases are the retro's main material.
4. On `PASS WITH FIXES`, the owner sees the draft with the suggested fixes; the agent does not apply them on its own.

## 3. Decision records

Every human decision on an output is recorded in its own file, `eb/log/decisions/<date>-<time>-<agent>.md`:

| Field | Content |
|---|---|
| Date and time | |
| Output | Path of the draft |
| Agent | Roster ID |
| Decision | `ACCEPTED`, `EDITED`, `REJECTED` (`terminology.md` §7) |
| Substantive | For `EDITED`: whether a fact, a conclusion or the structure changed (`autonomy.md` §3) |
| Reason | In the decider's words |
| Check | Path of the quality-gate check the owner saw, if the draft passed the gate |
| Facts added | Facts the owner added or corrected while editing, in the owner's words; empty if none |
| Decided by | The owner's role; "via operator <role>" when an operator recorded it |

One file per decision, so that two people never edit the same file. A rejection is recorded with its reason like any other decision; a rejection without a reason is a question for the retro, not a reason to skip the record.

## 4. Run records

Every finished agent run is recorded in its own file, `eb/log/runs/<date>-<time>-<agent>.md`: the agent, the time, its final message, and the paths it wrote. Runs are recorded automatically where the runtime allows it; otherwise the coordinator records them.

## 5. Shared repository routine

The shared workspace is a repository in the client's version-control system (`assembly.md` §5).

1. **Before starting work:** bring the workspace up to date.
2. **One writer per file:** an agent writes only `eb/work/<its id>/`; only a person changes `eb/brand-core/`; logs are one file per entry; team and runtime files are changed only by assembly or by an approved retro proposal.
3. **After each decision:** record the change with a message that says what happened in plain words ("Habr article draft accepted by the IT brand lead"), and share it.
4. **On a conflict:** never overwrite someone else's change. Stop, show the person what conflicts, and let them decide.
5. Original materials and text extracts never enter the repository.

## 6. Before anything leaves the workspace

Whatever the pipeline, before the owner sends or publishes an output: every number and factual claim in it is listed with its status and kind (`brand-core.md` §6), and the owner sees the list together with the draft.
