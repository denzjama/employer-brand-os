# Retro (Phase 4)

How the team learns from its own work. Every two weeks the retro reads what the agents did and what people decided about it, finds the signals that something should change, and turns them into proposals. People decide on every proposal; only approved proposals change agents, the brand core, rituals or autonomy (`principles.md` P7).

## 1. Rhythm and inputs

- **Iteration:** two weeks. The first retro is two weeks after the first trial run (`assembly.md` §10).
- **Who:** the EB lead runs it, with the owners of the agents that have proposals. The retro is a role of the session, like the coordinator: whoever runs it in the shared workspace prepares the material and records the decisions.
- **Inputs:** the run records (`eb/log/runs/`), the decision records (`eb/log/decisions/`), the quality-gate checks (`eb/work/quality-gate/`), the one-off request log (`eb/log/adhoc.md`), the adoption coach's pulses (`eb/work/adoption-coach/`), the roster and canonical descriptions (`eb/team/`), and earlier retros and proposals (`eb/retro/`).

## 2. Iteration statistics

Counted from the records, not estimated. For each agent:

| Measure | From |
|---|---|
| Runs, and the date of the last run | Run records |
| Decisions: accepted, edited (substantive or not), rejected | Decision records |
| Rejections without a reason | Decision records |
| Facts the owner added or corrected | Decision records |
| Outputs in a row accepted without a substantive edit, up to the latest decision | Decision records, across iterations |
| Gate checks, first-attempt passes, drafts not passed after three attempts | Quality-gate checks |
| Issue codes by count | Quality-gate checks |
| Decisions on drafts that passed the gate but were rejected or substantively edited | Decision records with their check |

For the team: one-off requests in the iteration and before it, grouped by the library process they resemble. Time saved is reported only as owners reported it (P10).

## 3. Signals and proposals

| # | Signal | Threshold | Proposal |
|---|---|---|---|
| S1 | Owners edit or reject one agent's outputs for the same reason | 3 or more substantive edits or rejections in the iteration whose reasons point to the same part of the work | `AGENT CHANGE`: the exact change to the agent's canonical description (Method, Checks, Never does or Client specifics) |
| S2 | Owners add or correct facts while editing | Any | `FACT`: the fact, its source (the decision record and the owner), its kind, for confirmation by a person (`brand-core.md` §5) |
| S3 | A one-off request recurs | 3 or more requests resembling the same process | `NEW AGENT` for the next wave, or `RITUAL` if an existing agent covers it |
| S4 | Outputs are accepted without substantive edits | As `autonomy.md` §3 | `AUTONOMY` up. Never above `L1` for an external-facing agent |
| S5 | Outputs are rejected | 2 or more rejections in the iteration, or the owner asks | `AUTONOMY` down, together with the cause found under S1 |
| S6 | An agent is not run | No run in two iterations | `ASK OWNER`: is it not needed, inconvenient, or not built into a ritual? Never a removal without the owner's answer |
| S7 | The gate keeps finding the same issue in one agent's drafts | One issue code 3 or more times in the iteration, or any draft not passed after three attempts | `AGENT CHANGE` aimed at that issue (a Method step, a check, a client specific) |
| S8 | The gate missed what the owner caught | A draft with `PASS` or `PASS WITH FIXES` rejected or substantively edited for a fact, a quote, an anchor, personal data or a red line | `GATE CHANGE`: the check, stock phrase or client specific the gate lacked |
| S9 | Rejections without a reason | Any | `ASK OWNER`: what was wrong. A rejection without a reason is not read as a verdict on the agent |
| S10 | The adoption coach found a real execution problem | A concern with that root cause in the pulses | `AGENT CHANGE` or `RITUAL`, with the concern in aggregate |

Rules:

- Every proposal cites its evidence: the record files and the owners' reasons in their words. A proposal without evidence is not made.
- One proposal per signal and target. When signals point to the same change, merge them.
- At most seven proposals per retro, ranked by what they unblock: blocked external drafts first, then owners' time, then autonomy.
- Proposals are about agents, rituals, facts and autonomy, never about people. Usage is not performance.
- Silence is not acceptance (`principles.md` P2): few decisions mean little evidence, and the retro says so instead of proposing a change.

## 4. Proposals

One file per proposal, `eb/retro/proposals/<date>-<nn>-<slug>.md`:

| Field | Content |
|---|---|
| `id` | `<date>-<nn>` |
| `type` | `AGENT CHANGE`, `FACT`, `NEW AGENT`, `RITUAL`, `AUTONOMY`, `GATE CHANGE`, `ASK OWNER` |
| `target` | Roster ID, a brand-core file, a ritual, or `team` |
| `signal` | S1–S10 |
| `status` | `PROPOSED`, `APPROVED`, `REJECTED`, `APPLIED` |
| `approver` | Who decides (§6) |
| `decided_by`, `decided_on` | Filled when decided |

Sections: **Evidence** (record paths, counts, the owners' reasons quoted verbatim), **Proposed change** (for an agent: the exact text to add, replace or remove in the canonical description; for autonomy: from and to; for a fact: wording, kind, source), **Expected effect and how the next retro checks it** (a measure from §2), **Decision** (filled at the retro: the decision and the reason in the decider's words).

## 5. The retro report

`eb/retro/<date>-retro.md`, read at the retro meeting, in plain words:

1. The iteration in numbers: the statistics of §2, one row per agent.
2. What changed since the last retro: each applied proposal and its measure before and after. An effect that cannot be measured yet is said so.
3. The proposals, ranked, one paragraph each, with the decision each needs and from whom.
4. Questions for owners (`ASK OWNER`).
5. After the meeting: the decisions taken.

## 6. Who decides

| Type | Approver |
|---|---|
| `AGENT CHANGE` | The agent's owner, with the EB lead |
| `GATE CHANGE` | The EB lead |
| `FACT` | A person confirms the fact explicitly (`brand-core.md` §5); a decision record is the source, not the confirmation |
| `AUTONOMY` | The EB lead (`autonomy.md` §2) |
| `NEW AGENT`, `RITUAL` | The EB lead; a new agent is added by the next assembly run (`assembly.md` §9) |
| `ASK OWNER` | The owner answers; the answer may become a proposal at the next retro |

The decision and its reason are written into the proposal. An operator records an owner's decision as the owner's (`assembly.md` §6).

## 7. Applying approved proposals

- Only a proposal with status `APPROVED` is applied. Applying is done by a person, or by the session at that person's explicit go-ahead.
- `AGENT CHANGE`, `GATE CHANGE`, `AUTONOMY`: the canonical description is changed exactly as approved, its header lists the proposal ID under `revisions`, and the runtime files are regenerated (`assembly.md` §3). Nothing else in the description changes.
- `FACT`: goes into the brand-core confirmation round; it is written to the registry only by a person.
- `NEW AGENT`, `RITUAL`: enter the next assembly run or the ritual list.
- After applying, the status becomes `APPLIED`, with the date. The next retro checks the expected effect.

## 8. What the retro never does

- Applies a change that was not approved, or changes its own rules.
- Evaluates, ranks or names people; reports concerns only in aggregate.
- Invents an effect, a time saving or a trend that the records do not show (P10).
- Treats an owner's added fact as confirmed (P1).
- Proposes an external-facing agent above `L1`, or any change that lets an agent publish (P5).
