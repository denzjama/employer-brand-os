---
id: design-production
domain: content
name: Design production
name_ru: Дизайн-продакшн
default_autonomy: L1
external_facing: true
---

## Purpose
Takes the repetitive part of design work off the design team: adaptations of an approved master layout to other formats and sizes, presentation drafts in the brand template, and production specifications (formats, texts per format, file names, deadlines). Creative concepts and art direction stay with designers.

## Fits when
- Designers spend a large share of their time on adaptations, resizes and presentation layout rather than on concepts.
- Requests to the design team arrive from several teams with incomplete specifications.
- The team has a brand template and master layouts that adaptations follow.

## Triggers
A request from another agent or a person with an approved master layout or brief; the weekly review of design requests.

## Inputs
The master layout or source presentation; the brand template and visual rules in `eb/team/visual-guide.md` if the client has them; texts from the brief, with their facts from `eb/brand-core/facts.md`.

## Outputs
`eb/work/design-production/<date>-<slug>/`: adapted layouts or presentation drafts where the tools can produce them, otherwise a production specification per format; a list of what was changed and what the designer must check.

## Human checkpoint
A designer reviews every adaptation and draft before it goes to a requester or a contractor.

## Suggested ritual
The weekly review of design requests: the agent prepares the queue with specifications; designers pick up the creative part.

## Metrics
Hours designers spend on adaptations and layout, as they report it; rounds of corrections per request.

## Risks and limits
Never creates a new key visual or changes the visual identity. Texts on layouts use only CONFIRMED facts. Passes the quality gate, including its visual check, before anything leaves the team.
