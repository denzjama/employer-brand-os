---
id: review-monitoring
domain: reputation
name: Review and mention monitoring
name_ru: Мониторинг отзывов и упоминаний
default_autonomy: L2
external_facing: false
---

## Purpose
Collects new employer reviews and mentions (hh.ru, Dream Job, Habr Career, Telegram channels, media), groups them by theme and tone, and flags the ones that need a reaction: reputational risk, a factual error, a question that deserves an answer.

## Fits when
- The company has employer reviews on public platforms.
- The team checks them by hand, irregularly, or only when something blows up.
- Leadership asks for a reputation picture.

## Triggers
Weekly schedule; on request when something is happening.

## Inputs
In the MVP: exports or copies of reviews placed in `eb/inbox/reviews/`, and public pages fetched from the web. Later: platform connectors. Previous digests for comparison.

## Outputs
`eb/work/review-monitoring/<date>-digest.md`: new items by source, themes with counts, change against the previous period, a "needs reaction" list with the reason for each.

## Human checkpoint
The owner decides which items need a response and who handles them. Risk items go to the EB lead the same day.

## Suggested ritual
Monday digest at the team meeting.

## Metrics
Coverage (sources checked out of sources listed); time from review to reaction; share of reviews answered.

## Risks and limits
Never contacts reviewers. Never guesses who wrote a review. Sources that could not be read are reported as not checked. Personal data in reviews is not copied into digests.
