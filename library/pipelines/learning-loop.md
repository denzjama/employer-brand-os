---
id: learning-loop
name: Learning loop
name_ru: Петля обучения
agents: adoption-coach
external_facing: false
---

## Purpose
Shows how people's decisions on agent outputs reach the retro: the coach reads the week's runs and decisions, brings the pulse to the weekly meeting, and what the team says becomes proposals for changing the agents.

## Fits when
Always: the adoption coach is in every first wave, and the diagnosis requires one pipeline that shows this loop.

## Trigger
The weekly team meeting.

## Steps

| From | To | What |
|---|---|---|
| log | adoption-coach | Runs and decisions of the week |
| adoption-coach | lead | Pulse and the plan for the 15 minutes |
| lead | owner | Questions for the owners at the meeting |
| owner | lead | What helped, what got in the way |
| lead | log | Proposals for the retro |

## Decision
The EB lead decides which concerns become proposals for the retro. Changes to agents are made only through an approved proposal.

## Variants
- Owners without access answer through their operators; their answers are attributed to the owner's role.

## Risks and limits
Nobody is named or ranked. Silence is not acceptance. Time saved only as owners reported it.
