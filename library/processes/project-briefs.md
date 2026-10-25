---
id: project-briefs
domain: creative
name: Project and event briefs
name_ru: Брифы проектов и событий
default_autonomy: L1
external_facing: false
---

## Purpose
Turns an approved idea or a request from the business (an event, a student programme, a hackathon, a campaign) into a brief for the team, an agency or a contractor: goal, audience, message, proof, deliverables, timeline, metrics, constraints.

## Fits when
- The team works with agencies or contractors.
- Briefs are written from scratch each time, or skipped.

## Triggers
On request.

## Inputs
The idea or request; `eb/brand-core/*`; the client's brief template, if any, in `eb/team/brief-template.md`.

## Outputs
`eb/work/project-briefs/<date>-<slug>.md`: the brief and a list of open questions for the requester.

## Human checkpoint
The project owner approves the brief before it goes to an agency.

## Suggested ritual
At the moment a project is approved; reviewed at the next team meeting.

## Metrics
Time to brief; rounds of agency questions.

## Risks and limits
No budget or timeline invented; missing ones are listed as questions.
