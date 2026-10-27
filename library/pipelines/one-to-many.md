---
id: one-to-many
name: One piece to all channels
name_ru: Один материал — во все каналы
agents: social-adaptation, quality-gate
external_facing: true
---

## Purpose
From one approved piece to versions for every channel the team runs, each ready for its channel owner.

## Fits when
- The team runs three or more channels.
- The same piece is rewritten by hand for each channel, or posted unchanged everywhere.

## Trigger
A piece is accepted (a decision record exists): a story, an announcement, a project result.

## Steps

| From | To | What |
|---|---|---|
| owner | coordinator | Accepted piece and the channels |
| coordinator | social-adaptation | Task in the handoff format |
| brand-core | social-adaptation | Voice, channel notes, confirmed facts |
| social-adaptation | quality-gate | Channel versions |
| quality-gate | owner | Versions with the check |
| owner | log | Decision and reason per channel |

## Decision
Each channel owner edits and posts their version.

## Variants
- Chained after the employee-story pipeline once the hero has approved the story.
- Different channel owners: the coordinator splits the versions and each owner records a decision.

## Risks and limits
The versions change shape, never substance: no new facts, quotes or numbers. An unapproved source is returned.
