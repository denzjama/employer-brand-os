---
id: talent-competitor-watch
domain: research
name: Talent competitor watch
name_ru: Конкуренты за таланты
default_autonomy: L2
external_facing: false
---

## Purpose
Tracks what the employers the client competes with for talent publicly say and do: their EVPs, careers pages, campaigns, programmes, notable posts. Produces a digest of changes, not a ranking.

## Fits when
- The client names specific competitors for talent.
- The team checks competitors by hand or not at all.
- Leadership asks "what are others doing?".

## Triggers
Monthly schedule; on request before a campaign or an EVP review.

## Inputs
The competitor list in `eb/team/competitors.md`; public pages fetched from the web; previous digests in `eb/work/talent-competitor-watch/`.

## Outputs
`eb/work/talent-competitor-watch/<date>-digest.md`: what changed at each competitor, with links and dates, and what it could mean for the client, marked as interpretation.

## Human checkpoint
The owner reads the digest and decides what goes to the team or to leadership.

## Suggested ritual
First team meeting of the month: five minutes on the digest.

## Metrics
Digests delivered on time; number of items the team acted on.

## Risks and limits
Only public sources, each with a link and a fetch date. No claims about a competitor that the source does not state. No conclusions about "the market" from a handful of employers. Sites that block automated access are listed as not checked, never guessed.
