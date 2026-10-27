---
id: employee-story
name: Employee story
name_ru: История сотрудника
agents: employee-stories, quality-gate
external_facing: true
---

## Purpose
From an interview transcript to a story draft that the owner can send to the hero for approval, with the approval pack ready.

## Fits when
- The team publishes or wants to publish employee stories.
- Stories take weeks, mostly waiting for approvals.

## Trigger
The owner brings an anonymised transcript.

## Steps

| From | To | What |
|---|---|---|
| owner | coordinator | Anonymised transcript, channel, deadline |
| coordinator | employee-stories | Task in the handoff format |
| brand-core | employee-stories | Voice, EVP pillars, confirmed facts |
| employee-stories | quality-gate | Draft, approval pack, list of numbers |
| quality-gate | owner | Draft with the check |
| owner | log | Decision and reason |

## Decision
The owner accepts, edits or rejects the draft and sends the approval pack to the hero. Publication waits for the hero's consent, recorded by the owner.

## Variants
- After approval, the accepted story goes to the one-to-many pipeline for channel versions.
- An owner without access works through an operator; the draft reaches the owner as an exported document.

## Risks and limits
A transcript with personal data stops at the agent's first step. Quotes are checked against the transcript by the gate. The story is never published by the pipeline.
