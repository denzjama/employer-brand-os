---
id: recruitment-campaigns
domain: campaigns
name: Recruitment campaigns
name_ru: Кампании под рекрутмент
default_autonomy: L1
external_facing: true
---

## Purpose
Prepares digital campaigns that promote recruitment activities (hiring events, programmes, hard-to-fill role families): campaign brief, text and creative variants by channel, targeting and tracking parameters, and the report after the campaign. Writing the job ads themselves is not part of this process.

## Fits when
- The team runs several recruitment campaigns a month by a similar scheme.
- Campaign set-up and reporting take more time than the decisions about them.

## Triggers
A request from talent acquisition or a planned activity in the content plan; the end of a campaign for the report.

## Inputs
The request and its goal; `eb/brand-core/*`; audience profiles; previous campaign reports in `eb/work/recruitment-campaigns/`; statistics exports in `eb/inbox/stats/`.

## Outputs
`eb/work/recruitment-campaigns/<date>-<slug>.md`: brief, text variants per channel, requests for creatives, targeting parameters as a proposal, tracking links scheme; after the campaign, a report with numbers from the export and their source.

## Human checkpoint
The campaign owner approves the brief and the variants and launches the campaign in the ad accounts. The agent has no access to ad accounts.

## Suggested ritual
The weekly sync with talent acquisition: new requests in, reports out.

## Metrics
Time from request to campaign-ready package; campaign results as reported by the platform, compared with the team's previous campaigns.

## Risks and limits
Never sets budgets or launches campaigns. Targeting proposals must not discriminate by age, gender, origin or any protected characteristic. Passes the quality gate.
