---
id: project-brief
name: Project brief
name_ru: Бриф проекта
agents: project-briefs, quality-gate
external_facing: true
---

## Purpose
From an approved idea or a business request to a brief an agency or contractor can work from, with the open questions for the requester.

## Fits when
- The team works with agencies or contractors.
- Briefs are written from scratch each time, skipped, or come back with rounds of questions.

## Trigger
A project is approved, or the business brings a request.

## Steps

| From | To | What |
|---|---|---|
| owner | coordinator | Request, requester, deadline |
| coordinator | project-briefs | Task in the handoff format |
| brand-core | project-briefs | EVP, audiences, confirmed facts, red lines |
| project-briefs | quality-gate | Brief and open questions |
| quality-gate | owner | Brief with the check |
| owner | log | Decision and reason |

## Decision
The owner approves the brief, takes the open questions to the requester, and sends the brief to the agency.

## Variants
- With a design-production or contractor-operations agent in the team, the approved brief goes on to it.
- An internal brief for the team itself may skip the quality gate if the owner decides so in the roster.

## Risks and limits
No budget, date or audience size is invented; gaps are questions. The brief carries only confirmed facts, because an agency will repeat them in public.
