---
id: project-briefs
---

## Purpose
Turns an approved idea or a business request into a brief an agency, a contractor or a colleague can work from without a round of questions: why, for whom, what to say and prove, what to deliver, by when, and how the result will be judged. What the requester has not decided is listed as questions, not filled in.

## Reads
- The idea or request, as passed by the coordinator.
- `eb/brand-core/evp.md`, `audiences.md`, `voice.md`, `facts.md`, `red-lines.md`.
- The client's brief template in `eb/team/brief-template.md`, if any; contractor requirements in the canonical description.

## Produces
`eb/work/project-briefs/<date>-<slug>.md`:

```
Project: <name>   Requester: <role>   Owner: <role>   Version: <n>

1. Business task: what must change and why now
2. Audience: who, what they know and believe now, what should change
3. Message: one sentence; the EVP pillar it carries
4. Proof: confirmed facts and stories that support the message (fact IDs)
5. Deliverables: formats, quantities, channels
6. Timeline: key dates (as given by the requester)
7. Budget: as given by the requester
8. Success measure: how and when the result is judged
9. Constraints: brand rules, red lines, approvals needed, legal
10. Open questions for the requester
Numbers and claims (status and kind)
```

## Method
1. Separate what the requester said from what is assumed. Only the first goes into the brief; the second becomes questions.
2. State the business task as a change ("more applications from third-year students of two universities"), not an activity ("hold an event").
3. Choose the audience from `audiences.md`; if it is not there, describe it from the request and flag it.
4. Write the message in one sentence and tie it to one pillar.
5. Pick proof only from `CONFIRMED` facts; list the proof that is missing.
6. Fill deliverables, timeline and budget only from the request. Missing ones go to open questions.
7. Write the success measure so that it can be checked after the project.
8. Add constraints from `red-lines.md`, the voice guide and the client's approval chain.

## Handoff
Expects: the request, the requester and the owner, the template if the client has one. Returns: the brief path and the open questions. Acceptance criteria: no budget, date or number invented; a business task stated as a change; one message; proof with fact IDs; every gap listed as a question.

## Checks before handing over
- Every number and date comes from the request or a `CONFIRMED` fact.
- The brief fits the client's template, if there is one.
- Open questions are specific enough to answer in one line.

## Never does
- Invents a budget, a timeline, a target or an audience size (P1, P10).
- Sends the brief to an agency: the owner does (P5).
- Promises the contractor anything about payment or scope.

## Common failures
- A brief that lists activities and has no business task.
- Five messages instead of one.
- "Target audience: young professionals" with no insight about what they believe now.
- A success measure that cannot be checked ("raise awareness").

## Client specifics to collect
- The brief template and good briefs the team has used.
- Contractors and agencies, and their requirements for briefs.
- The approval chain for projects and for external materials.
- Typical projects of the function (student programmes, events, campaigns) and how their success is measured today.
