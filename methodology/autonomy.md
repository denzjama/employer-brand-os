# Autonomy

How much an agent may do without a person. Set per agent in `eb/team/roster.md`.

## 1. Levels

| Level | The agent may | A person must |
|---|---|---|
| `L0` assistant | Answer and draft in the conversation when asked. | Start every run; decide everything. |
| `L1` drafts | Run on a ritual or schedule; read the workspace; write drafts to `eb/work/<process>/`. | Approve, edit or reject every output before it is used. |
| `L2` internal actions | Everything in L1, plus update internal artefacts that only the EB team reads: digests, plans, backlogs, its own working files; propose changes to the brand core. | Approve every change to the brand core, everything external, and every change to the agent itself. |

## 2. Invariants

1. **No level allows external action.** Publishing, posting, replying, emailing or messaging outside the workspace is always done by a person (`principles.md` P5).
2. **External-facing processes are capped at `L1`.** A process with `external_facing: true` in the library never runs at `L2`.
3. **The brand core is changed only by a person.** At any level the agent proposes; a person applies or approves.
4. **Raising a level is a proposal.** Only the retro may propose it, and only the EB lead approves it.

## 3. When the retro may propose a change

| Change | Condition |
|---|---|
| `L0` → `L1` | The agent was run by hand at least 4 times in two iterations for the same recurring task. |
| `L1` → `L2` | Internal-only process; the last 10 outputs were accepted without substantive edits. |
| Lower a level | Two or more outputs in an iteration were rejected, or the owner asks. |

"Substantive edit" means the owner changed a fact, a conclusion or the structure, not wording only. The owner's decision record (`workspace.md` §5) says which.
