---
id: periodic-report
name: Report for the CHRO
name_ru: Отчёт для HR-директора
agents: eb-metrics-report
external_facing: false
---

## Purpose
The monthly or quarterly report of the function for the CHRO, every number with its source and kind, ready a week before the meeting.

## Fits when
- The function reports to the CHRO or leadership regularly.
- The report is assembled by hand from several sources each time.

## Trigger
A week before the CHRO meeting.

## Steps

| From | To | What |
|---|---|---|
| lead | coordinator | Period, meeting date, new data |
| coordinator | eb-metrics-report | Task in the handoff format |
| log | eb-metrics-report | Runs and decisions of the period |
| brand-core | eb-metrics-report | Confirmed results and targets |
| eb-metrics-report | lead | Draft report and missing data |
| lead | log | Decision and reason |

## Decision
The EB lead edits and sends the report.

## Variants
- When the report also goes to leadership outside HR, add the quality gate before the lead.

## Risks and limits
No number without a source; missing data is shown as missing. Time saved by agents only as owners reported it.
