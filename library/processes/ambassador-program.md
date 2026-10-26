---
id: ambassador-program
domain: social
name: Ambassador programme support
name_ru: Амбассадорская программа
default_autonomy: L1
external_facing: true
---

## Purpose
Supports the employee ambassador programme: drafts answers to typical ambassador questions from an approved FAQ, prepares content kits and calendars for ambassadors, and summarises programme activity. The relationship with ambassadors stays with people.

## Fits when
- The company runs an ambassador programme and its coordinators answer the same questions again and again.
- Ambassadors ask for ready content or guidance on what they may post.

## Triggers
A batch of questions collected by the coordinator; the monthly content kit; on request.

## Inputs
The approved ambassador FAQ and rules in `eb/team/ambassador-guide.md`; `eb/brand-core/*`; anonymised question lists in `eb/inbox/ambassadors/`.

## Outputs
`eb/work/ambassador-program/<date>-answers.md`: draft answers to typical questions, marked with the FAQ item they rely on, and the questions that need a person; `eb/work/ambassador-program/<month>-kit.md`: content kit and calendar.

## Human checkpoint
The programme coordinator edits and sends every answer and kit.

## Suggested ritual
A weekly slot in which the coordinator works through the drafted answers.

## Metrics
Share of questions answered from the FAQ; time to answer; ambassador posts that used the kit.

## Risks and limits
Works only on anonymised question lists: names, contacts and personal details of ambassadors never enter the workspace. Never contacts ambassadors. Questions outside the FAQ go to a person, not to an improvised answer.
