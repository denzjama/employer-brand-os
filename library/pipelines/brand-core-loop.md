---
id: brand-core-loop
name: Brand-core loop
name_ru: Петля бренд-ядра
agents: evp-guardian
external_facing: false
---

## Purpose
Shows how a correction to the brand core reaches every agent: the guardian collects what is stale, contradictory or missing, a person decides and changes the core, and every next run of every agent uses the new version.

## Fits when
Always: every team has a brand core, and the diagnosis requires one pipeline that shows this loop.

## Trigger
The monthly brand-core review; new material in the inbox; a fact blocked repeatedly by the quality gate.

## Steps

| From | To | What |
|---|---|---|
| log | evp-guardian | Decisions and blocked claims that mention facts |
| coordinator | evp-guardian | New materials and the review date |
| evp-guardian | lead | Review agenda: proposed changes, contradictions, facts to confirm |
| lead | brand-core | Confirmed facts and approved changes, written by a person |
| brand-core | coordinator | New version used by every next run |
| lead | log | Decisions on the proposals |

## Decision
The EB lead approves changes to the EVP, voice and red lines; facts move to confirmed only by a person's explicit answer.

## Variants
- Without an EVP guardian in the wave, the coordinator prepares the same agenda from the quality-gate checks at the review.

## Risks and limits
No agent writes to the brand core. A newer document is not a confirmation; contradictions are questions for the lead.
