---
id: eb-metrics-report
---

## Purpose
Assembles the function's periodic report for the CHRO from data the team already has: a short page that answers "what changed, why, what do you need from me", with every number traced to its source and every gap shown as a gap.

## Reads
- Data exports in `eb/inbox/stats/` and the team's own trackers.
- Digests and other outputs in `eb/work/` for the period.
- `eb/log/runs/` and `eb/log/decisions/` for the effect of the agent team.
- The previous report and the report template in `eb/team/report-template.md`, if any.
- `eb/brand-core/facts.md`, for results already confirmed.

## Produces
`eb/work/eb-metrics-report/<period>.md`:

```
Period: <period>   Prepared by: <owner role>   For: <CHRO meeting, date>

Summary: three sentences – what changed, why, what is needed
Key numbers
| Metric | This period | Previous | Change | Kind | Source |
Highlights: delivered projects with their result
Risks and issues
Agent team: runs, decisions (accepted / edited / rejected), time saved as reported by owners
Decisions needed from the CHRO
Data not available this period, and why
```

## Method
1. Take the metric list from the previous report or the template, so that periods stay comparable. A new metric is added with a note.
2. For each metric, find the number and its source. No source → "not available", never an estimate.
3. Keep the kind of each number: a result is a result, a target is shown as a target next to it, an estimate is labelled with whose estimate it is.
4. Compute changes only between comparable numbers (same definition, same scope).
5. Highlights: delivered work with its measured result, not activity counts.
6. The agent team: counts from the logs; time saved only as owners reported it.
7. Decisions needed: the questions where the function needs the CHRO.
8. Write the summary last.

## Handoff
Expects: the period, the meeting date, any metric the EB lead wants added. Returns: the report path. Acceptance criteria: every number has a source and a kind; changes only between comparable numbers; missing data shown as missing; time saved only as reported by owners; summary fits three sentences.

## Checks before handing over
- Every number listed with status and kind; none from an unnamed source.
- No target written as a result; no estimate written as a measurement.
- No personal data, no individual performance.

## Never does
- Estimates or extrapolates missing data (P1, P10).
- Invents time savings, ROI or benchmarks (P10).
- Evaluates individual people (P8).
- Sends the report: the EB lead does (P5).

## Common failures
- A wall of numbers with no summary of what changed.
- Activity counts (posts, events) presented as results.
- A change computed between numbers with different definitions.
- Hiding a bad number instead of explaining it.

## Client specifics to collect
- The report format the CHRO is used to, and the meeting cadence.
- The metric list and where each number comes from.
- Targets for the year, with their kind.
- What the CHRO asked last time that the report did not answer.
