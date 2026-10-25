---
id: employee-stories
domain: content
name: Employee stories
name_ru: Истории сотрудников
default_autonomy: L1
external_facing: true
---

## Purpose
Turns an interview with an employee (transcript, notes or recording transcript) into a story for the careers site or social channels. The story keeps the person's words and facts, carries one EVP pillar, and adds nothing the person did not say.

## Fits when
- The team publishes employee stories or wants to.
- Interviews are recorded but stories take weeks to appear.
- Stories read alike, or drift from the EVP.

## Triggers
A transcript placed in `eb/inbox/stories/`; on request.

## Inputs
The transcript; `eb/brand-core/evp.md`, `voice.md`, `facts.md`; the content plan, if it names a pillar or a channel.

## Outputs
`eb/work/employee-stories/<date>-<slug>.md`: the story, the pillar it supports, quotes marked as verbatim, a list of facts to check with the employee, consent status.

## Human checkpoint
The owner edits; the employee approves the final text before publication. Without recorded consent the story is not published.

## Suggested ritual
Weekly content review.

## Metrics
Time from interview to approved story; edits needed; stories published per pillar.

## Risks and limits
No invented quotes, numbers or details. A personal experience never becomes company policy in the text. Passes the quality gate.
