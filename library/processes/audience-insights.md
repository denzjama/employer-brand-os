---
id: audience-insights
domain: strategy
name: Audience insights
name_ru: Инсайты по аудиториям
default_autonomy: L1
external_facing: false
---

## Purpose
Turns the research the function already has (surveys, interviews, funnel data, recruiter notes) into short, sourced profiles of target audiences: what they value, what they doubt, which channels reach them. Every statement in a profile points to the data behind it.

## Fits when
- The function hires for several distinct audiences (for example engineers, students, blue-collar staff).
- Research exists but is spread across reports nobody rereads.
- Campaigns are planned "for everyone".

## Triggers
On request; when new research lands in `eb/inbox/`; before campaign planning.

## Inputs
Research reports, survey results, interview transcripts and funnel exports in `eb/inbox/`; `eb/brand-core/audiences.md`.

## Outputs
Proposed updates to `eb/brand-core/audiences.md`; `eb/work/audience-insights/<audience>.md` with the profile, its sources and its gaps.

## Human checkpoint
The owner approves profile changes before they enter the core.

## Suggested ritual
Before each quarterly planning session.

## Metrics
Number of audiences with a sourced profile; share of profile statements with a source; whether campaign briefs reference a profile.

## Risks and limits
No statements about a population without data from that population. No stereotypes by age, gender or origin. Small samples are labelled as small.
