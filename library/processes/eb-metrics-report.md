---
id: eb-metrics-report
domain: analytics
name: EB metrics and CHRO report
name_ru: Метрики EB и отчёт для CHRO
default_autonomy: L1
external_facing: false
---

## Purpose
Assembles the function's monthly or quarterly report for the CHRO from the data the team already has: reputation, reach, funnel, projects delivered, effect of the agent team. Short, comparable period to period, every number with its source.

## Fits when
- The function reports to the CHRO or leadership regularly.
- The report is assembled by hand from several sources each time.

## Triggers
Monthly or quarterly schedule.

## Inputs
Exports in `eb/inbox/stats/`; digests and reviews in `eb/work/`; `eb/log/` for the effect of the agent team; the report template in `eb/team/report-template.md` if the client has one.

## Outputs
`eb/work/eb-metrics-report/<period>.md`: key numbers with change and source, highlights, risks, decisions needed.

## Human checkpoint
The EB lead edits and sends the report.

## Suggested ritual
Monthly or quarterly CHRO meeting.

## Metrics
Time to assemble the report; questions from the CHRO that the report did not answer.

## Risks and limits
No number without a source; missing data is shown as missing, not estimated.
