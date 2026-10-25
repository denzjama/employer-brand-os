---
id: employee-voice-analysis
domain: research
name: Employee voice analysis
name_ru: Голос сотрудников
default_autonomy: L1
external_facing: false
---

## Purpose
Analyses what employees say in exit and onboarding interviews, engagement and pulse surveys, and internal channels. Finds recurring themes, how they change over time, and where what employees say contradicts what the brand promises.

## Fits when
- The company runs exit or onboarding interviews or regular surveys.
- The results reach the EB team late or as a slide with three bullets.
- The team suspects a gap between the EVP and lived experience.

## Triggers
When a new batch of data lands in `eb/inbox/`; quarterly.

## Inputs
Anonymised exports in `eb/inbox/`; `eb/brand-core/evp.md`.

## Outputs
`eb/work/employee-voice-analysis/<date>-themes.md`: themes with counts over the supplied set, representative paraphrases, change against the previous period, EVP promises the data supports or contradicts.

## Human checkpoint
The owner decides what is shared and with whom. Findings about specific teams go to HR business partners, not into communication.

## Suggested ritual
Quarterly EVP health check with HR business partners.

## Metrics
Time from data arrival to analysis; number of EVP gaps found and addressed.

## Risks and limits
Works only on anonymised data; flags and stops on identifiable personal data. Counts are over the supplied set, never generalised to "employees". Verbatim quotes are not used outside the team without consent.
