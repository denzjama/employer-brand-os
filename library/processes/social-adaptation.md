---
id: social-adaptation
domain: social
name: Channel adaptation
name_ru: Адаптация под каналы
default_autonomy: L1
external_facing: true
---

## Purpose
Takes one approved piece (a story, an announcement, a project) and drafts versions for each channel the team runs: Telegram, VK, Habr, LinkedIn later. Each version respects the channel's format and the brand voice and keeps the facts of the original.

## Fits when
- The team runs three or more channels.
- The same content is rewritten by hand for each channel, or posted unchanged everywhere.

## Triggers
A piece marked approved in `eb/work/`; on request.

## Inputs
The approved piece; `eb/brand-core/voice.md`; channel notes in `eb/team/channels.md` (audience, format, length, what works).

## Outputs
`eb/work/social-adaptation/<date>-<slug>.md`: one draft per channel with notes on what changed and why.

## Human checkpoint
The channel owner edits and posts each version.

## Suggested ritual
Weekly content review, together with new stories.

## Metrics
Time from approved piece to channel-ready drafts; edits needed per channel.

## Risks and limits
Never adds facts absent from the original. Does not post. Passes the quality gate.
