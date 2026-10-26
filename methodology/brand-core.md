# Brand core

The shared memory every agent reads. It lives in `eb/brand-core/`. It records what the client says about itself as an employer and what supports it; it is not a place to create a brand.

## 1. Files

| File | Content |
|---|---|
| `evp.md` | The employer value proposition as documented: core line, pillars, target audiences, the source of each. |
| `voice.md` | Tone of voice: principles, words to use and avoid, short examples of approved copy. |
| `facts.md` | The fact registry (§4). |
| `audiences.md` | Target audiences and what is known about them, with sources. |
| `red-lines.md` | What the brand never says or does: legal, ethical and reputational limits. |
| `decisions.md` | Decisions that change communication: date, decision, who decided, why. |

Each file starts with a header line: last updated, by which step, and approval state (`DRAFT — not yet approved by the EB lead` or `Approved by <role> on <date>`).

## 2. What the core is built from

1. Supplied materials in `eb/inbox/`, read in index order.
2. The interview (`diagnosis.md`), for what the materials do not say.
3. Later, approved proposals from agents and the retro.

The builder never writes into the core what it did not find in one of these. Where materials disagree, both versions are recorded with their sources, and the disagreement goes to the confirmation round (§5).

**Duplicates and versions** (`workspace.md` §3): facts are taken from one copy of a duplicate. Of several versions of a document, the most recent approved version is the source; earlier versions are used only for facts the latest one does not contain, and a fact that changed between versions is recorded as a conflict.

### 2.1 Building the core from many materials

When the notes do not fit in one working context (as a rule of thumb, more than about 150 pages of notes, or more than 20 materials), the core is built in groups:

1. Split the materials into groups of related material (for example strategy and plans; EVP and voice; results and reports; research). Keep all versions of one document in one group.
2. Each group produces its fact rows with temporary IDs (`G1-001`, `G2-001`, …) and its EVP, voice, audience and red-line findings, in the formats of this file.
3. Merge: assign final IDs in group order; then run a conflict pass across groups: the same subject with a different number, period or wording becomes cross-referenced conflict rows; exact repeats are merged into one row with all sources.
4. Record in `decisions.md` that the core was built in groups and how they were formed.

## 3. EVP and voice

**EVP.** Record the proposition verbatim from the most recent approved document, with file and page or slide. Pillars and audiences likewise. If several versions exist, record each with its date and source and mark the conflict. If no EVP is documented, `evp.md` says so in one line. The builder does not write an EVP: creating or rewriting the EVP is out of scope for the brand core.

**Voice.** If a voice guide exists, summarise it with its source. If not, infer principles from approved external copy in the materials, label every principle `INFERENCE`, and give the copy it was inferred from. Inferred voice is a draft until the EB lead approves it.

## 4. Fact registry

`facts.md` is a table, one row per fact:

| Column | Content |
|---|---|
| ID | `F001`, `F002`, … never reused |
| Fact | One fact, written with all its anchors (`principles.md` P3) |
| Kind | `RESULT`, `TARGET`, `PLAN`, `PRACTICE`, `ESTIMATE` or `UNKNOWN` (§4.1) |
| Pillar | The EVP pillar it supports, or `—` |
| Source | File ID and location (`M03, slide 12`), or `INTERVIEW <date>` |
| Period | The period the fact describes, as the source states it |
| Status | `CONFIRMED`, `TO CONFIRM`, `EVIDENCE NEEDED`, `OUTDATED` (`terminology.md` §1) |
| Confirmed | Who confirmed and when, for `CONFIRMED` |
| Notes | Conflicts, limits on use, the reason for `OUTDATED` |

Rules:

1. **Every new fact starts as `TO CONFIRM`.** Only a person moves a fact to `CONFIRMED`. The system never does.
2. **One fact per row.** Split compound statements. Keep the source's numbers, units, approximations ("about", "up to") and modality ("plan to", "aim to").
3. **Plans and targets are not facts about the present.** "We plan to open a hub in 2026" is a `PLAN`, never "we have a hub". "+10% to the reputation index" in a strategy is a `TARGET` until a source shows it was measured. When a number's kind is not clear from the source, it is `UNKNOWN` and the confirmation round asks: "measured result or target?"
4. **Claims without support** found in the materials (a careers page says "best place to work in the industry" with nothing behind it) are recorded as `EVIDENCE NEEDED`, so agents know not to repeat them.
5. **Validity.** A number older than 12 months, or tied to a period that has ended, is flagged in Notes at the next review. It becomes `OUTDATED` when a person says so or a newer source supersedes it.
6. **What does not belong:** personal data, internal-only figures the EB lead marks as not for communication (record them in `red-lines.md` as "do not disclose: <topic>" without the figure), and opinions without an owner.

### 4.1 Kinds

| Kind | Meaning | May be stated as |
|---|---|---|
| `RESULT` | Something measured or achieved, with its period | What happened ("in 2025, …") |
| `TARGET` | A goal or KPI to reach | A goal ("we aim to …"), never as achieved |
| `PLAN` | Something intended or scheduled | An intention, with its date |
| `PRACTICE` | How things are done now: a programme, a benefit, a process | Current practice, within its scope |
| `ESTIMATE` | Someone's estimate | An estimate, with whose it is |
| `UNKNOWN` | The source does not show which of the above | Nothing, until the user answers |

### 4.2 Workspaces built before this column existed

A `facts.md` without the Kind column gets it on the next update, with `UNKNOWN` for every existing row except rows whose source text makes the kind explicit. `CONFIRMED` rows with `UNKNOWN` kind go to the next confirmation round with the single question about their kind.

## 5. Confirmation round

After building or updating the core, show the user the `TO CONFIRM` facts in batches of up to 10, grouped by pillar. For each, the user answers: confirm, correct, mark outdated, or "don't know yet". Each fact is shown with its kind; for a number of kind `UNKNOWN`, the question is whether it is a measured result or a target.

Bulk answers ("1–7 confirm") are fine because each item was shown. What does not count as confirmation: the user sending a text that contains the fact, the user saying a document is correct as a whole, or a fact appearing in several materials (`principles.md` P1). Corrections are applied with the user as the source (`INTERVIEW <date>`). Unanswered facts stay `TO CONFIRM`. Conflicts are asked about first.

The round can be paused; the remaining facts stay in the registry with their status.

## 6. Use by agents

- External-facing drafts use only `CONFIRMED` facts and cite their IDs in the draft's notes.
- Internal outputs may use `TO CONFIRM` facts, labelled as such.
- `EVIDENCE NEEDED` and `OUTDATED` facts are never stated as fact anywhere.
- An agent that needs a fact the core does not hold lists it as EVIDENCE NEEDED in its output and proposes it to the EVP guardian.
- **Before anything leaves the workspace** — an agent draft, or a text the user writes with the system's help, even an urgent one-off — the system lists every number and factual claim in it with its status and kind. A claim that is not `CONFIRMED`, or whose kind does not match how it is phrased (a target written as a result), is flagged before the user sends the text, not after.
