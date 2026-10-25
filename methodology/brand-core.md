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

## 3. EVP and voice

**EVP.** Record the proposition verbatim from the most recent approved document, with file and page or slide. Pillars and audiences likewise. If several versions exist, record each with its date and source and mark the conflict. If no EVP is documented, `evp.md` says so in one line. The builder does not write an EVP: creating or rewriting the EVP is out of scope for the brand core.

**Voice.** If a voice guide exists, summarise it with its source. If not, infer principles from approved external copy in the materials, label every principle `INFERENCE`, and give the copy it was inferred from. Inferred voice is a draft until the EB lead approves it.

## 4. Fact registry

`facts.md` is a table, one row per fact:

| Column | Content |
|---|---|
| ID | `F001`, `F002`, … never reused |
| Fact | One fact, written with all its anchors (`principles.md` P3) |
| Pillar | The EVP pillar it supports, or `—` |
| Source | File ID and location (`M03, slide 12`), or `INTERVIEW <date>` |
| Period | The period the fact describes, as the source states it |
| Status | `CONFIRMED`, `TO CONFIRM`, `EVIDENCE NEEDED`, `OUTDATED` (`terminology.md` §1) |
| Confirmed | Who confirmed and when, for `CONFIRMED` |
| Notes | Conflicts, limits on use, the reason for `OUTDATED` |

Rules:

1. **Every new fact starts as `TO CONFIRM`.** Only a person moves a fact to `CONFIRMED`. The system never does.
2. **One fact per row.** Split compound statements. Keep the source's numbers, units, approximations ("about", "up to") and modality ("plan to", "aim to").
3. **Plans are not facts about the present.** "We plan to open a hub in 2026" is recorded as a plan, with its date, never as "we have a hub".
4. **Claims without support** found in the materials (a careers page says "best place to work in the industry" with nothing behind it) are recorded as `EVIDENCE NEEDED`, so agents know not to repeat them.
5. **Validity.** A number older than 12 months, or tied to a period that has ended, is flagged in Notes at the next review. It becomes `OUTDATED` when a person says so or a newer source supersedes it.
6. **What does not belong:** personal data, internal-only figures the EB lead marks as not for communication (record them in `red-lines.md` as "do not disclose: <topic>" without the figure), and opinions without an owner.

## 5. Confirmation round

After building or updating the core, show the user the `TO CONFIRM` facts in batches of up to 10, grouped by pillar. For each, the user answers: confirm, correct, mark outdated, or "don't know yet". Corrections are applied with the user as the source (`INTERVIEW <date>`). Unanswered facts stay `TO CONFIRM`. Conflicts are asked about first.

The round can be paused; the remaining facts stay in the registry with their status.

## 6. Use by agents

- External-facing drafts use only `CONFIRMED` facts and cite their IDs in the draft's notes.
- Internal outputs may use `TO CONFIRM` facts, labelled as such.
- `EVIDENCE NEEDED` and `OUTDATED` facts are never stated as fact anywhere.
- An agent that needs a fact the core does not hold lists it as EVIDENCE NEEDED in its output and proposes it to the EVP guardian.
