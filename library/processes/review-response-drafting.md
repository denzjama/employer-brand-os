---
id: review-response-drafting
domain: reputation
name: Review response drafting
name_ru: Черновики ответов на отзывы
default_autonomy: L1
external_facing: true
---

## Purpose
Drafts responses to employer reviews in the brand voice, using only confirmed facts. Each draft says what it is based on and what the responder must check before posting.

## Fits when
- The company answers reviews, or wants to start.
- Responses are slow, templated or inconsistent between responders.

## Triggers
The "needs reaction" list from review monitoring; on request for a specific review.

## Inputs
The review text; `eb/brand-core/voice.md`, `facts.md`, `red-lines.md`; the response policy in `eb/team/response-policy.md` if the client has one.

## Outputs
`eb/work/review-response-drafting/<date>-<source>.md`: one draft per review, the facts used with their status, questions to check with the business before posting.

## Human checkpoint
A person edits, approves and posts every response. Responses to legal, safety or discrimination complaints go to the EB lead and are not drafted without their go-ahead.

## Suggested ritual
Right after the Monday digest: the owner works through the drafts.

## Metrics
Time to response; share of drafts posted with minor edits; the owner's edit notes (fuel for the retro).

## Risks and limits
Never argues with the reviewer, never discloses information about a person, never promises anything the facts do not support. Passes the quality gate before reaching the owner.
