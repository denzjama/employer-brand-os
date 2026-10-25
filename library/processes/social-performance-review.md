---
id: social-performance-review
domain: social
name: Social performance review
name_ru: Разбор эффективности соцсетей
default_autonomy: L2
external_facing: false
---

## Purpose
Reads channel statistics and turns them into a short review: what worked, what did not, which pillars and formats drive reach and engagement, what to try next. Feeds the content plan.

## Fits when
- The team runs channels and collects statistics but rarely draws conclusions from them.

## Triggers
Monthly; on request after a campaign.

## Inputs
Statistics exports in `eb/inbox/stats/`; the content plan; previous reviews.

## Outputs
`eb/work/social-performance-review/<month>.md`: top and bottom items with numbers, patterns by pillar and format, three suggestions marked as hypotheses.

## Human checkpoint
The owner decides which suggestions go into the next plan.

## Suggested ritual
Monthly planning meeting, before the plan draft.

## Metrics
Reviews delivered; suggestions tested; trend of the team's chosen channel metric.

## Risks and limits
No conclusions from samples too small to carry them; says so. No benchmarks against "the market" without supplied data.
