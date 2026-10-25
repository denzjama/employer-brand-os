---
id: funnel-analysis
domain: analytics
name: Hiring funnel analysis
name_ru: Анализ воронки найма
default_autonomy: L1
external_facing: false
---

## Purpose
Analyses funnel exports from the ATS or HCM: which sources and campaigns bring candidates, where candidates drop out, how it differs by audience and role family. Connects EB activity to hiring outcomes where the data allows it.

## Fits when
- The team has access to funnel data, or can get exports.
- The question "does employer brand help hiring?" is asked and not answered.

## Triggers
Monthly or quarterly; after a campaign.

## Inputs
Aggregated funnel exports in `eb/inbox/funnel/`; the campaign list from the content plan.

## Outputs
`eb/work/funnel-analysis/<period>.md`: conversion by stage and source, notable changes, hypotheses about causes marked as hypotheses, data gaps.

## Human checkpoint
The owner discusses findings with talent acquisition before acting.

## Suggested ritual
Monthly sync with talent acquisition.

## Metrics
Questions answered with data; decisions made from the analysis.

## Risks and limits
Works on aggregated data only; candidate-level personal data is refused. Correlation is not presented as effect.
