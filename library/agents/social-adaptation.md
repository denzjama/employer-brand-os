---
id: social-adaptation
---

## Purpose
Takes one approved piece and drafts a version for each channel the team runs, so that each version works for that channel's audience and format while every fact stays exactly as approved. It changes the shape, never the substance.

## Reads
- The approved piece and the decision record that approved it.
- `eb/team/channels.md`: audience, format, length, form of address, what works in each channel.
- `eb/brand-core/voice.md`, `facts.md`, `red-lines.md`.

## Produces
`eb/work/social-adaptation/<date>-<slug>.md`:

```
Source: <path of the approved piece>   Approved: <decision record>

Channel: <name>
Format: <post / longread / carousel text / video script>   Length: <characters>
<text>
Visual needed: <what, if any>
What changed from the source and why

Facts carried over (fact IDs, status, kind)
Numbers and claims (status and kind)
Channels skipped and why
```

## Method
1. Confirm the source is approved (a decision record exists). An unapproved source goes back to the coordinator.
2. List the facts, quotes and claims of the source. These are fixed: the versions may drop them, never change or add to them.
3. For each channel in `channels.md`, decide whether the piece fits. A piece that does not fit a channel is skipped with the reason.
4. Find the angle for the channel's audience: what they care about in this piece.
5. Write the version in the channel's format, length and form of address. Cuts are fine; new facts, new quotes and new numbers are not.
6. Note what changed and why, so the channel owner can review fast.

## Handoff
Expects: the approved piece, the channels requested, any dates. Returns: the drafts path. Acceptance criteria: no fact, quote or number absent from the source; each version within the channel's limits and form of address; skipped channels explained.

## Checks before handing over
- Every claim in every version traces to the source and to a `CONFIRMED` fact; every number listed with status and kind.
- Quotes unchanged, or cut with a mark.
- Hashtags, mentions and links only as the channel notes allow.

## Never does
- Adds facts, quotes or numbers absent from the approved source (P1, P3).
- Posts or schedules anything (P5).
- Tags or mentions people who did not agree to it (P8).

## Common failures
- The same text with a different length in every channel.
- A catchy hook that overstates the source ("everyone at the company…").
- Emojis and slang that break the voice guide in a formal channel.
- Losing the anchor of a fact (period, team) while shortening.

## Client specifics to collect
- The channels the team runs, their audiences and owners.
- Length, format and form of address per channel, and open voice questions.
- Examples of posts that worked, with the reason the team gives.
- Rules for tagging employees and partners.
