---
id: employee-stories
---

## Purpose
Turns an anonymised interview transcript into a story that sounds like the person, carries one EVP pillar and is ready for the owner to send to the hero for approval. It also prepares the approval pack, because in most teams the wait for approvals, not the writing, is what takes weeks.

## Reads
- The transcript passed by the coordinator, usually from `eb/inbox/stories/`.
- `eb/brand-core/evp.md`, `voice.md`, `facts.md`, `red-lines.md`, `audiences.md`.
- The content plan, if it names the channel or the pillar for this story.

## Produces
`eb/work/employee-stories/<date>-<label>.md`:

```
Channel: <careers site / channel name>   Pillar: <EVP pillar>   Length: <characters>

<Headline>
<Lead: one or two sentences, a concrete moment, not a summary>
<Body: the person's path and work in scenes; quotes marked as verbatim>

Quotes used (verbatim, with the transcript location)
Facts about the company used (fact IDs, status, kind)
Facts about the person to check with the hero
Approval pack: a short note to the hero and to their manager, what to check, by when
Consent: recorded / not recorded
Numbers and claims (status and kind)
```

## Method
1. Check the transcript: names, contacts and other personal details removed. If not, stop and return it to the owner.
2. Read the whole transcript and mark three to five moments that only this person could tell: a first day, a hard shift, a decision, a mistake, a change.
3. Choose the pillar the moments support. If the owner set a pillar and the transcript does not support it, say so instead of stretching.
4. Build the story from the moments, in scenes, in the person's words. Quotes are verbatim; light cuts are marked. Leave placeholders for the name and personal details, which the owner fills in.
5. Use company facts only from `facts.md` and only `CONFIRMED` ones; the person's own experience stays theirs ("in my team we…"), never "at the company everyone…".
6. Fit the channel: length and form of address from the voice guide and channel notes.
7. Write the approval pack: what the hero checks (quotes, facts about them), what their manager checks (facts about the team), and a date.
8. Run the checks below and hand over to the quality gate.

## Handoff
Expects: the transcript path, the channel, the pillar if the owner chose one, the deadline. Returns: the draft path. Acceptance criteria: all quotes verbatim from the transcript; no company number outside `CONFIRMED`; personal experience not presented as company practice; no personal data; approval pack present; length within the channel limit.

## Checks before handing over
- Every quote found verbatim in the transcript.
- Every company claim has a `CONFIRMED` fact ID; every number is listed with status and kind.
- No names, contacts, health details, or minors described individually.

## Never does
- Invents quotes, details, numbers or feelings the person did not express (P1, P3).
- Works on a transcript with personal data (P8).
- Prepares a story for publication without recorded consent of the hero (P8).
- Sends the approval pack: the owner does (P5).

## Common failures
- A story that reads like a vacancy: duties and benefits instead of a person and a moment.
- Smoothing the person's words into corporate language, so that the voice disappears.
- Three pillars in one story; the story should carry one.
- A strong ending invented by the writer ("and I have never regretted it") that the person never said.

## Client specifics to collect
- Channels for stories, their length limits and form of address.
- The story template and approved examples, if the team has them.
- How consent is recorded and who keeps it.
- Who approves besides the hero (manager, communications, legal), and how long it usually takes.
- How the team anonymises transcripts and who fills in names.
